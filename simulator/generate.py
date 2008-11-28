import random
import sys
import os
import math
import bit_params as c
import gen_params as gp



def rand_instr(instr_index):
	
	choose = lambda x: random.choice(x)
	
	dest = None
	op = None
	x = None
	y = None
	z = None
	
	op_num = num_0 = random.randint(0, 100)
	num_1 = random.randint(0, 100)
	num_2 = random.randint(0, 100)
	num_3 = random.randint(0, 100)
	
	"""
	70% of the time, a source should refer to something in memory
	30% of the time, a source should be an immediate
	"""
	
	if op_num in gp.cond_set:
		#Absolute branch 95% of the time.
			#60% of the time go backward some amount 
			#40% of the time go forward some amount
		#5% of the time just do something really weird (within the scope of the program)
		
		op = choose(gp.cond_set.ops)
		
		if num_1 in prob_branch:
			dest = str(WI_PROGRAM_COUNTER)
			bamount = int(num_2 / 2) + 2
			if amount <
			
			z = str(instr_index
		else:
			
		
	elif op_num in gp.cond_add:
		#Relative branch 95% of the time.
		#5% of the time just do something really weird (within the scope of the program)

	elif op_num in gp.comp_ops or op in gp.simp_ops:
		#70% of the time, have the destination be something in the output
		#30% of the time, have the destination be something in temp reg range
		
		if num_1 in gp.prob_dest_in_output:
			dest = random.randint(WI_OUTPUT_START, WI_OUTPUT_END + 1)
		else:
			dest = random.randint(WI_TEMP_REGS_START, WI_TEMP_REGS_END + 1)
			
		#60% of the time, operand X should be something in the input
		#30% of the time, operand X should be something from the temp regs
		#10% of the time, operand X should be something from the output
		
		if num_2 in gp.prob_source_in_input:
			x = random.randint(WI_INPUT_START, WI_INPUT_END + 1)
		elif num_2 in gp.prob_source_in_temp_regs:
			x = random.randint(WI_TEMP_REGS_START, WI_TEMP_REGS_END + 1)
		elif num_2 in gp.prob_source_in_output:
			x = random.randint(WI_OUTPUT_START, WI_OUTPUT_END + 1)
		else:
			raise Exception("WTF")
	
		#60% of the time, operand Y should be something in the input
		#30% of the time, operand Y should be something from the temp regs
		#10% of the time, operand Y should be something from the output
	
		if num_2 in gp.prob_source_in_input:
			x = random.randint(WI_INPUT_START, WI_INPUT_END + 1)
		elif num_2 in gp.prob_source_in_temp_regs:
			x = random.randint(WI_TEMP_REGS_START, WI_TEMP_REGS_END + 1)
		elif num_2 in gp.prob_source_in_output:
			x = random.randint(WI_OUTPUT_START, WI_OUTPUT_END + 1)
		else:
			raise Exception("WTF")
	

	
		#Operand Z is always a random number
	
	
	elif op_num in spec_ops:
		#80% of the time go backwards
		#20% of the time go forwards
		
	else:
		raise BadOperation("tried to create " + repr(op))
		
	
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

def generate():
	"""
	Basic structure:
		do
		
		while mem[2] < mem[WI_TOTAL_INPUT_BLOCKS]
		halt
	"""
	start = "0 iterinput 0 0 0"
	loop_1 = str(2) + " add 2m 1 666"
	loop_2 = str(c.WI_PROGRAM_COUNTER) + " setiflt 2m " + str(c.WI_NUM_INPUT_BLOCKS) + "m " + str(c.WI_PROGRAM_START)
	halt = "0 halt 0 0 0"
	seed = os.urandom(10)
	random.seed(seed)
	

def gen_program():
	"""Program:
		iterinput
		add 1 to tempvar mem[2]
		goto start if mem[2] < 20
	"""
	start = "0 iterinput 0 0 0" #428
	loop_1 = str(2) + " add 2m 1 666"
	loop_2 = str(c.WI_PROGRAM_COUNTER) + " setiflt 2m " + str(c.WI_NUM_INPUT_BLOCKS) + "m " + str(c.WI_PROGRAM_START)
	end = "0 halt 0 0 0"	#431
	
	program = '\n'.join([start, loop_1, loop_2, end])
	
	fh = open("/tmp/prog", 'w')
	p = program.split("\n")
	print "PROGRAM IS: ", p
	fh.writelines([str(parse_instr(i))+"\n" for i in p])
	fh.close()