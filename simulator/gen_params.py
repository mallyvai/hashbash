import random

class IncIncRange:
	
	def __init__(self, bound0, bound1):
		if bound0 < bound1:
			self.lower = bound0
			self.upper = bound1
		else:
			self.lower = bound1
			self.upper = bound0
			
	def __contains__(self, num):
		return num >= self.lower and num <= self.upper:



class OpProbRange:

	def __init__(self, ops_within, bound_0, bound_1):
		self.ops = ops_within
		self.prob_range = IncIncRange(bound_0, bound_1)

	def __contains__(self, num):
		return num in self.prob_range


cond_set = OpProbRange(["setifeq", "setiflt"], 0, 30)
cond_add = OpProbRange(["addifeq", "addifneq", "addiflt"], 30, 50)
comp_ops = OpProbRange(["mod", "add", "cshift", "shift"], 50, 75)
simp_ops = OpProbRange(["nand", "xor", "or", "not"], 75, 95)
spec_ops = OpProbRange(["iterinput"], 95, 99)

prob_branch = IncIncRange(0, 95)
prob_backward = IncIncRange(0, 59)
prob_forward = IncIncRange(59, 99)
