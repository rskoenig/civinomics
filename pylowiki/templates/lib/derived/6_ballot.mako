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
    <div class="row">
        <h3>${election['title']}</h3>
    </div>
    <div class="row spacer">
        <div class="col-xs-2">
            <img src="${scopeInfo['flag']}" width="80" height="60"> 
        </div>
        <div class="col-xs-9 text-left">
            <p>${scopeInfo['level']} of ${scopeInfo['name']}</p>
            <p>Election Date: ${election['electionDate']}</p>
        </div>
    </div><!-- row -->

    <div class="row spacer">
        <div class="col-xs-11 text-left">
            ${m.html(election['text'], render_flags=m.HTML_SKIP_HTML) | n}
        </div>
    </div><!-- row -->
    
    <div class="row spacer">
        <span class="grey">Posted by: </span>
        ${lib_6.userImage(author, className="avatar small-avatar")} ${lib_6.userLink(author)}
    </div><!-- row -->
    % if c.election.objType == 'revision':
        <div class="alert alert-error">
            This is a revision dated ${c.election.date}
        </div>
    % endif
</%def>

<%def name="showBallotInfo(ballot, author)">
    <div class="row spacer">
        <div class="col-xs-9 text-left">
            <h3>${ballot['title']}</h3>
        </div>
        <div class="col-xs-3 text-right">
            <a href="/election/${ballot['electionCode']}/${ballot['election_url']}/show">Back to Election</a>
        </div>
    </div><!-- row -->

    <div class="row spacer">
        <div class="col-xs-9 text-left">
            ${m.html(ballot['text'], render_flags=m.HTML_SKIP_HTML) | n}
        </div>
    </div><!-- row -->
    
    <div class="row">
        <div class="col-xs-9 text-left">
            <p><strong>Instructions</strong></p>
            ${m.html(ballot['instructions'], render_flags=m.HTML_SKIP_HTML) | n}
        </div>
    </div><!-- row -->
    
    <div class="row">
        <span class="grey">Posted by: </span>
        ${lib_6.userImage(author, className="avatar small-avatar")} ${lib_6.userLink(author)} &nbsp;&nbsp; <i class="glyphicon glyphicon-eye-open"></i> Views (${ballot['views']})
    </div><!-- row -->
    % if c.ballot.objType == 'revision':
        <div class="alert alert-error">
            This is a revision dated ${c.ballot.date}
        </div>
    % endif
</%def>

<%def name="showBallotmeasureInfo(ballotmeasure, author)">
    <div class="row spacer">
        <div class="col-xs-9 text-left">
            <h3>${ballotmeasure['title']}</h3>
        </div>
    </div><!-- row -->
    
    % if ballotmeasure['ballotMeasureOfficialURL'] != '':
        <div class="row spacer">
            <div class="col-xs-9 text-left">
                Official Web Site: <a href="${ballotmeasure['ballotMeasureOfficialURL']}" target="_blank">${ballotmeasure['ballotMeasureOfficialURL']}</a>
            </div>
        </div><!-- row -->
    % endif
    
    <div class="row spacer">
        <div class="col-xs-9 text-left">
            ${m.html(ballotmeasure['text'], render_flags=m.HTML_SKIP_HTML) | n}
        </div>
    </div><!-- row -->
    
    <div class="row spacer">
        <span class="grey">Posted by: </span>
        ${lib_6.userImage(author, className="avatar small-avatar")} ${lib_6.userLink(author)}
    </div><!-- row-->
    % if ballotmeasure.objType == 'revision':
        <div class="alert alert-error">
            This is a revision dated ${ballotmeasure.date}
        </div>
    % endif
</%def>

