<%!
    import pylowiki.lib.db.workshop     as workshopLib
    from pylowiki.lib.db.user import getUserByID
    from pylowiki.lib.db.generic import getThing
    import pylowiki.lib.db.activity as activityLib
    import pylowiki.lib.db.facilitator   as facilitatorLib
    import pylowiki.lib.utils   as utils
    import misaka as m

    import logging
    log = logging.getLogger(__name__)
%>

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="showScatterChart()">
  <div id="offsetDiv">
    <div id="test1" class='with-3d-shadow with-transitions'>
      <svg></svg>
    </div>
  </div>
</%def>

<%def name="scatterChart(stats)">
  <style>

    svg {
      overflow: hidden;
    }

    div {
      border: 0;
      margin: 0;
    }

    /*
    #offsetDiv {
      margin-left: 100px;
      margin-top: 100px;
    }
    */

    #test1 {
      margin: 0;
    }

    #test1 svg {
      height: 500px;
    }

  </style>
  
  <link href="/nvd3/src/nv.d3.css" rel="stylesheet" type="text/css">

  <script src="/nvd3/lib/d3.v3.js"></script>
  <script src="/nvd3/nv.d3.min.js"></script>
  <script src="/nvd3/src/tooltip.js"></script>
  <script src="/nvd3/src/utils.js"></script>
  <script src="/nvd3/src/models/legend.js"></script>
  <script src="/nvd3/src/models/axis.js"></script>
  <script src="/nvd3/src/models/distribution.js"></script>
  <script src="/nvd3/src/models/scatter.js"></script>
  <script src="/nvd3/src/models/scatterChart.js"></script>
  <script>

    //Format A
    var chart;
    nv.addGraph(function() {
      chart = nv.models.scatterChart()
        .showDistX(true)
        .showDistY(true)
        .useVoronoi(true)
        .color(d3.scale.category10().range())
        .transitionDuration(300)
        ;

      chart.xAxis.tickFormat(d3.format('.02f'));
      chart.yAxis.tickFormat(d3.format('.02f'));
      chart.tooltipContent(function(key) {
          return '<h2>' + key + '</h2>';
      });

      var data = ${stats | n}
      //console.log("data: " + data);
      
      //.datum(randomData(4,5))
      d3.select('#test1 svg')
          .datum(data)
          .call(chart);

      nv.utils.windowResize(chart.update);

      chart.dispatch.on('stateChange', function(e) { ('New State:', JSON.stringify(e)); });

      return chart;
    });

    function fPrintObject(o) {
      var out = '';
      for (var p in o) {
        if (typeof(o[p]) == 'object') {
          fPrintObject(o[p]);
        } else {
          out += p + ': ' + o[p] + '\n';
        }
      }
      console.log(out);
    }

    function randomData(groups, points) { //# groups,# points per group
      var data = [],
          shapes = ['circle', 'cross', 'triangle-up', 'triangle-down', 'diamond', 'square'],
          random = d3.random.normal();

      for (i = 0; i < groups; i++) {
        data.push({
          key: 'Group ' + i,
          values: []
        });

        for (j = 0; j < points; j++) {
          data[i].values.push({
            x: random(), 
            y: random(), 
            size: Math.random(), 
            shape: shapes[j % 6]
          });
        }
      }
      fPrintObject(data);
      return data;
    }

  </script>
</%def>

<%def name="showEdolfoWater()">
  <h1>Santa Cruz Water Consumption (2000-2010)</h1>

  <h4>Overall Metrics
    <div id="consumption">
      <svg></svg>
    </div>
  </h4>

  <h4>Breakdown of water use
    <div id="breakdown">
      <svg></svg>
    </div>
  </h4>
</%def>

