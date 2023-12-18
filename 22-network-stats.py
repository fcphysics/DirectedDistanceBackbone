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
    
    rGraphml = ['networks/{folder:s}/undirected_scc_network.graphml'.format(folder=folder),
                'networks/{folder:s}/directed_scc_network.graphml'.format(folder=folder)]
    rBraphml = ['networks/{folder:s}/undirected_{type:s}_backbone.graphml', 
                'networks/{folder}/directed_scc_backbone.graphml']
    
    wGstats = 'networks/{folder:s}/undirected-stats.csv'.format(folder=folder)
    #wGstats = 'networks/{folder:s}/undirected-stats_nedges.csv'.format(folder=folder)
    
    #df = pd.DataFrame(columns=['n_nodes', 'n_edges', 'density', 'tau_metric', 'tau_ultrametric', 'ultra_per_metric'], index=['min', 'harm', 'max', 'avg', 'mlscc'])
    df = pd.DataFrame(columns=['n_nodes', 'nedges', 'density', 'nedges_metric', 'nedges_ultrametric'], index=['max', 'avg', 'dir_scc'])
    
    types = [['max', 'avg'], ['dir_scc']]
    
    for i in range(2):
        G = nx.read_graphml(rGraphml[i])        
        for type in types[i]:
    
            df['n_nodes'][type] = G.number_of_nodes()                        
            df['nedges'][type] = G.number_of_edges()
            df['density'][type] = nx.density(G)    

            B = nx.read_graphml(rBraphml[i].format(folder=folder, type=type))
            
            '''
            df['tau_metric'][type] = B.number_of_edges()/df['n_edges'][type]
            df['tau_ultrametric'][type] = sum([int(w) for _, _, w in B.edges(data='ultrametric')])/df['n_edges'][type]
            df['ultra_per_metric'][type] = df['tau_ultrametric'][type]/df['tau_metric'][type]
            '''
            df['nedges_metric'][type] = B.number_of_edges()
            df['nedges_ultrametric'][type] = sum([int(w) for _, _, w in B.edges(data='ultrametric')])


    # Print
    print(df)
    df.to_csv(wGstats)
    print("\n")
