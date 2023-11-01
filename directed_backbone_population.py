# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 16:35:36 2023

@author: Felipe Xavier Costa
"""

import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

simas_metric = [16.14, 37.15, 1.75, 5.5, 9.23, 17.57, 46.97, 
                49.25, 7.84, 9.5, 31.96, 77.27, 81.13, 83.59, 
                2, 4.36, 8.1, 22.4, 27.49]

simas_ultrametric = [8.98, 16.75, 0.83, 0.2, 5.66, 5.53, 13.97, 
                     5.53, 0.66, 2.9, 11.65, 62.77, 70.62, 78.45, 
                     0.43, 1.47, 7.59, 7.79]



wcc_metric = [6.37, 47.44, 54, 55.69, 59, 99.86, 2.6, 35.08, 
              41.43, 51.49, 59.62, 70.51, 76.67, 91.63, 1.71, 
              24.67, 26.65, 27.43, 36.78, 59.53]

wcc_ultametric = [1.38, 2.17, 27.69, 26.77, 40.49, 99.84, 0.89, 
                  9.76, 21.99, 22.67, 23.78, 64.75, 33.33, 84.89, 
                  1.22, 5.44, 7.66, 18.98, 25.37, 2.75]



lscc_metric = [1.55, 26.82, 25.67, 2.17, 40.49, 9.46, 20.88, 
               22.02, 21.19, 59.92, 99.84, 0.89, 33.33, 2.75, 
               77.37, 18.63, 25.63, 1.22, 5.44, 7.66]

lscc_ultrametric = [23.39, 50.2, 46.41, 4.58, 68.63, 25.91, 48.53, 
                    41.67, 36.37, 90.63, 99.98, 34.22, 43.48, 4.62, 
                    87.6, 68.72, 67.44, 71.19, 22.06, 28.76]

def box_and_whisker(data, title, ylabel, xticklabels):
    """
    Create a box-and-whisker plot with significance bars.
    """
    ax = plt.axes()
    bp = ax.boxplot(data, widths=0.6, patch_artist=True)
    # Graph title
    ax.set_title(title, fontsize=14)
    # Label y-axis
    ax.set_ylabel(ylabel)
    # Label x-axis ticks
    ax.set_xticklabels(xticklabels)
    # Hide x-axis major ticks
    ax.tick_params(axis='x', which='major', length=0)
    # Show x-axis minor ticks
    xticks = [0.5] + [x + 0.5 for x in ax.get_xticks()]
    ax.set_xticks(xticks, minor=True)
    # Clean up the appearance
    ax.tick_params(axis='x', which='minor', length=3, width=1)

    # Change the colour of the boxes to Seaborn's 'pastel' palette
    colors = sns.color_palette('pastel')
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)

    # Colour of the median lines
    plt.setp(bp['medians'], color='k')

    # Check for statistical significance
    significant_combinations = []
    # Check from the outside pairs of boxes inwards
    ls = list(range(1, len(data) + 1))
    combinations = [(ls[x], ls[x + y]) for y in reversed(ls) for x in range((len(ls) - y))]
    for c in combinations:
        data1 = data[c[0] - 1]
        data2 = data[c[1] - 1]
        # Significance
        U, p = stats.mannwhitneyu(data1, data2, alternative='two-sided')
        if p < 0.05:
            significant_combinations.append([c, p])

    # Get info about y-axis
    bottom, top = ax.get_ylim()
    yrange = top - bottom

    # Significance bars
    for i, significant_combination in enumerate(significant_combinations):
        # Columns corresponding to the datasets of interest
        x1 = significant_combination[0][0]
        x2 = significant_combination[0][1]
        # What level is this bar among the bars above the plot?
        level = len(significant_combinations) - i
        # Plot the bar
        bar_height = (yrange * 0.08 * level) + top
        bar_tips = bar_height - (yrange * 0.02)
        plt.plot(
            [x1, x1, x2, x2],
            [bar_tips, bar_height, bar_height, bar_tips], lw=1, c='k')
        # Significance level
        p = significant_combination[1]
        if p < 0.001:
            sig_symbol = '***'
        elif p < 0.01:
            sig_symbol = '**'
        elif p < 0.05:
            sig_symbol = '*'
        text_height = bar_height + (yrange * 0.01)
        plt.text((x1 + x2) * 0.5, text_height, sig_symbol, ha='center', c='k')

    # Adjust y-axis
    bottom, top = ax.get_ylim()
    yrange = top - bottom
    ax.set_ylim(bottom - 0.02 * yrange, top)

    # Annotate sample size below each box
    for i, dataset in enumerate(data):
        sample_size = len(dataset)
        ax.text(i + 1, bottom, fr'n = {sample_size}', ha='center', size='x-small')

    plt.show()

box_and_whisker([simas_metric, wcc_metric, lscc_metric], 
                'title', 'ylabel', ['Simas', 'WCC', 'LSCC'])