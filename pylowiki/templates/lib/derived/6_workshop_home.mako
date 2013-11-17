<%!
   import pylowiki.lib.db.workshop     as workshopLib
   import pylowiki.lib.db.slideshow as slideshowLib
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

<%def name="whoListening()">
    <%
        users = []
        pending = []
        for listener in c.listeners:
            if 'userCode' in listener:
                user = getThing(listener['userCode'])
                users.append(user)
            else:
                pending.append(listener)
    %>
    <h4 class="section-header smaller section-header-inner">Listeners</h4>
    % if users:
        <ul class="media-list" id="workshopNotables">
        % for person in users:
            <%
                personTitle = person['name']
                personClass = 'listener'
            %>
            <li class="media notables-item">
                ${lib_6.userImage(person, className="avatar med-avatar media-object", linkClass="pull-left")}
                <div class="media-body">
                    ${lib_6.userLink(person, className="listener-name")}<br />
                    <small>${personTitle}</small>
                </div>
            </li>
            
        % endfor
        </ul>
     % endif
    % if pending:
        <hr>
        <div><p><em class="grey">Not yet participating. Invite them to join in.</em></p></div>
        <ul class="media-list" id="workshopNotables">
        % for person in pending:
            <%
                lName = person['name']
                lTitle = person['title']
                listenerCode = person['urlCode']
                personClass = 'pendingListener'
                if person['invites'] != '':
                    inviteList = person['invites'].split(',')
                    numInvites = str(len(inviteList))
                else:
                    numInvites = '0'
            %>
            <li class="media notables-item">
                % if 'user' in session and c.authuser:
                    <div class="pull-left rightbuttonspacing"><a href="#invite${listenerCode}" class="btn btn-primary btn-mini" data-toggle="modal"><i class="icon-envelope icon-white"></i> Invite</a></div>
                % else:
                    <div class="pull-left rightbuttonspacing"><a href="/workshop/${c.w['urlCode']}/${c.w['url']}/login/idea" class="btn btn-primary btn-mini"><i class="icon-envelope icon-white"></i> Invite</a></div>
                % endif
                <div class="media-body">
                    <span class="listener-name">${lName}</span><br />
                    <small>${lTitle}</small> 
                </div>
                % if 'user' in session and c.authuser:
                    <%
                        memberMessage = "Please join me and participate in this online Civinomics workshop.\nThere are good ideas and informed discussions, please login and listen in!"
                    %>
                    <div id="invite${listenerCode}" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="invite${listenerCode}Label" aria-hidden="true">
                        <div class="modal-header">
                            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                            <h3 id="invite${listenerCode}Label">Invite ${lName} to Listen</h3>
                        </div><!-- modal-header -->
                        <div class="modal-body"> 
                            <form ng-controller="listenerController" ng-init="code='${c.w['urlCode']}'; url='${c.w['url']}'; user='${c.authuser['urlCode']}'; listener='${listenerCode}'; memberMessage='${memberMessage}'" id="inviteListener" ng-submit="emailListener()" class="form-inline" name="inviteListener">
                            Add your message to the listener invitation:<br />
                            <textarea rows="6" class="field span12" ng-model="memberMessage" name="memberMessage">{{memberMessage}}</textarea>
                            <br />
                            <button class="btn btn-warning" data-dismiss="modal" aria-hidden="true">Close</button>
                            <button type="submit" class="btn btn-warning">Send Invitation</button>
                            <br />
                            <span ng-show="emailListenerShow">{{emailListenerResponse}}</span>
                            </form>
                        </div><!-- modal-footer -->
                    </div><!-- modal -->
                % endif
            </li>
        % endfor
        </ul>
        <hr>
     % endif
     % if 'user' in session and c.authuser:
        <ul class="media-list">
            <li class="media pendingListener notables-item">
                <em class="grey">Which public officials should participate?</em><br />
                <form ng-controller="listenerController" ng-init="code='${c.w['urlCode']}'; url='${c.w['url']}'; user='${c.authuser['urlCode']}'; suggestListenerText='';" id="suggestListenerForm" ng-submit="suggestListener()" class="form-inline suggestListener" name="suggestListenerForm">
                <input class="listenerInput" type="text" ng-model="suggestListenerText" name="suggestListenerText" placeholder="Suggest a Listener"  required>
                <button type="submit" class="btn btn-success btn-small">Submit</button>
                <br />
                <span ng-show="suggestListenerShow">{{suggestListenerResponse}}</span>
                </form>
            </li>
        </ul><!-- media-list -->
    % endif
