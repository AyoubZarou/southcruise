from startup.models import Countries, CountryPerformance, PerformanceIndex, Startup, StartupPerformance
from collections.abc import Iterable
from collections import defaultdict
import pandas as pd
import numpy as np
from django.db.models import Q
import datetime
from .js_scripts import DATA_FIELDS_MAPPER
from copy import deepcopy
import datetime


def filter_and_format(d: dict, fill=''):
    """format values of a dict, fill empty values with `fill` variable and format datetime objects
    :param d: a dictionary containing values a key: value mapping of soe fields
    :param fill: the value to use to format empty values
    :return: a formated dict
    """
    to_return = {}
    for k, v in d.items():
        if isinstance(v, datetime.datetime):
            to_return[k] = v.strftime("%m - %Y")
        elif not (isinstance(v, Iterable) and len(v)) and pd.isna(v):
            to_return[k] = fill
        else:
            to_return[k] = v
    return to_return


def select_fields(model_object, l):
    """ Select filed of an object from a model using django convention
     "object__object_name" is equivalent to retirieve model_object.object.object_name
    :param model_object:
    :param l: list of fields to retrieve
    :return:
    """
    to_ret = {}
    for name in l:
        k = name.split('__')
        o = model_object
        for part in k:
            o = getattr(o, part)
        to_ret[name] = o
    return to_ret


def create_frappe_dataset(d, fields_to_include, mapping_values=DATA_FIELDS_MAPPER):
    """ create dataset for frappe (https://frappe.io/datatable) from records d,
    while using fileds to include and mapping_values to format the fields
    :param d: records object
    :param fields_to_include: the fields to include when retrieving the data
    :param mapping_values: a mapping object, used to format the fields in a table (example: renaming the field name,
    adding  a forlat function ..)
    :return: a dataset used by frappe.js to create a table
    """
    mapping_values = deepcopy(mapping_values)
    columns = []
    concat_mapping = defaultdict(list)
    general_config = {'editable': False, 'resizable': True,
                      'sortable': False, 'focusable': True}
    for col in fields_to_include:
        if mapping_values is None or mapping_values[col] == {}:
            columns.append({"name": col, **general_config})
        else:
            mapped_value = mapping_values[col]
            if 'add_field' in mapped_value:
                a = mapped_value.pop('add_field')
                mapped_value.update(general_config)
                concat_mapping[col] = deepcopy(a)
            columns.append(mapped_value)
    data = []
    for value in d:
        sub_data = []
        for field in fields_to_include:
            concat_with = concat_mapping[field]
            to_append = []
            for v in [field] + concat_with:
                to_append.append(str(value[v]))

            sub_data.append("|".join(to_append))
        data.append(sub_data)
    return {"columns": columns, "data": data}


def get_startup_data(record):
    """
    :param record:  a startup object
    :return: a dict with data about the startup, normalized
    """
    capital = record.capital
    if record.creation_date is not None:
        years_since_creation = datetime.datetime.now().year - record.creation_date.year
    else:
        years_since_creation = np.nan
    nb_investors = len(record.investors.split('/'))
    nb_awards = len(record.awards.split('/'))
    impact = record.impact + 0
    innovation = record.innovation + 0
    nb_partnerships = len(record.partnerships.split('/'))
    nb_founders = len(record.founder.split('/'))
    maturity = record.maturity
    result = record.reported_net_result
    debt = record.reported_net_debt
    growth_rate = record.growth_rate
    nb_employees = record.number_of_employees
    capital = record.capital
    founders_mean_age = record.founders_mean_age
    founders_mean_education_level = record.founders_mean_education_level
    try:
        customers = int(record.customers)
    except:
        customers = np.nan
    structure = record.structure
    v = {key: val for key, val in locals().items() if key != "record"}
    startup_performance = record.startupperformance_set
    fund_raising_set = startup_performance.filter(Q(index="func_raising"))
    v['nb_fund_raising_years'] = len(fund_raising_set)
    v['fund_raising_value'] = sum([r.value for r in fund_raising_set])
    return v


