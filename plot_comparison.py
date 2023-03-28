import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable

##############################
## Backbone Size Comparison ##
##############################


data = pd.read_csv('Summary/BackboneSizeComparison.csv', index_col=0)

fig, ax = plt.subplots(figsize=(6,6))

ax.scatter(data.directed, data.undirected, s=50, c='b')
ax.plot([0, 1], [0, 1], 'k-', lw=2)
ax.set_xlabel('Directed Backbone Size')
ax.set_ylabel('Undirected Backbone Size')


# Annotate networks that have larger undirected than directed backbone
ax.annotate("Manizales Mobility", xy=(0.084591, 0.085090), xytext=(0.0, 0.3), arrowprops=dict(arrowstyle="->"))
ax.annotate("Giraffe Socialization", xy=(0.766667, 0.800000), xytext=(0.55, 0.9), arrowprops=dict(arrowstyle="->"))
ax.annotate("Co-morbidity Risk", xy=(0.474356, 0.505039), xytext=(0.3, 0.6), arrowprops=dict(arrowstyle="->"))

#plt.show()
plt.tight_layout()
plt.savefig('SizeComparison.pdf', dpi=300)

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
    plt.savefig('{type:s}FuzzyReciprocity.pdf'.format(type=data['label'][i]), dpi=300)

###########################
## Distortion Comparison ##
###########################


data = pd.read_csv('Summary/DistortionLogMean.csv', index_col=0)

print(len(data.directed))

fig, ax = plt.subplots(figsize=(6,6))

ax.scatter(data.directed, data.undirected, s=50, c='b')
ax.plot([0, 8], [0, 8], 'k-', lw=2)
ax.set_xlabel('Directed Distortion - Log Average')
ax.set_ylabel('Undirected Distortion - Log Average')

#ax.set_xscale("log")
#ax.set_yscale("log")

# Annotate networks that have larger undirected than directed backbone
ax.annotate("Telephone Calls", xy=(0.569559151142854, 0.513767171865907), xytext=(1.0, 0.4), arrowprops=dict(arrowstyle="->"))
ax.annotate("Drug Drug Interactions", xy=(0.874147261829192, 0.736701612921851), xytext=(1.5, 1.0), arrowprops=dict(arrowstyle="->"))
ax.annotate("Co-morbidity Risk", xy=(0.275701591576709, 0.247037530217323), xytext=(1.0, 0.05), arrowprops=dict(arrowstyle="->"))

#plt.show()
plt.tight_layout()
plt.savefig('DistortionComparison.pdf', dpi=300)
