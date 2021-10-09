
import sys
import itertools
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tk
from matplotlib.lines import Line2D

"""Simple and logged scatter plots for cerebellum and cerebrum morphology in primates.
Saves simple and logged plots to separate files. Will by default open windows with each figure,
comment out 'plt.show()' at end of file to save only."""

# TODO: make function take col_names list so they can choose.

try:
    data = pd.read_csv('all_species_values.csv', na_values='', usecols=range(7))
    data = data.dropna(how='all', axis='columns').drop(columns='Source')
    data.rename(columns={
        'Species ': 'Species',
        'CerebellumSurfaceArea': 'Cerebellum Surface Area',
        'CerebrumSurfaceArea': 'Cerebrum Surface Area',
        'CerebellumVolume ': 'Cerebellum Volume',
        'CerebrumVolume': 'Cerebrum Volume'
        }, inplace=True)

except FileNotFoundError:
    print('Please ensure you have the \'all_species_values.csv\' '
          'in the same directory as this program.')
    sys.exit()

colors = {
    'Hominidae':  '#7f48b5',
    'Hylobatidae': '#c195ed',
    'Cercopithecidae': '#f0bb3e',
    'Platyrrhini': '#f2e3bd'
    }

# Column 3 (Cerebrum Surface Area) is not plotted due to not enough data.
# Add '2' to index list below if want to include that column.
col_names = data.columns.to_numpy()[[4, 3, 1]]
var_combinations = tuple(itertools.combinations(col_names, 2))

# Gives legend markers same color as predefined taxon colors
handles = [
    Line2D([0], [0],
           color='w', marker='o', markerfacecolor=v,
           markeredgecolor='k',  markeredgewidth='0.5',
           markersize=4, label=k,
           ) for k, v in colors.items()
        ]


def plot_data(xy=var_combinations, logged=False):

    plt.rcParams['xtick.minor.size'] = 0
    plt.rcParams['xtick.minor.width'] = 0
    plt.rcParams['ytick.minor.size'] = 0
    plt.rcParams['ytick.minor.width'] = 0

    if not logged:
        fig1, axs1 = plt.subplots(1, (len(xy)), figsize=(16, 5), squeeze=False)
        axs1 = axs1.flatten()

        for i, (x, y) in enumerate(xy):
            axs1[i].scatter(data[x], data[y], c=data.Taxon.map(colors), edgecolor='k')

            axs1[i].set(
                title=f'Primate {xy[i][0]} against\n{xy[i][1]}',
                xlabel=f'{xy[i][0]}',
                ylabel=f'{xy[i][1]}'
            )

            ax_legend = axs1[i].legend(
                title='Taxon',
                title_fontsize='9',
                handles=handles,
                loc='upper left',
                fontsize=10
            )
            ax_legend.get_frame().set_color('white')

            fig1.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
            fig1.savefig('Simple Cerebellum Project Plots.png', bbox_inches='tight')

    elif logged:
        fig2, axs2 = plt.subplots(1, len(xy), figsize=(16, 5), squeeze=True)
        axs2 = axs2.flatten()

        for i, (x, y) in enumerate(xy):
            axs2[i].scatter(data[x], data[y], c=data.Taxon.map(colors), edgecolor='k')

            axs2[i].set(
                title=f'Logged Primate {xy[i][0]} against\n{xy[i][1]}',
                xlabel=f'Logged {xy[i][0]}',
                ylabel=f'Logged {xy[i][1]}'
            )

            ax_legend = axs2[i].legend(
                title='Taxon',
                title_fontsize='9',
                handles=handles,
                loc='upper left',
                fontsize=10
            )
            ax_legend.get_frame().set_color('white')

            axs2[i].set_xscale('log')
            axs2[i].get_xaxis().set_major_formatter(tk.ScalarFormatter())
            axs2[i].set_xticks([1, 5, 10, 25, 50, 100, 200, 400])

            axs2[i].set_yscale('log')
            axs2[i].get_yaxis().set_major_formatter(tk.ScalarFormatter())
            axs2[i].set_yticks([10, 25, 50, 100, 250, 500, 1000])

            fig2.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
            fig2.savefig('Logged Cerebellum Project Plots.png', bbox_inches='tight')


plot_data()

plot_data(logged=True)

plot_data((
    ('Cerebellum Surface Area', 'Cerebrum Volume'),),
    logged=True
    )

plt.show()
