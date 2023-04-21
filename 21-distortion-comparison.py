# coding=utf-8
# Author: Rion B Correia
# Date: Dec 05, 2017
#
# Description:
# Compare directed and undirected S_{ij} value distribution for networks.
# We perform a Mann-Whitney test to check the likelyhood that the directed distortion is statistically smaller than the undirected one
# That is, the AUC will measure the probability that a random S_dir is smaller than another random S_undir
#

from __future__ import division
# Plotting
import matplotlib as mpl
mpl.use('Agg')
mpl.rcParams['mathtext.fontset'] = 'cm'
mpl.rcParams['mathtext.rm'] = 'serif'
#mpl.rcParams['xtick.labelsize'] = 'medium'
import matplotlib.pyplot as plt
# General
import numpy as np
import pandas as pd
pd.set_option('display.max_rows', 40)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 1000)
import configparser
# Networks
import pickle as pk
from scipy.stats import mannwhitneyu

if __name__ == '__main__':
    #
    # Init
    #
    config = configparser.ConfigParser()
    config.read('networks.ini')
    networks = list(config.keys())[1:]
    
    uFdistortion = 'networks/{folder:s}/undirected_distortion.pickle'
    dFdistortion = 'networks/{folder:s}/distortion.pickle'
    
    df = pd.DataFrame({'name': np.zeros(len(networks), dtype=str), 
                       'AUC': np.zeros(len(networks)), 'PVal': np.zeros(len(networks)),
                       'directed': np.zeros(len(networks)), 'undirected': np.zeros(len(networks))})
    
    for idx, network in enumerate(networks):
        print(network)
        settings = config[network]
        folder = settings.get('folder')
        
        df.name[idx] = network
        
        directed = pk.load(open(dFdistortion.format(folder=folder), 'rb'))
        undirected = pk.load(open(uFdistortion.format(folder=folder), 'rb'))
        
        dir_svals = list(directed['metric'].values())
        undir_svals = list(undirected['metric'].values())
        
        U, p = mannwhitneyu(dir_svals, undir_svals, alternative='less')
    
        df.AUC[idx] = U/(len(dir_svals)*len(undir_svals))
        df.PVal[idx] = p
        df.directed[idx] = np.median(np.log(dir_svals))
        df.undirected[idx] = np.median(np.log(undir_svals))
    
    df.to_csv('Summary/Distortion_DirectComparison.csv')