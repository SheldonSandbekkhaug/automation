Follow these instructions to test your 5bit program on a Unix/Linux system.
test_5bit.py might work on other operating systems, but no guarantees are
made.

Copy your 5bit.c source code to the same directory that this README resides
in. Pick a directory that you wish to test your 5bit program against. Let's
say you want to test 5bit against ~/cs429/homework/

Enter the following in the command line:

./test_5bit -f ~/cs429/homework/

This will encode and decode every file in ~/cs429/homework/ and compare the
results with the original.

Please note that while I hope that the results will be accurate, I (Sheldon
Sandbekkhaug) cannot guarantee this script will produce correct results
100% of the time. Use this program at your own risk!
