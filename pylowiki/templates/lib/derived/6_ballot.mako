<%!
    import pylowiki.lib.db.user         as userLib
    import pylowiki.lib.db.generic      as genericLib
    import pylowiki.lib.utils           as utils
    import misaka as m

    import locale
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')
    
    import logging
    log = logging.getLogger(__name__)

    from pylowiki.lib.db.geoInfo import getGeoTitles, getStateList, getCountyList, getCityList, getPostalList
%>

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="showElectionInfo(election, author)">
    <% scopeInfo = utils.getPublicScope(c.election['scope']) %>
    <div class="row-fluid">
        <h3>${election['title']}</h3>
        <img src="${scopeInfo['flag']}" width="60" height="60"> ${scopeInfo['level']} of ${scopeInfo['name']}
    </div><!-- row-fluid -->
    <div class="spacer"></div>
    <div class="row-fluid"><div class="span2 text-right">Election Date:</div><div class="span9 text-left">${election['electionDate']}</div></div>
    
    <div class="row-fluid">
        <div class="span9">
            ${m.html(election['text'], render_flags=m.HTML_SKIP_HTML) | n}
        </div>
    </div><!-- row-fluid -->
    
    <div class="row-fluid">
        <span class="grey">Posted by: </span>
        ${lib_6.userImage(author, className="avatar small-avatar")} ${lib_6.userLink(author)}
    </div><!-- row-fluid -->
    % if c.election.objType == 'revision':
        <div class="alert alert-error">
            This is a revision dated ${c.election.date}
        </div>
    % endif
</%def>

<%def name="showBallotInfo(ballot, author)">
    <div class="row-fluid">
        <h3>${ballot['title']}</h3>
    </div><!-- row-fluid -->
    <div class="spacer"></div>

    <div class="row-fluid">
        <div class="span9">
            ${m.html(ballot['text'], render_flags=m.HTML_SKIP_HTML) | n}
        </div>
    </div><!-- row-fluid -->
    
    <div class="row-fluid">
        <div class="span9">
            ${m.html(ballot['instructions'], render_flags=m.HTML_SKIP_HTML) | n}
        </div>
    </div><!-- row-fluid -->
    
    <div class="row-fluid">
        <span class="grey">Posted by: </span>
        ${lib_6.userImage(author, className="avatar small-avatar")} ${lib_6.userLink(author)}
    </div><!-- row-fluid -->
    % if c.ballot.objType == 'revision':
        <div class="alert alert-error">
            This is a revision dated ${c.ballot.date}
        </div>
    % endif
</%def>

