# coding=utf-8
# Author: Rion B Correia
# Date: Dec 07, 2020
#
# Description: Reads a network and computes closure.
#
#
import gc
import numpy as np
import pandas as pd
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
import networkx as nx
import argparse
import configparser
# Distance Closure
from distanceclosure.dijkstra import all_pairs_dijkstra_path_length
from distanceclosure.utils import prox2dist
from distanceclosure.utils import dist2prox
# Utils
from utils import ensurePathExists


def jaccard(cij, ci, cj, min_support=0):
    if (ci + cj - cij) >= min_support:
        return cij / (ci + cj - cij)
    else:
        return 0.


if __name__ == '__main__':

    #
    # Init
    #
    config = configparser.ConfigParser()
    config.read('networks.ini')
    networks = list(config.keys())[1:]

    #
    # Args
    #
    parser = argparse.ArgumentParser()
    parser.add_argument("--network", default='bike-sharing', type=str, choices=networks, help="Network name.")
    args = parser.parse_args()

    # Arguments
    network = args.network
    
    # Settings
    settings = config[network]
    folder = settings.get('folder')
    weight_type = settings.get('weight-type')
    weight_attr = settings.get('weight-attr')
    norm_min_support = 10

    # Files
    wGgraphml = 'networks/{folder:s}/network-closure.graphml'.format(folder=folder)
    wGpickle = 'networks/{folder:s}/network-closure.gpickle'.format(folder=folder)

    # Load Network
    print("Loading network: {network:s}".format(network=network))
    rGfile = 'networks/{folder:s}/network.gpickle'.format(folder=folder)

    # Load graph
    G = nx.read_gpickle(rGfile)

    # Remove self-loops
    #print('Remove self-loops')
    #G.remove_edges_from(list(nx.selfloop_edges(G)))

    # Keep only largest connected component
    #print('Keep largest connected component')
    #G = G.subgraph(max(nx.connected_components(G), key=len)).copy()

    if weight_type == 'count':

        # Norm
        print('Normalizing')
        counts = {k: sum([d[weight_attr] for i, j, d in G.edges(nbunch=k, data=True)]) for k in G.nodes()}
        C_dict = {(i, j): d[weight_attr] for i, j, d in G.edges(data=True)}
        P_dict = {(i, j): jaccard(ci=counts[i], cj=counts[j], cij=c, min_support=norm_min_support) for (i, j), c in C_dict.items()}
        nx.set_edge_attributes(G, name='proximity', values=P_dict)
        weight_attr = 'proximity'

    if weight_type in ['count', 'proximity']:

        print('Prox -> Dist')
        P_dict = nx.get_edge_attributes(G, weight_attr)
        D_dict = {key: prox2dist(value) for key, value in P_dict.items()}
        nx.set_edge_attributes(G, name='distance', values=D_dict)

    if weight_type == 'distance':

        D_dict = nx.get_edge_attributes(G, name=weight_attr)
        P_dict = {key: dist2prox(value) for key, value in D_dict.items()}

    if (min(P_dict.values()) < 0) or (max(P_dict.values()) > 1.0):
        raise TypeError("Proximity values not in [0,1]")
    if min(D_dict.values()) < 0:
        raise TypeError("Distance values not in [0,inf)")

    # Set weights
    nx.set_edge_attributes(G, name='proximity', values=P_dict)
    nx.set_edge_attributes(G, name='weight', values=P_dict)
    nx.set_edge_attributes(G, name='distance', values=D_dict)

    # Identify original edges
    nx.set_edge_attributes(G, name='is_original', values={ij: True for ij in G.edges()})

    #
    # Metric computation
    #
    c = 1
    for i, metric_distances in all_pairs_dijkstra_path_length(G, weight='distance', disjunction=sum):
        if c % 10 == 0:
            print('> Metric Dijkstra: {c:} of {total:}'.format(c=c, total=G.number_of_nodes()))
        for j, metric_distance in metric_distances.items():

            # Only for existing edges
            if G.has_edge(i, j):
                G[i][j]['metric_distance'] = metric_distance
                G[i][j]['is_metric'] = True if ((metric_distance == G[i][j]['distance']) and (metric_distance != np.inf)) else False
        c += 1

    #
    # Ultrametric computation
    #
    c = 1
    for i, ultrametric_distances in all_pairs_dijkstra_path_length(G, weight='distance', disjunction=max):
        if c % 10 == 0:
            print('> Ultrametric Dijkstra: {c:} of {total:}'.format(c=c, total=G.number_of_nodes()))
        for j, ultrametric_distance in ultrametric_distances.items():

            # Only for existing edges
            if G.has_edge(i, j):
                G[i][j]['ultrametric_distance'] = ultrametric_distance
                G[i][j]['is_ultrametric'] = True if ((ultrametric_distance == G[i][j]['distance']) and (ultrametric_distance != np.inf)) else False
        c += 1

    # Are there any isolates?
    isolates = list(nx.isolates(G))
    print('number of isolates:', len(isolates))

    print('--- Calculating S Values ---')

    S_dict = {
        (i, j): float(d['distance'] / d['metric_distance'])
        for i, j, d in G.edges(data=True)
        if ((d.get('distance') < np.inf) and (d.get('metric_distance') > 0))
    }
    nx.set_edge_attributes(G, name='s-value', values=S_dict)

    print('--- Exporting Formats ---')
    ensurePathExists(wGgraphml)
    ensurePathExists(wGpickle)

    print('> Graphml')
    nx.write_graphml(G, wGgraphml)
    print('> gPickle')
    nx.write_gpickle(G, wGpickle)

