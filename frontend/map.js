function initMap() {

  var map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 0, lng: 0},
    zoom: 3,
    styles: [{
      featureType: 'poi',
      stylers: [{ visibility: 'off' }]  // Turn off points of interest.
    }, {
      featureType: 'transit.station',
      stylers: [{ visibility: 'off' }]  // Turn off bus stations, train stations, etc.
    }],
    disableDoubleClickZoom: true
  });

  var heatmap = new google.maps.visualization.HeatmapLayer({
    data: [],
    map: map,
    radius: 18
  });

  map.addListener('click', function(e) {
    var loc = new google.maps.LatLng(e.latLng.lat(), e.latLng.lng());
    var weight = Math.floor((Math.random() * 10) + 1);

    var arr = heatmap.getData();

    for (i = 0; i < weight; i++)
      arr.push(loc);
  });
}

$("#SelectKeyWord").on("click", "li a", function() {
    var platform = $(this).text();
    alert(platform);
});    