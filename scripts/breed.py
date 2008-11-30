import sys
import random
import breed_params as rp

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
	
	return ret_chrom
	
if __name__ == "__main__":
	
	print "usage: child parent_1 parent_2 "
	
	fh = open(sys.argv[2], 'r')
	one = fh.readlines()	
	fh.close()
	
	fh = open(sys.argv[3], 'r')
	two = fh.readlines()
	fh.close()
	
	fh = open(sys.argv[1], 'w')
	child = double_concatenation(one, two)
	fh.write(''.join(child))
	print "done"