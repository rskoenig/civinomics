<%!
    import time
    from pylowiki.lib.db.geoInfo import getGeoTitles, getStateList, getCountyList, getCityList, getPostalList
    from pylowiki.lib.db.user import getUserByEmail
    from pylowiki.lib.db.tag import getTagCategories
    import pylowiki.lib.db.workshop         as workshopLib
%>

<%def name="fields_alert()">
	% if 'alert' in session:
		<% alert = session['alert'] %> 
            <div class="alert alert-${alert['type']} workshop-admin" style="overflow: visible;">
                ## bad char: ×
                ## good char: x
                <button data-dismiss="alert" class="close">x</button>
                % if 'upgrade to a Professional' in alert['title']:
                    <div class="row">
                        <div class="col-sm-8">
                            <strong>${alert['title']}</strong>
                        </div>
                        <div class="col-sm-4">
                            <form name="workshopUpgrade" id="workshopUpgrade" action="/workshop/${c.w['urlCode']}/${c.w['url']}/upgrade/handler" method="POST" class="no-bottom">
                                <button type="submit" class="btn btn-large btn-civ pull-right">Upgrade to Pro</button>
                            </form>
                        </div>
                    </div>
                % else:
                    <strong>${alert['title']}</strong>
                % endif
            </div>
        <% 
           session.pop('alert')
           session.save()
        %>
	% endif
</%def>

<%def name="intro()">
    <div style="text-align: center">Build your workshop!<br />
    % if not c.published:
       <br />Checklist must be completed before the workshop can be published.<br />
    % endif
    </div>
</%def>


