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
    c['data'] = JSON.stringify(context);
    c['target'] = 'country_charts'
   c['csrfmiddlewaretoken'] = '{{csrf_token}}'
   console.log(context)
   $.ajax({
   url: "{% url 'update_session' %}",
    method: "POST",
    data: c,
    success:(response)=>{
       if (refresh){
        document.location.href = document.location.href;
       }
    }})
}

function update_year_since(that){
    let value = $(that).attr('value');
    let refers_to = $(that).attr('refers-to');
    to_change = $('#year-since-' + refers_to)
    to_change.html(that.value);
}
function remove_from_order(that){
    let refers_to  = $(that).attr('refers-to');
    $('#desired-order-' + refers_to).css('display', 'none')
    $('#excluded-order-' + refers_to).css('display', 'block')
}
function add_to_order(that){
    let refers_to  = $(that).attr('refers-to');
    $('#desired-order-' + refers_to).css('display', 'block')
    $('#excluded-order-' + refers_to).css('display', 'none')
}

var update_indexes_order = function(refresh){
    var els = $('#desired-order-sortable li');
    var order = [];
    console.log(els)
    for (i=0; i<els.length; i++){
        let el = $(els[i])
         if (el.css('display') !== "none"){
            order.push(parseInt(el.attr('refers-to')))
        }
    }
    var context = {}
    context['data'] = JSON.stringify(order);
    context['target'] = "indexes-order"
    context['csrfmiddlewaretoken'] = '{{csrf_token}}'
   $.ajax({
   url: "{% url 'update_session' %}",
    method: "POST",
    data: context,
    success:(response)=>{
       if (refresh){
        document.location.href = document.location.href;
       }
    }})

}

 $( function(){
    $( "#desired-order-sortable" ).sortable();
  } );
