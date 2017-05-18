<?php
	// read the config.ini file
	$db = parse_ini_file("config.ini");
	$host = $db['host'];
	$user = $db['user'];
	$pass = $db['pass'];

	// Open a connection to a MySQL server
	$connection = mysqli_connect($host,$user,$pass) or die('cannot connect');
		
	//load in passed database and table info, need to convert into loadable string;will give error otherwise
	//database is which DB to read the data from (will always be jays for the visualization)
	$database = mysqli_real_escape_string($connection,$_GET['db']);
	//table = which table to obtain information from
	$table = mysqli_real_escape_string($connection,$_GET['tbl']);
	//sen is the sensor to obtain data from
	$sen = mysqli_real_escape_string($connection,$_GET['sen']);
	//n is how many of the recent values to pull from the DB.
	$n = mysqli_real_escape_string($connection,$_GET['n']);
	// connect to the db
	$data = mysqli_select_db($connection,$database) or die('cannot show db');
	//Obtain n most recent values from DB
	$fetch_data = 'SELECT '.$sen.' FROM '.$table.' ORDER BY time ASC LIMIT '.$n;
	$fetch_cmd = mysqli_query($connection,$fetch_data)or die('visualization sql command is invalid');	
	if(mysqli_num_rows($fetch_cmd) > 0) {
		while($row = mysqli_fetch_array($fetch_cmd,MYSQLI_BOTH)){
			echo $row[$sen],' ';
		}
	}
?>