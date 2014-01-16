<%!    
    import logging
    log = logging.getLogger(__name__)
%>

################################################
## D3 graphs
################################################

<%def name="barChart(barData, chart, views, votes, downs, barText)">
  <style>
    #${chart} rect.views{
      fill: ${views};
    }

    #${chart} rect.totalVotes{
      fill: ${votes};
    }
    
    #${chart} rect.downVotes{
      fill: ${downs};
    }

    #${chart} text.views {
      fill: ${barText};
      font: 10px sans-serif;
      text-anchor: end;
    }

    #${chart} text.totalVotes {
      fill: white;
      font: 10px sans-serif;
      text-anchor: end;
    }

    #${chart} text.downVotes {
      fill: white;
      font: 10px sans-serif;
      text-anchor: end;
    }

    #${chart} .title { 
      font-size: 14px; 
      font-weight: bold; 
      fill: black;
    }

  </style>

  <svg id="${chart}"></svg>

  <script src="http://d3js.org/d3.v3.min.js"></script>
  <script>

    var margin = {
      top: 15, 
      right: 300, 
      bottom: 15, 
      left: 35
    }; 
    var width = 900 - margin.left - margin.right;
    var height = 600 - margin.top - margin.bottom;
    var barHeight = 20;

    var x = d3.scale.linear()
        .range([0, width]);

    var chart = d3.select("#${chart}")
        .attr("width", width + margin.left + margin.right);
    
    var data = ${barData | n}

    x.domain([0, d3.max(data, function(d) { return d.views; })]);

    chart.attr("height", barHeight * data.length + margin.top + margin.bottom);

    var bar = chart.selectAll("g")
        .data(data)
      .enter().append("g")
        .attr("transform", function(d, i) { return "translate(" + margin.left + "," + i * barHeight + ")"; });

    bar.append("rect")
          .attr("x", 0)
          .attr("width", function(d) { return x(d.views); })
          .attr("class", "views")
          .attr("height", barHeight - 1);

    bar.append("text")
          .attr("x", function(d) { return x(d.views) - 3; })
          .attr("y", barHeight / 2)
          .attr("dy", ".35em")
          .attr("class", "views")
          .text(function(d) { return d.views; });

    bar.append("rect")
          .attr("x", 0)
          .attr("width", function(d) { return x(d.totalVotes); })
          .attr("class", "totalVotes")
          .attr("height", barHeight - 1);

    bar.append("text")
          .attr("x", function(d) { return x(d.totalVotes) - 3; })
          .attr("y", barHeight / 2)
          .attr("dy", ".35em")
          .attr("class", "totalVotes")
          .text(function(d) { return d.totalVotes; });

    bar.append("rect")
          .attr("x", 0)
          .attr("width", function(d) { return x(d.downVotes); })
          .attr("class", "downVotes")
          .attr("height", barHeight - 1);

    bar.append("text")
          .attr("x", function(d) { return x(d.downVotes) - 3; })
          .attr("y", barHeight / 2)
          .attr("dy", ".35em")
          .attr("class", "downVotes")
          .text(function(d) { return d.downVotes; });

    bar.append("text")
        .attr("x", width + 5)
        .attr("y", barHeight / 2)
        .attr("dy", ".35em")
        .attr("class", "title")
        .style("text-anchor", "start")
        .text(function(d) { return d.title; });

    function type(d) {
      d.views = +d.views; // coerce to number
      return d;
    }

  </script>

</%def>

