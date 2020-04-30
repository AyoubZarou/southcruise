from .models import PerformanceIndex, StartupSector, OrderOpinion

from .config import DEFAULT_STARTUP_FILTERS
from . import utils
from .config import TAKE_INTO_ACCOUNT
import pandas as pd
import json
import numpy as np


def startup_filter_defaults() -> dict:
    """ get default filter for startup for new sessions
    :return: dict
    """
    filters = {"is_impact": False, "is_innovation": False, "is_awarded": False,
               "already_raised_funds": False}
    unique_sectors = pd.DataFrame(StartupSector.objects.all().values('sector')).sector.unique()
    filters['sectors'] = {value: True for value in unique_sectors}
    filters['creation_years_range'] = {"start": {str(year): False for year in range(2010, 2021)},
                                       "end": {str(year): False for year in range(2010, 2021)}}
    return filters


def charts_context_defaults() -> dict:
    """ get charts defaults, get the charts to include and the range of time to display
    """
    indexes = PerformanceIndex.objects.all()
    c = {index_el.id: {"name": index_el.name, 'checked': True,
                       'range': [2010, 2020], 'type': "bar",
                       "category": index_el.category} for index_el in indexes}
    return utils.unpivot_dict(c)


def _process_weights(d):
    # used to calculate real weights from ordered weights (see the guide)
    w = list(d.values())
    new_weights = []
    remain = 100
    for _w in w[:-1]:
        new_weights.append(int(remain * _w / 100))
        remain -= remain * _w / 100
    new_weights.append(int(remain))
    return dict(zip(map(int, d.keys()), new_weights))


def country_indexes_weights_defaults() -> dict:
    # average all the cached data
    pi_objects = PerformanceIndex.objects
    all_ids = [pi_objects.get(name=key).id for key, val in TAKE_INTO_ACCOUNT.items() if val]
    all_orders = OrderOpinion.objects.all().values('order')
    all_orders = [json.loads(order['order']) for order in all_orders]
    all_orders = [_process_weights(dict(zip(d['ids'], d['values']))) for d in all_orders]
    ret = {}
    for key in all_ids:
        v = np.mean([o.get(key, 0) for o in all_orders])
        if v != 0:
            ret[key] = v
    return ret


def startup_indexes_weights_default():
    return {id_: 10 for id_, val in DEFAULT_STARTUP_FILTERS.items() if val['chosen']}


def registered_company_filter_defaults():
    pass
