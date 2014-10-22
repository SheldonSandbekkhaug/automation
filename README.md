This repository, automation, holds a few scripts I've written to automate things, especially testing.

encryption_testing holds a Python script (test_5bit.py) to test encryption programs. The script feeds the encryption program (e.g. '5bit') a file to encrypt and stores the result in a temporary file. Next, the script decrypts the temporary file. Finally, the script compares the decrypted file to the original. This is done for every file in the user-specified directory and subdirectories.

lexer_testing holds a Python script that tests lexers written for the L programming language. It runs a "newer" lexer and a "reference" lexer and compares the output. This allows you to compare functionality between two versions and check if anything broke. Like test_5bit, the lexer is tested against all files in the specified directory.

parser_testing holds several scripts. The first is a Python script that functions in the same way as the lexer tester. The script writeProgram.py automatically generates random programs of arbitrary length in the L programming language (it does not use all the language constructs). The shell script generateTests.sh runs writeProgram.py, stores the result in a file, and runs testParser.py on the newly-generated file. The shell script does this an arbitrary number of times.

Most scripts follow the same usage format:

First place the script(s) in the same location as your executable. Then run the script (e.g. test_5bit) with:

./test_5bit.py -f path/to/directory/to/test/against

Let's say test_5bit is in ~/cs/429/
If I wanted to test the directory ~/cs/429/testfiles/ I would type:

./test_5bit.py -f testfiles

If I wanted to test the directory ~/history I could type either of these:

./test_5bit.py -f ../../history
./test_5bit.py -f ~/history