<%def name="basic()">

    <%
      if not c.started:
        wstarted = 0
      else:
        wstarted = 1
    %>
    <div class="section-wrapper">
        <div class="browse">
            <h4 class="section-header smaller">Basic Info</h4>
            <div class="row">
                <div class="col-sm-12" style="padding: 19px;">
                    <form name="edit_issue" id="edit_issue" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configureBasicWorkshopHandler" enctype="multipart/form-data" method="post" ng-cloak>
                        <fieldset>

                            <div class="form-group">
                                <div class="col-sm-12">
                                    <h4>Workshop Name</h4>
                                    <input id = "inputTitle" type="text" name="title" size="50" maxlength="100" value = "{{workshopTitle}}" ng-model = "workshopTitle" class="input-xxlarge editWorkshopName form-control"/>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="col-sm-12">
                                    <h4>Introduction</h4>
                                    <span class="muted">A one paragraph description why this matters.</span>
                                    <textarea rows="8" id = "inputDescription" name="description" size="50" class="col-sm-12 form-control">${c.w['description']}</textarea>
                                    <%
                                        if 'allowIdeas' in c.w and c.w['allowIdeas'] == '1':
                                            yesChecked = 'checked'
                                            noChecked = ''
                                        elif 'allowIdeas' in c.w and c.w['allowIdeas'] == '0':
                                            yesChecked = ''
                                            noChecked = 'checked'
                                        else:
                                            yesChecked = 'checked'
                                            noChecked = ''
                                    %>
                                </div>
                            </div>
                            <br>
                            <div class="spacer"></div>
                            <div class="form-group">
                                <div class="col-sm-12">
                                    <h4>Can participants add ideas</h4>
                                    <label class="radio">
                                        <input type="radio" id="allowIdeas" name="allowIdeas" value="1" ${yesChecked}> Yes
                                    </label>
                                    
                                    <label class="radio">
                                        <input type="radio" id="allowIdeas" name="allowIdeas" value="0" ${noChecked}> No
                                    </label>
                                    <% 
                                        if 'allowResources' in c.w and c.w['allowResources'] == '1':
                                            yesChecked = 'checked'
                                            noChecked = ''
                                        elif 'allowResources' in c.w and c.w['allowResources'] == '0':
                                            yesChecked = ''
                                            noChecked = 'checked'
                                        else:
                                            yesChecked = 'checked'
                                            noChecked = ''
                                    %>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="col-sm-12">
                                    <h4>Can participants add information resource links?</h4>
                                    <label class="radio">
                                        <input type="radio" id="allowResources" name="allowResources" value="1" ${yesChecked}> Yes
                                    </label>
                                    
                                    <label class="radio">
                                        <input type="radio" id="allowResources" name="allowResources" value="0" ${noChecked}> No
                                    </label>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="col-sm-12">
                                    <h4>Goals</h4>
                                    ##The goals should <strong>briefly</strong> describe what you want to accomplish with the workshop, and what you want from the workshop participants. They are displayed on the workshop home page.<br />
                                    <p class="muted">Double-click on an existing goal to edit.</p>
                                    <div ng-controller="GoalsCtrl">
                                        <p> {{remaining()}} of {{goals.length}} remaining </p>
                                        <ul class="unstyled goalList">
                                            <li ng-repeat="goal in goals">
                                                <span>
                                                <input type="checkbox" ng-model="goal.done" ng-click="goalStatus(goal)" class="goal-checkbox">
                                                <span class="goal-title done-{{goal.done}}" ng-dblclick="goalEditState(goal)" ng-hide="goal.editing">{{goal.title}}</span>
                                                <form ng-submit="goalEditDone(goal)" class="inline">
                                                    <input type="text" ng-show="goal.editing" value="{{goal.title}}" ng-model="editTitle" maxlength="100" civ-focus="goal.editing" civ-blur="goalEditState(goal)">
                                                </form>
                                                <a ng-click="deleteGoal(goal)" class="inline pull-right"><img src="/images/glyphicons_pro/glyphicons/png/glyphicons_192_circle_remove.png" class="deleteGoal"></a></span>
                                            </li>
                                        </ul>
                                        <form ng-submit="addGoal()" class="addGoal">
                                            <div class="input-group">
                                                <input type="text" ng-model="goalTitle" size="100" maxlength = "100" placeholder="New goal here" class="addGoal form-control" id="addGoal">
                                                <span class="input-group-btn">
                                                    <button class="btn btn-primary" type="submit" value="add">add</button>
                                                </span>
                                            </div>
                                        </form>
                                        <p class = "green">{{100 - goalTitle.length}}</p>
                                    </div>
                                </div>
                            </div>
                            <br>

                            % if not c.published:
                                <button type="submit" class="btn btn-warning btn-lg">Save Basic Info and Continue</button>
                            % else:
                                <button type="submit" class="btn btn-warning btn-lg">Save Basic Info</button>
                            % endif

                        </form>
                    </fieldset>
                </div><!-- col-sm-12 -->
            </div><!-- row -->
        </div><!-- browse -->
    </div><!-- section wrapper -->
</%def>

<%def name="scope()">
    <%
        if c.w['type'] == 'personal' or c.w['public_private'] == 'private':
            privateActive="active"
            publicActive="foo"
        else:
            privateActive="foo"
            publicActive="active"
    %>
        
    <div class="section-wrapper">
        <div class="browse">
            <h4 class="section-header smaller">Participants</h4>
            Specifiy if the workshop is public or private, and who may participate.
            <br>
            <br>
             ${change_scope()}

             % if c.w['public_private'] == 'private':
                <div class="tab-pane ${privateActive}" id="private">${private()}</div>
            % elif c.w['public_private'] == 'public':
                <div class="tab-pane ${publicActive}" id="public">${public()}</div>
            % endif

        </div><!-- browse -->
    </div><!-- section-wrapper -->              
</%def>