<%def name="showBallotcandidateInfo(ballotcandidate, author)">
    <div class="row spacer">
        <div class="col-xs-9 text-left">
            <h3>${ballotcandidate['title']}</h3>
        </div>
    </div><!-- row -->
    
    % if ballotcandidate['ballotCandidateParty'] != '':
        <div class="row spacer">
            <div class="col-xs-9 text-left">
                Party: ${ballotcandidate['ballotCandidateParty']}
            </div>
        </div><!-- row -->
    % endif
    
    % if ballotcandidate['ballotCandidateOfficialURL'] != '':
        <div class="row spacer">
            <div class="col-xs-9 text-left">
                Official Web Site: <a href="${ballotcandidate['ballotCandidateOfficialURL']}" target="_blank">${ballotcandidate['ballotCandidateOfficialURL']}</a>
            </div>
        </div><!-- row -->
    % endif

    <div class="row spacer">
        <div class="col-xs-9 text-left">
            ${m.html(ballotcandidate['text'], render_flags=m.HTML_SKIP_HTML) | n}
        </div>
    </div><!-- row -->
    
    <div class="row spacer">
        <span class="grey">Posted by: </span>
        ${lib_6.userImage(author, className="avatar small-avatar")} ${lib_6.userLink(author)}
    </div><!-- row -->
    % if ballotcandidate.objType == 'revision':
        <div class="alert alert-error">
            This is a revision dated ${ballotcandidate.date}
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
            public = c.election['election_public']
            electionDate = c.election['electionDate']
            electionOfficialURL = c.election['electionOfficialURL']
            if public == '1':
                publicChecked = 'checked'
            else:
                publicChecked = ""
        else:
            eScope = "0|0|0|0|0|0|0|0|0|0"
            title = ""
            tag = ""
            text = ""
            electionDate = ""
            electionOfficialURL = ""
            public = ""
            publicChecked = ""
    %>
    % if c.saveMessage and c.saveMessage != '':
        <div class="alert ${c.saveMessageClass}">
        <button type="button" class="close" data-dismiss="alert">&times;</button>
        ${c.saveMessage}
        </div>
    % endif
    <div class="row spacer>
        <div class="col-xs-12 text-left">
            % if c.edit:
                <form method="POST" name="edit_election" role="form" id="edit_ballot" action="/election/${c.election['urlCode']}/${c.election['url']}/electionEditHandler">
            % else:
                <form method="POST" name="edit_election" role="form" id="edit_ballot" action="/election/${c.authuser['urlCode']}/${c.authuser['url']}/electionNewHandler">
            % endif
            <div class="row">
                <h3>Election Information</h3>
            </div><!-- row -->
            <br>
            
            <div class="row">
                <div class="form-group">
                    <label for="electionTitle" class="control-label" required><strong>Election Title:</strong></label><br>
                    <input type="text" name="electionTitle" class="form-control" value="${title}"  required>
                </div><!-- form-group -->
            </div><!-- row -->
            
            <div class="row">
                <div class="form-group">
                    <label for="electionDate" class="control-label" required><strong>Election Date:</strong></label><br>
                    <input type="text" name="electionDate" class="col-xs-3" id="electionDate" value="${electionDate}" required>
                </div><!-- form-group -->
            </div><!-- row -->
            
            
            <div class="row spacer">
                <div class="form-group">
                    <label for="title" class="control-label" required><strong>Official Election URL:</strong></label><br>
                    <input type="text" name="electionOfficialURL" class="form-control" id="electionOfficialURL" value="${electionOfficialURL}">
                </div><!-- form-group -->
            </div><!-- row -->
            
            <div class="row spacer">
                <div class="form-group">
                    <label for="scope" class="control-label" required><strong>Public Jurisdiction:</strong></label><br>
                    ${geoSelect()}
                </div><!-- form-group -->
            </div><!-- row -->

            <div class="row spacer">
                <div class="form-group">
                    <label for="text" class="control-label" required><strong>Election Description:</strong></label>
                    ${lib_6.formattingGuide()}<br>
                    <textarea rows="10" class="form-control" id="electionText" name="electionText" required>${text}</textarea>
                </div>
            </div><!-- row -->
            
            
            <div class="row spacer">
                <div class="form-group">            
                    <input type="checkbox" name="public" ${publicChecked}> Publish this election
                </div><!-- form-group -->
            </div><!-- row -->

            <button type="submit" class="btn btn-warning btn-large pull-right" name="submit_summary">Save Changes</button>
        </form>
        </div><!-- col-xs-12 text-left -->
    </div><!-- row -->
</%def>