<%def name="edolfoWater()">
  <style>

    body {
      padding: 50px;
      font: 14px "Lucida Grande", Helvetica, Arial, sans-serif;
    }

    a {
      color: #00B7FF;
    }

    #consumption svg {
      height: 350px;
      width: 1000px;
      min-width: 600px;
      min-height: 100px;
    }

    #consumption {
      margin-top: 20px;
      margin-left: 20px;
    }

    #breakdown svg {
      height: 350px;
      width: 1000px;
      min-width: 600px;
      min-height: 100px;
    }

    #breakdown {
      margin-top: 20px;
      margin-left: 20px;
    }

  </style>
  <link href="//cdnjs.cloudflare.com/ajax/libs/nvd3/1.1.13-beta/nv.d3.min.css" rel='stylesheet' type='text/css'>
  <script src="//cdnjs.cloudflare.com/ajax/libs/nvd3/1.1.13-beta/nv.d3.min.js"></script>
  <script src="//cdnjs.cloudflare.com/ajax/libs/lodash.js/2.4.0/lodash.min.js"></script>
  <script>
    d3.csv('http://dataviz.hckrlabs.com/public/data/annual-h2o-consumption-gal-2000-2010.csv', function(data){
      nv.addGraph(function(){
        myData = [{
          key: 'Millions of gallons vs. Year',
          values: []
        }];
        data.forEach(function(d){
          var row = {};
          row.y =   parseInt(d.Business, 10) +
            parseInt(d['Coast Irrigation'], 10) +
            parseInt(d['Golf Course Irrigation'], 10) +
            parseInt(d['Multiple Residential'], 10) +
            parseInt(d.Industrial, 10) +
            parseInt(d.Irrigation, 10) +
            parseInt(d.Municipal, 10) +
            parseInt(d.Other, 10) +
            parseInt(d['Single Family Residential'], 10);
          row.x =   parseInt(d.Year, 10);
          myData[0].values.push(row);
        });

        var chart = nv.models.discreteBarChart()
          .x(function(d) { return d.x })
          .y(function(d) { return d.y }) // values must be x and y
          .margin({top: 30, right: 20, bottom: 50, left: 175})
          .tooltips(true)
          .showValues(true);

        chart.xAxis
          .axisLabel('Year')
          .tickFormat(d3.format('d'));

        chart.yAxis
          .axisLabel('Millions of gallons')
          .tickFormat(d3.format('d'));

        d3.select('#consumption svg')
          .datum(myData)
          .transition().duration(500).call(chart);

        nv.utils.windowResize(chart.update);
        return chart;
      });

      nv.addGraph(function(){
        myData = [
          {
            key: 'Industrial',
            values: []
          },
          {
            key: 'Irrigation',
            values: []
          },
          {
            key: 'Business',
            values: []
          },
          {
            key: 'Coast Irrigation',
            values: []
          },
          {
            key: 'Golf Course Irrigation',
            values: []
          },
          {
            key: 'Multiple Residential',
            values: []
          },
          {
            key: 'Municipal',
            values: []
          },
          {
            key: 'Other',
            values: []
          },
          {
            key: 'Single Family Residential',
            values: []
          }
        ];

        data.forEach(function(d){
          var row = {};
          row.y = +d.Industrial;
          row.x = +d.Year;
          myData[0].values.push(row);

          row = {};
          row.y = +d.Irrigation;
          row.x = +d.Year;
          myData[1].values.push(row);

          row = {};
          row.y = +d.Business;
          row.x = +d.Year;
          myData[2].values.push(row);

          row = {};
          row.y = +d['Coast Irrigation'];
          row.x = +d.Year;
          myData[3].values.push(row);

          row = {};
          row.y = +d['Golf Course Irrigation'];
          row.x = +d.Year;
          myData[4].values.push(row);

          row = {};
          row.y = +d['Multiple Residential'];
          row.x = +d.Year;
          myData[5].values.push(row);

          row = {};
          row.y = +d.Municipal;
          row.x = +d.Year;
          myData[6].values.push(row);

          row = {};
          row.y = +d.Other;
          row.x = +d.Year;
          myData[7].values.push(row);

          row = {};
          row.y = +d['Single Family Residential'];
          row.x = +d.Year;
          myData[8].values.push(row);
        });
        var chart = nv.models.multiBarChart();
        
        chart.xAxis
        .axisLabel('Year')
        .tickFormat(d3.format('d'));

        chart.yAxis
        .axisLabel('Millions of gallons')
        .tickFormat(d3.format('d'));

        d3.select('#breakdown svg')
        .datum(myData)
        .transition().duration(500)
        .call(chart);

        nv.utils.windowResize(chart.update);
        return chart;
      })
    });
  </script>
