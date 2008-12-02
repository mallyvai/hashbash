import gen_params as gp

average_length = gp.num_rnd_instrs
length_error_margin = 10

max_instructions_mutated = 5
min_instructions_mutated = 0

prob_mutate = gp.IncIncRange(0, 20)

hard_size_limit = 5000