</%def>

<%def name="showFacilitators()">
    % for facilitator in c.facilitators:
        Facilitator: ${lib_6.userLink(facilitator)}<br />
    % endfor
</%def>

<%def name="showActivity(activity)">
    <%
        numItems = 5
        shownItems = 0
    %>
    
    % for item in activity:
      <div class="media"  id="workshopActivity">
        <%
          if c.demo:
              author = getUserByID(item.owner)
              if not c.privs['admin']:
                  if 'user' in session:
                      if ((author['accessLevel'] != '300' and not facilitatorLib.isFacilitator(author, c.w)) and author.id != c.authuser.id):
                          continue
                  else:
                      if author['accessLevel'] != '300' and not facilitatorLib.isFacilitator(author, c.w):
                          continue
          if shownItems >= numItems:
              break
        %>
        <div class="pull-left">
          ${lib_6.userImage(getUserByID(item.owner), className="avatar small-avatar inline")}
        </div>
        <div class="media-body">
          ${lib_6.userLink(item.owner, className = "green green-hover", maxChars = 25)}
          ${lib_6.showItemInActivity(item, c.w, expandable = True)}
        </div>
      </div>
    % endfor
    
</%def>

<%def name="showSortChart1()">
    <div id="chart"></div>
</%def>

<%def name="sortChart1(stats)">
    <%
        # hi!
        spit =  ""
        for idea in stats:
            spit += " <p>%s</p>"%idea['views']
    
    %>
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
        makeSortButton('i', 1).text('Sort by month');
        makeSortButton('high', -1).text('Sort by high temperature');
        makeSortButton('rain', -1).text('Sort by precipitation');
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
        makeSortButton('i', 1).text('Sort by month');
        makeSortButton('high', -1).text('Sort by high temperature');
        makeSortButton('rain', -1).text('Sort by precipitation');
    </script>
    <p>${spit}</p>
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

<%def name="watchButton()">
    % if 'user' in session:
        % if c.isFollowing:
            <button class="btn btn-civ pull-right followButton following" data-URL-list="workshop_${c.w['urlCode']}_${c.w['url']}" rel="tooltip" data-placement="bottom" data-original-title="this workshop" id="workshopBookmark"> 
            <span><i class="icon-bookmark btn-height icon-light"></i><strong> Bookmarked </strong></span>
            </button>
        % else:
            <button class="btn pull-right followButton" data-URL-list="workshop_${c.w['urlCode']}_${c.w['url']}" rel="tooltip" data-placement="bottom" data-original-title="this workshop" id="workshopBookmark"> 
             <span><i class="icon-bookmark med-green"></i><strong> Bookmark </strong></span>
            </button>
        % endif
    % endif
</%def>

<%def name="watchButtonListing(w)">
    % if 'user' in session:
        <button class="btn btn-civ pull-right followButton following" data-URL-list="workshop_${w['urlCode']}_${w['url']}" rel="tooltip" data-placement="bottom" data-original-title="this workshop" id="workshopBookmark"> 
        <span><i class="icon-bookmark btn-height icon-light"></i> Bookmarked </span>
        </button>
    % endif
</%def>

<%def name="configButton(w)">
   <% workshopLink = "%s/preferences" % lib_6.workshopLink(w, embed = True, raw = True) %>
   <a class="btn btn-civ pull-right preferencesLink left-space" href="${workshopLink | n}" rel="tooltip" data-placement="bottom" data-original-title="workshop moderation and configuration"><span><i class="icon-wrench icon-white pull-left"></i></span></a>
</%def>

<%def name="previewButton()">
  <a class="btn btn-civ pull-right" href="${lib_6.workshopLink(c.w, embed=True, raw=True)}"><span><i class="icon-eye-open icon-white pull-left"></i> Preview </span></a>
</%def>

<%def name="viewButton()">
  <a class="btn btn-civ pull-right" href="${lib_6.workshopLink(c.w, embed=True, raw=True)}"><span><i class="icon-eye-open icon-white pull-left"></i> View </span></a>
