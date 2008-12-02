computation_directory = "/tmp/testgen"

#The maximum number of programs that can be in a given generation
max_num_functions = lambda : 20
#The minimum number of functions that have to be new
min_new_functions = lambda : int(.1 * max_num_functions())
max_new_functions = lambda : int(0.5 * max_num_functions())

max_bred_functions = lambda : max_num_functions() - min_new_functions()
min_bred_functions = lambda : max_num_functions() - max_new_functions()

#Maximum number of allowed workers
max_num_workers = 10

mcode_suffix = ".mc"
fit_suffix = ".fit"

#li is line index.
li_trivial = 0
threshold_trivial = .8

li_multi = 1

generation_suffix = ".gen"
