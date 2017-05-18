/*This function will communicate with server to print out data table*/
var visualData = 0;

function showTable(channel){
	visualData = 1; //set flag
	var datab = channel.value;
	var chann =  channel.id;
	var xmlhttp;
	$("#mapping").hide();//removes google map
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
			visualizeData();
		}
	}
	/*open and send new data inputs to php file*/
	xmlhttp.open("GET","FetchTable.php?data="+datab+"&ch="+chann,true);//pass variables to php file
	xmlhttp.send();
}

var vis_data = new Array();
vis_data = vis_getdata();
function visualizeData() {	
    //Space the graphs will occupy (originally width: 980, height: 500)
    var svg_width = 653;
    var svg_height = 333;

    //Specify how much padding on each side of the SVG (to look cleaner)
    var margin = {top: 20, right: 20, bottom: 20, left: 40};
    var width = svg_width - margin.left - margin.right;
    var height = svg_height - margin.top - margin.bottom;

    var count;
    var n = 40;
    var data = d3.map(vis_data);

        //Create the SVG element in which the graph will be placed.
        var svg = d3.select("#output").append("svg")
            .attr("width", width - margin.left - margin.right)
            .attr("height", height - margin.top - margin.bottom)
			.attr("class","visualData")
        g = svg.append("g").attr("transform", "translate(" + margin.left + "," + (margin.top) + ")");

        //Set the scale to linear 
        var x = d3.scaleLinear()
            .domain([0, n - 1]) //values that x can be
            .range([0, width]); //maps x values to the total width of svg
        var y = d3.scaleLinear()
            .domain([0, 100]) //values that y can be
            .range([height - (2*(margin.top+margin.bottom)), 0]);

		//return scaled values of the data
        //"i" is the index of the data (time) and "d" is the associated data
        var line = d3.line()
            .x(function(d, i) { return x(i); })
            .y(function(d, i) { return y(d); });

        //Set clip region (how far the line will be drawn)
        g.append("defs").append("clipPath")
            .attr("id", "clip")
            .append("rect")
            .attr("width", width)
            .attr("height", height);

        //Add subgroup to the chart for the x axis and draw it
        g.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + (height-2*(margin.top + margin.bottom)) + ")")
            .call(d3.axisBottom(x));

        //Add subgroup to chart for the y axis and draw it
        g.append("g")
            .attr("class", "y axis")
            .call(d3.axisLeft(y)
            /*.ticks(5)*/);     
    
        //Subgroup for the actual line to be drawn    
        g.append("g")
            //draw the line in the clip path
            .attr("clip-path", "url(#clip)")
            .append("path")
            .datum(vis_data)
            .attr("class", "line")
            .attr("d", line);	
}

/* Need to clear the page before loading new info/text */

function clearText(){
	$("#output").empty();
	$("#visualData").empty();
}

function doWait() {} 

/* calls on the mapping html code in index.php*/
function mapClick(){
	var test= "Modified";
	//console.log(test);
	//computes <div mapping>
	$("#mapping").show();
	visualData = 0; //disable visual data view
	//Reload();
	clearText();
}

var customLabel = {
	tester: {
	  label: 'D1'
	}
};

/*
	var rover_lat= document.getElementById("rover").valuex;
	var rover_long= document.getElementById("rover").valuey;
	var map = new google.maps.Map(document.getElementById("map"), {
	  center: new google.maps.LatLng(rover_lat, rover_long),
	  zoom: 16
	  */
	  
/* creates google map and places markers on it*/
var rectangle;
var map;
var infoWindow;
var verify;
var stream;
var center_pos;
var flight_status;
//so we can modify the bounds later
var bounds;

function update_Bounds(n,s,e,w){
	if((!n)&(!s) &(!e) & (!w)){//sets them by default
		console.log("null");
		bounds ={ //later will get one of the drones coordinates
		  north: 37.00246766,
		  south: 36.99795295,
		  east: -122.0617625,
		  west: -122.0678076
		};
		center_pos = {lat: 36.99783, lng: -122.063565}; //pick a center loc
	} else{
		bounds = { //else assigns values to loc
		  north: n,
		  south: s,
		  east: e,
		  west: w
		};
		center_pos = {lat: n, lng: e};
	}
}
	
function check_scan(a,b){
	var x1 = a.lat();
	var x2 = b.lat();
	var y1 = a.lng();
	var y2 = b.lng();
	
	update_Bounds(x1,x2,y1,y2);
	
	if (window.XMLHttpRequest) {// code for newer browsers			
		xmlhttp = new XMLHttpRequest();
	} else {// code for IE6, IE5
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}	
	/*Once its done retrieving the data from file specified below*/
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			//update warning display
			document.getElementById("display_status").innerHTML = xmlhttp.responseText;//display result on browser
			//once we are done checking make sure to continue live stream if running
			
		}
	}
	/*open and send new data inputs to php file*/
	xmlhttp.open("GET","ScanCheck.php?x1="+x1+"&x2="+x2+"&y1="+y1+"&y2="+y2,true);//pass variables to php file
	xmlhttp.send();
}

