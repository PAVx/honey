/* ----------------------------------------------------------------------------
File: dynamic2.js
Provides live data from the drones.
Status: Fake data and only a single svg graph
-----------------------------------------------------------------------------*/ 
//Space the graphs will occupy
var svg_width = 653
//var svg_width = 980
var svg_height = 333
//var svg_height = 500

//Specify how much padding on each side of the SVG (to look cleaner)
var margin = {top: 20, right: 20, bottom: 20, left: 40},
    width = svg_width - margin.left - margin.right,
    height = svg_height - margin.top - margin.bottom;

var num_sensors = 1;
var count;
var n = 40,
    random = d3.randomNormal(5, 1), //random number averaging to 0, std dev of 0.2
    data = d3.range(n).map(random);  //range: goes from 0 to n(40) in steps of 1. map: maps values from random onto data


//for(count=0;count<num_sensors;count++) {

d3.json("JSONData.json", function(error, json) {
    if(error) console.log("error reading data");
    console.log(json);  //Log output to console


//Create the SVG element in which the graph will be placed.
//"g" groups SVG elements together
var svg = d3.select("body").append("svg") //select the body region and add an svg
    .attr("width", width - margin.left - margin.right) //set the width of the svg to desired amount
    .attr("height", height - margin.top - margin.bottom) //set height of svg to desired amount
    g = svg.append("g").attr("transform", "translate(" + margin.left + "," + (margin.top) + ")"); //move the svg element to appropriate place

//Set the scale to linear 
var x = d3.scaleLinear()
    .domain([0, n - 1]) //values that x can be
    .range([0, width]); //maps x values to the total width of svg
var y = d3.scaleLinear()
    .domain([0, 10]) //values that y can be
//    .range([height, 0]); //maps y values to total height of svg
    .range([height - (2*(margin.top+margin.bottom)), 0]);

//Generate a line for the given data
//"i" is the index of the data (time) and "d" is the associated data
var line = d3.line()
    .x(function(d, i) { return x(i); })
    .y(function(d, i) { return y(d); });

//return scaled values of the data
var line2 = d3.line()
    .x(function(d, i) { return x(d.time); })
    .y(function(d, i) { return y(d.sensor0); });

//Set clip region (how far the line will be drawn)
g.append("defs").append("clipPath")
    .attr("id", "clip")
    .append("rect")
    .attr("width", width)
    .attr("height", height);

//Add subgroup to the chart for the x axis and draw it
g.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + (height-2*(margin.top + margin.bottom)) + ")")
    .call(d3.axisBottom(x));

//Add subgroup to chart for the y axis and draw it
g.append("g")
    .attr("class", "y axis")
    .call(d3.axisLeft(y)
            /*.ticks(5)*/);     
    
//Subgroup for the actual line to be drawn
    //for(count=0;count<num_sensors;count++) {
    
g.append("g")
    //draw the line in the clip path
    .attr("clip-path", "url(#clip)")
    .append("path")
    //.datum(data)
    .datum(json[0])
    .attr("class", "line")
    .transition()
    .duration(500)
    .ease(d3.easeLinear)
    .on("start", tick);
    

//}
    

//Updates the visualization to add new values and to remove old values
function tick() {
  // Push a new data point onto the back.
 // data.push(random());
  // Redraw the line.
  d3.select(this)
      .attr("d", line2)
      .attr("transform", null);
  // Slide it to the left.
  //d3.active(this)
      //.attr("transform", "translate(" + x(-1) + ",0)")
      //.transition()
      //.duration(500)
      //.on("start", tick);
  // Pop the old data point off the front.
  //data.shift();
}
    
    });