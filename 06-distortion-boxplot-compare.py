# coding=utf-8
# Author: Rion B Correia
# Date: Dec 05, 2017
#
# Description:
# Plot S_{ij} value distribution for networks
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
# Networks
import networkx as nx

# Violinplot
import seaborn as sns
from matplotlib import ticker as mticker


def generate_original_graph(G):
    GO = G.copy()
    edges2remove = [(i, j) for i, j, d in G.edges(data=True) if 'is_original' not in d]
    GO.remove_edges_from(edges2remove)
    return GO


def plot_global_boxplots(dfp):
    #print('Iterating networks')
    lsvals = []
    for idx, label, source, color in dfp.to_records():
        print("> Network: {label:s}".format(label=label))
        
        # Init
        rGpickle = 'networks/%s/network-closure.gpickle' % (source)


        # Load Network
        print('--- Loading Network gPickle (%s) ---' % (rGpickle))
        G = nx.read_gpickle(rGpickle)
        print('Network: %s' % (G.name))
        #
        # SubGraphs
        #
        # Original Graph, without the metric closure
        GO = generate_original_graph(G)

        #[d.get('s-value') for i, j, d in GO.edges(data=True) if float(d.get('s-value') or 0.0) > 1], reverse=True)
        ss = pd.Series([d.get('s-value') for i, j, d in GO.edges(data=True)], name='s-value')
        svals = sorted(ss.loc[(ss > 1.0)].sort_values(ascending=False), reverse=True)
        ## Compute Quartiles
        print("Q1: {}".format(np.quantile(svals, 0.25)))
        print("Median: {}".format(np.median(svals)))
        print("Q3: {}".format(np.quantile(svals, 0.75)))
        lsvals.append(svals)
        #lsvals.append(np.log10(svals))

    dfp['s-values'] = lsvals
    print(dfp)
    #
    wImgFile = "compare-s-values-US-Airports.pdf"

    # Plot
    fig, ax = plt.subplots(figsize=(5.5, 3.6))


    '''
    flierprops = {'marker': '.', 'markeredgecolor': '#7f7f7f'}
    meanprops = {'marker': 'o', 'markerfacecolor': 'black', 'markeredgecolor': 'black', 'ms': 7}
    medianprops = {'color': 'white', 'lw': 2}

    bp = ax.boxplot(dfp['s-values'].to_list(),
                    widths=0.60, notch=True, showfliers=True, showmeans=True, patch_artist=True,
                    flierprops=flierprops,
                    meanprops=meanprops,
                    medianprops=medianprops)

    for patch, color in zip(bp['boxes'], dfp['color'].tolist()):
        patch.set_facecolor(color)
    '''

    sns.violinplot(data=dfp['s-values'].to_list(), ax=ax)
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("$10^{{{x:.0f}}}$"))
    ymin, ymax = ax.get_ylim()
    tick_range = np.arange(np.floor(ymin), ymax)
    ax.yaxis.set_ticks(tick_range)
    ax.yaxis.set_ticks([np.log10(x) for p in tick_range for x in np.linspace(10 ** p, 10 ** (p + 1), 10)], minor=True)

    ax.set_title('U.S. Airports')
    ax.set_xticklabels(dfp['label'].to_list())
    #ax.set_yscale('log')

    #ax.set_ylabel(r'$log(s_{ij}>1)$', fontsize='x-large')
    ax.set_ylabel(r'$s_{ij}>1$', fontsize='x-large')
    ax.grid()

    plt.tight_layout()
    #plt.subplots_adjust(left=0.12, right=0.97, bottom=0.10, top=0.95, wspace=0, hspace=0.0)
    plt.savefig(wImgFile, dpi=150)  # , pad_inches=0.05)
    #plt.show()


if __name__ == '__main__':
    #
    # Init
    #
    source = ''  # sociopatterns, salathe, toth
    # # salathe: high-school
    # # sociopatterns: exhibit, high-school, hospital, conference, primary-school, workplace
    # # toth: elementary-school, middle-school
    project = ''
    normalization = ''  # social, time, time_all
    # time_window = '20S'

    # # For Toth projects
    # # - elementary-school = ['2013-01-31','2013-02-01','all']
    # # - middle-school = :['2012-11-28','2012-11-29','all']
    #date = 'all'
    date = None
    date = ''

    data = [
        ('Undirected', 'us-airports-2006-undirected'),
        ('Directed', 'us-airports-2006')
    ]
    dfp = pd.DataFrame(data, columns=['label', 'source'])
    #dfp['color'] = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']#, '#bcbd22']
    dfp['color'] = ['#1f77b4', '#ff7f0e']

    #print(dfp)
    plot_global_boxplots(dfp)