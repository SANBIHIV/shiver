#!/usr/bin/env python2
from __future__ import print_function

## Author: Chris Wymant, c.wymant@imperial.ac.uk
## Acknowledgement: I wrote this while funded by ERC Advanced Grant PBDR-339251
##
## Overview:
ExplanatoryMessage = '''This script removes those columns/positions in alignment
that are wholly 'blank', i.e. consist solely of the gap character "-". Output is
printed to stdout.'''

import argparse
import os
import sys
from Bio import AlignIO

# Define a function to check files exist, as a type for the argparse.
def File(MyFile):
  if not os.path.isfile(MyFile):
    raise argparse.ArgumentTypeError(MyFile+' does not exist or is not a file.')
  return MyFile

# Set up the arguments for this script
ExplanatoryMessage = ExplanatoryMessage.replace('\n', ' ').replace('  ', ' ')
parser = argparse.ArgumentParser(description=ExplanatoryMessage)
parser.add_argument('FastaFile', type=File)
parser.add_argument('-?', '--q-mark', action='store_true', help='''Also consider
the '?' character (assumed throughout Chris Wymant's code to mean missing
coverage) to be blank.''')
parser.add_argument('-U', '--uninformative', action='store_true', help='''Also
remove those columns in which all non-blank bases are all identical.''')
args = parser.parse_args()

# Are we checking just for "-", or also for "?"
BlankChars = '-'
if args.q_mark:
  BlankChars += '?'

alignment = AlignIO.read(args.FastaFile, "fasta")
AlignmentLength = alignment.get_alignment_length()
for column in reversed(xrange(AlignmentLength)):
  RemoveThisCol = True
  FirstBaseSeen = None
  for base in alignment[:, column]:
    if not base in BlankChars:
      if args.uninformative:
        if FirstBaseSeen == None:
          FirstBaseSeen = base
        elif base != FirstBaseSeen:
          RemoveThisCol = False
          break
      else:
        RemoveThisCol = False
        break
  if RemoveThisCol:
    alignment = alignment[:, :column] + alignment[:, column+1:]

AlignIO.write(alignment, sys.stdout, 'fasta')
