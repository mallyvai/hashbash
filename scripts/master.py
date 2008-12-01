import processing as proc
import master_params as mp
import os
import generate
import simulate
import random

path_dir = lambda num: os.path.join(mp.computation_directory, str(num))

def make_next_dir(gen_num):
	dirname = path_dir(str(gen_num))
	os.mkdir(dirname)
	return dirname


def find_unmeasured_programs(path):
	path_files = os.listdir(path)
	code_files = [filename for filename in path_files if mp.mcode_suffix in filename ]
	
	unmeasured = []
	for filename in code_files:
		if filename[:-1*len(mp.mcode_suffix)] + mp.fit_suffix not in path_files:
			unmeasured.append(filename)
	
	return unmeasured

def filtered_filenames(path):
	filenames = os.listdir(path)
	candidates = {}
	
	#Trivial screening
	for filename in filenames:
		if filename[-1*len(mp.mcode_suffix):] == mp.fit_suffix:
			fh = open(filename)
			lines = fh.readlines()
			fh.close()
			trivial = float(lines[mp.li_trivial])
			if trivial < mp.threshold_trivial:
				candidates[filename[-4:]] = lines
	
	#candidates that have information about the (very expensive) randomness test
	advanced_candidates = []
	for candidate, fitness in candidates.iteritems():
		if len(fitness) > 2: #hacky hacky\
			advanced_candidates.append((candidate, fitness))
			del candidates[candidate]
	
	
	basic_candidates = [(candidate, fitness) for candidate, fitness in candidates.iteritems()]
	basic_candidates.sort(lambda x, y: cmp(x[1][mp.li_trivial], y[1][mp.li_trivial]))
	
	filtered_candidates = advanced_candidates + basic_candidates
	
	return [i[0] for i in filtered_candidates]

def choose_partners(ordered_candidates):
	"""
	Random selection
	"""
	final_candidates = []
	num_to_breed = random.randint(mp.min_bred_functions, mp.max_bred_functions)
	for i in xrange(num_to_breed):
		final_candidates.append( (random.choice(ordered_candidates), random.choice(ordered_candidates)) )

def breed_fittest(one, two):
	None


def initialize():
	make_next_dir(0)
	for i in xrange(mp.max_num_functions()):
		generate.main(path_dir(i))

def handle_generation(num):
	path = path_dir(num)
	pool = proc.Pool(mp.max_num_workers)
	
	unmeasured = find_unmeasured(path)
	
	for i in unmeasured:
		print unmeasured
	
	pool.map(measure_program, unmeasured)
	
	#We now have fitness function output for every program in this directory.
	#Lets arrange them by the fittest discarding the stupid ones.
	ordered_candidates = filtered_filenames(path)
	partners = choose_partners(ordered_candidates)
	for i in partners:
		print unmeasured
	#Breeding time.
	#pool.map(breed_fittest, partners)

if __name__ == "__main__":
	initialize()