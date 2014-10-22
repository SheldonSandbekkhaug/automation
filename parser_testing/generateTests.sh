#!/bin/bash
# Hacky script to automate running of writeProgram.py
# Also tests the parser on those newly-created L-programs

mkdir -p TestCases/GeneratedTests
c=1
while [ $c -le 100 ]
do
  ./writeProgram.py > TestCases/GeneratedTests/$c.txt
  ./testParser.py -f TestCases/GeneratedTests/$c.txt
  (( c++ ))
done
