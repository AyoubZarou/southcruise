function startup_filter_values(){
    var is_impact = $('#is-impact')[0].checked;
    var is_innovation = $('#is-innovation')[0].checked;
    var is_awarded = $('#is-awarded')[0].checked;
    var raised_funds = $('#already-raised-funds')[0].checked;
    var years_since_foundation = parseInt($('#foundation-date')[0].value)
    return {"is_impact": is_impact, "is_innovation": is_innovation,
            "is_awarded": is_awarded, "already_raised_funds": raised_funds,
             "years_since_foundation": years_since_foundation}
}

function set_startup_filter_values(values){
   $('#is-impact')[0].checked = values["is_impact"];
   $('#is-innovation')[0].checked = values["is_innovation"];
   $('#is-awarded')[0].checked = values["is_awarded"];
   $('#already-raised-funds')[0].checked = values["already_raised_funds"];
   $('#foundation-date')[0].value = values["years_since_foundation"];
}

function get_country_indexes_weights(){
    var els = $('#desired-order-sortable>li')
    let l = {}
    let ids = []
    let values = []
    for (i=0; i<els.length; i++){
        if ($(els[i]).css('display')  == "block"){
            let refered_to = $(els[i]).attr('refers-to');
            let slider_value = $('#slider-weights-'+refered_to)[0].value
            ids.push(parseInt(refered_to))
            values.push(parseInt(slider_value))
            l[parseInt(refered_to)] = parseInt(slider_value)
        }
    }
    data = {"id": ids, 'weights': values}
    return data;
}

function get_startup_indexes_weights(side){
    let prefix = ""
    if (side == "startup"){
        prefix = "startup-"
    }
    console.log(side);
    var els = $(`#desired-${prefix}order-sortable>li`)
    let l = []
    var ids = []
    for (i=0; i<els.length; i++){
        if ($(els[i]).css('display')  == "block"){
            let refered_to = $(els[i]).attr('refers-to');
            let slider_value = $(`#${prefix}slider-weights-`+refered_to)[0].value
            ids.push(parseInt(refered_to))
            l.push(parseInt(slider_value))
        }
    }
    return {"ids": ids, "values": l}
}

