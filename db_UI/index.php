<!DOCTYPE html>
<html lang="es">
<head>
	<meta charset="utf-8" / name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Tables from MySQL Database</title>
	<link rel="shortcut icon" href="db_UI/pavx_logo.ico">
	<!---  include script and stylesheet files --->
	<link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Merienda+One" />
	<link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
	<link rel="stylesheet" type="text/css" href="db_UI/style.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
	<script type="text/javascript" src="db_UI/script.js"></script>
        <script type= "text/javascript" src="http://d3js.org/d3.v4.min.js"></script>
	
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
	$home = $db['rover']; //upload from config
	?>
	
	<div style="background-image: url(db_UI/forest_background.jpg);" class="backg">
		<div class="main">	
			<img class="img-circle" src="db_UI/pavx_logo.png" alt="logo" align="left"/>
			<h2> DataBase </h2>
		</div>
			<!----- create tabs -------->
			<ul class="nav nav-tabs">
				<li> <!--create home tab: map displayed-->
					<a href="javascript:void(0)" class="tablinks" onclick="mapClick()" id="defaultOpen">Home</a>
				</li>
				<?php
				/* Create other tabs for databases */
				while($tabs = mysqli_fetch_array($all_database,MYSQLI_BOTH)){//access and iterates all the databases, creating each tab
					if( (strcmp($tabs[0],"information_schema") != 0) & (strcmp($tabs[0],"mysql") !=0 ) & (strcmp($tabs[0],"phpmyadmin")!=0 ) &
								(strcmp($tabs[0],"performance_schema")!=0 ) & (strcmp($tabs[0],"sys") != 0) & (strcmp($tabs[0],$home) != 0)){//don't show default db
						echo "<li class='dropdown'>";//creates dropdown menu
						echo "<a class='dropdown-toggle' data-toggle='dropdown' id=".$tabs[0]." >". $tabs[0]. "<span class='caret'></span></a>";	
						echo "<ul class='dropdown-menu'>";
							$data = mysqli_select_db($connection,$tabs[0]);//make sure to connect to new database
							$tables = mysqli_query($connection,'SHOW TABLES') or die('cannot show tables');
							while($cur_table = mysqli_fetch_row($tables)) {//this access and iterates all the tables, creating dropdown tabs
								echo "<li> <button class='link' id='".$cur_table[0]."' value='".$tabs[0]."' onclick='showTable( ".$cur_table[0]." )'> ".$cur_table[0]."</button>";
								echo "</li>";
							}
						echo "</ul>";
						echo "</li>";
					}
				}	
				
				/*remember to put the button values x and y for rover coord*/
				?>
			</ul>			
		</div>		

	<script>
		// Get the element with id="defaultOpen" and click on it
		document.getElementById("defaultOpen").click();
	</script>
		
	<!-- Used when printing data visualization -->
	<div id="output"><b> </b>	 </div>
	<!-- Used for printing map and markers --->
	<div id="mapping" class="mapstyle"><b> 
	<!-- include weather API here -->
		<div class="weather_input">
			<ul id="user_info">
				<input class="submitText" id="city" type="text" placeholder="City">
				<input class="submitText" id="state" type="text" placeholder="State / Providence">
				<button id="submit" class="btn btn-success" onclick="LoadWeather()" >Get the weather</button>
			</ul>
			<div class="location" id="display_weather">
				 <?php require 'weather_getInfo.php'; ?> <!-- set up default weather--> 
			</div>
		</div>

		<div class="showMap">
			<h3>PSAV Map</h3>		
			<div id="map" style="width: 600px; height: 400px;"></div>
			<script async defer
			src="https://maps.googleapis.com/maps/api/js?key=AIzaSyC_HcJ7YyXFD0fVavbN0DuBN7_N2HnHvao&libraries=visualization&callback=initMap">
			</script>
			<br>
		</div> 
		
		<div class="flightStatus" id="display_status">
			<?php require 'flight_status.php'; ?>
		</div>
		
		<div class="mapRefresh">
			<button class="refresh" id="stream" value="start" onclick="stream_Map(this.id)"> Start </button>	
			
			<button class="refresh" id="scan" value="start" onclick="scan_Map(this.id)"> Scan </button>	
		</div>

	
	</b></div>	
	<br>
</body>
</html>