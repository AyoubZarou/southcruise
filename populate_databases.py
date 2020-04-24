import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "southcruise.settings")
import django
from django.utils import timezone
import pandas as pd
import numpy as np
import random
import itertools
from collections import defaultdict

django.setup()
from startup.models import (Countries, CountryPerformance, Startup, PerformanceIndex, StartupPerformance, \
                            StartupActivityCountry, StartupSector)

TO_REFRESH = [Startup, StartupPerformance,
              StartupActivityCountry, StartupSector]
for model in TO_REFRESH:
    model.objects.all().delete()

countries_code = {'AGO': 'Angola', 'BDI': 'Burundi', 'BEN': 'Benin', 'BFA': 'Burkina Faso', 'BWA': 'Botswana',
                  'CAF': 'Central African Republic',
                  'CIV': "Ivory Coast", 'CMR': 'Cameroon', 'COD': 'Democratic Republic of the Congo',
                  'COG': 'Republic of the Congo',
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
                  'UGA': 'Uganda', 'ZAF': 'South Africa', 'ZMB': 'Zambia', 'ZWE': 'Zimbabwe', 'SWZ': 'Swaziland',
                  'SSD': 'South Sudan'}

# Reporocessing Startup Data
# mapping used to map countries on the dataset to their unique country code
startup_data_country_mapping = {
    'Rwanda': 'RWA', 'Angola': 'AGO', 'South Africa': 'ZAF', 'Maroc': 'MAR',
    'Nigeria': 'NGA', "Côte d'ivoire": 'CIV', 'Cameroun': 'CMR', 'Egypte': 'EGY',
    'Ghana': 'GHA', 'Kenya': 'KEN', 'Madagascar': 'MDG', 'Tunisie': 'TUN',
    'Tanzanie': 'TZA', 'Senegal': 'SEN', 'Afrique du Sud': "ZAF", 'Ouganda': "UGA",
    "Mauritius": 'MAU',
}
# path to sartup data
startup_data_path = "C:\\Users\\ZAROU\\Desktop\\southcruise_data\\South_cruise_startup_base (version 1).xlsx"
# used to rename the fields
field_names = {
    "Company": "name",
    "Sector": "sector",
    "Pays": 'country_name',
    "Pays d'activité": "activity_countries",
    "Année de création ": "creation_date",
    "Niveau de maturité": "maturity",
    "Fondateur": "founder",
    "site web": "website",
    "Customers": "customers",
    "Operiationals": "operationals",
    "Potentiel de marché/client": "market_potential",
    "Principaux investisseurs": "investors",
    "Partenariat": "partnerships",
    "Innovation": "innovation",
    "Impact": "impact",
    "Awards": "awards",
    "Taux de croissance reporté": "growth_rate",
    "Chiffre d'affaire reporté": "capital",
    "Presentation": "presentation",
    "Nombre d'employés": "number_of_employees",
    "Levée de fonds": "fund_raising",
    "Année levée de fonds": "fund_raising_year",
    'Résultat net reporté': 'reported_net_result',
    "Moyenne d'âge des fondateurs": "founders_mean_age",
    "Strucuture de l'entreprise": "structure",
    'Dette nette reportée': 'reported_net_debt',
    "Niveau d'éducation des fondateurs": 'founders_mean_education_level',
    "Contact": 'contact',
}
# used to map sector to a more restrective set
sector_mapping = {
    "Logisitics & transport": ["Logisitics", "Logistique", "Transport", "Mobility Tech"],
    "Communication": ['Telecommunication', "Télécommunication", "Communication", "Telecom"],
    "Services": ['Services', "Service", "E-Services", "E-services", "e-Services", "Consumer Service", ],
    "Tech": ["Tech", "EduTech", "CivicTech", "FinTech", "Fintech", "E-Services", "E-services", "e-Services",
             "AgriTech", "Edutech", "Tech - R&D", "Tech - Events",
             "Technologie", "Mobility Tech", "Technology", "Site internet", ],
    "Education": ['Education', 'EduTech', "Edutech"],
    "Commerce & Business": ['Commerce', "e-Commerce", "E-commerce", "Business"],
    "Health": ["Health Tech", "Healthcare", ],
    "Energy": ["Energy", "Energie", "Energie "],
    "Media": ["Media", "Musique", "Audiovisual"],
    "tourism": ['Agro-Tourism', "Tourisme"],
    "Environment": ['Environment', "Environment", ' Environment'],
    "Food & Agriculture": ['Agriculture', "Baby Food", "Food", "AgriTech", "Agro-Tourism"],
    "Industry & Production": ["Production", "Industries Créatives", "Electronic Recycling"],
}

