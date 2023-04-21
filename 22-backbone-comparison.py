# coding=utf-8
# Author: Rion B Correia
# Date: Dec 05, 2017
#
# Description:
# Compare directed and undirected backbone sizes for networks
#

from __future__ import division
# Plotting
import matplotlib as mpl
mpl.use('Agg')
mpl.rcParams['mathtext.fontset'] = 'cm'
mpl.rcParams['mathtext.rm'] = 'serif'
#mpl.rcParams['xtick.labelsize'] = 'medium'
import matplotlib.pyplot as plt
# General
import numpy as np
import pandas as pd
pd.set_option('display.max_rows', 40)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 1000)
import configparser
# Networks
import networkx as nx
import pickle as pk

if __name__ == '__main__':
    #
    # Init
    #
    config = configparser.ConfigParser()
    config.read('networks.ini')
    networks = list(config.keys())[1:]
    
    dGfile = 'networks/{folder:s}/network.graphml'
    dBfile = 'networks/{folder:s}/backbone.graphml'
    
    uGfile = 'networks/{folder:s}/undirected_network.graphml'
    uBfile = 'networks/{folder:s}/undirected_backbone.graphml'
    
    df = pd.DataFrame({'name': np.zeros(len(networks), dtype=str), 'directed': np.zeros(len(networks)), 'undirected': np.zeros(len(networks))})
    
    for idx, network in enumerate(networks):
        print(network)
        settings = config[network]
        folder = settings.get('folder')
        
        df.name[idx] = network
        
        G = nx.read_graphml(dGfile.format(folder=folder))
        B = nx.read_graphml(dBfile.format(folder=folder))
        
        df.directed[idx] = B.number_of_edges()/G.number_of_edges()
        
        G = nx.read_graphml(uGfile.format(folder=folder))
        B = nx.read_graphml(uBfile.format(folder=folder))
        
        df.undirected[idx] = B.number_of_edges()/G.number_of_edges()
    
    df.to_csv("Summary/BackboneSizeComparison.csv")
    