# coding=utf-8
# Author: Rion B Correia
# Date: May 30, 2022
#
# Description: Preprocesses the bike sharing dataset and transform it into a gpickle networkx.DiGraph object
# Source: https://github.com/konstantinklemmer/bikecommclust/blob/master/data/trips.zip
# Paper: https://arxiv.org/pdf/1804.05584.pdf
#
#
import pandas as pd
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
import networkx as nx


if __name__ == '__main__':

    df = pd.read_csv('trips.zip', index_col=0)
    print(df.head())

    # Add MetaData
    dfm = pd.read_csv('stations.csv', index_col=0)

    # FILTERS as in Munoz-Mendez (2018)
    # Trips that start or end at a repair station.
    # Trips that do not report correct destinations and show a negative duration.
    # Trips that do not report the bicycle ID.
    df = df.loc[(df['StartStation Id'].isin(dfm.index)) & (df['EndStation Id'].isin(dfm.index)), :]

    # Group
    dfg = df.groupby(['StartStation Id', 'EndStation Id']).agg({'Duration': 'sum', 'Bike Id': 'count'})

    # Rename
    dfg.rename(columns={'Duration': 'sum-duration', 'Bike Id': 'count-trips'}, inplace=True)
    #dfg.index.rename({'StartStation Id': 'i', 'EndStation Id': 'j'}, inplace=True)

    # FILTER: Min of 5 trips to be considered an edge
    dfg = dfg.loc[dfg['count-trips'] >= 7, :]

    # Avg trip duration
    dfg['avg-trip-duration'] = dfg['sum-duration'] / dfg['count-trips']

    # Reset index
    dfg.reset_index(inplace=True)
    dfg.rename(columns={'StartStation Id': 'i', 'EndStation Id': 'j'}, inplace=True)
    print(dfg.head())

    # Remove self-loops (i == j)
    dfg = dfg.loc[~(dfg['i'] == dfg['j']), :]

    # to DiGraph
    G = nx.from_pandas_edgelist(dfg, source='i', target='j', edge_attr=['avg-trip-duration'], create_using=nx.DiGraph)

    # Metadata
    nx.set_node_attributes(G, name='label', values=dfm['name'])
    nx.set_node_attributes(G, name='lat', values=dfm['lat'])
    nx.set_node_attributes(G, name='lon', values=dfm['long'])
    nx.set_node_attributes(G, name='nbikes', values=dfm['nbBikes'])
    nx.set_node_attributes(G, name='ndocks', values=dfm['nbDocks'])

    # Export
    nx.write_gpickle(G, 'network.gpickle')