<%def name="editBallot()">
    <% 
        title = c.ballot['title']
        number = c.ballot.sort
        text = c.ballot['text']
        instructions = c.ballot['instructions']
        ballotSlate = c.ballot['ballotSlate']
        if 'slateInfo' in c.ballot:
            slateInfo = c.ballot['slateInfo']
        else:
            slateInfo = '1'
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
                $scope.measures = 0;
            };
            $scope.setCandidateNo = function() {
                $scope.candidate = 0;
                $scope.measures = 1;
            };
        }
    </script>
    <div class="row spacer>
        <div class="col-xs-12">
            <form method="POST" name="edit_ballot" id="edit_ballot" role="form" action="/ballot/${c.ballot['urlCode']}/${c.ballot['url']}/ballotEditHandler" ng-controller="Ctrl">
            <div class="row">
                <h3>Ballot Information</h3>
            </div><!-- ro -->
            <br>
            
            <div class="form-group">
                <label for="title" class="control-label" required><strong>Ballot Title:</strong></label><br>
                <input type="text" name="ballotTitle" class="form-control" value="${title}" required>
            </div><!-- form-group -->
            <div class="row spacer">
                <label for="ballotNumber" class="control-label" required><strong>Ballot Number in Election:</strong></label><br>
                <input type="text" name="ballotNumber" class="col-xs-1" value="${number}" required>
             </div><!-- row -->
            <div class="row spacer">
                <%
                    if c.ballot and c.ballot['ballotSlate'] == 'measures':
                        measuresChecked = 'checked'
                        candidatesChecked = ''
                    else:
                        measuresChecked = ''
                        candidatesChecked = 'checked'
                %>
                <label for="ballotSlate" class="control-label" required><strong>Ballot Slate Type:</strong></label><br>
                <label class="radio">
                    <input type="radio" name="ballotSlate" id="ballotSlate1" ng-model="ballotSlate1" value="measures" ng-click="setCandidateNo();" ${measuresChecked} required>
                    Ballot measures
                </label>
                <div ng-show="measures">
                    <label for="slateInfo1" class="control-label" required><strong>The term used to refer to the ballot measure. (Initiative, Proposition, etc):</strong></label>
                    <input type="text" name="slateInfo1" class="form-control" value="${slateInfo}" required>
                </div>
                <label class="radio">
                    <input type="radio" name="ballotSlate" id="ballotSlate2" ng-model="ballotSlate2" ng-click="setCandidateYes();" ${candidatesChecked} value="candidates" required>
                    Candidates for office
                </label>
                <div ng-show="candidate">
                    <label for="slateInfo2" class="control-label" required><strong>Can vote for max of how many candidates on slate:</strong></label>
                    <select name="slateInfo2">
                        <% 
                            voteMax = 20
                            loop = 1
                        %>
                        % while loop < voteMax + 1:
                            <%
                                if slateInfo == str(loop):
                                    selected = "selected"
                                else:
                                    selected = ""
                            %>
                            <option ${selected}>${loop}</option>
                            <% loop += 1 %>
                        % endwhile
                    </select>
                </div>
            </div><!-- row -->

            
            <div class="form-group spacer">
                <label for="text" class="control-label" required><strong>Ballot Description:</strong></label><br>
                ${lib_6.formattingGuide()}<br>
                <textarea rows="10" id="ballotText" name="ballotText" class="form-control" required>${text}</textarea>
            </div><!-- form-group -->
            <div class="form-group">
                <label for="text" class="control-label" required><strong>Ballot Instructions:</strong></label><br>
                <textarea rows="10" id="ballotInstructions" name="ballotInstructions" class="form-control" required>${instructions}</textarea>
            </div><!-- form-group -->
            <div class="form-group">            
                <p><button type="submit" class="btn btn-warning btn-large pull-right" name="submit_summary">Save Changes</button></p>
            </div><!-- form-group -->
        </form>
        </div><!-- col-xs-12  -->
    </div><!-- row -->
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
    <div class="row"><span id="planetSelect">
        <div class="col-xs-3 text-left">Planet:</div>
        <div class="col-xs-8 text-left">
            <select name="geoTagPlanet" id="geoTagPlanet" class="geoTagCountry">
                <option value="0">Earth</option>
            </select>
        </div><!-- col-xs-8 text-left -->
    </span><!-- countrySelect -->
    </div><!-- row -->     
    <div class="row"><span id="countrySelect">
        <div class="col-xs-3 text-left">Country:</div>
        <div class="col-xs-8 text-left">
            <select name="geoTagCountry" id="geoTagCountry" class="geoTagCountry">
                <option value="0">Select a country</option>
                <option value="United States" ${countrySelected}>United States</option>
            </select>
        </div><!-- col-xs-8 text-left -->
    </span><!-- countrySelect -->
    </div><!-- row -->
    <div class="row"><span id="stateSelect">
        % if c.country != "0":
            <div class="col-xs-3 text-left">State:</div>
            <div class="col-xs-8 text-left">
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
            </div><!-- col-xs-8 text-left -->
        % else:
            Leave 'Country' blank if the election jurisdiction applies to the entire planet.
        % endif
    </span></div><!-- row -->
    <div class="row"><span id="countySelect">
        % if c.state != "0":
            <% counties = getCountyList("united-states", c.state) %>
            <% cityMessage = "Leave blank 'County' blank if the election jurisdiction applies to the entire state." %>
            <div class="col-xs-3 text-left">County:</div>
            <div class="col-xs-8 text-left">
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
            </div><!-- col-xs-8 text-left -->
        % else:
            <% cityMessage = "" %>
            ${countyMessage}
        % endif
    </span></div><!-- row -->
    <div class="row"><span id="citySelect">
        % if c.county != "0":
            <% cities = getCityList("united-states", c.state, c.county) %>
            <% postalMessage = "Leave 'City' blank if the election jurisdiction applies to the entire county." %>
            <div class="col-xs-3 text-left">City:</div>
            <div class="col-xs-8 text-left">
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
            </div><!-- col-xs-8 text-left -->
        % else:
            <% postalMessage = "" %>
            ${cityMessage}
        % endif
        </span></div><!-- row -->
    <div class="row"><span id="postalSelect">
        % if c.city != "0":
            <% postalCodes = getPostalList("united-states", c.state, c.county, c.city) %>
            <% underPostalMessage = "or leave blank if your the election jurisdiction is specific to the entire city." %>
            <div class="col-xs-3 text-left">Zip Code:</div>
            <div class="col-xs-8 text-left8">
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
            </div><!-- col-xs-8 text-left -->
        % else:
            <% underPostalMessage = "" %>
            ${postalMessage}
        % endif
        </span></div><!-- row -->
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
                    $scope.measures = 0;
                };
                $scope.setCandidateNo = function() {
                    $scope.candidate = 0;
                    $scope.measures = 1;
                };
            }
        </script>
        <div class="row">
            <button type="button" class="btn btn-success" data-toggle="collapse" data-target="#addItem"><i class="icon icon-white icon-plus"></i> Ballot</button>
            <div id="addItem" class="collapse">
                <form action="/election/${election['urlCode']}/${election['url']}/ballotNewHandler" role="form" method="POST" ng-controller="Ctrl">
                    <div class="form-group spacer">
                        <label for="ballotTitle">Title</label><br>
                        <input type="text" name="ballotTitle" class="form-control" required>
                    </div><!-- form-group -->
                    <div class="form-group">
                        <label for="ballotNumber">Listing Order Number in Election</label><br>
                        <input type="text" name="ballotNumber" class="col-xs-1" required><br>
                    </div><!-- form-group -->
                    <div class="form-group spacer">
                        <label for="ballotSlate" class="control-label" required><strong>Ballot Slate Type:</strong></label>
                        <label class="radio">
                            <input type="radio" name="ballotSlate" id="ballotSlate1" value="measures" ng-click="setCandidateNo();"  required>
                            Ballot measures
                        </label>
                        <div ng-show="!candidate">
                            <label for="slateInfo" class="control-label"<strong>The term used to refer to the ballot measure. (Initiative, Proposition, etc):</strong></label>
                            <input type="text" name="slateInfoMeasures" class="span2" value="">
                        </div>
                        <label class="radio">
                            <input type="radio" name="ballotSlate" id="ballotSlate2" ng-model="ballotSlate2" ng-click="setCandidateYes();"  value="candidates" required>
                            Candidates for office
                        </label>
                        <div ng-show="candidate">
                            <label for="slateInfo" class="control-label"><strong>Can vote for max of how many candidates on slate:</strong></label>
                            <select name="slateInfoCandidates">
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
                    </div><!-- form-group -->
                    ${lib_6.formattingGuide()}
                    <div class="form-group spacer">
                        <label for="ballotText">Text</label><br>
                        <textarea rows="3" name="ballotText" class="form-control" required></textarea>
                    </div><!-- form-group -->
                    <div class="form-group">
                        <label for="ballotInstructions" >Instructions</label>
                        <textarea rows="3" name="ballotInstructions" class="form-control" required></textarea>
                    </div><!-- form-group -->
                    <div class="form-group">
                        <p><button class="btn btn-success" type="submit" class="btn">Save Item</button>
                        <button class="btn btn-danger" type="reset" value="Reset">Cancel</button></p>
                    </div><!-- form-group -->
                </form>
            </div>
        </div><!-- row -->
    % endif
