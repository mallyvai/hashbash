import psyco
psyco.full()

import random
import sys
import os
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
	
	r_dest = None
	r_op = None
	r_x = None
	r_y = None
	r_z = None
	
	op_num = num_0 = random.randint(0, 99)
	num_1 = random.randint(0, 99)
	num_2 = random.randint(0, 99)
	num_3 = random.randint(0, 99)
	
	"""
	70% of the time, a source should refer to something in memory
	30% of the time, a source should be an immediate
	"""
	if bp.ENABLE_DEBUG: print "op_num", op_num
	if op_num in gp.cond_set or op_num in gp.cond_add:
		if bp.ENABLE_DEBUG: print "in cond set or add"
		if op_num in gp.cond_add:
			r_op = choose(gp.cond_add.ops)
		else:
			r_op = choose(gp.cond_set.ops)
		
		#50% of the time, x should be a valid program mem location
		#50% of the time, x should be some not-too-large immediate.
		if num_1 in gp.prob_branch_mem:
			r_x = random.randint(bp.WI_TEMP_REGS_START, bp.WI_TEMP_REGS_START + instr_index) #hacky hacky
			r_x = m_ify(r_x)
		else:
			r_x = random.randint(0, bp.SMALLISH_NUMBER)
		
		#Similar for y except restrict it to the regs
		if num_2 in gp.prob_branch_mem:
			r_y = random.randint(bp.WI_TEMP_REGS_START, bp.WI_TEMP_REGS_END) #hacky hacky
			r_y = m_ify(r_y)
		else:
			r_y = random.randint(0, bp.SMALLISH_NUMBER)
		
		if op_num in gp.cond_set:
			if r_z in gp.prob_branch_backward:
				r_z = random.randint(bp.WI_PROGRAM_START, instr_index)
			else:
				r_z = random.randint(instr_index + 1, end_instr_index)
		
		else:
			r_z = random.randint(0, end_instr_index-instr_index)
		r_dest = bp.WI_PROGRAM_COUNTER
		
	elif op_num in gp.comp_ops or op_num in gp.simp_ops:
		if bp.ENABLE_DEBUG: print "in comp or simp"
		if op_num in gp.comp_ops:
			r_op = choose(gp.comp_ops.ops)
		else:
			r_op = choose(gp.simp_ops.ops)
			
		#70% of the time, have the destination be something in the output
		#30% of the time, have the destination be something in temp reg range
	
		if num_1 in gp.prob_dest_in_output:
			r_dest = random.randint(bp.WI_OUTPUT_START, bp.WI_OUTPUT_END + 1)
		else:
			r_dest = random.randint(bp.WI_TEMP_REGS_START, bp.WI_TEMP_REGS_END + 1)
			
		#60% of the time, operand X should be something in the input
		#30% of the time, operand X should be something from the temp regs
		#10% of the time, operand X should be something from the output
		
		if num_2 in gp.prob_source_in_input:
			r_x = random.randint(bp.WI_INPUT_START, bp.WI_INPUT_END + 1)
		elif num_2 in gp.prob_source_in_temp_regs:
			r_x = random.randint(bp.WI_TEMP_REGS_START, bp.WI_TEMP_REGS_END + 1)
		else: #num_2 in gp.prob_source_in_output:
			r_x = random.randint(bp.WI_OUTPUT_START, bp.WI_OUTPUT_END + 1)
	
		#60% of the time, operand Y should be something in the input
		#30% of the time, operand Y should be something from the temp regs
		#10% of the time, operand Y should be something from the output
	
		if num_3 in gp.prob_source_in_input:
			r_y = random.randint(bp.WI_INPUT_START, bp.WI_INPUT_END + 1)
		elif num_3 in gp.prob_source_in_temp_regs:
			r_y = random.randint(bp.WI_TEMP_REGS_START, bp.WI_TEMP_REGS_END + 1)
		else: #num_3 in gp.prob_source_in_output:
			r_y = random.randint(bp.WI_OUTPUT_START, bp.WI_OUTPUT_END + 1)
	
		#Operand Z is always a random number
		r_z = random.getrandbits(16)
		r_x = prob_m_ify(r_x, gp.prob_is_mem)
		r_y = prob_m_ify(r_y, gp.prob_is_mem)
		
	elif op_num in gp.spec_ops:
		#80% of the time go backwards (XOR of bits in x is 0)
		#20% of the time go forwards (XOR of bits in y is 1)
		r_op = choose(gp.spec_ops.ops)
		if num_1 in gp.prob_iter_forward:
			r_x = 1
			desired = 0
		else:
			r_x = 0
			desired = 1
		
		#Hardwired hack. Change later.
		while get_xor(r_x) != desired:
			r_x = random.getrandbits(16)
		r_y = random.getrandbits(16)
		r_z = random.getrandbits(16)
		
	else:
		raise BadOperation("tried to create " + repr(r_op) + " " + repr(op_num))
	
	if r_dest is None: r_dest = random.getrandbits(16)
	if r_op is None: r_op = random.getrandbits(4)
	if r_x is None: r_x = random.getrandbits(16)
	if r_y is None: r_y = random.getrandbits(16)
	if r_z is None: r_z = random.getrandbits(16)
			
	
	return ' '.join([str(r_dest), str(r_op), str(r_x), str(r_y), str(r_z)])

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

	if bp.ENABLE_DEBUG: print fields
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

