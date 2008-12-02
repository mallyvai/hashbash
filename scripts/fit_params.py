collision_seed = 5498

class Stage:
	def __init__(self, attempts, lower, upper, collisions):
		self.attempts = attempts
		self.lower = lower
		self.upper = upper
		self.collisions = collisions

trivial = Stage(20, -10, 10, 0)
one = Stage(50, -100000, 100000, 0)
two = Stage(50, 30, 80, 0)
three = Stage(50, 1, 2**200, 0)