</%def>

<%def name="addBallotMeasure(ballot, author)">
    % if 'user' in session and (c.authuser['email'] == author['email'] or userLib.isAdmin(c.authuser.id)):
        <div class="row">
            <button type="button" class="btn btn-success" data-toggle="collapse" data-target="#addItem"><i class="icon icon-white icon-plus"></i> Ballot Measure</button>
            <div id="addItem" class="collapse spacer">
                <form action="/ballot/${ballot['urlCode']}/${ballot['url']}/ballotMeasureAddHandler" role="form" method="POST">
                    <fieldset>
                        <label>Title</label>
                        <input type="text" name="ballotMeasureTitle" class="span6" required>
                        <label>Official Web Site URL</label>
                        <input type="text" name="ballotMeasureOfficialURL" class="span6" required>
                        <label>Listing Order Number in Ballot</label>
                        <input type="text" name="ballotMeasureNumber" class="span1" required>
                        <label>Text</label>
                        ${lib_6.formattingGuide()}<br>
                        <textarea rows="3" name="ballotMeasureText" class="span6" required></textarea>
                        
                        <p><button class="btn btn-success" type="submit" class="btn">Save Item</button>
                        <button class="btn btn-danger" type="reset" value="Reset">Cancel</button></p>
                    </fieldset>
                </form>
            </div>
        </div><!-- row -->
    % endif
