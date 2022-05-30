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


def extract_n_random_graphs(G, n=1, *arg, **kwargs):
    for i in range(n):
        yield generate_random_graph(G, *arg, **kwargs)


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
