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
    console.log('dada')
    var datasets;
    var data = {{performance|safe}};
    var colors = {{colors|safe}};
    console.log(colors)
    var datasets_set = []
    var years = [];
    var indicator_values
    for (var l in data){
        datasets = [];
        indicator_values = data[l]['value'];
        for (var country in indicator_values){
            datasets.push({data: indicator_values[country][2],
                            label: indicator_values[country][1],
                            backgroundColor: colors[indicator_values[country][0]]})

        }
        console.log(datasets)
        years.push(data[l]['year'])
        datasets_set.push(datasets)
    }
    var ctx;
    var n;
    for (var l in datasets_set){
        n = parseInt(l)+ 1
        console.log("#performance-chart-" + n)
        ctx = $("#performance-chart-" + n)[0].getContext('2d');
        new Chart(ctx, {"type": 'bar',
                data: { labels: years[n-1],
                    datasets: datasets_set[n-1]
                    },
                options:{}})
    }

});