</%def>

<%def name="workshopNavButton(workshop, count, objType, active = False)">
    <%
        imageMap = {'discussion':'/images/glyphicons_pro/glyphicons/png/glyphicons_244_conversation.png',
                    'idea':'/images/glyphicons_pro/glyphicons/png/glyphicons_064_lightbulb.png',
                    'resource':'/images/glyphicons_pro/glyphicons/png/glyphicons_050_link.png',
                    'home':'/images/glyphicons_pro/glyphicons/png/glyphicons_020_home.png',
                    'information':'/images/glyphicons_pro/glyphicons/png/glyphicons_318_more_items.png',
                    'activity':'/images/glyphicons_pro/glyphicons/png/glyphicons_057_history.png'}
        titleMap = {'discussion':' Forum',
                    'idea':' Vote',
                    'resource':' Links',
                    'home':' Home',
                    'information':' Information',
                    'activity':'Activity'}
        linkHref = lib_6.workshopLink(workshop, embed = True, raw = True)
        if objType != 'home':
            linkHref += '/' + objType
        linkClass = 'btn workshopNav'
        if active:
            linkClass += ' selected-nav'
        linkID = objType + 'Button'
    %>
    <a class="${linkClass}" id="${linkID}" href = "${linkHref | n}"> <img class="workshop-nav-icon" src="${imageMap[objType] | n}"> ${titleMap[objType]}
    (${count})
    </a>
</%def>

<%def name="workshopNav(w, listingType)">
   <% 
      activity = activityLib.getActivityForWorkshop(w['urlCode'])
      discussionCount = 0
      ideaCount = 0
      resourceCount = 0
      activityCount = len(activity)
      for item in activity:
         if c.demo:
            author = getUserByID(item.owner)
            if not c.privs['admin']:
               if 'user' in session:
                  if ((author['accessLevel'] != '300' and not facilitatorLib.isFacilitator(author, c.w)) and author.id != c.authuser.id):
                     continue
               else:
                  if author['accessLevel'] != '300' and not facilitatorLib.isFacilitator(author, c.w):
                     continue
         
         if item.objType == 'discussion':
            discussionCount += 1
         elif item.objType == 'idea':
            ideaCount += 1
         elif item.objType == 'resource':
            resourceCount += 1
   %>
   <div class="btn-group four-up">
   <% 
      if listingType == 'resources' or listingType == 'resource':
         workshopNavButton(w, ideaCount, 'home')
         workshopNavButton(w, resourceCount, 'information', active = True)
         workshopNavButton(w, discussionCount, 'discussion')
         workshopNavButton(w, activityCount, 'activity')
      elif listingType == 'discussion':
         workshopNavButton(w, ideaCount, 'home')
         workshopNavButton(w, resourceCount, 'information')
         workshopNavButton(w, discussionCount, 'discussion', active = True)
         workshopNavButton(w, activityCount, 'activity')
      elif listingType == 'ideas' or listingType == 'idea':
         workshopNavButton(w, ideaCount, 'home', active = True)
         workshopNavButton(w, resourceCount, 'information')
         workshopNavButton(w, discussionCount, 'discussion')
         workshopNavButton(w, activityCount, 'activity')
      elif listingType == 'activity':
         workshopNavButton(w, ideaCount, 'home')
         workshopNavButton(w, resourceCount, 'information')
         workshopNavButton(w, discussionCount, 'discussion')
         workshopNavButton(w, activityCount, 'activity', active = True)
      else:
         workshopNavButton(w, ideaCount, 'home')
         workshopNavButton(w, resourceCount, 'information')
         workshopNavButton(w, discussionCount, 'discussion')
         workshopNavButton(w, activityCount, 'activity')
   %>
   </div>
</%def>

