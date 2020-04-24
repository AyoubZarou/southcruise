var update_countries = function(){
            let ch = $('#selected-countries').children();
            let l = []
            for (var c=0; c<ch.length; c++){
                if ($(ch[c]).css('display') == 'block'){
                    l.push($(ch[c]).attr('refers-to'));
                }
            }
            if (l.length >= 1){
            window.location.href = window.location.href.split('?')[0] + '?country=' + l.join(',')}
            else{
            window.location.href = window.location.href.split('?')[0];
            }
        }
var delete_country_from_selection = function(that){
        var key = $(that).attr('refers-to');
        $("svg #" + key).attr('class', '');
        $('#selected-country-' + key).css('display', 'none')


      }

var show_global_startup_detail = function(that){
        let referee = $(that).attr('refers-to');
       if ($('#' + referee).css('display') == 'block'){
            $('#' + referee).css('display', 'none');
            $('#grid-startup-detail').attr('class', 'col-12');
            $('#startup-detailed-detail').css('display', 'none');
      }
      else {
      $('#startup-detailed-detail .startup-detail-card').css('display', 'none');
        $('#' + referee).css('display', 'block');
             $('#grid-startup-detail').attr('class', 'col-6');
             $('#startup-detailed-detail').css('class', 'col-5');
            $('#startup-detailed-detail').css('display', 'block');
        }
      }
var maximize_minimize_charts = function(that){
      let maximized = $('#chart-maximize').attr("maximized")
      if (maximized=="false"){
            $('#africa-svg-div').css('display', 'none');
            $('#charts-div').removeClass('col-md-8');
            $('#charts-div').addClass('col-md-12');
            $('#chart-maximize').attr("maximized", 'true');
            $('#maximizer-icon-charts').css('display', 'none');
            $('#minimizer-icon-charts').css('display', 'block');
        }
        else {
            $('#africa-svg-div').css('display', 'block');
            $('#charts-div').addClass('col-md-8');
            $('#charts-div').removeClass('col-md-12');
            $('#chart-maximize').attr("maximized", "false");
            $('#maximizer-icon-charts').css('display', 'block');
            $('#minimizer-icon-charts').css('display', 'none');
        }
      }