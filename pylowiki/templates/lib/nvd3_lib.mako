<%!    
    import logging
    log = logging.getLogger(__name__)
%>

################################################
## NVD3 library
################################################

<%def name="initiativeStackedGroupedData(sbgData, sbgData2)">

    <style>
        #chartViews {
          height: 330px;
        }
        #chartViews svg {
          height: 300px;
        }

        #chartVotes {
          height: 330px;
        }
        #chartVotes svg {
          height: 300px;
        }

        #chartYesNo {
          height: 330px;
        }
        #chartYesNo svg {
          height: 300px;
        }

    </style>

    <h5>Views by Activity Type</h5>
    <div id="chartViews">
        <svg></svg>
    </div>

    <h5>Yes/No Votes by Date</h5>
    <div id="chartYesNo">
        <svg></svg>
    </div>

    <h5>Votes by Activity Type</h5>
    <div id="chartVotes">
        <svg></svg>
    </div>

    <link href="/nvd3/src/nv.d3.css" rel="stylesheet" type="text/css">
    <script id="nvd3On" src="/nvd3/lib/d3.v3.js"></script>
    <script src="/nvd3/nv.d3.min.js"></script>
   
    <script> 

        nv.addGraph(function() {
            var graphData = ${sbgData | n}

            var margin = {
              top: 5, 
              right: 10, 
              bottom: 65, 
              left: 55
            };
            var width = 900 - margin.left - margin.right;
            //var height = 300 - margin.top – margin.bottom;

            var chart = nv.models.multiBarChart()
                .margin({top: 5, right: 10, bottom: 65, left: 55})
                .width(width)
                .x(function(d) { return d['x'] })
                .y(function(d) { return d['y'] });

            chart.xAxis
              .rotateLabels(-45)
              .tickFormat(function(d) {
                return d3.time.format('%b %d %Y')(new Date(d))
              });

            chart.yAxis
              .tickFormat(d3.format(',.1f'));

            //console.log(exampleData());
            //console.log(graphData);
            d3.select('#chartViews svg')
              .datum(graphData)
            .transition().duration(500).call(chart);

          nv.utils.windowResize(chart.update);

          return chart;
        });

        nv.addGraph(function() {
            var graphData2 = ${sbgData2 | n}
            
            var margin = {
              top: 5, 
              right: 10, 
              bottom: 65, 
              left: 55
            };
            var width = 900 - margin.left - margin.right;
            //var height = 300 - margin.top – margin.bottom;

            var chart = nv.models.multiBarChart()
                .margin({top: 5, right: 10, bottom: 65, left: 55})
                .width(width)
                .x(function(d) { return d['x'] })
                .y(function(d) { return d['upsOrDowns'] });

            chart.xAxis
              .rotateLabels(-45)
              .tickFormat(function(d) {
                return d3.time.format('%b %d %Y')(new Date(d))
              });

            chart.yAxis
              .tickFormat(d3.format(',.1f'));

            //console.log(exampleData());
            //console.log(graphData2);
            d3.select('#chartYesNo svg')
              .datum(graphData2)
            .transition().duration(500).call(chart);

          nv.utils.windowResize(chart.update);

          return chart;
        });

        nv.addGraph(function() {
            var graphData = ${sbgData | n}
            
            var margin = {
              top: 5, 
              right: 10, 
              bottom: 65, 
              left: 55
            };
            var width = 900 - margin.left - margin.right;
            //var height = 300 - margin.top – margin.bottom;

            var chart = nv.models.multiBarChart()
                .margin({top: 5, right: 10, bottom: 65, left: 55})
                .width(width)
                .x(function(d) { return d['x'] })
                .y(function(d) { return d['numVotes'] });

            chart.xAxis
              .rotateLabels(-45)
              .tickFormat(function(d) {
                return d3.time.format('%b %d %Y')(new Date(d))
              });

            chart.yAxis
              .tickFormat(d3.format(',.1f'));

            //console.log(exampleData());
            //console.log(graphData);
            d3.select('#chartVotes svg')
              .datum(graphData)
            .transition().duration(500).call(chart);

          nv.utils.windowResize(chart.update);

          return chart;
        });

        function exampleData() {
          return stream_layers(3,10+Math.random()*100,.1).map(function(data, i) {
            return {
              key: 'Stream' + i,
              values: data
            };
          });
        }
        /* Inspired by Lee Byron's test data generator. */
        function stream_layers(n, m, o) {
          if (arguments.length < 3) o = 0;
          function bump(a) {
            var x = 1 / (.1 + Math.random()),
                y = 2 * Math.random() - .5,
                z = 10 / (.1 + Math.random());
            for (var i = 0; i < m; i++) {
              var w = (i / m - y) * z;
              a[i] += x * Math.exp(-w * w);
            }
          }
          return d3.range(n).map(function() {
              var a = [], i;
              for (i = 0; i < m; i++) a[i] = o + o * Math.random();
              for (i = 0; i < 5; i++) bump(a);
              return a.map(stream_index);
            });
        }

        /* Another layer generator using gamma distributions. */
        function stream_waves(n, m) {
          return d3.range(n).map(function(i) {
            return d3.range(m).map(function(j) {
                var x = 20 * j / m - i / 3;
                return 2 * x * Math.exp(-.5 * x);
              }).map(stream_index);
            });
        }

        function stream_index(d, i) {
          return {x: i, y: Math.max(0, d)};
        }
    </script>