<%def name="imagePreviewer(w)">
  <!-- using the data-clearing twice on a page leads to slide skipping this function allows a preview but will not launch slideshow -->
  <% 
    images = slideshowLib.getSlidesInOrder(slideshowLib.getSlideshow(w))
    count = 0
  %>
  <ul class="gallery thumbnails no-bottom">
    % for image in images:
      <% 
        imageFormat = 'jpg'
        if 'format' in image.keys():
          imageFormat = image['format']

        spanX = 'noShow'
        if count <= 5:
          spanX = 'span4'
      %>
      % if image['deleted'] != '1':
        <li class="${spanX} slideListing">
          % if image['pictureHash'] == 'supDawg':
             <a href="#moreimages" data-toggle="tab" ng-click="switchImages()">
                <img src="/images/slide/slideshow/${image['pictureHash']}.slideshow"/>
             </a>
          % else:
            <a href="#moreimages" data-toggle="tab" ng-click="switchImages()">
              <!-- div with background-image needed to appropirately size and scale image in workshop_home template -->
              <div class="slide-preview" style="background-image:url('/images/slide/${image['directoryNum']}/slideshow/${image['pictureHash']}.${imageFormat}');"/>
              </div>
            </a>
          % endif
        </li>
      % endif
      <% count += 1 %>
    % endfor
  </ul>
</%def>


<%def name="slideshow(w, *args)">
    <% 
        slides = slideshowLib.getSlidesInOrder(slideshowLib.getSlideshow(w)) 
        slideNum = 0
        spanX = ""
        if 'hero' in args:
          spanX = "span8"
    %>
    <div class="${spanX}">
        <ul class="gallery thumbnails no-bottom" data-clearing>
        <%
          for slide in slides:
            if slide['deleted'] != '1':
              if 'hero' in args:
                _slideListing(slide, slideNum, 'hero')
              else:
                _slideListing(slide, slideNum)
              slideNum += 1
        %>
        </ul>
    </div>
    % if 'hero' in args:
        <% infoHref = lib_6.workshopLink(c.w, embed = True, raw = True) + '/information' %>
        <div class="span4">
          <p class="description" style="color: #FFF; padding-top: 15px;">
            ${lib_6.ellipsisIZE(c.w['description'], 285)}
            <a href="${infoHref}">read more</a>
          </p>
        </div>
    % endif
</%def>

<%def name="_slideListing(showSlide, slideNum, *args)">
    <%
      if slideNum == 0:
          spanX = "span12"
      else:
          spanX = "noShow"
      slideFormat = 'jpg'
      if 'format' in showSlide.keys():
          slideFormat = showSlide['format']
    %>
    % if slideNum == 0 and 'hero' in args:
      <li class="${spanX} no-bottom">
      % if showSlide['pictureHash'] == 'supDawg':
          <a href="/images/slide/slideshow/${showSlide['pictureHash']}.slideshow">
          <div class="slide-hero" style="background-image:url('/images/slide/slideshow/${showSlide['pictureHash']}.slideshow');" data-caption="${showSlide['title']}"/></div>
          </a>
      % else:
          <a href="/images/slide/${showSlide['directoryNum']}/slideshow/${showSlide['pictureHash']}.${slideFormat}">
          <!-- img class is needed by data-clearing to assemble the slideshow carousel-->
          <img class="noShow"src="/images/slide/${showSlide['directoryNum']}/slideshow/${showSlide['pictureHash']}.${slideFormat}" data-caption="${showSlide['title']}"/>
          <!-- div with background-image needed to appropirately size and scale image in workshop_home template -->
          <div class="slide-hero" style=" background-image:url('/images/slide/${showSlide['directoryNum']}/slideshow/${showSlide['pictureHash']}.${slideFormat}');" data-caption="${showSlide['title']}"/>
              <div class="well slide-hero-caption">
                  <i class="icon-play"></i> Slideshow
              </div>
          </div>
          </a>
      % endif
      </li>
    % else:
      <li class="span4 slideListing">
        % if showSlide['pictureHash'] == 'supDawg':
           <a href="/images/slide/slideshow/${showSlide['pictureHash']}.slideshow">
              <img src="/images/slide/slideshow/${showSlide['pictureHash']}.slideshow" data-caption="${showSlide['title']}"/>
           </a>
        % else:
            <a href="/images/slide/${showSlide['directoryNum']}/slideshow/${showSlide['pictureHash']}.${slideFormat}">
              <!-- img class is needed by data-clearing to assemble the slideshow carousel-->
              <img class="noShow" src="/images/slide/${showSlide['directoryNum']}/slideshow/${showSlide['pictureHash']}.${slideFormat}" data-caption="${showSlide['title']}"/>
              <!-- div with background-image needed to appropirately size and scale image in workshop_home template -->
              <div class="slide-preview" style="background-image:url('/images/slide/${showSlide['directoryNum']}/slideshow/${showSlide['pictureHash']}.${slideFormat}');" data-caption="${showSlide['title']}"/>
              </div>
            </a>
        % endif
      </li>
    % endif
