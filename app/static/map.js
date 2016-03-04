var keyword = null;
var lat = null;
var lng = null;
var heatmap = null;
var marker = null;

var xmlhttp = new XMLHttpRequest();

/*
 * Listen to the http request 
 */
xmlhttp.onreadystatechange = function() {
	if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
		var text = JSON.parse(xmlhttp.responseText); 
		if (text['pattern'] == "global") {
			var locs = text['tweets'];
			var arr = heatmap.getData();
			for (var i = 0; i < locs.length; ++i) {
			    var loc = new google.maps.LatLng(parseInt(locs[i][1]), parseInt(locs[i][0]));
				arr.push(loc);
			}
		} else {
			var tweets = text['tweets'];
			console.log(tweets);
		}
	}
};

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
		sendHttp("local");
  	});
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
	sendHttp("global");
});

function sendHttp(pattern) {

	/*
	 * Remind the user to pick a location and a keyword
	 */
	if (keyword == null) {
		alert("Please pick a keyword");
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

	if (pattern == "global") {
		/*
		 * Clear the previous data
		 */
		var arr = heatmap.getData();
		while (arr.length > 0)
			arr.pop();

		/*
		 * HTTP request sent
		 */
		xmlhttp.open("POST", "/global?kw=" + keyword + "&start=" + beginDate + "&end=" + endDate, true);
		xmlhttp.send();

	} else {
		xmlhttp.open("POST", "/local?kw=" + keyword + "&start=" + beginDate + "&end=" + endDate + "&lat=" + lat + "&lon=" + lng, true);
		xmlhttp.send();
	}
}



