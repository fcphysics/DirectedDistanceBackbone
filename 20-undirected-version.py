# coding=utf-8
# Authors: Rion B. Correia & Felipe Xavier Costa
# Date: Apr 22, 2023
#
# Description: Builds different undirected representations of directed graphs.
#
#
import networkx as nx
import argparse
import configparser
# Distance Closure
import distanceclosure as dc
from distanceclosure.utils import prox2dist
# Utils
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
    rGraphml = 'networks/{folder:s}/network.graphml'.format(folder=folder)
    wGraphml = 'networks/{folder:s}/undirected_networks.pickle'.format(folder=folder)
    
    # Load Network
    print("Loading network: {network:s}".format(network=network))
    G = nx.read_graphml(rGraphml)
    
    nx.set_edge_attributes(G, values=None, name='alpha')
    
    U = {'min': nx.Graph(), 'max': nx.Graph(), 'avg': nx.Graph()}
    for g in U.values():
        g.add_nodes_from(G.nodes())
    
    for u, v, w in G.edges(data=True):
        if w['alpha'] == None:
            G[u][v]['alpha'] = 0.0
            pij = w['proximity']
            if G.has_edge(v, u):
                G[v][u]['alpha'] = 0.0
                pji = G[v][u]['proximity']
                pmin = min(pij, pji)
                U['min'].add_edge(u, v, distance=prox2dist(pmin))
            else:
                pji = 0
            
            pmax = max(pij, pji)
            pavg = 0.5*(pij+pji)        
                    
            U['max'].add_edge(u, v, distance=prox2dist(pmax))
            U['avg'].add_edge(u, v, distance=prox2dist(pavg))

    #nx.write_graphml(U, wGraphml)
    pk.dump(U, open(wGraphml, 'wb'))
    print("Done")
    
    