<%def name="editElection()">
    <% 
        postalCodeSelected = ""
        citySelected = ""
        countySelected = ""
        if c.election:
            eScope = c.election['scope']
            title = c.election['title']
            text = c.election['text']
            electionDate = c.election['electionDate']
            electionOfficialURL = c.election['electionOfficialURL']
            if public == 'on':
                publicChecked = 'checked'
            else:
                publicChecked = ""
        else:
            eScope = "0|0|0|0|0|0|0|0|0|0"
            title = ""
            group = ""
            tag = ""
            text = ""
            electionDate = ""
            electionOfficialURL = ""
            public = ""
            publicChecked = ""
            
        scopeList = eScope.split('|')
        if scopeList[9] == '0' and scopeList[8] == '0':
            countySelected = "selected"
        elif scopeList[9] == '0' and scopeList[8] != '0':
            citySelected = "selected"
        else:
            postalCodeSelected = "selected"

    %>
    % if c.saveMessage and c.saveMessage != '':
        <div class="alert ${c.saveMessageClass}">
        <button type="button" class="close" data-dismiss="alert">&times;</button>
        ${c.saveMessage}
        </div>
    % endif
    <div class="row-fluid>
        <div class="span12">
            % if c.edit:
                <form method="POST" name="edit_election" id="edit_ballot" action="/election/${c.election['urlCode']}/${c.election['url']}/electionEditHandler">
            % else:
                <form method="POST" name="edit_election" id="edit_ballot" action="/election/${c.authuser['urlCode']}/${c.authuser['url']}/electionNewHandler">
            % endif
            <div class="row-fluid">
                <h3>Election Information</h3>
            </div><!-- row-fluid -->
            <br>
            
            <div class="row-fluid">
                <div class="span6">
                    <label for="title" class="control-label" required><strong>Election Title:</strong></label>
                    <input type="text" name="electionTitle" class="span12" value="${title}" required>
                </div><!-- span6 -->
                <div class="span6">
                    <div class="alert alert-info">
                        Keep it short and descriptive.
                    </div><!-- alert -->
                </div><!-- span6 -->
            </div><!-- row-fluid -->
            
            <div class="row-fluid">
                <div class="span6">
                    <label for="title" class="control-label" required><strong>Election Date:</strong></label>
                    <input type="text" name="electionDate" id="electionDate" class="span6" value="${electionDate}" required>
                </div><!-- span6 -->
                <div class="span6">
                    <div class="alert alert-info">
                        Date of the election.
                    </div><!-- alert -->
                </div><!-- span6 -->
            </div><!-- row-fluid -->
            
            
            <div class="row-fluid">
                <div class="span6">
                    <label for="title" class="control-label" required><strong>Official Election URL:</strong></label>
                    <input type="text" name="electionOfficialURL" id="electionOfficialURL" class="span6" value="${electionOfficialURL}">
                </div><!-- span6 -->
                <div class="span6">
                    <div class="alert alert-info">
                        The URL to the official election web site.
                    </div><!-- alert -->
                </div><!-- span6 -->
            </div><!-- row-fluid -->
            
            <div class="row-fluid spacer">
                <div class="span6">
                    <label for="scope" class="control-label" required><strong>Public Jurisdiction:</strong></label>
                    ${geoSelect()}
                </div><!-- span6 -->
                <div class="span6">
                    <div class="alert alert-info">
                        The region or legal jurisdiction associated with the election.
                    </div><!-- alert -->
                </div><!-- span6 -->
            </div><!-- row-fluid -->

            <div class="row-fluid spacer">
                <div class="span6">
                    <label for="text" class="control-label" required><strong>Election Description:</strong></label>
                    ${lib_6.formattingGuide()}
                </div>
                <div class="span6">
                    <div class="alert alert-info">
                        A short description about the ballot or election.
                    </div>
                </div><!-- span6 -->
            </div><!-- row-fluid -->
            <textarea rows="10" id="electionText" name="electionText" class="span12" required>${text}</textarea>
            
            <div class="row-fluid spacer">
                <div class="span6">            
                    <input type="checkbox" name="public" ${publicChecked}> Publish this election
                </div><!-- span6 -->
                <div class="span6">
                    <div class="alert alert-info">
                        Makes the election viewable by members and the public, with members able to comment and vote.
                    </div><!-- alert -->
                </div><!-- span6 -->
            </div><!-- row-fluid -->

            <button type="submit" class="btn btn-warning btn-large pull-right" name="submit_summary">Save Changes</button>
        </form>
        </div><!-- span12 -->
    </div><!-- row-fluid -->
</%def>


