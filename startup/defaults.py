from startup.models import PerformanceIndex, StartupSector
from . import utils
from .config import TAKE_INTO_ACCOUNT
import pandas as pd


def startup_filter_defaults():
    filters = {"is_impact": False, "is_innovation": False, "is_awarded": False,
            "already_raised_funds": False}
    unique_sectors = pd.DataFrame(StartupSector.objects.all().values('sector')).sector.unique()
    filters['sectors'] = {value: True for value in unique_sectors}
    filters['creation_years_range'] = {"start": {str(year): False for year in range(2010, 2021)},
                        "end": {str(year): False for year in range(2010, 2021)}}
    return filters


def charts_context_defaults():
    indexes = PerformanceIndex.objects.all()
    c = {index_el.id: {"name": index_el.name, 'checked': True,
                       'range': [2010, 2020], 'type': "bar",
                       "category": index_el.category} for index_el in indexes}
    return utils.unpivot_dict(c)


def indexes_order_defaults():
    return {val["id"]: 10 for _, val in TAKE_INTO_ACCOUNT.items() if val['include']}


DEFAULT_STARTUP_FILTERS = {
    1: {"name": "impact", 'chosen': False, "value": 100, "alt": "impact"},
    2: {"name": "innovation", 'chosen': False, "value": 100, 'alt': 'innovation'},
    3: {"name": "awards", "chosen": False, 'value': 100, "alt": "awards"},
    4: {"name": "capital", "chosen": True, "value": 100, "alt": 'capital'},
    5: {"name": "number of employees", "chosen": False, 'value': 20, 'alt': 'number_of_employees'},
    6: {"name": "debt", "chosen": False, "value": 20, 'alt': 'net_debt'},
    7: {"name": 'net result', 'chosen': True, "value": 10, 'alt': 'net_result'},
    8: {"name": "number of founders", 'chosen': True, "value": 20, 'alt': 'founders'},
    9: {"name": "investors", 'chosen': True, "value": 20, 'alt': 'investors'},
    10: {"name": "years since creation", 'chosen': False, "value": 20, 'alt': 'years_since_creation'},
    11: {"name": 'Country performance', 'chosen': True, "value": 100, 'alt': 'country_performance'}
}


def startup_indexes_default():
    return {id_: 10 for id_, val in DEFAULT_STARTUP_FILTERS.items() if val['chosen']}
