from django.shortcuts import render
from django.http import HttpResponse
from .models import Countries, CountryPerformance, Startup, PerformanceIndex
from . import session_update as ssu
from django.db.models import Q
from copy import deepcopy
import pandas as pd
from . import notation
from .details_retrieval import startup_details
from . import defaults
from . import utils
from . import config
import numpy as np


def update_session(request):
    data_dict = request.POST.dict()
    target = data_dict['target']
    data = data_dict['data']
    if target == 'country_charts':
        ssu.update_country_charts_session(data, request)
    elif target == "indexes-order":
        ssu.update_indexes_order_session(data, request)
    elif target == "startup-filters":
        ssu.update_startup_filters_session(data, request)
    return HttpResponse('ok')


def name_indexes(idxs):
    ret = {}
    for key in idxs:
        name = [key_ for key_, val in config.TAKE_INTO_ACCOUNT.items() if val['id'] == key][0]
        ret[key] = {"name": name, "value": idxs[key], 'chosen': True}
    left = {val['id']: {"name": key, "value": 0, "chosen": False}
            for key, val in config.TAKE_INTO_ACCOUNT.items() if val['include'] and val['id'] not in idxs}
    return {**ret, **left}
    all_indexes = {val['id']: {"name": key_} for key_, val in config.TAKE_INTO_ACCOUNT.items() if val['include']}
    for idx in all_indexes:
        all_indexes[idx]['chosen'] = idx in idxs
        all_indexes[idx]['value'] = np.random.randint(0, 100)
    return all_indexes


def country_performance_colors(order):
    notes = notation.totals_from_weights(order)
    return notes


def get_startup_filter_rendering_context():
    startups = pd.DataFrame(Startup.objects.all().values())
    years_range = range(startups.creation_date.min().year, startups.creation_date.max().year + 1)
    net_result_range = [startups.reported_net_result.min(), startups.reported_net_result.max()]
    net_debt_range = [startups.reported_net_debt.min(), startups.reported_net_debt.max()]
    return {key: val for key, val in locals().items() if key != "startups"}


def index(request):
    countries = Countries.objects.all()
    if 'charts_data' in dict(request.session):
        charts_context = dict(request.session)['charts_data']
    else:
        charts_context = defaults.charts_context_defaults()
    if 'indexes_order' in dict(request.session):
        indexes_order = request.session['indexes_order']
    else:
        indexes_order = defaults.indexes_order_defaults()
    if 'startup_filters' in dict(request.session):
        startup_filters = request.session['startup_filters']
    else:
        startup_filters = defaults.startup_filter_defaults()
    colors = country_performance_colors(indexes_order)
    for el, val in colors.items():
        colors[el]['color'] = utils.color_from_rating(val['note'])

    def _process_weights(w):
        l = []
        remain = 100
        for _w in w[:-1]:
            l.append(int(remain * _w / 100))
            remain -= remain * _w / 100
        l.append(int(remain))
        return l

    indexes_order = {int(key): val for key, val in indexes_order.items()}
    indexes_order = deepcopy(indexes_order)
    indexes_order = dict(zip(indexes_order.keys(), _process_weights(list(indexes_order.values()))))
    colors = country_performance_colors(indexes_order)
    for el, val in colors.items():
        colors[el]['color'] = utils.color_from_rating(val['note'])
    c = {"codes": colors, "indexes": charts_context, "indexes_order": name_indexes(indexes_order),
         "startup_filters": startup_filters, "startup_indexes_order": defaults.startup_indexes_default(),
         "startup_filters_render": get_startup_filter_rendering_context()}
    try:
        country = request.GET['country']
    except:
        return render(request, 'registred_company/index.html', c)
    else:
        country_list = request.GET['country'].split(',')
        startups_full_view, startups = startup_details(country_list, startup_filters)
        return render(request, 'registred_company/index.html',
                      {**c, 'performance': get_country_performance(country_list,
                                                                   context=charts_context),
                       "startups": startups,
                       "startups_full_view": startups_full_view,
                       'colors': utils.spectral_colors(country_list)})


def get_context_query(context):
    ret = Q()
    for category, category_values in context.items():
        for index_el in category_values:
            if category_values[index_el]['checked']:
                q_years = utils.var_in_range_query(category_values[index_el]['range'])
                q_index = Q(performance_index__id=index_el)
                ret = ret | (q_index & q_years)
    return ret


def get_country_performance(country_list, context={}):
    query = Q()
    for country in country_list:
        query = query | Q(country__country_code=country)
    context_query = get_context_query(context)
    performance_objects = CountryPerformance.objects.filter(query & context_query)
    v = performance_objects.values("year", 'value', 'country__country_name',
                                   "performance_index__name", "performance_index__id",
                                   "country__country_code")
    df = pd.DataFrame(v).rename({"country__country_name": "country_name",
                                 "performance_index__name": "performance_index",
                                 "performance_index__id": "performance_index_id",
                                 "country__country_code": "country_code"}, axis=1)
    df = df.drop_duplicates(
        subset=['performance_index', "performance_index_id", 'country_code', 'country_name', 'year'])
    s = df.set_index(['performance_index', "performance_index_id", 'country_code', 'country_name', 'year']).unstack(
        ['country_code', 'country_name'])['value'].round(2).fillna('null')
    grouped = s.groupby(level=[0, 1])
    reagg = grouped.apply(lambda series: series.to_dict('list')).rename('value').to_frame()
    reagg = reagg.join(grouped.apply(lambda series: series.index.get_level_values(-1).to_list()).rename('year'))
    out = reagg.reset_index().to_dict('records')
    for x in out:
        x['value'] = [[*key, value] for key, value in x['value'].items()]
    return out


def get_country_codes():
    country_dict = {}
    countries = Countries.objects
    for el in countries.all():
        country_dict[el.country_code] = {"name": el.country_name}
    return country_dict
