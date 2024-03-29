function startup_filter_values() {
    var is_impact = $('#is-impact')[0].checked;
    var is_innovation = $('#is-innovation')[0].checked;
    var is_awarded = $('#is-awarded')[0].checked;
    var raised_funds = $('#already-raised-funds')[0].checked;
    var start_creation_date = $('#creation-date-from-select')[0].value;
    var end_creation_date = $('#creation-date-to-select')[0].value;
    var start_year_options = $('#creation-date-from-select option');
    var end_year_options = $('#creation-date-to-select option');
    var start = {};
    var end = {};
    for (i=0; i<start_year_options.length; i++){
        let option = start_year_options[i];
        if (option.value != ""){
            start[option.value] = option.selected;}
    }
    for (i=0; i<end_year_options.length; i++){
        let option = end_year_options[i];
         if (option.value != ""){
            end[option.value] = option.selected;
            }
    }
    let sectors = $('#startup-sectors option')
    let selected_sectors = {};
    for (i=0; i<sectors.length; i++){
        let sector = sectors[i];
        selected_sectors[sector.value] = sector.selected
    }
    return {
        "is_impact": is_impact,
        "is_innovation": is_innovation,
        "is_awarded": is_awarded,
        "already_raised_funds": raised_funds,
        "creation_date_range": [start_creation_date, end_creation_date],
        "sectors": selected_sectors,
        "creation_years_range": {"start": start, "end": end}
    }
}

function set_startup_filter_values(values) {
    $('#is-impact')[0].checked = values["is_impact"];
    $('#is-innovation')[0].checked = values["is_innovation"];
    $('#is-awarded')[0].checked = values["is_awarded"];
    $('#already-raised-funds')[0].checked = values["already_raised_funds"];
    $('#foundation-date')[0].value = values["years_since_foundation"];
}

function get_indexes_weights(side, all_values) {
//    all_values ,bool, include the non selected filters too
    let prefix = ""
    if (side == "startup") {
        prefix = "startup-"
    }
    else if (side == 'company'){
        prefix = 'company-'
    }
    var els = $(`#desired-${prefix}order-sortable>li`)
    let l = []
    var ids = []
    var names = []
    var hidden_l = []
    var hidden_ids = []
    var hidden_names = []
    for (i = 0; i < els.length; i++) {
        let name = $(els[i]).attr('refered-name')
         let refered_to = $(els[i]).attr('refers-to');
          let slider_value = $(`#${prefix}slider-weights-` + refered_to)[0].value
          let id ;
            if (side != "company"){
            id = parseInt(refered_to)}
            else {
            id = refered_to
            }
            let value = parseInt(slider_value)
        if ($(els[i]).css('display') == "block") {
            names.push(name)
            ids.push(id)
            l.push(value)
        } else if (all_values){
            hidden_names.push(name)
            hidden_ids.push(id)
            hidden_l.push(value)

       }
    }
    ret = { "ids": ids, "values": l, 'names': names}
    if (all_values){
        ret['hidden_ids'] = hidden_ids;
        ret['hidden_values'] = hidden_l;
        ret['hidden_names'] = hidden_names;
    }
    return ret
}

function get_selected_charts_values() {
    var include_charts = $('#include-charts input');
    var l = [];
    var r;
    var context = {}
    for (var i = 0; i < include_charts.length; i++) {
        if (include_charts[i].type == "checkbox") {
            r = $(include_charts[i])
            context[parseInt(r.attr('value'))] = { "name": r.attr('name'), 'checked': include_charts[i].checked }
        } else if (include_charts[i].type == "range") {
            r = $(include_charts[i])
            year_min = parseInt(include_charts[i].value)
            context[parseInt(r.attr('refers-to'))]['range'] = [year_min, 2020]
        }
    };
    var char_type = $('#include-charts select');
    for (var i = 0; i < char_type.length; i++) {
        r = $(char_type[i]);
        context[parseInt(r.attr('refers-to'))]['type'] = char_type[i].value
    }
    return context
}