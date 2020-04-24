import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "southcruise.settings")
import django
import pandas as pd
import datetime

django.setup()
from startup.models import (Countries, CountryPerformance, Startup, PerformanceIndex, StartupPerformance,
                            StartupActivityCountry, StartupSector, RegisteredCompany,
                            RegisteredCompanyPerformance, CountryNotation)

from startup.config import TAKE_INTO_ACCOUNT
CountryNotation.objects.all().delete()

MAX_LOOK_BACK_YEARS = 3
k = {}
current_year = datetime.datetime.now().year
for key, val in TAKE_INTO_ACCOUNT.items():
    if val['include']:
        per_index = PerformanceIndex.objects.get(pk=val['id'])
        values = CountryPerformance.objects.filter(performance_index=per_index).values('country', 'value', 'year')
        df = pd.DataFrame(values)
        df = df.query(f'year >= {current_year - MAX_LOOK_BACK_YEARS}')
        df = df.sort_values(by='year').groupby('country')[['value']].last()
        df['value'] = (df['value'] - df.value.min()) / (df.value.max() - df.value.min())
        for c, n in df.value.iteritems():
            country = Countries.objects.get(pk=c)
            notation = CountryNotation(country=country, index=per_index, note=n)
            notation.save()
