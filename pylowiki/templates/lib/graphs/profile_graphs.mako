<%!
    import pylowiki.lib.db.workshop     as workshopLib
    import pylowiki.lib.db.initiative   as initiativeLib
    import pylowiki.lib.db.facilitator  as facilitatorLib
    import pylowiki.lib.db.listener     as listenerLib
    import pylowiki.lib.db.follow       as followLib
    import pylowiki.lib.db.user         as userLib
    import pylowiki.lib.db.pmember      as pmemberLib
    import pylowiki.lib.db.generic      as genericLib
    import pylowiki.lib.utils           as utils
    
    import logging, os
    log = logging.getLogger(__name__)
%>

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="showWorkshopsJson()">
    ## I have the workshop list in json form now.
    ## print out all of the entries using angular
    ## this eventually make it easy to organize by role
    ## for now, just get the list out and set up links that'll fetch the activity for any
    ## listed workshop
</%def>

<%def name="showWorkshops(workshops, **kwargs)">
    <link href='/styles/progress_bars.css' rel='stylesheet' type='text/css'>
    <table class="table table-hover table-condensed"><tbody>
        % for workshop in workshops:
            <tr><td>
                <div class="media profile-workshop">
                    <a class="pull-left" ${lib_6.workshopLink(workshop)}>
                      <div class="thumbnail tight media-object" style="height: 60px; width: 90px; margin-bottom: 5px; background-image:url(${lib_6.workshopImage(workshop, raw=True) | n}); background-size: cover; background-position: center center;"></div>
                    </a>
                    <%
                        if 'imageOnly' in kwargs:
                            if kwargs['imageOnly'] == True:
                                return
                        if 'role' in kwargs:
                            role = kwargs['role']
                        else:
                            role = ''
                    %>
                    <div class="media-body">
                        <a ${lib_6.workshopLink(workshop)} class="listed-item-title media-heading lead bookmark-title">${workshop['title']}</a>
                        <span class="label label-inverse pull-right">${workshop['relation']}</span>
                        ${workshopGraphSimple(workshop)}
                    </div>
                </div>
            </td></tr>
        % endfor
    </tbody></table>
</%def>

################################################
## D3 graphs for the profile page
################################################

<%def name="includeD3()">
    <script src="/js/vendor/d3.v3.min.js" charset="utf-8"></script>
</%def>

##################################################
## function: listeningOverview()
## Upon first arriving at the profile page. We have
## a list of workshop objects to play with. In order to 
## save time and bandwidth this function is some eye candy
## that'll work with the workshop objects, giving the user a
## chance to dig into any one of them.
##################################################

<%def name="workshopGraphSimple(workshop)">
    <div style="margin-top: 10px;">
        <div class="row-fluid" >
            <div class="span2">
                    <p>
                        % if workshop['public_private'] == 'public':
                            Public
                        % else:
                            Private
                        % endif
                        </br>
                        % if workshop['published'] == '1':
                            Published
                        % elif workshop['deleted'] == '1':
                            Deleted
                        % elif workshop['disabled'] == '1':
                            Disabled
                        % endif
                    </p>
            </div>
            <div class="span4">

                Users can contribute:</br>
                % if workshop['allowDiscussions'] == '1':
                    <div class="settings-icon yes">
                % else:
                    <div class="settings-icon no">
                % endif
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Discussions</div>
                
                % if workshop['allowIdeas'] == '1':
                    <div class="settings-icon yes">
                % else:
                    <div class="settings-icon no">
                % endif
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ideas</div>
                
                % if workshop['allowResources'] == '1':
                    <div class="settings-icon yes">
                % else:
                    <div class="settings-icon no">
                % endif
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Resources</div>
                
                % if workshop['allowSuggestions'] == '1':
                    <div class="settings-icon yes">
                % else:
                    <div class="settings-icon no">
                % endif
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Listener Suggestions</div>
            </div><!-- span3 -->
            <div class="span2">
                facilitators
            </div><!-- span3 -->
            <div class="span4">
                <div class="row">
                    <div class="span6">
                        ${workshop['numPosts']} posts
                    </div>
                    <div class="span6">
                        <div class="meter orange nostripes">
                            <span id="post${workshop['urlCode']}" style="width: 0%"></span>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="span6">
                        ${workshop['numBookmarks']} bookmarks
                    </div>
                    <div class="span6">
                        <div class="meter red nostripes">
                            <span id="bookmark${workshop['urlCode']}" style="width: 0%"></span>
                        </div>
                    </div>
                </div>
            </div><!-- span3 -->
        </div><!-- row-fluid -->
    </div><!-- margin-top -->

