$(function() {
  var $tabButtonItem = $('#tab-button li'),
      $tabSelect = $('#tab-select'),
      $tabContents = $('.tab-contents'),
      activeClass = 'is-active';

  $tabButtonItem.first().addClass(activeClass);
  $tabContents.not(':first').hide();

  $tabButtonItem.find('a').on('click', function(e) {
    var target = $(this).attr('href');

    $tabButtonItem.removeClass(activeClass);
    $(this).parent().addClass(activeClass);
    $tabSelect.val(target);
    $tabContents.hide();
    $(target).show();
    e.preventDefault();
  });
  $tabSelect.on('change', function() {
    var target = $(this).val(),
        targetSelectNum = $(this).prop('selectedIndex');

    $tabButtonItem.removeClass(activeClass);
    $tabButtonItem.eq(targetSelectNum).addClass(activeClass);
    $tabContents.hide();
    $(target).show();
  });
    var datasets;
    var data = {{performance|safe}};
    var colors = {{colors|safe}};
    console.log(colors)
    var datasets_set = []
    var years = [];
    var indicator_values;
    var per_index_ids = []
    var idx;
        var ctx;
    var n;
    var True = true;
    var False = false;
    var charts_data = {{indexes|safe}};
    function merge_dicts(d){
        let values = Object.values(charts_data)
        return values.reduce(function (r, o) {
                Object.keys(o).forEach(function (k) { r[k] = o[k]; });
                return r;
    }, {});
    return values
    }
    charts_data = merge_dicts(charts_data);
    var to_push;
    for (var l=0; l<data.length; l++){
        datasets = [];
        indicator_values = data[l]['value'];
        idx = '' + data[l]['performance_index_id']
        for (var country in indicator_values){
            to_push = {data: indicator_values[country][2],
                            label: indicator_values[country][1],
                            borderColor: colors[indicator_values[country][0]],
                            }
            if (charts_data[idx]['type'] == "bar"){
                to_push['backgroundColor'] = colors[indicator_values[country][0]];
            }
            datasets.push(to_push)
        }
        console.log(datasets)
        years.push(data[l]['year'])
        datasets_set.push(datasets)
    }

    for (n=1; n<datasets_set.length +1; n++){
        ctx = $("#performance-chart-" + n)[0].getContext('2d');
        idx = '' + data[n-1]['performance_index_id']
        new Chart(ctx, {"type": charts_data[idx]['type'],
                data: { labels: years[n-1],
                    datasets: datasets_set[n-1],
                    },
                options:{}})
    }
    var sub_charts_data = {{startups_full_view|safe}}
    for (var i=0; i<sub_charts_data.length; i++){
        let row = sub_charts_data[i]['performance']
        let id =  sub_charts_data[i]['id']
        if (row !== undefined){
            keys = Object.keys(row)
            for (var j=0; j< keys.length; j++){
             let key = keys[j]
             let ctx = $(`#performance-index-${key}-${id}`)[0].getContext('2d');
             let data = row[key];
             let options = { scales: { yAxes: [{ ticks: { beginAtZero: false } }],
                                     xAxes: [{ barPercentage: 0.2 }] }}
            new Chart(ctx, {type: "bar", data:{"labels": data["year"],
                                                 datasets: [{"label": key, "data": data["value"],
                                                   "backgroundColor": "green"}]},
                                                       options: options
                                                   })
            }
        }

    }
});