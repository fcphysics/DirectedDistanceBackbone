# coding=utf-8
# Author: Felipe Xavier Costa
# Date: May 3, 2023
#
# Description: Compare backbone inside and outside SCC.
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
    wGstats = 'networks/{folder:s}/components-stats.csv'.format(folder=folder)
    
    # Load graph
    G = nx.read_graphml(rGfile)
    
    LSCC = G.subgraph(max(nx.strongly_connected_components(G), key=len))
            
    # Load backbone
    B = nx.read_graphml(rBfile)
    
    nEmLSCC = 0
    for u, v in B.edges():
        if LSCC.has_edge(u, v):
            nEmLSCC += 1
    
    # to Result Series
    sR = pd.Series({
        'n-nodes': G.number_of_nodes(),
        'n-edges': G.number_of_edges(),
        # Metric
        'n-edges-metric': B.number_of_edges(),
        # LSCC
        'n-nodes-lscc': LSCC.number_of_nodes(),
        'n-edges-lscc': LSCC.number_of_edges(),
        # Metric
        'n-edges-metric-lscc': nEmLSCC,
    }, name=network, dtype='object')
    
    sR.to_csv(wGstats)