<%def name="editBallot()">
    <% 
        postalCodeSelected = ""
        citySelected = ""
        countySelected = ""
        if c.ballot:
            bScope = c.ballot['scope']
            title = c.ballot['title']
            text = c.ballot['text']
            electionDate = c.ballot['electionDate']
            electionOfficialURL = c.ballot['electionOfficialURL']
            ballotSlate = c.ballot['ballotSlate']
            if 'candidateMax' in c.ballot:
                candidateMax = c.ballot['candidateMax']
            else:
                candidateMax = '1'
            public = c.ballot['public']
            if public == 'on':
                publicChecked = 'checked'
            else:
                publicChecked = ""
        else:
            bScope = "0|0|0|0|0|0|0|0|0|0"
            title = ""
            group = ""
            tag = ""
            text = ""
            electionDate = ""
            electionOfficialURL = ""
            ballotSlate = ""
            candidateMax = "1"
            public = ""
            publicChecked = ""
            
        scopeList = bScope.split('|')
        if scopeList[9] == '0' and scopeList[8] == '0':
            countySelected = "selected"
        elif scopeList[9] == '0' and scopeList[8] != '0':
            citySelected = "selected"
        else:
            postalCodeSelected = "selected"

    %>
    % if c.saveMessage and c.saveMessage != '':
        <div class="alert ${c.saveMessageClass}">
        <button type="button" class="close" data-dismiss="alert">&times;</button>
        ${c.saveMessage}
        </div>
    % endif
    <script>
        function Ctrl($scope) {
            $scope.candidate = 0;
            $scope.setCandidateYes = function() {
                $scope.candidate = 1;
            };
            $scope.setCandidateNo = function() {
                $scope.candidate = 0;
            };
        }
    </script>
    <div class="row-fluid>
        <div class="span12">
            % if c.editBallot:
                <form method="POST" name="edit_ballot" id="edit_ballot" action="/ballot/${c.ballot['urlCode']}/${c.ballot['url']}/ballotEditHandler" ng-controller="Ctrl">
            % else:
                <form method="POST" name="edit_ballot" id="edit_ballot" action="/ballot/${c.authuser['urlCode']}/${c.authuser['url']}/ballotNewHandler" ng-controller="Ctrl">
            % endif
            <div class="row-fluid">
                <h3>Ballot Information</h3>
            </div><!-- row-fluid -->
            <br>
            
            <div class="row-fluid">
                <div class="span6">
                    <label for="title" class="control-label" required><strong>Ballot Title:</strong></label>
                    <input type="text" name="ballotTitle" class="span12" value="${title}" required>
                </div><!-- span6 -->
                <div class="span6">
                    <div class="alert alert-info">
                        Keep it short and descriptive.
                    </div><!-- alert -->
                </div><!-- span6 -->
            </div><!-- row-fluid -->
            
            <div class="row-fluid">
                <div class="span6">
                    <label for="title" class="control-label" required><strong>Election Date:</strong></label>
                    <input type="text" name="electionDate" id="electionDate" class="span6" value="${electionDate}" required>
                </div><!-- span6 -->
                <div class="span6">
                    <div class="alert alert-info">
                        Date of the election.
                    </div><!-- alert -->
                </div><!-- span6 -->
            </div><!-- row-fluid -->
            
            
            <div class="row-fluid">
                <div class="span6">
                    <label for="title" class="control-label" required><strong>Official Election URL:</strong></label>
                    <input type="text" name="electionOfficialURL" id="electionOfficialURL" class="span6" value="${electionOfficialURL}">
                </div><!-- span6 -->
                <div class="span6">
                    <div class="alert alert-info">
                        The URL to the official election web site.
                    </div><!-- alert -->
                </div><!-- span6 -->
            </div><!-- row-fluid -->
            
            <div class="row-fluid">
                <%
                    if c.ballot and c.ballot['ballotSlate'] == 'measures':
                        measuresChecked = 'checked'
                        candidatesChecked = ''
                    else:
                        measuresChecked = ''
                        candidatesChecked = 'checked'
                %>
                <div class="span6">
                    <label for="ballotSlate" class="control-label" required><strong>Ballot Slate Type:</strong></label>
                    <label class="radio">
                        <input type="radio" name="ballotSlate" id="ballotSlate1" value="measures" ng-click="setCandidateNo();" ${measuresChecked} required>
                        Ballot measures
                    </label>
                    <label class="radio">
                        <input type="radio" name="ballotSlate" id="ballotSlate2" ng-model="ballotSlate2" ng-click="setCandidateYes();" ${candidatesChecked} value="candidates" required>
                        Candidates for office
                    </label>
                    <div ng-show="candidate">
                        <label for="candidateMax" class="control-label" required><strong>Can vote for max of how many candidates on slate:</strong></label>
                        <select name="candidateMax">
                            <% 
                                voteMax = 20
                                loop = 1
                            %>
                            % while loop < voteMax + 1:
                                <%
                                    if int(candidateMax) == loop:
                                        selected = "selected"
                                    else:
                                        selected = ""
                                %>
                                <option ${selected}>${loop}</option>
                                <% loop += 1 %>
                            % endwhile
                        </select>
                    </div>
                </div><!-- span6 -->
                <div class="span6">
                    <div class="alert alert-info">
                        The type of ballot slate. Ballot measures with yes/no vote per measure, or candidates with a maximum of N votes for the slate.
                    </div><!-- alert -->
                </div><!-- span6 -->
            </div><!-- row-fluid -->

            <div class="row-fluid spacer">
                <div class="span6">
                    <label for="scope" class="control-label" required><strong>Public Jurisdiction:</strong></label>
                    ${geoSelect()}
                </div><!-- span6 -->
                <div class="span6">
                    <div class="alert alert-info">
                        The region or legal jurisdiction associated with the election.
                    </div><!-- alert -->
                </div><!-- span6 -->
            </div><!-- row-fluid -->

            <div class="row-fluid spacer">
                <div class="span6">
                    <label for="text" class="control-label" required><strong>Ballot/Election Description:</strong></label>
                    ${lib_6.formattingGuide()}
                </div>
                <div class="span6">
                    <div class="alert alert-info">
                        A short description about the ballot or election.
                    </div>
                </div><!-- span6 -->
            </div><!-- row-fluid -->
            <textarea rows="10" id="ballotText" name="ballotText" class="span12" required>${text}</textarea>
            
            <div class="row-fluid spacer">
                <div class="span6">            
                    <input type="checkbox" name="public" ${publicChecked}> Publish this ballot
                </div><!-- span6 -->
                <div class="span6">
                    <div class="alert alert-info">
                        Makes the ballot viewable by members and the public, with members able to comment and vote.
                    </div><!-- alert -->
                </div><!-- span6 -->
            </div><!-- row-fluid -->

            <button type="submit" class="btn btn-warning btn-large pull-right" name="submit_summary">Save Changes</button>
        </form>
        </div><!-- span12 -->
    </div><!-- row-fluid -->
