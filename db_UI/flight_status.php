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
	$homedb = $db['rover'];
	$drone = $db['drone'];
	echo "<form>";
	echo "<fieldset>";
    echo "<legend>Status:</legend>";
	
	//display scanned coordinates (4pts)
	echo "<p id='coordinates'>";
	echo "Selected coordinates: <br>";
	while($rover = mysqli_fetch_array($all_database,MYSQLI_BOTH)){
		if( (strcmp($rover[0],$homedb) == 0)){ //we only have one base
			//display coordinates to scan from home base
			$Hbase = mysqli_select_db($connection,$rover[0]);//make sure to connect to new database
			$Fdetails = mysqli_query($connection,'SHOW TABLES') or die('cannot show tables');//i am expecting a table to read and write too
			while($cur_table = mysqli_fetch_row($Fdetails)) {//this access and iterates through tables
				/* Select most recent timestamp from each table in database -- for testing*/
				$query = 'SELECT `x_0`, `y_0`, `x_1`, `y_1` From '.$cur_table[0].' ORDER by time DESC LIMIT 1';
				$query_cmd = mysqli_query($connection,$query) or die('Invalid query:');
				$coord = mysqli_fetch_assoc($query_cmd);
				echo "Coordinate0: ( ".$coord['x_0'].", ".$coord['y_0'].") <br>";
				echo "Coordinate1: ( ".$coord['x_1'].", ".$coord['y_1'].") <br>";
			}			
		}
	}
	echo "</p>";
	
	$all_databases = mysqli_query($connection,'SHOW DATABASES') or die('cannot show tables');
	//display all drones battery levels
	echo "<p id='batterylevel'>";
	echo "Battery Level Status:";
	echo " <br>";

	while($tabs = mysqli_fetch_array($all_databases,MYSQLI_BOTH)){//access and iterates all the databases only for drone
		if( (strcmp($tabs[0],$drone) == 0)){//select only drone database
			$data = mysqli_select_db($connection,$tabs[0]);//make sure to connect to new database
			$tables = mysqli_query($connection,'SHOW TABLES') or die('cannot show tables');
			//
			while($cur_table = mysqli_fetch_row($tables)) {
				echo "- ".$cur_table[0]; //display drone name
				/* Select most recent timestamp from each table in database -- for testing*/
				$fetch_all = 'SELECT `time` From '.$cur_table[0].' ORDER by time DESC LIMIT 1';
			//	$fetch_cmd = mysqli_query($connection,$fetch_all) or die('Invalid query:');
			//	$row = mysqli_fetch_assoc($fetch_cmd);
				//echo $row['time']; --will be battery level
				echo " = Battery Level";
				echo "<br>";
			}
		}
	}	
	echo "</p>";
	
	//check for weather conditions
	echo "<p id='updateWarn'>";
		echo "Warnings: <br>";
		if($weather_wind_mph < 10){ //check forecast
			echo "None: Safe to fly";
		}else{
			echo "error";
		}

	echo "</p>";
	echo "</fieldset>";
	echo "</form>";

?>