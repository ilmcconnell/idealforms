import sys
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
from idealforms.formatters import Formatter, money_formatter, default_formatter
from typing import Dict, List, Tuple, Optional


DataDict = Dict[str, float]


def bar(data: DataDict,
        x_label: str,
        y_label: str,
        title: str,
        sort_on: str = 'values',
        sort_desc: bool = True,
        reverse_color_order: bool = False,
        axis_limit: Optional[float] = None,
        tick_count: int = 5,
        cmap_name: str = "Reds",
        in_bar_labels: bool = True,
        short_bar_label: str = 'out',
        figsize: Tuple[float, float] = (8, 4),
        formatter: Optional[Formatter] = None,
        **kwargs) -> Tuple[plt.Figure, plt.Axes]:
    """
    Plot a nice bar graph
    data: DataDict, dictinoary with data to plot, key: label v:bar height
    x_label: str, label for x axis - bar height values
    y_label: str, label for y axis - label categories
    title: str, title for chart
    sort: str = 'values' or 'alpha' sort by bar height or label name
    axis_limit: Optional[float] = None, set max bar height size
    tick_count: int = 5, set number of ticks to use for bar heights
    cmap_name: str = "Reds" matplot lib color map name to color bars
    in_bar_labels: bool = True, plot bar height value bar, False: plot outside bar
    short_bar_label: str = 'out', 'skip' if in bar label is too long for for bar, plot outside or don't plot
    figsize: Tuple[float, float] = (8, 4), overall fig size to plot
    formatter: Optional[Formatter] = None, idealforms.formatter class to use formatting data labels
    :return: Tuple[plt.Figure, plt.Axes]:
    """

    if not formatter:
        formatter = default_formatter

    # sort dict
    if sort_on == 'values':
        data = dict(sorted(data.items(),
                           key=lambda kv: kv[1],
                           reverse=sort_desc))  # type: ignore

    if sort_on == 'alpha':
        data = dict(sorted(data.items(),
                           key=lambda kv: kv[0],
                           reverse=sort_desc))  # type: ignore

    # split data dict into lists for plotting
    categories: List[str] = list(data.keys())
    heights: List[float] = list(data.values())

    # get params from data
    max_height: float = max(heights)
    data_color_normalized = [value/max_height for value in heights]
    if reverse_color_order:
        data_color_normalized = data_color_normalized[::-1]
    if not axis_limit:
        axis_limit = max_height

    # pyplot global params
    plt.rcParams.update({'figure.autolayout': True})
    plt.style.use('ggplot')

    # create figure and axes objects plus color mapping
    fig, ax = plt.subplots(figsize=figsize)
    my_cmap = plt.cm.get_cmap(cmap_name)
    my_cmap = my_cmap(np.linspace(0, 1, int(3*len(heights))))  # limit color range to darker colors
    my_cmap = ListedColormap(my_cmap[len(heights):, :-1])
    colors = my_cmap(data_color_normalized)
    renderer = fig.canvas.get_renderer()
    # plotting
    ax.barh(categories, heights, color=colors, **kwargs)
    ax.set(xlabel=x_label,
           ylabel=y_label,
           title=title,
           xlim=(0, axis_limit))

    # bar labels
    bar_end_offset = max_height/100
    bar_label_vertical_alignment = 'center'
    bar_label_fontsize = plt.rcParams['axes.labelsize']
    if in_bar_labels:
        for i, height in enumerate(heights):
            i, height = int(i), int(height)
            txt = ax.text(height - bar_end_offset, i, formatter(height, None),
                          fontsize=bar_label_fontsize,
                          verticalalignment=bar_label_vertical_alignment,
                          horizontalalignment='right',
                          c='white')
            bb = txt.get_window_extent(renderer=renderer).transformed(ax.transData.inverted())
            label_length = bb.width
            bar_length = ax.patches[i].get_width()
            if label_length > bar_length and short_bar_label == 'out':
                txt.set_x(height + bar_end_offset)
                txt.set_horizontalalignment('left')
                txt.set_color('black')
            elif label_length > bar_length and short_bar_label == 'skip':
                txt.set_text('')

    if not in_bar_labels:
        for i, height in enumerate(data.values()):
            i, height = int(i), int(height)
            ax.text(height + bar_end_offset, i, formatter(height, None),
                    fontsize=bar_label_fontsize,
                    verticalalignment=bar_label_vertical_alignment,
                    horizontalalignment='left',
                    c='black')

    # x axes formatting
    labels = ax.get_xticklabels()
    plt.setp(labels,
             rotation=45,
             horizontalalignment='right')
    ax.set_xticks(np.linspace(0,
                              axis_limit,
                              tick_count))
    ax.xaxis.set_major_formatter(formatter)

    # supress background, grid and spines
    ax.patch.set_facecolor('white')
    ax.patch.set_alpha(0)
    ax.grid(False)
    for spine in ['top', 'right', 'bottom', 'left']:
        ax.spines[spine].set_visible(False)

    # plot baseline
    ax.axvline(0, c='grey', linewidth=1, zorder=3)

    # plot bar gradations
    for p in ax.patches:
        for tick in ax.get_xticks():
            if tick < p.get_width() and tick != 0:
                ax.plot([tick, tick], [p.xy[1], p.xy[1] + p.get_height()],
                        linewidth=.75,
                        c='lightgrey')

    return fig, ax


def main():
    data = dict(apples=500000.0,
                oranges=1200000.0,
                mangos=2200005.0)

    fig, ax = bar(data,
                  x_label='revenue',
                  y_label='fruit',
                  title='Fruit Revenue',
                  sort_on='values',
                  axis_limit=2500000,
                  formatter=money_formatter)

    return fig, ax


def init():
    if __name__ == '__main__':
        sys.exit(main())


init()
