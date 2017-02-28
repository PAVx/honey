<?php
	// read the config.ini file
	$db = parse_ini_file("config.ini");
	$host = $db['host'];
	$user = $db['user'];
	$pass = $db['pass'];
	
	// Opens a connection to a MySQL server
	$connection = mysqli_connect ($host, $user, $pass) or die('Not connected : ' . mysql_error());
	
	header("Content-type: text/xml");//may need to remove for debugging but re-add it later!!
	// Start XML file, echo parent node
	echo '<markers>'; //to create following markers
	
	//fetchall databases
	$all_database = mysqli_query($connection,'SHOW DATABASES') or die('cannot show tables');
	//itterate through the database and select most recent time stamp, lat and long pts
	while($database = mysqli_fetch_array($all_database,MYSQLI_BOTH)){
		// Set the active MySQL database 
		if( (strcmp($database[0],"information_schema") != 0) & (strcmp($database[0],"mysql") !=0 ) & 
								(strcmp($database[0],"performance_schema")!=0 ) & (strcmp($database[0],"sys") != 0) ){//don't show default db
			$db_selected = mysqli_select_db($connection,$database[0]) or die ('Can\'t use db : ' . mysql_error());
			
			// Select most recent timestamp from each table in database
			$tableList = mysqli_query($connection,'SHOW TABLES') or die('cannot show tables');
			while($table = mysqli_fetch_row($tableList)) {//this access and iterates all the table withing database
				$query = 'SELECT `loc_x`, `loc_y`,`pts` From '.$table[0].' ORDER by time DESC LIMIT 1';
				$result = mysqli_query($connection,$query) or die('Invalid query:');

				// Iterate through the row, printing XML nodes for only recent/lastest timestamp
				$row = mysqli_fetch_assoc($result);
				// Add to XML document node
				echo '<marker ';
				echo 'name="' .$table[0] . '" ';//table name
				echo 'pts="' . $row['pts'] . '" ';//point of interest
				echo 'lat="' . $row['loc_x'] . '" ';//latitude --> need to be float!
				echo 'lng="' . $row['loc_y'] . '" ';//longitude -->need to be float
				echo 'type="'. $database[0]. '" ';//database name
				echo '/>';
			}
		}
	}	
	// End XML file	
	echo '</markers>';
?>