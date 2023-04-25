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
# Utils
from utils import ensurePathExists
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
   
    # Files
    wGgraphml = 'networks/{folder:s}/undirected_backbones.pickle'.format(folder=folder)
    wFdistortion = 'networks/{folder:s}/undirected_distortions.pickle'.format(folder=folder)

    # Load Network
    print("Loading network: {network:s}".format(network=network))
    rGfile = 'networks/{folder:s}/undirected_networks.pickle'.format(folder=folder)
    G = pk.load(open(rGfile, 'rb'))
    
    # Dictionary of distortion distribution
    distortion_dist = {'min': dict(), 'max': dict(), 'avg': dict()}
    
    for type in ['min', 'max', 'avg']:
        print(type)
                #
        # Metric computation
        #
        G[type], s_values = dc.backbone(G[type], weight='distance', kind='metric', distortion=True)
        distortion_dist[type]['metric'] = s_values
        #
        # Ultrametric computation
        #
        U, s_values = dc.backbone(G[type], weight='distance', kind='ultrametric', distortion=True)
        distortion_dist[type]['ultrametric'] = s_values
        nx.set_edge_attributes(G[type], name='ultrametric', values={(u, v): U.has_edge(u, v) for u, v in G[type].edges()})
            
    print('--- Exporting Formats ---')
    ensurePathExists(wGgraphml)
    ensurePathExists(wFdistortion)

    print('> Backbone')
    pk.dump(G, open(wGgraphml, 'wb'))
    print('> Distortion')
    pk.dump(distortion_dist, open(wFdistortion, 'wb'))        
    print('\n')
