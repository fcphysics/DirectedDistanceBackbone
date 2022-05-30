# coding=utf-8
# Author: Rion B Correia
# Date: May 30, 2022
#
# Description: Preprocesses the bike sharing dataset and transform it into a gpickle networkx.DiGraph object
# Source: https://github.com/konstantinklemmer/bikecommclust/blob/master/data/trips.zip
#
#
import pandas as pd
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
import networkx as nx

#446 {}
#446 501 {'duration': 15240, 'ntrips': 25, 'distance': 609.6}
#[Finished in 1.4s]

if __name__ == '__main__':

    df = pd.read_csv('trips.zip', index_col=0)
    print(df.head())


    dfg = df.groupby(['StartStation Id', 'EndStation Id']).agg({'Duration': 'sum', 'Bike Id': 'count'})
    
    # Rename
    dfg.rename(columns={'Duration': 'sum-duration', 'Bike Id': 'count-trips'}, inplace=True)
    dfg.index.rename({'StartStation Id': 'i', 'EndStation Id': 'j'}, inplace=True)
    
    # Avg trip duration
    dfg['avg-trip-duration'] = dfg['sum-duration'] / dfg['count-trips']
    print(dfg.head())

    # Reset index
    dfg.reset_index(inplace=True)

    # Remove self-loops (i == j)
    dfg = dfg.loc[~(dfg['i'] ==dfg['j']), :]

    # to DiGraph
    G = nx.from_pandas_edgelist(dfg, source='i', target='j', edge_attr=['avg-trip-duration'], create_using=nx.DiGraph)

    # Add MetaData
    dfm = pd.read_csv('metadata.txt', index_col=0)
    #
    nx.set_node_attributes(G, name='label', values=dfm['name'])
    nx.set_node_attributes(G, name='lat', values=dfm['lat'])
    nx.set_node_attributes(G, name='lon', values=dfm['long'])
    nx.set_node_attributes(G, name='nbikes', values=dfm['nbBikes'])
    nx.set_node_attributes(G, name='ndocks', values=dfm['nbDocks'])

    # Export
    nx.write_gpickle(G, 'network.gpickle')