from django.shortcuts import render
from django.http import HttpResponse

from .models import Countries, CountryPerformance, Startup, StartupSector, PerformanceIndex
from . import session_update as ssu
from django.db.models import Q
import pandas as pd
from . import (notation, defaults, utils, config)
from .details_retrieval import startup_details, registered_company_details


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
    elif target == "startup-indexes-order":
        ssu.update_startup_indexes_order_session(data, request)
    elif target == "target-view":
        ssu.update_target_view(data, request)
    return HttpResponse('ok')


def get_startup_filter_rendering_context():
    # get global data about startups used to set up the filters template
    startups = pd.DataFrame(Startup.objects.all().values())
    years_range = range(startups.creation_date.min().year, startups.creation_date.max().year + 1)
    net_result_range = [startups.reported_net_result.min(), startups.reported_net_result.max()]
    net_debt_range = [startups.reported_net_debt.min(), startups.reported_net_debt.max()]
    unique_sectors = StartupSector.objects.all().values('sector')
    sectors = pd.DataFrame(unique_sectors).sector.unique().tolist()
    return {key: val for key, val in locals().items() if key not in ["startups", 'unique_sectors']}


def _render_startup_view(request):
    c = _load_session(request)
    c['target_view'] = "startup"
    try:
        country = request.GET['country']
    except:
        return render(request, 'index.html', c)
    else:
        country_list = request.GET['country'].split(',')

        startups_full_view, startups = startup_details(country_list, c['startup_filters'],
                                                       weights=c['startup_indexes_weights'],
                                                       context={"countries_notes": {key: val['note'] for key,
                                                                                                         val in
                                                                                    c['codes'].items()}})
        return render(request, 'index.html',
                      {**c,
                       "startups": startups,
                       "startups_full_view": startups_full_view})


def _render_registered_company_view(request):
    context = _load_country_session(request)
    context['target_view'] = "registered_company"
    try:
        country = request.GET['country']
    except:
        return render(request, 'index.html', context)
    else:
        country_list = request.GET['country'].split(',')
    companies, companies_dataset = registered_company_details(country_list)
    context.update({"companies": companies, "companies_dataset": companies_dataset})
    return render(request, 'registred_company/index.html', context)


def index(request):
    target = dict(request.session).get('target_view', 'startup')
    if target == "startup":
        return _render_startup_view(request)
    else:
        return _render_registered_company_view(request)


def get_country_context_query(context):
    """ get a query used to filter out the non-needed coutry performance data"""
    ret = Q()
    for category, category_values in context.items():
        for index_el in category_values:
            if category_values[index_el]['checked']:
                q_years = utils.var_in_range_query(category_values[index_el]['range'])
                q_index = Q(performance_index__id=index_el)
                ret = ret | (q_index & q_years)
    return ret


def get_country_performance(country_list: list, context: dict = {}):
    """
    :param country_list: List of country codes used to retrieve the data for these countries
    :param context: context used to filter the data (if an indicator is not to be sent, or to be sent on a
    limited range)
    :return: a dictionary containing the data
    """
    query = Q()
    for country in country_list:
        query = query | Q(country__country_code=country)
    context_query = get_country_context_query(context)
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
    data = grouped.apply(lambda series: series.to_dict('list')).rename('value').to_frame()
    # join with the year data (the get_level_values(-1) allows to get the year data as a list)
    data = data.join(grouped.apply(lambda series: series.index.get_level_values(-1).to_list()).rename('year'))
    out = data.reset_index().to_dict('records')
    for x in out:
        # include the country name and country code on the value data (as the first two level data of the index)
        x['value'] = [[*key, value] for key, value in x['value'].items()]
    return out


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


def _load_country_session(request):
    if 'charts_data' in dict(request.session):
        charts_context = dict(request.session)['charts_data']
    else:
        charts_context = defaults.charts_context_defaults()
    if 'indexes_order' in dict(request.session):
        indexes_order = request.session['indexes_order']
    else:
        indexes_order = defaults.country_indexes_weights_defaults()
    indexes_order = _process_weights(indexes_order)
    colors = notation.country_notation(indexes_order)
    for el, val in colors.items():
        colors[el]['color'] = utils.color_from_rating(val['note'])
    context = {"codes": colors,
               "indexes": charts_context,
               "indexes_order": _name_indexes(indexes_order)}
    try:
        country = request.GET['country']
    except:
        return context
    else:
        country_list = request.GET['country'].split(',')
        return {**context,
                'performance': get_country_performance(country_list, context=charts_context),
                'colors': utils.spectral_colors(country_list)}


def _load_session(request):
    _country_session = _load_country_session(request)
    if 'startup_filters' in dict(request.session):
        startup_filters = request.session['startup_filters']
    else:
        startup_filters = defaults.startup_filter_defaults()
    if 'startup_indexes_order' in dict(request.session):
        startup_indexes_order = request.session['startup_indexes_order']
        startup_indexes_order = _process_weights(startup_indexes_order)
    else:
        startup_indexes_order = defaults.startup_indexes_weights_default()

    return {"startup_filters": startup_filters,
            "startup_indexes_order": _name_startup_indexes(startup_indexes_order),
            "startup_filters_render": get_startup_filter_rendering_context(),
            "startup_indexes_weights": _startup_weights_from_order(startup_indexes_order),
            **_country_session}


def _name_indexes(idxs):
    ret = {}
    ref = config.TAKE_INTO_ACCOUNT
    pes = PerformanceIndex.objects
    for idx, include in ref.items():
        id = pes.get(name=idx).id
        in_idxs = id in idxs
        if in_idxs and include:
            ret[id] = {"name": idx, "value": idxs[id], 'chosen': True}
        elif include:
            ret[id] = {"name": idx, "value": 0, 'chosen': False}
    return {**{key: ret[key] for key in idxs}, **{key: ret[key] for key in ret if key not in idxs}}


def _name_startup_indexes(idxs):
    idxs = {int(key): val for key, val in idxs.items()}
    ref = config.DEFAULT_STARTUP_FILTERS
    chosen = {key: {"chosen": True, "name": ref[key]['name'], 'alt': ref[key]["alt"], 'chosen': True,
                    "value": val} for key, val in idxs.items()}
    non_chosen = {key: val for key, val in ref.items() if key not in idxs}
    for v in non_chosen.values():
        v['chosen'] = False
    return {**chosen, **non_chosen}


def _startup_weights_from_order(order):
    ref = config.DEFAULT_STARTUP_FILTERS
    # alt contains an alternative name for the index (valid python variable name)
    return {ref[key]['alt']: w for key, w in order.items()}
