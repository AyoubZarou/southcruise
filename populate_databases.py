import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "southcruise.settings")
import django
from django.utils import timezone
import pandas as pd
import numpy as np
import random

django.setup()
from startup.models import Countries, CountryPerformance, Startup, PerformanceIndex

Countries.objects.all().delete()
CountryPerformance.objects.all().delete()
Startup.objects.all().delete()

countries_code = {'AGO': 'Angola', 'BDI': 'Burundi', 'BEN': 'Benin', 'BFA': 'Burkina Faso', 'BWA': 'Botswana',
                  'CAF': 'Central African Republic',
                  'CIV': "Cote d'Ivoire", 'CMR': 'Cameroon', 'COD': 'Congo Democratic Republic',
                  'COG': 'Congo Republic',
                  'DJI': 'Djibouti', 'DZA': 'Algeria', 'EGY': 'Egypt', 'ERI': 'Eritrea', 'ETH': 'Ethiopia',
                  'GAB': 'Gabon', 'GHA': 'Ghana', 'GIN': 'Guinea', 'GMB': 'Gambia', 'GNB': 'Guinea-Bissau',
                  'GNQ': 'Equatorial Guinea', 'KEN': 'Kenya', 'LBR': 'Liberia', 'LBY': 'Libya', 'LSO': 'Lesotho',
                  'MAR': 'Morocco',
                  'MDG': 'Madagascar', 'MLI': 'Mali', 'MOZ': 'Mozambique', 'MRT': 'Mauritania', 'MWI': 'Malawi',
                  'NAM': 'Namibia',
                  'NER': 'Niger', 'NGA': 'Nigeria', 'RWA': 'Rwanda', 'SDN': 'Sudan', 'SEN': 'Senegal',
                  'SLE': 'Sierra Leone',
                  'SOM': 'Somalia', 'SSD': 'South Sudan', 'TCD': 'Chad', 'TGO': 'Togo', 'TUN': 'Tunisia',
                  'TZA': 'Tanzania',
                  'UGA': 'Uganda', 'ZAF': 'South Africa', 'ZMB': 'Zambia', 'ZWE': 'Zimbabwe', 'SWZ': 'Eswatini',
                  'SSD': 'Sounth Sudan'}

path = "C:\\Users\\ZAROU\\Desktop\\data"
names = os.listdir(path)
NB_STARTUP_RANGE = [10, 20]
str_list = list('AZERTYUIOPMLJHGDSQWXCVBN')


def generate_name():
    i = random.randint(3, 10)
    return "".join(np.random.choice(str_list, i))


for country, country_name in countries_code.items():
    Countries(country_code=country, country_name=country_name).save()

for p in names:
    df = pd.read_csv(os.path.join(path, p), skiprows=3)
    df = df.set_index(['Country Code'])
    cols = df.columns.str.isnumeric()
    performance_index = PerformanceIndex(name=df['Indicator Name'].iloc[0])
    performance_index.save()
    df = df.loc[:, cols].stack().dropna().reset_index().rename({'level_1': 'year'}, axis=1)
    for country, country_name in countries_code.items():
        sub_df = df[df['Country Code'] == country]
        country_ = Countries.objects.get(country_code=country)
        n_startups = random.randint(*NB_STARTUP_RANGE)
        for i in range(n_startups):
            star = Startup(country=country_, name=generate_name(), capital=np.random.uniform(10000, 100000),
                           number_of_employees=np.random.randint(2, 30),
                           creation_date=timezone.now() - timezone.timedelta(days=np.random.randint(100, 2000)),
                           website='www.testexample.com')

            print(country_.country_name, star.name)
            star.save()
        for _, row in sub_df.iterrows():
            cp = CountryPerformance(country=country_, year=row['year'], value=row[0],
                                    performance_index=performance_index)
            cp.save()
