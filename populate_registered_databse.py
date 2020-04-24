import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "southcruise.settings")
import django
import pandas as pd

django.setup()
from startup.models import (Countries, CountryPerformance, Startup, PerformanceIndex, StartupPerformance,
                            StartupActivityCountry, StartupSector, RegisteredCompany, RegisteredCompanyPerformance)

countries_mapping = {'AGO': 'Angola', 'BDI': 'Burundi', 'BEN': 'Benin', 'BFA': 'Burkina Faso', 'BWA': 'Botswana',
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
                     'SSD': 'South Sudan', "MAU": "Mauritius"}

pivoted_countries_mapping = {val: key for key, val in countries_mapping.items()}

PATH_TO_FILE = "C:/Users/ZAROU/Desktop/southcruise_data/SouthCruise_companies_cotee_.xls"
df = pd.read_html(PATH_TO_FILE, skiprows=1, header=0)[0]

melted = df.melt(id_vars=['Security', 'RIC', 'Country', 'TRBC Sector', 'GICS Sector']).dropna()
groups = melted.groupby(['Security', 'RIC', 'Country', 'TRBC Sector', 'GICS Sector']).groups

for (security, ric, country, trbc_sector, gics_sector), idx in groups.items():
    print(security)
    country_code = pivoted_countries_mapping[country]
    sub_df = melted.loc[idx, ['variable', 'value']]
    country = Countries.objects.get(country_code=country_code)
    company = RegisteredCompany(country=country, security=security, trbc_sector=trbc_sector,
                                gics_sector=gics_sector)
    company.save()
    for _, s in sub_df.iterrows():
        var = s.variable
        value = s.value
        per = RegisteredCompanyPerformance(company=company, index=var, value=value)
        per.save()
