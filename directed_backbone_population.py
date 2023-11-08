# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 16:35:36 2023

@author: Felipe Xavier Costa
"""

import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import seaborn as sns

simas_metric = [16.14, 37.15, 1.75, 5.5, 9.23, 17.57, 46.97, 
                49.25, 7.84, 9.5, 31.96, 77.27, 81.13, 83.59, 
                2, 4.36, 8.1, 22.4, 27.49]

simas_ultrametric = [8.98, 16.75, 0.83, 0.2, 5.66, 5.53, 13.97, 
                     5.53, 0.66, 2.9, 11.65, 62.77, 70.62, 78.45, 
                     0.43, 1.47, 7.59, 7.79]

wcc_metric = [6.37, 47.44, 54, 55.69, 59, 99.86, 2.6, 35.08, 
              41.43, 51.49, 59.62, 70.51, 76.67, 91.63, 1.71, 
              24.67, 26.65, 27.43, 36.78, 59.53]

wcc_ultrametric = [1.38, 2.17, 27.69, 26.77, 40.49, 99.84, 0.89, 
                  9.76, 21.99, 22.67, 23.78, 64.75, 33.33, 84.89, 
                  1.22, 5.44, 7.66, 18.98, 25.37, 2.75]

lscc_metric = [6.62, 53.43, 55.32, 47.44, 59, 36.52, 43.02, 
               52.85, 58.25, 66.12, 2.6, 76.67, 59.53, 88.32, 
               27.11, 38, 1.71, 24.67, 26.65]

lscc_ultrametric = [1.55, 26.82, 25.67, 2.17, 40.49, 9.46, 
                    20.88, 22.02, 21.19, 59.92, 0.89, 33.33, 
                    2.75, 77.37, 18.63, 25.63, 1.22, 5.44, 7.66]

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

data = {'metric' :[simas_metric, lscc_metric, wcc_metric], 'ultrametric': [simas_ultrametric, lscc_ultrametric, wcc_ultrametric]}

'''
from itertools import permutations

for btype, sets in data.items():
    print(btype)
    for i, j in permutations(range(len(sets)), 2):
        U, p = stats.mannwhitneyu(sets[i], sets[j], alternative='less')
        print(i, j, U, p)
'''

fig, ax = plt.subplot_mosaic(np.array(list(data.keys())).reshape(1, len(data.keys())), figsize=(16, 8))

for btype, sets in data.items():
    ax[btype].boxplot(sets, labels=[r'Simas $\it{et\,\, al.}$ 2021', 'LSCC', 'WCC'], widths=0.4)
    for idx, vals in enumerate(sets):
        ax[btype].scatter(np.full(len(vals), idx+1), vals, c='k', marker='o', alpha=0.25)
    
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
