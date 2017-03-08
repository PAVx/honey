<?php
	// read the config.ini file
	$db = parse_ini_file("config.ini");
	$host = $db['host'];
	$user = $db['user'];
	$pass = $db['pass'];
	// Open a connection to a MySQL server
	$connection = mysqli_connect($host,$user,$pass) or die('cannot connect');	
	//load in passed database and table info
	$database = mysqli_real_escape_string($connection,$_GET['data']);
	$table = mysqli_real_escape_string($connection,$_GET['ch']);
	/* connect to the db */
	$data = mysqli_select_db($connection,$database) or die('cannot show db');

	/* show table */
	echo '<h3>',$table,'</h3>';
	//print data table for channel
	$fetch_all = 'SELECT * From '.$table.' ORDER by time';
	$fetch_cmd = mysqli_query($connection,$fetch_all);
	echo '<table cellpadding="0" cellspacing="0" class="db-table">';
	echo '<tr><th>Time</th><th>Loc_X</th><th>Loc_Y</th><th>Loc_Z</th><th>Meas_Val</th><th>pts</th></tr>';
	if(mysqli_num_rows($fetch_cmd) > 0) {
		while($row = mysqli_fetch_array($fetch_cmd,MYSQLI_BOTH)){//print each row in table
			echo '<tr>';
			echo '<td>',$row['time'],'</td>','<td>',$row['loc_x'],'</td>','<td>',$row['loc_y'],'</td>';
			echo '<td>',$row['loc_z'],'</td>','<td>',$row['meas_val'],'</td>','<td>',$row['pts'],'</td>';
			echo '</tr>';
		}				
	}
	echo '</table><br>';
	
?>