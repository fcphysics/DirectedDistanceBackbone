# coding=utf-8
# Author: Rion B Correia & Felipe Xavier Costa
# Date: Feb 22, 2023
#
# Description: Reads a network and computes backbone size statistics.
#
#
import numpy as np
import pandas as pd
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
#pd.options.display.float_format = '{:.2%}'.format
import networkx as nx
import argparse
import configparser
from utils import get_asymmetry_distribution
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
    #
    network = args.network
    #
    settings = config[network]
    folder = settings.get('folder')
    
    # Files
    rGfile = 'networks/{folder:s}/network.graphml'.format(folder=folder)
    rBfile = 'networks/{folder:s}/backbone.graphml'.format(folder=folder)
    wGstats = 'networks/{folder:s}/network_lscc-stats.csv'.format(folder=folder)
    #wFasymmetry = 'networks/{folder:s}/backbone_asymmetry.pickle'.format(folder=folder)

    # Load graph
    G = nx.read_graphml(rGfile)
    scc_nodes = max(nx.strongly_connected_components(G), key=len)
    G = G.subgraph(scc_nodes)
    
    # Calculate stats
    n_nodes = G.number_of_nodes()
    n_edges = G.number_of_edges()

    density = nx.density(G)
        
    # Load backbone
    # Metric
    G = nx.read_graphml(rBfile)
    G = G.subgraph(scc_nodes)
    
    n_edges_metric = G.number_of_edges()

    # New asymmetry dist
    #alpha = dict()
    #alpha['metric'] = get_asymmetry_distribution(G)
    # Ultrametric
    #edges2remove = [(i, j) for i, j, d in G.edges(data=True) if 'ultrametric' not in d]
    #G.remove_edges_from(edges2remove)
    #n_edges_ultrametric = G.number_of_edges()
    n_edges_ultrametric = sum([int(w) for _, _, w in G.edges(data='ultrametric')])
    #alpha['ultrametric'] = get_asymmetry_distribution(G)
    
    # to Result Series
    sR = pd.Series({
        'n_nodes': n_nodes,
        'n_edges': n_edges,
        #
        'density': density,
        #
        #'n-edges-metric': n_edges_metric,
        #'n-edges-ultrametric': n_edges_ultrametric,
        #
        'tau_metric': (n_edges_metric / n_edges),
        'tau_ultrametric': (n_edges_ultrametric / n_edges),
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
