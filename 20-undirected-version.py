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
    wGraphml = ['networks/{folder:s}/undirected_wcc_network.graphml'.format(folder=folder),
                'networks/{folder:s}/undirected_scc_network.graphml'.format(folder=folder),
                'networks/{folder:s}/directed_scc_network.graphml'.format(folder=folder)]
    
    # Load Network
    print("Loading network: {network:s}".format(network=network))
    G = nx.read_graphml(rGraphml)
    nx.set_edge_attributes(G, values=None, name='alpha')
    lscc = max(nx.strongly_connected_components(G), key=len)
    
    U = [nx.Graph(), nx.Graph(), nx.DiGraph()] # WCC (min and harm) , LSCC (max and avg) , Directed from max and avg
    U[0].add_nodes_from(G.nodes())
    U[1].add_nodes_from(lscc)
    U[2].add_nodes_from(lscc)
    
    for u, v, w in G.edges(data=True):
        if w['alpha'] == None:
            G[u][v]['alpha'] = 0.0
            din = G[u][v]['distance']

            if G.has_edge(v, u):
                G[v][u]['alpha'] = 0.0
                dout = G[v][u]['distance']
                
                if (din + dout) == 0.0:
                    U[0].add_edge(u, v, harm_distance=0.0, min_distance=0.0)
                else:
                    U[0].add_edge(u, v, harm_distance=2*din*dout/(din + dout), min_distance=min(din, dout))
                
                if u in lscc and v in lscc:
                    U[1].add_edge(u, v, avg_distance=0.5*(din + dout), max_distance=max(din, dout))
            else:
                U[0].add_edge(u, v, harm_distance=2*din, min_distance=din)
    
    U[1] = U[1].subgraph(max(nx.connected_components(U[1]), key=len))
    U[2] = G.edge_subgraph(U[1].to_directed().edges())
    
    for i in range(3):
        nx.write_graphml(U[i], wGraphml[i])
    #pk.dump(U, open(wGraphml, 'wb'))
    print("Done")
    
    