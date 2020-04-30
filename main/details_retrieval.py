import datetime
from collections import defaultdict
from collections.abc import Iterable
from copy import deepcopy
import django

import numpy as np
import pandas as pd
from django.db.models import Q

from .js_scripts import DATA_FIELDS_MAPPER
from .models import (Startup,
                     RegisteredCompany, RegisteredCompanyPerformance)
from typing import List, Tuple


def filter_and_format(d: dict, fill: str = ''):
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


def select_fields(model_object: django.db.models.Model, l: List[str]):
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


def create_frappe_dataset(d: dict, fields_to_include: List[str], mapping_values: dict = DATA_FIELDS_MAPPER):
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


def get_startup_data(record: Startup):
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
    country_code = record.country.country_code
    try:
        customers = int(record.customers)
    except:
        customers = np.nan
    structure = record.structure
    v = {key: val for key, val in locals().items() if key != "record"}
    startup_performance = record.startupperformance_set
    fund_raising_set = startup_performance.filter(Q(index="fund_raising"))
    v['nb_fund_raising_years'] = len(fund_raising_set)
    v['fund_raising_value'] = sum([r.value for r in fund_raising_set])
    return v


def _exp_law(x, lambda_=1):
    return 1 - np.exp(-1 / lambda_ * x)


def aggregate_data_into_mark(data: dict, weights: dict, context: dict) -> int:
    # normalize the data into the [0, 1] interval
    d = {'impact': data['impact'] + 0,
         "innovation": data['innovation'] + 0,
         "investors": min(data['nb_investors'] * 0.2, 1),
         "founders": min(data['nb_founders'] * 0.2, 1),
         "years_since_creation": (_exp_law(data['years_since_creation'], 4) if data['years_since_creation'] else 0),
         "maturity": {"Mature": 1, "Amorçage": 0, "Croissance": 0.3, "Développement": 0.6}.get(data['maturity'], 0),
         "growth_rate": _exp_law(data['growth_rate'], 0.5) if data['growth_rate'] else 0,
         "capital": _exp_law(data['capital'], 2_000_000) if data['capital'] else 0,
         "net_result": _exp_law(data['result'], 1_000_000) if data['result'] else 0,
         "net_debt": 1 - _exp_law(data['debt'], 1_000_000) if data['debt'] else 0,
         "awards": _exp_law(data['nb_awards'], 5),
         "number_of_employees": _exp_law(data['nb_employees'], 100) if data['nb_employees'] else 0,
         "customers": _exp_law(data['customers'], 10000) if data['customers'] else 0,
         "nb_partnerships": _exp_law(data['nb_partnerships'], 4) if data['nb_partnerships'] else 0,
         "country_performance": context['countries_notes'][data['country_code']],
         "nb_fund_raising_years": _exp_law(data['nb_fund_raising_years'], 3) if data['nb_fund_raising_years'] else 0,
         "fund_raising_value": _exp_law(data['fund_raising_value'], 1_000_000) if data['fund_raising_value'] else 0,
         "founders_mean_age_ob": _exp_law(data["founders_mean_age"], 40) if data['founders_mean_age']
         else _exp_law(20, 40),
         "founders_mean_age_yb": 1 - _exp_law(data["founders_mean_age"], 20) if data['founders_mean_age']
         else 1 - _exp_law(40, 20),
         }
    mark = sum([d[key] * val for key, val in weights.items() if key in d])
    return int(mark)


def startup_filter_query(filter_object: dict) -> Q:
    """
    :param filter_object: a dict containing filters to apply to the startups,
    :return: Q object with partial startup filter, that is used on the startup table to filter startups, the only part
    not taken into account by this filter is the startup yearly performance (fund raising for example) and sectors,
    these are being taken care of later
    """

    def exists_and_true(key: str) -> bool:
        # check if a key is present in the filter object and if its value is True
        return key in filter_object and filter_object[key]

    if filter_object is None:
        return Q()
    q = Q()
    for key in ['is_impact', 'is_innovation']:
        if exists_and_true(key):
            q = q & Q(**{key.split('_')[1]: True})
    if exists_and_true('is_awarded'):
        q = q & (~Q(awards=""))

    if 'creation_years_range' in filter_object:
        start = [key for key, val in filter_object['creation_years_range']['start'].items() if val]
        start = start[0] if len(start) else ''
        end = [key for key, val in filter_object['creation_years_range']['end'].items() if val]
        end = end[0] if len(end) else ''
        if start != '':
            start = datetime.datetime(year=int(start), day=1, month=1)
            q = q & Q(creation_date__gte=start)
        if end != '':
            end = datetime.datetime(year=int(end), day=1, month=1)
            q = q & Q(creation_date__lte=end)
    return q


