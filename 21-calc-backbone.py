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
    rUGraphml = 'networks/{folder:s}/undirected_scc_network.graphml'.format(folder=folder)
    rDGraphml = 'networks/{folder:s}/directed_scc_network.graphml'.format(folder=folder)
    
    wFdistortion = 'networks/{folder:s}/undirected_distortions.pickle'.format(folder=folder)
    wGraphml = 'networks/{folder:s}/undirected_{type:s}_backbone.graphml'

    # Dictionary of distortion distribution
    #distortion_dist = {'min': dict(), 'max': dict(), 'avg': dict(), 'harm': dict()}
    distortion_dist = {'max': dict(), 'avg': dict()}
    
    # Load Network
    print("Loading network: {network:s}".format(network=network))
    
    types = ['max', 'avg']
    
    U = nx.read_graphml(rUGraphml)
    for type in types:
        # Metric computation
        B, s_values = dc.backbone(U, weight=f'{type}_distance', kind='metric', distortion=True)
        distortion_dist[type]['metric'] = s_values
        
        # Ultrametric computation
        M, s_values = dc.backbone(U, weight=f'{type}_distance', kind='ultrametric', distortion=True)
        distortion_dist[type]['ultrametric'] = s_values
        
        nx.set_edge_attributes(B, name='ultrametric', values={(u, v): M.has_edge(u, v) for u, v in B.edges()})
        
        print(f'> {type} Backbone')
        nx.write_graphml(B, wGraphml.format(folder=folder, type=type))        

    print('> Distortion')
    pk.dump(distortion_dist, open(wFdistortion, 'wb'))        
    print('\n')
    
    distortion_dist = dict()
    
    G = nx.read_graphml(rDGraphml)
    # Metric computation
    B, distortion_dist['metric'] = dc.backbone(G, weight='distance', kind='metric', distortion=True)
    
    # Ultrametric computation
    M, distortion_dist['ultrametric'] = dc.backbone(G, weight='distance', kind='ultrametric', distortion=True)
    
    nx.set_edge_attributes(B, name='ultrametric', values={(u, v): M.has_edge(u, v) for u, v in B.edges()})
    
    print(f'> MLSCC Backbone')
    nx.write_graphml(B, f'networks/{folder}/directed_scc_backbone.graphml')
    print('> Distortion')
    pk.dump(distortion_dist, open(f'networks/{folder}/directed_scc_distortion.pickle', 'wb'))        
    print('\n')
