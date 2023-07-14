import math
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import (
    ListedColormap,
    get_named_colors_mapping
)
import numpy as np
from idealforms.formatters import Formatter, money_formatter, default_formatter
from typing import Dict, List, Tuple, Optional, Iterable


DataDict = Dict[str, float]



def pie(data: DataDict,
        title: str,
        reverse_color_order: bool = False,
        reverse_only_non_largest_colors_order: bool = False,
        largest_color = 'xkcd:dusty red',
        cmap_name: str = "Greys",
        in_bar_labels: bool = True,
        short_bar_label: str = 'out',
        figsize: Tuple[float, float] = (8, 8),
        formatter: Optional[Formatter] = None,
        **kwargs) -> Tuple[plt.Figure, plt.Axes]:
    """
    Plot a nice pie chart
    data: DataDict, dictionary with data to plot, key: label v: value
    title: str, title for chart
    sort_on: str = 'values' or 'alpha' sort by values or label names
    cmap_name: str = "Reds" matplot lib color map name to color bars
    in_bar_labels: bool = True, plot value in pie section, False: value outside pie section
    short_bar_label: str = 'out', 'skip' if in label is too big for for section, plot outside, skip: don't plot
    figsize: Tuple[float, float] = (8, 4), overall fig size to plot
    formatter: Optional[Formatter] = None, idealforms.formatter class to use formatting data labels
    :return: Tuple[plt.Figure, plt.Axes]:
    """
    
    if not formatter:
        formatter = default_formatter

    # sort dict big to small
    data = dict(sorted(data.items(),
                       key=lambda kv: kv[1],
                       reverse=True))  # type: ignore
    original_sum = sum(data.values())

    # only show 4 values max, remainder = others
    data = {k: v for i, (k, v) in enumerate(data.items()) if i < 3}
    data['others'] = original_sum - (sum(data.values()))

    # convert to percent
    data = {k: round(v/original_sum*100, 2) for k, v in data.items()}

    # split data dict into lists for plotting
    categories: List[str] = list(data.keys())
    portions: List[float] = list(data.values())

    # get params from data
    max_portion: float = max(portions)
    data_color_normalized = [value/max_portion for value in portions]
    if reverse_color_order:
        data_color_normalized = data_color_normalized[::-1]

    # pyplot global params
    plt.rcParams.update({'figure.autolayout': True})
    plt.style.use('ggplot')

    # create figure and axes objects plus color mapping
    fig, ax = plt.subplots(1, 1, figsize=(max(figsize), max(figsize)))
    renderer = fig.canvas.get_renderer()

    my_cmap = plt.cm.get_cmap(cmap_name)
    my_cmap = my_cmap(np.linspace(0, 1, int(3*len(portions))))  # limit color range to darker colors
    my_cmap = ListedColormap(my_cmap[len(portions):, :-1])
    colors = my_cmap(data_color_normalized)

    # set largest portion to be contrast color here. largest_color
    colors[0] = convert_hex_to_rgb(
        get_named_colors_mapping()[largest_color]
    )
    if reverse_color_order:
        colors = colors[::-1]
    elif reverse_only_non_largest_colors_order:
        colors[1:] = colors[1:][::-1]

    # set labels to be name and % on new line
    labels = [category+'\n'+str(portion)+' %' for category, portion in data.items()]

    # plotting
    patches, texts = ax.pie(
        portions, 
        labels=labels, 
        labeldistance=0.5,
        colors=colors,
        # counterclock=False,
        startangle=90,
        **kwargs
    )
    
    ax.set_title(title)
    # ax.legend()
    #     patches,
    #     texts,
    #     bbox_to_anchor=(1, 0.5),
    #     loc="center right",
    #     fontsize=8,
    #     bbox_transform=plt.gcf().transFigure
    # )
    # plt.subplots_adjust(left=0.0, bottom=0.1, right=0.8)
    return fig, ax



def convert_hex_to_rgb(hex_color: str) -> List[float]:
    r, g, b = [int(d1 + d2, 16)/255 for d1, d2 in pairwise(hex_color[1:])]
    a = 1.0
    return [r, g, b, a]


def pairwise(i: Iterable):
    "s -> (s0, s1), (s2, s3), ..., (sn-1, sn)"
    a = iter(i)
    return zip(a, a)
