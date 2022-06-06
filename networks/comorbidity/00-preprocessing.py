
import networkx as nx
import pandas as pd
import numpy as np

def LogOdds2P(lodds=1):
    return 1./(1 + np.exp(-lodds))

def Str2Dist(p):
    return ( (1./p) - 1 )

def main():

    # Comorbidity
    fname = "comorbidity_odds_matrix.csv"
    df = pd.read_csv(fname, index_col=0)

    df.values[[np.arange(len(df))]*2] = np.nan # Remove self-loops
    df = df.stack().reset_index().rename(columns={'level_0': 'FROM', 'level_1':'TO', 0:'LogInc'})

    df['strength'] = df.LogInc.apply(LogOdds2P)
    df['distance'] = df.strength.apply(Str2Dist)

    G = nx.from_pandas_edgelist(df, source='FROM', target='TO', edge_attr=['LogInc', 'distance', 'strength'], create_using=nx.DiGraph)
    
    # Get the largest connected component
    lwcc = max(nx.weakly_connected_components(G), key=len) # Get the largest connected component
    G = G.subgraph(lwcc)
    
    nx.write_gpickle(G.copy(), "network.gpickle")


if __name__ == "__main__":
    main()