</%def>

<%def name="geoSelect()">
    <% 
        countrySelected = ""
        countyMessage = ""
        cityMessage = ""
        postalMessage = ""
        underPostalMessage = ""
        if c.country!= "0":
            countrySelected = "selected"
            states = c.states
            countyMessage = "Leave 'State' blank if the election jurisdiction applies to the entire country."
        endif
    %>
    <div class="row-fluid"><span id="planetSelect">
        <div class="span3">Planet:</div>
        <div class="span8">
            <select name="geoTagPlanet" id="geoTagPlanet" class="geoTagCountry">
                <option value="0">Earth</option>
            </select>
        </div><!-- span8 -->
    </span><!-- countrySelect -->
    </div><!-- row-fluid -->     
    <div class="row-fluid"><span id="countrySelect">
        <div class="span3">Country:</div>
        <div class="span8">
            <select name="geoTagCountry" id="geoTagCountry" class="geoTagCountry">
                <option value="0">Select a country</option>
                <option value="United States" ${countrySelected}>United States</option>
            </select>
        </div><!-- span8 -->
    </span><!-- countrySelect -->
    </div><!-- row-fluid -->
    <div class="row-fluid"><span id="stateSelect">
        % if c.country != "0":
            <div class="span3">State:</div><div class="span8">
            <select name="geoTagState" id="geoTagState" class="geoTagState" onChange="geoTagStateChange(); return 1;">
            <option value="0">Select a state</option>
            % for state in states:
                % if state != 'District of Columbia':
                    % if c.state == state['StateFullName']:
                        <% stateSelected = "selected" %>
                    % else:
                        <% stateSelected = "" %>
                    % endif
                    <option value="${state['StateFullName']}" ${stateSelected}>${state['StateFullName']}</option>
                % endif
            % endfor
            </select>
            </div><!-- span8 -->
        % else:
            Leave 'Country' blank if the election jurisdiction applies to the entire planet.
        % endif
    </span></div><!-- row-fluid -->
    <div class="row-fluid"><span id="countySelect">
        % if c.state != "0":
            <% counties = getCountyList("united-states", c.state) %>
            <% cityMessage = "Leave blank 'County' blank if the election jurisdiction applies to the entire state." %>
            <div class="span3">County:</div><div class="span8">
            <select name="geoTagCounty" id="geoTagCounty" class="geoTagCounty" onChange="geoTagCountyChange(); return 1;">
                <option value="0">Select a county</option>
                % for county in counties:
                    % if c.county == county['County'].title():
                        <% countySelected = "selected" %>
                    % else:
                        <% countySelected = "" %>
                    % endif
                    <option value="${county['County'].title()}" ${countySelected}>${county['County'].title()}</option>
                % endfor
            </select>
            </div><!-- span8 -->
        % else:
            <% cityMessage = "" %>
            ${countyMessage}
        % endif
    </span></div><!-- row -->
    <div class="row-fluid"><span id="citySelect">
        % if c.county != "0":
            <% cities = getCityList("united-states", c.state, c.county) %>
            <% postalMessage = "Leave 'City' blank if the election jurisdiction applies to the entire county." %>
            <div class="span3">City:</div><div class="span8">
            <select name="geoTagCity" id="geoTagCity" class="geoTagCity" onChange="geoTagCityChange(); return 1;">
            <option value="0">Select a city</option>
                % for city in cities:
                    % if c.city == city['City'].title():
                        <% citySelected = "selected" %>
                    % else:
                        <% citySelected = "" %>
                    % endif
                    <option value="${city['City'].title()}" ${citySelected}>${city['City'].title()}</option>
                % endfor
            </select>
            </div><!-- span8 -->
        % else:
            <% postalMessage = "" %>
            ${cityMessage}
        % endif
        </span></div><!-- row-fluid -->
    <div class="row-fluid"><span id="postalSelect">
        % if c.city != "0":
            <% postalCodes = getPostalList("united-states", c.state, c.county, c.city) %>
            <% underPostalMessage = "or leave blank if your the election jurisdiction is specific to the entire city." %>
            <div class="span3">Zip Code:</div><div class="span8">
            <select name="geoTagPostal" id="geoTagPostal" class="geoTagPostal" onChange="geoTagPostalChange(); return 1;">
            <option value="0">Select a zip code</option>
                % for pCode in postalCodes:
                    % if c.postal == str(pCode['ZipCode']):
                        <% postalSelected = "selected" %>
                    % else:
                        <% postalSelected = "" %>
                    % endif
                    <option value="${pCode['ZipCode']}" ${postalSelected}>${pCode['ZipCode']}</option>
                % endfor
            </select>
            </div><!-- span8 -->
        % else:
            <% underPostalMessage = "" %>
            ${postalMessage}
        % endif
        </span></div><!-- row-fluid -->
    <div class="row-fluid"><span id="underPostal">${underPostalMessage}</span><br /></div><!-- row -->
    <br/>
