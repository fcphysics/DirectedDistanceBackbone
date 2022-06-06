import networkx as nx
import pandas as pd
import numpy as np

def Str2Dist(p):
    return ( (1./p) - 1 )

def main():

    # Giraffe Affiliative Contacts
    fname = 'giraffe_affiliative.edgelist'
    G = nx.read_weighted_edgelist(fname, create_using=nx.DiGraph)
    
    # Find connected component
    lwcc = max(nx.weakly_connected_components(G), key=len) # Get the largest connected component
    G = G.subgraph(lwcc)
    
    # Calculate relative strength
    kin = G.in_degree(weight="weight")
    prob = {(u, v): d["weight"]/kin[v] for u, v, d in G.edges(data=True)}
    nx.set_edge_attributes(G, prob, "strength")
    
    # Calculate distance
    dist = {(u, v): Str2Dist(d["strength"]) for u, v, d in G.edges(data=True)}
    nx.set_edge_attributes(G, dist, "distance")

    nx.write_gpickle(G.copy(), "network.gpickle")
    



if __name__ == "__main__":
    main()