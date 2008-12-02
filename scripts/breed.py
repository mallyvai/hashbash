import psyco
psyco.full()

import sys
import random
import breed_params as rp
import bit_params as bp

def mutate(chrom):
	min_mut = rp.min_instructions_mutated
	max_mut = min(len(chrom) - 1, rp.max_instructions_mutated)
	
	if len(chrom) <= rp.min_instructions_mutated: min_mut = 1
	
	mutate_this_many = random.randint(min_mut, max_mut)
	words_to_mutate = random.sample(range(len(chrom)-1), mutate_this_many)
	for i in words_to_mutate:
		chrom[i] = int(chrom[i])
		#use a distribution such that higher bits have lower probability of being selected
		chrom[i] &= random.getrandbits(68)
		chrom[i] %= bp.MAX_WORD_SIZE
		chrom[i] = str(chrom[i]) + "\n" #I didn't add this line. Fixing this bug caused me untold hours of pain. Next iteration needs a better object model...
	return chrom

def separate_comments(cell):
	comments = []
	code = []
	for line in cell:
		if line.isspace() or len(line) == 0: None
		elif "#" in line : comments.append(line)
		else: code.append(line)
	return code, comments


def breed(one, two):
	one_code, one_comments = separate_comments(one)
	two_code, two_comments = separate_comments(two)
	
	ret_chrom = double_concatenation(one_code, two_code)
	
	if random.randint(0, 99) in rp.prob_mutate:
		ret_chrom = mutate(ret_chrom)

	return ret_chrom

def double_concatenation(one, two):
	"""
	Concatenate the chromosomes, and remove some number of elements from the middle
	to get the overall length to within a few cells of the "average"
	"""
		
		
	ret_chrom = []
	
	ret_chrom.extend(one)
	ret_chrom.extend(two)
	
	"""
	Choose indices i, j s.t
	len - j - i = new_length; i >  1; j < (len - 2)
	len - new_length = j + i
	randomly choose some j appropriately; i will follow
	
	"""
	
	new_length = rp.average_length + rp.length_error_margin * random.choice([-1, 1])
	remove_amount = len(ret_chrom) - new_length
	
	rem_start = remove_amount
	rem_end = remove_amount + rem_start - 1
	
	last_acceptable_end = len(ret_chrom) - 3
	first_acceptable_end = 1 + remove_amount
	
	
	rem_end = random.randint(first_acceptable_end, last_acceptable_end)
	rem_start = rem_end - last_acceptable_end
	
	ret_chrom = ret_chrom[:rem_start] + ret_chrom[rem_end + 1:]
	
	#Make sure that the function doesn't balloon out of control
	difference = len(ret_chrom) - rp.hard_size_limit
	if difference > 0:
		for i in xrange(difference):
			ret_chrom.pop(int(len(ret_chrom)/2))
	return ret_chrom

if __name__ == "__main__":
	
	#usage: child parent_1 parent_2
	
	fh = open(sys.argv[2], 'r')
	one = fh.readlines()	
	fh.close()
	
	fh = open(sys.argv[3], 'r')
	two = fh.readlines()
	fh.close()
	
	fh = open(sys.argv[1], 'w')
	child = double_concatenation(one, two)
	fh.write(''.join(child))