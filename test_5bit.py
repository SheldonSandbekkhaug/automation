#!/usr/bin/env python

""" A tool to test 5bit, a C encryption program.

Author: Sheldon Sandbekkhaug
Written September 2013

Use this script at your own risk. It is only intended to work on Unix
systems, and is not guaranteed to be 100% accurate (though I hope it is!).

See README.md for usage and more information.

"""


import os
import shlex
import argparse
import tempfile
import subprocess


program_to_test = "5bit.c" # Source code file
binary_name = "5bit"


def main():
    """ Get args from the command line and run the tests. """
    args = parse_args() # Get arguments from command line
    path = args.filepath
    path = os.path.expanduser(path) # Expand "~"

    # Compile the program to be tested
    compile_command = "gcc " + program_to_test + " -o " + binary_name
    subprocess.call(shlex.split(compile_command))

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
    enc_file, enc_file_path = tempfile.mkstemp()

    # Temporary file that will hold decoded data
    dec_file, dec_file_path = tempfile.mkstemp()

    # Run the program and store the results in enc_file
    encode_command = binary_name + " " + filepath
    subprocess.call(shlex.split(encode_command), stdout=enc_file)

    # Decode enc_file using the program and store the results in dec_file
    decode_command = binary_name + " -d " + enc_file_path
    subprocess.call(shlex.split(decode_command), stdout=dec_file)
    
    # Compare the decoded and original files
    compare_command = "cmp " + filepath + " " + dec_file_path

    # Check the return code of the comparison
    try:
        subprocess.check_call(shlex.split(compare_command))
    except subprocess.CalledProcessError:
        print("File FAILED: " + filepath)
    else:
        # Don't print anything if we're quiet
        if quiet:
            pass
        else:
            print("FILE OK: " + filepath)

    # Remove the temporary files since we're done with them
    os.remove(enc_file_path)
    os.remove(dec_file_path)


main()
