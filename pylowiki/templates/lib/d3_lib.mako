<%!    
    import logging
    log = logging.getLogger(__name__)
%>

################################################
## D3 graphs
################################################

<%def name="includeD3()">
  <script src="/js/vendor/d3.v3.min.js" charset="utf-8"></script>
</%def>

<%def name="dcCommuterSurvey()">
  <style>
      h2.surveyTitle { 
          float: right;
      } 
      h2.surveyTitle span {
          font-size: 14px; 
          font-weight: normal; 
      }
      h4 span {
          font-size: 0.9em; 
          font-weight: normal; 
      }


      .dc-chart rect.bar {
          fill: aquamarine;
      }
      .dc-chart path.line {
          stroke-width: 3px;
          stroke-opacity: 1;
          stroke: aquamarine;
      }

      .dc-chart g.row text {
          font-size: 1em !important;
          font: arial !important;

      }

      .dc-chart .pie-slice {
          fill: black !important;
          font-size: 0.8em !important;
      }

      .table {
          width: 60%;
      }
  </style>

  <script src='/js/vendor/crossfilter.js' type='text/javascript'></script> 
  <script src='/js/vendor/dc.js' type='text/javascript'></script>
  <link href='/styles/vendor/dc.css' rel='stylesheet' type='text/css'>

  <div class='container'>
      <div class='row'>
          <div class='span11 offset1'> 
              <div class="dc-data-count" style="float: left;"> 
                  <h2 class="surveyTitle">Commuter Survey Results
                      <span> 
                          <span class="filter-count"></span>
                          selected out of
                          <span class="total-count"></span> 
                          records | <a href="javascript:dc.filterAll(); dc.renderAll();">Reset</a> 
                      </span>
                  </h2> 
              </div>
          </div>
      </div>

      <div class='row'>   <!-- wide left area, tall right column -->   
          <div class='span9'> 
              <div class='row'>
                  <div class='span5 offset1' id='dc-salary-chart'> 
                      <h4>Salary distribution</h4>
                  </div>
                  <div class='span5 offset1' id='dc-commuteDuration-chart'>
                      <h4>Commute Duration</h4> 
                  </div>
              </div>
              <div class='row'>
                  <div class='span11 offset1' id='dc-age-chart'>
                      <h4>Age of commuters polled</h4> 
                  </div>
              </div>
              <div class='row'> 
                  <div class='span5 offset1' id='dc-college-chart'>
                      <h4>Attended college in area
                          <span>
                              <a class="reset"
href="javascript:collegeChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                          </span>
                      </h4> 
                  </div>
                  <div class='span5 offset1' id='dc-commuteType-chart'>
                      <h4>Commute Method
                          <span>
                              <a class="reset"
href="javascript:commuteTypeChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                          </span>
                      </h4> 
                  </div>
              </div>
          </div>   <!-- END wide left area -->   
          <div class='span3'>   <!-- tall right column -->   
              <div class='span12' id='dc-employmentType-chart'>
                  <h4>Job Type
                      <span>
                          <a class="reset"
