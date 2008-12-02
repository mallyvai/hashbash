import processing as proc
import master_params as mp
import os
import generate
import simulate
import random
import tempfile
import shutil
import fitness
import breed
import glob

path_dir = lambda generation: os.path.abspath(os.path.join(mp.computation_directory, str(generation)+mp.generation_suffix))

def make_next_dir(gen_num):
	dirname = path_dir(str(gen_num))
	os.mkdir(dirname)
	return dirname


def find_unmeasured(path):
	path_files = os.listdir(path)
	path_files = [os.path.join(path, filename) for filename in path_files]
	code_files = [filename for filename in path_files if mp.mcode_suffix in filename ]
	
	unmeasured = []
	for filename in code_files:
		if filename[:-1*len(mp.mcode_suffix)] + mp.fit_suffix not in path_files:
			unmeasured.append(filename)
	
	return unmeasured

def filtered_filenames(path):
	filenames = os.listdir(path)
	filenames = [os.path.join(path, i) for i in filenames]
	candidates = {}

	#Trivial screening
	for filename in filenames:
		cur_prefix = filename[:-1*len(mp.fit_suffix)]
		cur_suffix = filename[-1*len(mp.fit_suffix):]
		if cur_suffix == mp.fit_suffix:
			fh = open(filename)
			lines = fh.readlines()
			fh.close()
			trivial = float(lines[mp.li_trivial])
			if trivial < mp.threshold_trivial:
				candidates[cur_prefix] = lines
	
	#candidates that have information about the (very expensive) randomness test
	advanced_candidates = []
	for candidate, fitness in candidates.iteritems():
		if len(fitness) > 2: #hacky hacky\
			advanced_candidates.append((candidate, fitness))
			del candidates[candidate]
	
	
	basic_candidates = [(candidate, fitness) for candidate, fitness in candidates.iteritems()]
	
	basic_candidates.sort(lambda x, y: cmp(x[1][mp.li_trivial], y[1][mp.li_trivial]))
	
	
	filtered_candidates = advanced_candidates + basic_candidates
	
	print filtered_candidates
	return [i[0] for i in filtered_candidates]

def choose_partners(ordered_candidates):
	"""
	Random selection
	"""
	final_candidates = []
	lower = min(mp.min_bred_functions(), len(ordered_candidates))
	upper = min(mp.max_bred_functions(), len(ordered_candidates))
	num_to_breed = random.randint(lower, upper)
	for i in xrange(num_to_breed):
		final_candidates.append( (random.choice(ordered_candidates), random.choice(ordered_candidates)) )
	return final_candidates

def breed_fittest(partner_filenames):
	fh = open(partner_filenames[0], 'r')
	one = fh.readlines()	
	fh.close()
	
	fh = open(partner_filenames[1], 'r')
	two = fh.readlines()
	fh.close()
	
	child = double_concatenation(one, two)
	
	#append the child's parents as a comment.
	child.append(''.join(["\n#",one, ";", two]))
	return child

def measure_program(filename):
	in_filename = filename
	out_filename = filename[:-1*len(mp.mcode_suffix)]+mp.fit_suffix
	print in_filename, out_filename
	memory = simulate.initialize_memory(in_filename)
	ratio = fitness.main(memory)
	
	statistics = [ratio]
	
	#We create the file.
	tmp_tuple = tempfile.mkstemp(dir="/tmp/")
	tmp_fh = tmp_tuple[0]
	tmp_name = tmp_tuple[1]
	
	os.close(tmp_fh)
	
	fh = open(tmp_name, 'w')
	fh.write(''.join([str(i) for i in statistics]))
	fh.close()
	
	#I hope to god this cannot fail in-transit. Please please please be atomic.
	shutil.move(tmp_name, out_filename)

def initialize():
	make_next_dir(0)
	path = path_dir(0)
	for i in xrange(mp.max_num_functions()):
		filename = os.path.join(path, str(i)+mp.mcode_suffix)
		generate.main(filename)

"""
"Handling" a generation means computing the fitness of each of its members.
"""

def measure_generation(num):
	path = path_dir(num)
	pool = proc.Pool(mp.max_num_workers)
	
	unmeasured = find_unmeasured(path)
	pool.map(measure_program, unmeasured)
	
"""
"Creating" a generation N means breeding the previous generation once it
has been fully handled, and creating new chromosomes to fill in the gaps.
"""

def create_generation(num):
	if num < 0: raise IndexError(str(num) + " is too small. Must be >= 0.")
	
	#We now have fitness function output for every program in this directory.
	#Lets arrange them by the fittest discarding the stupid ones.
	ordered_candidates = filtered_filenames(prev)
	partners = choose_partners(ordered_candidates)

	#Breeding time.
	result = pool.map_async(breed_fittest, partners)
	result.wait()
	children = result.get()
	
	final = []
	num_randgen = random.randint(mp.min_new_functions, mp.max_new_functions)
	for i in xrange(num_randgen):
		final.append(generate(gp.num_rnd_instrs))

#Returns None, None if no generations exist
#Otherwise return biggest_path, biggest_num
def find_biggest_generation():
	path = path_dir("")
	contents = glob.glob(path_dir("*"+mp.generation_suffix))
	contents.sort(reverse=True)
	contents = [os.path.join(path, i) for i in contents]
	if len(contents) == 0: return None, None
	return contents[0], os.path.basename(contents[0])[:-len(mp.generation_suffix)]

def main(additional_generations_to_create):
	if num < 0: raise IndexError(str(num) + " is too small. Must be >= 0.")
	biggest_path, biggest_num = find_biggest_generation()
	for i in xrange(biggest_num+1, biggest_num + additional_generations_to_create):
		handle_generation(i)
		create_generation(i+1)
		
if __name__ == "__main__":
	main(1)