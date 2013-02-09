<%!
    import time
    from pylowiki.lib.db.geoInfo import getGeoTitles, getStateList, getCountyList, getCityList, getPostalList
    from pylowiki.lib.db.user import getUserByEmail
    from pylowiki.lib.db.workshop import getCategoryTagList
    from pylowiki.lib.db.tag import getWorkshopTagCategories
%>

<%def name="fields_alert()">
	% if 'alert' in session:
		<% alert = session['alert'] %> 
        <div class="alert alert-${alert['type']}">
            ## bad char: ×
            ## good char: x
            <button data-dismiss="alert" class="close">x</button>
            <strong>${alert['title']}</strong>
        </div>
        <% 
           session.pop('alert')
           session.save()
        %>
	% endif
</%def>

<%def name="intro()">
    <div style="text-align: center">Build your workshop!<br />
    % if c.w['startTime'] == '0000-00-00':
       <br />Checklist must be completed before the workshop can be published.<br />
    % endif
    </div>
</%def>


<%def name="basic()">

    <%
      if c.w['startTime'] == '0000-00-00':
        wstarted = 0
      else:
        wstarted = 1
    %>
    <div class="section-wrapper">
        <div class="browse">
            <h4 class="section-header smaller">Setup Your Workshop</h4>
            <div class="row-fluid">
                <div class="span6">
                    <form name="edit_issue" id="edit_issue" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configureBasicWorkshopHandler" enctype="multipart/form-data" method="post" >
                            <legend>Settings</legend>
                            <label>Name</label>
                            <input id = "inputTitle" type="text" name="title" size="50" maxlength="70" value = "{{workshopTitle}}" ng-model = "workshopTitle" class="editWorkshopName"/>
                            <label>Description</label>
                            <input id = "inputDescription" type="text" name="description" size="50" maxlength="70" value = "${c.w['description']}" class="editWorkshopDescription"/>
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
                            <label>Participants can add ideas</label>
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
                            <label>Participants can add information resource links</label>
                            <label class="radio">
                                <input type="radio" id="allowResources" name="allowResources" value="1" ${yesChecked}> Yes
                            </label>
                            
                            <label class="radio">
                                <input type="radio" id="allowResources" name="allowResources" value="0" ${noChecked}> No
                            </label>
                            % if c.w['startTime'] == '0000-00-00':
                                <button type="submit" class="btn btn-warning">Save Settings and Continue</button>
                            % else:
                                <button type="submit" class="btn btn-warning">Save Settings</button>
                            % endif
                        </fieldset>
                    </form>
                </div><!-- span6 -->
                <div class="span6">
                <legend>Goals</legend>
                    ##The goals should <strong>briefly</strong> describe what you want to accomplish with the workshop, and what you want from the workshop participants. They are displayed on the workshop home page.<br />
                    <p class="muted">Double-click on an existing goal to edit.</p>
                    <div ng-controller="GoalsCtrl">
                        <p> {{remaining()}} of {{goals.length}} remaining </p>
                        <ul class="unstyled goalList">
                            <li ng-repeat="goal in goals">
                                <input type="checkbox" ng-model="goal.done" ng-click="goalStatus(goal)" class="goal-checkbox">
                                <span class="goal-title done-{{goal.done}}" ng-dblclick="goalEditState(goal)" ng-hide="goal.editing">{{goal.title}}</span>
                                <form ng-submit="goalEditDone(goal)" class="inline">
                                    <input type="text" ng-show="goal.editing" value="{{goal.title}}" ng-model="editTitle" maxlength="60" civ-focus="goal.editing" civ-blur="goalEditState(goal)">
                                </form>
                                <a ng-click="deleteGoal(goal)" class="inline pull-right"><img src="/images/glyphicons_pro/glyphicons/png/glyphicons_192_circle_remove.png" class="deleteGoal"></a>
                            </li>
                        </ul>
                        <form ng-submit="addGoal()" class="addGoal">
                            <div class="input-append">
                                <input type="text" ng-model="goalTitle" size="60" maxlength = "60" placeholder="New goal here" class="addGoal" id="addGoal">
                                <button class="btn btn-primary" type="submit" value="add">add</button>
                            </div>
                        </form>
                        <p class = "green">{{60 - goalTitle.length}}</p>
                    </div>
                </div><!-- span6 -->
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
            <h4 class="section-header smaller">Workshop Scope</h4>
            Specifiy if the workshop is public or private, and who may participate.<br /><br />
             ${change_scope()}
            <div class="tabbable">
                <ul class="nav nav-tabs" id="scopeTab">
                <li class="${privateActive}"><a href="#private" data-toggle="tab">Private Workshop</a></li>
                <li class="${publicActive}"><a href="#public" data-toggle="tab">Public Workhop</a></li>
                </ul>
                <div class="tab-content">
                    <div class="tab-pane ${privateActive}" id="private">${private()}</div>
                    <div class="tab-pane ${publicActive}" id="public">${public()}</div>
                </div><!-- tab-content -->
            </div><!-- tabbable -->
        </div><!-- browse -->
    </div><!-- section-wrapper -->              
