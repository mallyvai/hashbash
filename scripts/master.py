import processing as proc
import master_params as mp
import os
import generate
import simulate

path_dir = lambda num, os.path.join(mp.computation_directory, str(num))

def make_next_dir(gen_num):
	dirname = path_dir(str(gen_num))
	os.mkdir(dirname)
	return dirname


def find_unmeasured_programs(path):
	path_files = os.listdir(path)
	code_files = [filename if mp.mcode_suffix in filename for filename in path_files]
	
	unmeasured = []
	for filename in code_files:
		if filename[:len(mp.mcode_suffix)] + fit_suffix not in path_files:
			unmeasured.append(filename)
	
	return unmeasured


def choose_partners(path):
	"""
	Bigamous breeding strategy:
		Suppose we have hash functions A-E in fitness order A B C D E
		A, B
		C, D
		E dies
	"""

def initialize():
	make_next_dir(0)
	for i in xrange(mp.max_num_functions):
		generate.main(filename)

def handle_generation(num):
	path = path_dir(num)
	pool = proc.Pool(mp.max_num_workers)
	
	unmeasured = find_unmeasured(path)
	pool.map(measure_program, unmeasured)
	
	#We now have fitness function output for every program in this directory.
	#Breeding time.
	
	partners = choose_partners(path)
	pool.map(breed_fittest, partners)