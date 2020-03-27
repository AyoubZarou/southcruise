      window.onload = function () {

         var codes = {{codes|safe}};
         for (var key in codes ){
          $("svg #" + key).attr('title', codes[key]['name'])
          $("svg #" + key).css('fill', codes[key]['color'])
          $("svg #" + key + ' path').css('fill', codes[key]['color'])

          $("svg #" + key).tooltipster();
          $("svg #" + key).on('click', function(){
          var cls = $(this).attr('class');
          console.log(cls);
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
      };

     var update_countries = function(){
            let ch = $('#selected-countries').children();
            let l = []
            for (var c=0; c<ch.length; c++){
                if ($(ch[c]).css('display') == 'block'){
                console.log($(ch[c]))
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
             $('#grid-startup-detail').attr('class', 'col-7');
             $('#startup-detailed-detail').css('class', 'col-5');
            $('#startup-detailed-detail').css('display', 'block');
        }
      }
      var maximize_minimize_charts = function(){
      let maximized = $('#chart-maximize').attr("maximized")
      if (maximized=="false"){
        $('#africa-svg-div').css('display', 'none');
        $('#charts-div').removeClass('col-md-8');
        $('#charts-div').addClass('col-md-12');
        $('#chart-maximize').attr("maximized", 'true');
        }
        else {
        $('#africa-svg-div').css('display', 'block');
        $('#charts-div').addClass('col-md-8');
        $('#charts-div').removeClass('col-md-12');
        $('#chart-maximize').attr("maximized", "false")
        }
      }