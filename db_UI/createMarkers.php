<?php
	/*load credential information from config.ini*/
	$db = parse_ini_file("config.ini");
	$host = $db['host'];
	$user = $db['user'];
	$pass = $db['pass'];
	$dronedb = $db['drone'];
	/* Open a connection to a MySQL server */
	$connection = mysqli_connect ($host, $user, $pass) or die('Not connected : ' . mysql_error());
	
	header("Content-type: text/xml");
	/* Start XML file */
	echo '<markers>'; // needed to create following markers to place on map
	
	/* fetchall databases */
	$all_database = mysqli_query($connection,'SHOW DATABASES') or die('cannot show tables');
	/*itterate through the database and select most recent time stamp, lat and long pts */
	while($database = mysqli_fetch_array($all_database,MYSQLI_BOTH)){ //select only the drone db
		/* Set markers only for the active rover tables */
		if(strcmp($database[0],$dronedb) == 0 ){//search only the drones database
			/* connect to new database */
			$db_selected = mysqli_select_db($connection,$database[0]) or die ('cannot access db : ' . mysql_error());
			$droneList = mysqli_query($connection,'SHOW TABLES') or die('cannot show tables');
			/* Access and iterates all the tables within current database */
			while($table = mysqli_fetch_row($droneList)) {
				/* Select most recent timestamp from each table in database */
				$query = 'SELECT `loc_x`, `loc_y` From '.$table[0].' ORDER by time DESC LIMIT 1';
				$result = mysqli_query($connection,$query) or die('Invalid query:');
				
				/* Iterate through the row, printing XML nodes for only recent/lastest timestamp */
				$row = mysqli_fetch_assoc($result);
				/* Add to XML document node */
				echo '<marker ';
				echo 'name="' .$table[0] . '" ';
				echo 'lat="' . $row['loc_x'] . '" ';
				echo 'lng="' . $row['loc_y'] . '" ';
				echo 'type="'. $database[0]. '" ';
				echo '/>';
			}
		}
	}	
	// End of XML file	
	echo '</markers>';
?>