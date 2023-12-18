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

# Utils
import pandas as pd
import networkx as nx

if __name__ == '__main__':

    #
    # Init
    #
    config = configparser.ConfigParser()
    config.read('networks.ini')
    networks = list(config.keys())[1:]
 
    df = pd.DataFrame(0, index=networks, columns=['nodes', 'components', 'lcc', 'isolates', 'tuples', 'chains', 'stars', 'trees', 'complete', 'others', 'reducible'])
    df.drop('host-pathogen', inplace=True)
    
    for network in df.index:
        print(network)
        folder = config[network].get('folder')
        
        rGraphml = 'networks/{folder:s}/network_lscc.graphml'.format(folder=folder)
        G = nx.read_graphml(rGraphml)
        nx.set_edge_attributes(G, values=None, name='alpha')
        
        U = nx.Graph()
        U.add_nodes_from(G.nodes())
        
        for u, v, w in G.edges(data=True):
            if w['alpha'] == None:
                G[u][v]['alpha'] = 0.0
                din = G[u][v]['distance']
                
                if G.has_edge(v, u):
                    G[v][u]['alpha'] = 0.0
                    dout = G[v][u]['distance']
                    
                    U.add_edge(u, v, avg_distance=0.5*(din + dout), max_distance=max(din, dout))
        
        df['nodes'][network] = U.number_of_nodes()
        df['components'][network] = nx.number_connected_components(U)
        
        lcc_nodes = max(nx.connected_components(U), key=len)
        df['lcc'][network] = len(lcc_nodes)
        
        U.remove_nodes_from(lcc_nodes)
        if nx.is_empty(U):
            df['reducible'][network] = 1
            continue
            
        in_group = set()      
        for cc in nx.connected_components(U):
            if len(cc) == 1:
                df['isolates'][network] += 1
                in_group.update(cc)
            elif len(cc) == 2:
                df['tuples'][network] += 1
                in_group.update(cc)
            else:
                g = U.subgraph(cc)
                if nx.is_isomorphic(g, nx.complete_graph(len(cc))):
                    df['complete'][network] += 1
                    in_group.update(cc)
                elif nx.is_isomorphic(g, nx.path_graph(len(cc))):
                    df['chains'][network] += 1
                    in_group.update(cc)
                elif nx.is_isomorphic(g, nx.star_graph(len(cc)-1)):
                    df['stars'][network] += 1
                    in_group.update(cc)
                elif nx.is_tree(g):
                    df['trees'][network] += 1
                    in_group.update(cc)
        
        U.remove_nodes_from(in_group)
        df['others'][network] = nx.number_connected_components(U)
        
        #if not nx.is_empty(U):
            #nx.draw(U, pos=nx.circular_layout(U), with_labels=True)
            #plt.show()
        
        df['reducible'][network] = 1 + df['others'][network] + df['complete'][network]
    
    # Manual Fix
    df['isolates']['bike-sharing'] = 2
    df['isolates']['caviar-proj'] = 3
    df['isolates']['yeast-grn'] = 4
    df['isolates']['business-faculty'] = 10
    
    df['undirected_trees'] = df.tuples + df.chains + df.stars + df.trees
    
    
    print(df)
    df.to_csv('Summary/UndirectedComponents.csv', index=True)
    