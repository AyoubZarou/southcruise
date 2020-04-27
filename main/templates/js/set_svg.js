$('#minimizer-icon-charts').css('display', 'none');
// if the value is nan (np.nan) set it to undefined so it would be parsed safely with javascript engine
var nan = undefined;
var codes = {{codes | safe}};
// add color, name, tooltip for each country, with adding a select possibility
for (var key in codes) {
    $("svg #" + key).attr('title', codes[key]['name'])
    $("svg #" + key).css('fill', codes[key]['color'])
    $("svg #" + key + ' path').css('fill', codes[key]['color']) // sometimes the country has several path parts
    $("svg #" + key).tooltipster();
    $("svg #" + key).on('click', function() {
        var cls = $(this).attr('class');
        var id = $(this)[0].id;
        if (cls === "" | cls === undefined) {
            $(this).attr('class', 'selected-path');
            $('#selected-country-' + id).css('display', 'block');
        } else {
            $(this).attr('class', '');
            $('#selected-country-' + id).css('display', 'none');
        }
    })
}
var ids = [];
// get selected paths
let sp = window.location.href.split('=');
if (sp.length >= 2) {
    ids = sp[1].split(',')
}
// highlight selected paths
for (var i = 0; i < ids.length; i++) {
    $("svg #" + ids[i]).attr('class', 'selected-path');
    $('#selected-country-' + ids[i]).css('display', 'block');
}