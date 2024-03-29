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

 var update_charts_fields = function(refresh){
    var context = get_selected_charts_values()
    let target = 'country_charts'
    send_update_request(context, target, refresh)
}

var update_indexes_order = function(refresh, side){
    var w = get_indexes_weights(side);
    let target;
    if (side == "startup"){
        target = "startup-indexes-order"
    } else {
        target = "indexes-order"
    }
    after_refresh = ()=>{
    update_indexes_weights(side)
    }
    send_update_request(w, target, refresh, after_refresh)

}

var update_company_indexes_order = function(refresh){
    let w = get_indexes_weights("company", true);
    let length = w['ids'].length;
    let hidden_length = w['hidden_ids'].length;
    let ids = w['ids'].concat(w['hidden_ids'])
    let names = w['names'].concat(w['hidden_names'])
    let values = w['values'].concat(w['hidden_values'])
    let chosen = Array.apply(null, Array(length + hidden_length)).map(function(i, j){
                                                        if (j<length){return true}; return false})
    let data = {ids, names, values, chosen}
    send_update_request(data, 'company-indexes-order', refresh)
}

var update_startup_filters = function(refresh){
    var data = startup_filter_values()
    target = "startup-filters"
    send_update_request(data, target, refresh)
}

var  target_view = function(target_view){
    var target = "target-view";
    send_update_request({"target_view": target_view}, target, true)

}