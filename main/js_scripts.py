from collections import defaultdict

""" Format startups table, if the field name is provided, the filed would be renamed, 
    the format function is used to folat the field, if we want to format the filed using another field we pass 
    the other filed to as an argument, but as format takes on argument, we pass the values joined using `|`, so to 
    retrieve the separate fields, all we have to do is add splitd_values = value.split('|') in our script, the fileds 
    to add are in add_fields variable

"""

DATA_FIELDS_MAPPER = defaultdict(lambda: {})

# format the website
DATA_FIELDS_MAPPER['website'] = {
    "name": "website",
    "format": '(value) =>  `<a class="text-primary" href="${value}">${value}</a>`',
    "width": 2
}
# format the capital
DATA_FIELDS_MAPPER['capital'] = {
    "name": "capital",
    "format": '(value) =>  {if (value){\
                return `<span class="float-right"> $ ${parseInt(value)}</span>`};\
                 return `<span class="float-right" style="color: #DDDDDD"> Not provided </span>`}',
    "width": 2
}

# presentation should have higher width than the other fields
DATA_FIELDS_MAPPER['presentation'] = {
    "name": "Presentation",
    "width": 5,
}

# format the name, so when clicked upon it displays the startup detail on the side using the
# `show_global_startup_detail` function
DATA_FIELDS_MAPPER['name'] = {
    "name": "name",
    "format": '(value) => { \
    var split = value.split(`|`);\
    return `<span onclick="show_global_instrument_detail(this)" \
    refers-to="startup-detailed-${split[1]}" \
    style="cursor:pointer"> ${split[0]} </span>`}',
    "add_field": ['id'],
}

# format country name to display as a badge

DATA_FIELDS_MAPPER['country__country_name'] = {
    "name": "Country",
    "add_field": ['country__country_code'],
    "format": '(value)=>{ \
    var split = value.split(`|`);\
     return `<span class="badge badge-pill badge-primary badge-${split[1]}"> ${split[0]} </span>` \
    }'
}

# display sectors as `,` separated
DATA_FIELDS_MAPPER['sectors'] = {
    "name": "Sectors",
    "format": '(value)=>{value = eval(value ); return value.join(`, `)}'
}

DATA_FIELDS_MAPPER['security'] = {
    "name": "security",
    "format": '(value) => { \
    var split = value.split(`|`); \
    return `<span onclick="show_global_instrument_detail(this, \'company\')" \
    refers-to="company-detailed-${split[1]}" \
    style="cursor:pointer"> ${split[0]} </span>`}',
    "add_field": ['id'],
}