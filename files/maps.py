request  = container.REQUEST
REQUEST  = context.REQUEST
RESPONSE = request.RESPONSE

print context.standard_html_header(context, request)

print '''
  <script type="text/javascript">
  function loadMap(x, y) {

    if(GBrowserIsCompatible()) {

      var map = new GMap2(document.getElementById("map"));
      
      map.addMapType(G_PHYSICAL_MAP);
      
      map.addControl(new GSmallMapControl());
      map.addControl(new GHierarchicalMapTypeControl());
      
      map.addControl(new GScaleControl());

      map.setCenter(new GLatLng(x, y), 8);

      map.setMapType(G_PHYSICAL_MAP);

      var point = new GLatLng(x, y);
//    map.addOverlay(new GMarker(point));

      // Creates a marker at the given point with the given number label
//    function createMarker(point) {
//      var marker = new GMarker(point);
//        GEvent.addListener(marker, "click", function() {
//          marker.openInfoWindowHtml("UC Merced");
//        });
//      return marker;
//    }

//    map.addOverlay(createMarker(point));
    }
  }
  </script>
'''

x =   37.366
y = -120.422

print '<body onload="loadMap(' + str(x) + ',' + str(y) + ')" onunload="GUnload()">'

print '<div id="map"></div>'

print '</body>'

print context.standard_html_footer(context, request)

return printed
