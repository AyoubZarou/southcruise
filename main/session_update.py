import json
from main.models import PerformanceIndex, OrderOpinion
from collections import defaultdict


def update_country_charts_session(data, request):
    """ Update the session of the user to include what charts he wants to display
    :param data: data to update the session with, in a form of a dumped json
    :param request: the request object, it contains the session object to update
    the data has the form {chart_id:int: {year_range, chart_type, include_chart: bool}}
    """
    context = json.loads(data)
    context = {int(key): context[key] for key in context}
    d = defaultdict(dict)
    for key, v in context.items():
        category = PerformanceIndex.objects.get(pk=key).category
        d[category][key] = v
    request.session['charts_data'] = dict(d)


def _process_weights(w):
    l = []
    remain = 100
    for _w in w[:-1]:
        l.push(int(remain * _w / 100))
        remain -= remain * _w / 100
    l.push(int(remain))
    return l


def update_indexes_order_session(data, request):
    data = json.loads(data)
    print("data is", data, type(data))
    # weights = _process_weights(data['weights'])

    session_id = '_SessionBase__session_key'
    try:
        session_key = request.session.session_key
        print("session key", request.session.session_key)
        exists = OrderOpinion.objects.filter(session_key=session_key)
        if len(exists):
            exists.update(order=json.dumps(data))
        else:
            opinion = OrderOpinion(session_key=session_key, order=json.dumps(data))
            opinion.save()
    except:
        pass
    request.session['indexes_order'] = dict(zip(data['ids'], data['values']))
    print(request.session["indexes_order"], 'after')


def update_startup_indexes_order_session(data, request):
    data = json.loads(data)
    request.session['startup_indexes_order'] = dict(zip(data['ids'], data['values']))


def update_startup_filters_session(data, request):
    data = json.loads(data)
    request.session['startup_filters'] = data


def update_target_view(data, request):
    data = json.loads(data)
    print('data is', data)
    request.session['target_view'] = data['target_view']