</%def>

<%def name="addBallotCandidate(ballot, author)">
    % if 'user' in session and (c.authuser['email'] == author['email'] or userLib.isAdmin(c.authuser.id)):
        <div class="row-fluid">
            <button type="button" class="btn btn-success" data-toggle="collapse" data-target="#addItem"><i class="icon icon-white icon-plus"></i> Ballot Candidate</button>
            <div id="addItem" class="collapse spacer">
                <form action="/ballot/${ballot['urlCode']}/${ballot['url']}/ballotCandidateAddHandler" role="form" method="POST">
                    <div class="form-group">
                        <label for="ballotCandidateTitle">Title</label><br>
                        <input type="text" name="ballotCandidateTitle" class="form-control" required>
                    </div><!-- form-group -->
                    <div class="form-group">
                        <label for="ballotCandidateParty">Party</label><br>
                        <input type="text" name="ballotCandidateParty" class="form-control">
                    </div><!-- form-group -->
                    <div class="form-group">
                        <label for="ballotCandidateOfficialURL">Official Web Site URL</label><br>
                        <input type="text" name="ballotCandidateOfficialURL" class="form-control" required>
                    </div><!-- form-group -->
                    <div class="form-group">
                        <label for="ballotCandidateNumber">Listing Order Number in Ballot</label><br>
                        <input type="text" name="ballotCandidateNumber" class="col-xs-1" required>
                    </div><!-- form-group -->
                    <div class="form-group spacer">
                        <label for="ballotCandidateText">Text</label><br>
                        ${lib_6.formattingGuide()}<br>
                        <textarea rows="3" name="ballotCandidateText" class="form-control" required></textarea>
                    </div><!-- form-group -->
                    <div class="form-group">
                        
                        <p><button class="btn btn-success" type="submit" class="btn">Save Item</button>
                        <button class="btn btn-danger" type="reset" value="Reset">Cancel</button></p>
                    </div><!-- form-group -->
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