startup_df = pd.read_excel(startup_data_path)
startup_df.rename(field_names, axis=1, inplace=True)
# delete every filed not having any value in it
startup_df = startup_df.loc[:, startup_df.notna().sum().ne(0)]
startup_df['country_code'] = startup_df.country_name.map(startup_data_country_mapping)
startup_df.dropna(subset=['country_code'], inplace=True)
# split activity countries so we can have a set of countries for each entry
startup_df['activity_countries'] = startup_df.activity_countries.str.split('/')

# pivot the sector mapping
pivot_mapping = defaultdict(list)
for k, v in sector_mapping.items():
    for i in v:
        pivot_mapping[i].append(k)
# map every entry on the sector values to a set of sectors on the new set, while concatenating sets of sectors if
# there is more than one sector chosen (specified by "/" or "\n")
startup_df['sector_values'] = (startup_df.sector.str.split('/|\n')
                               .apply(lambda x: [*itertools.chain(*[pivot_mapping[i] for i in x])]))
# convert the creation data to an actual data
startup_df['capital'] = startup_df.capital.astype(str).str.extract('(\d+)')[0]
startup_df['year_of_creation'] = startup_df.creation_date.apply(lambda x: int(x) if not np.isnan(x) else -1)
startup_df['creation_date'] = pd.to_datetime("01-01-" + startup_df.year_of_creation.astype(str),
                                             format="%d-%m-%Y", errors="coerce")

startup_df['innovation'] = startup_df['innovation'].notna()
startup_df['impact'] = startup_df['impact'].notna()
# startup_df['reported_net_result'] = startup_df['reported_net_result'].str.extract('(\d+)').astype(float)[0]

fund_raising_values = (startup_df['fund_raising'].str.split('/', expand=True)
                       .apply(lambda x: x.str.extract("(\d+)")[0], axis=1).astype(float))
fund_raising_years = (startup_df['fund_raising_year']
                      .apply(lambda x: x if pd.isna(x) else str(x)).str.split('/', expand=True))


def dict_values(l):
    a, b = l
    return {int(x): y for x, y in zip(a, b) if pd.notna(x) and pd.notna(y)}


startup_df['fund_raising_dicts'] = [*map(dict_values, zip(fund_raising_years.values, fund_raising_values.values))]

path = "C:\\Users\\ZAROU\\Desktop\\southcruise_data\\Countries extraction"
names = os.listdir(path)
dfs = []
for name in names:
    year = int(name.split('_')[-1].split(".")[0])
    df = pd.read_html(os.path.join(path, name), skiprows=1, header=0)[0]
    df['year'] = year
    dfs.append(df)
countries_performance_df = pd.concat(dfs)
countries_performance_df['COUNTRY CODE'] = (countries_performance_df['COUNTRY NAME']
                                            .map({val: key for key, val in countries_code.items()}))

ECO = "ECONOMIC"
SOC = "SOCAIL"
INF = "INFRASTRACTURE"

