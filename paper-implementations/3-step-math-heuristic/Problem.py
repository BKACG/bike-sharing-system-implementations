import numpy as np

class Problem:
	def __init__(self, file_name):
		f = open(file_name, "r")
		self.N = 200
		self.c = [int(i) for i in f.readline().split(' ')]
		# self.ld = [int(i) for i in f.readline().split(' ')]
		# self.ud = [int(i) for i in f.readline().split(' ')]
		self.s0 = [int(i) for i in f.readline().split(' ')]
		self.V = int(f.readline())
		self.k = [int(i) for i in f.readline().split(' ')]
		self.L = int(f.readline())
		self.U = int(f.readline())

		self.t = []
		for i in range(self.N + 1):
			ti = [int(ii) for ii in f.readline().split(' ')]
			self.t.append(ti)
		self.t = np.array(self.t)
		
		self.alpha = float(f.readline())
		self.T = int(f.readline())

	def f(self, i, s):
		if s > self.c[i] or s < 0:
			return self.infty
		if s >= self.ld[i] and s <= self.ud[i]:
			return 0
		return min(abs(s - self.ld[i]), abs(s - self.ud[i])) / (self.ud[i] - self.ld[i] + 1)
		