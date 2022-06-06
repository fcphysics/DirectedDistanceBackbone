import networkx as nx
import pandas as pd
import numpy as np

import scipy.io as sio


def Str2Dist(p):
	return ( (1./p) - 1 )

def main():

	fname = 'SAND_TM_Estimation_Data.mat'
	MATF = sio.loadmat(fname)
	Y = np.matmul(MATF['A'], np.transpose(MATF['X']))
	G = nx.DiGraph()
	for i in range(Y.shape[0]):
		source = MATF['edgenames'][i][0][0][1:5]
		target = MATF['edgenames'][i][0][0][6:10]
		weight = np.sum(Y[0])
		if source != target:
			G.add_edge(source, target, distance=weight)
	
	lwcc = max(nx.weakly_connected_components(G), key=len) # Get the largest connected component
	G = G.subgraph(lwcc)
	#G.remove_edges_from(nx.selfloop_edges(G))

	nx.write_gpickle(G.copy(), "network.gpickle")	
	

if __name__ == "__main__":
	main()