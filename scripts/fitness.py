import psyco
psyco.full()

import random
import sys
import simulate
import gen_params as gp
import fit_params as fp
import fit_tests

#Because there is a chance that we attempt to hash the same thing twice,
#we will have to store pretty much everything
def attempt(memory, input_string, ht):
	collisions = 0
	output = simulate.simulate(memory, str(input_string))
	
	#We've seen this output before
	if output in ht:
		#We have NOT seen this input string before
		if input_string not in ht[output]:
		#We have a collision
			ht[output][input_string] = True
			collisions += 1

	#Haven't seen the output before. Just set up the dictionary.
	else:
		ht[output] = {}
	
	return collisions


def multi_test(memory, ht, tests=fit_tests.tests):
	random.seed(fp.collision_seed)

	#Not strictly ratios; just single numbers
	#we are attempting to minimize
	ratios = [test(memory, ht, attempt) for test in tests]
	
	return [0] + ratios

def main(memory, tests = fit_tests.tests):
	ht = {}
	try:	
		ratios = multi_test(memory, ht, tests)
		return ratios
	except fit_tests.TrivialHashFunction:
		return [1.0] * len(tests)
	
if __name__ == "__main__":
	in_filename = sys.argv[1]
	out_filename = sys.argv[2]
	
	memory = simulate.initialize_memory(in_filename)
	ratio = main(memory)
	
	fh = open(out_filename, 'w')
	fh.write(str(ratio))
	fh.close()