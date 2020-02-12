import numpy as np
import csv

class Problem:
	def __init__(self):
		self.N = 50

		penalties_file = open('penalties.csv')
		penalties = csv.reader(penalties_file)

		capacities_file = open('capacities.csv')
		capacities = csv.reader(capacities_file)
		self.c = []
		for row in capacities:
			for col in row:
				self.c.append(int(col))
		self.infty = sum(self.c)

		self.f = []
		for row in penalties:
			tmp_row = []
			for col in row:
				tmp_col = float(col)
				if tmp_col <= 0:
					tmp_col = self.infty
				tmp_row.append(tmp_col)
			self.f.append(tmp_row)

		initial_file = open('real.csv')
		initial = csv.reader(initial_file)
		self.s0 = []
		for row in initial:
			for col in row:
				self.s0.append(int(col))

		self.V = 2
		self.k = []
		for i in range(self.V):
			self.k.append(25)

		self.L = 60
		self.U = 60

		distances_file = open('distances.csv')
		distances = csv.reader(distances_file)
		self.t = []
		for row in distances:
			tmp_row = []
			for col in row:
				tmp_row.append(int(col))
			self.t.append(tmp_row)

		self.alpha = 1/900
		self.T = 18000

		self.D = 800