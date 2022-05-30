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
    wGstats = 'networks/{folder:s}/network-stats.csv'.format(folder=folder)

    # Load Closure
    G = nx.read_gpickle(rGpickle)

    # Extract Backbones from edge property (see utils.py)
    Gm = extract_metric_graph(G)
    Gu = extract_ultrametric_graph(G)

    # Calculate stats
    n_nodes = G.number_of_nodes()
    n_edges = G.number_of_edges()

    density = nx.density(G)

    n_edges_metric = Gm.number_of_edges()
    n_edges_ultrametric = Gu.number_of_edges()

    # to Result Series
    sR = pd.Series({
        'n-nodes': n_nodes,
        'n-edges': n_edges,
        #
        'density': density,
        #
        'n-edges-metric': n_edges_metric,
        'n-edges-ultrametric': n_edges_ultrametric,
        #
        '%-edges-metric': (n_edges_metric / n_edges),
        '%-edges-ultrametric': (n_edges_ultrametric / n_edges),
        #
        '%-redundancy-metric': 1 - (n_edges_metric / n_edges),
        '%-redundancy-ultrametric': 1 - (n_edges_ultrametric / n_edges),
        #
        '%-edges-ultrametric/metric': ((n_edges_ultrametric / n_edges) / (n_edges_metric / n_edges)),
        #
    }, name=network, dtype='object')

    # Print
    print(sR)
    sR.to_csv(wGstats)
