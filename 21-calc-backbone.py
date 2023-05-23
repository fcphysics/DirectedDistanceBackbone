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
    rGfile = 'networks/{folder:s}/undirected_networks.pickle'.format(folder=folder)
    wFdistortion = 'networks/{folder:s}/undirected_distortions.pickle'.format(folder=folder)
    wGstats = 'networks/{folder:s}/undirected_networks-stats.csv'.format(folder=folder)

    # Load Network
    print("Loading network: {network:s}".format(network=network))
    components = pk.load(open(rGfile, 'rb'))
    
    
    df = pd.DataFrame(columns=['n-nodes', 'nd-edges', 'nu-edges', 'tau-metric', 'tau-ultrametric', 
                           'tau-avg-metric', 'tau-avg-ultrametric', 'tau-max-metric', 'tau-max-ultrametric'], index=range(len(components)))
    
    single_s = {'metric': dict(), 'ultrametric': dict(), 'avg-metric': dict(), 
                             'avg-ultrametric': dict(), 'max-metric': dict(), 'max-ultrametric': dict()}
    
    s_values = [single_s.copy() for _ in range(len(components))]
    
    for idx, (D, U) in enumerate(components):
        df['n-nodes'][idx] = D.number_of_nodes()
        df['nd-edges'][idx] = D.number_of_edges()
        df['nu-edges'][idx] = U.number_of_edges()
        
        for kind in ['metric', 'ultrametric']:
            B, s_values[idx][kind] = dc.backbone(D, weight='distance', kind=kind, distortion=True)
            df[f'tau-{kind}'][idx] = B.number_of_edges()/df['nd-edges'][idx]
            for utype in ['avg', 'max']:
                B, s_values[idx][f'{utype}-{kind}'] = dc.backbone(U, weight=f'{utype}_distance', kind=kind, distortion=True)
                df[f'tau-{utype}-{kind}'][idx] = B.number_of_edges()/df['nu-edges'][idx]
            
    
    print('--- Exporting Formats ---')
    ensurePathExists(wFdistortion)

    print('> Backbone Statistics')
    df.to_csv(wGstats)
    print('> Distortion')
    pk.dump(s_values, open(wFdistortion, 'wb'))        
    print('\n')