</%def>

<%def name="tags()">
    <div class="section-wrapper">
        <div class="browse">
            <h4 class="section-header smaller">Category Tags</h4>
            Tags are descriptive key words used to categorize your workshop.<br />
            <form name="workshop_tags" id="workshop_tags" class="left form-inline" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configureTagsWorkshopHandler" enctype="multipart/form-data" method="post" >
            <div class="row-fluid">
                <div class="span1">
                </div><!-- span1 -->
                <div class="span5">
                    <% 
                        tagList = getWorkshopTagCategories()
                    %>
                    <br />
                    Choose at least one category: <span class="help-inline"><span class="label label-important">Required</span></span><br />
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
                    % if c.w['startTime'] == '0000-00-00':
                        <button type="submit" class="btn btn-warning">Save Tags and Continue</button>
                    % else:
                        <button type="submit" class="btn btn-warning">Save Tags</button>
                    % endif
                </div><!-- span5 -->
            </div><!-- row -->
            </form>
        </div><!-- browse -->
    </div><!-- section-header -->
</%def>



<%def name="edit_background()">
    <div class="section-wrapper">
        <div class="browse">
            <h4 class="section-header smaller">Workshop Introduction</h4>
            Help your workshop guests get started with an introduction to the issues covered in your workshop.  Keep it short—2-4 paragraphs works best.<br />
            <form name="workshop_background" id="workshop_background" class="left form-inline" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/update/background/handler" enctype="multipart/form-data" method="post" >
                <br /><strong>Introduce visitors to your workshop:</strong><br />
                <div class="well">
                    <textarea rows="10" id="data" name="data" >${c.page['data']}</textarea>
                    <div style="text-align:right; padding-right:35px;">
                        <button type="submit" class="btn btn-warning" name="submit">Save Changes</button>
                    </div><!-- text-align -->
                </div><!-- well -->
            </form>
        </div><!-- browse -->
    </div><!-- sectio-wrapper -->
</%def>

<%def name="change_scope()">
    % if c.w['type'] == 'professional':
        <%
            if c.w['public_private'] == 'public':
                currentScope = 'Public'
                newScope = 'Private'
            else:
                currentScope = 'Private'
                newScope = 'Public'
        %>
        <form name="scope" id="scope" class="left form-inline" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configure${newScope}WorkshopHandler" enctype="multipart/form-data" method="post" >
        Current scope: ${currentScope}  <button type="submit" class="btn btn-mini btn-warning" name="changeScope">Change to ${newScope}</button>     
        </form>
    % endif
</%def>

<%def name="private()">
    <ul>
    % if c.w['type'] == 'personal':
        <li>Personal workshops are private and limited to 10 participants.</li>
    % endif
    <li>Private workshops are not visible to the public.</li>
    <li>Private workshops are invitation only.</li>
    </ul>
    <form name="private" id="private" class="left form-inline" action="/workshop/${c.w['urlCode']}/${c.w['url']}/configurePrivateWorkshopHandler" enctype="multipart/form-data" method="post" >
    <br /><strong>Manage Workshop Participants List</strong><br />
    % if c.pmembers:        
        <br />${len(c.pmembers)} Private Members in This Workshop &bull; <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/listPrivateMembersHandler" target="_blank">Show List of Private Members</a><br /><br />
    % endif
    <!--
    <form name="private" id="private" class="left" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configurePrivateWorkshopHandler" enctype="multipart/form-data" method="post" >
    -->

        <div class="container-fluid well">
            <strong>Invite People To Your Workshop</strong><br>
            <div class="row-fluid">
                <div class="span6">
                Enter the email addresses of people to invite, one per line.<br />
                <textarea rows=6 cols=50 name="newMember"/></textarea>
                </div><!-- span6 -->
                <div class="span6">
                Click to email an invitation: <input type="checkbox" name="sendInvite" value="sendInvite"><br />
                Add optional message to invitation: <textarea rows=2 cols=50 name="inviteMsg"/></textarea><br />
                <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/previewInvitation" target="_blank">Preview Invitation</a> (will open in a new window)<br />

                </div><!-- span6 -->
            </div><!-- row-fluid -->
            <br /><button type="submit" class="btn btn-warning" name="addMember">Add Member to List</button>
        </div><!-- container-fluid -->

    % if c.pmembers:
        <div class="container-fluid well">
            <strong>Delete People From Your Workshop</strong><br>
            Choose email address to delete:<br />
            <select name="removeMember">
            % for pmember in c.pmembers:
                <option value="${pmember['email']}">${pmember['email']}</option>
            % endfor
            </select><br />
            <br /><button type="submit" class="btn btn-warning" name="deleteMember">Delete Member from List</button>
        </div><!-- container-fluid -->
    % endif
    % if c.w['startTime'] == '0000-00-00':
        <div class="container-fluid well">
            <button type="submit" class="btn btn-warning" name="continueToNext">Continue to Next Step</button>
        </div><!-- container-fluid -->
    % endif
    </form>
    <br />