</%def>

<%def name="showSunburst1()">
    <h1>Coffee Flavour Wheel</h1>
    <div id="vis"></div>
</%def>

<%def name="sunburst1(data)">
  <style>
    path {
      stroke: #000;
      stroke-width: 1.5;
      cursor: pointer;
    }

    text {
      font: 11px sans-serif;
      cursor: pointer;
    }

    body {
      width: 880px;
      margin: 0 auto;
    }

    h1 {
      text-align: center;
      margin: .5em 0;
    }

    p#intro {
      text-align: center;
      margin: 1em 0;
    }
  </style>
  <script>
    var width = 840,
        height = width,
        radius = width / 2,
        x = d3.scale.linear().range([0, 2 * Math.PI]),
        y = d3.scale.pow().exponent(1.3).domain([0, 1]).range([0, radius]),
        padding = 5,
        duration = 1000;

    var div = d3.select("#vis");

    div.select("img").remove();

    var vis = div.append("svg")
        .attr("width", width + padding * 2)
        .attr("height", height + padding * 2)
      .append("g")
        .attr("transform", "translate(" + [radius + padding, radius + padding] + ")");

    div.append("p")
        .attr("id", "intro")
        .text("Click to zoom!");

    var partition = d3.layout.partition()
        .sort(null)
        .value(function(d) { return 5.8 - d.depth; });

    var arc = d3.svg.arc()
        .startAngle(function(d) { return Math.max(0, Math.min(2 * Math.PI, x(d.x))); })
        .endAngle(function(d) { return Math.max(0, Math.min(2 * Math.PI, x(d.x + d.dx))); })
        .innerRadius(function(d) { return Math.max(0, d.y ? y(d.y) : d.y); })
        .outerRadius(function(d) { return Math.max(0, y(d.y + d.dy)); });

    //d3.json(wheelData, function(error, json) {
      var cleanData = '${data}'
      cleanData = cleanData.replace(/&quot;/g,'"')
      console.log(cleanData);
      var jsonData = JSON.parse( cleanData );
      var nodes = partition.nodes({children: jsonData});

      var path = vis.selectAll("path").data(nodes);
      path.enter().append("path")
          .attr("id", function(d, i) { return "path-" + i; })
          .attr("d", arc)
          .attr("fill-rule", "evenodd")
          .style("fill", colour)
          .on("click", click);

      var text = vis.selectAll("text").data(nodes);
      var textEnter = text.enter().append("text")
          .style("fill-opacity", 1)
          .style("fill", function(d) {
            return brightness(d3.rgb(colour(d))) < 125 ? "#eee" : "#000";
          })
          .attr("text-anchor", function(d) {
            return x(d.x + d.dx / 2) > Math.PI ? "end" : "start";
          })
          .attr("dy", ".2em")
          .attr("transform", function(d) {
            var multiline = (d.name || "").split(" ").length > 1,
                angle = x(d.x + d.dx / 2) * 180 / Math.PI - 90,
                rotate = angle + (multiline ? -.5 : 0);
            return "rotate(" + rotate + ")translate(" + (y(d.y) + padding) + ")rotate(" + (angle > 90 ? -180 : 0) + ")";
          })
          .on("click", click);
      textEnter.append("tspan")
          .attr("x", 0)
          .text(function(d) { return d.depth ? d.name.split(" ")[0] : ""; });
      textEnter.append("tspan")
          .attr("x", 0)
          .attr("dy", "1em")
          .text(function(d) { return d.depth ? d.name.split(" ")[1] || "" : ""; });

      function click(d) {
        path.transition()
          .duration(duration)
          .attrTween("d", arcTween(d));

        // Somewhat of a hack as we rely on arcTween updating the scales.
        text.style("visibility", function(e) {
              return isParentOf(d, e) ? null : d3.select(this).style("visibility");
            })
          .transition()
            .duration(duration)
            .attrTween("text-anchor", function(d) {
              return function() {
                return x(d.x + d.dx / 2) > Math.PI ? "end" : "start";
              };
            })
            .attrTween("transform", function(d) {
              var multiline = (d.name || "").split(" ").length > 1;
              return function() {
                var angle = x(d.x + d.dx / 2) * 180 / Math.PI - 90,
                    rotate = angle + (multiline ? -.5 : 0);
                return "rotate(" + rotate + ")translate(" + (y(d.y) + padding) + ")rotate(" + (angle > 90 ? -180 : 0) + ")";
              };
            })
            .style("fill-opacity", function(e) { return isParentOf(d, e) ? 1 : 1e-6; })
            .each("end", function(e) {
              d3.select(this).style("visibility", isParentOf(d, e) ? null : "hidden");
            });
      }
    //});

    function isParentOf(p, c) {
      if (p === c) return true;
      if (p.children) {
        return p.children.some(function(d) {
          return isParentOf(d, c);
        });
      }
      return false;
    }

    function colour(d) {
      if (d.children) {
        // There is a maximum of two children!
        var colours = d.children.map(colour),
            a = d3.hsl(colours[0]),
            b = d3.hsl(colours[1]);
        // L*a*b* might be better here...
        return d3.hsl((a.h + b.h) / 2, a.s * 1.2, a.l / 1.2);
      }
      return d.colour || "#fff";
    }

    // Interpolate the scales!
    function arcTween(d) {
      var my = maxY(d),
          xd = d3.interpolate(x.domain(), [d.x, d.x + d.dx]),
          yd = d3.interpolate(y.domain(), [d.y, my]),
          yr = d3.interpolate(y.range(), [d.y ? 20 : 0, radius]);
      return function(d) {
        return function(t) { x.domain(xd(t)); y.domain(yd(t)).range(yr(t)); return arc(d); };
      };
    }

    function maxY(d) {
      return d.children ? Math.max.apply(Math, d.children.map(maxY)) : d.y + d.dy;
    }

    // http://www.w3.org/WAI/ER/WD-AERT/#color-contrast
    function brightness(rgb) {
      return rgb.r * .299 + rgb.g * .587 + rgb.b * .114;
    }
  </script>
