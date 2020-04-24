{% include 'js/retrieve_filter_values.js' %}

//Send an update request to update the session variables
var send_update_request = function(data, target, refresh, after_refresh){
        var context = {"data": JSON.stringify(data)};
        context['target'] = target;
        context['csrfmiddlewaretoken'] = '{{csrf_token}}';
       $.ajax({
       url: "{% url 'update_session' %}",
        method: "POST",
        data: context,
        success:(response)=>{
        console.log(after_refresh)
           if (refresh){
            document.location.href = document.location.href;
            if (after_refresh !== undefined){
            after_refresh()
            }
           }
        }})
 }
// update the fields to display for the country charts, with the type of chart and range in years
var update_charts_fields = function(refresh){
  var include_charts = $('#include-charts input');
  var l = [];
  var r;
  var context = {}
    for (var i=0; i<include_charts.length; i++){

                if (include_charts[i].type == "checkbox"){
                r = $(include_charts[i])
                context[parseInt(r.attr('value'))] = {"name": r.attr('name'), 'checked': include_charts[i].checked}}
                else if (include_charts[i].type == "range"){
                    r = $(include_charts[i])
                    year_min = parseInt(include_charts[i].value)
                    context[parseInt(r.attr('refers-to'))]['range'] = [year_min, 2020]
                }
    };
    var char_type =  $('#include-charts select');
    for (var i=0; i<char_type.length; i++){
        r = $(char_type[i]);
        context[parseInt(r.attr('refers-to'))]['type'] = char_type[i].value
    }
    var c = {}
    let target = 'country_charts'
    send_update_request(data, target, refresh)
}

function update_year_since(that){
    let value = $(that).attr('value');
    let refers_to = $(that).attr('refers-to');
    to_change = $('#year-since-' + refers_to)
    to_change.html(that.value);
}
function remove_from_order(that, side){
    if (side == "startup"){
          let refers_to  = $(that).attr('refers-to');
        $('#desired-startup-order-' + refers_to).css('display', 'none')
    $('#excluded-startup-order-' + refers_to).css('display', 'block')
    } else {
    let refers_to  = $(that).attr('refers-to');
    $('#desired-order-' + refers_to).css('display', 'none')
    $('#excluded-order-' + refers_to).css('display', 'block')
    update_indexes_weights()}
}
function add_to_order(that, side){
    if (side == "startup"){
        let refers_to  = $(that).attr('refers-to');
        $('#desired-startup-order-' + refers_to).css('display', 'block')
    $('#excluded-startup-order-' + refers_to).css('display', 'none')
    } else {
    let refers_to  = $(that).attr('refers-to');
    $('#desired-order-' + refers_to).css('display', 'block')
    $('#excluded-order-' + refers_to).css('display', 'none')
    update_indexes_weights();

}}

var update_indexes_order = function(refresh){
var val = get_country_indexes_weights();
    var els = $('#desired-order-sortable li');
    var order = [];
    for (i=0; i<els.length; i++){
        let el = $(els[i])
         if (el.css('display') !== "none"){
            order.push(parseInt(el.attr('refers-to')))
        }
    }
    let target = "indexes-order"
    after_refresh = ()=>{
    update_indexes_weights()
    }
    send_update_request(val, target, refresh, after_refresh)

}

var update_startup_filters = function(refresh){
    var data = startup_filter_values()
    target = "startup-filters"
    send_update_request(data, target, refresh)
}
function update_indexes_weights(that, side){
     let prefix = ""
    if (side == "startup"){
        prefix = "startup-"
    }
    let weights = get_startup_indexes_weights(side)
    let ids = weights['ids']
    let values = weights['values']
    let real_values = []
    let remain = 100
    for (i=0; i< values.length - 1; i++){
        let val = values[i] * remain / 100
        remain = remain - val
        real_values.push(Math.round(val))
    }
    real_values.push(Math.round(remain))
    for (i=0; i< real_values.length; i++){
        let idx = ids[i];
        let val = real_values[i]
        $(`#${prefix}span-value-for-` + idx).html(val + ' %')
        $(`#${prefix}slider-weights-`+idx).removeAttr('disabled')
    }
    $(`#${prefix}slider-weights-`+ids[ids.length - 1]).attr('disabled', '')
}