HIGHER_IS_BETTER_WITH_CAT = {
    'GROSS GOVERNMENT DEBT (% OF GDP)': [False, ECO],
    'INFLATION, CONSUMER PRICES (ANNUAL %)': [False, ECO],
    'GDP, REAL USD (MILLIONS)': [True, ECO],
    'FDI, INWARD, % OF GDP': [True, ECO],
    'UNEMPLOYMENT RATE, ILO DEFINITION': [False, SOC],
    'GDP GROWTH (ANNUAL %)': [True, ECO],
    'GDP PER CAPITA (US$)': [True, ECO],
    'GDP PER CAPITA GROWTH (ANNUAL %)': [True, ECO],
    'IFO POLITICAL INSTABILITY': [False, SOC],
    'INDUSTRY, VALUE ADDED (% OF GDP)': [True, ECO],
    'INFLATION': [True, ECO],
    'LABOR FORCE PARTICIPATION RATE, TOTAL (% OF TOTAL AGES 15-64)': [True, ECO],
    'LIFE EXPECTANCY AT BIRTH, TOTAL (YEARS)': [True, SOC],
    'LONG-TERM UNEMPLOYMENT (% OF TOTAL UNEMPLOYMENT)': [False, SOC],
    'POPULATION, TOTAL': [True, SOC],
    'TAX REVENUE (% OF GDP)': [False, ECO],
    'TAX REVENUE, CORPORATE (%YOY)': [False, ECO],
    'UNEMPLOYMENT RATE (STANDARDIZED)': [False, SOC],
    'UNEMPLOYMENT RATE (%YOY, STANDARDIZED)': [False, SOC],
    'UNEMPLOYMENT': [False, SOC],
    'SAVINGS, PERSONAL SECTOR (%YOY)': [True, SOC],
    'POPULATION IN THE LARGEST CITY (% OF URBAN POPULATION)': [True, SOC],
    'NET TAXES ON PRODUCTS (US$)': [False, ECO],
    'MOBILE CELLULAR SUBSCRIPTIONS (DATA FROM ITU)': [True, SOC],
    'MOBILE CELLULAR SUBSCRIPTIONS (PER 100 PEOPLE) (DATA FROM ITU)': [True, SOC],
    'LISTED DOMESTIC COMPANIES, TOTAL': [True, ECO],
    'LABOR FORCE, TOTAL': [True, SOC],
    'INDUSTRY, VALUE ADDED (US$)': [True, ECO],
    'GDP PER PERSON EMPLOYED (CONSTANT 1990 PPP $)': [True, ECO],
    'GDP PER CAPITA, PPP (CURRENT INTERNATIONAL $)': [True, ECO],
    'ENERGY PRODUCTION (KT OF OIL EQUIVALENT)': [True, ECO],
    'ENERGY IMPORTS, NET (% OF ENERGY USE)': [False, ECO],
    'EMPLOYMENT TO POPULATION RATIO, AGES 15-24, TOTAL (%)': [True, SOC],
    'EMPLOYMENT IN SERVICES (% OF TOTAL EMPLOYMENT)': [True, ECO],
}

if Countries in TO_REFRESH:
    for country, country_name in countries_code.items():
        Countries(country_code=country, country_name=country_name).save()

if CountryPerformance in TO_REFRESH:
    groups = countries_performance_df.groupby('COUNTRY CODE').groups
    for col, (higher_is_better, category) in HIGHER_IS_BETTER_WITH_CAT.items():
        print(col)
        performance_index = PerformanceIndex(name=col, category=category,
                                             higher_is_better=higher_is_better)
        performance_index.save()
        for country_code, idx in groups.items():
            s = countries_performance_df.loc[idx, [col, 'year']]
            s = s.dropna(subset=[col])
            country = Countries.objects.get(country_code=country_code)
            for i, series in s.iterrows():
                val, year = series.values
                cp = CountryPerformance(country=country, year=year, value=val,
                                        performance_index=performance_index)
                cp.save()

if Startup in TO_REFRESH:
    cols_to_exclude = ['activity_countries', "sector_values", "fund_raising",
                       "fund_raising_year", 'sector', "year_of_creation",
                       "country_name", "fund_raising_dicts", "country_code"]
    for i, da in startup_df.iterrows():
        print("name :", da['name'])
        startup_d = da[da.index.difference(cols_to_exclude)].to_dict()
        country = Countries.objects.get(country_code=da.country_code)
        values = dict([*filter(lambda x: not pd.isna(x[1]), startup_d.items())])
        startup = Startup(**values, country=country)
        startup.save()
        fund_raising_dict = da.fund_raising_dicts
        for year, value in fund_raising_dict.items():
            startup_perf = StartupPerformance(startup=startup, index="fund_raising", year=year, value=value)
            startup_perf.save()
        for sector in da.sector_values:
            StartupSector(startup=startup, sector=sector).save()
        if type(da.activity_countries) is list:
            for country in da.activity_countries:
                StartupActivityCountry(startup=startup, country=country).save()
