import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
import numpy as np

#import matplotlib
#matplotlib.use('TkAgg')

import configparser
config = configparser.ConfigParser()
config.read('networks.ini')
networks = list(config.keys())[1:]

Type = {'business-faculty': 'Social',
 'cs-faculty': 'Social',
 'history-faculty': 'Social',
 'caviar-proj': 'Social',
 'celegans-her': 'Biomedical',
 'celegans-male': 'Biomedical',
 'colombia-calls': 'Social',
 'colombia-mobility': 'Technological',
 'mobility-manizales': 'Technological',
 'mobility-medellin': 'Technological',
 'tennis-loss': 'Social',
 'yeast-grn': 'Biomedical',
 'bike-sharing': 'Technological',
 'giraffe': 'Social',
 'comorbidity': 'Biomedical',
 'phone-calls': 'Social',
 'us-airports': 'Technological',
 'DDI': 'Biomedical',
 'us-weblinks': 'Technological',
 'host-pathogen': 'Biomedical'}

###############################
###  Backbone Sizes Tables  ###
###############################

df_wcc = pd.DataFrame(columns=['type', 'n_nodes', 'nedges', 'density', 'tau_metric', 'tau_ultrametric', 'ultra_per_metric'], index=networks)
df_scc = pd.DataFrame(columns=['type', 'n_nodes', 'nedges', 'density', 'tau_metric', 'tau_ultrametric', 'ultra_per_metric'], index=networks)

for network in networks:
    folder = config[network].get('folder')
    
    data = pd.read_csv(f'networks/{folder}/network-stats.csv', index_col=0)
    
    df_wcc['type'][network] = Type[network]   
    for col in ['n_nodes', 'nedges', 'density', 'ultra_per_metric']:
        df_wcc[col][network] = data[network][col]    
    df_wcc['tau_metric'][network] = data[network]['nedges_metric']/data[network]['nedges']
    df_wcc['tau_ultrametric'][network] = data[network]['nedges_ultrametric']/data[network]['nedges']
    
    try:
        data = pd.read_csv(f'networks/{folder}/network_lscc-stats.csv', index_col=0)
    
        df_scc['type'][network] = Type[network]   
        for col in ['n_nodes', 'nedges', 'density', 'ultra_per_metric']:
            df_scc[col][network] = data[network][col]    
        df_scc['tau_metric'][network] = data[network]['nedges_metric']/data[network]['nedges']
        df_scc['tau_ultrametric'][network] = data[network]['nedges_ultrametric']/data[network]['nedges']
    except:
        df_scc.drop(labels=network, inplace=True)
    
print(df_wcc)
df_wcc.to_csv('Summary/BackboneStats.csv')
print(df_scc)
df_scc.to_csv('Summary/BackboneStats_LSCC.csv')



#################################
###  Undirected Sizes Tables  ###
#################################

df_cc = pd.DataFrame(columns=['type', 'n_nodes', 'nu_edges', 'nd_edges', 'metric', 'ultrametric', 
                              'metric_avg', 'ultrametric_avg', 'metric_max', 'ultrametric_max'], index=networks)
df_cc.drop('host-pathogen', inplace=True)

for network in networks:
    if network == 'host-pathogen':
        continue
    folder = config[network].get('folder')
    
    data = pd.read_csv(f'networks/{folder}/undirected-stats.csv', index_col=0)
    
    df_cc['type'][network] = Type[network]
    df_cc['n_nodes'][network] = data['n_nodes']['dir_scc']
    df_cc['nu_edges'][network] = data['nedges']['max']
    df_cc['nd_edges'][network] = data['nedges']['dir_scc']
        
    for btype in ['metric', 'ultrametric']:
        df_cc[f'{btype}'][network] = data[f'nedges_{btype}']['dir_scc']/df_cc['nd_edges'][network]
        for ntype in ['max', 'avg']:
            df_cc[f'{btype}_{ntype}'][network] = data[f'nedges_{btype}'][ntype]/df_cc['nu_edges'][network]
            
    
    #break

#print(df_cc)
df_cc.to_csv('Summary/UndirectedBackboneStats.csv')

