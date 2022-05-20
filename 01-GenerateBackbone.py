import networkx as nx
import numpy as np
import distanceclosure as dc
import pandas as pd

from pprint import pprint

def main():

	NetPath = 'networks/'
	
	data = {'NetName': [], 
	'NNode': [], 'NEdges': [],
	'NMetric': [], 'NUltra': [] }

	#df = pd.DataFrame()

	print("Biological Nets")
	folder = "biological/"

	bio_nets = ['comorbidity.gpickle', 'hostpathogen.gpickle']

	for net in bio_nets:
		#print(net)
		data['NetName'].append(net)
		G = nx.read_gpickle(NetPath+folder+net)
		G.remove_edges_from(list(nx.selfloop_edges(G)))
		data['NNode'].append(G.number_of_nodes())
		data['NEdges'].append(G.number_of_edges())
		GC = dc.distance_closure(G, kind='metric', weight='distance', only_backbone=True)
		metric_edges = list(nx.get_edge_attributes(GC, 'is_metric').values())
		data['NMetric'].append(np.sum(metric_edges))
		GC = dc.distance_closure(G, kind='ultrametric', weight='distance', only_backbone=True)
		metric_edges = list(nx.get_edge_attributes(GC, 'is_ultrametric').values())
		data['NUltra'].append(np.sum(metric_edges))

	#pprint(data)

	print("Social Nets")
	folder = "social/"

	soc_nets = ['calls_duration.gpickle', 'giraffe_affiliative.gpickle']
	
	for net in soc_nets:
		data['NetName'].append(net)
		G = nx.read_gpickle(NetPath+folder+net)
		G.remove_edges_from(list(nx.selfloop_edges(G)))
		data['NNode'].append(G.number_of_nodes())
		data['NEdges'].append(G.number_of_edges())
		GC = dc.distance_closure(G, kind='metric', weight='distance', only_backbone=True)
		metric_edges = list(nx.get_edge_attributes(GC, 'is_metric').values())
		data['NMetric'].append(np.sum(metric_edges))
		GC = dc.distance_closure(G, kind='ultrametric', weight='distance', only_backbone=True)
		metric_edges = list(nx.get_edge_attributes(GC, 'is_ultrametric').values())
		data['NUltra'].append(np.sum(metric_edges))


	print("Technological Nets")
	folder = "technological/"

	tech_nets = ['avg_trip_duration.gpickle', 'PoP_volume_flow.gpickle', 'water_pipes.gpickle']

	for net in tech_nets:
		data['NetName'].append(net)
		G = nx.read_gpickle(NetPath+folder+net)
		G.remove_edges_from(list(nx.selfloop_edges(G)))
		data['NNode'].append(G.number_of_nodes())
		data['NEdges'].append(G.number_of_edges())
		GC = dc.distance_closure(G, kind='metric', weight='distance', only_backbone=True)
		metric_edges = list(nx.get_edge_attributes(GC, 'is_metric').values())
		data['NMetric'].append(np.sum(metric_edges))
		GC = dc.distance_closure(G, kind='ultrametric', weight='distance', only_backbone=True)
		metric_edges = list(nx.get_edge_attributes(GC, 'is_ultrametric').values())
		data['NUltra'].append(np.sum(metric_edges))

	df = pd.DataFrame.from_dict(data)
	df.to_csv("DirectedBackbone.csv")

if __name__ == "__main__":
	main()