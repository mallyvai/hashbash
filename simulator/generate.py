import random
import sys
import os
import math
import bit_params as bp
import gen_params as gp

"""
Let's have some delicious copy-pasta
"""
def get_xor(field):
	ret = 1 & field
	while field != 0:
		field >>= 1
		ret ^= (1 & field)
	return ret

def m_ify(num):
	return str(num) + "m"

def prob_m_ify(num, prob):
	if random.randint(0, 100) in prob:
		return m_ify(num)
	return str(num)

def rand_instr(instr_index, end_instr_index):
	"""
	Accepts the location of this instruction in memory
	Accepts where the last planned instruction memory is going to be located
	"""
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
	
	if op_num in gp.cond_set or op_num in gp.cond_add:
		
		op = choose(gp.cond_set.ops)
		
		#50% of the time, x should be a valid program mem location
		#50% of the time, x should be some not-too-large immediate.
		if num_1 in gp.prob_branch_mem:
			x = random.randint(WI_TEMP_REGS_START, instr_index) #hacky hacky
			x = m_ify(z)
		else:
			x = random.randint(SMALLISH_NUMBER)
		
		#Similar for y except restrict it to the regs
		if num_2 in gp.prob_branch_mem:
			y = random.randint(WI_TEMP_REGS_START, WI_TEMP_REGS_END) #hacky hacky
			y = m_ify(z)
		else:
			y = random.randint(SMALLISH_NUMBER)
		
		if op_num in gp.cond_set:
			if z in gp.prob_branch_backward:
				z = random.randint(WI_PROGRAM_START, instr_index)
			if z in gp.prob_branch_forward:
				z = random.randint(instr_index + 1, end_instr_index)
			gp.
		if op_num in gp.cond_add:
			dest = WI_PROGRAM_COUNTER
		
	elif op_num in gp.comp_ops or op_num in gp.simp_ops:
		
		if op_num in gp.comp_ops:
			op = choose(gp.comp_ops.ops)
		else:
			op = choose(gp.simp_ops.ops)
			
		#70% of the time, have the destination be something in the output
		#30% of the time, have the destination be something in temp reg range
	
		if num_1 in gp.prob_dest_in_output:
			dest = random.randint(bp.WI_OUTPUT_START, bp.WI_OUTPUT_END + 1)
		else:
			dest = random.randint(bp.WI_TEMP_REGS_START, bp.WI_TEMP_REGS_END + 1)
			
		#60% of the time, operand X should be something in the input
		#30% of the time, operand X should be something from the temp regs
		#10% of the time, operand X should be something from the output
		
		if num_2 in gp.prob_source_in_input:
			x = random.randint(bp.WI_INPUT_START, bp.WI_INPUT_END + 1)
		elif num_2 in gp.prob_source_in_temp_regs:
			x = random.randint(bp.WI_TEMP_REGS_START, bp.WI_TEMP_REGS_END + 1)
		else: #num_2 in gp.prob_source_in_output:
			x = random.randint(bp.WI_OUTPUT_START, bp.WI_OUTPUT_END + 1)
	
		#60% of the time, operand Y should be something in the input
		#30% of the time, operand Y should be something from the temp regs
		#10% of the time, operand Y should be something from the output
	
		if num_3 in gp.prob_source_in_input:
			y = random.randint(bp.WI_INPUT_START, bp.WI_INPUT_END + 1)
		elif num_3 in gp.prob_source_in_temp_regs:
			y = random.randint(bp.WI_TEMP_REGS_START, bp.WI_TEMP_REGS_END + 1)
		else: #num_3 in gp.prob_source_in_output:
			y = random.randint(bp.WI_OUTPUT_START, bp.WI_OUTPUT_END + 1)
	
		#Operand Z is always a random number
		z = random.getrandbits(16)
		x = m_ify(y)
		y = m_ify(y)
		
	elif op_num in gp.spec_ops:
		#80% of the time go backwards (XOR of bits in x is 0)
		#20% of the time go forwards (XOR of bits in y is 1)
		if num_1 in gp.prob_iter_forward:
			x = 1
			desired = 0
		else:
			x = 0
			desired = 1
		
		#Hardwired hack. Change later.
		while get_xor(x) != desired:
			x = gp.getrandbits(16)
		y = gp.getrandbits(16)
		z = gp.getrandbits(16)
		
	else:
		raise BadOperation("tried to create " + repr(op))
	
	return ' '.join([dest, op, x, y, z])

class BadOperation(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def parse_instr(instr):
	def generate_instr(op, x, y, z, dest):
		return (bp.ops[op] << bp.S_OPCODE) + (x << bp.S_X) + (y << bp.S_Y) + (z << bp.S_Z) + (dest << bp.S_DEST)
	
	imm_bit = bp.IMM * (2**(16 - 1))
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
	if op not in bp.ops:
		raise BadOperation(op + " doesn't exist.")
	
	fields = [adjust_field(i) for i in fields]
	dest = fields[0]
	x = fields[1]
	y = fields[2]
	z = fields[3]

	return generate_instr(op, x, y, z, dest)
	
def op_from_probs(num):
	if num >= 0 and num < 30:
		return random.choice(gp.simp_ops)
	elif num >= 30 and num < 50:
		return random.choice(gp.comp_ops)
	elif num >= 50 and num < 70:
		return random.choice(gp.cond_add)
	else:
		return random.choice(gp.cond_set)

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
	loop_2 = str(bp.WI_PROGRAM_COUNTER) + " setiflt 2m " + str(bp.WI_NUM_INPUT_BLOCKS) + "m " + str(bp.WI_PROGRAM_START)
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
	loop_2 = str(bp.WI_PROGRAM_COUNTER) + " setiflt 2m " + str(bp.WI_NUM_INPUT_BLOCKS) + "m " + str(bp.WI_PROGRAM_START)
	end = "0 halt 0 0 0"	#431
	
	program = '\n'.join([start, loop_1, loop_2, end])
	
	fh = open("/tmp/prog", 'w')
	p = program.split("\n")
	print "PROGRAM IS: ", p
	fh.writelines([str(parse_instr(i))+"\n" for i in p])
	fh.close()