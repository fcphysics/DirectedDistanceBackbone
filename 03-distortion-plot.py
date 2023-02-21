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

def generate_original_graph(G):
    GO = G.copy()
    edges2remove = [(i, j) for i, j, d in G.edges(data=True) if 'is_original' not in d]
    GO.remove_edges_from(edges2remove)
    return GO

'''
def plot_s_dist(source, project, normalization, date=None):
    # Init
    if date is not None:
        rGpickle = 'results/%s/%s/%s/graph-%s.gpickle' % (source, project, date, normalization)
    else:
        rGpickle = 'results/%s/%s/graph-%s.gpickle' % (source, project, normalization)

    source_str = source.title()

    if date is not None:
        wImgFile = "images/%s/%s/%s/%s/dist-s-values.pdf" % (source, project, date, normalization)
        project_str = project.replace('-', ' ').title() + ' - ' + date.title()
    else:
        wImgFile = "images/%s/%s/%s/dist-s-values.pdf" % (source, project, normalization)
        project_str = project.replace('-', ' ').title()

    # Load Network
    print('--- Loading Network gPickle (%s) ---' % (rGpickle))
    G = nx.read_gpickle(rGpickle)
    print('Network: %s' % (G.name))
    #
    # SubGraphs
    #
    # Original Graph, without the metric closure
    GO = generate_original_graph(G)

    ss = pd.Series([d.get('s_value') for i, j, d in GO.edges(data=True)], name='s-value')

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
    R, p = fit.distribution_compare('power_law', 'lognormal')
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
        ln_goodness = '$\mu = {mu:.2f}; \sigma = {sigma:.3f}$'.format(mu=fit.lognormal.mu, sigma=fit.lognormal.sigma)
        ax.annotate(ln_goodness, xy=(.03, .05), xycoords='axes fraction', color='#2ca02c')
    #
    pw_label = r'Power law fit'
    ln_label = r'Lognormal fit'
    #ex_label = r'Lognormal fit'
    fit.power_law.plot_pdf(color='#aec7e8', linewidth=1, linestyle='--', label=pw_label, ax=ax)
    fit.lognormal.plot_pdf(color='#98df8a', linewidth=1, linestyle='--', label=ln_label, ax=ax)
    #fit.exponential.plot_pdf(color='#c5b0d5', linewidth=1, linestyle='--', label=ex_label, ax=ax)

    #
    ax.set_title(r'Semi-metric edges ($s_{{ij}}>1)$' '\n' '{source:s} - {project:s} ({normalization:s})'.format(source=source_str, project=project_str, normalization=normalization))
    ax.set_ylabel(r'$P(s_{ij} \geq x)$')
    ax.set_xlabel(r'$s_{ij}$ frequency')

    ax.grid()

    ax.legend(loc='best')

    plt.tight_layout()
    # plt.subplots_adjust(left=0.09, right=0.98, bottom=0.07, top=0.90, wspace=0, hspace=0.0)
    plt.savefig(wImgFile, dpi=150, bbox_inches='tight')  # , pad_inches=0.05)
'''


def plot_s_dist(folder, date=None):
    
    rGpickle = 'networks/{folder:s}/network-closure.gpickle'.format(folder=folder)

    if date is not None:
        wImgFile = 'networks/{folder:s}/{date:s}/dist-s-values.pdf'.format(folder=folder, date=date)
        #"images/%s/%s/%s/%s/dist-s-values.pdf" % (source, project, date, normalization)
        #project_str = project.replace('-', ' ').title() + ' - ' + date.title()
    else:
        wImgFile = 'networks/{folder:s}/dist-s-values.pdf'.format(folder=folder)
        #project_str = project.replace('-', ' ').title()

    # Load Network
    print('--- Loading Network gPickle (%s) ---' % (rGpickle))
    G = nx.read_gpickle(rGpickle)
    print('Network: %s' % (G.name))
    #
    # SubGraphs
    #
    # Original Graph, without the metric closure
    GO = generate_original_graph(G)

    ss = pd.Series([d.get('s-value') for i, j, d in GO.edges(data=True)], name='s-value')

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
    R, p = fit.distribution_compare('power_law', 'lognormal')
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
        ln_goodness = '$\mu = {mu:.2f}; \sigma = {sigma:.3f}$'.format(mu=fit.lognormal.mu, sigma=fit.lognormal.sigma)
        ax.annotate(ln_goodness, xy=(.03, .05), xycoords='axes fraction', color='#2ca02c')
    #
    pw_label = r'Power law fit'
    ln_label = r'Lognormal fit'
    #ex_label = r'Lognormal fit'
    fit.power_law.plot_pdf(color='#aec7e8', linewidth=1, linestyle='--', label=pw_label, ax=ax)
    fit.lognormal.plot_pdf(color='#98df8a', linewidth=1, linestyle='--', label=ln_label, ax=ax)
    #fit.exponential.plot_pdf(color='#c5b0d5', linewidth=1, linestyle='--', label=ex_label, ax=ax)

    #
    ax.set_title(r'Semi-metric edges ($s_{{ij}}>1)$' '\n' '{source:s}'.format(source=folder))
    ax.set_ylabel(r'$P(s_{ij} \geq x)$')
    ax.set_xlabel(r'$s_{ij}$ frequency')

    ax.grid()

    ax.legend(loc='best')

    plt.tight_layout()
    # plt.subplots_adjust(left=0.09, right=0.98, bottom=0.07, top=0.90, wspace=0, hspace=0.0)
    plt.savefig(wImgFile, dpi=150, bbox_inches='tight')  # , pad_inches=0.05)


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
    plot_s_dist(folder)
    # Files
    #rGpickle = 'networks/{folder:s}/network-closure.gpickle'.format(folder=folder)
    #rGedgelist = 'networks/{folder:s}/network-closure.csv.gz'.format(folder=folder)
    #wGstats = 'networks/{folder:s}/network-stats.csv'.format(folder=folder)

    '''
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
    '''