</%def>

<%def name="showSortChart1()">
   <div id="chart"></div>
</%def>

<%def name="sortChart1(stats)">
    <%
        # attempt1: construct raw data sting
        #dataString = "[\n"
        #for idea in stats:
        #    entry = "{'i': %s, 'total': '%s', 'yes': %s, 'no': %s},\n"%(idea['index'], idea['totalVotes'], idea['percentYes'], idea['percentNo'])
        #    dataString += entry
        # clip the last ',' off this string
        #dataString = dataString[:-1]
        #dataString += "\n];"
        #### attempt1 done ####

        # attempt2 work with a json object

    %>
    <style>
        #chart {
          background-color: #fff;
        }
        svg {
          display: block;
          margin-bottom: 10px;
        }
        .totals line {
          stroke-width: 2px;
          stroke: #f88;
        }
        .yeses line {
          stroke-width: 2px;
          stroke: #88f;
        }
        text {
          font-size: 13px;
          font-family: sans-serif;
        }
        text.small {
          font-size: 10px;
          fill: #666;
        }
    </style>
    <script>
        var w = 900;
        var h = 220;
        // hi todd here
        //console.log( $ { stats | n } );
        //var jsonData = JSON.parse( stats );

        var data = ${stats | n}
        
        /*var data = [
          {'i':  0,'title': 'more cones',   'total': 147, 'yes': 55.6},
          {'i':  1,'title': 'less braf',  'total': 50, 'yes': 83.5},
          {'i':  2,'title': 'be cooler than..',     'total': 53, 'yes': 93.7},
          {'i':  3,'title': 'its just too easy to..',     'total': 158, 'yes': 32.7},
          {'i':  4,'title': 'more office space',       'total': 64, 'yes': 51.9},
          {'i':  5,'title': 'i had it up to here',      'total': 70, 'yes': 81.6},
          {'i':  6,'title': 'no way is this gonna..',      'total': 76, 'yes': 0.7},
          {'i':  7,'title': 'vote on stuff',    'total': 176, 'yes': 10.9},
          {'i':  8,'title': 'whos your daddy', 'total': 70, 'yes': 51.5},
          {'i':  9,'title': 'slap it',   'total': 59, 'yes': 63.5},
          {'i': 10,'title': 'more please',  'total': 5, 'yes': 56.6},
          {'i': 11,'title': 'hos up gs up',  'total': 45, 'yes': 45.4},
        ];*/
        

        var dataTitleLink = function(d) {
            var objectLink = '<a href="http://www.thehomie.com">' + d['title'].substr(0, 7) + '..' + '</a>';
            return objectLink;
        };
        var dataTitle = function(d) {
            var title = d['title'].substr(0, 7) + '..';
            return title;
        };
        var dataTotal = function(d) { return d['totalVotes']; };
        var dataYes = function(d) { return d['percentYes']; };
        var keyFn = dataTitle;

        // new: .domain([0, d3.max(data, dataTotal)])
        // orig: .domain(d3.extent(data, dataTotal))
        var totalScale = d3.scale.linear()
            .domain(d3.extent(data, dataTotal))
            .range([100, 0]);
        var yesScale = d3.scale.linear()
            //.domain([0, d3.max(data, dataYes)])
            .domain(d3.extent(data, dataYes))
            .range([50, 0]);
        var xScale = d3.scale.linear()
            .domain([0, data.length])
            .range([0, w]);
        var datumWidth = xScale(1) - xScale(0);
        //var datumWidth = 125;
        
        //console.log("xScale(1):"+xScale(1));

        var chart = d3.select('#chart').append('svg')
            .attr('width', w)
            .attr('height', h);
        var totalG = chart.append('g').attr('class', 'totals')
            //.attr('transform', 'translate(0, 20)');
            // place the totals below the lowest yesPercent score, give a 10px buffer:
            .attr('transform', 'translate(' + [0, 30 + d3.max(yesScale.range())] + ')');
        var yesG = chart.append('g').attr('class', 'yeses')
            // move the yespercent listings 20px down into the chart area
            .attr('transform', 'translate(0, 20)');
            //.attr('transform', 'translate(' + [0, 30 + d3.max(totalScale.range())] + ')');

        var title = chart.append('text')
            .attr('x', w / 2)
            .attr('y', h - 10)
            .attr('text-anchor', 'middle')
            .text('Vote Distribution');
        var dataLink = chart.append('a')
            .attr('xlink:href', 'https://civinomics.com');
        dataLink.append('text')
            .attr('class', 'small')
            .attr('x', w / 2)
            .attr('y', h)
            .attr('text-anchor', 'middle')
            .text('[source]');


        var drawChart = function() {
            var totalGs = totalG.selectAll('g.tick').data(data, keyFn);
            var newTotalGs = totalGs.enter().append('g')
                  .attr('class', 'tick');
              totalGs.transition().duration(1000)
                  .attr('transform', function(d, i) {
                    return 'translate(' + [xScale(i) + datumWidth / 2, totalScale(dataTotal(d))] + ')';
                  })
              newTotalGs.append('line')
                  .attr('x1', -datumWidth / 2)
                  .attr('x2', datumWidth / 2);
              newTotalGs.append('text')
                  .attr('class', 'small')
                  .attr('text-anchor', 'middle')
                  .attr('dy', '-0.3em');
              totalGs.select('text')
                  .text(function(d) { return dataTotal(d) + 'v'; });
            
            
            var yesGs = yesG.selectAll('g.tick').data(data, keyFn);


            var newYesGs = yesGs.enter().append('g')
                  .attr('class', 'tick');
              yesGs.transition().duration(1000)
                  .attr('transform', function(d, i) {
                    return 'translate(' + [xScale(i) + datumWidth / 2, yesScale(dataYes(d))] + ')';
                  })
              newYesGs.append('line')
                  .attr('x1', -datumWidth / 2)
                  .attr('x2', datumWidth / 2);
              newYesGs.append('text')
                  .attr('class', 'small')
                  .attr('text-anchor', 'middle')
                  .attr('dy', '-0.3em');
              yesGs.select('text')
                  .text(function(d) { return dataYes(d) + '%'; });
            
            
            var labels = chart.selectAll('text.title').data(data, keyFn);

            /* works but text doesn't transition
            var labels = chart.selectAll('text.title')
                .data(data, keyFn)
                .enter().append("svg:a")
                .attr("xlink:href", "http://www.thehomie.com")
                    .append("text")
                    .attr('class', 'title small')
                    .attr('y', h - 25)
                    .attr('text-anchor', 'middle');
            
            labels.transition().duration(1000)
                .attr('x', function(d, i) { return xScale(i) + datumWidth / 2; })
                .text(function(d) { return dataTitle(d); });
            */

            /* kinda works - no x transition
            labels.enter().append("svg:a")
                .attr("xlink:href", "http://www.thehomie.com")
                    .append('text')
                    .attr('class', 'title small')
                    .attr('text-anchor', 'middle');
            labels.transition().duration(1000)
                .attr('x', function(d, i) { return xScale(i) + datumWidth / 2; })
                .attr('y', h - 25)
                .text(function(d) { return dataTitle(d); });
            */

            //        .attr("dx", 0)
            //        .attr("dy", "1em") // Controls padding to place text above bars
            //        .text(function(d) { return d.xCoordinate;})
            //        .attr("fill", "Black");
            
            
            // would be nice to link back to the ideas / objects themselves
            //labels.append("svg:a")
            //    .attr("xlink:href", function(d){return d['link'];});
            
            // standard form works
            labels.enter().append('text')
                .attr('class', 'title small')
                .attr('y', h - 25)
                .attr('text-anchor', 'middle');
            labels.transition().duration(1000)
                .attr('x', function(d, i) { return xScale(i) + datumWidth / 2; })
                .text(function(d) { return dataTitle(d); });

        };


        drawChart();
        var makeSortButton = function(field, rev) {
          return d3.select('#chart').append('button')
              .on('click', function() {
                data.sort(function(a, b) { return rev * (a[field] - b[field]); });
                drawChart();
              });
        };
        makeSortButton('i', 1).text('Sort by date');
        makeSortButton('totalVotes', -1).text('Sort by total');
        makeSortButton('percentYes', -1).text('Sort by percent yes');
    </script>
