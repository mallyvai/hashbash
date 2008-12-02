import bit_params as c
	
	def disassemble(instr):		
		str_x = None
		str_y = None
		str_z = None
		str_dest = None
		str_op = None
		
		def get_xor(field):
			ret = 1 & field
			while field != 0:
				field >>= 1
				ret ^= (1 & field)
			return ret
		
		f_op = get_field(instr, c.M_OPCODE, c.S_OPCODE)
		f_x = get_field(instr, c.M_X, c.S_X)
		f_y = get_field(instr, c.M_Y, c.S_Y)
		f_z = get_field(instr, c.M_Z, c.S_Z)
		f_dest = get_field(instr, c.M_DEST, c.S_DEST)

		msd_x = get_msd(f_x, c.B_X)
		msd_y = get_msd(f_y, c.B_Y)
		msd_z = get_msd(f_z, c.B_Z)
		msd_dest = get_msd(f_dest, c.B_DEST)
		
		xor_x = get_xor(f_x)
		xor_y = get_xor(f_y)
		xor_z = get_xor(f_z)
		xor_dest = get_xor(f_dest)
		
		x = None
		y = None
		z = None
		dest = None
		
		str_x = c.r_ops[f_op]
		str_y = msd_dest
		
		
		if msd_x == c.IMM:
			x = f_x & c.M_FVAL
			if c.ENABLE_DEBUG: print "x is imm"
		else: 
			x = m[f_x]
			if c.ENABLE_DEBUG: print "pulling x from mem", f_x
		
		if msd_y == c.IMM:
			y = f_y & c.M_FVAL
			if c.ENABLE_DEBUG: print "y is imm"
		else: 
			y = m[f_y]
			if c.ENABLE_DEBUG: print "pulling y from mem", f_y
		
		if msd_z == c.IMM:
			z = f_z & c.M_FVAL
			if c.ENABLE_DEBUG: print "y is imm"
		
		else:
			z = m[f_z]
			if c.ENABLE_DEBUG: print "pulling z from mem", f_z
		
		if msd_dest == c.IMM:
			dest = f_dest & c.M_FVAL
			if c.ENABLE_DEBUG: print "dest is imm"
		else: 
			dest = m[f_dest] & c.M_FVAL
			if c.ENABLE_DEBUG: print "pulling dest from mem"
		
		dbg_brk()
		if c.ENABLE_DEBUG: print c.r_ops[f_op]
		
		"""Now lets go and actually do the calculations..."""
		if f_op == c.ops["and"]: m[dest] = x & y
		elif f_op == c.ops["nand"]: m[dest] = ~(x & y)
		elif f_op == c.ops["xor"]: m[dest] = x ^ y
		elif f_op == c.ops["or"]: m[dest] = x | y
		elif f_op == c.ops["not"]: m[dest] = ~x
		
		elif f_op == c.ops["mod"]: 
			if y > 0:
				m[dest] = x % y
			else:
				m[dest] = x
				
		elif f_op == c.ops["add"]: 
			if xor_z == 1: y *= -1 #sub if the relevant bit is 1
			if c.ENABLE_DEBUG: print "X+Y=", x+y
			if c.ENABLE_DEBUG: print "X", x,"","Y", y
			m[dest] = x + y
		elif f_op == c.ops["shift"]:
			y = abs(y)
			y %= sys.maxint
			
			if xor_z == 1:
				m[dest] = restricted_left_shift(x, y, c.NUM_BITS)	 #shift left
			else:  #shift right
				m[dest] = x >> y
		elif f_op == c.ops["cshift"]:
			y = abs(y)
			y %= sys.maxint
			
			if xor_z == 1:
				m[dest] = restricted_circ_left_shift(x, y, c.NUM_BITS)
			else:
				m[dest] = restricted_circ_right_shift(x, y, c.NUM_BITS)
				
		elif f_op == c.ops["addifeq"]:
			if x == y:
				m[dest] = m[dest] + z
		elif f_op == c.ops["addifneq"]:
			if x != y:
				m[dest] = m[dest] + z
		elif f_op == c.ops["addiflt"]:
			if x < y:
				m[dest] = m[dest] + z
		
		elif f_op == c.ops["setifeq"]:
			if x == y:
				m[dest] = z
		elif f_op == c.ops["setiflt"]:
			if x < y:
				m[dest] = z
		
		elif f_op == c.ops["iterinput"]:
			
		elif f_op == c.ops["halt"]:
