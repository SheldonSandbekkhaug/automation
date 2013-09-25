Use these files to test your encoding and decoding.
Compare results with:

cmp original_file new_file

If the two files are identical, nothing will be printed. If they are
different, the number of the first byte where they differ will be printed.

For example, to check if fox.5b was decoded correctly, you could type:
5bit -d fox.5b > fox_decoded.txt
cmp fox.txt fox_decoded.txt