def generate_1(num_rand_instrs):
	"""
	Basic structure:
		do
		[ rand instructions ]
		while mem[2] < mem[WI_TOTAL_INPUT_BLOCKS]
		halt
	"""
	start = "0 iterinput 0 0 0"
	rand_instrs = []
	loop_1 = str(2) + " add 2m 1 666"
	loop_2 = str(bp.WI_PROGRAM_COUNTER) + " setiflt 2m " + str(bp.WI_NUM_INPUT_BLOCKS) + "m " + str(bp.WI_PROGRAM_START)
	halt = "0 halt 0 0 0"
	seed = os.urandom(10)
	random.seed(seed)
	
	for i in xrange(num_rand_instrs):
		rand_instrs.append(rand_instr(i, num_rand_instrs + bp.WI_PROGRAM_START+1))
	program = [start]
	program.extend(rand_instrs)
	program.extend([loop_1, loop_2, halt])
	
	
	#if bp.ENABLE_DEBUG: for line in program: print line
	mc = [str(parse_instr(i))+"\n" for i in program]
	return mc

def generate_2(num_rand_instrs):
	num_rand_instrs *= 10
	
	start = "0 iterinput 0 0 0"
	rand_instrs = []
	loop_1 = str(2) + " add 2m 1 666"
	halt = "0 halt 0 0 0"
	seed = os.urandom(10)
	random.seed(seed)
	
	for i in xrange(num_rand_instrs):
		rand_instrs.append(rand_instr(i, num_rand_instrs + bp.WI_PROGRAM_START+1))
	program = [start]
	program.extend(rand_instrs)
	program.extend([halt])
	
	
	#if bp.ENABLE_DEBUG: for line in program: print line
	mc = [str(parse_instr(i))+"\n" for i in program]
	return mc

def dumb_program(useless):
	start = "0 iterinput 0 0 0"
	mid = str(bp.WI_OUTPUT_START) + " add" + " 0 " + str(bp.WI_INPUT_START) + "m " + " 0 "
	halt = "0 halt 0 0 0"
	program = [start,mid,halt]
	
	mc = [str(parse_instr(i))+"\n" for i in program]
	return mc

def generate(num_rnd_instrs):
	return dumb_program(num_rnd_instrs)
	

def main(filename):
	fh = open(filename, 'w')
	mc = generate(gp.num_rnd_instrs)
	fh.write(''.join(mc))
	fh.close()
	
if __name__ == "__main__":
	main(sys.argv[1])