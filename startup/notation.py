from startup.models import Countries, CountryPerformance, PerformanceIndex, Startup, StartupPerformance
from django.db.models import Q
import pandas as pd

def totals_from_weights(weights, years=[2018, 2019]):
    keys = list(weights.keys())
    q = Q()
    for key in keys:
        q = q | Q(performance_index_id=key)
    q_years = Q()
    for year in years:
        q_years = q_years | Q(year=year)
    q = q #& q_years
    df_values = CountryPerformance.objects.filter(q).values()
    df = pd.DataFrame(df_values)
    values = (df.sort_values(by="year")
              .groupby(['country_id', 'performance_index_id'])['value'].last().unstack(-1))
    mins = values.min(axis=0)
    maxes = values.max(axis=0)
    higher_is_better = (pd.DataFrame(PerformanceIndex.objects.all()
                                     .values('id', 'higher_is_better')).set_index('id').iloc[:, 0])
    normalized = values.subtract(mins, axis=1).divide(maxes - mins, axis=1)
    normalized = normalized.multiply(2 * higher_is_better.loc[normalized.columns] - 1)
    s = pd.Series(weights)
    value_by_country = (normalized * s).sum(axis=1)
    value_by_country = (value_by_country - value_by_country.min()) / (value_by_country.max() - value_by_country.min())
    to_return = {}
    for country_id, note in value_by_country.iteritems():
        c = Countries.objects.get(pk=country_id)
        name = c.country_name
        code = c.country_code
        to_return[code] = {"name": name, "note": note}
    return to_return









