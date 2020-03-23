from django.shortcuts import render
from django.http import HttpResponse
from .models import Countries
import pandas as pd
import random


def index(request):
    country_codes = Countries.objects.all()
    df = pd.DataFrame.from_records(country_codes.values())
    data = df[['country_code', 'country_name']].set_index('country_code').to_dict()
    colors = {}
    for key in data['country_name']:
        color = random.random() / 4
        red = int(255 * (color + 0.25))
        green = int(255 * (0.75 - color))
        color_str = f'rgb({red}, {green}, 0)'
        colors[key] = color_str
    data['colors'] = colors
    return render(request, 'africamap.html', data)


def country_view(request):
    country = request.GET['country']
    for_country = Countries.objects.filter(country_code=country)
    df = pd.DataFrame.from_records(for_country.values())
    context = {'country_code': country}
    data = {}
    config = {"GDP_growth": {"name": 'gross domestic product annual growth (%)', 'type': 'bar'},
              "GDP_cum": {"name": 'cumulative GDP growth', 'type': 'line'}}
    if df.shape[0] != 0:
        context['country_name'] = df.country_name.iloc[0]
        context['year'] = df['year'].to_list()
        data['GDP_growth'] = df['GDP_growth'].round(2).to_list()
        data['GDP_cum'] = df['GDP_growth'].divide(100).add(1).cumprod().round(2).to_list()
    context['data'] = data
    context['config'] = config
    return render(request, 'country.html', context)

def contact_us_view(request):
    return render(request, 'contact_us.html', {})
# Create your views here.
