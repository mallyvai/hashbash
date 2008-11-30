collision_seed = 5498

class Stage:
	def __init__(self, attempts, lower, upper, collisions):
		self.attempts = attempts
		self.lower = lower
		self.upper = upper
		self.collisions = collisions

trivial = Stage(20, -10, 10, 0)
one = Stage(100, -100000, 100000, 0)
two = Stage(100, 30, 80, 0)