</%def>

<%def name="addBallot(election, author)">
    % if 'user' in session and (c.authuser['email'] == author['email'] or userLib.isAdmin(c.authuser.id)):
        <script>
            function Ctrl($scope) {
                $scope.candidate = 0;
                $scope.setCandidateYes = function() {
                    $scope.candidate = 1;
                };
                $scope.setCandidateNo = function() {
                    $scope.candidate = 0;
                };
            }
        </script>
        <div class="row-fluid">
            <button type="button" class="btn btn-success" data-toggle="collapse" data-target="#addItem"><i class="icon icon-white icon-plus"></i> Ballot</button>
            <div id="addItem" class="collapse">
                <form action="/election/${election['urlCode']}/${election['url']}/ballotNewHandler" method="POST" ng-controller="Ctrl">
                    <fieldset>
                        <label>Title</label>
                        <input type="text" name="ballotTitle" class="span6" required>
                        <label>Listing Order Number in Election</label>
                        <input type="text" name="ballotNumber" class="span1" required>
                        <label for="ballotSlate" class="control-label" required><strong>Ballot Slate Type:</strong></label>
                        <label class="radio">
                            <input type="radio" name="ballotSlate" id="ballotSlate1" value="measures" ng-click="setCandidateNo();"  required>
                            Ballot measures
                        </label>
                        <label class="radio">
                            <input type="radio" name="ballotSlate" id="ballotSlate2" ng-model="ballotSlate2" ng-click="setCandidateYes();"  value="candidates" required>
                            Candidates for office
                        </label>
                        <div ng-show="candidate">
                            <label for="candidateMax" class="control-label" required><strong>Can vote for max of how many candidates on slate:</strong></label>
                            <select name="candidateMax">
                                <% 
                                    voteMax = 20
                                    loop = 1
                                %>
                                % while loop < voteMax + 1:
                                    <option>${loop}</option>
                                    <% loop += 1 %>
                                % endwhile
                            </select>
                        </div><!-- ng-show -->
                        ${lib_6.formattingGuide()}<br>
                        <label>Text</label>
                        <textarea rows="3" name="ballotText" class="span6" required></textarea>
                        <label>Instructions</label>
                        <textarea rows="3" name="ballotInstructions" class="span6" required></textarea>
                        <p><button class="btn btn-success" type="submit" class="btn">Save Item</button>
                        <button class="btn btn-danger" type="reset" value="Reset">Cancel</button></p>
                    </fieldset>
                </form>
            </div>
        </div><!-- row-fluid -->
    % endif
</%def>

<%def name="addBallotMeasure(ballot, author)">
    % if 'user' in session and (c.authuser['email'] == author['email'] or userLib.isAdmin(c.authuser.id)):
        <div class="row-fluid">
            <button type="button" class="btn btn-success" data-toggle="collapse" data-target="#addItem"><i class="icon icon-white icon-plus"></i> Ballot Measure</button>
            <div id="addItem" class="collapse">
                <form action="/ballot/${ballot['urlCode']}/${ballot['url']}/ballotMeasureAddHandler" method="POST">
                    <fieldset>
                        <label>Title</label>
                        <input type="text" name="ballotTitle" class="span6" required>
                        <label>Listing Order Number in Election</label>
                        <input type="text" name="ballotNumber" class="span1" required>
                        <label>Text</label>
                        ${lib_6.formattingGuide()}<br>
                        <textarea rows="3" name="ballotMeasureText" class="span6" required></textarea>
                        
                        <p><button class="btn btn-success" type="submit" class="btn">Save Item</button>
                        <button class="btn btn-danger" type="reset" value="Reset">Cancel</button></p>
                    </fieldset>
                </form>
            </div>
        </div><!-- row-fluid -->
    % endif
