ENABLE_DEBUG = False

MAX_CYCLES = 50000

NUM_BITS = 68
NUM_WORDS = NUM_LINES =  2**15
MAX_WORD_SIZE = (2**NUM_BITS) - 1


"""Shifts to get fields"""
S_OPCODE = 0
S_X = 4
S_Y = 20
S_Z = 36
S_DEST = 52

"""Masks to get fields"""
M_OPCODE = 15
M_X = 65535 << 4
M_Y = M_X << 16
M_Z = M_Y << 16
M_DEST = M_Z << 16

"""Mask for the field val (everything that's not the immediate bit)"""
M_FVAL = NUM_WORDS - 1

"""MSDigit mask for fields"""
B_OPCODE = 8
B_X = 32768
B_Y = 32768
B_Z = 32768
B_DEST = 32768

"""Opcode values with shorthand"""
ops = opcodes = {
		"and": 0,
	  	"nand": 1,
		"xor": 2,
		"or": 3,
		"not": 4,
		"mod": 5,
		"add": 6,
		"cshift": 7,
		"shift": 8,
		"addifeq": 9,
		"addifneq": 10,
		"addiflt": 11,
		"setifeq": 12,
		"halt": 13,
		"setiflt": 14,
		"iterinput": 15}
		
dict_invert = lambda d: dict(zip(d.values(), d.keys()))
r_ops = dict_invert(ops)

IMM = 1

WORD_SIZE = NUM_BITS
BLOCK_SIZE = NUM_BITS
BLOCK_MASK = 2**BLOCK_SIZE - 1
NUM_INPUT_BLOCKS = 2 * 3 *  BLOCK_SIZE # Number of blocks a call to iterinput will start.
NUM_OUTPUT_BLOCKS = 2 
#WI is Word Index; aka the location in memory
WI_PROGRAM_COUNTER = 1 #Index in which the program counter is stored

WI_TOTAL_INPUT_SIZE = 12 #The index of the word the total size of the input is going to be dumped into every time every time iterinput is called
WI_BLOCK_SIZE = WI_TOTAL_INPUT_SIZE + 2 #Index of the word the block size for the input is going to be dumped into every time iterinput is called
WI_NUM_INPUT_BLOCKS = WI_BLOCK_SIZE + 2 #Index for number of blocks a call to iterinput will create
WI_INPUT_START = WI_NUM_INPUT_BLOCKS + 2 #Index of the word the input's going to start in
WI_INPUT_END = WI_INPUT_START + NUM_INPUT_BLOCKS - 1
WI_OUTPUT_START = WI_INPUT_END + 1
WI_OUTPUT_END = WI_OUTPUT_START + NUM_OUTPUT_BLOCKS - 1
WI_PROGRAM_START = WI_OUTPUT_END + 1 #Index of the word the program itself is going to start in.


def Denary2Binary(n):
	#
	'''convert denary integer n to binary string bStr'''
	#
	bStr = ''
	#
	#if n < 0: raise ValueError, "must be a positive integer"
	#
	if n == 0: return '0'
	#
	while n != 0:
		if (1 & n) == 1:
			bStr = '1' + bStr
		else:
			bStr =  '0' + bStr
		n >>= 1
	return bStr

conv = Denary2Binary