from main.models import PerformanceIndex, StartupSector

from .config import DEFAULT_STARTUP_FILTERS
from . import utils
from .config import TAKE_INTO_ACCOUNT
import pandas as pd


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


def country_indexes_weights_defaults() -> dict:
    pi_objects = PerformanceIndex.objects
    return {pi_objects.get(name=key).id: 10 for key, val in TAKE_INTO_ACCOUNT.items() if val}


def startup_indexes_weights_default():
    return {id_: 10 for id_, val in DEFAULT_STARTUP_FILTERS.items() if val['chosen']}
