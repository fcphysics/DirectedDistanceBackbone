# coding=utf-8
# Author: Rion B Correia
# Date: Dec 05, 2017
# Edited by: Felipe Xavier Costa
# Edited on: Jun 08, 2022
#
# Description:
# Reads a network and plot its S_{ij} value distribution
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
from utils import extract_metric_graph, extract_ultrametric_graph
import pickle as pk

def plot_s_dist(folder, kind='metric', date=None):
    
    rFdistortion = 'networks/{folder:s}/distortion.pickle'.format(folder=folder)

    if date is not None:
        wImgFile = 'networks/{folder:s}/{date:s}/dist-s-values-{kinds:s}.pdf'.format(folder=folder, date=date, kind=kind)
    else:
        wImgFile = 'networks/{folder:s}/dist-s-values-{kind:s}.pdf'.format(folder=folder, kind=kind)
    
    data = pk.load(open(rFdistortion, 'rb'))
    ss = pd.Series(list(data[kind].values()), name='s-value')

    # Select only s-values
    dfs = ss.loc[(ss > 1.0)].sort_values(ascending=False).to_frame()
    xmin = dfs['s-value'].min()
    xmin = 1
    fit = powerlaw.Fit(dfs['s-value'], xmin=xmin, estimate_discrete=False)

    alpha = fit.power_law.alpha
    sigma = fit.power_law.sigma
    print('Powerlaw: alpha:', alpha)
    print('sigma:', sigma)

    # Compare
    R, p = fit.distribution_compare('power_law', 'lognormal_positive')
    print("R:", R, 'p-value', p)

    fig, ax = plt.subplots(figsize=(5, 4))

    fit.plot_pdf(color='#d62728', linewidth=2, label='Empirical data', ax=ax)

    #
    Rp = '$R = {R:.2f}$; $p = {p:.3f}$'.format(R=R, p=p)
    ax.annotate(Rp, xy=(.03, .13), xycoords='axes fraction', color='black')

    if R > 0:
        pw_goodness = '$\sigma = {sigma:.3f}$'.format(sigma=fit.power_law.sigma)
        ax.annotate(pw_goodness, xy=(.03, .05), xycoords='axes fraction', color='#1f77b4')
    else:
        ln_goodness = '$\mu = {mu:.2f}; \sigma = {sigma:.3f}$'.format(mu=fit.lognormal_positive.mu, sigma=fit.lognormal_positive.sigma)
        ax.annotate(ln_goodness, xy=(.03, .05), xycoords='axes fraction', color='#2ca02c')
    #
    pw_label = r'Power law fit'
    ln_label = r'Lognormal fit'

    fit.power_law.plot_pdf(color='#aec7e8', linewidth=1, linestyle='--', label=pw_label, ax=ax)
    fit.lognormal_positive.plot_pdf(color='#98df8a', linewidth=1, linestyle='--', label=ln_label, ax=ax)

    #
    ax.set_title(r'Semi-metric edges ($s_{{ij}}>1)$' '\n' '{source:s}'.format(source=folder))
    ax.set_ylabel(r'$P(s_{ij} \geq x)$')
    ax.set_xlabel(r'$s_{ij}$ frequency')

    ax.grid()

    ax.legend(loc='best')

    plt.tight_layout()
    # plt.subplots_adjust(left=0.09, right=0.98, bottom=0.07, top=0.90, wspace=0, hspace=0.0)
    #plt.savefig(wImgFile, dpi=150, bbox_inches='tight')  # , pad_inches=0.05)
    plt.savefig('bike_trips.pdf', dpi=150, bbox_inches='tight')


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
    #plot_s_dist(folder, kind='ultrametric')