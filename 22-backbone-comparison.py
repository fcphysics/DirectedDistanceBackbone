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
    
    uGfile = 'networks/{folder:s}/undirected_networks.pickle'
    uBfile = 'networks/{folder:s}/undirected_backbones.pickle'
    
    dfM = pd.DataFrame({'name': np.zeros(len(networks), dtype=str), 'directed': np.zeros(len(networks)), 
                       'Max': np.zeros(len(networks)), 'Min': np.zeros(len(networks)), 'Avg': np.zeros(len(networks))})
    dfU = pd.DataFrame({'name': np.zeros(len(networks), dtype=str), 'directed': np.zeros(len(networks)), 
                       'Max': np.zeros(len(networks)), 'Min': np.zeros(len(networks)), 'Avg': np.zeros(len(networks))})
    
    for idx, network in enumerate(networks):
        print(network)
        settings = config[network]
        folder = settings.get('folder')
        
        dfM.loc[idx, 'name'] = network
        dfU.loc[idx, 'name'] = network
        
        G = nx.read_graphml(dGfile.format(folder=folder))
        B = nx.read_graphml(dBfile.format(folder=folder))
        
        dfM.loc[idx, 'directed'] = B.number_of_edges()/G.number_of_edges()
        dfU.loc[idx, 'directed'] = sum([int(w['ultrametric']) for _, _, w in B.edges(data=True)])/G.number_of_edges()
        
        G = pk.load(open(uGfile.format(folder=folder), 'rb'))
        B = pk.load(open(uBfile.format(folder=folder), 'rb'))
        
        for type in ['min', 'max', 'avg']:
            if G[type].number_of_edges() > 0:
                dfM.loc[idx, type.capitalize()] = B[type].number_of_edges()/G[type].number_of_edges()
                dfU.loc[idx, type.capitalize()] = sum([int(w['ultrametric']) for _, _, w in B[type].edges(data=True)])/G[type].number_of_edges()
            else:
                print(type)
    
    dfM.to_csv("Summary/MetricBackboneSizeComparison.csv")
    dfU.to_csv("Summary/UltrametricBackboneSizeComparison.csv")
    