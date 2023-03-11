##########################################################################
# 
# msa_sp_score.py 
#
# Computes the sum-of-pairs score of an MSA stored in FASTA format using
# a specific score-matrix and gapcost cf. mandatory project 3 in AiB.
#
# Christian Storm Pedersen, 21-sep-2009
#
##########################################################################

import os
import sys
import string

##########################################################################
# Usage
##########################################################################

def print_usage():
	print """
Usage: msa_sp_score.py <filename>

where <filename> contains a multiple sequence alignment over the alphabet
{a,c,g,t,-} in FASTA format.
"""

##########################################################################
# Cost parameters and helper functions
##########################################################################

cost = [[0, 5, 2, 5, 5],  # A
        [5, 0, 5, 2, 5],  # C
        [2, 5, 0, 5, 5],  # G
        [5, 2, 5, 0, 5],  # T
        [5, 5, 5, 5, 0]]  #-'

dict_str2seq = {'a':0, 'c':1, 'g':2, 't':3, 'A':0, 'C':1, 'G':2, 'T':3, '-':4, 'N':0, 'R':0, 'S':0}

def str2seq(s):
    try:
        seq = map(lambda c : dict_str2seq[c], list(s))
        return seq
    except KeyError, h:
        print "ERROR: Illegal character", h, "in input string."
        sys.exit(1)

###########################################################################
# read_fasta(filename)
#
# Returns an array of strings. The strings correspond to the strings
# defined in the FASTA file 'filename' with whitespaces removed.
###########################################################################

def read_fasta(filename):
	f = open(filename)
	res = []
	curr_str = ""
	curr_name = ""
	for l in f.readlines():
		l = string.strip(l)
		# Ignore empty lines
		if len(l) == 0:
			continue
		# Ignore comment lines
		elif l[0] == ';':
			continue
		# A new string starts when a new name is found
		elif l[0] == '>':
			if curr_name != "":
				res.append(remove_whitespaces(curr_str))
			curr_str = ""
			curr_name = l[1:].strip()
		# Otherwise append current line to the current string
		else:
			curr_str = curr_str + l
	res.append(remove_whitespaces(curr_str))
	return res

def remove_whitespaces(s):
	return string.join(s.split(), "")
	
###########################################################################
# compute_sp_score(filename)
#
# Returns the sp-score of the MSA stored in the FASTA file 'filename'
###########################################################################

def compute_sp_score(filename):	
	# Read FASTA file and convert input strings to sequences
	row = []
	for s in read_fasta(filename):
		row.append(str2seq(s))
	# Compute the score of each induced pairwise alignment
	score = 0
	for i in range(len(row)):
		for j in range(i+1, len(row)):
			if len(row[i]) != len(row[j]):
				print "ERROR: Rows", i, "and", j, "have different lengths."
				sys.exit(1)
			for c in range(len(row[i])):
				score = score + cost[row[i][c]][row[j][c]]
	return score

if __name__ == '__main__':

	if len(sys.argv) != 2:
		print_usage()
		sys.exit(1)
	try:
		print compute_sp_score(sys.argv[1])
	except IOError:
		print "ERROR: Cannot open input file %s" % (sys.argv[1])
		sys.exit(1)