var ne;
var sw;
var flag = 0;
var heatmap;
var num_drones = 1;
var hm_data;
var hmap_exists = false;
hm_data = new Array();
//hm_refresh(30);

function scan_Map(values) {
	console.log("scanning");//for debugging
	var id = document.getElementById(values);
	console.log(id.value);
	if (id.value == "start") {//start scanning
		id.value = "stop";
		var streamMap = document.getElementById('stream');
		if (streamMap.value == "stop") {//check if you were streaming before
			clearInterval(stream); //stop streaming
		}
		id.innerHTML = "Check";//change text for button
		flag++;
		
		if(flag > 1){
			console.log("1");
			flag = 1;
		}else{
			update_Bounds();//load default or get one of drones coord
		}
		//create new map with rectangle ---> update map by using set map
		map = new google.maps.Map(document.getElementById('map'), {
			center: center_pos,
			zoom:16,
			mapTypeId: 'hybrid'
		});

		// Define the rectangle and set its editable property to true.
		rectangle = new google.maps.Rectangle({
		  bounds: bounds,
		  editable: true,
		  draggable: true
		});
		rectangle.setMap(map);

		// Add an event listener on the rectangle.
		rectangle.addListener('bounds_changed', showNewRect);

		// Define an info window on the map.
		infoWindow = new google.maps.InfoWindow();
		console.log("fin");//for debugging		
	}
	else if(id.value == "stop"){//stop and check coordinates
        id.value = "start";
		id.innerHTML = "Scan";
		var streamMap = document.getElementById('stream');
		if (streamMap.value == "stop") {//check if you were streaming before
			stream = setInterval(Reload,1000); //continue streaming
		}
		//check if ne and sw is null, if so set up default
		check_scan(ne, sw );
   } 
}
//Toggles the heatmap on and off
function toggle_hmap() {
	hm_refresh(30);
	//Check to see if the heatmap has been initliazed already
	if(!hmap_exists) {
		//Create the heatmap if not initialized
		heatmap = new google.maps.visualization.HeatmapLayer({
        	data: hm_draw(),
        	map: map
    	});	
    	hmap_exists = true;
	}
	else {
		heatmap.setMap(heatmap.getMap() ? null : map);
	}
}

var tdata;
//Reads the database, adding any entries whose score is above threshold to the heatmap table
function hm_refresh(threshold) {
	var xmlhttp;	
	if (window.XMLHttpRequest) {// code for newer browsers			
		xmlhttp = new XMLHttpRequest();
	} else {// code for IE6, IE5
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}	
        xmlhttp.onreadystatechange = function() {
        	if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        		//Parse the returned string of DB values from the php
				tdata = xmlhttp.responseText.split(" ");
				var d_arr = tdata.slice(0, -1); 
				d_arr.forEach(function(element) {
				   	hm_data.push(parseFloat(element));
				});
		}
	}
	xmlhttp.open("GET","HeatMap.php?data=jays&n="+num_drones+"&th="+threshold,true);//pass variables to php file    
    xmlhttp.send();
}