def aggregate_data_into_mark_(data):
    d = {'impact': data['impact'] + 0,
         "innovation": data['innovation'] + 0,
         "investors": min(data['nb_investors'] * 0.2, 1),
         "founders": min(data['nb_founders'] * 0.2, 1),
         "years_since_creation": (min(data['years_since_creation'] * 0.2, 1) if data['years_since_creation'] else 0),
         "maturity": {"Mature": 1, "Amorçage": 0, "Croissance": 0.3, "Développement": 0.6, '': 0}.get(data['maturity']),
         "growth_rate": min(data['growth_rate'] * 1.5, 1),
         "capital": min(1, data['capital'] / 2_000_000),
         "net_result": min(1, data['reported_net_result'] / 1_000_000),
         "net_debt": max(-1, data['reported_net_debt'] / 1_000_000),
         }


def note_from_data_and_weights(data, weights):
    s = sum(weights.values())
    weights = {key: val / s for key, val in weights.items()}
    mark = sum([weights[key] * data[key] for key in weights])
    return mark


def aggregate_data_into_mark(data, weights=None):
    if weights is not None:
        return note_from_data_and_weights(data, weights)
    IMPACT_BONUS = 1
    INNOVATON_BONUS = 1
    PER_INVESTOR = 2
    PER_FOUNDER = 1
    PER_EXISTING_YEAR = 1.5
    MATURITY = lambda x: {"Mature": 3, "Amorçage": 0, "Croissance": 1, "Développement": 2, '': 0}.get(x) if x else 0
    GROWTH_RATE = lambda x: 2 * x / 0.1 if x else 0
    final_mark = 0
    final_mark += IMPACT_BONUS if data['impact'] else 0
    final_mark += INNOVATON_BONUS if data['innovation'] else 0
    final_mark = data['nb_investors'] * PER_INVESTOR
    final_mark += data['nb_founders'] * PER_FOUNDER
    final_mark += (data['years_since_creation'] * PER_EXISTING_YEAR if data['years_since_creation']
                   else PER_EXISTING_YEAR * 0.5)
    final_mark += MATURITY(data['maturity'])
    final_mark += GROWTH_RATE(data['growth_rate'])
    return final_mark


def startup_filter_query(filter_object):
    """
    :param filter_object: a dict containing filters to apply to the startups,
    :return:
    """

    def exists_and_true(key):
        return key in filter_object and filter_object[key]

    if filter_object is None:
        return Q()
    q = Q()
    for key in ['is_impact', 'is_innovation']:
        if exists_and_true(key):
            q = q & Q(**{key.split('_')[1]: True})
    if exists_and_true('is_awarded'):
        q = q & (~Q(awards=""))
    if "years_since_foundation" in filter_object:
        years = int(filter_object['years_since_foundation'])
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=years * 365)
        q = q & Q(creation_date__lte=now - delta)
    return q


def startup_details(country_list, filter_object=None, weights=None):
    if filter_object is None:
        filter_object = defaultdict(lambda: None)
    ret = {}
    query = Q()
    for country in country_list:
        query = query | Q(country__country_code=country)
    query = query & startup_filter_query(filter_object)
    startup_objects = list(Startup.objects.filter(query))
    if "already_raised_funds" in filter_object and filter_object["already_raised_funds"]:
        def ff(ob):
            """filter function used to filter the data"""
            return len(ob.startupperformance_set.filter(index="func_raising")) > 0

        startup_objects = [*filter(ff, startup_objects)]
    raw_fields = ['name', 'capital', 'creation_date', 'number_of_employees', 'maturity', 'founder', 'customers',
                  'operationals', 'market_potential', 'investors', 'partnerships', 'innovation', 'impact', 'awards',
                  'growth_rate', 'reported_net_result', 'reported_net_debt', 'website', 'presentation',
                  'country__country_name',
                  'country__country_code', 'id']
    startups = []
    for startup in startup_objects:
        d = select_fields(startup, raw_fields)
        performance_set = pd.DataFrame(startup.startupperformance_set.all().values())
        if performance_set.size != 0:
            d['performance'] = (performance_set.groupby('index')
                                .agg({"year": list, "value": list}).to_dict(orient='index'))
        d['activity_countries'] = [k['country'] for k in startup.startupactivitycountry_set.all().values('country')]
        d['sectors'] = [k['sector'] for k in startup.startupsector_set.all().values('sector')]
        d['note'] = aggregate_data_into_mark(get_startup_data(startup), weights=None)
        startups.append(filter_and_format(d))
    startups = sorted(startups, key=lambda x: x['note'], reverse=True)
    fields_to_display = ['name', 'country__country_name', 'maturity', 'sectors', 'note']
    return startups, create_frappe_dataset(startups, fields_to_display)