</%def>

<%def name="public()">
    <ul>
    <li>Public workshops are visible to everyone!</li> 
    <li>Residents of the specificied geographic area are encouraged to participate.</li>
    <li>Unlimited participants!</li>
    </ul>
    <br />
    <p>Specify the geographic area associated with your workshop: <span class="label label-important">Required</span></span>:</p>
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
    <br />
    <form name="scope" id="scope" class="left form-inline" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configurePublicWorkshopHandler" enctype="multipart/form-data" method="post" >
    <div class="row-fluid"><span id="countrySelect">
        <div class="span1"></div><div class="span2">Country:</div><!-- span2 -->
        <div class="span9"><select name="geoTagCountry" id="geoTagCountry" class="geoTagCountry">
            <option value="0">Select a country</option>
            <option value="United States" ${countrySelected}>United States</option>
        </select>
        </div><!-- span9 -->
    </span>
    </div><!-- row -->
    <div class="row-fluid"><span id="stateSelect">
        % if c.country != "0":
            <div class="span1"></div><div class="span2">State:</div><div class="span9">
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
            </div><!-- span9 -->
        % else:
            or leave blank if your workshop is specific to the entire planet.
        % endif
    </span></div><!-- row-fluid -->
    <div class="row-fluid"><span id="countySelect">
        % if c.state != "0":
            <% counties = getCountyList("united-states", c.state) %>
            <% cityMessage = "or leave blank if your workshop is specific to the entire state." %>
            <div class="span1"></div><div class="span2">County:</div><div class="span9">
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
            </div><!-- span9 -->
        % else:
            <% cityMessage = "" %>
            ${countyMessage}
        % endif
    </span></div><!-- row -->
    <div class="row-fluid"><span id="citySelect">
        % if c.county != "0":
            <% cities = getCityList("united-states", c.state, c.county) %>
            <% postalMessage = "or leave blank if your workshop is specific to the entire county." %>
            <div class="span1"></div><div class="span2">City:</div><div class="span9">
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
            </div><!-- span9 -->
        % else:
            <% postalMessage = "" %>
            ${cityMessage}
        % endif
        </span></div><!-- row-fluid -->
    <div class="row-fluid"><span id="postalSelect">
        % if c.city != "0":
            <% postalCodes = getPostalList("united-states", c.state, c.county, c.city) %>
            <% underPostalMessage = "or leave blank if your workshop is specific to the entire city." %>
            <div class="span1"></div><div class="span2">Postal Code:</div><div class="span9">
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
            </div><!-- span9 -->
        % else:
            <% underPostalMessage = "" %>
            ${postalMessage}
        % endif
        </span></div><!-- row-fluid -->
    <div class="row-fluid"><span id="underPostal">${underPostalMessage}</span><br /></div><!-- row -->
    <br />
    <% 
        if c.w['startTime'] == '0000-00-00':
            buttonMsg = "Save And Continue To Next Step"
        else:
            buttonMsg = "Save Geographic Area"
    %>
    <div class="row-fluid">
        <div class="well">
            <button type="submit" class="btn btn-warning">${buttonMsg}</button>
        </div><!-- well -->
    </div><!-- row -->
    </form>
</%def>

<%def name="publish()">
    % if c.w['startTime'] == '0000-00-00' and c.basicConfig and c.slideConfig and c.backConfig and c.tagConfig:
        <div class="well">
            <form name="edit_issue" id="edit_issue" class="left form-inline" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configureStartWorkshopHandler" enctype="multipart/form-data" method="post" >
            <strong>Your workshop is ready to publish: </strong> <button type="submit" class="btn btn-warning" name="startWorkshop" value="Start" >Publish Workshop</button>
            </form>
        </div><!-- well -->
    % endif
</%def>
