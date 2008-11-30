import processing as proc
import master_params as mp
import os
import generate
import simulate

path_dir = lambda num, os.path.join(mp.computation_directory, str(num))

def make_next_dir(x):
	dirname = path_dir(x)
	os.mkdir(dirname)
	return dirname

def measure_program(filename):
	"""Fitness junk here"""


def initialize():
	make_next_dir(0)
	for i in xrange(mp.max_num_functions):
		generate.main(filename)

def handle_generation(num):
	pool = proc.Pool(mp.max_num_workers)
	result = pool.map(measure_program, os.listdir(path_dir(num)))
	