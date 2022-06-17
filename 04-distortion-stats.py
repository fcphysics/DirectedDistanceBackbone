# coding=utf-8
# Author: Rion B Correia
# Date: Dec 07, 2020
#
# Description: Reads a network and computes closure.
#
#
import numpy as np
import pandas as pd
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
#pd.options.display.float_format = '{:.2%}'.format
import networkx as nx
import argparse
import configparser
from utils import extract_metric_graph, extract_ultrametric_graph


if __name__ == '__main__':

    #
    # Init
    #
    config = configparser.ConfigParser()
    config.read('networks.ini')
    networks = list(config.keys())[1:]

    #
    # Args
    #
    parser = argparse.ArgumentParser()
    parser.add_argument("--network", default='bike-sharing', type=str, choices=networks, help="Network name.")
    args = parser.parse_args()
    #
    network = args.network
    #
    settings = config[network]
    folder = settings.get('folder')

    # Files
    rGpickle = 'networks/{folder:s}/network-closure.gpickle'.format(folder=folder)
    rGedgelist = 'networks/{folder:s}/network-closure.csv.gz'.format(folder=folder)
    wGstats = 'networks/{folder:s}/distortion-stats.csv'.format(folder=folder)

    # Load Closure
    G = nx.read_gpickle(rGpickle)
    ss = pd.Series([d.get('s-value') for i, j, d in G.edges(data=True)], name='s-value')
    # Select only s-values
    dfs = ss.loc[(ss > 1.0)].sort_values(ascending=False).to_frame()
    print(dfs.head())

    n_nodes = G.number_of_nodes()
    n_edges = G.number_of_edges()

    # to Result Series
    sR = pd.Series({
        'n-nodes': n_nodes,
        'n-edges': n_edges,
        #
        'avg-metric-distrotion': dfs['s-value'].mean(),
        'std-metric-distrotion': dfs['s-value'].std(),
        #
    }, name=network, dtype='object')

    # Print
    print(sR)
    sR.to_csv(wGstats)