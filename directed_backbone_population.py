# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 16:35:36 2023

@author: Felipe Xavier Costa
"""

import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
#import seaborn as sns
import pandas as pd

undirected_backbone = {'Network': ['Fr-Ho', 'It-SC', 'Ir-Ex-min', 'Ir-Ex-mean', 'Ir-Ex-max', 'Fr-Wo', 'Fr-PS', 'Fr-HS', 'US-ES', 'US-MS', 'US-HS', 'Freeman', 'Cond-mat-2003', 'Cond-mat', 'Net-Science', 'C-elegans', 'Enterocyte_GRN', 'HCN-Coarse', 'HCN-Fine', 'HCN-fMRI', 'HCN-Physical', 'Instagram_depression', 'MyLib-journals', 'MyLib-keywords', 'MyLib-users', 'Wikipedia-Fact'],
                       'metric': [19.05, 14.03, 39.17, 48.44, 57.71, 17.43, 9.5, 10.36, 6.82, 6.19, 7.84, 31.96, 77.27, 81.13, 83.59, 46.97, 1.75, 9.23, 17.57, 5.5, 49.25, 8.1, 22.4, 4.36, 27.49, 2],
                       'ultrametric': [None, None, None, None, None, None, None, None, None, None, None, 11.65, 62.77, 70.62, 78.45, 13.97, 0.83, 5.66, 5.53, 0.2, 5.53, 1.47, 7.59, 0.43, 7.79, None]}
df_und = pd.DataFrame.from_dict(undirected_backbone)

directed_backbone = {'Network': ['Yeast_GRN', 'Co-morbidity_Risk', 'CElegans-Male', 'CElegans-Hermaphrodite', 'DDI', 'host-pathogen', 'Colombia_calls', 'Business_Faculty', 'History_Faculty', 'Computer_Science_Faculty', 'Tennis_losses', 'CAVIAR_Project', 'Giraffe_Socialization', 'Students_calls', 'Colombia_mobility', 'Medellin_mobility', 'Manizales_mobility', 'US_Airports_2006', 'US_Weblinks', 'Bicycle_trips'],
                     'wcc_metric': [6.37, 47.44, 54.00, 55.69, 59.00, 99.86, 2.60, 35.08, 41.43, 51.49, 59.62, 70.51, 76.67, 91.63, 1.71, 24.67, 26.65, 27.43, 36.78, 59.53],
                     'wcc_ultrametric': [1.38, 2.17, 27.69, 26.77, 40.49, 99.84, 0.89, 9.76, 21.99, 22.67, 23.78, 64.75, 33.33, 84.89, 1.22, 5.44, 7.66, 18.98, 25.37, 2.75],
                     'lscc_metric': [6.62, 47.44, 53.43, 55.32, 59.00, None, 2.60, 36.52, 43.02, 52.85, 58.25, 66.12, 76.67, 88.32, 1.71, 24.67, 26.65, 27.11, 38.00, 59.53],
                     'lscc_ultrametric': [1.55, 2.17, 26.82, 25.67, 40.49, None, 0.89, 9.46, 20.88, 22.02, 21.19, 59.92, 33.33, 77.37, 1.22, 5.44, 7.66, 18.63, 25.63, 2.75]}
df_dir = pd.DataFrame.from_dict(directed_backbone)


def sig_symbol(p):
    if p < 0.001:
        return '***'
    elif p < 0.01:
        return '**'
    elif p < 0.05:
        return '*'

# Drawing #

#print(min(simas_metric), max(simas_metric))
#print(min(simas_ultrametric), max(simas_ultrametric))

data = {'metric' :[df_und.metric.dropna, df_dir.lscc_metric.dropna, df_dir.wcc_metric.dropna], 
        'ultrametric': [df_und.ultrametric.dropna, df_dir.lscc_ultrametric.dropna, df_dir.wcc_ultrametric.dropna]}

for btype in ['metric', 'ultrametric']:
    data[btype]


'''
from itertools import permutations

for btype, sets in data.items():
    print(btype)
    for i, j in permutations(range(len(sets)), 2):
        U, p = stats.mannwhitneyu(sets[i], sets[j], alternative='less')
        print(i, j, U, p)
'''

fig, ax = plt.subplot_mosaic(np.array(list(data.keys())).reshape(1, len(data.keys())), figsize=(16, 8))
sets = [None, None, None]
colors = ['#f1a340', '#998ec3', '#998ec3']
medianprops = dict(linestyle='solid', linewidth=1.5, color='k')

for btype in ['metric', 'ultrametric']:

    sets[0] = list(df_und[btype].dropna())
    sets[1] = list(df_dir[f'lscc_{btype}'].dropna())
    sets[2] = list(df_dir[f'wcc_{btype}'].dropna())
    #break
    
    bplot = ax[btype].boxplot(sets, labels=['Undirected', 'LSCC', 'WCC'], widths=0.4, vert=True, patch_artist=True, medianprops=medianprops)
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
    for idx, vals in enumerate(sets):
        ax[btype].scatter(np.full(len(vals), idx+1), vals, c=colors[idx], marker='o')
    
    bottom = 101
    eps = 0.01
    for i, j in [(0, 1), (0, 2)]:
        U, p = stats.mannwhitneyu(sets[i], sets[j], alternative='less')
        print(i, j, U/(len(sets[i])*len(sets[j])), p)
        ax[btype].plot([1+i+eps, 1+i+eps, 1+j-eps, 1+j-eps], [bottom, bottom+2, bottom+2, bottom], lw=1, c='k')
        ax[btype].text(1+0.5*(i+j), bottom+2.5, 'p={pval:.02f}'.format(pval=p), ha='center', c='k')
        bottom += 3
    
    ax[btype].set_ylabel(rf'$\tau^{btype[0]}$', fontsize=20, rotation=0)
    ax[btype].tick_params(axis='x', labelsize=18)
    ax[btype].set_title(f'{btype.capitalize()} Backbone', fontsize=20)
    #plt.xticks(fontsize=18)

plt.tight_layout()
plt.show()
