from startup.models import Countries, CountryPerformance, PerformanceIndex, Startup, StartupPerformance
from collections.abc import Iterable
from collections import defaultdict
import pandas as pd
from django.db.models import Q
import datetime
from .js_scripts import DATA_FIELDS_MAPPER
from copy import deepcopy

def filter_and_format(d: dict, fill=''):
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
    to_ret = {}
    for name in l:
        k = name.split('__')
        o = model_object
        for part in k:
            o = getattr(o, part)
        to_ret[name] = o
    return to_ret


# create dataset for frappe (https://frappe.io/datatable) from records

def create_frappe_dataset(d, fields_to_include, mapping_values=DATA_FIELDS_MAPPER):
    mapping_values = deepcopy(mapping_values)
    columns = []
    concat_mapping = defaultdict(list)
    general_config = {'editable': False, 'resizable': True,
            'sortable': False, 'focusable': True}
    for col in fields_to_include:
        if mapping_values is None or  mapping_values[col] is None:
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


def startup_details(country_list):
    ret = {}
    query = Q(country__country_code=country_list[0])
    for country in country_list[1:]:
        query = query | Q(country__country_code=country)
    startup_objects = Startup.objects.filter(query)

    raw_fields = ['name', 'capital', 'creation_date', 'number_of_employees', 'maturity', 'founder', 'customers',
         'operationals', 'market_potential', 'investors', 'partnerships', 'innovation', 'impact', 'awards',
         'growth_rate', 'reported_net_result', 'reported_net_debt', 'website', 'presentation', 'country__country_name',
         'country__country_code', 'id']
    startups = []
    for startup in startup_objects:
        d = select_fields(startup, raw_fields)
        performance_set = pd.DataFrame(startup.startupperformance_set.all().values())
        if performance_set.size != 0:
            d['performance'] =(performance_set.groupby('index')
                               .agg({"year": list, "value": list}).to_dict(orient='index'))
        d['activity_countries'] = [k['country'] for k in startup.startupactivitycountry_set.all().values('country')]
        d['sectors'] = [k['sector'] for k in startup.startupsector_set.all().values('sector')]
        startups.append(filter_and_format(d))
    fields_to_display = ['name', 'country__country_name', 'maturity', 'sectors']
    return startups, create_frappe_dataset(startups, fields_to_display)