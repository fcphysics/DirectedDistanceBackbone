from matplotlib_venn import venn2, venn3, venn2_circles
import matplotlib.pyplot as plt
import pandas as pd

import configparser
import networkx as nx

# Make sure we don't try to do GUI stuff when running tests
import sys, os
if 'py.test' in os.path.basename(sys.argv[0]): # (XXX: Ugly hack)
    import matplotlib
    matplotlib.use('Agg')

from matplotlib.pyplot import gca

from matplotlib_venn._common import *
from matplotlib_venn._venn2 import compute_venn2_subsets, compute_venn2_areas, solve_venn2_circles, compute_venn2_regions, compute_venn2_colors

def custom_venn2(subsets, set_labels=('A', 'B'), set_colors=('r', 'g'), alpha=0.4, normalize_to=1.0, ax=None, data_offset=0.0, label_offset=0.0, rounding=2):
    '''
    Custom version of venn2 from matplotlib_venn.
    '''
    if isinstance(subsets, dict):
        subsets = [subsets.get(t, 0) for t in ['10', '01', '11']]
    elif len(subsets) == 2:
        subsets = compute_venn2_subsets(*subsets)

    areas = compute_venn2_areas(subsets, normalize_to)
    centers, radii = solve_venn2_circles(areas)
    regions = compute_venn2_regions(centers, radii)
    colors = compute_venn2_colors(set_colors)

    if ax is None:
        ax = gca()
    prepare_venn_axes(ax, centers, radii)

    # Create and add patches and subset labels
    patches = [r.make_patch() for r in regions]
    for (p, c) in zip(patches, colors):
        if p is not None:
            p.set_facecolor(c)
            p.set_edgecolor('none')
            p.set_alpha(alpha)
            ax.add_patch(p)
    label_positions = [r.label_position() for r in regions]
    
    #print(label_positions)
    offset_positions = [0, 0]#[data_offset*[a.mid_point()[0] for a in r.arcs][1] for r in regions]
    for i in range(2):
        label_positions[i][0] += offset_positions[i]
    #print(label_positions)

    subset_labels = [ax.text(lbl[0], lbl[1], str(round(s/normalize_to, rounding)), va='center', ha='center') if lbl is not None else None for (lbl, s) in zip(label_positions, subsets)]

    # Position set labels
    if set_labels is not None:
        label_positions = [centers[0] + np.array([- radii[0], - 0.5*radii[0]]),
                           centers[1] + np.array([radii[1], 0.5*radii[0]])]
        for i in range(2):
            label_positions[i][0] += label_offset*offset_positions[i]
        labels = [ax.text(pos[0], pos[1], txt, size='large', ha='right', va='top') for (pos, txt) in zip(label_positions, set_labels)]
        labels[1].set_ha('left')
    else:
        labels = None
    return VennDiagram(patches, subset_labels, labels, centers, radii)


if __name__ == '__main__':
    
    # Build Venn Diagram with the edges in the LSCC that are metric
    # 1 - Metric edges not in LSCC
    # 2 - semi-metric LSCC edges in WCC
    # 3 - metric edges in LSCC
    # Normalize to - Edges in WCC
    #df = pd.read_csv('LOCAL/Edges_Components.csv')
    #df.set_index('network', inplace=True)
    #print(df)

    config = configparser.ConfigParser()
    config.read('networks.ini')
    networks = list(config.keys())[1:]

    for network in networks:
        
        folder = config[network].get('folder')
        
        GLS = nx.read_graphml('networks/{folder:s}/network_lscc.graphml'.format(folder=folder))
        G = nx.read_graphml('networks/{folder:s}/network.graphml'.format(folder=folder))
        
        BLS = nx.read_graphml('networks/{folder:s}/backbone_lscc.graphml'.format(folder=folder))
        B = nx.read_graphml('networks/{folder:s}/backbone.graphml'.format(folder=folder))
        
        metric_not_lscc = 0
        metric_in_lscc = 0
        semi_metric_lscc = 0
        
        for u, v in G.edges():
            if B.has_edge(u, v):
                if BLS.has_node(u) and BLS.has_node(v) and BLS.has_edge(u, v):
                    metric_in_lscc += 1
                else:
                    metric_not_lscc += 1
            elif GLS.has_node(u) and GLS.has_node(v) and GLS.has_edge(u, v):
                semi_metric_lscc += 1
        
        nedges = G.number_of_edges()
        print(network, metric_not_lscc/nedges, semi_metric_lscc/nedges, metric_in_lscc/nedges)
        
        fig, ax = plt.subplots()
        custom_venn2(subsets = (metric_not_lscc, semi_metric_lscc, metric_not_lscc), 
                     set_labels = ('Backbone', 'LSCC'), alpha=0.7, normalize_to=G.number_of_edges())
        ax.set_title(network)
        plt.tight_layout()
        plt.savefig('networks/{folder:s}/components_backbone.pdf'.format(folder=folder), dpi=300)
        plt.clf()
        #break
