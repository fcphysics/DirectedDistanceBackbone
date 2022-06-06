import networkx as nx
import pandas as pd
import numpy as np

def Str2Dist(p):
	return ( (1./p) - 1 )

def main():

	# Water Pipes
	df = pd.read_table('exnet_pipes.txt')
	names = df.columns
	G = nx.from_pandas_edgelist(df, source=names[1], target=names[2], edge_attr=names[3], create_using=nx.DiGraph)
	dist = nx.get_edge_attributes(G, names[3])
	nx.set_edge_attributes(G, dist, "distance")
	G.remove_edges_from(nx.selfloop_edges(G))

	lwcc = max(nx.weakly_connected_components(G), key=len) # Get the largest connected component
	G = G.subgraph(lwcc)

	dfm = pd.read_table('exnet_junct.txt')

	nx.set_node_attributes(G, name='label', values=dfm['Node'])
	nx.set_node_attributes(G, name='X', values=dfm['X-Coord'])
	nx.set_node_attributes(G, name='Y', values=dfm['Y-Coord'])

	nx.write_gpickle(G.copy(), "network.gpickle")

if __name__ == "__main__":
	main()