var vdata;
function vis_getdata() {
	var xmlhttp;
	var vis_data = new Array();
	if (window.XMLHttpRequest) {// code for newer browsers			
		xmlhttp = new XMLHttpRequest();
	} else {// code for IE6, IE5
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange = function() {
		if(xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			//Parse the returned string of data values
			vdata  = xmlhttp.responseText.split(" ");
			var v_arr = vdata.slice(0, -1);
			v_arr.forEach(function(element) {
				vis_data.push(parseFloat(element));
			});
		}
	}
	//Once it works, make this more dynamic
	xmlhttp.open("GET", "visualization.php?db=jays&tbl=jay0&sen=sensor0_data&n=8");
	xmlhttp.send();
	return vis_data;
}

//uses the heatmap table to create data points for the heatmap
function hm_draw() {
    var heatmap_arr = new Array();
    var i = 0;
	do {
    	heatmap_arr.push(new google.maps.LatLng(hm_data[i], hm_data[i+1]));
    	i += 2;
	}
	while(i < hm_data.length-1);
	return heatmap_arr;
}

      // Show the new coordinates for the rectangle in an info window.

/** @this {google.maps.Rectangle} */
function showNewRect(event) {
	console.log("showrect");//for debugging
	ne = rectangle.getBounds().getNorthEast();
	sw = rectangle.getBounds().getSouthWest();
	
	var infowincontent = document.createElement("div");
	infowincontent.className = "markerText";
	var strong = document.createElement("strong");
	strong.textContent = 'New Location';
	infowincontent.appendChild(strong);
	infowincontent.appendChild(document.createElement("br"));
	var NE_loc = document.createElement("text");
	NE_loc.textContent =   'New north-east corner: ' + ne.lat() + ', ' + ne.lng();
	infowincontent.appendChild(NE_loc);
	infowincontent.appendChild(document.createElement("br"));
	var SW_loc = document.createElement("text");
	SW_loc.textContent = 'New south-west corner: ' + sw.lat() + ', ' + sw.lng();
	infowincontent.appendChild(SW_loc);

	// Set the info window's content and position.
	infoWindow.setContent(infowincontent);
	infoWindow.setPosition(ne);
	infoWindow.open(map);
}

function initMap() {
	map = new google.maps.Map(document.getElementById("map"), {
	  center: {lat: 36.999783, lng: -122.063565},//get one of drone coordinates
	  zoom: 16,
	  mapTypeId: 'hybrid'
	});				
	
	infoWindow = new google.maps.InfoWindow();	

	//create markers --> not displaying marker? -need to debug-may have to do w/ path
	// Change this depending on the name of your PHP or XML file
	loadFile('createMarkers.php', function(data) {
	var xml = data.responseXML;//should have the array of markers created from php file
	var markers = xml.documentElement.getElementsByTagName("marker");
		Array.prototype.forEach.call(markers, function(markerElem) {
		  var name = markerElem.getAttribute("name");
		 // var pts = markerElem.getAttribute("pts");
		  var type = markerElem.getAttribute("type");
		  var point = new google.maps.LatLng(
			  parseFloat(markerElem.getAttribute("lat")),
			  parseFloat(markerElem.getAttribute("lng"))
		  );

		  // Create content for marker on click 
		  var infowincontent = document.createElement("div");
		    infowincontent.className = "markerText";
		    var strong = document.createElement("strong");
		    strong.textContent = name;
		    infowincontent.appendChild(strong);
		    infowincontent.appendChild(document.createElement("br"));
			// var ptInt = document.createElement("text");
			// ptInt.textContent = pts; --> may display battery level instead
			// infowincontent.appendChild(ptInt);
			// infowincontent.appendChild(document.createElement("br"));
			var position = document.createElement("text");
			position.textContent = point;
			infowincontent.appendChild(position);
		  // end of marker content//
			
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
		request = new ActiveXObject('Microsoft.XMLHTTP');
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
function Reload(){
	console.log(visualData);
	if(visualData == 0){ //make sure to only display if user is not in visual data setting
		clearText(); //clear visual data text before loading new information
		$("#mapping").show();
		//initMap();
	}	
}

/* Function to start streaming data on map and stream status*/

function stream_Map(button_id){
	var id = document.getElementById(button_id);
	console.log(id.value);
	if (id.value == "start") {
		id.value = "stop";
		stream = setInterval(Reload,1000);//calls reload every sec
		check_flight(); //call once
		flight_status = setInterval(check_flight,600000);//set next time event, every 10 min
		id.innerHTML = "Stop";
	}
	else if(id.value == "stop"){
        id.value = "start";
		clearInterval(stream);
		clearInterval(flight_status);
		id.innerHTML = "Start";
   }	
}

//loads the weather information from user input 
var curr_city;
var curr_state;
function LoadWeather(){
	var xmlhttp;
	console.log("Load Weather");//for debugging
	if (window.XMLHttpRequest) {// code for newer browsers			
		xmlhttp = new XMLHttpRequest();
	} else {// code for IE6, IE5
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	/*Once its done retrieving the data from file specified below*/
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			//reset input, or text box to be blank
			document.getElementById("city").value = "";
			document.getElementById("state").value = "";
			check_flight(); //call once
			flight_status = setInterval(check_flight,600000);//then set next time event, every 10 min(600000 ms)
			//update weather display
			document.getElementById("display_weather").innerHTML = xmlhttp.responseText;//display result on browser
			//check for flight status and start timer event
			
		}
	}
	//get values (text) from input form box
	curr_city = document.getElementById("city").value;
	curr_state = document.getElementById("state").value;
	var curr_display = "show";
	/*open and send new data inputs to php file*/
	xmlhttp.open("GET","weather_getInfo.php?display="+curr_display+"&state="+curr_state+"&city="+curr_city,true);//pass variables to php file
	xmlhttp.send();
}

/*  verifies if drones are safe to fly, and continuously checks every 10min when start is selected 
	or when user selects new city and state. It stops checking when user stops loading*/
function check_flight(){
	var xmlhttp;
	console.log("Check flight");//for debugging
	if (window.XMLHttpRequest) {// code for newer browsers			
		xmlhttp = new XMLHttpRequest();
	} else {// code for IE6, IE5
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	/*Once its done retrieving the data from file specified below*/
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			//update warning display
			document.getElementById("display_status").innerHTML = xmlhttp.responseText;//display result on browser
		}
	}
	/*open and send new data inputs to php file*/
	xmlhttp.open("GET","flight_status.php",true);//pass variables to php file
	xmlhttp.send();
}







