<%!    
    import logging
    log = logging.getLogger(__name__)
%>

################################################
## NVD3 library
################################################

<%def name="searchPageInitiativePopularity(jsonInitiatives)">
    <%
        # for each initiative build an object
        # if percent < 50, calc negative version for series 1 place initiative in it
        # data = []
        # series1 = {"key":"Series1", "color":"#ddd", "values":[]}
        # series2 = {"key":"Series2", "color":"#ccc", "values":[]}
        # for iniative in initiatives:
        #   if percent > 50:
        #     # pecent 50 and above ranges 0 to 100% of right bar
        #     thisInit = {}
        #     thisInit["label"] = "%s, %s votes"%(initiative['title'], initiative['voteCount'])
        #     thisInit["value"] = initiative['percentYes'] * math for bar number
        #     series2["values"].append(thisInit)
        #   else:
        #   ..
        """
          var data = [
          {
            "key": "Series1",
            "color": "#d62728",
            "values": [
              { 
                "label" : "Group A" ,
                "value" : -1.8746444827653
              } , 
              { 
                "label" : "Group B" ,
                "value" : -8.0961543492239
              } , 
              { 
                "label" : "Group C" ,
                "value" : -0.57072943117674
              }
            ]
          },
          {
            "key": "Series2",
            "color": "#1f77b4",
            "values": [
              { 
                "label" : "Group A" ,
                "value" : 25.307646510375
              } , 
              { 
                "label" : "Group B" ,
                "value" : 16.756779544553
              }
            ]
          }
        ];
        """
        
    %>
    <style>

        #chart svg {
          height: 200px;
        }

    </style>


    <div id="chart">
        <svg></svg>
    </div>

    <link href="/nvd3/src/nv.d3.css" rel="stylesheet" type="text/css">
    <script id="nvd3On" src="/nvd3/lib/d3.v3.js"></script>
    <script src="/nvd3/nv.d3.min.js"></script>
    
    <script> 
        var inits = ${jsonInitiatives | n}
        console.log("yo rap");
        console.log(inits);
        console.log("end rap");
        var data = [
          {
            "key": "Series1",
            "color": "#d62728",
            "values": [
              { 
                "label" : "Group A" ,
                "value" : -1.8746444827653
              } , 
              { 
                "label" : "Group B" ,
                "value" : -8.0961543492239
              } , 
              { 
                "label" : "Group C" ,
                "value" : -0.57072943117674
              } , 
              { 
                "label" : "Group D" ,
                "value" : -2.4174010336624
              } , 
              {
                "label" : "Group E" ,
                "value" : -0.72009071426284
              } , 
              { 
                "label" : "Group F" ,
                "value" : -0.77154485523777
              } , 
              { 
                "label" : "Group G" ,
                "value" : -0.90152097798131
              } , 
              {
                "label" : "Group H" ,
                "value" : -0.91445417330854
              } , 
              { 
                "label" : "Group I" ,
                "value" : -0.055746319141851
              }
            ]
          },
          {
            "key": "Series2",
            "color": "#1f77b4",
            "values": [
              { 
                "label" : "Group A" ,
                "value" : 25.307646510375
              } , 
              { 
                "label" : "Group B" ,
                "value" : 16.756779544553
              } , 
              { 
                "label" : "Group C" ,
                "value" : 18.451534877007
              } , 
              { 
                "label" : "Group D" ,
                "value" : 8.6142352811805
              } , 
              {
                "label" : "Group E" ,
                "value" : 7.8082472075876
              } , 
              { 
                "label" : "Group F" ,
                "value" : 5.259101026956
              } , 
              { 
                "label" : "Group G" ,
                "value" : 0.30947953487127
              } , 
              { 
                "label" : "Group H" ,
                "value" : 0
              } , 
              { 
                "label" : "Group I" ,
                "value" : 0 
              }
            ]
          }
        ];
        nv.addGraph(function() {
          var chart = nv.models.multiBarHorizontalChart()
              .x(function(d) { return d.label })
              .y(function(d) { return d.value })
              .margin({top: 3, right: 2, bottom: 25, left: 1})
              .showValues(true)
              .tooltips(false)
              .showControls(false);

          chart.yAxis
              .tickFormat(d3.format(',.2f'));

          d3.select('#chart svg')
              .datum(data)
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