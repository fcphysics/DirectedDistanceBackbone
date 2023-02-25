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
    wGgraphml = 'networks/{folder:s}/backbone.graphml'.format(folder=folder)
    wFdistortion = 'networks/{folder:s}/distortion.pickle'.format(folder=folder)
    wFasymmetry = 'networks/{folder:s}/asymmetry.pickle'.format(folder=folder)

    # Load Network
    print("Loading network: {network:s}".format(network=network))
    rGfile = 'networks/{folder:s}/network.graphml'.format(folder=folder)

    # Load graph
    G = nx.read_graphml(rGfile)
    
    #
    # Asymmetry distribution
    #
    alpha = get_asymmetry_distribution(G)
    
    # Dictionary of distortion distribution
    distortion_dist = dict()
    #
    # Metric computation
    #
    G, s_values = dc.backbone(G, weight='distance', kind='metric', distortion=True)
    distortion_dist['metric'] = s_values
    nx.set_edge_attributes(G, name='metric', values=True)
    #
    # Ultrametric computation
    #
    U, s_values = dc.backbone(G, weight='distance', kind='ultrametric', distortion=True)
    distortion_dist['ultrametric'] = s_values
    nx.set_edge_attributes(G, name='ultrametric', values={edg: True for edg in U.edges()})
        
    print('--- Exporting Formats ---')
    ensurePathExists(wGgraphml)
    ensurePathExists(wFdistortion)
    ensurePathExists(wFasymmetry)

    print('> Backbone')
    nx.write_graphml(G, wGgraphml)
    print('> Distortion')
    pk.dump(distortion_dist, open(wFdistortion, 'wb'))
    print('> Asymmetry')
    pk.dump(alpha, open(wFasymmetry, 'wb'))
    print('\n\n')
