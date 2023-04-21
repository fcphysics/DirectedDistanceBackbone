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
import pickle as pk

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
    rFdistortion = 'networks/{folder:s}/distortion.pickle'.format(folder=folder)
    wGstats = 'networks/{folder:s}/distortion-stats.csv'.format(folder=folder)

    # Select only s-values
    dfs = pd.DataFrame().from_dict(pk.load(open(rFdistortion, 'rb')))
    print(dfs.head())

    # to Result Series
    sR = pd.Series({
        'avg-metric-distrotion': dfs['metric'].mean(),
        'std-metric-distrotion': dfs['metric'].std(),
        'med-metric-distrotion': dfs['metric'].median(),
        #
        'avg-ultrametric-distrotion': dfs['ultrametric'].mean(),
        'std-ultrametric-distrotion': dfs['ultrametric'].std(),
        'med-ultrametric-distrotion': dfs['ultrametric'].median(),
    }, name=network, dtype='object')

    # Print
    print(sR)
    sR.to_csv(wGstats)