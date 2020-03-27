from django.shortcuts import render
from django.http import HttpResponse
from .models import Countries, CountryPerformance, Startup
from django.db.models import Q
import pandas as pd
import random


def random_color():
    color = random.random()
    red = int(255 * color)
    green = int(255 * (1 - color))
    return f'rgba({red}, {green}, 0, 0.5)'


def get_colors(country_list):
    return {country: random_color() for country in country_list}


def index(request):
    countries = Countries.objects.all()
    d = {}
    for el in countries:
        d[el.country_code] = {'name': el.country_name, 'color': random_color()}
    try:
        country = request.GET['country']
    except:
        return render(request, 'index.html', {"codes": d})
    else:
        country_list = request.GET['country'].split(',')
        return render(request, 'index.html', {"codes": d, 'performance': get_country_performance(country_list),
                                              "startups": startup_details(country_list), 'colors':
                                                  get_colors(country_list)})


def get_country_performance(country_list):
    query = Q(country__country_code=country_list[0])
    for country in country_list[1:]:
        query = query | Q(country__country_code=country)
    performance_objects = CountryPerformance.objects.filter(query)
    l = []
    country_names = set()
    for ob in performance_objects:
        country_names.add(ob.country.country_name)
        d = {'year': ob.year, 'value': ob.value, "country_name": ob.country.country_name,
             "performance_index": ob.performance_index, "country_code": ob.country.country_code}
        l.append(d)
    df = pd.DataFrame.from_records(l)
    aggregated = df.groupby(['performance_index', 'country_code']).agg({"country_name": 'first',
                                                                        'year': lambda x: x.to_list(),
                                                                        'value': lambda x: x.to_list()})
    s = df.set_index(['performance_index', 'country_code', 'country_name', 'year']).unstack(
        ['country_code', 'country_name'])['value'].fillna('')
    grouped = s.groupby(level=0)
    reagg = grouped.apply(lambda series: series.to_dict('list')).rename('value').to_frame()
    reagg = reagg.join(grouped.apply(lambda series: series.index.get_level_values(-1).to_list()).rename('year'))
    out = reagg.reset_index().to_dict('records')
    for x in out:
        x['value'] = [[*key, value] for key, value in x['value'].items()]
    return out


def startup_details(country_list):
    ret = {}
    query = Q(country__country_code=country_list[0])
    for country in country_list[1:]:
        query = query | Q(country__country_code=country)
    startup_objects = Startup.objects.filter(query)
    fields = ['country__country_name', 'country__country_code', 'name', 'capital', 'creation_date',
              'number_of_employees', 'website']
    startups_df = pd.DataFrame(startup_objects.values(*fields))
    startups_dict = startups_df.to_dict('records')
    return startups_dict


def get_country_codes():
    country_dict = {}
    countries = Countries.objects
    for el in countries.all():
        country_dict[el.country_code] = {"name": el.country_name}
    return country_dict


def country_view(request):
    country = request.GET['country']
    country_list = request.GET['country'].split(',')
    country_dict = {}
    countries = Countries.objects
    for el in countries.all():
        country_dict[el.country_code] = el.country_name
    context = {'codes': country_dict}
    countries_data = {}
    query = Q(country__country_code=country_list[0])
    for country in country_list[1:]:
        query = query | Q(country__country_code=country)
    performance_objects = CountryPerformance.objects.filter(query)
    startup_objects = Startup.objects.filter(query)
    fields = ['country__country_name', 'country__country_code', 'name', 'capital', 'creation_date',
              'number_of_employees', 'website']
    startups_df = pd.DataFrame(startup_objects.values(*fields))
    startups_dict = startups_df.to_dict('records')
    context['startups'] = startups_dict
    l = []
    country_names = set()
    for ob in performance_objects:
        country_names.add(ob.country.country_name)
        d = {'year': ob.year, 'value': ob.value, "country_name": ob.country.country_name,
             "performance_index": ob.performance_index, "country_code": ob.country.country_code}
        l.append(d)
    context['country_name'] = ";".join(list(country_names))
    df = pd.DataFrame.from_records(l)
    aggregated = df.groupby(['performance_index', 'country_code']).agg({"country_name": 'first',
                                                                        'year': lambda x: x.to_list(),
                                                                        'value': lambda x: x.to_list()})
    s = df.set_index(['performance_index', 'country_code', 'country_name', 'year']).unstack(
        ['country_code', 'country_name'])['value']
    grouped = s.groupby(level=0)
    reagg = grouped.apply(lambda series: series.to_dict('list')).rename('value').to_frame()
    reagg = reagg.join(grouped.apply(lambda series: series.index.get_level_values(-1).to_list()).rename('year'))
    context['reaggregated_data'] = reagg.reset_index().to_dict('records')
    data = dict()
    for key in aggregated.index.get_level_values(0).unique():
        d = aggregated.loc[key].to_dict('index')
        all_c_data = {}
        for cou, k in d.items():
            all_c_data[cou] = {"country_name": k['country_name']}
            ds = []
            for x, y in zip(k['year'], k['value']):
                ds.append({"x": x, "y": y})
            all_c_data[cou]['data'] = ds
        data[key] = all_c_data
    context['colors'] = {c: random_color() for c in country_list}
    context['data'] = data
    return render(request, 'country.html', context)


def contact_us_view(request):
    return render(request, 'contact_us.html', {})
# Create your views here.
