from django.shortcuts import render
from django.http import HttpResponse
from .models import Countries, CountryPerformance, Startup, PerformanceIndex
from .session_update import update_country_charts_session, update_indexes_order_session
from django.db.models import Q
import pandas as pd
import numpy as np
import random
from matplotlib.pyplot import get_cmap
from collections import defaultdict
from .notation import totals_from_weights
from .details_retrieval import startup_details


def random_color():
    color = random.random()
    red = int(255 * color)
    green = int(255 * (1 - color))
    return f'rgba({red}, {green}, 0, 0.5)'

def color_from_note(note):
    if np.isnan(note):
        return 'rgba(0, 0, 255, 0.1)'
    red = int(255 * (1 - note))
    green = int(255 * note)
    return f'rgba({red}, {green}, 0, 0.5)'

def update_session(request):
    data_dict = request.POST.dict()
    target = data_dict['target']
    data = data_dict['data']
    if target == 'country_charts':
        update_country_charts_session(data, request)
    elif target == "indexes-order":
        update_indexes_order_session(data, request)
    return HttpResponse('ok')


def get_colors(country_list):
    values = np.linspace(0, 1, len(country_list))
    cmap = get_cmap('Spectral')
    co = cmap(values)
    colors = (co[:, :3] * 255).astype(int)
    mapped = [', '.join(c) for c in colors.astype(str)]
    return {country: f'rgba({mapped[i]}, {co[i, -1]})' for i, country in enumerate(country_list)}

def unpivot_context(context):
    d = defaultdict(dict)
    for id_, values in context.items():
        category = values.pop('category')
        d[category][id_] = values
    return dict(d)

def get_index_order():
    return [k[0] for k in PerformanceIndex.objects.all().values_list('id')]

def name_indexes(idxs):
    all_idexes = PerformanceIndex.objects.all()
    ret = {}
    for idx in all_idexes:
        chosen = idx.id in idxs
        ret[idx.id] = {"name": idx.name, "chosen": chosen}
    return ret

def country_performance_colors(order):
    w = {}
    for i, j in enumerate(order[::-1], 1):
        w[j] = i
    notes = totals_from_weights(w)
    return notes


def get_indexes():
    indexes = PerformanceIndex.objects.all()
    c = {index_el.id: {"name": index_el.name, 'checked': True,
                          'range': [2000, 2020], 'type': random.choice(['bar', 'line']),
                          "category": index_el.category} for index_el in indexes}
    return unpivot_context(c)


def index(request):
    countries = Countries.objects.all()
    if 'charts_data' in dict(request.session):
        context = dict(request.session)['charts_data']
    else:
        context = get_indexes()
    if 'indexes_order' in dict(request.session):
        indexes_order = request.session['indexes_order']
    else:
        indexes_order = get_index_order()
    colors = country_performance_colors(indexes_order)
    for el, val in colors.items():
        colors[el]['color'] = color_from_note(val['note'])
    c = {"codes": colors, "indexes":context, "indexes_order": name_indexes(indexes_order)}
    try:
        country = request.GET['country']
    except:
        return render(request, 'index.html', c)
    else:
        country_list = request.GET['country'].split(',')
        startups_full_view, startups = startup_details(country_list)
        return render(request, 'index.html', { **c, 'performance': get_country_performance(country_list,
                                                                                     context=context),
                                              "startups": startups,
                                               "startups_full_view": startups_full_view,
                                            'colors': get_colors(country_list)})


def get_years_query(year_range):
    if len(year_range) == 1:
        return Q(year__gte=year_range[0])
    else:
        return Q(year__gte=year_range[0]) & Q(year__lte=year_range[1])


def get_context_query(context):
    ret = Q()
    for category, category_values in context.items():
        for index_el in category_values:
            if category_values[index_el]['checked']:
                q_years = get_years_query(category_values[index_el]['range'])
                q_index = Q(performance_index__id=index_el)
                ret = ret | (q_index & q_years)
    return ret


def get_country_performance(country_list, context={}):
    query = Q(country__country_code=country_list[0])
    for country in country_list[1:]:
        query = query | Q(country__country_code=country)
    context_query = get_context_query(context)
    performance_objects = CountryPerformance.objects.filter(query & context_query)
    l = []
    country_names = set()
    for ob in performance_objects:
        country_names.add(ob.country.country_name)
        d = {'year': ob.year, 'value': ob.value, "country_name": ob.country.country_name,
             "performance_index": ob.performance_index.name,
             "performance_index_id": ob.performance_index.id,
             "country_code": ob.country.country_code}
        l.append(d)
    df = pd.DataFrame.from_records(l)
    aggregated = df.groupby(['performance_index', 'country_code']).agg({"country_name": 'first',
                                                                        'year': lambda x: x.to_list(),
                                                                        'value': lambda x: x.to_list()})
    df = df.drop_duplicates(subset=['performance_index', "performance_index_id", 'country_code', 'country_name', 'year'])
    s = df.set_index(['performance_index', "performance_index_id", 'country_code', 'country_name', 'year']).unstack(
        ['country_code', 'country_name'])['value'].round(2).fillna('null')
    grouped = s.groupby(level=[0, 1])
    reagg = grouped.apply(lambda series: series.to_dict('list')).rename('value').to_frame()
    reagg = reagg.join(grouped.apply(lambda series: series.index.get_level_values(-1).to_list()).rename('year'))
    out = reagg.reset_index().to_dict('records')
    for x in out:
        x['value'] = [[*key, value] for key, value in x['value'].items()]
    return out


# def startup_details(country_list):
#     ret = {}
#     query = Q(country__country_code=country_list[0])
#     for country in country_list[1:]:
#         query = query | Q(country__country_code=country)
#     startup_objects = Startup.objects.filter(query)
#     fields = ['country__country_name', 'country__country_code', 'name', 'reported_net_result', 'creation_date',
#               'number_of_employees', 'website']
#     startups_df = pd.DataFrame(startup_objects.values(*fields))
#     startups_dict = startups_df.to_dict('records')
#     return [*map(filter_nan_out, startups_dict), ]

def filter_nan_out(d: dict):
    return dict([*filter(lambda x: not pd.isna(x[1]), [*d.items()])])


def get_country_codes():
    country_dict = {}
    countries = Countries.objects
    for el in countries.all():
        country_dict[el.country_code] = {"name": el.country_name}
    return country_dict
