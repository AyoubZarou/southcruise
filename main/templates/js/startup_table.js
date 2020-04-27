// set the startups table
// set True and False so it would be parsed safely
var True = true
var False = false
{% if target_view == "startup" %}
var data = {{startups|safe}}
var id_section = '#startup-detail-table'
{% else %}
var data = {{companies_dataset|safe}}
var id_section = "#companies-detail-table"
{% endif %}
for (i = 0; i < data['columns'].length; i++) {
    if (typeof data['columns'][i]['format'] === "string") {
        data['columns'][i]['format'] = eval(data['columns'][i]['format'])
    }
}

let dt = new DataTable(id_section, {
    columns: data['columns'],
    data: data['data'],
    layout: 'ratio'
}, )