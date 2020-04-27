{% include 'js/retrieve_filter_values.js' %}


// update the displayed year for each country chart when the range is changed (on the country filters)
function update_year_since(that){
    let value = $(that).attr('value');
    let refers_to = $(that).attr('refers-to');
    to_change = $('#year-since-' + refers_to)
    to_change.html(that.value);
}

// remove an indicator from order for performance indexes order
function remove_from_order(that, side){
    if (side == "startup"){
         // for startup indicators (number of employees, ...)
          let refers_to  = $(that).attr('refers-to');
        $('#desired-startup-order-' + refers_to).css('display', 'none')
    $('#excluded-startup-order-' + refers_to).css('display', 'block')
    } else {
         // for country indicators (GDP, GDP per capita ....)
    let refers_to  = $(that).attr('refers-to');
    $('#desired-order-' + refers_to).css('display', 'none')
    $('#excluded-order-' + refers_to).css('display', 'block')
    update_indexes_weights()}
}
// add an indcator to the order
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

// update shown indicators weights depending on the order and how far the cursor is pushed
// the convention is that, if for example we have the first cursor at 50% the second at 40% and the third at 100 % and
// so on, the first weight would be 100/100 * 50% = 50%, the second wound be (100 - 50)/100 * 40 % = 20 % and the
// third would be (100 - 50 - 20)/100 * 100% = 30%, and the rest would be at 0
function update_shown_indexes_weights(that, side){
     let prefix = ""
    if (side == "startup"){
        prefix = "startup-"
    }
    let weights = get_indexes_weights(side)
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
    // disable the last cursor as the last value is the remain, so the cursor doesn't add any value
    $(`#${prefix}slider-weights-`+ids[ids.length - 1]).attr('disabled', '')
}
