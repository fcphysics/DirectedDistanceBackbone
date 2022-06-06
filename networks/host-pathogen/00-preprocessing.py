
# Data found in: https://figshare.com/articles/dataset/SpeciesInteractions_EID2/1381853
# Citation: Wardeh, M., Risley, C., McIntyre, M., Setzkorn, C., & Baylis, M. Figshare https://doi.org/10.6084/m9.figshare.1381853 (2014)

import networkx as nx
import pandas as pd
import numpy as np

def Str2Dist(p):
    return ( (1./p) - 1 )

def main():

    # Host-Pathogen
    fname = "SpeciesInteractions_EID2.csv"
    df = pd.read_csv(fname)
    G = nx.from_pandas_edgelist(df, source="Cargo", target="Carrier", edge_attr="Sequences count", create_using=nx.DiGraph)
    
    # Remove edges without "Sequence count"
    zero_counts = [(u, v) for u, v, d in G.edges(data=True) if d["Sequences count"] == 0.0]
    G.remove_edges_from(zero_counts)
    G.remove_edges_from(nx.selfloop_edges(G))
    
    # Get connected component
    lwcc = max(nx.weakly_connected_components(G), key=len) # Get the largest connected component
    #print(lwcc)
    G = G.subgraph(lwcc)
    
    
    # Compute relative counts as strength
    kin = G.in_degree(weight="Sequences count")
    prob = {(u, v): d["Sequences count"]/kin[v] for u, v, d in G.edges(data=True)}
    nx.set_edge_attributes(G, prob, "strength")
    # Compute distance
    dist = {(u, v): Str2Dist(d["strength"]) for u, v, d in G.edges(data=True)}
    nx.set_edge_attributes(G, dist, "distance")
    
    nx.write_gpickle(G.copy(), "network.gpickle")
    


if __name__ == "__main__":
    main()