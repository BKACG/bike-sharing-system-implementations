import numpy as np
from Problem import Problem

class Clustering:

	def __init__(self, problem, D):
		self = problem
		self.D = D

	def cluster_union(self, i, j):
		self.cluster[i] = self.cluster[i].union(self.cluster[j])
		self.cluster_bike[i] += self.cluster_bike[j]
		self.cluster.pop(j)
		self.cluster_bike.pop(j)

	def diameter(self, i, j):
		d = 0
		for x in self.cluster[i]:
			for y in self.cluster[j]:
				d = max(d, t[x][y], t[y][x])
		return d

	def cost(self, cluster, total_bike):
		ss = np.zeros(self.n)
		for i in range(1, total_bike):
			min_cost = self.infty
			best_sel = -1
			for j in cluster:
				tmp_cost = self.f(j, ss[j] + 1)
				if tmp_cost < min_cost:
					min_cost = tmp_cost
					best_sel = j
			ss[best_sel] += 1
		return sum([self.f(i, ss[i]) for i in s])

	def cal_saving(self, i, j):
		CI = cost(self.cluster[i], self.cluster_bike[i])
		CJ = cost(self.cluseter[j], self.cluster_bike[j])
		CIJ = cost(set().union(self.cluster[i], self.cluseter[j]), self.cluster_bike[i] + self.cluster_bike[j])
		return CI + CJ - CIJ


	def clustering(self):
		self.cluster = []
		self.cluster_bike = []
		for i in range(1, self.N + 1):
			self.cluster.append(set([i]))
			self.cluster_bike.append(self.s0[i])
		while True:
			max_saving = -1
			best_union = (-1, -1)
			for i in range(len(self.cluster)):
				for j in range(i + 1, len(self.cluster)):
					if (diameter(i, j) > self.D):
						continue
					tmp_saving = cal_saving(i, j)
					if (tmp_saving > max_saving):
						max_saving = tmp_saving
						best_union = (i, j)
			if max_saving == -1:
				break
			cluster_union(*best_union)