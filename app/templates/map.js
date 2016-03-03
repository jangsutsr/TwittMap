var keyword = null;
var lat = null;
var lng = null;
var heatmap = null;
var marker = null;

var xmlhttp = new XMLHttpRequest();
var url = "http://127.0.0.1:5000/user/";

/*
 * Listen to the http request 
 */
xmlhttp.onreadystatechange = function() {
	if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
		alert(xmlhttp.responseText);
	}
};

// function drawHeatMap(locs) {
// 	for (int i = 0; i < locs.length; ++i)
// 		arr.push(locs);
// }

function initMap() {

	/* 
	 * Initilize the Google Map
	 */
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

	/* 
	 * Initilize the HeatMap
	 */
	heatmap = new google.maps.visualization.HeatmapLayer({
		data: [],
		map: map,
		radius: 18
	});

	/* 
	 * On click, recored the location and place a marker
	 */
	map.addListener('click', function(e) {
		lat = e.latLng.lat().toString();
		lng = e.latLng.lng().toString();
		
		if (marker != null)
			marker.setMap(null);
		marker = new google.maps.Marker({
			position: e.latLng,
			map: map
		});
		marker.setMap(map);
  });

	// loc = new google.maps.LatLng(e.latLng.lat(), e.latLng.lng());
	// var weight = Math.floor((Math.random() * 10) + 1);

	// var arr = heatmap.getData();

	// for (i = 0; i < weight; i++)
	//   	arr.push(loc);
	// });
}

/* 
 * Change the keyword of dropdown
 */
$(".dropdown").on("click", "li a", function() {
	keyword = $(this).text();
	$(".dropdown-toggle").html(keyword + ' <span class="caret"></span>');
}); 


/* 
 * Initilize two datetimepickers
 */
$('#datetimepicker1').datetimepicker();
$('#datetimepicker2').datetimepicker();

/*
 * When clicking the sumbit button, send a POST request
 */
$("button").on("click", function() {

	/*
	 * Clear the previous data
	 */
	var arr = heatmap.getData();
	while (arr.length > 0)
		arr.pop();

	/*
	 * Remind the user to pick a location and a keyword
	 */
	if (keyword == null) {
		alert("Please pick a keyword");
		return;
	}
	if (lat == null || lng == null) {
		alert("Please pick a location");
		return;
	}

	/* 
	 * Get the begin date and end date 
	 */
	var beginDate = $("#datetimepicker1 input").val().split("/").join("-").split(" ").join("+");
	var endDate = $("#datetimepicker2 input").val().split("/").join("-").split(" ").join("+");
	if (beginDate == "" || endDate == "") {
		alert("Please pick the begin date and end date");
		return;
	}

	/*
	 * HTTP request sent
	 */
	xmlhttp.open("POST", url + "?kw=" + keyword + "&start=" + beginDate + "&end=" + endDate + "&lat=" + lat + "&lon=" + lng, true);
	xmlhttp.send();
});