</%def>

<%def name="showSortChart1Example()">
    <div id="chart"></div>
</%def>

<%def name="sortChart1Example(stats)">
    <style>
        #chart {
          background-color: #fff;
        }
        svg {
          display: block;
          margin-bottom: 10px;
        }
        .highs line {
          stroke-width: 2px;
          stroke: #f88;
        }
        .rains line {
          stroke-width: 2px;
          stroke: #88f;
        }
        text {
          font-size: 13px;
          font-family: sans-serif;
        }
        text.small {
          font-size: 10px;
          fill: #666;
        }
    </style>
    <script>
        var w = 300;
        var h = 220;

        var data = [
          {'i':  0,'month': 'January',   'high': 47, 'rain': 5.6},
          {'i':  1,'month': 'February',  'high': 50, 'rain': 3.5},
          {'i':  2,'month': 'March',     'high': 53, 'rain': 3.7},
          {'i':  3,'month': 'April',     'high': 58, 'rain': 2.7},
          {'i':  4,'month': 'May',       'high': 64, 'rain': 1.9},
          {'i':  5,'month': 'June',      'high': 70, 'rain': 1.6},
          {'i':  6,'month': 'July',      'high': 76, 'rain': 0.7},
          {'i':  7,'month': 'August',    'high': 76, 'rain': 0.9},
          {'i':  8,'month': 'September', 'high': 70, 'rain': 1.5},
          {'i':  9,'month': 'October',   'high': 59, 'rain': 3.5},
          {'i': 10,'month': 'November',  'high': 51, 'rain': 6.6},
          {'i': 11,'month': 'December',  'high': 45, 'rain': 5.4},
        ];


        var dataMonth = function(d) { return d['month']; };
        var dataHigh = function(d) { return d['high']; };
        var dataRain = function(d) { return d['rain']; };
        var keyFn = dataMonth;


        var highScale = d3.scale.linear()
            .domain(d3.extent(data, dataHigh))
            .range([100, 0]);
        var rainScale = d3.scale.linear()
            .domain([0, d3.max(data, dataRain)])
            .range([50, 0]);
        var xScale = d3.scale.linear()
            .domain([0, data.length])
            .range([0, w]);
        var datumWidth = xScale(1) - xScale(0);

        var chart = d3.select('#chart').append('svg')
            .attr('width', w)
            .attr('height', h);
        var highG = chart.append('g').attr('class', 'highs')
            .attr('transform', 'translate(0, 20)');
        var rainG = chart.append('g').attr('class', 'rains')
            .attr('transform', 'translate(' + [0, 30 + d3.max(highScale.range())] + ')');

        var title = chart.append('text')
            .attr('x', w / 2)
            .attr('y', h - 10)
            .attr('text-anchor', 'middle')
            .text('Seattle Climate');
        var dataLink = chart.append('a')
            .attr('xlink:href', 'http://en.wikipedia.org/wiki/Seattle');
        dataLink.append('text')
            .attr('class', 'small')
            .attr('x', w / 2)
            .attr('y', h)
            .attr('text-anchor', 'middle')
            .text('[source]');


        var drawChart = function() {
            var highGs = highG.selectAll('g.tick').data(data, keyFn);
            var newHighGs = highGs.enter().append('g')
                  .attr('class', 'tick');
              highGs.transition().duration(1000)
                  .attr('transform', function(d, i) {
                    return 'translate(' + [xScale(i) + datumWidth / 2, highScale(dataHigh(d))] + ')';
                  })
              newHighGs.append('line')
                  .attr('x1', -datumWidth / 2)
                  .attr('x2', datumWidth / 2);
              newHighGs.append('text')
                  .attr('class', 'small')
                  .attr('text-anchor', 'middle')
                  .attr('dy', '-0.3em');
              highGs.select('text')
                  .text(function(d) { return dataHigh(d) + '°F'; });
            
            
            var rainGs = rainG.selectAll('g.tick').data(data, keyFn);


            var newRainGs = rainGs.enter().append('g')
                  .attr('class', 'tick');
              rainGs.transition().duration(1000)
                  .attr('transform', function(d, i) {
                    return 'translate(' + [xScale(i) + datumWidth / 2, rainScale(dataRain(d))] + ')';
                  })
              newRainGs.append('line')
                  .attr('x1', -datumWidth / 2)
                  .attr('x2', datumWidth / 2);
              newRainGs.append('text')
                  .attr('class', 'small')
                  .attr('text-anchor', 'middle')
                  .attr('dy', '-0.3em');
              rainGs.select('text')
                  .text(function(d) { return dataRain(d) + '"'; });
            
            
            var labels = chart.selectAll('text.month').data(data, keyFn);
            
            
            labels.enter().append('text')
                  .attr('class', 'month small')
                  .attr('y', h - 25)
                  .attr('text-anchor', 'middle');
              labels.transition().duration(1000)
                  .attr('x', function(d, i) { return xScale(i) + datumWidth / 2; })
                  .text(function(d) { return dataMonth(d).substr(0, 3); });
            
            
        };


        drawChart();
        var makeSortButton = function(field, rev) {
          return d3.select('#chart').append('button')
              .on('click', function() {
                data.sort(function(a, b) { return rev * (a[field] - b[field]); });
                drawChart();
              });
        };
        var spitTest = function(testText) {
          return d3.select('#chart').append('p')
              .text(textText);
        };
        makeSortButton('i', 1).text('Sort by month');
        makeSortButton('high', -1).text('Sort by high temperature');
        makeSortButton('rain', -1).text('Sort by precipitation');
    </script>