href="javascript:employmentTypeChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a>
                      </span>
                  </h4>
              </div>
          </div>   <!-- END tall right column -->   
      </div>

      <div class='row'> 
          <div class='span10 offset1'>
              <table class='table table-hover' id='dc-table-graph'> 
                  <thead>
                      <tr class='header'> 
                          <th>Commute Activity</th> 
                          <th>Years at Job</th> 
                          <th>Seniority</th> 
                          <th>Salary</th>
                          <th>Why Commute</th>
                          <th>Why Live Here</th>
                          <th>Residence Duration</th>
                          <th>Worked in Santa Cruz</th>
                          <th>Why not work in Santa Cruz</th>
                          <th>Salary needed to work here</th>
                          <th>Children</th>
                          <th>Rent or own</th>
                      </tr>
                  </thead>
              </table>
          </div>

      </div> 

  </div>

  <script>
      // Create the dc.js chart objects & link to div
      var salaryChart = dc.barChart("#dc-salary-chart");
      var commuteDurationChart = dc.lineChart("#dc-commuteDuration-chart");
      var ageChart = dc.barChart("#dc-age-chart");
      var collegeChart = dc.rowChart("#dc-college-chart");
      var employmentTypeChart = dc.rowChart("#dc-employmentType-chart");
      var commuteTypeChart = dc.rowChart("#dc-commuteType-chart");

      var dataTable = dc.dataTable("#dc-table-graph");

      var data = null;
      
      // NOTE: the csv file's fields tend to get wrapped in apostrophes thanks to open office:
      // ( "field", "field", .. )
      //   remove these or the csv loader here won't work e.g.: ( field, field, .. )
      d3.csv("/surveys/techCommuterSurvey6.csv", function(error, data) {
          //console.log(error);
          //console.log(data);
          /*
              <th>Commute Duration</th>             commuteDuration 
              <th>Commute Type</th>                 travelType
              <th>Commute Activity</th>             commuteActivity 
              <th>Employment Type</th>              employmentType  
              <th>Years at Job</th>                 employmentDuration  
              <th>Seniority</th>                    employmentLevel
              <th>Salary</th>                       salary
              <th>Why Commute</th>                  whyCommute
              <th>Why Live Here</th>                whyLiveHere 
              <th>College in Santa Cruz</th>        collegeInSantaCruz  
              <th>Residence Duration</th>           residenceDuration 
              <th>Worked in Santa Cruz</th>         workedInSantaCruz 
              <th>Why not work in Santa Cruz</th>   whyNoWorkInSantaCruz  
              <th>Salary needed to work here</th>   whatSalaryNeeded  
              <th>Children</th>                     children  
              <th>Rent or own</th>                  rentOrOwn 
              <th>Age</th>                          age
          */

          data.forEach(function(d) {
              d.commuteDuration = +d.commuteDuration/60;
              d.employmentDuration = +d.employmentDuration;
              d.salary = +d.salary;
              d.residenceDuration = +d.residenceDuration;
              d.age = +d.age;
          });

          // Run the data through crossfilter and load our 'facts'
          var facts = crossfilter(data);

          // reset all button - this includes all facts
          var all = facts.groupAll();

          // reset all button - count all the facts
          dc.dataCount(".dc-data-count") 
              .dimension(facts) 
              .group(all);

          // determine the spread of salaries
          var salaryValue = facts.dimension(function (d) { 
              return d.salary;
          });
          var salaryValueGroup = salaryValue.group();


          // determine the spread of commute times
          var commuteDurationValue = facts.dimension(function (d) { 
              return d.commuteDuration;
          });
          // calculate the spread of the sum for how many of each commute time there is
          var commuteDurationValueGroupCount = commuteDurationValue.group() 
              .reduceCount(function(d) { return d.commuteDuration; }) // counts

          // determine the spread of the commuters' ages
          var ageValue = facts.dimension(function (d) { 
              return d.age;
          });
          var ageValueGroupCount = ageValue.group()
              .reduceCount(function(d) { return d.age; }) // counts
          
          var collegeValue = facts.dimension(function (d) {
              //console.log("college: " + d.collegeWhere)
              switch (d.collegeWhere) {
                  case 'UCSC': return "0.UCSC";
                  case 'Cabrillo': return "1.Cabrillo";
                  default: return "2.No answer";
              } 
          });
          var collegeValueGroup = collegeValue.group();

          // employmentType 
          //var employmentType = facts.dimension(function (d) { return d.employmentType; });
          
          var employmentType = facts.dimension(function (d) {
              //console.log("college: " + d.collegeWhere)
              switch (d.employmentType) {
                  case '(blank)': return "0.No answer";
                  case 'Bio Engineer': return "1.Bio Engineer";
                  case 'Business Development': return "2.Business Development";
                  case 'Design': return "3.Design";
                  case 'Education': return "4.Education";
                  case 'Electrical Engineer': return "5.Electrical Engineer";
                  case 'Executive': return "6.Executive";
                  case 'Finance': return "7.Finance";
                  case 'Hardware QA': return "8.Hardware QA";
                  case 'IT': return "9.IT";
                  case 'Legal': return "10.Legal";
                  case 'Management': return "11.Management";
                  case 'Manufacturing': return "12.Manufacturing";
                  case 'Marketing': return "13.Marketing";
                  case 'Mechanical Engineer': return "14.Mechanical Engineer";
                  case 'Operations': return "15.Operations";
                  case 'Recruiter': return "16.Recruiter";
                  case 'Sales': return "17.Sales";
                  case 'Software Developer': return "18.Software Developer";
                  case 'Support Engineer': return "19.Technical Support";
                  case 'Technical Support': return "19.Technical Support";
                  case 'Technical Writer': return "19.Technical Support";
                  default: return "0.No answer";
              } 
          });
          var employmentTypeGroup = employmentType.group();

          // commuteType 
          var commuteType = facts.dimension(function (d) {
              switch (d.travelType) {
                  case 'Company bus': return "0.Company bus";
                  case 'Car (solo)': return "1.Car (solo)";
                  case 'Independent shuttle': return "2.Independent shuttle";
                  case 'Carpool': return "3.Carpool";
                  default: return "4.No answer";
              } 
          });
          var commuteTypeGroup = commuteType.group();

          // Create dataTable dimension
          var commuteDurationDimension = facts.dimension(function (d) { 
              return d.commuteDuration;
          });

          // Setup the charts

          var commasFormatter = d3.format(",.0f");
          // bar chart of salaries and their sum of occurences
          salaryChart.width(400) 
              .height(150) 
              .margins({top: 10, right: 10, bottom: 20, left: 20}) 
              .dimension(salaryValue) 
              .group(salaryValueGroup) 
              .transitionDuration(500) 
              .centerBar(true) 
              .gap(-8)
              .filter([0, 550000]) 
              .x(d3.scale.linear().domain([0, 550000])) 
              .elasticY(true) 
              .xAxis()
              .tickFormat(function(d) { return "$" + commasFormatter(d); })
              .ticks(6);

          var hoursFormatter = function(d) {
            if (d > 1)
                return d + "hrs";
            else
                return d + " hour";
          }
          // bar chart of commute duration and its sum of occurences
          commuteDurationChart.width(400) 
              .height(150) 
              .margins({top: 10, right: 10, bottom: 20, left: 20}) 
              .dimension(commuteDurationValue) 
              .group(commuteDurationValueGroupCount) 
              .transitionDuration(500)
              .brushOn(false) 
              .title(function(d){
                  return d.key / 60
                  + " hrs \nNumber of Commuters: " + d.value; 
                  })
              .x(d3.scale.linear().domain(d3.extent(data, function(d) { return d.commuteDuration; })))
              .elasticY(true) 
              .xAxis()
              .tickFormat(function(d) { return hoursFormatter(d); })
              .ticks(5);

          var yearsFormatter = function(d) {
              return d + " yrs old";
          }
          // age graph
          ageChart.width(800) 
              .height(150) 
              .margins({top: 10, right: 10, bottom: 20, left: 40}) 
              .dimension(ageValue) 
              .group(ageValueGroupCount) 
              .transitionDuration(500) 
              .centerBar(true) 
              .gap(-6)
              .elasticY(true) 
              .filter([0, 71]) 
              .x(d3.scale.linear().domain((d3.extent(data, function(d) { return d.age + 2; }))))
              .xAxis()
              .tickFormat(function(d) { return yearsFormatter(d); });

          var commutersFormatter = function(d) {
            if (d > 1)
                return d + " people";
            else if (d == 1)
                return d + " person";
            else
                return d;
          }
          // row chart for college attendance
          collegeChart.width(400) 
              .height(220) 
              .margins({top: 25, left: 40, right: 40, bottom: 40}) 
              .dimension(collegeValue) 
              .group(collegeValueGroup) 
              .colors(d3.scale.category20c())
              .label(function (d){
                  return d.key.split(".")[1];
                  })
              .title(function(d){return d.value + " commuters";}) 
              .xAxis()
              .tickFormat(function(d) { return commutersFormatter(d); })
              .ticks(4);

          // pie chart for distribution of commute types
          commuteTypeChart.width(400) 
              .height(220) 
              .dimension(commuteType) 
              .group(commuteTypeGroup)
              .colors(d3.scale.category20b())
              .label(function (d){
                  return d.key.split(".")[1];
                  }) 
              .title(function(d){return d.value + " commuters";})
              .xAxis()
              .tickFormat(function(d) { return commutersFormatter(d); })
              .ticks(4);

          // pie chart for distribution of employment types
          employmentTypeChart.width(220) 
              .height(620) 
              .margins({top: 25, left: 5, right: 10, bottom: 40}) 
              .dimension(employmentType) 
              .group(employmentTypeGroup) 
              .colors(d3.scale.category20c())
              .label(function (d){
                  return d.key.split(".")[1];
                  }) 
              .title(function(d){return d.value + " commuters.";})
              .xAxis()
              .ticks(4);

              
          // Table of commuter survey data
          dataTable.width(760).height(800) 
              .dimension(commuteDurationDimension)
                  .group(function(d) { return "Commuter Survey Table" 
                      })
                  .size(10) 
              .columns([
                  function(d) { return d.commuteActivity; },
                  function(d) { return d.employmentDuration; },
                  function(d) { return d.employmentLevel; },
                  function(d) { return d.salary; },
                  function(d) { return d.whyCommute; },
                  function(d) { return d.whyLiveHere; },
                  function(d) { return d.residenceDuration; },
                  function(d) { return d.workedInSantaCruz; },
                  function(d) { return d.whyNoWorkInSantaCruz; },
                  function(d) { return d.whatSalaryNeeded; },
                  function(d) { return d.children; },
                  function(d) { return d.rentOrOwn; },
              ])
              .sortBy(function(d){ 
                  return d.commuteDuration; 
              })
              .order(d3.ascending);

          // Render the Charts
          dc.renderAll();

      });

  </script>

