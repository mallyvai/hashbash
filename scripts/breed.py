import sys
import random
import breed_params as rp

def mutate(chrom):
	chrom = chrom[:]
	mutate_this_many = random.randint(rp.min_instructions_mutated, rp.max_instructions_mutated)
	words_to_mutate = random.sample(range(len(chrom)-1), mutate_this_many)
	for i in words_to_mutate:
		chrom[i] = int(chrom[i])
		#use a distribution such that higher bits have lower probability of being selected
		print "ABOUT TO VOMIT"
		chrom[i] &= random.getrandbits(68)
	return chrom

def double_concatenation(one, two):
	"""
	Concatenate the chromosomes, and remove some number of elements from the middle
	to get the overall length to within a few cells of the "average"
	"""
	
	
	def separate_comments(cell):
		comments = []
		code = []
		for line in cell:
			if len(line) == 0: None
			elif "#" in line : comments.append(line)
			else: code.append(line)
		return code, comments
	
	one_code, one_comments = separate_comments(one)
	two_code, two_comments = separate_comments(two)
	
	ret_chrom = []
	
	ret_chrom.extend(one_code)
	ret_chrom.extend(two_code)
	
	
	
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
	
	if random.randint(0, 99) in rp.prob_mutate:
		ret_chrom = mutate(ret_chrom)

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