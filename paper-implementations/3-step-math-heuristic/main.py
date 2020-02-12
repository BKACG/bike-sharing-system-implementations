import time
from Problem import Problem
from Clustering import Clustering

from ArcIndexedFormulation import ArcIndexedFormulation

def main():
	problem = Problem()
	clusters = Clustering(problem)
	clusters.clustering()
	# print(clusters.cluster)


	clusters.shortage = []
	clusters.stations_shortage = []
	tmp_stations_shortage = {}

	for i_cluster in range(len(clusters.cluster)):
		cluster = clusters.cluster[i_cluster]
		clusters.shortage.append(0)
		for station in cluster:
			(_, min_idx) = min((v, i) for i, v in enumerate(problem.f[station]))
			clusters.shortage[i_cluster] += problem.s0[station] - min_idx
			tmp_stations_shortage[station] = problem.s0[station] - min_idx
	
	(_, min_idx) = min((v, i) for i, v in enumerate(problem.f[0]))
	tmp_stations_shortage[0] = problem.s0[0] - min_idx
	for idx in range(problem.N):
		clusters.stations_shortage.append(tmp_stations_shortage[idx])

	clusters.cluster_path = []
	clusters.cluster_path_length = []
	clusters.cluster_pen = []
	clusters.cluster_lud = []
	clusters.cluster_internal_time = []
	for i_cluster in range(len(clusters.cluster)):
		tmp_path = []
		best_path = []
		num_bikes = max(0, -clusters.shortage[i_cluster])
		best_path, pl = find_path(clusters, num_bikes, clusters.cluster[i_cluster], tmp_path, best_path)
		clusters.cluster_path.append(best_path)
		clusters.cluster_path_length.append(pl)
		# print(pl, problem.T * (problem.V - 0.5) / problem.N * len(clusters.cluster[i_cluster]))
		limit = max(0, problem.T * (problem.V - 0.5) / problem.N * len(clusters.cluster[i_cluster]) - pl)
		# print(limit)
		clusters.cluster_pen.append(0)
		tmp_s = []
		clusters.cluster_lud.append([])
		clusters.cluster_internal_time.append(0)
		for station in clusters.cluster_path[i_cluster]:
			tmp_s.append(clusters.problem.s0[station])
			clusters.cluster_lud[i_cluster].append(clusters.problem.s0[station])
		load_unload_decision(clusters, i_cluster, limit, tmp_s, 0)
		clusters.cluster_internal_time[i_cluster] = limit - clusters.cluster_internal_time[i_cluster]
		# print(clusters.cluster_internal_time[i_cluster])
		clusters.cluster_internal_time[i_cluster] += clusters.cluster_path_length[i_cluster]
		clusters.cluster_internal_time[i_cluster] = max(0, clusters.cluster_internal_time[i_cluster])

	print(clusters.cluster_internal_time)
	print(clusters.cluster_pen)


def find_path(clusters, num_bikes, cluster, tmp_path, best_path):
	if (len(tmp_path) == len(cluster)):
		t1 = path_length(clusters, tmp_path)
		t2 = path_length(clusters, best_path)
		if (t1 < t2) or (len(best_path) == 0):
			best_path = []
			for i in tmp_path:
				best_path.append(i)
		return best_path, min(t1, t2)
	pl = 0
	for i in cluster:
		if (i not in tmp_path) and (num_bikes + clusters.stations_shortage[i] in range(clusters.problem.k[0] + 1)):
			tmp_path.append(i)
			best_path, pl = find_path(clusters, num_bikes + clusters.stations_shortage[i], cluster, tmp_path, best_path)
			tmp_path.pop(-1)
	return best_path, pl

def load_unload_decision(clusters, i_cluster, limit, tmp_s, x):
	cluster = clusters.cluster[i_cluster]
	cluster_path = clusters.cluster_path[i_cluster]
	if x == len(cluster_path) or limit < 0:
		t1 = pen(clusters, i_cluster, tmp_s)
		t2 = pen(clusters, i_cluster, clusters.cluster_lud[i_cluster])
		if (t1 < t2) or (len(clusters.cluster_lud[i_cluster]) == 0):
			clusters.cluster_internal_time[i_cluster] = limit
			clusters.cluster_pen[i_cluster] = t1
			for i in range(len(tmp_s)):
				clusters.cluster_lud[i_cluster][i] = tmp_s[i]
		return
	c = cluster_path[x]
	r = range(min(0, clusters.stations_shortage[c]), max(0, clusters.stations_shortage[c]))
	for l in r:
		tmp = limit
		if (tmp_s[x] - l) in range(clusters.problem.c[clusters.cluster_path[i_cluster][x]]):
			if (l > 0):
				tmp -= l * clusters.problem.L
			else:
				tmp -= l * clusters.problem.U
			if tmp >= 0:
				tmp_s[x] -= l
				load_unload_decision(clusters, i_cluster, tmp, tmp_s, x+1)
				tmp_s[x] += l

def path_length(clusters, path):
	tmp = 0
	for i in range(1, len(path)):
		tmp += clusters.problem.t[path[i-1]][path[i]]
	return tmp

def pen(clusters, i_cluster, s):
	tmp = 0
	pen = 0
	for i in range(len(s)):
		tmp_station = clusters.cluster_path[i_cluster][i]
		pen += clusters.problem.f[tmp_station][s[i]]
	for i in clusters.cluster[i_cluster]:
		if i not in (s):
			tmp_station = i
			tmp_station = clusters.problem.f[tmp_station][clusters.problem.s0[tmp_station]]
	return pen

if __name__ == "__main__":
	second = time.time()
	main()
	print(time.time() - second)