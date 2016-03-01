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

var keyword = null;

var xmlhttp = new XMLHttpRequest();
var url = "http://127.0.0.1:5000/user/";
xmlhttp.onreadystatechange = function() {
	if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
		if (keyword == null)
			alert("Please pick a keyword");
		else
			alert(xmlhttp.responseText);
	}
};

$(".dropdown").on("click", "li a", function() {
	keyword = $(this).text();
	$(".dropdown-toggle").html(keyword + ' <span class="caret"></span>');
}); 

$('#dateselector1').datepicker("clearDates");
$('#dateselector2').datepicker("clearDates");

$("button").on("click", function() {
	var beginDate = document.getElementById("dateselector1").value.split("/").join("-");
	var endDate = document.getElementById("dateselector2").value.split("/").join("-");
	xmlhttp.open("POST", url + "keyword=" + keyword + "&beginDate=" + beginDate + "&endDate=" + endDate, true);
	xmlhttp.send();
});



