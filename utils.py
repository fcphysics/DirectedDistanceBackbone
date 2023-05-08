import os
# import sys
import random
import networkx as nx


def extract_metric_graph(G):
    GM = G.copy()
    edges2remove = [(i, j) for i, j, d in G.edges(data=True) if d['is_metric'] == False]
    GM.remove_edges_from(edges2remove)
    return GM


def extract_ultrametric_graph(G):
    GU = G.copy()
    edges2remove = [(i, j) for i, j, d in G.edges(data=True) if d['is_ultrametric'] == False]
    GU.remove_edges_from(edges2remove)
    return GU


def extract_random_graph(G, edges_to_keep=0):
    GR = G.copy()
    edges2remove = random.sample(list(GR.edges(data=True)), edges_to_keep)
    GR.remove_edges_from(edges2remove)
    return GR


def extract_threshold_graph(G, edges_to_keep=0):
    GT = G.copy()
    edges2remove = sorted(GT.edges(data=True), key=lambda x: x[2]['weight'])[:-edges_to_keep]
    GT.remove_edges_from(edges2remove)
    return GT


def get_graph_variables(G, *arg, **kwargs):
    dM = nx.get_node_attributes(G, *arg)
    s = set(dM.values())
    n = len(s)
    sM = {m: set([k for k, v in dM.items() if v == m]) for m in s}
    #
    return n, s, sM, dM


def ensurePathExists(filepath):
    """Given a file with path, ensures a path exists by creating a directory if needed. """
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))

def get_asymmetry_distribution(G, weight='proximity'):
    """ Compute the (absolute) asymmetry distribution in edge direction.

    Parameters
    ----------
    G : nx.Graph
        Networkx directed graph.
    weight : str, optional
        Attribute to compute the asymmetry with respect to, by default 'distance'.
    
    """
    
    if not nx.is_directed(G):
        raise NotImplementedError
    
    Gc = G.copy()
    nx.set_edge_attributes(Gc, name='asymmetry', values=2.0)
    
    alpha_values = []
    for u, v, d in Gc.edges(data=True):
        if d['asymmetry'] == 2.0:
            if Gc.has_edge(v, u):
                if Gc[u][v][weight] == Gc[v][u][weight]:
                    alpha = 0.0
                else:
                    alpha = (Gc[u][v][weight] - Gc[v][u][weight])/(Gc[u][v][weight] + Gc[v][u][weight])
                
                Gc[u][v]['asymmetry'] = alpha
                Gc[v][u]['asymmetry'] = -alpha
                alpha_values.append(abs(alpha))
            else:
                Gc[u][v]['asymmetry'] = 1.0
                alpha_values.append(1.0)
                
    return alpha_values

def fuzzy_reciprocity(G, weight='proximity'):
    
    pbar = sum(list(dict(nx.get_edge_attributes(G, name=weight)).values()))/(G.number_of_nodes()*(G.number_of_nodes() - 1))    
    
    cov = 0
    stdev = 0
    for u, v in G.edges():
        if G.has_edge(v, u):
            cov += (G[u][v][weight] - pbar)*(G[v][u][weight] - pbar)
        else:
            cov -= pbar*(G[u][v][weight] - pbar)
        stdev += (G[u][v][weight] - pbar)*(G[u][v][weight] - pbar)
    
    return cov/stdev

def venn3_sqr_diagram(Ne, Nb, Nc, Nbc, width=0.1, title=None):

    import matplotlib.patches as mpatches
    import matplotlib.pyplot as plt
    import numpy as np
    
    fig, ax = plt.subplots(figsize=(5, 10))
    fig.set_facecolor('tab:gray')
    ax.set_facecolor('tab:gray')
    
    L1 = Nb/Ne
    L2 = Nc/Ne
    L3 = Nbc/Ne
        
    artist = [mpatches.Rectangle((0.0, 0.0), width, 1.0, color='b'),
              mpatches.Rectangle((0.0, 0.0), width, L1, color='g'),
              mpatches.Rectangle((0.0, L1-L3), width, L2, color='r', alpha=0.5)]
    
    for art in artist:
        ax.add_artist(art)
    
    ax.text(0.5*width, 0.5*(L1-L3), Nb-Nbc, verticalalignment='center', horizontalalignment='center', color='w')
    ax.text(0.5*width, (L1-L3)+0.5*L3, Nbc, verticalalignment='center', horizontalalignment='center', color='w')
    ax.text(0.5*width, L1+0.5*(L2-L3), Nc-Nbc, verticalalignment='center', horizontalalignment='center', color='w')
    ax.text(0.5*width, 0.5*(1+L1+L2-L3), Ne-(Nb+Nc-Nbc), verticalalignment='center', horizontalalignment='center', color='w')
    
    ax.text(1.01*width, 0.5*(L1-L3), 'Backbone WCC', verticalalignment='center', horizontalalignment='left', color='k')
    ax.text(1.01*width, (L1-L3)+0.5*L3, 'Backbone LSCC', verticalalignment='center', horizontalalignment='left', color='k')
    ax.text(1.01*width, L1+0.5*(L2-L3), 'Semi-metric LSCC', verticalalignment='center', horizontalalignment='left', color='k')
    ax.text(1.01*width, 0.5*(1+L1+L2-L3), 'Semi-Metric WCC', verticalalignment='center', horizontalalignment='left', color='k')
    
    ax.set_title(title)
    ax.set_xlim((0.0, 1.3*width))
    #ax.set_ylim((-pad, 0.5+pad))
    ax.set_axis_off()
    
    #plt.show()
    plt.savefig(f'Figures/Components/{title}.png')
    
    
def plot_s_dist(data, folder):
    
    import matplotlib.pyplot as plt
    import powerlaw
    import pandas as pd
    
    ss = pd.Series(list(data), name='s-value')

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
    plt.savefig(f'{folder}.pdf', dpi=150, bbox_inches='tight')
    #plt.show()