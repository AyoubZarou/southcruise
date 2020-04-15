import json
from startup.models import PerformanceIndex
from collections import defaultdict


def update_country_charts_session(data, request):
    """ Update the session of the user to include what charts he wants to display
    :param data: data to update the session with, in a form of a dumped json
    :param request: the request object, it contains the session object to update
    the data has the form {chart_id:int: {year_range, chart_type, include_chart}}
    """
    context = json.loads(data)
    context = {int(key): context[key] for key in context}
    d = defaultdict(dict)
    for key, v in context.items():
        category = PerformanceIndex.objects.get(pk=key).category
        d[category][key] = v
    request.session['charts_data'] = dict(d)

def update_indexes_order_session(data, request):
    data = json.loads(data)
    request.session['indexes_order'] = data