</%def>

<%def name="workshopGraphOverview(workshop)">
    ## initialize the data we need for this page
    <%
        totalPosts = 0
        totalBookmarks = 0
        maxPosts = 0
        maxBookmarks = 0
        ##totalNotAllowing = {}
        for workshop in workshops:
            totalPosts += int(workshop['numPosts'])
            totalBookmarks += int(workshop['numBookmarks'])
            if int(workshop['numPosts']) > maxPosts:
                maxPosts = int(workshop['numPosts'])
            if int(workshop['numBookmarks']) > maxBookmarks:
                maxBookmarks = int(workshop['numBookmarks'])

        if maxPosts == 0:
            postLevel = int(workshop['numPosts']) / maxPosts
        else:
            postLevel = 0
        if maxBookmarks == 0:
            bookmarkLevel = int(workshop['numBookmarks']) / maxBookmarks
        else:
            bookmarkLevel = 0
    %>
    <link href='/styles/progress_bars.css' rel='stylesheet' type='text/css'>
    <div class="row">
        <div class="span5 offset1">
            <p>Highest number posts in this list: ${maxPosts}</p>
        </div>
        <div class="span6">
            <p>Highest number of bookmarks in this list: ${maxBookmarks}</p>
        </div>
    </div>
    <div class="media well searchListing">
        <div class="span7 offset1"><!-- left column -->
            <div class="row">
                <div class="span8">
                    <h4 class="media-heading">
                        <a href="${workshop['url']}">${workshop['title']}</a>
                    </h4>
                </div>
                <div class="span2">
                    <p>
                        % if workshop['public_private'] == 'public':
                            Public workshop
                        % else:
                            Private workshop
                        % endif
                    </p>
                </div>
                <div class="span2">
                    % if workshop['published'] == '1':
                        published
                    % elif workshop['deleted'] == '1':
                        Deleted
                    % elif workshop['disabled'] == '1':
                        Disabled
                    % endif
                </div>
            </div>
            <div class="row">
                <div class="span12">
                    scope
                </div>
            </div>
            <div class="row">
                <div class="span12">
                    % if workshop['allowDiscussions'] == '1':
                        Disc
                    % endif
                    % if workshop['allowIdeas'] == '1':
                        ideas 
                    % endif
                    ${workshop['allowResources']}
                    ${workshop['allowSuggestions']}
                </div>
            </div>
            <div class="row">
                <div class="span12">
                    ${workshop['facilitators']}
                    ${workshop['workshop_category_tags']}
                </div>
            </div>
        </div> <!-- end left column -->
        <div class="span4"> <!-- right column -->
            <div class="row">
                <div class="span4">
                    ${workshop['numPosts']} posts
                </div>
                <div class="span8">
                    <div class="meter orange nostripes">
                        <span style="width: 10%"></span>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="span4">
                    ${workshop['numBookmarks']} bookmarks
                </div>
                <div class="span8">
                    <div class="meter red nostripes">
                        <span style="width: 33.3%"></span>
                    </div>
                </div>
            </div>
        </div> <!-- end right column -->
    </div>
    
</%def>

