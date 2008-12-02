import simulate
import fit_params as fp
import random


def random_string(length):
	return ''.join([chr(random.getrandbits(8)) for i in xrange(length)])


class TrivialHashFunction(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)


def trivial(memory, ht, attempt):
	"""
	Handles the trivial case of bad functions that don't really do anything.
	"""
	collisions = 0
	total = 0
	for i in xrange(fp.trivial.lower, fp.trivial.upper):
		collisions += attempt(memory, str(i), ht)
		total += 1
	return collisions/total

def stage_one(memory, ht, attempt):
	collisions = 0
	total = 0
	#stage one - a bunch of random numbers. smallish ones.
	for i in xrange(fp.one.attempts):
		input_string = random.uniform(fp.one.lower, fp.one.upper)
		collisions += attempt(memory, input_string, ht)
		total += 1
	return collisions/total

def stage_two(memory, ht, attempt):
	collisions = 0
	total = 0
	#stage two - a bunch of random strings, medium-ish ones.
	for i in xrange(fp.two.attempts):
		size = random.randint(fp.two.lower, fp.two.upper)
		rnd_str = random_string(size)
		collisions += attempt(memory, rnd_str, ht)
		total += 1
	return collisions/total
	
def stage_three(memory, ht, attempt):
	#stage three - the shifting test. start off with 1 and keep shifting it for a long time.
	collisions = 0
	total = 0
	counter = fp.three.lower
	for i in xrange(fp.three.attempts):
		counter >>= 1
		collisions += attempt(memory, counter, ht)
		total += 1
	return collisions/total

basic_tests = tests = [trivial, stage_one, stage_two, stage_three]