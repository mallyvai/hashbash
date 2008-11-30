import random
import sys
import simulate
import gen_params as gp
import fit_params as fp

def random_string(length):
	return ''.join([chr(random.getrandbits(8)) for i in xrange(length)])

def attempt(memory, input_string, ht):
	collisions = 0
	output = simulate.simulate(memory, str(input_string))
	try:
		ht[output] += 1
		collisions += 1
		
	except KeyError:
		ht[output] = 1
	return collisions

def trivial(memory, ht):
	"""
	Handles the trivial case of bad functions that don't really do anything.
	
	"""

def collision(memory, ht):
	random.seed(fp.collision_seed)
	
	collisions = 0
	
	#stage one - a bunch of random numbers. smallish ones.
	for i in xrange(fp.one.attempts):
		input_string = random.uniform(fp.one.lower, fp.one.upper)
		collisions += attempt(memory, input_string, ht)
	
	#stage two - a bunch of random strings, medium-ish ones.
	for i in xrange(fp.two.attempts):
		size = random.randint(fp.two.lower, gp.two.upper)
		rnd_str = random_string(size)
		collisions += attempt(memory, rnd_str, ht)
	
	#stage three - iterate the range through which we went through in one
	for i in xrange(fp.one.lower, fp.one.upper):
		collisions += attempt(memory, str(i), ht)
	
	return collisions
	

if __name__ == "__main__":
	in_filename = sys.argv[1]
	out_filename = sys.argv[2]