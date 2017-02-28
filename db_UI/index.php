<!DOCTYPE html>
<html lang="es">
<head>
	<meta charset="utf-8" / name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Tables from MySQL Database</title>
	<link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
	<link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Merienda+One" />
	<link rel="stylesheet" type="text/css" href="style.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
	
</head>

<body>
	
	<?php
	/*load credential information from config.ini*/
	$db = parse_ini_file("config.ini");
	$host = $db['host'];
	$user = $db['user'];
	$pass = $db['pass'];
	/* connect to the db */
	$connection = mysqli_connect($host,$user,$pass);
	/* retrieve all databases*/
	$all_database = mysqli_query($connection,'SHOW DATABASES') or die('cannot show tables');
	?>
	
	<div style="background-image: url(forest_background.jpg);" class="backg">
		<div class="main">	
			<img class="img-circle" src="pavx_logo.png" alt="logo" align="left"/>
			<h2> DataBase </h2>
		</div>
			<!----- create tabs -------->
			<ul class="nav nav-tabs">
				<li> <!--create home tab: map displayed-->
					<a href="javascript:void(0)" class="tablinks" onclick="openTab(event,'Home')" id="defaultOpen">Home</a>
				</li>
				<?php
				$db_count = 0;//don't print default, may or may not need it
				$table_count = 0;
				$db_names = array();//holds database names
				$table_names = array(); //holds table names
				while($tabs = mysqli_fetch_array($all_database,MYSQLI_BOTH)){//this access and iterates all the databases, creating tabs
					if( (strcmp($tabs[0],"information_schema") != 0) & (strcmp($tabs[0],"mysql") !=0 ) & 
								(strcmp($tabs[0],"performance_schema")!=0 ) & (strcmp($tabs[0],"sys") != 0) ){//don't show default db
						$db_names[$db_count] = $tabs[0];//store database name 
						echo "<li class='dropdown'>";//creates dropdown menu
						echo "<a class='dropdown-toggle' data-toggle='dropdown' id=".$tabs[0]." >". $tabs[0]. "<span class='caret'></span></a>";	
						echo "<ul class='dropdown-menu'>";
							$data = mysqli_select_db($connection,$tabs[0]);//make sure to connect to new database
							$tables = mysqli_query($connection,'SHOW TABLES') or die('cannot show tables');
							while($cur_table = mysqli_fetch_row($tables)) {//this access and iterates all the tables, creating dropdown tabs
								$table_names[$table_count] = $cur_table[0];
								echo "<li> <button class='link' id='".$cur_table[0]."' value='".$tabs[0]."' onclick='showTable( ".$cur_table[0]." )'> ".$cur_table[0]."</button>";
								echo "</li>";
								$table_count++;
							}
							
						echo "</ul>";
						echo "</li>";
						$db_count++;
					}
				}	
				?>
			</ul>			
	</div>
	
	<script>
	function downloadUrl(url,callback) {
		var request;
		if(window.ActiveXObject){
			request = new ActiveXObject('Microsoft.XMLHTTP')
		}else{
		 request = new XMLHttpRequest;
		}

		request.onreadystatechange = function() {
			if (request.readyState == 4) {
				request.onreadystatechange = doNothing;
				callback(request, request.status);
			}
		};
		request.open('GET', url, true);
		request.send(null);
	}
	</script>
	
	
	<div class="MapDisplay">
	<div id= "Home" class= "tabcontent">
		<h3>My Google Maps</h3>
		<div id="map" style="width: 400px; height: 300px;"> </div>
		<script type="text/javascript"> 
			var customLabel = {
				tester: {
				  label: 'D1'
				  
				}
		    };
			
			function initMap() {
				var infoWindow = new google.maps.InfoWindow;
				var map = new google.maps.Map(document.getElementById('map'), {
				  center: new google.maps.LatLng(36.999783, -122.063565),
				  zoom: 12
				});
				
				
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
	</div>
	</div>
		
	<script>
	function showTable(channel){
		var datab = channel.value;
		var chann =  channel.id;
		console.log(datab);
		console.log(chann);
		/*ajax code --> client is able to commuincate with server*/
		if (window.XMLHttpRequest) {// code for newer browsers			
		xmlhttp = new XMLHttpRequest();
		} else {// code for IE6, IE5
			xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
		}
		/*Once its done retrieving the data*/
		xmlhttp.onreadystatechange = function() {
			if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
				document.getElementById("output").innerHTML = xmlhttp.responseText;
			}
		}
		xmlhttp.open("GET","FetchTable.php?data="+datab+"&ch="+chann,true);//pass variables to php file
		xmlhttp.send();
	}
	</script>
	
	
	<script>
	function openTab(evt,map) {//displays map
		var name = document.getElementById(map);
		console.log(map);
		var tablinks,tabcontent;
		//erase any tab content from previous maps
		tabcontent = document.getElementsByClassName("tabcontent");
		for (i = 0; i < tabcontent.length; i++) { tabcontent[i].style.display = "none"; }
		tablinks = document.getElementsByClassName("tablinks");
		for (i = 0; i < tablinks.length; i++) { tablinks[i].className = tablinks[i].className.replace(" active", "");  }
		
		document.getElementById(map).style.display = "block";
		evt.currentTarget.className += " active";
	}
	// Get the element with id="defaultOpen" and click on it
	document.getElementById("defaultOpen").click();
	</script>


 	<br>
	<div id="output"><b> </b></div>
</body>
</html>