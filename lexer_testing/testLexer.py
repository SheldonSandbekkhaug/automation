#!/usr/bin/env python

""" A tool to automate testing of an L-language lexer. It compares the
output of your parser with the reference lexer for every file in the
specified directory (and its subdirectories).

Before running, put the reference lexer and your lexer in this directory.

Usage:

./testLexer.py -f DIRECTORY_OR_FILE

"""


import os
import shlex
import argparse
import tempfile
import subprocess


binary_name = "lexer"
correct_lexer = "correct_lexer"


def main():
    """ Get args from the command line and run the tests. """
    args = parse_args() # Get arguments from command line
    path = args.filepath
    path = os.path.expanduser(path) # Expand "~"

    if (os.path.isdir(path)):
        # Test each file in the directory recursively
        test_directory(path, args.quiet)
    else:
        # Test the one file
        test_file(path, args.quiet)


def parse_args():
    """ Parse the argmunts from the command line. """
    parser = argparse.ArgumentParser()

    # Get the file/directory to test the program on
    parser.add_argument("-f", "--filepath",
                        help="Relative or absolute path to file or " + \
                             "directory you wish to test against",
                        default="."
                       )
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Quiet output; Only print errors"
                       )

    return parser.parse_args()


def test_directory(path, quiet):
    """ Recursively test each file in the directory.
    path is an absolute path to the directory
    quiet is whether the output should be quiet (1) or not (0)

    """
    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            # Build the filepath to the file to test against
            filepath = os.path.join(dirname, filename)
            test_file(filepath, quiet)


def test_file(filepath, quiet):
    """ Test the program against one file. 
    filepath should be an absolute path to the file to be tested against.
    quiet is whether the output should be quiet (1) or not (0)

    """
    # Temporary file that will hold encoded data
    our_output, our_output_path = tempfile.mkstemp()

    # Temporary file that will hold decoded data
    their_output, their_output_path = tempfile.mkstemp()

    # Run the program and store the results in our_output
    encode_command = binary_name + " " + filepath
    subprocess.call(shlex.split(encode_command), stdout=our_output)


    # Decode our_output using the program and store the results in their_output
    decode_command = correct_lexer + " " + filepath
    subprocess.call(shlex.split(decode_command), stdout=their_output)
    
    # Compare the decoded and original files
    compare_command = "cmp " + our_output_path + " " + their_output_path

    # Check the return code of the comparison
    try:
        subprocess.check_call(shlex.split(compare_command))
    except subprocess.CalledProcessError:
        print("FILE FAILED: " + filepath)
    else:
        # Don't print anything if we're quiet
        if quiet:
            pass
        else:
            print("FILE OK: " + filepath)

    # Remove the temporary files since we're done with them
    os.remove(our_output_path)
    os.remove(their_output_path)


main()
