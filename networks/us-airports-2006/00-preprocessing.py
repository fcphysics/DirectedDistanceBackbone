import networkx as nx
import pandas as pd
import numpy as np
import zipfile

def Str2Dist(p):
    return ( (1./p) - 1 )

def main():

    # Airport Meta Data
    dfm = pd.read_csv('983081491_T_MASTER_CORD.zip', parse_dates=['AIRPORT_START_DATE', 'AIRPORT_THRU_DATE'], index_col=0)
    # Remove airports built after 2006
    dfm = dfm.loc[(dfm['AIRPORT_START_DATE'] <= '2006-12-31'), :]
    # Remove airports in US Territories
    dfm = dfm.loc[~(dfm['AIRPORT_STATE_CODE'].isin(['TT', 'AS', 'GU', 'MP', np.nan])), :]
    # Update longitude of Alaskan airports beyond the -180 longitude
    dfm.loc[(dfm['LONGITUDE'] > 0), 'LONGITUDE'] = dfm.loc[(dfm['LONGITUDE'] > 0), 'LONGITUDE'] - 360
    # Group and keep only last record for each airport_id
    dfmg = dfm.groupby('AIRPORT_ID').apply(lambda x: x.nlargest(1, columns=['AIRPORT_START_DATE']))
    dfmg.set_index('AIRPORT_ID', inplace=True)

    # Passenger data
    df = pd.read_csv('983062542_T_T100D_SEGMENT_US_CARRIER_ONLY.zip', usecols=['PASSENGERS', 'ORIGIN_AIRPORT_ID', 'DEST_AIRPORT_ID'])
    # Only records with at least one passenger
    df = df.loc[(df['PASSENGERS'] > 0), :]
    # Only airports in the metadata
    df = df.loc[(df['ORIGIN_AIRPORT_ID'].isin(dfmg.index)) & (df['DEST_AIRPORT_ID'].isin(dfmg.index)), :]


    dfg = df.groupby(['ORIGIN_AIRPORT_ID', 'DEST_AIRPORT_ID']).agg({'PASSENGERS': 'sum'})
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

    # Metadata
    nx.set_node_attributes(G, name='name', values=dfmg['DISPLAY_AIRPORT_NAME'])
    nx.set_node_attributes(G, name='code', values=dfmg['AIRPORT'])
    nx.set_node_attributes(G, name='lat', values=dfmg['LATITUDE'])
    nx.set_node_attributes(G, name='lon', values=dfmg['LONGITUDE'])

    nx.write_gpickle(G.copy(), "network.gpickle")


if __name__ == "__main__":
    main()