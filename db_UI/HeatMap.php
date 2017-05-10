<?php
	// read the config.ini file
	$db = parse_ini_file("config.ini");
	$host = $db['host'];
	$user = $db['user'];
	$pass = $db['pass'];

	// Open a connection to a MySQL server
	$connection = mysqli_connect($host,$user,$pass) or die('cannot connect');
		
	//load in passed database and table info, need to convert into loadable string;will give error otherwise
	$database = mysqli_real_escape_string($connection,$_GET['data']);
	$n = mysqli_real_escape_string($connection,$_GET['n']);
	$threshold = mysqli_real_escape_string($connection,$_GET['th']);
	/* connect to the db */
	$data = mysqli_select_db($connection,$database) or die('cannot show db');
	//Obtain values above threshold from DB and save them as JSON
	for($i = 0; $i<1; $i++) {
		$fetch_data = 'SELECT `loc_x`, `loc_y` FROM jay'.$i.' WHERE sensor0_pts > '.$threshold;
		$fetch_cmd = mysqli_query($connection,$fetch_data)or die('panic im a teapot');	
		if(mysqli_num_rows($fetch_cmd) > 0) {
			while($row = mysqli_fetch_array($fetch_cmd,MYSQLI_BOTH)){
				echo $row['loc_y'],' ',$row['loc_x'],' ';
			}
		}
	}
?>