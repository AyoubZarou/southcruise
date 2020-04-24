from matplotlib.pyplot import get_cmap
from matplotlib.colors import Normalize
import pandas as pd
import numpy as np
from django.db.models import Q
from collections import defaultdict
from copy import deepcopy

NAN_COLOR = 'rgba(0, 0, 255, 0.1)'


def color_from_rating(rating: float, cmap='Greens', nan_color=NAN_COLOR):
    """
    :param nan_color: color to use in case rating is a nan
    :param rating: a value between 0 and 1
    :param cmap: a cmap to use to generate the color
    :return: a color as an rgb string
    """
    if pd.isna(rating):
        return nan_color
    norm = Normalize(vmin=-0.5, vmax=1)
    cmap = get_cmap(cmap) if isinstance(cmap, str) else cmap
    color = cmap(norm(rating))
    value = [int(i * 255) for i in color[:3]] + [color[3]]
    return "rgb({}, {}, {}, {})".format(*value)


def spectral_colors(l):
    """
    :param l: a list to map each element to a color
    :return: a dict with each value in l is mapped to a color
    """
    values = np.linspace(0, 1, len(l))
    cmap = get_cmap('Spectral')
    co = cmap(values)
    colors = (co[:, :3] * 255).astype(int)
    mapped = [', '.join(c) for c in colors.astype(str)]
    return {country: f'rgba({mapped[i]}, {co[i, -1]})' for i, country in enumerate(l)}


def var_in_range_query(range_, var_name="year"):
    """ get an abstract query havinh the var_name in the range_
    :param range_: a range of values or a single value
    :param var_name: a var name to use for the Q django query object
    :return: a Q query object
    """
    if len(range_) == 0:
        return Q(**{var_name + '__eq': range_[0]})
    else:
        return Q(**{var_name + '__gte': range_[0]}) & Q(**{var_name + '__lte': range_[1]})


def filter_nan_out(d: dict):
    """
    :param d: a dict of values
    :return: filter any record on the dictionary if the value is nan
    """
    return dict([*filter(lambda x: not pd.isna(x[1]), [*d.items()])])


def unpivot_dict(di, key="category", inplace=True):
    if not inplace:
        di = deepcopy(di)
    d = defaultdict(dict)
    for id_, values in di.items():
        category = values.pop(key)
        d[category][id_] = values
    return dict(d)
