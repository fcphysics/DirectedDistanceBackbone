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
    
    U = {'min': nx.Graph(), 'max': nx.Graph(), 'avg': nx.Graph(), 'harm': nx.Graph()}
    for g in U.values():
        g.add_nodes_from(G.nodes())
    
    for u, v, w in G.edges(data=True):
        if w['alpha'] == None:
            G[u][v]['alpha'] = 0.0
            din = G[u][v]['distance']
            if G.has_edge(v, u):
                G[v][u]['alpha'] = 0.0
                dout = G[v][u]['distance']
                
                U['min'].add_edge(u, v, distance=min(din, dout))
                U['max'].add_edge(u, v, distance=max(din, dout))
                U['avg'].add_edge(u, v, distance=0.5*(din + dout))
                
                if (din + dout) == 0.0:
                    U['harm'].add_edge(u, v, distance=0.0)
                else:
                    U['harm'].add_edge(u, v, distance=2*din*dout/(din + dout))
            
            else:
                U['min'].add_edge(u, v, distance=din)
                U['harm'].add_edge(u, v, distance=2*din)
            

    #nx.write_graphml(U, wGraphml)
    pk.dump(U, open(wGraphml, 'wb'))
    print("Done")
    
    