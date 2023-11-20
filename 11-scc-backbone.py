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
import pickle as pk

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
    wGgraphml = 'networks/{folder:s}/backbone_lscc.graphml'.format(folder=folder)
    wFdistortion = 'networks/{folder:s}/distortion_lscc.pickle'.format(folder=folder)
    #wFasymmetry = 'networks/{folder:s}/asymmetry.pickle'.format(folder=folder)
    
    # Load Network
    rGfile = 'networks/{folder:s}/network_lscc.graphml'.format(folder=folder) 

    # Load graph
    print("Loading network: {network:s}".format(network=network))
    Go = nx.read_graphml(rGfile)
    
    #
    # Asymmetry distribution
    #
    #alpha = get_asymmetry_distribution(Go)
    
    # Dictionary of distortion distribution
    distortion_dist = dict()
    #
    # Metric computation
    #
    G, s_values = dc.backbone(Go, weight='distance', kind='metric', distortion=True)
    distortion_dist['metric'] = s_values
    nx.set_edge_attributes(G, name='metric', values=True)
    #
    # Ultrametric computation
    #
    U, s_values = dc.backbone(Go, weight='distance', kind='ultrametric', distortion=True)
    distortion_dist['ultrametric'] = s_values
    nx.set_edge_attributes(G, name='ultrametric', values={(u, v): U.has_edge(u, v) for u, v in G.edges()})
        
    print('--- Exporting Formats ---')
    ensurePathExists(wGgraphml)
    ensurePathExists(wFdistortion)
    #ensurePathExists(wFasymmetry)

    print('> Backbone')
    nx.write_graphml(G, wGgraphml)
    print('> Distortion')
    pk.dump(distortion_dist, open(wFdistortion, 'wb'))
    #print('> Asymmetry')
    #pk.dump(alpha, open(wFasymmetry, 'wb'))
    
    print('\n\n')
    
    wGstats = 'networks/{folder:s}/network_lscc-stats.csv'.format(folder=folder)
    
    # Calculate stats
    n_nodes = Go.number_of_nodes()
    n_edges = Go.number_of_edges()

    density = nx.density(Go)
    
    n_edges_metric = G.number_of_edges()
    n_edges_ultrametric = U.number_of_edges()
    
    # to Result Series
    sR = pd.Series({
        'n_nodes': n_nodes,
        'nedges': n_edges,
        #
        'density': density,
        #
        #'n-edges-metric': n_edges_metric,
        #'n-edges-ultrametric': n_edges_ultrametric,
        #
        'nedges_metric': n_edges_metric,
        'nedges_ultrametric': n_edges_ultrametric,
        #
        #'%-redundancy-metric': 1 - (n_edges_metric / n_edges),
        #'%-redundancy-ultrametric': 1 - (n_edges_ultrametric / n_edges),
        #
        'ultra_per_metric': (n_edges_ultrametric / n_edges_metric),
        #
    }, name=network, dtype='object')

    # Print
    print(sR)
    sR.to_csv(wGstats)
    #print('> Asymmetry')
    #pk.dump(alpha, open(wFasymmetry, 'wb'))
    print("\n\n")
