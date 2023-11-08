# coding=utf-8
# Authors: Rion B. Correia & Felipe Xavier Costa
# Date: Apr 22, 2023
#
#
#

import networkx as nx
import argparse
import configparser

import matplotlib.pyplot as plt
import pandas as pd
import powerlaw
import numpy as np
import pickle as pk

from _shortest_path import source_target_dijkstra_path

### Main ###
config = configparser.ConfigParser()
config.read('networks.ini')
#networks = list(config.keys())[1:]

btype = 'max' #'avg' # 

if btype == 'avg':
    disjunction = sum
    bbone = 'metric'
elif btype == 'max':
    disjunction = max
    bbone = 'ultrametric'

for group in ['Undirected', 'Directed']:
    print(group)
    df = pd.read_csv('Summary/Larger_{group:s}.csv'.format(group=group), index_col=0)
    #print(df)

    df['partial'] = pd.Series(0, index=df.index)
    df['complete'] = pd.Series(0, index=df.index)

    df['partial_undirected'] = pd.Series(0, index=df.index)
    df['complete_undirected'] = pd.Series(0, index=df.index)

    for network in df.index:
        print(network)
        folder = config[network].get('folder')
        
        U = nx.read_graphml(f'networks/{folder}/undirected_{btype}_backbone.graphml')
        Bd = nx.read_graphml(f'networks/{folder}/mlscc_backbone.graphml')

        if btype == 'max':
            is_um = nx.get_edge_attributes(U, name='ultrametric')
            um_edges = [key for key, val in is_um.items() if val]
            Bu = U.edge_subgraph(um_edges).copy()
        elif btype == 'avg':
            Bu = U.copy()

        svals = pk.load(open(f'networks/{folder}/mlscc_distortion.pickle', 'rb'))
        for (u, v) in svals[bbone].keys():                
            if Bd.has_edge(v, u):
                df.loc[network, 'partial'] += 1
                df.loc[network, 'partial_undirected'] += int(Bu.has_edge(u, v))
            else:
                path1 = list(source_target_dijkstra_path(Bd, source=u, target=v, weight='distance', disjunction=disjunction)) #all_paths[u][v] #list(nx.shortest_path(Bd, source=u, target=v, weight='distance'))
                path2 = list(source_target_dijkstra_path(Bd, source=v, target=u, weight='distance', disjunction=disjunction)) #all_paths[v][u] #list(nx.shortest_path(Bd, source=v, target=u, weight='distance'))
                path2.reverse()
                if not (path1 == path2):
                    df.loc[network, 'complete'] += 0.5
                    df.loc[network, 'complete_undirected'] += 0.5*int(Bu.has_edge(u, v))
        
        #print(network, partial, complete, partial_undirected, complete_undirected)
        #break
    
    df['total'] = df['partial'] + df['complete']
    df['total_undirected'] = df['partial_undirected'] + df['complete_undirected']
    
    df.to_csv(f'Summary/{bbone.capitalize()}_UnreciprocalPaths_{group}.csv')
    print(df)
