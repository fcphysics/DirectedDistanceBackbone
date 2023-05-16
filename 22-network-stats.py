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
    rGfile = 'networks/{folder:s}/undirected_networks.pickle'.format(folder=folder)
    rBfile = 'networks/{folder:s}/undirected_backbones.pickle'.format(folder=folder)
    wGstats = 'networks/{folder:s}/undirected_networks-stats.csv'.format(folder=folder)
    #wFasymmetry = 'networks/{folder:s}/backbone_asymmetry.pickle'.format(folder=folder)

    # Load graph
    G = pk.load(open(rGfile, 'rb'))
    B = pk.load(open(rBfile, 'rb'))
    
    df = pd.DataFrame(columns=['n-nodes', 'n-edges', 'density', '%-edges-metric','%-edges-ultrametric'],
                      index=['min', 'max', 'avg', 'harm'])
    
    for type in ['min', 'max', 'avg', 'harm']:
        print(type)
        df['n-nodes'][type] = G[type].number_of_nodes()
        df['n-edges'][type] = G[type].number_of_edges()
        df['density'][type] = nx.density(G[type])
        
        if df['n-edges'][type] > 0:
            df['%-edges-metric'][type] = B[type].number_of_edges()/df['n-edges'][type]
            df['%-edges-ultrametric'][type] = sum([int(d) for _, _, d in B[type].edges(data='ultrametric')])/df['n-edges'][type]
        else:
            df['%-edges-metric'][type] = 0.0
            df['%-edges-ultrametric'][type] = 0.0

    # Print
    print(df)
    df.to_csv(wGstats)
    print("\n\n")