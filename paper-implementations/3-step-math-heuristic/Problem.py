import numpy as np

class Problem:
	def __init__(self, file_name, D):
		f = open(file_name, "r")
		self.N = int(f.readline())
		self.c = [int(i) for i in f.readline().split(' ')]
		self.infty = sum(self.c)
		self.ld = [int(i) for i in f.readline().split(' ')]
		self.ud = [int(i) for i in f.readline().split(' ')]
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
		self.D = D

	def f(self, i, s):
		if s > self.c[i] or s < 0:
			return self.infty
		if s >= self.ld[i] and s <= self.ud[i]:
			return 0
		return min(abs(s - self.ld[i]), abs(s - self.ud[i])) / (self.ud[i] - self.ld[i] + 1)

	def cluster_union(self, i, j):
		self.cluster[i] = self.cluster[i].union(self.cluster[j])
		self.cluster_bike[i] += self.cluster_bike[j]
		self.cluster.pop(j)
		self.cluster_bike.pop(j)

	def diameter(self, i, j):
		d = 0
		for x in self.cluster[i]:
			for y in self.cluster[j]:
				d = max(d, self.t[x][y], self.t[y][x])
		return d

	def cost(self, cluster, total_bike):
		# print(cluster, total_bike)
		ss = np.zeros(self.N + 1)
		for i in range(1, total_bike + 1):
			max_reduce_cost = -self.infty
			best_sel = -1
			for j in cluster:
				tmp_cost = self.f(j, ss[j]) - self.f(j, ss[j] + 1)
				if tmp_cost > max_reduce_cost:
					max_reduce_cost = tmp_cost
					best_sel = j
			if best_sel != -1:
				ss[best_sel] += 1
		# print(ss, sum([self.f(i, ss[i]) for i in cluster]))
		return sum([self.f(i, ss[i]) for i in cluster])

	def cal_saving(self, i, j):
		CI = self.cost(self.cluster[i], self.cluster_bike[i])
		CJ = self.cost(self.cluster[j], self.cluster_bike[j])
		CIJ = self.cost(set().union(self.cluster[i], self.cluster[j]), self.cluster_bike[i] + self.cluster_bike[j])
		# print(i, j, CI, CJ, CIJ)
		return CI + CJ - CIJ


	def clustering(self):
		self.cluster = []
		self.cluster_bike = []
		for i in range(1, self.N + 1):
			self.cluster.append(set([i]))
			self.cluster_bike.append(self.s0[i])
		while True:
			max_saving = -self.infty
			best_union = (-1, -1)
			for i in range(len(self.cluster)):
				for j in range(i + 1, len(self.cluster)):
					if (self.diameter(i, j) <= self.D):
						tmp_saving = self.cal_saving(i, j)
						if (tmp_saving > max_saving):
							max_saving = tmp_saving
							best_union = (i, j)
			if max_saving < 0:
				break
			self.cluster_union(*best_union)