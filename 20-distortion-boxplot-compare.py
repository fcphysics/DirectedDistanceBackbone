# coding=utf-8
# Author: Rion B Correia
# Date: Dec 05, 2017
#
# Description:
# Compare directed and undirected S_{ij} value distribution for networks
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
import pickle as pk

def plot_global_boxplots(dfp, kind='metric', part=1):
    print('Iterating networks')
    lsvals = []
    for idx, label, folder, color in dfp.to_records():
        print("> Network: {label:s}".format(label=label))
        
        # Init
        rFdistortion = 'networks/{folder:s}/distortion.pickle'.format(folder=folder)
        
        data = pk.load(open(rFdistortion, 'rb'))
        ss = pd.Series(list(data[kind].values()), name='s-value')
        svals = sorted(ss.loc[(ss > 1.0)].sort_values(ascending=False), reverse=True)
        ## Compute Quartiles
        print("Q1: {}".format(np.quantile(svals, 0.25)))
        print("Median: {}".format(np.median(svals)))
        print("Q3: {}".format(np.quantile(svals, 0.75)))
        lsvals.append(np.log10(svals))
    
    xmax = np.ceil(max([max(svals) for svals in lsvals])+1)
    dfp['s-values'] = lsvals
    #print(dfp)
    #
    wImgFile = "compare-s-values-ordered-{kind:s}-part{part}.pdf".format(kind=kind, part=part)

    # Plot
    fig, ax = plt.subplots(figsize=(5.5, 3.6))

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

    #ax.set_title('Distortion comparison')
    ax.set_xticklabels(dfp['label'].to_list())
    #ax.set_yscale('log')
    ax.set_yticks(np.arange(0, xmax))
    ax.set_yticklabels([r'$10^{}$'.format(int(n)) for n in np.arange(0, xmax)])

    ax.set_ylabel(r'$s_{ij}>1$', fontsize='large')
    ax.grid()

    #plt.tight_layout()
    plt.subplots_adjust(left=0.12, right=0.97, bottom=0.10, top=0.95, wspace=0, hspace=0.0)
    plt.savefig(wImgFile, dpi=150)  # , pad_inches=0.05)


if __name__ == '__main__':
    #
    # Init
    #
    
    kind = 'ultrametric'
    
    data = [('Pipes', 'water-pipes'), ('Bike', 'bike-sharing'), ('C.S.', 'academic_hiring/computer_science'),
        ('Co. Risk', 'comorbidity'), ('Hist.', 'academic_hiring/history'), ('Giraffe', 'giraffe'), ('Tennis', 'tennis_losses')]

    dfp = pd.DataFrame(data, columns=['label', 'folder'])
    dfp['color'] = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']#, '#7f7f7f', '#bcbd22']

    plot_global_boxplots(dfp, kind=kind, part=1)
    
    data = [('Buss.', 'academic_hiring/business'), ('Worm Her.', 'celegans/hermaphrodite'), ('Calls', 'phone-calls'),
        ('Worm Male', 'celegans/male'), ('DDI', 'DDI'), ('Mob. Med.', 'mobility/medellin'), ('SSI', 'host-pathogen')]
    
    dfp = pd.DataFrame(data, columns=['label', 'folder'])
    dfp['color'] = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']#, '#7f7f7f', '#bcbd22']
    
    plot_global_boxplots(dfp, kind=kind, part=2)
    
    data = [('CAVIAR', 'caviar_proj'), ('Mob. Man.', 'mobility/manizales'), ('Yeast', 'yeast_grn'),
        ('US-Web.', 'weblinks_us'), ('US-Air.', 'us-airports-2006'), ('Col. Call', 'colombia_social/calls'),
        ('Col. Mob.', 'colombia_social/mobility')]
    
    dfp = pd.DataFrame(data, columns=['label', 'folder'])
    dfp['color'] = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']#, '#7f7f7f', '#bcbd22']
    
    plot_global_boxplots(dfp, kind=kind, part=3)