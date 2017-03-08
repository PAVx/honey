<?php
	/*load credential information from config.ini*/
	$db = parse_ini_file("config.ini");
	$host = $db['host'];
	$user = $db['user'];
	$pass = $db['pass'];
	/* Open a connection to a MySQL server */
	$connection = mysqli_connect ($host, $user, $pass) or die('Not connected : ' . mysql_error());
	
	header("Content-type: text/xml");
	/* Start XML file */
	echo '<markers>'; // needed to create following markers to place on map
	
	/* fetchall databases */
	$all_database = mysqli_query($connection,'SHOW DATABASES') or die('cannot show tables');
	/*itterate through the database and select most recent time stamp, lat and long pts */
	while($database = mysqli_fetch_array($all_database,MYSQLI_BOTH)){
		/* Set markers only for the active MySQL databases (and maybe not the first drone) */
		if( (strcmp($database[0],"information_schema") != 0) & (strcmp($database[0],"mysql") !=0 ) & 
				(strcmp($database[0],"performance_schema")!=0 ) & (strcmp($database[0],"sys") != 0) ){//don't show default db
			/* connect to new database */
			$db_selected = mysqli_select_db($connection,$database[0]) or die ('Can\'t use db : ' . mysql_error());
			$tableList = mysqli_query($connection,'SHOW TABLES') or die('cannot show tables');
			
			/* Access and iterates all the tables within current database */
			while($table = mysqli_fetch_row($tableList)) {
				/* Select most recent timestamp from each table in database */
				$query = 'SELECT `loc_x`, `loc_y`,`pts` From '.$table[0].' ORDER by time DESC LIMIT 1';
				$result = mysqli_query($connection,$query) or die('Invalid query:');
				
				/* Iterate through the row, printing XML nodes for only recent/lastest timestamp */
				$row = mysqli_fetch_assoc($result);
				/* Add to XML document node */
				echo '<marker ';
				echo 'name="' .$table[0] . '" ';
				echo 'pts="' . $row['pts'] . '" ';
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