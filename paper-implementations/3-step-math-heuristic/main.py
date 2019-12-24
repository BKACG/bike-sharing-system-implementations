from Problem import Problem
from Clustering import Clustering

def main():
	D = 20
	problem = Problem('problem.txt', D)
	problem.clustering()
	print(problem.cluster)
	pass

if __name__ == "__main__":
	main()