<%def name="bulletChart(bulletData)">

  <style>

    .bullet { font: 10px sans-serif; } 
    .bullet .marker { stroke: #000; stroke-width: 2px; } 
    .bullet .tick line { stroke: #666; stroke-width: .5px; } 
    .bullet .range.s0 { fill: #eee; } 
    .bullet .range.s1 { fill: #ddd; } 
    .bullet .range.s2 { fill: #ccc; } 
    .bullet .measure.s0 { fill: steelblue; } 
    .bullet .title { font-size: 14px; font-weight: bold; } 
    .bullet .subtitle { fill: #999; }

  </style> 

  <script src="http://d3js.org/d3.v3.min.js" charset="utf-8"></script>
  <script src="/d3/bullet.js"></script>

  <div>
    <p id='link' class='ideaListingTitle'>
      &nbsp;
    </p>
  </div>
  <button>Update</button>
  <div id="bulletChart">
  </div>
  
  <script>
    var margin = {
      top: 15, 
      right: 400, 
      bottom: 15, 
      left: 15
    }; 
    var width = 1000 - margin.left - margin.right;
    var height = 60 - margin.top - margin.bottom;

    var chart = d3.bullet() 
      .width(width)
      .height(height);

    var data = ${bulletData | n}

    var svg = d3.select("#bulletChart")
      .selectAll("svg")
        .data(data) 
      .enter().append("svg")
        .attr("class", "bullet") 
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom) 
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")") 
        .call(chart);

    var titlePlacement = width + 5;

    var title = svg.append("g") 
      .style("text-anchor", "start") 
      .attr("transform", "translate(" + titlePlacement + "," + height / 2 + ")");

    title.append("text") 
      .attr("class", "title") 
      .text(function(d) { return d.title; });

    title.append("text") 
      .attr("class", "subtitle") 
      .attr("dy", "1em") 
      .text(function(d) { return d.subtitle; });

    d3.selectAll("button").on("click", function() { 
      svg.datum(randomize).call(chart.duration(1000));
    });

    function randomize(d) { 
      if (!d.randomizer) d.randomizer = randomizer(d); 
      d.markers = d.markers.map(d.randomizer); 
      d.measures = d.measures.map(d.randomizer); 
      return d;
    }

    function randomizer(d) { 
      var k = d3.max(d.ranges) * .2; 
      return function(d) {
        return Math.max(0, d + k * (Math.random() - .5));
      }
    };

  </script>

</%def>

<%def name="newGraph(newData)">

  <style>

    path { 
      stroke: steelblue; 
      stroke-width: 2; 
      fill: none;
    }

    .axis path, .axis line {
      fill: none; 
      stroke: grey; 
      stroke-width: 1; 
      shape-rendering: crispEdges;
    }

    path {
      stroke: steelblue;
      stroke-width: 2;
      fill: none;
    }

    .grid .tick { 
      stroke: lightgrey; 
      opacity: 0.7;
    } 

    .grid path {
      stroke-width: 0;
    }

    .area { 
      fill: lightsteelblue; 
      stroke-width: 0;
    }

    text.shadow { 
      stroke: white;
      stroke-width: 2.5px; 
      opacity: 0.9;
    }

    div.tooltip { 
      position: absolute; 
      text-align: center; 
      width: 7em; 
      height: 4.5em; 
      padding: 0.4em; 
      font: 1em sans-serif; 
      background: lightsteelblue; 
      border: 0px; 
      border-radius: 0.6em; 
      pointer-events: none;
    }

  </style>

  <div>
    <p id='link' class='ideaListingTitle'>
      &nbsp;
    </p>
  </div>
  <div id="newChart">
    <!--<div id="option"> 
      <input name="updateButton" type="button" value="Update" onclick="updateData()"/>
    </div>-->
  </div>

  <script src="http://d3js.org/d3.v3.min.js" charset="utf-8"></script>
  <script>
    var margin = {
      top: 46, 
      right: 200, 
      bottom: 100, 
      left: 60
    }; 
    var width = 1050 - margin.left - margin.right;
    var height = 496 - margin.top - margin.bottom;

    var voteColors = {
      zero: "darkorchid",
      one: "mediumslateblue",
      aboveOne: "yellow",
      aboveQuarter: "deepskyblue",
      aboveHalf: "cyan",
      aboveThreeQuarters: "lime"
    }

    // expecting date to arrive in standard msql format
    var parseDate = d3.time.format("%Y-%m-%d %H:%M:%S").parse;
    
    var x = d3.time.scale().range([0, width]);
    
    var y = d3.scale.linear().range([height, 0]); 
    
    var xAxis = d3.svg.axis().scale(x)
      .orient("bottom").ticks(10)
      .tickFormat(d3.time.format("%m/%d/%y")); 

    var yAxis = d3.svg.axis().scale(y)
      .orient("left").ticks(5);

    function make_x_axis() { 
      return d3.svg.axis()
        .scale(x) 
        .orient("bottom") 
        .ticks(5)
    }
    
    function make_y_axis() { 
      return d3.svg.axis()
        .scale(y) 
        .orient("left") 
        .ticks(10)
    }


    var valueline = d3.svg.line()
      .x(function(d) { return x(parseDate(d.date)); }) 
      .y(function(d) { return y(+d.views); });

    var svg = d3.select("#newChart") 
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom) 
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


    // Get the data - in this case it's json in a variable
    var graphData = ${newData | n}
    //console.log(graphData);

    // Scale the range of the data
    var maxViews = d3.max(graphData, function(d) { return +d.views; });
    var maxVotes = d3.max(graphData, function(d) { return +d.totalVotes; });
    x.domain(d3.extent(graphData, function(d) { return parseDate(d.date); })); 
    y.domain([0, maxViews]);
    
    svg.append("g") 
      .attr("class", "grid") 
      .attr("transform", "translate(0," + height + ")") 
      .call(make_x_axis()
        .tickSize(-height, 0, 0) 
        .tickFormat("")
      )
    
    svg.append("g") 
      .attr("class", "grid") 
      .call(make_y_axis()
        .tickSize(-width, 0, 0) 
        .tickFormat("")
      )

    /*
    svg.append("path")  // Add the valueline path.
      .attr("class", "line")
      .attr("d", valueline(graphData));
    */

    var ttDiv = d3.select("#newChart")
      .append("div") 
      .attr("class", "tooltip") 
      .style("opacity", 0);

    function approval(u,t) {
      //console.log(t + " " + u);
      if (+t > 0) {
        var approval = Math.ceil(u/t)*100;
        return approval+"% approval <br/>";
      } else {
        return "";
      }
    }
    
    function popular(u,t) {
      if (+t > 0) {
        var score = Math.ceil(u/t)*100;
        if (score>50) {
          return true;
        } else {
          return false;
        }
      } else {
        return false;
      }
    }

    var linkDiv = d3.select("#link")

    svg.selectAll("dot") 
        .data(graphData)
      .enter().append("a") 
        .attr("xlink:href", function(d) {
          return d.url
        })
        .append( "circle" )
        .attr("r", function(d) {
          if (popular(d.upVotes, d.totalVotes)) {
            return 6;
          } else {
            return 3;
          }
        })
        .attr("cx", function(d) { return x(parseDate(d.date)); })
        .attr("cy", function(d) { return y(+d.views); })
        .style("fill", function(d) {
          if (+d.totalVotes > 3*maxVotes/4) {
            return voteColors.aboveThreeQuarters;
          } else if (+d.totalVotes > maxVotes/2) {
            return voteColors.aboveHalf;
          } else if (+d.totalVotes > maxVotes/4) {
            return voteColors.aboveQuarter;
          } else if (+d.totalVotes > 1) {
            return voteColors.aboveOne;
          } else if (+d.totalVotes > 0) {
            return voteColors.one;
          } else {
            return voteColors.zero;
          }
        })
        .style("stroke", function(d) {
          if (+d.totalVotes > maxVotes/4) {
            return "grey";
          } else {
            return "lavender";
          }
        })
        //.on("click", function(d) {
        //  linkDiv.html("<a href='" + d.url + "'>" + d.title + "</a>")
        //})
        .on("mouseover", function(d) {          
          linkDiv.html('<a href="' + d.url + '" class="listed-item-title">' + d.title + '</a>')
          ttDiv.transition() 
            .duration(200)
            .style("opacity", .9); 
          ttDiv.html(d.type + "<br/>" + d.totalVotes + " votes" + "<br/>" + approval(d.upVotes, d.totalVotes) + d.views + " views")
            .style("left", (d3.event.pageX) + "px") 
            .style("top", (d3.event.pageY - 58) + "px")
            .style("pointer-events", "none");
        }) 
        .on("mouseout", function(d) {
          ttDiv.transition() 
            .duration(500)
            .style("opacity", 0);
        });

    svg.append("g") // Add the X Axis 
      .attr("class", "x axis") 
      .attr("transform", "translate(0," + height + ")") 
      .call(xAxis)
      .selectAll("text")
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", function(d) {
            return "rotate(-35)"
        });

    svg.append("g") 
      .attr("class", "y axis") 
      .call(yAxis);

    // text label for the x axis
    svg.append("text")  
      .attr("transform", "translate(" + (width / 2) + " ," + (height + 3*margin.bottom/4) + ")")
      .style("text-anchor", "middle") 
      .text("Last Activity");

    svg.append("text") 
      .attr("transform", "rotate(-90)") 
      .attr("y", 0 - margin.left)
      .attr("x", 0 - (height / 2)) 
      .attr("dy", "1em") 
      .style("text-anchor", "middle") 
      .text("# of Views");
    
    svg.append("text") 
      .attr("x", (width / 2)) 
      .attr("y", 0 - (margin.top / 2)) 
      .attr("text-anchor", "middle") 
      .style("font-size", "16px") 
      .style("text-decoration", "underline")
      .attr("class", "shadow")
      .text("All Activities");

    svg.append("text") 
      .attr("x", (width / 2)) 
      .attr("y", 0 - (margin.top / 2)) 
      .attr("text-anchor", "middle") 
      .style("font-size", "16px") 
      .style("text-decoration", "underline") 
      .text("All Activities");

    // legend
    /*var voteColors = {
      zero: "darkorchid",
      one: "mediumslateblue",
      aboveOne: "yellow",
      aboveQuarter: "deepskyblue",
      aboveHalf: "cyan",
      aboveThreeQuarters: "lime"
    }*/
    
    var boxSpacing = 105;

    var lineSpaceMultiplier = 1.3;

    svg.append("text") 
      .attr("x", width)
      .attr("dx", "3em")
      .attr("y", "0.8em")
      .style("font-size", "16px") 
      .style("text-anchor", "start") 
      .style("text-decoration", "underline")
      .text("Legend");

    svg.append("text") 
      .attr("x", width + 5)
      .attr("y", (2 * lineSpaceMultiplier) + "em")
      .attr("dy", ".85em")
      .style("font-size", "14px") 
      .style("text-anchor", "start") 
      .text("Most votes: ");

    svg.append("rect")
      .attr("x", width + boxSpacing)
      .attr("y", (2 * lineSpaceMultiplier) + "em")
      .attr("height", "1em") 
      .attr("width", "2em")
      .style("fill", voteColors.aboveThreeQuarters)
      .style("stroke", "grey")

    svg.append("text") 
      .attr("x", width + 5)
      .attr("y", (3 * lineSpaceMultiplier) + "em")
      .attr("dy", ".85em")
      .style("font-size", "14px") 
      .style("text-anchor", "start") 
      .text("Many votes: ");

    svg.append("rect")
      .attr("x", width + boxSpacing)
      .attr("y", (3 * lineSpaceMultiplier) + "em")
      .attr("height", "1em") 
      .attr("width", "2em")
      .style("fill", voteColors.aboveHalf)
      .style("stroke", "grey")

    svg.append("text") 
      .attr("x", width + 5)
      .attr("y", (4 * lineSpaceMultiplier) + "em")
      .attr("dy", ".85em")
      .style("font-size", "14px") 
      .style("text-anchor", "start") 
      .text("Some votes: ");

    svg.append("rect")
      .attr("x", width + boxSpacing)
      .attr("y", (4 * lineSpaceMultiplier) + "em")
      .attr("height", "1em") 
      .attr("width", "2em")
      .style("fill", voteColors.aboveQuarter)
      .style("stroke", "grey")

    svg.append("text") 
      .attr("x", width + 5)
      .attr("y", (5 * lineSpaceMultiplier) + "em")
      .attr("dy", ".85em")
      .style("font-size", "14px") 
      .style("text-anchor", "start") 
      .text("Above 1 vote: ");

    svg.append("rect")
      .attr("x", width + boxSpacing)
      .attr("y", (5 * lineSpaceMultiplier) + "em")
      .attr("height", "1em") 
      .attr("width", "2em")
      .style("fill", voteColors.aboveOne)
      .style("stroke", "lavender")

    svg.append("text") 
      .attr("x", width + 5)
      .attr("y", (6 * lineSpaceMultiplier) + "em")
      .attr("dy", ".85em")
      .style("font-size", "14px") 
      .style("text-anchor", "start") 
      .text("One vote: ");

    svg.append("rect")
      .attr("x", width + boxSpacing)
      .attr("y", (6 * lineSpaceMultiplier) + "em")
      .attr("height", "1em") 
      .attr("width", "2em")
      .style("fill", voteColors.one)
      .style("stroke", "lavender")

    svg.append("text") 
      .attr("x", width + 5)
      .attr("y", (7 * lineSpaceMultiplier) + "em")
      .attr("dy", ".85em")
      .style("font-size", "14px") 
      .style("text-anchor", "start") 
      .text("Zero votes: ");

    svg.append("rect")
      .attr("x", width + boxSpacing)
      .attr("y", (7 * lineSpaceMultiplier) + "em")
      .attr("height", "1em") 
      .attr("width", "2em")
      .style("fill", voteColors.zero)
      .style("stroke", "lavender")

    svg.append("text") 
      .attr("x", width + 5)
      .attr("y", (9 * lineSpaceMultiplier) + "em")
      .attr("dy", ".85em")
      .style("font-size", "13px") 
      .style("text-anchor", "start") 
      .style("fill", "grey")
      .text("Click a dot to visit the item.");

    svg.append("text") 
      .attr("x", width + 5)
      .attr("y", (10 * lineSpaceMultiplier) + "em")
      .attr("dy", ".85em")
      .style("font-size", "13px") 
      .style("text-anchor", "start") 
      .style("fill", "grey")
      .text("Hover over a dot to see info.");

    svg.append("text") 
      .attr("x", width + 5)
      .attr("y", (13 * lineSpaceMultiplier) + "em")
      .attr("dy", ".85em")
      .style("font-size", "12px") 
      .style("text-anchor", "start") 
      .style("fill", "grey")
      .text("Larger dots are popular.");

    svg.append("text") 
      .attr("x", width + 5)
      .attr("y", (15 * lineSpaceMultiplier) + "em")
      .attr("dy", ".85em")
      .style("font-size", "12px") 
      .style("text-anchor", "start") 
      .style("fill", "grey")
      .text("Smaller dots are unpopular,");

    svg.append("text") 
      .attr("x", width + 5)
      .attr("y", (16 * lineSpaceMultiplier) + "em")
      .attr("dy", ".85em")
      .style("font-size", "12px") 
      .style("text-anchor", "start") 
      .style("fill", "grey")
      .text("or no votes have been cast");

    svg.append("text") 
      .attr("x", width + 5)
      .attr("y", (17 * lineSpaceMultiplier) + "em")
      .attr("dy", ".85em")
      .style("font-size", "12px") 
      .style("text-anchor", "start") 
      .style("fill", "grey")
      .text("on the item.");

  </script>

</%def>