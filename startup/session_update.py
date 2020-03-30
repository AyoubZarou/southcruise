import json


def update_country_charts_session(data, request):
    context = json.loads(data)
    context = {int(key): context[key] for key in context}
    request.session['charts_data'] = context