</%def>

<%def name="electionModeration(thing)">
    <%
        if 'user' not in session or thing.objType == 'revision' or c.privs['provisional']:
            return
        adminID = 'admin-%s' % thing['urlCode']
        publishID = 'publish-%s' % thing['urlCode']
        unpublishID = 'unpublish-%s' % thing['urlCode']
    %>
    <div class="btn-group">
        % if (c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id)) and thing.objType != 'electionUnpublished':
            <a href="/election/${thing['urlCode']}/${thing['url']}/electionEdit" class="btn btn-mini">Edit</a>
            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${unpublishID}">trash</a>
        % elif thing.objType == 'electionUnpublished' and thing['unpublished_by'] != 'parent':
            % if thing['unpublished_by'] == 'admin' and userLib.isAdmin(c.authuser.id):
                <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${publishID}">publish</a>
            % elif thing['unpublished_by'] == 'owner' and c.authuser.id == thing.owner:
                <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${publishID}">publish</a>
            % endif
        % endif
        % if c.revisions:
            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#revisions">revisions (${len(c.revisions)})</a>
        % endif

        % if userLib.isAdmin(c.authuser.id):
            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${adminID}">admin</a>
        % endif
    </div>
    
    % if thing['disabled'] == '0':
        % if (c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id)):
            % if thing.objType == 'electionUnpublished':
                ${lib_6.publishThing(thing)}
            % else:
                ${lib_6.unpublishThing(thing)}
            % endif
            % if userLib.isAdmin(c.authuser.id):
                ${lib_6.adminThing(thing)}
            % endif
        % endif
    % else:
        % if userLib.isAdmin(c.authuser.id):
            ${lib_6.adminThing(thing)}
        % endif
    % endif
    % if c.revisions:
        <div id="revisions" class="collapse">
            <ul class="unstyled">
            % for revision in c.revisions:
                <li>Revision: <a href="/election/${revision['urlCode']}/${revision['url']}/show">${revision.date}</a></li>
            % endfor
            </ul>
        </div>
    % endif
</%def>


<%def name="ballotModeration(thing)">
    <%
        if 'user' not in session or thing.objType == 'revision' or c.privs['provisional']:
            return
        adminID = 'admin-%s' % thing['urlCode']
        publishID = 'publish-%s' % thing['urlCode']
        unpublishID = 'unpublish-%s' % thing['urlCode']
    %>
    <div class="btn-group">
        % if (c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id)) and thing.objType != 'ballotUnpublished':
            <a href="/ballot/${thing['urlCode']}/${thing['url']}/ballotEdit" class="btn btn-mini">Edit</a>
            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${unpublishID}">trash</a>
        % elif thing.objType == 'ballotUnpublished' and thing['unpublished_by'] != 'parent':
            % if thing['unpublished_by'] == 'admin' and userLib.isAdmin(c.authuser.id):
                <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${publishID}">publish</a>
            % elif thing['unpublished_by'] == 'owner' and c.authuser.id == thing.owner:
                <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${publishID}">publish</a>
            % endif
        % endif
        % if c.revisions:
            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#revisions">revisions (${len(c.revisions)})</a>
        % endif

        % if userLib.isAdmin(c.authuser.id):
            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${adminID}">admin</a>
        % endif
    </div>
    
    % if thing['disabled'] == '0':
        % if (c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id)):
            % if thing.objType == 'ballotUnpublished':
                ${lib_6.publishThing(thing)}
            % else:
                ${lib_6.unpublishThing(thing)}
            % endif
            % if userLib.isAdmin(c.authuser.id):
                ${lib_6.adminThing(thing)}
            % endif
        % endif
    % else:
        % if userLib.isAdmin(c.authuser.id):
            ${lib_6.adminThing(thing)}
        % endif
    % endif
    % if c.revisions:
        <div id="revisions" class="collapse">
            <ul class="unstyled">
            % for revision in c.revisions:
                <li>Revision: <a href="/ballot/${revision['urlCode']}/${revision['url']}/show">${revision.date}</a></li>
            % endfor
            </ul>
        </div>
    % endif
</%def>
