import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
import numpy as np

###############################
###  Backbone Sizes Tables  ###
###############################

def percent_round(x):
    return np.round(100*x, 2)

def scientific(x):
    return "{:.2e}".format(x)

'''
for files in ['BackboneStats', 'BackboneStats_LSCC']:
    df = pd.read_csv(f'Summary/{files}.csv', index_col=0)
    df.reset_index(inplace=True)
    df.sort_values(['type', 'tau_metric'], inplace=True)
    #print(df)
    df.to_latex(f'LOCAL/Tables/{files}.tex', columns=['index', 'n_nodes', 'nedges', 'density', 'tau_metric', 'tau_ultrametric', 'ultra_per_metric'],
                index=False, header=['Network', '$ \ abs  X $', '$ \ abs D(X) $', 'Density', '$\ tau^m$', '$\ tau^u$', '$ \ tau^u / \ tau^m $'],
                column_format='l|l|rrr|c|c|c|', formatters={'index': str, 'n_nodes': int, 'nedges': int, 'density': scientific, 'tau_metric': percent_round, 'tau_ultrametric': percent_round, 'ultra_per_metric': percent_round})
    #break

    
df = pd.read_csv(f'Summary/StrongComponents.csv', index_col=0)
df.reset_index(inplace=True)
#df.sort_values(['type', 'tau_metric'], inplace=True)
#print(df)
df.to_latex(f'LOCAL/Tables/StrongComponents.tex', columns=['index', 'nodes', 'components', 'lscc', 'isolates', 'tuples', 'chains', 'stars', 'trees', 'reducible'],
            index=False, header=['Network', '$ \ abs  X $', '$ \ abs SCC(D(X)) $', '$ \ abs LSCC(X) $', 'Isolates', 'Tuples', 'Chains', 'Stars', 'Trees', 'Reducibles'],
            column_format='l|cc|c|ccccc|c', formatters={'index': str, 'nodes': int, 'components': int, 'lscc': int, 'isolates': int, 'tuples': int, 'chains': int, 'stars': int, 'trees': int, 'reducible': int})
'''

df = pd.read_csv('Summary/UndirectedBackboneStats.csv', index_col=0)
df.reset_index(inplace=True)
df.sort_values(['type', 'metric'], inplace=True)
#print(df)
df['max_edges'] = df['n_nodes']*(df['n_nodes']-1)
df['density'] = df['nd_edges']/df['max_edges'] 
df['ultra_per_metric'] = df.ultrametric/df.metric
df.to_latex(f'LOCAL/Tables/UndirectedBackboneStats.tex', columns=['index', 'n_nodes', 'nd_edges', 'density', 'metric', 'ultrametric', 'ultra_per_metric'],
            index=False, header=['Network', '$ \ abs  X $', '$ \ abs D(X) $', 'Density', '$\ tau^m$', '$\ tau^u$', '$ \ tau^u / \ tau^m $'],
            column_format='l|l|rrr|c|c|c|', formatters={'index': str, 'n_nodes': int, 'nd_edges': int, 'density': scientific, 'metric': percent_round, 'ultrametric': percent_round, 'ultra_per_metric': percent_round})
