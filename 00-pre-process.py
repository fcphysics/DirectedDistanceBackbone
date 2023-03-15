# coding=utf-8
# Authors: Rion B. Correia & Felipe Xavier Costa
# Date: Feb 21, 2023
#
# Description: Reads a network and computes its backbone and distortion.
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
import distanceclosure as dc
from distanceclosure.utils import prox2dist
from distanceclosure.utils import dist2prox
# Utils
from utils import ensurePathExists, get_asymmetry_distribution


# For networkx 2.0+
import pickle as pk
def read_gpickle(file_name):
    with open(file_name, 'rb') as f:
        G = pk.load(f)
    return G


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
    wGgraphml = 'networks/{folder:s}/network.graphml'.format(folder=folder)
    
    # Load Network
    print("Loading network: {network:s}".format(network=network))
    rGfile = 'networks/{folder:s}/network.gpickle'.format(folder=folder)

    # Load graph (networkx 1.x)
    # G = nx.read_gpickle(rGfile)
    # Load graph (networkx 2.0+)
    G = read_gpickle(rGfile)

    # Remove self-loops
    print('Remove self-loops')
    G.remove_edges_from(list(nx.selfloop_edges(G)))

    # Keep only largest connected component
    print('Keep largest connected component')
    G = G.subgraph(max(nx.weakly_connected_components(G), key=len)).copy()

    if weight_type in 'proximity':

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
    nx.set_edge_attributes(G, name='distance', values=D_dict)
    
    print('> Network')
    nx.write_graphml(G, wGgraphml)
    