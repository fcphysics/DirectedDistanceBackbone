import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
import numpy as np

#import matplotlib
#matplotlib.use('TkAgg')

##############################
## Backbone Size Comparison ##
##############################

df = pd.read_csv('Summary/BackboneCompareStats.csv', index_col=0)

fig, ax = plt.subplots(1, 2, figsize=(12, 6))

# Same commands for both axis
ax[0].scatter(df['metric'], df[f'metric_avg'], marker='s', c='g', label='Average')
ax[1].scatter(df['ultrametric'], df[f'ultrametric_max'], marker='^', c='b', label='Maximum')

for i in range(2):
    ax[i].plot([0, 1], [0, 1], 'k-')
    #ax[i].legend(fontsize=12, loc=4)
    ax[i].set_aspect('equal')

ax[0].set_title('Metric Backbone Size', fontsize=20)    
ax[0].set_ylabel(r'$\tau^m(\Delta^{avg})$', fontsize=16)
ax[0].set_xlabel(r'$\tau^m(\tilde{D})$', fontsize=16)

ax[1].set_title('Ultrametric Backbone Size', fontsize=20)    
ax[1].set_ylabel(r'$\tau^u(\Delta^{max})$', fontsize=16)
ax[1].set_xlabel(r'$\tau^u(\tilde{D})$', fontsize=16)

# Add Ultrametric inset
axes = zoomed_inset_axes(ax[1], 4.0, loc=2, borderpad=1.8)
axes.scatter(df['ultrametric'], df['ultrametric_max'], marker='^', c='b', label='Maximum')
axes.plot([0, 0.1], [0, 0.1], 'k-')

axes.yaxis.tick_right()
axes.set_xlim((0, 0.1))
axes.set_ylim((0, 0.1))
axes.set_aspect('equal')
axes.set_yticks([0.0, 0.05, 0.10])

plt.tight_layout()
#plt.show()
plt.savefig('Figures/BackboneSizeComparison.png', dpi=300)


'''
##############################
## Fuzzy Reciprocity Change ##
##############################


df_rho = pd.read_csv('Summary/ReciprocitySummary.csv', index_col=0)

data = {'y': [df_rho.rhoM, df_rho.rhoU], 'color': [df_rho.tauM, df_rho.tauU], 'label': ['Metric', 'Ultrametric']}
outliers = {'giraffe': [0.703352800982276, 0.6973506911729956], 'caviar': [0.6719405559626447,0.6704650849232279]}

lims = [0, 1]

for i in range(2):
    fig, ax = plt.subplots(figsize=(6, 6))
    
    sc = ax.scatter(df_rho.rho, data['y'][i], c=data['color'][i], cmap='summer', vmin=0, vmax=1)
    
    divider = make_axes_locatable(ax)
    ax_cb = divider.append_axes("right", size="5%", pad=0.05)
    fig.add_axes(ax_cb)
    plt.colorbar(sc, cax=ax_cb)
    ax_cb.set_ylabel('Backbone Size')
    
    ax.plot(lims, lims, '-k')
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    
    ax.set_ylabel('{label:s} Fuzzy Reciprocity'.format(label=data['label'][i]))
    ax.set_xlabel('Fuzzy Reciprocity')
    
    # Annotate networks with increase in reciprocity <-> decrease in directionality
    ax.annotate("Giraffe Socialization", xy=(0.663235714889572, outliers['giraffe'][i]), xytext=(0.4, 0.8), arrowprops=dict(arrowstyle="->"))
    ax.annotate("Caviar Project", xy=(0.6718661800354505, outliers['caviar'][i]), xytext=(0.3, 0.6), arrowprops=dict(arrowstyle="->"))
    
    plt.tight_layout()
    plt.savefig('Figures/{type:s}FuzzyReciprocity.pdf'.format(type=data['label'][i]), dpi=300)

#####################################
## Distortion Comparison - LogMean ##
#####################################


data = pd.read_csv('Summary/DistortionLogMean.csv', index_col=0)

fig, ax = plt.subplots(figsize=(6,6))

ax.scatter(data.directed, data.undirected, s=50, c='b')
ax.plot([0.0625, 8], [0.0625, 8], 'k-', lw=2)
ax.set_xlabel('Directed Distortion - Log Average')
ax.set_ylabel('Undirected Distortion - Log Average')

ax.set_xscale("log", base=2)
ax.set_yscale("log", base=2)

# Annotate networks that have larger undirected than directed backbone
ax.annotate("Telephone Calls", xy=(0.569559151142854, 0.513767171865907), xytext=(1.0, 0.4), arrowprops=dict(arrowstyle="->"))
ax.annotate("Drug Drug Interactions", xy=(0.874147261829192, 0.736701612921851), xytext=(1.5, 1.0), arrowprops=dict(arrowstyle="->"))
ax.annotate("Co-morbidity Risk", xy=(0.275701591576709, 0.247037530217323), xytext=(1.0, 0.12), arrowprops=dict(arrowstyle="->"))

#plt.show()
plt.tight_layout()
plt.savefig('Figures/DistortionComparison.pdf', dpi=300)



####################################
## Distortion Comparison - Median ##
####################################


data = pd.read_csv('Summary/Distortion_Median.csv', index_col=0)

fig, ax = plt.subplots(figsize=(6,6))

ax.scatter(data.directed, data.undirected, s=50, c='b')
ax.plot([1, 2048], [1, 2048], 'k-', lw=2)
ax.set_xlabel('Directed Distortion - Median')
ax.set_ylabel('Undirected Distortion - Median')

ax.set_xscale("log", base=2)
ax.set_yscale("log", base=2)

# Annotate networks that have larger undirected than directed backbone
ax.annotate("Telephone Calls", xy=(1.7674876847290641,1.6737934181360763), xytext=(8.0, 2.0), arrowprops=dict(arrowstyle="->"))
ax.annotate("Drug Drug Interactions", xy=(2.3968306435179834, 2.08905174785705), xytext=(8.0, 4.0), arrowprops=dict(arrowstyle="->"))
ax.annotate("Co-morbidity Risk", xy=(1.317454667101697, 1.2802271595641688), xytext=(4.0, 1.2), arrowprops=dict(arrowstyle="->"))

#plt.show()
plt.tight_layout()
plt.savefig('Figures/DistortionMedianComparison.pdf', dpi=300)

'''