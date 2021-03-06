<?php
//we can also pass the city location from index.php [ state, city]
	//do jquery instead of mysql_affected_rows
	$QueryState = $_GET['state'];
    $QueryCity = str_replace(' ', '_', $_GET['city']);
	$QueryDisplay = $_GET['display'];
	//set default city and state
	if(!$QueryState || !$QueryCity ){
		$QueryCity = str_replace(' ', '_','Santa Cruz');
		$QueryState = "CA";
		$QueryDisplay = "show";
		$check_forecast = 0;
	} 
	
	//list global variables  --> may not even need all of them, select the ones you do
	/* Display Location --default*/
	$current_location;
	$current_city;
	$current_state;
	$current_zip;
	
	/* Station Data */
	$current_station_id;
	$current_observation_time;
	
	/* Weather Data */
	$weather;
	$weather_temp_f;
	$weather_temp_c;
	$weather_relative_humidity ;
	$weather_wind_string;
	$weather_wind_dir;
	$weather_wind_mph;
	//
	$weather_dewpoint_string;
	$weather_dewpoint_f;
	$weather_dewpoint_c;
	//
	$weather_heat_index_string;
	$weather_heat_index_f;
	$weather_heat_index_c ;
	//
	$weather_precip_1hr_string ;
	$weather_precip_1hr_in;
	$weather_precip_1hr_metric;
	$weather_precip_today_string ;
	$weather_precip_today_in;
	$weather_precip_today_metric;
	//
	$current_icon;
	$current_icon_url;
	$current_forecast_url;
	$current_history_url;
	$current_ob_url;
	
	//check for parsing
	$check = strcmp($QueryDisplay ,"show");		
	if($check == 0 ){
		$json_string = file_get_contents("http://api.wunderground.com/api/5eda6c03f8f8ae0b/conditions/q/".$QueryState."/".$QueryCity.".json");
		
		$parsed_json = json_decode($json_string,true);

		//list all the elements, that you will need for your parser program
		/* Display Location --default*/
		$current_location = $parsed_json['current_observation']['display_location']['full'];
		$current_city = $parsed_json['current_observation']['display_location']['city'];
		$current_state = $parsed_json['current_observation']['display_location']['state'];
		$current_zip = $parsed_json['current_observation']['display_location']['zip'];
		
		/* Weather Data */
		$weather = $parsed_json['current_observation']['weather'];
		$weather_temp_f = $parsed_json['current_observation']['temp_f'];
		$weather_temp_c = $parsed_json['current_observation']['temp_c'];
		$weather_relative_humidity = $parsed_json['current_observation']['relative_humidity'];
		$weather_wind_string = $parsed_json['current_observation']['wind_string'];
		$weather_wind_dir = $parsed_json['current_observation']['wind_dir'];
		$weather_wind_mph = $parsed_json['current_observation']['wind_mph'];
		//
		$weather_dewpoint_string = $parsed_json['current_observation']['dewpoint_string'];
		$weather_dewpoint_f = $parsed_json['current_observation']['dewpoint_f'];
		$weather_dewpoint_c = $parsed_json['current_observation']['dewpoint_c'];
		//
		$weather_heat_index_string = $parsed_json['current_observation']['heat_index_string'];
		$weather_heat_index_f = $parsed_json['current_observation']['heat_index_f'];
		$weather_heat_index_c = $parsed_json['current_observation']['heat_index_c'];
		//
		$weather_precip_1hr_string = $parsed_json['current_observation']['precip_1hr_string'];
		$weather_precip_1hr_in = $parsed_json['current_observation']['precip_1hr_in'];
		$weather_precip_1hr_metric = $parsed_json['current_observation']['precip_1hr_metric'];
		$weather_precip_today_string = $parsed_json['current_observation']['precip_today_string'];
		$weather_precip_today_in = $parsed_json['current_observation']['precip_today_in'];
		$weather_precip_today_metric = $parsed_json['current_observation']['precip_today_metric'];
		//
		$current_icon = $parsed_json['current_observation']['icon'];
		$current_icon_url = $parsed_json['current_observation']['icon_url'];
		$current_forecast_url = $parsed_json['current_observation']['forecast_url'];
		$current_history_url = $parsed_json['current_observation']['history_url'];
		$current_ob_url = $parsed_json['current_observation']['ob_url'];
		
		//parse for the week...
		$forecast_string = file_get_contents("http://api.wunderground.com/api/5eda6c03f8f8ae0b/forecast/q/".$QueryState."/".$QueryCity.".json");
		$parsed_forecast = json_decode($forecast_string,true);
		
		//table 1
		$curr_time = time();
		$curr_date = date("l, F d",$curr_time);
		echo "<table class='WeatherInfo'>";
		echo "<tbody>";
		echo "<tr>";
			echo "<td>". $current_city . ", " . $current_state . " (" . $current_zip  . ") </td>"; //creates columns
			echo "<td>  </td>"; //create gap
			echo "<td>".$curr_date ." </td>"; 
		echo "</tr>";
		echo "</tbody>";
		echo "</table>";
		
		//table 2
		echo "<table class='WeatherGUI'>";
		echo "<tbody>";
		echo "<thead> <tr>";//list weekday
			echo "<th>". $parsed_forecast['forecast']['simpleforecast']['forecastday'][0]['date']['weekday_short'] . "</th>";
			echo "<th>". $parsed_forecast['forecast']['simpleforecast']['forecastday'][1]['date']['weekday_short'] . "</th>";
			echo "<th>". $parsed_forecast['forecast']['simpleforecast']['forecastday'][2]['date']['weekday_short'] . "</th>";
			echo "<th>". $parsed_forecast['forecast']['simpleforecast']['forecastday'][3]['date']['weekday_short'] . "</th>";
		echo "</tr> </thead>";
		echo "<tr>";//list icon
			echo "<td> <img src='https://icons.wxug.com/i/c/g/". $parsed_forecast['forecast']['simpleforecast']['forecastday'][0]['icon'] .".gif'> </td>"; //icon for weekD0
			echo "<td> <img src='https://icons.wxug.com/i/c/g/". $parsed_forecast['forecast']['simpleforecast']['forecastday'][1]['icon'] .".gif'> </td>"; //icon for weekD1
			echo "<td> <img src='https://icons.wxug.com/i/c/g/". $parsed_forecast['forecast']['simpleforecast']['forecastday'][2]['icon'].".gif'> </td>"; //icon for weekD2
			echo "<td> <img src='https://icons.wxug.com/i/c/g/". $parsed_forecast['forecast']['simpleforecast']['forecastday'][3]['icon'] .".gif'> </td>"; //icon for weekD3
		echo "</tr>";
		echo "<tr>";//list description
			echo "<td>". $parsed_forecast['forecast']['simpleforecast']['forecastday'][0]['conditions'] ."</td>"; //descr. for weekD0
			echo "<td>". $parsed_forecast['forecast']['simpleforecast']['forecastday'][1]['conditions'] ."</td>"; //descr. for weekD1
			echo "<td>". $parsed_forecast['forecast']['simpleforecast']['forecastday'][2]['conditions'] ."</td>"; //descr. for weekD2
			echo "<td>". $parsed_forecast['forecast']['simpleforecast']['forecastday'][3]['conditions'] ."</td>"; //descr. for weekD3
		echo "</tr>";
		echo "<tr>";//list temp 
			echo "<td>". $parsed_forecast['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit'] ."&deg;F/ ".
					$parsed_forecast['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit'] ."&deg;F</td>"; //temp for weekD0
			echo "<td>".  $parsed_forecast['forecast']['simpleforecast']['forecastday'][1]['high']['fahrenheit'] ."&deg;F/ ".
					$parsed_forecast['forecast']['simpleforecast']['forecastday'][1]['low']['fahrenheit']."&deg;F</td>"; //temp for weekD1
			echo "<td>".  $parsed_forecast['forecast']['simpleforecast']['forecastday'][2]['high']['fahrenheit'] ."&deg;F/ ".
					$parsed_forecast['forecast']['simpleforecast']['forecastday'][2]['low']['fahrenheit'] ."&deg;F</td>"; //temp for weekD2
			echo "<td>".  $parsed_forecast['forecast']['simpleforecast']['forecastday'][3]['high']['fahrenheit'] ."&deg;F/ ".
					$parsed_forecast['forecast']['simpleforecast']['forecastday'][3]['low']['fahrenheit'] ."&deg;F</td>"; //temp for weekD3
		echo "</tr>";
		echo "</tbody>";
		echo "</table>";
		
		// echo "<p><span id='Location'> Location: ".$current_city . ", " . $current_state . " (" . $current_zip . ") </span></p>";
		// echo "<p><span id='temp'> Temperature: ". $weather_temp_f ." </span></p>";
		// echo "<p><span id='wind'> Wind Speed: ". $weather_wind_mph ." </span></p>";
		// echo "<p><span id='temp'> Humidity: ". $weather_relative_humidity ." </span></p>";
		// echo "<p><span id='wind'> Precipitation: ". $weather_precip_today_metric ." </span></p>";
		// echo "<p><span id='wind'> Dewpoint: ". $weather_dewpoint_string ." </span></p>";
		// echo "<p><span id='wind'> <img src='https://icons.wxug.com/i/c/h/". $current_icon .".gif'> Description: ". $current_icon." </span></p>";
	} 
	
?>