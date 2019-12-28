from pulp import *
import numpy as np

class ArcIndexedFormulation:
	def __init__(self, problem = None):
		self.problem = problem
		N = problem['N']
		V = problem['V']
		s0 = problem['s0']
		c = problem['c']
		k = problem['k']
		f = problem['f']
		t = problem['t']
		alpha = problem['alpha']
		T = problem['T']
		L = problem['L']
		U = problem['U']

		x = self.x = []
		y = self.y = []
		trans_fee = self.trans_fee = None
		yL = self.yL = []
		yU = self.yU = []
		q = self.q = []
		s = self.s = []
		g = self.g = []
		self.allDV = [x, y, yL, yU, q, s, g]
		for i in range(len(N)):
			x.append([])
			y.append([])
			yL.append([])
			yU.append([])
			q.append([])
			for j in range(len(N)):
				x[i].append([])
				y[i].append([])
				for v in range(len(V)):
					var_name = 'x_{' + ','.join([str(N[i]), str(N[j]), str(V[v])]) + '}'
					x[i][j].append(LpVariable(var_name, cat = 'Binary'))
					trans_fee += t[i][j] * x[i][j][v]
					var_name = 'y_{' + ','.join([str(N[i]), str(N[j]), str(V[v])]) + '}'
					y[i][j].append(LpVariable(var_name, cat = 'Integer', lowBound = 0, upBound = k[v]))
			for v in range(len(V)):
				var_name = 'yL_{' + ','.join([str(N[i]), str(V[v])]) + '}'
				yL[i].append(LpVariable(var_name, cat = 'Integer', lowBound = 0, upBound = k[v]))
				var_name = 'yU_{' + ','.join([str(N[i]), str(V[v])]) + '}'
				yU[i].append(LpVariable(var_name, cat = 'Integer', lowBound = 0, upBound = k[v]))
				var_name = 'q_{' + ','.join([str(N[i]), str(V[v])]) + '}'
				q[i].append(LpVariable(var_name, cat = 'Integer', lowBound = 0, upBound = k[v]))
			var_name = 's_{' + str(i) + '}'
			s.append(LpVariable(var_name, cat = 'Integer', lowBound = 0, upBound = c[i]))
			var_name = 'g_{' + str(i) + '}'
			g.append(LpVariable(var_name, cat = 'Continuous'))
		M = self.M = sum(c)

		objectiveFunction = self.objectiveFunction = sum(g) + alpha * trans_fee
		objective = self.objective = LpMinimize

		constraints = self.constraints = []

		for i in range(len(N)):
			constraints.append(s[i] == s0[i] - sum([yL[i][v] - yU[i][v] for v in range(len(V))]))
		for i in range(len(N)):
			for v in range(len(V)):
				tij = []
				tji = []
				for j in range(len(N)):
					if j != i:
						tij.append(y[i][j][v])
						tji.append(y[j][i][v])
				constraints.append(yL[i][v] - yU[i][v] == sum(tij) - sum(tji))
		for i in range(len(N)):
			for j in range(len(N)):
				if j != i:
					for v in range(len(V)):
						constraints.append(y[i][j][v] <= k[v] * x[i][j][v])
		for i in range(len(N)):
			for v in range(len(V)):
				tij = []
				tji = []
				for j in range(len(N)):
					if j != i:
						tij.append(x[i][j][v])
						tji.append(x[j][i][v])
				constraints.append(sum(tij) == sum(tji))
		for i in range(len(N)):
			for v in range(len(V)):
				tij = []
				for j in range(len(N)):
					if j != i:
						tij.append(x[i][j][v])
				constraints.append(sum(tij) <= 1)
		for i in range(len(N)):
			constraints.append(sum(yL[i]) <= s0[i])
		for i in range(len(N)):
			constraints.append(sum(yU[i]) <= c[i] - s0[i])
		for v in range(len(V)):
			constraints.append(sum(yL[:][v]) - sum(yU[:][v]) == 0)
		for v in range(len(V)):
			tmp = []
			for i in range(len(N)):
				for j in range(len(N)):
					if i != j:
						tmp.append(t[i][j] * x[i][j][v])
			constraints.append(L * (sum(yL[:][v]) + sum(y[0][:][v])) + U * (sum(yU[:][v]) + sum(y[:][0][v])) + sum(tmp) <= T)
		for j in range(len(N)):
			for v in range(len(V)):
				for i in range(len(N)):
					if i != j:
						constraints.append(q[j][v] >= q[i][v] + 1 - M * (1 - x[i][j][v]))
		for i in range(len(N)):
			for u in range(c[i]):
				tb = f(i, u + 1) - f(i, u)
				ta = f(i, u) - tb
				constraints.append(g[i] >= ta + tb * s[i])

	def solve(self):
		lpProblem = LpProblem('arcIndexedFormulation', self.objective)
		lpProblem += self.objectiveFunction
		for constraint in self.constraints:
			lpProblem += constraint
		return lpProblem.solve()