</%def>

<%def name="searchPageInitiativePopularity(jsonInitiatives)">
    
    <style>
        #chart {
          height: 330px;
        }
        #chart svg {
          height: 300px;
        }

    </style>


    <div id="chart">
        <svg></svg>
    </div>

    <link href="/nvd3/src/nv.d3.css" rel="stylesheet" type="text/css">
    <script id="nvd3On" src="/nvd3/lib/d3.v3.js"></script>
    <script src="/nvd3/nv.d3.min.js"></script>

    
    <script> 
        
      var allData = ${jsonInitiatives | n}
      //console.log('yo');
      console.log(allData);
      //console.log('mtv raps');
        
      nv.addGraph(function() {
        var chart = nv.models.multiBarHorizontalChart()
            .x(function(d) { return d['label'] })
            .y(function(d) { return d.value })
            .margin({top: 5, right: 25, bottom: 15, left: 5})
            .showValues(false)
            .tooltips(true)
            .showControls(false)
            .height(300)
            .width(200)
            .yDomain([0,100]);

        chart.yAxis
            .tickFormat(d3.format(',d'));

        d3.select('#chart svg')
            .datum(allData)
          .transition().duration(500)
            .call(chart);

        nv.utils.windowResize(chart.update);

        return chart;
      });
        
    </script>
</%def>

################################################
## votePieIncludes
## : usage
##  - this must be called on the same page as the following function, votePie
##  - this should be called once while multiple instances of votePie may be called
##  - e.g. nvd3Lib.votePieIncludes() called once on 6_workshop_home, 
##      ${lib_6.yesNoVote(c.thing, 'pieChart')} called with each idea listing on page
##      - or, ${nvd3Lib.votePieIncludes()} and ${lib_6.yesNoVote(c.thing, 'detail', 'pieChart')}
##        called together on an individual idea page
##      - NOTE votePie() is called from within the yesNoVote() function in 6_lib.mako 
##          when the 'pieChart' option is included
################################################
<%def name="votePieIncludes()">
    <link href="/nvd3/src/nv.d3.css" rel="stylesheet" type="text/css">
    <script id="nvd3On" src="/nvd3/lib/d3.v3.js"></script>
    <script src="/nvd3/nv.d3.min.js"></script>
    <script src="/nvd3/src/utils.js"></script>
    <script src="/nvd3/src/models/pie.js"></script>
</%def>

################################################
## votePie
## :usage
##  - votePie() is called from within the yesNoVote() function in 6_lib.mako when the
##   'pieChart' option is included: ${lib_6.yesNoVote(c.thing, 'detail', 'pieChart')}
##  -  votePieIncludes() must be called once on the same page for any instances of this function to work
## :params
##  - percentYes: integer representing the percentage of yes votes
##  - pieCode: string representing the urlCode of the object this is associated with
##      pieCode is used to match the javascript with the <svg tag that will be used for the graph
## :bugs
##  - on a page with multiple instances, only some of them display
##      ANSWER: this is because javascript is non-blocking. an asynchronous waterfall routine is needed
## :to do
##  - get the pie to generate based on the yes or no vote of the user if that vote changes or is submitted
################################################
<%def name="votePie(percentYes, pieCode)">
    <%
        yes = percentYes
        no = 100 - yes
    %>
    <svg id="pie${pieCode}" class="yesNoPie"></svg>

    <style>
        .ynScoreWrapper{
            padding-top: 0px;
        }

        .yesNoPie {
            position: relative;
            top: -14px;
        }

        .noScore{
            position: relative;
            top: 10px;
        }

    </style>

    <script> 

        var testdata = [
            { 
                key: "${no}%",
                y: ${no}
            },
            { 
                key: "${yes}%",
                y: ${yes}
            }
        ];

        var selectString = "#pie" + "${pieCode}";
        console.log("slst: " + selectString);
        console.log("y/n: " + "${yes} ${no}");

        nv.addGraph(function() {
            //var width = nv.utils.windowSize().width - 40,
            //    height = nv.utils.windowSize().height / 2 - 40;
            var width = 40,
                height = 40;

            var chart = nv.models.pie()
                .values(function(d) { return d })
                .width(width)
                .height(height)
                .donut(true);

            d3.select(selectString)
                .datum([testdata])
              .transition().duration(400)
                .attr('width', width)
                .attr('height', height)
                .call(chart);

            return chart;
        });
      
    </script>
</%def>