<%def name="tags()">
    <div class="section-wrapper">
        <div class="browse">
            <h4 class="section-header smaller">Tags</h4>
            Tags are descriptive key words used to categorize your workshop.<br />
            <form name="workshop_tags" id="workshop_tags" class="left form-inline" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configureTagsWorkshopHandler" enctype="multipart/form-data" method="post" >
            <div class="row">
                <div class="col-sm-1">
                </div><!-- span1 -->
                <div class="col-sm-5">
                    <% 
                        tagList = getTagCategories()
                    %>
                    <br />
                    <strong>Pick 1 or 2</strong> <span class="help-inline"><span class="label label-important">Required</span></span><br />
                    <fieldset>
                    % for tag in tagList:
                        % if tag in c.categories:
                            <% checked = 'checked' %>
                        % else:
                            <% checked = 'unchecked' %>
                        % endif
                        <label class="checkbox">
                        <input type="checkbox" name="categoryTags" value="${tag}" ${checked} /> ${tag}
                        </label><br />
                    % endfor
                    </fieldset>
                    <br />
                    % if not c.published:
                        <button type="submit" class="btn btn-warning btn-lg">Save Tags and Continue</button>
                    % else:
                        <button type="submit" class="btn btn-warning btn-lg">Save Tags</button>
                    % endif
                </div><!-- col-sm-5 -->
            </div><!-- row -->
            </form>
        </div><!-- browse -->
    </div><!-- section-header -->

    <script>
        $(function(){
            var max = 2;
            var checkboxes = $('input[type="checkbox"]');

            checkboxes.change(function(){
                var current = checkboxes.filter(':checked').length;
                checkboxes.filter(':not(:checked)').prop('disabled', current >= max);
                });
        });
    </script>
</%def>

<%def name="edit_ratings()">
	<div class="section-wrapper wiki-well">
		<div class="browse">
			<h4 class="section-header smaller"> Ratings </h4>
			<div class="col-sm-12" style="padding: 19px;" ng-controller="ratingsController">
			%if c.w['rating_criteria']:
				<p ng-init="initCriteria('${c.w['rating_criteria']}')"></p>
			%endif
				<div class="form-group">
					<form ng-submit="sendCriteriaList('${c.w['urlCode']}','${c.w['url']}')">
						<p>Choose the type of rating for the ideas in this workshop:</p>
						<div class="col-xs-6">			
							<input type="radio" name="rating_type" value="yesno" ng-model="rating.type"> Yes / No
						</div> <!-- col-xs-6 yesno -->
						
						<div class="col-xs-6">
							<input type="radio" name="rating_type" value="criteria" ng-model="rating.type"> Rated criteria 
							<div ng-show="rating.type === 'criteria'">
							 <ul >
	                                            <li ng-repeat="criteria in rating.criteriaList">
	                                                <span>
	                                                <span class="goal-title">{{criteria}}      </span>
	                                                <a class="inline" class="" ng-click="deleteCriteriaFromList(criteria)"><img src="/images/glyphicons_pro/glyphicons/png/glyphicons_192_circle_remove.png" class="deleteGoal" style="width:45%"></a></span>
	                                            </li>
	                                        </ul>
	                                        <div class="alert alert-danger" role="alert" ng-if="alert.message!='' && alert.type == 'error'">{{alert.message}}</div>
	                                        
	                                            <div class="input-group">
	                                                <input type="text" size="100" maxlength = "100" placeholder="Add a criteria" ng-model="criteriaName" class="addGoal form-control" id="">
	                                                <span class="input-group-btn">
	                                                    <button class="btn btn-primary" type="button" value="add" ng-click="addCriteriaToList(criteriaName)">add</button>
	                                                </span>
	                                            </div>
												<div class="alert alert-warning" role="alert" ng-if="alert.message!='' && alert.type === 'criteria'">{{alert.message}}</div>	
							</div>
							
						</div> <!-- col-xs-6 criteria -->
						% if not c.published:
                                <button type="submit" class="btn btn-warning btn-lg pull-right" style="margin-top:10px">Save Ratings and Continue</button>
                            % else:
                                <button type="submit" class="btn btn-warning btn-lg pull-right" style="margin-top:10px">Save Ratings</button>
                            % endif
					</form><!-- ratings form -->
				</div> <!-- form-group -->
			</div>	<!-- col-sm-12 -->
		</div> <!-- browse -->
	</div> <!-- section-wrapper -->
</%def>


