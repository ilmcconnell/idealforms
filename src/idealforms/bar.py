import sys
import matplotlib.pyplot as plt
import numpy as np
from idealforms.formatters import Formatter, money_formatter, default_formatter
from typing import Dict, List, Tuple, Union, Optional


DataDict = Dict[str, float]


def bar(data: DataDict,
        x_label: str,
        y_label: str,
        title: str,
        sort: str = 'values',
        axis_limit: Optional[float] = None,
        tick_count: int = 5,
        cmap_name: str = "Reds",
        in_bar_labels: bool = True,
        formatter: Optional[Formatter] = None) -> Tuple[plt.Figure, plt.Axes]:

    if not formatter:
        formatter = default_formatter

    # sort dict
    if sort == 'values':
        data = dict(sorted(data.items(),
                           key=lambda kv: kv[1]))  # type: ignore
    if sort == 'alpha':
        data = dict(sorted(data.items(),
                           key=lambda kv: kv[0],
                           reverse=True))  # type: ignore

    # split data dict into lists for plotting
    categories: List[str] = list(data.keys())
    heights: List[float] = list(data.values())

    # get params from data
    max_height: Union[int, float] = max(heights)
    data_color_normalized = [value/max_height for value in heights]
    if not axis_limit:
        axis_limit = max_height

    # pyplot global params
    plt.rcParams.update({'figure.autolayout': True})
    plt.style.use('ggplot')

    # create figure and axes objects plus color mapping
    fig, ax = plt.subplots(figsize=(8, 4))
    my_cmap = plt.cm.get_cmap(cmap_name)
    colors = my_cmap(data_color_normalized)

    # plotting
    ax.barh(categories, heights, color=colors)
    ax.set(xlabel=x_label,
           ylabel=y_label,
           title=title,
           xlim=(0, axis_limit))

    # bar labels
    bar_end_offset = max_height/66.6
    bar_label_vertical_alignment = 'center'
    bar_label_fontsize = 16
    if in_bar_labels:
        for i, height in enumerate(heights):
            i, height = int(i), int(height)
            ax.text(height - bar_end_offset, i, formatter(height, None),
                    fontsize=bar_label_fontsize,
                    verticalalignment=bar_label_vertical_alignment,
                    horizontalalignment='right',
                    c='white')

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
                  sort='values',
                  axis_limit=2500000,
                  formatter=money_formatter)

    return fig, ax


def init():
    if __name__ == '__main__':
        sys.exit(main())


init()
