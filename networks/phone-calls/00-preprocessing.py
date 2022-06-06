
# Data found in: https://figshare.com/articles/dataset/The_Copenhagen_Networks_Study_interaction_data/7267433/1?file=14579972

import networkx as nx
import pandas as pd
import numpy as np

import scipy.io as sio

def Str2Dist(p):
    return ( (1./p) - 1 )

def main():


    # Comunication - Phone Calls
    fname = "calls.csv"
    df = pd.read_csv(fname)
    # Ignore unanswered calls
    df = df.loc[df['duration'] >0, ['caller', 'callee', 'duration', 'timestamp']]
    dfg = df.groupby(['caller', 'callee']).agg({'duration':'sum', 'timestamp':'count'})
    dfg = dfg.rename(columns={'timestamp':'count'})
    
    # Avg trip duration
    dfg['avg-call-duration'] = dfg['duration'] / dfg['count']
    
    # Reset index
    dfg.reset_index(inplace=True)

    # Remove self-loops (i == j)
    dfg = dfg.loc[~(dfg['caller'] ==dfg['callee']), :]
    #print(dfg.head())
    
    G = nx.from_pandas_edgelist(dfg, source="caller", target="callee",
     edge_attr=['avg-call-duration', 'duration', 'count'], create_using=nx.DiGraph)
    # Get the largest connected component
    lwcc = max(nx.weakly_connected_components(G), key=len) 
    G = G.subgraph(lwcc)

    nx.write_gpickle(G.copy(), "network.gpickle")

if __name__ == "__main__":
    main()