<%def name="edit_background()">
    <div class="section-wrapper wiki-well">
        <div class="browse">
            <h4 class="section-header smaller">Background</h4>
            <a href="#" class="btn btn-mini btn-info pull-left bottom-space" onclick="window.open('/help/markdown.html','popUpWindow','height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');"><i class="icon-list"></i> <i class="icon-picture"></i> View Formatting Guide</a><br>
            <div class="row">
                <div class="col-xs-12">
                    <form name="workshop_background" id="workshop_background" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/update/background/handler" enctype="multipart/form-data" method="post" >
                        <div class="form-group">
                            <textarea rows="10" id="data" name="data" class="col-sm-12 form-control">${c.page['data']}</textarea>
                        </div>
                       <div class="background-edit-wrapper form-group">
                            % if not c.published:
                                <button type="submit" name="submit" class="btn btn-warning pull-right">Save Background and Continue</button>
                            % else:
                                <button type="submit" name="submit" class="btn btn-warning pull-right">Save Changes</button>
                            % endif
                       </div><!-- text-align -->
                    </form>
                    <div class="preview-information-wrapper" id="live_preview">
                       hi
                    </div>
                </div>
            </div>
            
        </div><!-- browse -->
    </div><!-- sectio-wrapper -->
</%def>

<%def name="change_scope()">
    <div class="col-sm-3"><strong>Current Scope:</strong></div>
        <%
            if c.w['public_private'] == 'public':
                currentScope = 'Public'
                newScope = 'Private'
            else:
                currentScope = 'Private'
                newScope = 'Public'
        %>
        <form name="scope" id="scope" class="left form-inline" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configure${newScope}WorkshopHandler" enctype="multipart/form-data" method="post" >
            <div class="row">
                <div class="col-sm-2">
                    <label class="radio">
                        <input type="radio" name="optionsRadios" id="optionsRadios1" value="Private" 
                        % if currentScope == 'Private':
                            checked
                        % endif
                        >
                        Private  <i class="icon-group set-scope-icon"></i>
                    </label>
                </div>
                <div class="col-sm-2">
                    <label class="radio">
                    % if c.w['type'] == 'professional':
                        <input type="radio" name="optionsRadios" id="optionsRadios2" value="Public"
                        % if currentScope == 'Public':
                            checked
                        % endif
                        >
                        Public  <i class="icon-globe set-scope-icon"></i>
                    % else:
                    <button class="transparent">
                        <input type="radio" name="optionsRadios" id="optionsRadios2" value="Public" disabled>
                    </button>
                        Public  <i class="icon-globe set-scope-icon"></i>
                    % endif
                    </label>
                </div>
                <div class="col-sm-3">
                    % if c.w['type'] == 'professional':
                        <button type="submit" class="btn btn-warning" name="changeScope">Change Scope</button>
                    % else:
                        <button class="disabled btn btn-warning">Change Scope</button>
                    % endif
                </div> 
            </div>  
        </form>
</%def>

<%def name="private()">

    % if c.w['public_private'] != 'public':
        <div class="container-fluid well">
            <table class="boxOffsetParent">
                <tr>
                    <td rowspan="2" class="scope-icon">
                        <i class="icon-group icon-4x"></i>
                    </td>
                    <td>
                        <h4><lead>Private</lead></h4>
                    </td>
                </tr>
                <tr>
                    <td>
                        <ul>
                            <li>Private workshops are not visible to the public.</li>
                            <li>Private workshops are invitation only.</li>
                            % if c.w['type'] == 'personal':
                                <li>Free workshops are limited to 20 participants.</li>
                            % endif
                        </ul>
                    </td>
                </tr>
            </table>
            <hr>
            <div class="row">
                <strong>Add People</strong><br>
                    ${emailInvite()}
                    <br>

                    % if c.pmembers:
                        <form name="private" id="private" class="left form-inline" action="/workshop/${c.w['urlCode']}/${c.w['url']}/configurePrivateWorkshopHandler" enctype="multipart/form-data" method="post" >
                            <hr>
                            <strong>Workshop Members (${len(c.pmembers)})</strong><br>
                            <br>
                            
                            <% 
                                memberList = []
                                for pmember in c.pmembers:
                                    memberList.append(pmember['email'])
                                memberList.sort()
                            %>

                            <select name="selected_members">
                            % for member in memberList:
                                <option valuevalue="${member}">${member}</option>
                            % endfor
                            </select>

                            <button type="submit" class="btn" name="resendInvites"><i class="icon-envelope"></i> Resend Invite</button>
                            <button type="submit" class="btn btn-danger" name="deleteMembers"><i class="icon-trash icon-white"></i> Delete Member</button><br>
                            <br>
                        </form>
                    % endif
            </div><!-- row -->
        </div><!-- container-fluid -->
    % endif
    </form>
    <br />
