var datasets;
var data = {{ performance|safe}};
var colors = {{colors|safe}};
var datasets_set = []
var years = [];
var indicator_values;
var per_index_ids = []
var idx;
var ctx;
var n;
// we set True and False so that the python dictionary will be parsed without a problem
var True = true;
var False = false;
var charts_data = {{indexes|safe}};

// used to merge a set of dictionaries
function merge_dicts(d) {
    let values = Object.values(d)
    return values.reduce(function(r, o) {
        Object.keys(o).forEach(function(k) {
            r[k] = o[k];
        });
        return r;
    }, {});
    return values
}
charts_data = merge_dicts(charts_data);
var to_push;
for (var l = 0; l < data.length; l++) {
    datasets = [];
    indicator_values = data[l]['value'];
    idx = '' + data[l]['performance_index_id']
    for (var country in indicator_values) {
        to_push = {
            data: indicator_values[country][2],
            label: indicator_values[country][1],
            borderColor: colors[indicator_values[country][0]],
        }
        if (charts_data[idx]['type'] == "bar") {
            to_push['backgroundColor'] = colors[indicator_values[country][0]];
        }
        datasets.push(to_push)
    }
    years.push(data[l]['year'])
    datasets_set.push(datasets)
}
for (n = 1; n < datasets_set.length + 1; n++) {
    idx = '' + data[n - 1]['performance_index_id']
    ctx = $("#performance-chart-" + idx)[0].getContext('2d');
    new Chart(ctx, {
        "type": charts_data[idx]['type'],
        data: {
            labels: years[n - 1],
            datasets: datasets_set[n - 1],
        },
        options: {}
    })
}

// change the displayed graph when one is selected
$('#chart-select').on('change', (event) => {
    var id_idx = $(event["target"].selectedOptions[0]).attr("refers-to");
    var charts = $('#charts-container .tab-pane');
    var delete_tab, show_tab;
    for (i = 0; i < charts.length; i++) {
        let tab = $(charts[i]);
        console.log(tab);
        let refered_idx = tab.attr('refers-to');
        if (refered_idx === id_idx) {
            show_tab = tab
        } else if (tab.hasClass('show active')) {
            delete_tab = tab
        }
    }
    show_tab.addClass('show active')
    delete_tab.removeClass('show active')
})