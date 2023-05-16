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
    wGstats = 'networks/{folder:s}/network-stats.csv'.format(folder=folder)
    #wFasymmetry = 'networks/{folder:s}/backbone_asymmetry.pickle'.format(folder=folder)

    # Load graph
    G = nx.read_graphml(rGfile)
    
    # Calculate stats
    wcc_nodes = G.number_of_nodes()
    wcc_edges = G.number_of_edges()

    density = nx.density(G)
    
    LSCC = G.subgraph(max(nx.strongly_connected_components(G), key=len))
    
    lscc_nodes = LSCC.number_of_nodes()
    lscc_edges = LSCC.number_of_edges()
        
    # Load backbone
    G = nx.read_graphml(rBfile)
    # Metric
    tau_wcc_metric = G.number_of_edges()/wcc_edges
    # Ultrametric AND LSCC
    tau_wcc_ultrametric = 0 #sum([int(d) for _, _, d in G.edges(data='ultrametric')])/wcc_edges
    tau_lscc_metric = 0
    tau_lscc_ultrametric = 0
    for u, v, ultra in G.edges(data='ultrametric'):
        if LSCC.has_edge(u, v):
            tau_lscc_metric += 1
        if ultra:
            tau_wcc_ultrametric += 1
            if LSCC.has_edge(u, v):
                tau_lscc_ultrametric += 1
    
    tau_wcc_ultrametric /= wcc_edges
    if lscc_edges > 0.0:
        tau_lscc_ultrametric /= lscc_edges
        tau_lscc_metric /= lscc_edges
    
    # to Result Series
    sR = pd.Series({
        'n-nodes': wcc_nodes,
        'n-edges': wcc_edges,
        #
        'density': density,
        #
        'LSCC-nodes': lscc_nodes,
        'LSCC-edges': lscc_edges,
        #
        'tau-metric': tau_wcc_metric,
        'tau-ultrametric': tau_wcc_ultrametric,
        #
        'LSCC-tau-metric': tau_lscc_metric,
        'LSCC-tau-ultrametric': tau_lscc_ultrametric,
        #
        'ultrametric_metric_ratio': (tau_wcc_ultrametric/tau_wcc_metric),
        'LSCC-ultrametric_metric_ratio': (tau_lscc_ultrametric/tau_lscc_metric if tau_lscc_metric > 0 else 0),
        #
    }, name=network, dtype='object')

    # Print
    print(sR)
    sR.to_csv(wGstats)
    #print('> Asymmetry')
    #pk.dump(alpha, open(wFasymmetry, 'wb'))
    print("\n\n")
