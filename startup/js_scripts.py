from collections import defaultdict

DATA_FIELDS_MAPPER = defaultdict(lambda: None)

DATA_FIELDS_MAPPER['website'] = {
    "name": "website",
    "format": '(value) =>  `<a class="text-primary" href="${value}">${value}</a>`',
    "width": 2
}

DATA_FIELDS_MAPPER['presentation'] = {
    "name": "Presentation",
    "width": 5,
    # "format": '(value) => value.replace("\n", "</br>")'
}

DATA_FIELDS_MAPPER['name'] = {
    "name": "name",
    "format": '(value) => { \
    var split = value.split(`|`);\
    return `<span onclick="show_global_startup_detail(this)" \
    refers-to="startup-detailed-${split[1]}" \
    style="cursor:pointer"> ${split[0]} </span>`}',
    "add_field": ['id'],
}

DATA_FIELDS_MAPPER['country__country_name'] = {
    "name": "Country",
    "add_field": ['country__country_code'],
    "format": '(value)=>{ \
    var split = value.split(`|`);\
     return `<span class="badge badge-pill badge-primary badge-${split[1]}"> ${split[0]} </span>` \
    }'
}

DATA_FIELDS_MAPPER['sectors'] = {
    "name": "Sectors",
    "format": '(value)=>{value = eval(value ); return value.join(`, `)}'
}