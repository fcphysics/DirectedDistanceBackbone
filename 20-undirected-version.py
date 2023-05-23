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
    
    # Select largest connected component
    G = G.subgraph(max(nx.strongly_connected_components(G), key=len))
    nx.set_edge_attributes(G, values=None, name='alpha')
    
    U = nx.Graph()
    U.add_nodes_from(G.nodes())
    
    for u, v, w in G.edges(data=True):
        if w['alpha'] == None:
            G[u][v]['alpha'] = 0.0
            if G.has_edge(v, u):
                G[v][u]['alpha'] = 0.0
                
                din = G[u][v]['distance']
                dout = G[v][u]['distance']
                
                U.add_edge(u, v, avg_distance=0.5*(din + dout), max_distance=max(din, dout))
    
    components = []
    for c in nx.connected_components(U):
        if len(c) > 2:
            components.append((G.subgraph(c).copy(), U.subgraph(c).copy()))

    #nx.write_graphml(U, wGraphml)
    pk.dump(components, open(wGraphml, 'wb'))
    print("Done")
    
    