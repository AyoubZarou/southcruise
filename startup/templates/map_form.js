      window.onload = function () {
        var format_name = function(name){
         let l = name.split('_');
         l = l.map((name) => name.charAt(0).toUpperCase() + name.substring(1))
         return l.join(' ');
        }
        // Create canvas and define attributes shared by all paths.
        var h = window.innerHeight;
        var w = window.innerWidth;
        var R = Raphael("container");
        transform_x = 0.7 / 750 * Math.min(w, h)

        R.setViewBox(0,0,w,h,true);
        R.canvas.setAttribute('preserveAspectRatio', 'none');
        var svg = document.querySelector("svg");
        svg.removeAttribute("width");
        svg.removeAttribute("height");
          attr = {
          "stroke": "#fff",
          "stroke-miterlimit": "4",
          "stroke-width": "0.1",
          "transform": "s" + transform_x+"," + transform_x+",400,60" // Scales the path to a useful size.
        };
        // Define map object.
        var africaMap = {};
        var countries_abbr = {{country_name|safe}};
        var countries_colors = {{colors|safe}}
        for (var nation in africaPaths) {
          // Draw a path, then apply attributes to it.
          africaMap[nation] = R.path(africaPaths[nation]).attr(attr);
          africaMap[nation].attr('href', "{% url 'country_view' %}" + "?country=" + nation)
          africaMap[nation].attr('title', countries_abbr[nation]);
          africaMap[nation].attr('fill', countries_colors[nation]);
          // Name the internal Raphael id after the africaPaths property name.
          africaMap[nation].id = nation;
          // Name the element id after the africaPaths property name.
          africaMap[nation].node.id = nation;
           // africaMap[nation][0].onclick = function(){console.log}
          africaMap[nation][0].onmouseover = function(){
            console.log(format_name(this.id));
          }
        }
      };