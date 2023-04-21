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
    rGraphml = 'networks/{folder:s}/network.graphml'.format(folder=folder)
    wGraphml = 'networks/{folder:s}/undirected_network.graphml'.format(folder=folder)
    
    # Load Network
    print("Loading network: {network:s}".format(network=network))
    G = nx.read_graphml(rGraphml)
    
    nx.set_edge_attributes(G, values=None, name='alpha')
    
    U = nx.Graph()
    U.add_nodes_from(G.nodes())
    
    # Average reciprocal distance
    for u, v, w in G.edges(data=True):
        if w['alpha'] == None:
            if G.has_edge(v, u):
                G[v][u]['alpha'] = 0.0
                U.add_edge(u, v, distance=0.5*(w['distance'] + G[v][u]['distance']))
            else:
                U.add_edge(u, v, distance=w['distance'])

    nx.write_graphml(U, wGraphml)
    print("Done")
    
    