</%def>

<%def name="showd3Bar3()">
    <div class="d3Bar3"></div>
</%def>

<%def name="d3Bar3(stats)">
    <%
        nIdea = stats['idea']
        nDiscussion = stats['discussion']
        nResource = stats['resource']
        nComment = stats['comment']
        ideaText = "Idea"
        if nIdea > 1: ideaText += "s"
        discussionText = "Discussion"
        if nDiscussion > 1: discussionText += "s"
        resourceText = "Resource"
        if nResource > 1: resourceText += "s"
        commentText = "Comment"
        if nComment > 1: commentText += "s"

    %>
    <style>

        .bar {
          fill: steelblue;
        }

        .bar:hover {
          fill: green;
        }

        .axis {
          font: 10px sans-serif;
        }

        .axis path,
        .axis line {
          fill: none;
          stroke: #000;
          shape-rendering: crispEdges;
        }

        .x.axis path {
          display: none;
        }

    </style>
    <script>

        var margin = {top: 20, right: 20, bottom: 30, left: 40},
            width = 960 - margin.left - margin.right,
            height = 500 - margin.top - margin.bottom;

        var x = d3.scale.ordinal()
            .rangeRoundBands([0, width], .1);

        var y = d3.scale.linear()
            .range([height, 0]);
        
        var svg = d3.select(".d3Bar3").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var data = [
            {name: "${ideaText}",    value:  ${nIdea}},
            {name: "${discussionText}",    value:  ${nDiscussion}},
            {name: "${resourceText}",     value: ${nResource}},
            {name: "${commentText}",   value: ${nComment}}
        ];

        x.domain(data.map(function(d) { return d.name; }));
        y.domain([0, d3.max(data, function(d) { return d.value; })]);

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom");

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left")
            .ticks(d3.max(data, function(d) { return d.value; }), "");

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
          .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Posts");

        svg.selectAll(".bar")
            .data(data)
          .enter().append("rect")
            .attr("class", "bar")
            .attr("x", function(d) { return x(d.name); })
            .attr("width", x.rangeBand())
            .attr("y", function(d) { return y(d.value); })
            .attr("height", function(d) { return height - y(d.value); });

    </script>
