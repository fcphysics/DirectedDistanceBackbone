# coding=utf-8
# Author: Rion B Correia
# Date: Dec 05, 2017
# Edited by: Felipe Xavier Costa
# Edited on: Jun 08, 2022
#
# Description:
# Reads a network and outputs its S_{ij} value distribution
#

from __future__ import division
# Plotting
import matplotlib as mpl
mpl.use('Agg')
mpl.rcParams['mathtext.fontset'] = 'cm'
mpl.rcParams['mathtext.rm'] = 'serif'
mpl.rcParams['xtick.labelsize'] = 'medium'
import matplotlib.pyplot as plt
# General
import numpy as np
import pandas as pd
pd.set_option('display.max_rows', 40)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 1000)
# Networks
import networkx as nx
import powerlaw
# IO Operations
import argparse
import configparser
import pickle as pk

def plot_s_dist(folder, kind):
    
    summary = pd.DataFrame({'R': {'mlscc': 0, 'min': 0, 'max': 0, 'avg': 0}, 'p': {'mlscc': 0, 'min': 0, 'max': 0, 'avg': 0}, 
                       'alpha': {'mlscc': 0, 'min': 0, 'max': 0, 'avg': 0}, 'gamma': {'mlscc': 0, 'min': 0, 'max': 0, 'avg': 0},
                       'mu': {'mlscc': 0, 'min': 0, 'max': 0, 'avg': 0}, 'sigma': {'mlscc': 0, 'min': 0, 'max': 0, 'avg': 0},
                       'mean': {'mlscc': 0, 'min': 0, 'max': 0, 'avg': 0}, 'median': {'mlscc': 0, 'min': 0, 'max': 0, 'avg': 0},
                       'stdev': {'mlscc': 0, 'min': 0, 'max': 0, 'avg': 0}})
    
    data = pk.load(open(f'networks/{folder}/mlscc_distortion.pickle', 'rb'))

    ss = pd.Series(list(data[kind].values()), name='s-value')
        
    summary['mean']['mlscc'] = ss.mean()
    summary['median']['mlscc'] = ss.median()
    summary['stdev']['mlscc'] = ss.std()
    
    # Select only s-values
    dfs = ss.loc[(ss > 1.0)].sort_values(ascending=False).to_frame()
    xmin = 1
    fit = powerlaw.Fit(dfs['s-value'], xmin=xmin, estimate_discrete=False)
    summary['R']['mlscc'], summary['p']['mlscc'] = fit.distribution_compare('power_law', 'lognormal_positive') # Compare
    # Parameters
    summary['alpha']['mlscc'] = fit.power_law.alpha
    summary['gamma']['mlscc'] = fit.power_law.sigma
    summary['mu']['mlscc'] = fit.lognormal_positive.mu
    summary['sigma']['mlscc'] = fit.lognormal_positive.sigma


    data = pk.load(open(f'networks/{folder}/undirected_distortions.pickle', 'rb'))

    for type in ['min', 'max', 'avg']:
        ss = pd.Series(list(data[type][kind].values()), name='s-value')
        
        summary['mean'][type] = ss.mean()
        summary['median'][type] = ss.median()
        summary['stdev'][type] = ss.std()
        
        # Select only s-values
        dfs = ss.loc[(ss > 1.0)].sort_values(ascending=False).to_frame()
        xmin = 1
        fit = powerlaw.Fit(dfs['s-value'], xmin=xmin, estimate_discrete=False)
        summary['R'][type], summary['p'][type] = fit.distribution_compare('power_law', 'lognormal_positive') # Compare
        # Parameters
        summary['alpha'][type] = fit.power_law.alpha
        summary['gamma'][type] = fit.power_law.sigma
        summary['mu'][type] = fit.lognormal_positive.mu
        summary['sigma'][type] = fit.lognormal_positive.sigma
    
    wSummaryFile = 'networks/{folder:s}/undirected_{kind}_distortion_fits.csv'.format(folder=folder, kind=kind)
    summary.to_csv(wSummaryFile)
    


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

    # Plot Distortion Distribution
    plot_s_dist(folder, kind='metric')
    plot_s_dist(folder, kind='ultrametric')