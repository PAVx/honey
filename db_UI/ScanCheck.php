<?php
	/*load credential information from config.ini*/
	$db = parse_ini_file("config.ini");
	$host = $db['host'];
	$user = $db['user'];
	$pass = $db['pass'];
	/* connect to the db */
	$connection = mysqli_connect($host,$user,$pass) or die('Connecting fail');
	
	//get coordinates
	$x1 = mysqli_real_escape_string($connection,$_GET['x1']);
	$x2 = mysqli_real_escape_string($connection,$_GET['x2']);
	$y1 = mysqli_real_escape_string($connection,$_GET['y1']);
	$y2 = mysqli_real_escape_string($connection,$_GET['y2']);	
	$alert = 0;

	//calculate scanned area offset
	//where pt1,pt2 is ne, pt3,4 is sw
	$width = $y2 - $y1;
	$height= $x1 -$x2;
	$area = $width * $height; //make sure to scale for actual math
	$temp = "2017-03-16 03:27:52";
	//get battery levels
	
	
	echo "<form>";
	echo "<fieldset>";
    echo "<legend>Status:</legend>";
	//check if the area is within the limits,then insert it into database
	if($area){
		$database = $db['rover']; //log onto correct database!! get from config file
		$data = mysqli_select_db($connection,$database) or die('cannot show db'); /* connect to the db */
		$time =time();
		$timestamp = date("Y-m-d H:i:s",$time);
		$insert= "INSERT INTO flight (`time`, `alert`, `x_0`, `y_0`, `x_1`, `y_1`) VALUES ('".$timestamp."',".$alert.",".$x1.",".$y1.",".$x2.",".$y2.")";
		$query_cmd = mysqli_query($connection,$insert) or die('Invalid query:');
		//then update status
		echo "<p>";
		echo "Area scan is with in Battery Level Requirements";
		echo "</p>";
		//display scanned coordinates (4pts)
		echo "<p>";
		echo "Selected coordinates: <br>";
		echo "Coordinate0: ( ".$x1.", ".$y1.") <br>";
		echo "Coordinate1: ( ".$x2.", ".$y2.") <br>";
		echo "</p>";

	} else{ 
		//if not then display warning for selected scanning area
		echo "<p>";
			echo "Warnings: <br>";
			echo "ERROR: Selected scanning area invalid";
		echo "</p>";		
	}	
	echo "</p>";
	echo "</fieldset>";
	echo "</form>";	
		
		
	
	


?>