<%def name="dcCommuterSurvey()">
  <div class='row-fluid' name="dc-data-top" data-spy="affix" data-offset-top="1150" >
    <div class="dc-data-count well" style="float: left; margin-top: 0;"> 
      <span> 
          <span class="filter-count"></span>
          selected out of
          <span class="total-count"></span> 
          records | <a href="#dc-data-top" name="dc-data-count" onclick="javascript:dc.filterAll(); dc.renderAll();">Reset</a> 
      </span>
    </div>
  </div>
  <div class='row-fluid'>   
    <div class='span4' id='dc-commuteDuration-chart'>
        <h4>How much time do you spend each day commuting over the hill and back?</h4> 
    </div>
    <div class='span4' id='dc-commuteType-chart'>
      <h4>How do you get to work over the hill?
        <span>
          <a class="reset" href="#dc-data-top" onclick="javascript:commuteTypeChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4> 
    </div>
    <div class='span4' id='dc-commuteActivity-chart'>
      <h4>What do you primarily do on the bus during your commute?
        <span>
          <br />(click to filter results)
          <a class="reset" href="#dc-data-top" onclick="javascript:commuteActivityChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
  </div><!-- row-fluid -->
  <hr>
  <div class="row-fluid">
    <div class='span4' id='dc-employmentType-chart'>
      <h4>What is your functional employment area at your current job?
        <span>
          <a class="reset" href="#dc-data-count" onclick="javascript:employmentTypeChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a>
        </span>
      </h4>
    </div>
    <div class='span4' id='dc-employmentDuration-chart'>
        <h4>How long have you been with your current employer?</h4> 
    </div>
    <div class='span4' id='dc-senority-chart'>
      <h4>What is your position or level of seniority?
        <span>
          <a class="reset" href="#dc-data-count" onclick="javascript:senorityChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
  </div><!-- row-fluid -->
  <hr>
  <div class="row-fluid">
    <div class='span4' id='dc-salary-chart'> 
      <h4>Salary Range
        <span>
            (drag sliders to filter results)
        </span>
      </h4>
    </div>
    <div class='span4' id='dc-whyCommute-chart'>
      <h4>Why do you choose to work over the hill? (Pick the MOST IMPORTANT reason).
        <span>
            <br>
            <a class="reset" href="#dc-data-count" onclick="javascript:whyCommuteChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
    <div class='span4' id='dc-whyLiveInSc-chart'>
      <h4>Why do you choose to live in Santa Cruz? (Pick the MOST IMPORTANT reason).
        <span>
          <br>
          <a class="reset" href="#dc-data-count" onclick="javascript:whyLiveInScChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
  </div><!-- row-fluid -->
  <hr>
  <div class="row-fluid">
    <div class='span4' id='dc-college-chart'>
      <h4>Did you go to college in Santa Cruz?
        <span>
          <br>
          <a class="reset" href="#dc-data-count" onclick="javascript:collegeChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4> 
    </div>
    <div class='span4' id='dc-residenceDuration-chart'>
      <h4>How long have you lived in Santa Cruz?
        <span>
          <br />(drag to filter results)
          <a class="reset" href="#dc-data-count" onclick="javascript:residenceDurationChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
    <div class='span4' id='dc-workedInSc-chart'>
      <h4>Have you ever worked in Santa Cruz?
        <span>
            <br />(click to filter results)
            <a class="reset" href="#dc-data-count" onclick="javascript:workedInScChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
  </div><!-- row-fluid -->
  <hr>
  <div class="row-fluid">
    <div class='span4' id='dc-whyNotWorkInSc-chart'>
      <h4>Why did you stop working in Santa Cruz?
        <span>
          <br />(click to filter results)
          <a class="reset" href="#dc-data-count" onclick="javascript:whyNotWorkInScChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
    <div class='span4' id='dc-salaryNeeded-chart'>
      <h4>Within what percentage of your current total compensation (salary, stock options, health and benefits, job position) would a Santa Cruz opportunity have to come for you to forgo your current job and commute?
        <span>
          <br />(click to filter results)
          <a class="reset" href="#dc-data-count" onclick="javascript:salaryNeededChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
    <div class='span4' id='dc-heardOfStartupNewsHere-chart'>
      <h4>How much have you heard about recent start-up activity in Santa Cruz?
        <span>
          <br />(click to filter results)
          <a class="reset" href="#dc-data-count" onclick="javascript:heardOfStartupNewsHereChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
  </div><!-- row-fluid -->
  <hr>
  <div class="row-fluid">
    <div class='span4' id='dc-consideredJobsInSantaCruz-chart'>
      <h4>Have you considered exploring job openings with any Santa Cruz tech companies or startups?
        <span>
          <br>
          <a class="reset" href="#dc-data-count" onclick="javascript:consideredJobsInSantaCruzChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
    <!--
    <div class='span4' id='dc-techEventsInSantaCruz-chart'>
      <h4>Which of the following Santa Cruz tech-community events have you attended?
        <span>
          <br>
          <a class="reset" href="#dc-data-count" onclick="javascript:techEventsInSantaCruzChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
    -->
    <div class='span8' id='dc-age-chart'>
      <h4>Age of Respondents
        <span>
            (drag sliders to filter results)
        </span>
      </h4>
    </div>
  </div><!-- row-fluid -->
  <hr>
  <div class="row-fluid">
    <div class='span4' id='dc-maritalStatus-chart'>
      <h4>Marital status
        <span>
          <br />(click to filter results)
          <a class="reset" href="#dc-data-count" onclick="javascript:maritalStatusChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
    <div class='span4' id='dc-children-chart'>
      <h4>Do you have children 17 years of age or younger living in the household?
        <span>
          <br />(click to filter results)
          <a class="reset" href="#dc-data-count" onclick="javascript:childrenChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
    <div class='span4' id='dc-rentOrOwn-chart'>
      <h4>Do you rent or own your home?
        <span>
          <br />(click to filter results)
          <a class="reset" href="#dc-data-count" onclick="javascript:rentOrOwnChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
  </div><!-- row-fluid -->
  <!-- removing table for now
  <hr>
   <div class='row-fluid'> 
    <div class='span12'>
      <div class='dc-data-count2'>
        <span> 
          Table listing
          <span class="filter-count"></span>
          records out of
          <span class="total-count"></span> 
          people surveyed | <a href="#dc-data-count" onclick="javascript:dc.filterAll(); dc.renderAll();">Reset</a> 
        </span>
      </div>
    </div> 
    <h4>Comments or Suggestions for improving the Santa Cruz tech-ecosystem?</h4>
    <table class='table table-hover' style="width: 100%;" id='dc-table-graph'> 
    </table>
  </div> -->
  <hr>
  <div class='row-fluid'> 
    <div class='span12' id='dc-commentsOrSuggestions-chart'>
      <h4>Comments and Suggestions</h4>
      <div id="commentsOrSuggestionsContainer">
      </div>
    </div>
  </div>

  <script src='/js/vendor/crossfilter111.min.js' type='text/javascript'></script>
  <script src='/js/vendor/dc130.min.js' type='text/javascript'></script>
  <link href='/styles/vendor/dc.css' rel='stylesheet' type='text/css'>
  
  <script>
      // Create the dc.js chart objects & link to div
      var salaryChart = dc.barChart("#dc-salary-chart");
      var commuteDurationChart = dc.lineChart("#dc-commuteDuration-chart");

      var ageChart = dc.barChart("#dc-age-chart");
      var senorityChart = dc.rowChart("#dc-senority-chart");
      
      var collegeChart = dc.rowChart("#dc-college-chart");
      var commuteTypeChart = dc.rowChart("#dc-commuteType-chart");
      var employmentDurationChart = dc.lineChart("#dc-employmentDuration-chart");

      var employmentTypeChart = dc.rowChart("#dc-employmentType-chart");
      

      var workedInScChart = dc.pieChart("#dc-workedInSc-chart");
      var whyLiveInScChart = dc.pieChart("#dc-whyLiveInSc-chart");
      var residenceDurationChart = dc.lineChart("#dc-residenceDuration-chart");
      
      var rentOrOwnChart = dc.pieChart("#dc-rentOrOwn-chart");
      var whyNotWorkInScChart = dc.pieChart("#dc-whyNotWorkInSc-chart");
      var salaryNeededChart = dc.pieChart("#dc-salaryNeeded-chart");

      var heardOfStartupNewsHereChart = dc.pieChart("#dc-heardOfStartupNewsHere-chart");
      var consideredJobsInSantaCruzChart = dc.pieChart("#dc-consideredJobsInSantaCruz-chart");
      var techEventsInSantaCruzChart = dc.pieChart("#dc-techEventsInSantaCruz-chart");

      var maritalStatusChart = dc.pieChart("#dc-maritalStatus-chart");
      var childrenChart = dc.pieChart("#dc-children-chart");
      var whyCommuteChart = dc.pieChart("#dc-whyCommute-chart");
      var commuteActivityChart = dc.pieChart("#dc-commuteActivity-chart");

      //var dataTable = dc.dataTable("#dc-table-graph");

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
              if (d.commentsOrSuggestions != "(blank)") {
                  $('#commentsOrSuggestionsContainer').append('<p>* ' + d.commentsOrSuggestions + '</p>');
              }
          });

          // Run the data through crossfilter and load our 'facts'
          var facts = crossfilter(data);

          // reset all button - this includes all facts
          var all = facts.groupAll();

          // reset all button - count all the facts
          dc.dataCount(".dc-data-count") 
              .dimension(facts) 
              .group(all);
          // note: code for table
          //dc.dataCount(".dc-data-count2") 
          //    .dimension(facts) 
          //    .group(all);


          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          var salaryValue = facts.dimension(function (d) { 
              return d.salary;
          });
          var salaryValueGroup = salaryValue.group();

          var commuteDurationValue = facts.dimension(function (d) { 
              return d.commuteDuration;
          });
          var commuteDurationValueGroup = commuteDurationValue.group();
              //.reduceCount(function(d) { return d.commuteDuration; }) // counts

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          var ageValue = facts.dimension(function (d) { 
              return d.age;
          });
          var ageValueGroup = ageValue.group()
              .reduceCount(function(d) { return d.age; }) // counts

          var senorityValue = facts.dimension(function (d) {
              //console.log("college: " + d.collegeWhere)
              switch (d.employmentLevel) {
                  case 'C-Level Executive': return "1.C-Level Executive";
                  case 'Consultant': return "2.Consultant";
                  case 'Director': return "3.Director";
                  case 'Independent Contractor': return "4.Independent Contractor";
                  case 'Intern': return "5.Intern";
                  case 'Team Manager': return "6.Team Manager";
                  case 'Team Member': return "7.Team Member";
                  case 'Vice President': return "8.Vice President";
                  default: return "0.No answer";
              } 
          });
          var senorityValueGroup = senorityValue.group();

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          var collegeValue = facts.dimension(function (d) {
              //console.log("college: " + d.collegeWhere)
              switch (d.collegeWhere) {
                  case 'UCSC': return "0.UCSC";
                  case 'Cabrillo': return "1.Cabrillo";
                  default: return "2.No answer";
              } 
          });
          var collegeValueGroup = collegeValue.group();

          var commuteType = facts.dimension(function (d) {
              switch (d.travelType) {
                  case 'Company bus': return "0.Company bus";
                  case 'Car (single occupancy)': return "1.Car (single occupancy)";
                  case 'Independent shuttle': return "2.Independent shuttle";
                  case 'Carpool': return "3.Carpool";
                  default: return "4.No answer";
              } 
          });
          var commuteTypeGroup = commuteType.group();

          var employmentDuration = facts.dimension(function (d) { 
              return d.employmentDuration;
          });
          var employmentDurationGroup = employmentDuration.group()
              .reduceCount(function(d) { return d.employmentDuration; }) // counts

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
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
                  case 'Engineering (other)': return "19.Enginering (other)";
                  case 'Other': return "19.Other";
                  default: return "0.No answer";
              } 
          });
          var employmentTypeGroup = employmentType.group();

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          var workedInSc = facts.dimension(function (d) {
              if (d.workedInSantaCruz == "(blank)") {
                  return "No answer";
              } else {
                  return d.workedInSantaCruz;
              }
          });
          var workedInScGroup = workedInSc.group();

          var whyLiveInSc = facts.dimension(function (d) {
              if (d.whyLiveHere == "(blank)") {
                  return "No answer";
              } else {
                  return d.whyLiveHere;
              }
          });
          var whyLiveInScGroup = whyLiveInSc.group();

          var residenceDuration = facts.dimension(function (d) { 
              if (d.residenceDuration == "(blank)") {
                  return 0;
              } else {
                  return d.residenceDuration;
              }
          });
          residenceDurationGroup = residenceDuration.group()
              .reduceCount(function(d) { return d.residenceDuration; }) // counts

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          var rentOrOwn = facts.dimension(function (d) {
              if (d.rentOrOwn == "(blank)") {
                  return "No answer";
              } else {
                  return d.rentOrOwn;
              }
          });
          var rentOrOwnGroup = rentOrOwn.group();

          var whyNotWorkInSc = facts.dimension(function (d) {
              if (d.whyNoWorkInSantaCruz == "(blank)") {
                  return "No answer";
              } else {
                  return d.whyNoWorkInSantaCruz;
              }
          });
          var whyNotWorkInScGroup = whyNotWorkInSc.group();

          var salaryNeeded = facts.dimension(function (d) {
              if (d.whatSalaryNeeded == "(blank)") {
                  return "No answer";
              } else {
                  return d.whatSalaryNeeded;
              }
          });
          var salaryNeededGroup = salaryNeeded.group();

          var heardOfStartupNewsHere = facts.dimension(function (d) {
              if (d.heardOfStartupNewsHere == "(blank)") {
                  return "No answer";
              } else {
                  return d.heardOfStartupNewsHere;
              }
          });
          var heardOfStartupNewsHereGroup = heardOfStartupNewsHere.group();

          var consideredJobsInSantaCruz = facts.dimension(function (d) {
              if (d.consideredJobsInSantaCruz == "(blank)") {
                  return "No answer";
              } else {
                  return d.consideredJobsInSantaCruz;
              }
          });
          var consideredJobsInSantaCruzGroup = consideredJobsInSantaCruz.group();

          var techEventsInSantaCruz = facts.dimension(function (d) {
              if (d.techEventsInSantaCruz == "(blank)") {
                  return "Have not attended an event";
              } else {
                  return d.techEventsInSantaCruz;
              }
          });
          var techEventsInSantaCruzGroup = techEventsInSantaCruz.group();

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          var children = facts.dimension(function (d) {
              if (d.children == "(blank)") {
                  return "No answer";
              } else {
                  return d.children;
              }
          });
          var childrenGroup = children.group();

          var maritalStatus = facts.dimension(function (d) {
              if (d.maritalStatus == "(blank)") {
                  return "No answer";
              } else {
                  return d.maritalStatus;
              }
          });
          var maritalStatusGroup = maritalStatus.group();

          var whyCommute = facts.dimension(function (d) {
              if (d.whyCommute == "(blank)") {
                  return "No answer";
              } else {
                  return d.whyCommute;
              }
          });
          var whyCommuteGroup = whyCommute.group();

          var commuteActivity = facts.dimension(function (d) {
              if (d.commuteActivity == "(blank)") {
                  return "Not a bus commuter";
              } else {
                  return d.commuteActivity;
              }
          });
          var commuteActivityGroup = commuteActivity.group();

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

          // Create dataTable dimension
          var commuteDurationDimension = facts.dimension(function (d) { 
            return d.commuteDuration;
          });

          // Setup the charts
          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          var commasFormatter = d3.format(",.0f");
          salaryChart.width(280) 
              .height(150) 
              .margins({top: 10, right: 10, bottom: 20, left: 20}) 
              .dimension(salaryValue) 
              .group(salaryValueGroup) 
              .transitionDuration(500) 
              .centerBar(true) 
              .gap(-8)
              .x(d3.scale.linear().domain([0, 510000])) 
              .filter([0, 505000])
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
          commuteDurationChart.width(370) 
              .height(150) 
              .margins({top: 10, right: 10, bottom: 20, left: 20}) 
              .dimension(commuteDurationValue) 
              .group(commuteDurationValueGroup) 
              .transitionDuration(500)
              .title(function(d){
                  return d.key
                  + " hrs \nNumber of Commuters: " + d.value; 
                  })
              .x(d3.scale.linear().domain([0.5,6.5]))
              .elasticY(true) 
              .filter([0.6, 5.1])
              .xAxis()
              .tickFormat(function(d) { return hoursFormatter(d); })
              .ticks(6);

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          var yearsFormatter = function(d) {
              return d + " years";
          }
          // age graph
          ageChart.width(400) 
              .height(220) 
              .margins({top: 10, right: 10, bottom: 20, left: 40}) 
              .dimension(ageValue) 
              .group(ageValueGroup) 
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

          senorityChart.width(400) 
              .height(250) 
              .dimension(senorityValue) 
              .group(senorityValueGroup)
              .colors(d3.scale.category20b())
              .label(function (d){
                  return d.key.split(".")[1];
                  }) 
              .title(function(d){return d.value + " commuters";})
              .xAxis()
              .tickFormat(function(d) { return commutersFormatter(d); })
              .ticks(4);

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          collegeChart.width(200) 
              .height(220) 
              .margins({top: 15, left: 15, right: 15, bottom: 15}) 
              .dimension(collegeValue) 
              .group(collegeValueGroup) 
              .colors(d3.scale.category20c())
              .label(function (d){
                  return d.key.split(".")[1];
                  })
              .title(function(d){return d.value + " commuters";}) 
              .xAxis()
              .tickFormat(function(d) { return d; })
              .ticks(3);

          commuteTypeChart.width(200) 
              .height(250) 
              .margins({top: 15, left: 15, right: 15, bottom: 15}) 
              .dimension(commuteType) 
              .group(commuteTypeGroup)
              .colors(d3.scale.category20b())
              .label(function (d){
                  return d.key.split(".")[1];
                  }) 
              .title(function(d){return d.value + " commuters";})
              .xAxis()
              .tickFormat(function(d) { return d; })
              .ticks(3);

          employmentDurationChart.width(290) 
              .height(248) 
              .margins({top: 40, right: 10, bottom: 20, left: 20}) 
              .dimension(employmentDuration) 
              .group(employmentDurationGroup) 
              .transitionDuration(500)
              .elasticY(true)
              .x(d3.scale.linear().domain([0,12.5]))
              .filter([0, 12.1])
              .xAxis()
              .ticks(4)
              .tickFormat(function(d) { return yearsFormatter(d); });

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          employmentTypeChart.width(220) 
              .height(300) 
              .margins({top: 5, left: 5, right: 10, bottom: 40}) 
              .dimension(employmentType) 
              .group(employmentTypeGroup) 
              .colors(d3.scale.category20c())
              .label(function (d){
                  return d.key.split(".")[1];
                  }) 
              .title(function(d){return d.value + " commuters.";})
              .xAxis()
              .ticks(4);

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          // pie chart section begins here
          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          workedInScChart.width(300) 
              .height(220) 
              .radius(100) 
              .innerRadius(30) 
              .dimension(workedInSc) 
              .group(workedInScGroup) 
              .title(function(d){return d.data.key + ", " + d.value;});


          whyLiveInScChart.width(300) 
              .height(220) 
              .radius(100) 
              .innerRadius(30) 
              .dimension(whyLiveInSc) 
              .group(whyLiveInScGroup) 
              .title(function(d){return d.data.key + ", " + d.value;});

          residenceDurationChart.width(280) 
              .height(220) 
              .margins({top: 10, right: 10, bottom: 20, left: 20}) 
              .dimension(residenceDuration) 
              .group(residenceDurationGroup) 
              .transitionDuration(500)
              .elasticY(true) 
              .x(d3.scale.linear().domain([0,12.3]))
              .filter([0, 12.2]) 
              .xAxis()
              .ticks(4)
              .tickFormat(function(d) { return yearsFormatter(d); });

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          rentOrOwnChart.width(300) 
              .height(220) 
              .radius(100) 
              .innerRadius(30) 
              .dimension(rentOrOwn) 
              .group(rentOrOwnGroup) 
              .title(function(d){return d.data.key + ", " + d.value;});

          whyNotWorkInScChart.width(300) 
              .height(220) 
              .radius(100) 
              .innerRadius(30) 
              .dimension(whyNotWorkInSc) 
              .group(whyNotWorkInScGroup) 
              .title(function(d){return d.data.key + ", " + d.value;});

          salaryNeededChart.width(300) 
              .height(220) 
              .radius(100) 
              .innerRadius(30) 
              .dimension(salaryNeeded) 
              .group(salaryNeededGroup) 
              .title(function(d){return d.data.key + ", " + d.value;});

          heardOfStartupNewsHereChart.width(300) 
              .height(220) 
              .radius(100) 
              .innerRadius(30) 
              .dimension(heardOfStartupNewsHere) 
              .group(heardOfStartupNewsHereGroup) 
              .title(function(d){return d.data.key + ", " + d.value;});

          techEventsInSantaCruzChart.width(300) 
              .height(220) 
              .radius(100) 
              .innerRadius(30) 
              .dimension(techEventsInSantaCruz) 
              .group(techEventsInSantaCruzGroup) 
              .title(function(d){return d.data.key + ", " + d.value;});

          consideredJobsInSantaCruzChart.width(300) 
              .height(220) 
              .radius(100) 
              .innerRadius(30) 
              .dimension(consideredJobsInSantaCruz) 
              .group(consideredJobsInSantaCruzGroup) 
              .title(function(d){return d.data.key + ", " + d.value;});

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          maritalStatusChart.width(300) 
              .height(220) 
              .radius(100) 
              .innerRadius(30) 
              .dimension(maritalStatus) 
              .group(maritalStatusGroup) 
              .title(function(d){return d.data.key + ", " + d.value;});  

          childrenChart.width(300) 
              .height(220) 
              .radius(100) 
              .innerRadius(30) 
              .dimension(children) 
              .group(childrenGroup) 
              .title(function(d){return d.data.key + ", " + d.value;});

          whyCommuteChart.width(300) 
              .height(220) 
              .radius(100) 
              .innerRadius(30) 
              .dimension(whyCommute) 
              .group(whyCommuteGroup) 
              .title(function(d){return d.data.key + ", " + d.value;});

          commuteActivityChart.width(300) 
              .height(220) 
              .radius(100) 
              .innerRadius(30) 
              .dimension(commuteActivity) 
              .group(commuteActivityGroup) 
              .title(function(d){return d.data.key + ", " + d.value;});

          // Table of commuter survey data
          //dataTable.width(760).height(800) 
          //    .dimension(commuteDurationDimension)
          //        .group(function(d) { return ''})
          //    .columns([
          //        function(d) { return commentsOrSuggestionsFormatter(d.commentsOrSuggestions); },
          //    ])
          //    .sortBy(function(d){ 
          //        return d.commuteDuration; 
          //    })
          //    .order(d3.ascending);

          // Render the Charts
          dc.renderAll();

      });

  </script>

</%def>