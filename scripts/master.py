import os
import random
import tempfile
import shutil
import glob
import sys

import generate
import simulate
import fitness
import breed

import processing as proc
import master_params as mp
import gen_params as gp

def gen_dir(gen_num):
	base = str(gen_num) + mp.generation_suffix
	if gen_num is None or len(str(gen_num)) == 0:
		base = ""
	return os.path.abspath(os.path.join(mp.computation_directory, base))
	
gen_member = lambda generation, num: os.path.join(gen_dir(generation), str(num) + mp.mcode_suffix)

def make_next_dir(gen_num):
	dirname = gen_dir(str(gen_num))
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

def filtered_filenames(num):
	path = gen_dir(num)
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
	for candidate, fit in candidates.iteritems():
		if len(fit) > 2: #hacky hacky\
			advanced_candidates.append((candidate, fit))
			del candidates[candidate]
	
	
	basic_candidates = [(candidate, fit) for candidate, fit in candidates.iteritems()]
	
	basic_candidates.sort(lambda x, y: cmp(x[1][mp.li_trivial], y[1][mp.li_trivial]))
	
	
	filtered_candidates = advanced_candidates + basic_candidates
	
	return [i[0]+mp.mcode_suffix for i in filtered_candidates]

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
	
	one_name = partner_filenames[0]
	two_name = partner_filenames[1]
	
	fh = open(one_name, 'r')
	one = fh.readlines()	
	fh.close()
	
	fh = open(two_name, 'r')
	two = fh.readlines()
	fh.close()
	
	child = breed.double_concatenation(one, two)
	
	#Append the child's parents as a comment.
	print "closer"
	child.append(''.join(["\n#",str(one_name), ";", str(two_name)]))
	
	return child

def measure_program(filename):
	in_filename = filename
	out_filename = filename[:-1*len(mp.mcode_suffix)]+mp.fit_suffix
	
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
	path = gen_dir(0)
	for i in xrange(mp.max_num_functions()):
		filename = os.path.join(path, str(i)+mp.mcode_suffix)
		generate.main(filename)

"""
"Handling" a generation means computing the fitness of each of its members.
"""

def measure_generation(num):
	pool = proc.Pool(mp.max_num_workers)

	path = gen_dir(num)
	
	unmeasured = find_unmeasured(path)
	pool.map(measure_program, unmeasured)
	
"""
"Creating" a generation N means breeding the previous generation once it
has been fully handled, and creating new chromosomes to fill in the gaps.
"""

"""
Creates a generation directory with num
"""
def create_generation(num):
	if num <= 0: raise IndexError(str(num) + " is too small. Must be > 0.")
	pool = proc.Pool(mp.max_num_workers)
	
	#We now have fitness function output for every program in this directory.
	#Lets arrange them by the fittest discarding the stupid ones.
	ordered_candidates = filtered_filenames(str(num-1))
	partners = choose_partners(ordered_candidates)
	
	#Breeding time.
	print "prolly gonna vomit soon"
	result = pool.map_async(breed_fittest, partners)
	print "wtf"
	result.wait()
	print "waa"
	children = result.get()
	
	print "almost..."
	num_randgen = random.randint(mp.min_new_functions(), mp.max_new_functions())
	for i in xrange(num_randgen):
		children.append(generate.generate(gp.num_rnd_instrs))
	print "oh god?"
	os.mkdir(gen_dir(num))
	
	for child, i in zip(children, xrange(len(children))):
		fh = open(gen_member(num, i), 'w')
		child = [str(word) for word in child]
		child.append("\n")
		fh.write(''.join(child))
		fh.close()
	
class NoGenerationsExist(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)


#Returns None, None if no generations exist
#Otherwise return biggest_path, biggest_num
def find_biggest_generation():
	path = gen_dir("")
	contents = glob.glob(gen_dir("*"))
	
	def int_part(pathname):
		base = os.path.basename(pathname)
		name = base[:-len(mp.generation_suffix)]
		print int(name)
		return int(name)
	print "CONTENTS%%%%%%%%%%", contents
	contents.sort(key=int_part, reverse=True)
	
	print "CONTENTS~~~~~~~", contents
	if len(contents) == 0: raise NoGenerationsExist(path)
	return contents[0], int(os.path.basename(contents[0])[:-len(mp.generation_suffix)])

def main(additional_generations_to_create):
	if additional_generations_to_create < 0: raise IndexError(str(additional_generations_to_create) + " is too small. Must be >= 0.")
	
	biggest_path, biggest_num = None, None
	
	try:
		biggest_path, biggest_num = find_biggest_generation()
	except NoGenerationsExist:
		initialize()
		biggest_path, biggest_num = find_biggest_generation()

	
	for i in xrange(biggest_num, biggest_num + additional_generations_to_create):
		measure_generation(i)
		create_generation(i+1)
		
if __name__ == "__main__":
	
	try:
		print sys.argv[1]
		if sys.argv[1] == "-f":
			shutil.rmtree(mp.computation_directory)
			os.mkdir(mp.computation_directory)
	except IndexError: None
	
	main(40)