var keyword = null;
var markers = [];
var map = null;
var xmlhttp = new XMLHttpRequest();

var bludMarker = "http://maps.google.com/mapfiles/ms/icons/blue-dot.png";
var redMarker = "http://maps.google.com/mapfiles/ms/icons/red-dot.png";
var yellowMarker = "http://maps.google.com/mapfiles/ms/icons/yellow-dot.png";


function attachMessage(marker, meg) {
	var infowindow = new google.maps.InfoWindow({
		content: meg
	});

	marker.addListener('click', function() {
		infowindow.open(map, marker);
	});
}

/*
 * Listen to the http request 
 */
xmlhttp.onreadystatechange = function() {
	if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
		// clear the existing markers
		while (markers.length != 0)
			markers.pop().setMap(null);
		// add new markers
		var tweets = JSON.parse(xmlhttp.responseText)['tweets']; 
		for (var i = 0; i < tweets.length; ++i) {
			var tweet = tweets[i];
			var loc = new google.maps.LatLng(parseInt(tweet["coordinates"][1]), parseInt(tweet["coordinates"][0]));
			var icon = null;
			if (tweet['sen'] == 'positive')
				icon = redMarker;
			else if (tweet['sen'] == 'negative')
				icon = yellowMarker;
			else
				icon = bludMarker;
			var text = tweet['text'];
			var marker = new google.maps.Marker({
				icon: icon,
				position: loc,
				map: map,
				title: text
			});
			marker.setMap(map);
			markers.push(marker);
			attachMessage(marker, text);
		}
	}
};

function initMap() {

	/* 
	 * Initilize the Google Map
	 */
	map = new google.maps.Map(document.getElementById('map'), {
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
	sendHttp();
});

function sendHttp() {

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

	/*
	 * HTTP request sent
	 */
	xmlhttp.open("POST", "/global?kw=" + keyword + "&start=" + beginDate + "&end=" + endDate, true);
	xmlhttp.send();
}



