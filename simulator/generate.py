import random
import sys
import math
import bit_params as c
	
class BadOperation(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)


def parse_instr(instr):
	def generate_instr(op, x, y, z, dest):
		return (c.ops[op] << c.S_OPCODE) + (x << c.S_X) + (y << c.S_Y) + (z << c.S_Z) + (dest << c.S_DEST)
	
	imm_bit = c.IMM * (2**(16 - 1))
	mem_bit = 0
	if imm_bit == 0:
		mem_bit = 1 * (2**(16 - 1))
	
	def adjust_field(field):
		if "m" in field:				
			return int(field.strip("m")) + mem_bit
		return int(field) + imm_bit

	fields = instr.split()
	trans_fields = []

	print "FIELDS: ", fields
	op = fields.pop(1)
	if op not in c.ops:
		raise BadOperation(op + " doesn't exist.")
	
	fields = [adjust_field(i) for i in fields]
	dest = fields[0]
	x = fields[1]
	y = fields[2]
	z = fields[3]

	return generate_instr(op, x, y, z, dest)

cond_set = ["setifeq", "setiflt"]
cond_add = ["addifeq", "addifneq", "addiflt"]
comp_ops = ["mod", "add", "cshift", "shift"]
simp_ops = ["nand", "xor", "or", "not"]

def op_from_probs(num):
	if num >= 0 and num < 30:
		return random.choice(simp_ops)
	elif num >= 30 and num < 50:
		return random.choice(comp_ops)
	elif num >= 50 and num < 70:
		return random.choice(cond_add)
	else:
		return random.choice(cond_set)

def get_rand_bits(num_rand_bits, msd):
	return random.randint(0, 2**num_rand_bits) | ( msd << (num_rand_bits - 1))
	
def gen_program():
	"""Program:
		iterinput
		add 1 to tempvar mem[2]
		goto start if mem[2] < 20
	"""
	start = "0 iterinput 0 0 0" #428
	loop_1 = str(2) + " add 2m 1 666"
	loop_2 = str(c.WI_PROGRAM_COUNTER) + " setiflt 2m 50 " + str(c.WI_PROGRAM_START)
	end = "0 halt 0 0 0"	#431
	
	program = '\n'.join([loop_1,loop_1,loop_1,end])
	
	fh = open("/tmp/prog", 'w')
	p = program.split("\n")
	print "PROGRAM IS: ", p
	fh.writelines([str(parse_instr(i))+"\n" for i in p])
	fh.close()