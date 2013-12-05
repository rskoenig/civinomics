<%!    
    import logging
    log = logging.getLogger(__name__)
%>

################################################
## NVD3 library
################################################

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