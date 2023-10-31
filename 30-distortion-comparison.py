# coding=utf-8
# Author: Felipe X. Costa
#
# Description:
# Compare directed and undirected S_{ij} value distribution for networks.
# We perform a Mann-Whitney test to check the likelyhood that the directed distortion is statistically smaller than the undirected one
# That is, the AUC will measure the probability that a random S_dir is smaller than another random S_undir
#

from __future__ import division
# Plotting
import networkx as nx
import argparse
import configparser

import matplotlib.pyplot as plt
import pandas as pd
import powerlaw
import numpy as np
import pickle as pk
# Networks
import pickle as pk
from scipy.stats import mannwhitneyu

alternative = {'business-faculty': 'greater', 'cs-faculty': 'greater', 'history-faculty': 'greater', 'celegans-her': 'greater', 'celegans-male': 'greater', 
               'tennis-loss': 'greater', 'bike-sharing': 'greater', 'giraffe': 'less', 'comorbidity': 'greater', 'caviar-proj': 'greater', 
               'colombia-calls': 'less', 'colombia-mobility': 'less', 'mobility-manizales': 'greater', 'mobility-medellin': 'greater', 
               'yeast-grn': 'less', 'us-airports': 'less', 'DDI': 'greater', 'us-weblinks': 'greater'}

if __name__ == '__main__':
    #
    # Init
    #
    config = configparser.ConfigParser()
    config.read('networks.ini')
    #networks = list(config.keys())[1:]
    
    for group in ['Undirected', 'Directed']:
        print(group)
        df = pd.read_csv('Summary/Larger_{group:s}.csv'.format(group=group), index_col=0)
        
        for network in df.index:
            #print(network)
            folder = config[network].get('folder')

            svals_dir = pk.load(open(f'networks/{folder}/mlscc_distortion.pickle', 'rb'))
            svals_undir = pk.load(open(f'networks/{folder}/undirected_distortions.pickle', 'rb'))

            # Metric Comparison
            X = np.array(list(svals_dir['metric'].values()))
            Y = np.array(list(svals_undir['avg']['metric'].values()))

            U, p = mannwhitneyu(X, Y, alternative=alternative[network], method='asymptotic')
            AUC = U/(len(X)*len(Y))
            print(network, AUC, alternative[network], p)

            fig, ax = plt.subplots()
            #ax.boxplot([np.log10(X), np.log10(Y)], labels=['Directed', 'Undirected'])
            ax.boxplot([X, Y], labels=['Directed', 'Undirected'])
            ax.set_ylabel('Log Metric Distortion')
            if alternative[network] == 'greater':
                ax.set_title(f'{AUC=:.2f}    $p_>$= {p:.2e}')
            if alternative[network] == 'less':
                ax.set_title(f'{AUC=:.2f}    $p_<$= {p:.2e}')
            plt.savefig(f'networks/{folder}/metric_distortion_comparison.png', dpi=300) 
            plt.clf()


            # Ultrametric Comparison
            X = np.array(list(svals_dir['ultrametric'].values()))
            Y = np.array(list(svals_undir['max']['ultrametric'].values()))

            U, p = mannwhitneyu(X, Y, alternative=alternative[network], method='asymptotic')
            AUC = U/(len(X)*len(Y))
            print(network, AUC, alternative[network], p)

            fig, ax = plt.subplots()
            #ax.boxplot([np.log10(X), np.log10(Y)], labels=['Directed', 'Undirected'])
            ax.boxplot([X, Y], labels=['Directed', 'Undirected'])
            ax.set_ylabel('Log Metric Distortion')
            if alternative[network] == 'greater':
                ax.set_title(f'{AUC=:.2f}    $p_>$= {p:.2e}')
            if alternative[network] == 'less':
                ax.set_title(f'{AUC=:.2f}    $p_<$= {p:.2e}')
            plt.savefig(f'networks/{folder}/ultrametric_distortion_comparison.png', dpi=300) 
            plt.clf()


