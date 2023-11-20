import matplotlib.pyplot as plt
import pandas as pd
import configparser
import networkx as nx

if __name__ == '__main__':
    
    #df = pd.read_csv('LOCAL/Edges_Components.csv')
    #df.set_index('network', inplace=True)
    #print(df)

    config = configparser.ConfigParser()
    config.read('networks.ini')
    networks = list(config.keys())[1:]

    df = pd.DataFrame(0, index=networks, columns=['nodes', 'components', 'lscc', 'isolates', 'tuples', 'chains', 'stars', 'trees', 'complete', 'others', 'reducible'])
    #print(df)

    for network in networks:
        print(network)
        folder = config[network].get('folder')
        
        rGraphml = 'networks/{folder:s}/network.graphml'.format(folder=folder)
        G = nx.read_graphml(rGraphml)
        
        df['nodes'][network] = G.number_of_nodes()
        df['components'][network] = nx.number_strongly_connected_components(G)
        
        if df['components'][network] == df['nodes'][network]:
            continue
        
        lscc_nodes = max(nx.strongly_connected_components(G), key=len)
        df['lscc'][network] = len(lscc_nodes)
        
        lscc = G.subgraph(lscc_nodes).copy()
        wGraphml = 'networks/{folder:s}/network_lscc.graphml'.format(folder=folder)
        nx.write_graphml(lscc, wGraphml)
        
        G.remove_nodes_from(lscc_nodes)
        if nx.is_empty(G):
            df['reducible'][network] = 1
            continue
                
        in_group = set()      
        for cc in nx.strongly_connected_components(G):
            if len(cc) == 1:
                df['isolates'][network] += 1
                in_group.update(cc)
            elif len(cc) == 2:
                df['tuples'][network] += 1
                in_group.update(cc)
            else:
                g = G.subgraph(cc)
                if nx.is_isomorphic(g, nx.complete_graph(len(cc), create_using=nx.DiGraph)):
                    df['complete'][network] += 1
                    in_group.update(cc)
                else:
                    u = g.to_undirected()
                    if nx.is_isomorphic(u, nx.path_graph(len(cc))):
                        df['chains'][network] += 1
                        in_group.update(cc)
                    elif nx.is_isomorphic(u, nx.star_graph(len(cc)-1)):
                        df['stars'][network] += 1
                        in_group.update(cc)
                    elif nx.is_tree(u):
                        df['trees'][network] += 1
                        in_group.update(cc)
        
        G.remove_nodes_from(in_group)
        df['others'][network] = nx.number_strongly_connected_components(G)
        
        df['reducible'][network] = 1 + df['others'][network] + df['complete'][network]
    
    print(df)
    df.to_csv('Summary/StrongComponents.csv')