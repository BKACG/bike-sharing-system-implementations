import time
from Problem import Problem
from Clustering import Clustering

from ArcIndexedFormulation import ArcIndexedFormulation

def main():
	problem = Problem()
	clusters = Clustering(problem)
	clusters.clustering()
	print(len(clusters.cluster))
	m = 0
	c = 0
	for i in clusters.cluster:
		m = max(m, len(i))
		if (len(i) == 1):
			c += 1
	print(m)
	print(c)

main()