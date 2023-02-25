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


#def extract_n_random_graphs(G, n=1, *arg, **kwargs):
#    for i in range(n):
#        yield generate_random_graph(G, *arg, **kwargs)


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