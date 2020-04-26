// set the startups table
// set True and False so it would be parsed safely
var True = true
var False = false
var data = {{startups|safe}}

for (i = 0; i < data['columns'].length; i++) {
    if (typeof data['columns'][i]['format'] === "string") {
        data['columns'][i]['format'] = eval(data['columns'][i]['format'])
    }
}
let dt = new DataTable('#startup-detail-table', {
    columns: data['columns'],
    data: data['data'],
    layout: 'ratio'
}, )