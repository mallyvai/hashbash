import random

num_rnd_instrs = 150

class IncIncRange:
	
	def __init__(self, bound0, bound1):
		if bound0 < bound1:
			self.lower = bound0
			self.upper = bound1
		else:
			self.lower = bound1
			self.upper = bound0
			
	def __contains__(self, num):
		return num >= self.lower and num <= self.upper

class OpProbRange:

	def __init__(self, ops_within, bound_0, bound_1):
		self.ops = ops_within
		self.prob_range = IncIncRange(bound_0, bound_1)

	def __contains__(self, num):
		return num in self.prob_range


cond_set = OpProbRange(["setifeq", "setiflt"], 0, 4)
cond_add = OpProbRange(["addifeq", "addifneq", "addiflt"], 5, 9)
comp_ops = OpProbRange(["mod", "add", "cshift", "shift"], 10, 44)
simp_ops = OpProbRange(["nand", "xor", "or", "not"], 45, 95)
spec_ops = OpProbRange(["iterinput"], 96, 99)

prob_branch = IncIncRange(0, 95)
prob_branch_backward = IncIncRange(0, 59)
prob_branch_forward = IncIncRange(59, 99)
prob_branch_mem = IncIncRange(0, 49)


prob_dest_in_output = IncIncRange(0, 74)
prob_source_in_input = IncIncRange(0, 59)
prob_source_in_temp_regs = IncIncRange(60, 89)
prob_source_in_output = IncIncRange(90, 99)

prob_is_mem = IncIncRange(0, 49)


prob_iter_backward = IncIncRange(0, 79)
prob_iter_forward = IncIncRange(80, 99)