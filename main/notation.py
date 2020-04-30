import pandas as pd

from .models import CountryNotation


def country_notation(weights):

    notation = CountryNotation.objects.values('country__country_code', 'index_id', 'note', 'country__country_name')
    notation = pd.DataFrame(notation)
    notation = notation.set_index(['country__country_code', 'country__country_name', 'index_id']).note.unstack(-1)
    notation = (notation * pd.Series(weights)).sum(axis=1)
    notation = (notation - notation.min()) / (notation.max() - notation.min())
    to_return = {}
    for (country_id, country_name), note in notation.iteritems():
        to_return[country_id] = {"name": country_name, "note": note}
    return to_return
