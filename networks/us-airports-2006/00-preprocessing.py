import networkx as nx
import pandas as pd
import numpy as np
import zipfile

def Str2Dist(p):
    return ( (1./p) - 1 )

def main():

    # Passenger Travel
    fname = '983062542_T_T100D_SEGMENT_US_CARRIER_ONLY.zip'
    df = pd.read_csv(fname, compression='zip')

    dfg = df.groupby(['ORIGIN_AIRPORT_ID', 'DEST_AIRPORT_ID']).agg({'PASSENGERS': 'sum'})
    dfg = dfg.loc[dfg['PASSENGERS'] >= 1.0, :] # Trips with at least one passenger
    dfg.reset_index(inplace=True)

    # Remove Self-Loops
    dfg = dfg.loc[~(dfg['ORIGIN_AIRPORT_ID'] == dfg['DEST_AIRPORT_ID']), :]

    G = nx.from_pandas_edgelist(dfg, source='ORIGIN_AIRPORT_ID', target='DEST_AIRPORT_ID', edge_attr=['PASSENGERS'], create_using=nx.DiGraph)
    
    # Get the largest connected component
    lwcc = max(nx.weakly_connected_components(G), key=len) # Get the largest connected component
    G = G.subgraph(lwcc)

    # Compute relative counts as strength
    kin = G.in_degree(weight='PASSENGERS')
    prob = {(u, v): d['PASSENGERS']/kin[v] for u, v, d in G.edges(data=True)}
    nx.set_edge_attributes(G, prob, "strength")
    # Compute distance
    dist = {(u, v): Str2Dist(d["strength"]) for u, v, d in G.edges(data=True)}
    nx.set_edge_attributes(G, dist, "distance")

    fname = '983081491_T_MASTER_CORD.zip'
    df = pd.read_csv(fname, compression='zip')

    # Metadata
    nx.set_node_attributes(G, name='name', values=df['DISPLAY_AIRPORT_NAME'])
    nx.set_node_attributes(G, name='code', values=df['AIRPORT'])
    nx.set_node_attributes(G, name='lat', values=df['LATITUDE'])
    nx.set_node_attributes(G, name='lon', values=df['LONGITUDE'])

    nx.write_gpickle(G.copy(), "network.gpickle")


if __name__ == "__main__":
    main()