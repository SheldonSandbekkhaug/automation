#!/usr/bin/env python

""" Script that writes simple, random L-programs.

Usage:

./writeProgram.py > OUTPUT_FILENAME

"""

from random import *

import sys

ops = ["+", "-", "*", "/", "&", "|", "=", "<>", "<", "<=", ">", ">=", "@",]

MAX_NUMBER = sys.maxint

def main():
  sys.stdout.write(str(MAX_NUMBER) + ' + ')

  for x in range(0, 10):
    print(addExpression())
    sys.stdout.write(' ' + choice(ops) + " ")
  
  print(addExpression())

def addExpression():
  rand = randint(0,10)

  if (rand <= 2):
    return addIfThenElse()
  else:
    outputStr = ""
    outputStr += '(' + str(randint(0, MAX_NUMBER)) 
    outputStr +=  choice(ops) + " " 
    outputStr += str(randint(0, MAX_NUMBER)) + ')'
  return outputStr

def addIfThenElse():
  return ("if " + addExpression() +"then " + addExpression() +  " else\n" +
    addExpression())


main()   