</%def>

<%def name="public()">
    <div class="container-fluid well">
        <table class="boxOffsetParent">
            <tr>
                <td rowspan="2" class="scope-icon">
                    <i class="icon-globe icon-4x"></i>
                </td>
                <td>
                    <h4><lead>Public</lead></h4>
                </td>
            </tr>
            <tr>
                <td>
                    <ul>
                        <li>Public workshops are visible to everyone.</li>
                        <li>Residents of the specified geographic area will be encouraged to participate.</li>
                        <li>Unlimited participants.</li>
                    </ul>
                </td>
            </tr>
        </table>
        <br>
        <hr>
        <strong>Geographic Area</strong><br> 
        <br>
        <p>Specify the geographic area associated with your workshop:</p>
        <% 
            countrySelected = ""
            countyMessage = ""
            cityMessage = ""
            postalMessage = ""
            underPostalMessage = ""
            if c.country!= "0":
                countrySelected = "selected"
                states = getStateList("united-states")
                countyMessage = "or leave blank if your workshop is specific to the entire country."
            else:
                countrySelected = ""
            endif
        %>
        <form name="scope" id="scope" class="left" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configurePublicWorkshopHandler" enctype="multipart/form-data" method="post" >  
        <div class="row"><span id="planetSelect">
            <div class="col-sm-1"></div><div class="col-sm-2">Planet:</div>
            <div class="col-sm-9">
                <select name="geoTagPlanet" id="geoTagPlanet" class="geoTagCountry">
                    <option value="0">Earth</option>
                </select>
            </div><!-- col-sm-9 -->
        </span><!-- countrySelect -->
        </div><!-- row -->     
        <div class="row"><span id="countrySelect">
            <div class="col-sm-1"></div><div class="col-sm-2">Country:</div>
            <div class="col-sm-9">
                <select name="geoTagCountry" id="geoTagCountry" class="geoTagCountry">
                    <option value="0">Select a country</option>
                    <option value="United States" ${countrySelected}>United States</option>
                </select>
            </div><!-- col-sm-9 -->
        </span><!-- countrySelect -->
        </div><!-- row -->
        <div class="row"><span id="stateSelect">
            % if c.country != "0":
                <div class="col-sm-1"></div><div class="col-sm-2">State:</div><div class="col-sm-9">
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
                </div><!-- col-sm-9 -->
            % else:
                or leave blank if your workshop is specific to the entire planet.
            % endif
        </span></div><!-- row -->
        <div class="row"><span id="countySelect">
            % if c.state != "0":
                <% counties = getCountyList("united-states", c.state) %>
                <% cityMessage = "or leave blank if your workshop is specific to the entire state." %>
                <div class="col-sm-1"></div><div class="col-sm-2">County:</div><div class="col-sm-9">
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
                </div><!-- col-sm-9 -->
            % else:
                <% cityMessage = "" %>
                ${countyMessage}
            % endif
        </span></div><!-- row -->
        <div class="row"><span id="citySelect">
            % if c.county != "0":
                <% cities = getCityList("united-states", c.state, c.county) %>
                <% postalMessage = "or leave blank if your workshop is specific to the entire county." %>
                <div class="col-sm-1"></div><div class="col-sm-2">City:</div><div class="col-sm-9">
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
                </div><!-- col-sm-9 -->
            % else:
                <% postalMessage = "" %>
                ${cityMessage}
            % endif
            </span></div><!-- row -->
        <div class="row"><span id="postalSelect">
            % if c.city != "0":
                <% postalCodes = getPostalList("united-states", c.state, c.county, c.city) %>
                <% underPostalMessage = "or leave blank if your workshop is specific to the entire city." %>
                <div class="col-sm-1"></div><div class="col-sm-2">Postal Code:</div><div class="col-sm-9">
                <select name="geoTagPostal" id="geoTagPostal" class="geoTagPostal" onChange="geoTagPostalChange(); return 1;">
                <option value="0">Select a postal code</option>
                    % for pCode in postalCodes:
                        % if c.postal == str(pCode['ZipCode']):
                            <% postalSelected = "selected" %>
                        % else:
                            <% postalSelected = "" %>
                        % endif
                        <option value="${pCode['ZipCode']}" ${postalSelected}>${pCode['ZipCode']}</option>
                    % endfor
                </select>
                </div><!-- col-sm-9 -->
            % else:
                <% underPostalMessage = "" %>
                ${postalMessage}
            % endif
            </span></div><!-- row -->
        <div class="row"><span id="underPostal">${underPostalMessage}</span><br /></div><!-- row -->
        <br />
        <% 
            buttonMsg = "Save Geographic Area"
        %>
        <div class="row">
                <button type="submit" class="btn btn-warning">${buttonMsg}</button>
        </div><!-- row -->
        </form>
        <hr>
        <strong>Invite Participants</strong><br>
        <br>
        <span class="help-inline">Share this Link:  </span>
        <input type="text" class="col-sm-9 form-control" value="${c.shareURL}"></input>
        <br>
        <!--
        <br>
        <strong>Share on Facebook; Tweet</strong>
        <br> -->
        <br>
        <div class="row centered"><strong><em>OR</em></strong></div>
        <br>
        ${emailInvite()}
    </div>