def startup_details(country_list: List[str], filter_object: dict = None,
                    weights: dict = None, context: dict = None) -> Tuple[dict, dict]:
    """
    :param country_list: list of countries to take into account
    :param filter_object: a filter dict (see startup filter default in defaults)
    :param weights: weights for each startup field, used to aggregate a mark per startup
    :param context: the context is a dict containing context values, as mark per country to be used for startups
    :return:a list of startup details and Frappe dataset
    """
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
            return len(ob.startupperformance_set.filter(index="fund_raising")) > 0

        startup_objects = [*filter(ff, startup_objects)]
    if 'sectors' in filter_object:
        selected_sectors = [sector for sector, value in filter_object['sectors'].items() if value]

        # filter function
        def ff(ob):
            sectors = [record['sector'] for record in ob.startupsector_set.all().values('sector')]
            isin = [sector in selected_sectors for sector in sectors]
            return sum(isin) > 0

        startup_objects = [*filter(ff, startup_objects)]

    # selected fields for each startup
    raw_fields = ['name', 'capital', 'creation_date', 'number_of_employees', 'maturity', 'founder', 'customers',
                  'operationals', 'market_potential', 'investors', 'partnerships', 'innovation', 'impact', 'awards',
                  'growth_rate', 'reported_net_result', 'reported_net_debt', 'website', 'presentation',
                  'country__country_name', 'country__country_code', 'id', 'investment_need', 'founders_mean_age',
                  'founders_mean_education_level']
    startups = []
    for startup in startup_objects:
        d = select_fields(startup, raw_fields)
        performance_set = pd.DataFrame(startup.startupperformance_set.all().values())
        if performance_set.size != 0:
            d['performance'] = (performance_set.groupby('index')
                                .agg({"year": list, "value": list}).to_dict(orient='index'))
        d['activity_countries'] = [k['country'] for k in startup.startupactivitycountry_set.all().values('country')]
        d['sectors'] = [k['sector'] for k in startup.startupsector_set.all().values('sector')]
        d['note'] = aggregate_data_into_mark(get_startup_data(startup), weights=weights, context=context)
        startups.append(filter_and_format(d))
    startups = sorted(startups, key=lambda x: x['note'], reverse=True)
    fields_to_display = ['name', 'country__country_name', 'maturity', 'sectors', 'capital', 'note']
    return startups, create_frappe_dataset(startups, fields_to_display)


def _process_weights(d):
    # used to calculate real weights from ordered weights (see the guide)
    w = list(d.values())
    new_weights = []
    remain = 100
    for _w in w[:-1]:
        new_weights.append(int(remain * _w / 100))
        remain -= remain * _w / 100
    new_weights.append(int(remain))
    return dict(zip(d.keys(), new_weights))


def registered_company_details(country_list: List[str], filter_object: dict = None,
                               weights: dict = None, context: dict = None):
    query = Q()
    weights = _process_weights({w['name']: w['value'] for w in weights.values()})
    details = get_registered_company_table()
    details =(details - details.min(axis=0)) / (details.max(axis=0) - details.min(axis=0))
    for country in country_list:
        query = query | Q(country__country_code=country)
    companies_list = list(RegisteredCompany.objects.filter(query))
    companies = []
    fields_to_select = ['security', 'gics_sector', 'country__country_name', 'country__country_code', 'id']
    for company in companies_list:
        selected_fields = select_fields(company, fields_to_select)
        note = round((pd.Series(weights) * details.loc[selected_fields['id']].iloc[0, :]).sum())
        performance_set = RegisteredCompanyPerformance.objects.filter(company_id=company.id).values()
        performance_set = {val['index']: round(val['value'], 2) for val in performance_set}
        companies.append({**selected_fields, **performance_set, 'note': note})
    companies = sorted(companies, key=lambda x: x['note'], reverse=True)
    fields_to_display = ['security', 'gics_sector', 'country__country_name', 'Company Market Cap (USD)', 'note']
    return companies, create_frappe_dataset(companies, fields_to_display)


def get_registered_company_table() -> pd.DataFrame:
    """
    Get a pivoted table summarizing registred companies data
    """
    details = (pd.DataFrame(RegisteredCompanyPerformance.objects.all()
                            .values('index', 'value', 'company__gics_sector', 'company__id',
                                    'company__trbc_sector', 'company__security', 'company__country__country_code')))
    details.columns = [col.split('__')[-1] for col in details.columns]
    return pd.pivot_table(details, values=['value'], index=['id', 'security', 'gics_sector', 'trbc_sector'],
                          columns=['index'])['value']