</%def>

<%def name="showd3Bar2(stats)">

    <svg class="chart2"></svg>

</%def>

<%def name="d3Bar2(stats)">
    <%
        nIdea = stats['idea']
        nDiscussion = stats['discussion']
        nResource = stats['resource']
        nComment = stats['comment']
        ideaText = "Idea"
        if nIdea > 1: ideaText += "s"
        discussionText = "Discussion"
        if nDiscussion > 1: discussionText += "s"
        resourceText = "Resource"
        if nResource > 1: resourceText += "s"
        commentText = "Comment"
        if nComment > 1: commentText += "s"

    %>
    <style>

        .chart2 rect {
          fill: steelblue;
        }

        .chart2 text {
          fill: white;
          font: 10px sans-serif;
          text-anchor: end;
        }

    </style>
    <script>

        var width = 420,
            barHeight = 20;

        var x = d3.scale.linear()
            .range([0, width]);

        var chart = d3.select(".chart2")
            .attr("width", width);

        // var data = ["", "${nDiscussion}", "${nResource}", "${nComment}"];
        var data = [
            {name: "${ideaText}",    value:  ${nIdea}},
            {name: "${discussionText}",    value:  ${nDiscussion}},
            {name: "${resourceText}",     value: ${nResource}},
            {name: "${commentText}",   value: ${nComment}}
        ];        

        x.domain([0, d3.max(data, function(d) { return d.value; })]);

        chart.attr("height", barHeight * data.length);

        var bar = chart.selectAll("g")
            .data(data)
          .enter().append("g")
            .attr("transform", function(d, i) { return "translate(0," + i * barHeight + ")"; });

        bar.append("rect")
            .attr("width", function(d) { return x(d.value); })
            .attr("height", barHeight - 1);

        bar.append("text")
            .attr("x", function(d) { return x(d.value) - 3; })
            .attr("y", barHeight / 2)
            .attr("dy", ".35em")
            .text(function(d) { return d.value; });

    </script>
</%def>

<%def name="showd3Bar(stats)">
    
    <div class="chart">
    </div>

</%def>

<%def name="d3Bar(stats)">
    <%

        nDiscussion = stats['discussion']
        nResource = stats['resource']
        nIdea = stats['idea']
        nComment = stats['comment']

    %>
    <style>

        .chart div {
            font: 10px sans-serif;
            text-align: right;
            padding: 3px;
            margin: 1px;
            color: white;
        }

    </style>
    <script>

        var data = ["${nIdea}", "${nDiscussion}", "${nResource}", "${nComment}"];

        var x = d3.scale.linear()
            .domain([0, d3.max(data)])
            .range([0, d3.max(data)*10]);

        d3.select(".chart")
            .selectAll("div")
                .data(data)
            .enter().append("div")
                .style("width", function(d) { return x(d) + "px"; })
                .style("background-color", function(d, i) { return i % 2 ? "steelblue" : "blue";})
                .text(function(d) { return d; });

    </script>
</%def>