</%def>

<%def name="publish()">
    % if not c.started and c.basicConfig and c.slideConfig and c.backConfig and c.tagConfig and c.participantsConfig:
        <div>
            <form name="edit_issue" id="edit_issue" class="left form-inline no-bottom" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configureStartWorkshopHandler" enctype="multipart/form-data" method="post" >
            <button type="submit" class="btn btn-warning btn-block btn-lg" name="startWorkshop" value="Start" >Publish Workshop</button>
            </form>
        </div>

    % elif c.w['startTime'] == '0000-00-00':
        <button class="btn btn-warning btn-block btn-lg disabled publishButton" rel="tooltip" data-placement="bottom" data-original-title="You must complete all steps before publishing your workshop">Publish Workshop</button>

    % else:
        <form class="no-bottom" action="/workshop/${c.w['urlCode']}/${c.w['url']}/publish/handler" method=POST>
            % if workshopLib.isPublished(c.w):
                <button type="submit" class="btn btn-warning btn-block btn-lg publishButton" value="unpublish" rel="tooltip" data-placement="bottom" data-original-title="This will temporarily unpublish your workshop, removing it from listings and activity streams.">Unpublish Workshop</button>
            % else:
                <button type="submit" class="btn btn-warning btn-block btn-lg publishButton" value="publish" rel="tooltip" data-placement="bottom" data-original-title="Republishes your workshop, making it visible in listings and activity streams.">Publish Workshop</button>
            % endif
        </form>

    % endif
</%def>

<%def name="emailInvite()">
    <form name="private" id="private" action="/workshop/${c.w['urlCode']}/${c.w['url']}/configurePrivateWorkshopHandler" enctype="multipart/form-data" method="post" >
        <div class="form-group">
            <label for="newMember" class="help-inline">Enter the email addresses of people to invite, separated by commas or cut and paste from Excel.</label>
            <textarea class="form-control" rows=1 name="newMember"/></textarea>
        </div><!-- row -->
        <div class="form-group">
            <label for="inviteMsg" class="help-inline">Add optional message to email invitation:</label>
            <textarea class="form-control" rows=2 name="inviteMsg"/></textarea><br />
            <!-- 
            <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/previewInvitation" target="_blank">Preview Invitation</a> (will open in a new window)<br />
            -->
        </div><!-- row -->
        <br /><button type="submit" class="btn btn-primary" name="addMember"><i class="icon-envelope icon-white"></i> Send Invites</button>
    </form>
</%def>
