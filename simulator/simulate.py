"""
Run with form
simulate.py codefile configfile

configfile has the form:
	max_allowed_cycles: 
	
machine code files have one instruction per line. "comment" lines
are of the form
# mycomment
these are intended to be used for comments, but also for possible
chromosomal division of sorts.

The simulator reads in files and returns the 'hashes' generated by them.

"""

import sys

NUM_LINES =  65536
M_OPCODE = 15
M_Z = 65535 << 4
M_Y = M_Z << 16
M_X = M_Z << 16
M_DEST = M_X << 16

MAX_CYCLES = 50000
# B and C should ALWAYS be directly above A.
WI_INPUT_START #A) The index of the starting word the input will be dumped into every time the magic function is called.
WI_TOTAL_INPUT_SIZE = 10 #B) The index of the word the total size of the input is going to be dumped into every time the magic function is called 
WI_BLOCK_SIZE = 11#C) The index of the word the input's blocksize will be dumped into every time the magic function is called


class Program:
	def __init__(self, filename):
		
		fh = open(sys.argv[1], 'r')
		lines = fh.readlines()
		self.memory = [int(line) for line in lines if line[0] != '#']
		while len(memory) < NUM_LINES:
			memory.append(0)
	def next(self):
		return cycle_coun

fh = open(sys.argv[2], 'r')
lines = fh.readlines()
options = [line.split() for line in lines]
max_cycles = int(options[0][1])
fh.close()
