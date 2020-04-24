 $('#minimizer-icon-charts').css('display', 'none');
 var nan = undefined;
 var codes = {{codes|safe}};
 for (var key in codes ){
      $("svg #" + key).attr('title', codes[key]['name'])
      $("svg #" + key).css('fill', codes[key]['color'])
      $("svg #" + key + ' path').css('fill', codes[key]['color'])

      $("svg #" + key).tooltipster();
      $("svg #" + key).on('click', function(){
      var cls = $(this).attr('class');
      var id = $(this)[0].id;

      if (cls === "" | cls === undefined){
      $(this).attr('class', 'selected-path');
       $('#selected-country-' + id).css('display', 'block');
     }else{
        $(this).attr('class', '');
        $('#selected-country-' + id).css('display', 'none');
     }
     })
}
var ids = [];
let sp = window.location.href.split('=');
if (sp.length >= 2){
    ids = sp[1].split(',')
}
for (var i=0; i<ids.length; i++){
    $("svg #" + ids[i]).attr('class', 'selected-path');
    $('#selected-country-' + ids[i]).css('display', 'block');
}