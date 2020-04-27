// updated selected countries (called when clicked on refresh button with new countries selected)
var update_countries = function() {
    let ch = $('#selected-countries').children();
    let l = []
    for (var c = 0; c < ch.length; c++) {
        if ($(ch[c]).css('display') == 'block') {
            l.push($(ch[c]).attr('refers-to'));
        }
    }
    // refresh with new url, so the data would be served from the backend
    if (l.length >= 1) {
        window.location.href = window.location.href.split('?')[0] + '?country=' + l.join(',')
    } else {
        window.location.href = window.location.href.split('?')[0];
    }
}
// apply style to unselected countries
var delete_country_from_selection = function(that) {
    var key = $(that).attr('refers-to');
    $("svg #" + key).attr('class', '');
    $('#selected-country-' + key).css('display', 'none')
}
// show details about a startup when clicked upon on the table, or hide it if it's already shown
var show_global_instrument_detail = function(that, side) {
    if (side == undefined){
            side = 'startup';
    }
    console.log(side)
    let refered_to = $(that).attr('refers-to');
    if ($('#' + refered_to).css('display') == 'block') {
        $('#' + refered_to).css('display', 'none');
        $(`#grid-${side}-detail`).attr('class', 'col-12');
        $(`#${side}-detailed-detail`).css('display', 'none');
    } else {
        $(`#${side}-detailed-detail .${side}-detail-card`).css('display', 'none');
        $('#' + refered_to).css('display', 'block');
        $(`#grid-${side}-detail`).attr('class', 'col-6');
        $(`#${side}-detailed-detail`).css('class', 'col-5');
        $(`#${side}-detailed-detail`).css('display', 'block');
    }
}

var show_global_company_detail = function(that) {
    let refered_to = $(that).attr('refers-to');
    if ($('#' + refered_to).css('display') == 'block') {
        $('#' + refered_to).css('display', 'none');
        $('#grid-company-detail').attr('class', 'col-12');
        $('#company-detailed-detail').css('display', 'none');
    } else {
        $('#company-detailed-detail .company-detail-card').css('display', 'none');
        $('#' + refered_to).css('display', 'block');
        $('#grid-company-detail').attr('class', 'col-6');
        $('#company-detailed-detail').css('class', 'col-5');
        $('#company-detailed-detail').css('display', 'block');
    }
}
// called when charts are being minimized or maximized (it hides the map and makes the charts full screen)
var maximize_minimize_charts = function(that) {
    let maximized = $('#chart-maximize').attr("maximized")
    if (maximized == "false") {
        $('#africa-svg-div').css('display', 'none');
        $('#charts-div').removeClass('col-md-8');
        $('#charts-div').addClass('col-md-12');
        $('#chart-maximize').attr("maximized", 'true');
        $('#maximizer-icon-charts').css('display', 'none');
        $('#minimizer-icon-charts').css('display', 'block');
    } else {
        $('#africa-svg-div').css('display', 'block');
        $('#charts-div').addClass('col-md-8');
        $('#charts-div').removeClass('col-md-12');
        $('#chart-maximize').attr("maximized", "false");
        $('#maximizer-icon-charts').css('display', 'block');
        $('#minimizer-icon-charts').css('display', 'none');
    }
}