</%def>


<%def name="constancyChart(constancyData, chart, typeName, barColor, barHover)">

<style>

  #${chart} .${chart}bar rect {
    fill: ${barColor};
  }

  #${chart} .${chart}bar:hover rect {
    fill: ${barHover};
  }

  #${chart} a:hover {
    fill:#D15D00;
  }

  #${chart} a {
    font-size: 1.3em;
  }

  .value {
    fill: white;
  }

  .axis {
    shape-rendering: crispEdges;
  }

  .axis path {
    fill: none;
    stroke: none;
  }

  .x.axis line {
    stroke: #eee;
    stroke-opacity: .8;
  }

  .y.axis path {
    stroke: black;
  }


</style>


<p id="${chart}menu">
  <b>Top ${typeName} by various counts</b><br>Compare by: 
  <select></select>
</p>
<div id="${chart}">
</div>

<script>

  var margin = {
      top: 20, 
      right: 500, 
      bottom: 20, 
      left: 40
    }; 

  data = ${constancyData | n}

  var ${chart}barHeight = 28;
  var ${chart}totalHeight = ${chart}barHeight * data.length;
  
  var width = 960 - margin.left - margin.right;
  var ${chart}height = ${chart}totalHeight + margin.top + margin.bottom;

  var format = d3.format("d");
  var ${chart}states;
  var age;

  var ${chart}x = d3.scale.linear()
      .range([0, width]);

  var ${chart}y = d3.scale.ordinal()
      .rangeRoundBands([0, ${chart}height], .1);

  var ${chart}xAxis = d3.svg.axis()
      .scale(${chart}x)
      .orient("top")
      .tickSize(-${chart}height - margin.bottom)
      .tickFormat(format);

  var ${chart}svg = d3.select("#${chart}").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", ${chart}height + margin.top + margin.bottom)
      .style("margin-left", -margin.left + "px")
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  ${chart}svg.append("g")
      .attr("class", "x axis");
  
  ${chart}svg.append("g")
      .attr("class", "y axis")
    .append("line")
      .attr("class", "domain")
      .attr("y2", ${chart}height);

  var ${chart}menu = d3.select("#${chart}menu select")
      .on("change", ${chart}change);

  ${chart}states = data;
  
  var ${chart}ages = d3.keys(${chart}states[0]).filter(function(key) {
    return key != "views" && key != "code" && key != "title" && key != "url" && key != "totalVotes" && key != "yesPercent";
  });


  ${chart}menu.selectAll("option")
      .data(${chart}ages)
    .enter().append("option")
      .text(function(d) { return d; });

  ${chart}menu.property("value", "Total Views");

  ${chart}redraw();
  

  var altKey;

  d3.select(window)
      .on("keydown", function() { altKey = d3.event.altKey; })
      .on("keyup", function() { altKey = false; });

  function ${chart}change() {

    d3.transition()
        .duration(altKey ? 4000 : 1500)
        .each(${chart}redraw);
  }

  function ${chart}redraw() {
    var age1 = ${chart}menu.property("value");
    var top = ${chart}states.sort(function(a, b) { return b[age1] - a[age1]; });

    ${chart}y.domain(top.map(function(d) { return d.code; }));

    var ${chart}bar = ${chart}svg.selectAll(".${chart}bar")
        .data(top, function(d) { return d.code; });

    var ${chart}barEnter = ${chart}bar.enter().insert("g", ".axis")
        .attr("class", "${chart}bar")
        .attr("transform", function(d) { return "translate(0," + (${chart}y(d.code) + ${chart}height) + ")"; })
        .style("fill-opacity", 0);

    ${chart}barEnter
        .append("rect")
        .attr("width", age && function(d) { return ${chart}x(d[age]); })
        .attr("height", ${chart}y.rangeBand());

    ${chart}barEnter.append("a") 
        .attr("xlink:href", function(d) {
          return d.url
        })
        .attr("class", "listed-item-title")
        .append("text")
        .attr("x", width + 5)
        .attr("y", ${chart}y.rangeBand() / 2)
        .attr("dy", ".35em")
        .attr("text-anchor", "start")
        .text(function(d) { return d.title; });

    ${chart}barEnter.append("text")
        .attr("class", "value")
        .attr("x", age && function(d) { return ${chart}x(d[age]) - 3; })
        .attr("y", ${chart}y.rangeBand() / 2)
        .attr("dy", ".35em")
        .attr("text-anchor", "end");

    ${chart}x.domain([0, top[0][age = age1]]);

    var ${chart}barUpdate = d3.transition(${chart}bar)
        .attr("transform", function(d) { return "translate(0," + (d.y0 = ${chart}y(d.code)) + ")"; })
        .style("fill-opacity", 1);

    ${chart}barUpdate.select("rect")
        .attr("width", function(d) { return ${chart}x(d[age]); });

    ${chart}barUpdate.select(".value")
        .attr("x", function(d) { return ${chart}x(d[age]) - 3; })
        .text(function(d) { return format(d[age]); });

    var ${chart}barExit = d3.transition(${chart}bar.exit())
        .attr("transform", function(d) { return "translate(0," + (d.y0 + ${chart}height) + ")"; })
        .style("fill-opacity", 0)
        .remove();

    ${chart}barExit.select("rect")
        .attr("width", function(d) { return ${chart}x(d[age]); });

    ${chart}barExit.select(".value")
        .attr("x", function(d) { return ${chart}x(d[age]) - 3; })
        .text(function(d) { return format(d[age]); });

    d3.transition(${chart}svg).select(".x.axis")
        .call(${chart}xAxis);
  }

</script>

</%def>

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

    var data = ${barData | n}

    var dataViews = function(d) { return d.views; };
    var dataVotes = function(d) { return d.totalVotes; };

    var viewScale = d3.scale.linear()
      .domain([0, d3.max(data, dataViews)])
      .range([0, width]);
    // if I give votes the same width scale as views I may be able to display them as a stacked bar group
    // worth a try, if I can get this working 
    var totalVoteScale = d3.scale.linear()
      .domain([0, d3.max(data, dataVotes)])
      .range([0, width]);

    var chart = d3.select("#${chart}")
        .attr("width", width + margin.left + margin.right);
    

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
          .attr("height", (7 * barHeight / 8));

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
          .attr("height", (3 * barHeight / 4));

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
