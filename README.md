Author: Sheldon Sandbekkhaug

Written September 2013

test_5bit.py is a tool to test 5bit, a C encryption program. When given a file
or directory, test_5bit will encode each file, decode it, and compare
the result to the original.

Use this script at your own risk! It is only intended to work on Unix
systems, and is not guaranteed to be 100% accurate (though I hope it is!).

The script will also compile 5bit.c to the output binary "5bit".

Usage and examples:

First place this file in the same location as 5bit.c Then run this script with:

./test_5bit -f path/to/directory/to/test/against

Let's say test_5bit is in ~/cs/429/
If I wanted to test the directory ~/cs/429/testfiles/ I would type:

./test_5bit -f testfiles

If I wanted to test the directory ~/history I could type either of these::

./test_5bit -f ../../history
./test_5bit -f ~/history
