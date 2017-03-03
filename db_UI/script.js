/*This function will communicate with server to print out data table*/
function showTable(channel){
	var datab = channel.value;
	var chann =  channel.id;
	var xmlhttp;
	$("#mapping").hide();//hides google map
	/*ajax code --> client is able to commuincate with server*/
	if (window.XMLHttpRequest) {// code for newer browsers			
		xmlhttp = new XMLHttpRequest();
	} else {// code for IE6, IE5
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	/*Once its done retrieving the data from file specified below*/
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			document.getElementById("output").innerHTML = xmlhttp.responseText;//display result on browser
		}
	}
	/*open and send new data inputs to php file*/
	xmlhttp.open("GET","FetchTable.php?data="+datab+"&ch="+chann,true);//pass variables to php file
	xmlhttp.send();
}

/* Need to clear the page before loading new info/text */
function clearText(){
	$("#output").empty();
}

function doWait() {} 

/* calls on the mapping html code in index.php*/
function mapClick(){
	var test= "Modified";
	console.log(test);
	//computes <div mapping>
	$("#mapping").show();
	clearText();
}


var customLabel = {
	tester: {
	  label: 'D1'
	}
};

/* creates google map and places markers on it*/
function initMap() {
	var map = new google.maps.Map(document.getElementById("map"), {
	  center: new google.maps.LatLng(36.999783, -122.063565),
	  zoom: 16
	});				
	 var infoWindow = new google.maps.InfoWindow;			
	//create markers
	// Change this depending on the name of your PHP or XML file
	loadFile('createMarkers.php', function(data) {
	var xml = data.responseXML;//should have the array of markers created from php file
	var markers = xml.documentElement.getElementsByTagName("marker");
		Array.prototype.forEach.call(markers, function(markerElem) {
		  var name = markerElem.getAttribute("name");
		  var pts = markerElem.getAttribute("pts");
		  var type = markerElem.getAttribute("type");
		  var point = new google.maps.LatLng(
			  parseFloat(markerElem.getAttribute("lat")),
			  parseFloat(markerElem.getAttribute("lng"))
		  );

		  /* Create content for marker on click */
		  var infowincontent = document.createElement("div");
		    infowincontent.className = "markerText";
		    var strong = document.createElement("strong");
		    strong.textContent = name;
		    infowincontent.appendChild(strong);
		    infowincontent.appendChild(document.createElement("br"));
			var ptInt = document.createElement("text");
			ptInt.textContent = pts;
			infowincontent.appendChild(ptInt);
			infowincontent.appendChild(document.createElement("br"));
			var position = document.createElement("text");
			position.textContent = point;
			infowincontent.appendChild(position);
		  /* end of marker content*/
			
			var icon = customLabel[type] || {};
			
			var marker = new google.maps.Marker({
				map: map,
				position: point,
				label: icon.label
			});
			
			marker.addListener("click", function() {
				infoWindow.setContent(infowincontent);
				infoWindow.open(map, marker);
			});
		});
	});			
	}
	
	/* helper function to load xml file and return markers*/
function loadFile(filename,callback) {
	var request;
	/*ajax code --> client is able to commuincate with server*/
	if(window.ActiveXObject){
		request = new ActiveXObject('Microsoft.XMLHTTP')
	}else{
	 request = new XMLHttpRequest;
	}
	/*Once its done retrieving the data from file specified below*/
	request.onreadystatechange = function() {
		if (request.readyState == 4 && request.status == 200) {
			request.onreadystatechange = doWait;
			//returns functions output, depending on the file indicated
			callback(request, request.status);
		}
	};
	request.open('GET', filename, true);
	request.send(null);
}

/* function that will reload the marker points and google maps*/
//added button to refresh, but will need to check automaticakky
function Reload(){
	clearText();
	var test= "Reload";
	console.log(test);
	$("#mapping").show();
	clearText();
}
