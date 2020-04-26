var sub_charts_data = {{startups_full_view | safe}}
for (var i = 0; i < sub_charts_data.length; i++) {
    let row = sub_charts_data[i]['performance']
    let id = sub_charts_data[i]['id']
    if (row !== undefined) {
        keys = Object.keys(row)
        for (var j = 0; j < keys.length; j++) {
            let key = keys[j]
            let ctx = $(`#performance-index-${key}-${id}`)[0].getContext('2d');
            let data = row[key];
            let options = {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: false
                        }
                    }],
                    xAxes: [{
                        barPercentage: 0.2
                    }]
                }
            }
            new Chart(ctx, {
                type: "bar",
                data: {
                    "labels": data["year"],
                    datasets: [{
                        "label": key,
                        "data": data["value"],
                        "backgroundColor": "green"
                    }]
                },
                options: options
            })
        }
    }
}