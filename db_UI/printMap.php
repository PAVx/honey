<!DOCTYPE html>
<html lang="es">
<head>

</head>

<body>
	<h3>My Google Maps</h3>
	<div id="map" style="width: 400px; height: 300px;"> </div>
	<script type="text/javascript"> 
		var customLabel = {
			tester: {
			  label: 'D1'
			  
			}
		};
		
		function initMap() {
			var map = new google.maps.Map(document.getElementById('map'), {
			  center: new google.maps.LatLng(36.999783, -122.063565),
			  zoom: 12
			});
			
			var infoWindow = new google.maps.InfoWindow;
			//create markers
			
			// Change this depending on the name of your PHP or XML file
			downloadUrl('createMarkers.php', function(data) {
			var xml = data.responseXML;
			var markers = xml.documentElement.getElementsByTagName('marker');
				Array.prototype.forEach.call(markers, function(markerElem) {
				  var name = markerElem.getAttribute('name');
				  var pts = markerElem.getAttribute('pts');
				  var type = markerElem.getAttribute('type');
				  var point = new google.maps.LatLng(
					  parseFloat(markerElem.getAttribute('lat')),
					  parseFloat(markerElem.getAttribute('lng'))
				  );

				  var infowincontent = document.createElement('div');
				  var strong = document.createElement('strong');
				  strong.textContent = name
				  infowincontent.appendChild(strong);
				  infowincontent.appendChild(document.createElement('br'));

					var text = document.createElement('text');
					text.textContent = pts
					infowincontent.appendChild(text);
					var icon = customLabel[type] || {};
					var marker = new google.maps.Marker({
						map: map,
						position: point,
						label: icon.label
					});
					marker.addListener('click', function() {
						infoWindow.setContent(infowincontent);
						infoWindow.open(map, marker);
					});
				});
			});			
		// Extend markerBounds with each random point.
		}
		
		function doNothing() {}
	</script>

	<script async defer
		src="https://maps.googleapis.com/maps/api/js?key=AIzaSyC_HcJ7YyXFD0fVavbN0DuBN7_N2HnHvao&callback=initMap">
	</script>

	
	
		
</body>
</html>