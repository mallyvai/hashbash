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
		return (c.ops[op] << c.S_OPCODE) + (x << c.S_X) + (y << c.S_Y) + (z << c.S_Z)
	
	def adjust_field(field):
		#Hardwired immediate bit. Less flexible. Screw it.
		imm_bit = 2 ** 67
		
		if "m" in field:
			return int(field.strip("m"))
		return int(field) + imm_bit

	fields = instr.split()
	trans_fields = []

	print fields
	op = fields.pop(1)
	if op not in c.ops:
		raise BadOperation(op + " doesn't exist.")
	
	fields = [adjust_field(i) for i in fields]
	dest = fields[0]
	x = fields[1]
	y = fields[2]
	z = fields[3]

	return generate_instr(op, x, y, z, dest)




cond_set = ["setifeq", "setifneq", "setiflt"]
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
	start = "0 iterinput 0 0 0"
	loop_1 = str(1) + " add 1m 1 1"
	loop_2 = str(c.WI_PROGRAM_COUNTER) + " setiflt 1m 64 1" + str(c.WI_PROGRAM_START)
	end = "0 halt 0 0 0"
	
	program = '\n'.join([start, loop_1, loop_2, end])
	
	return program

fh = open("/tmp/prog", 'w')
p = gen_program().split("\n")
print c.Denary2Binary(p)
fh.writelines([str(parse_instr(i))+"\n" for i in p])
fh.close()

