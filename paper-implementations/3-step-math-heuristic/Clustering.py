import numpy as np
from Problem import Problem

class Clustering:

	def __init__(self, problem, D):
		self.problem = problem
		self.infty = sum(problem.c)
		self.D = D

	def cluster_union(self, i, j):
		self.cluster[i] = self.cluster[i].union(self.cluster[j])
		self.cluster_bike[i] += self.cluster_bike[j]
		self.cluster.pop(j)
		self.cluster_bike.pop(j)

	def diameter(self, i, j):
		problem = self.problem
		d = 0
		for x in self.cluster[i]:
			for y in self.cluster[j]:
				d = max(d, problem.t[x][y], problem.t[y][x])
		return d

	def cost(self, cluster, total_bike):
		problem = self.problem
		ss = np.zeros(problem.N + 1)
		for i in range(1, total_bike + 1):
			max_reduce_cost = -self.infty
			best_sel = -1
			for j in cluster:
				tmp_cost = problem.f(j, ss[j]) - problem.f(j, ss[j] + 1)
				if tmp_cost > max_reduce_cost:
					max_reduce_cost = tmp_cost
					best_sel = j
			if best_sel != -1:
				ss[best_sel] += 1
		return sum([problem.f(i, ss[i]) for i in cluster])

	def cal_saving(self, i, j):
		CI = self.cost(self.cluster[i], self.cluster_bike[i])
		CJ = self.cost(self.cluster[j], self.cluster_bike[j])
		union_cluster = set().union(self.cluster[i], self.cluster[j])
		union_cluster_bike = self.cluster_bike[i] + self.cluster_bike[j]
		CIJ = self.cost(union_cluster, union_cluster_bike)
		return CI + CJ - CIJ


	def clustering(self):
		problem = self.problem
		self.cluster = []
		self.cluster_bike = []
		for i in range(1, problem.N + 1):
			self.cluster.append(set([i]))
			self.cluster_bike.append(problem.s0[i])
		while True:
			max_saving = -self.infty
			best_union = None
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