</%def>

<%def name="_slide(slide, slideNum, numSlides)">
  <!-- original code -->
   <% 
      if slideNum == 0:
         spanX = "span12"
      else:
         if slideNum <= 3:
            if numSlides == 2:
               spanX = "span4 offset4 thumbnail-gallery"
            elif numSlides == 3:
               spanX = "span4 offset1 thumbnail-gallery"
            elif numSlides >= 4:
               spanX = "span4 thumbnail-gallery"
         else:
            spanX = "noShow"
   %>
      <li class="${spanX}">
      % if slide['pictureHash'] == 'supDawg':
         <a href="/images/slide/slideshow/${slide['pictureHash']}.slideshow">
            <img src="/images/slide/slideshow/${slide['pictureHash']}.slideshow" data-caption="${slide['title']}"/>
         </a>
      % elif 'format' in slide.keys():
         <a href="/images/slide/${slide['directoryNum']}/slideshow/${slide['pictureHash']}.${slide['format']}">
            <img src="/images/slide/${slide['directoryNum']}/slideshow/${slide['pictureHash']}.${slide['format']}" data-caption="${slide['title']}"/>
         </a>
      % else:
         <a href="/images/slide/${slide['directoryNum']}/slideshow/${slide['pictureHash']}.jpg">
            <img src="/images/slide/${slide['directoryNum']}/slideshow/${slide['pictureHash']}.jpg" data-caption="${slide['title']}"/>
         </a>
      % endif
      % if slideNum == 0:
         <small class="centered">${slide['title']}</small>
      % endif
   </li>
</%def>

<%def name="showInfo(workshop)">
    <div>
    <p class="description" >
      ${c.w['description']}
    </p>
    % if c.information and 'data' in c.information: 
        <hr class="list-header">
        ${m.html(c.information['data'], render_flags=m.HTML_SKIP_HTML) | n}
    % endif
    </div>
</%def>

<%def name="showGoals(goals)">
    % if len(goals) == 0:
        <p>This workshop has no goals!</p>
    % else:
        <div id="workshopGoals">
        <ol class="workshop-goals">
        % for goal in goals:
            % if goal['status'] == '100':
                <li class="done-true"><span>${goal['title']}</span></li>
            % else:
                <li><span>${goal['title']}</span></li>
            % endif
        % endfor
        </ul>
        </div><!-- workshopGoals -->
    % endif
</%def>

<%def name="showScope()">
    <%
        if c.w['public_private'] == 'public':
            scopeName = c.scope['level']
            scopeString = 'Scope: '
            if scopeName == 'earth':
                scopeString += 'the entire planet Earth.'
            else:
                # More mapping for the postal code, this time to display Postal Code instead of just Postal.
                # The real fix for this is through use of message catalogs, which we will need to implement
                # when we support multiple languages in the interface, so for right now this kludge is
                # "good enough"
                if scopeName == 'postalCode':
                    scopeNeme = 'Postal Code '

                scopeString += "the " + scopeName.title() + " of "
                scopeString += c.scope['name']\
                        .replace('-', ' ')\
                        .title()
        else:
            scopeString = "Scope: This is a private workshop."
    %>
    ${scopeString | n}
</%def>

<%def name="displayWorkshopFlag(w, *args)">
    <%
        workshopFlag = '/images/flags/generalFlag.gif'
        href = '#'
        if w['public_private'] == 'public':
            scope = workshopLib.getPublicScope(w)
            href = scope['href']
            workshopFlag = scope['flag']
        else:
            workshopFlag = '/images/flags/generalGroup.gif'
        flagSize = 'med-flag'
        if 'small' in args:
          flagSize = 'small-flag'

    %>
    <a href="${href}"><img class="thumbnail span ${flagSize}" src="${workshopFlag}"></a>
</%def>
