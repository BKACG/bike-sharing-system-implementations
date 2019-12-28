from Problem import Problem
from Clustering import Clustering

from ArcIndexedFormulation import ArcIndexedFormulation

def main():
	D = 20
	problem = Problem('problem.txt')
	clusters = Clustering(problem, D)
	clusters.clustering()
	# print(clusters.cluster)
	aif = ArcIndexedFormulation({"N": [0, 1, 2, 3, 4],
		"V": [1, 2, 3, 4],
		'k': [5, 5, 5, 5],
		'c': [10, 10, 10, 10, 10],
		's0': [5, 5, 5, 5, 5],
		't': [[1, 2, 3, 4, 5],
		[1, 2, 3, 4, 5],
		[1, 2, 3, 4, 5],
		[1, 2, 3, 4, 5],
		[1, 2, 3, 4, 5]],
		'alpha': 0.3,
		'T': 100,
		'U': 1,
		'L': 1,
		'f': problem.f})
	aif.solve()

if __name__ == "__main__":
	main()