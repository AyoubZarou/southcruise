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
    console.log(c['data'])
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
