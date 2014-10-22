#!/usr/bin/env python

""" A tool to automate testing of an L-language parser. It compares the
output of your parser with the reference parser for every file in the
specified directory (and its subdirectories).

Before running, put l-interpreter (the reference interpreter) 
and your parser in this directory.

Usage:

./testParser.py -f DIRECTORY_OR_FILE

Use this script at your own risk. It is only intended to work on Unix
systems, and is not guaranteed to be 100% accurate (though I hope it is!).

See README.md for usage and more information.

"""


import os
import shlex
import argparse
import tempfile
import subprocess


binary_name = "parser"
correct_program = "l-interpreter -ast"

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
    decode_command = correct_program + " " + filepath
    subprocess.call(shlex.split(decode_command), stdout=their_output)

    # Temporary file for the AST
    ast_file, ast_file_path = tempfile.mkstemp()
    
    # Get the AST from the correct parser's output
    saw_stars = False
    with open(their_output_path, 'r') as parser_output:
      with open(ast_file_path, 'w') as ast_file_open:
        for line in parser_output:
          if (line == "*****************************************\n"):
            ast_file_open.write(line)
            saw_stars = True
           # Handle the "error case" discrepancy
          elif ("syntax error" in line):
              ast_file_open.write(line)
              ast_file_open.write("Parse result NULL\n")
          elif (saw_stars == False):
            ast_file_open.write(line)

    # Compare the decoded and original files
    compare_command = "cmp " + our_output_path + " " + ast_file_path

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
    os.remove(ast_file_path)


main()
