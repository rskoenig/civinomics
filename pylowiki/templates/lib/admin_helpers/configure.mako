<%!
    from pylowiki.lib.db.geoInfo import getGeoTitles, getStateList, getCountyList, getCityList
    from pylowiki.lib.db.user import getUserByEmail
    from pylowiki.lib.db.workshop import getCategoryTagList
%>

<%def name="fields_alert()">
	% if 'alert' in session:
		<% alert = session['alert'] %> 
        <div class="alert alert-${alert['type']}">
            <button data-dismiss="alert" class="close">×</button>
            <strong>${alert['title']}</strong>
        </div>
        <% 
           session.pop('alert')
           session.save()
        %>
	% endif
</%def>

<%def name="intro()">
    Use these forms to configure your workshop.<br />
    % if c.w['startTime'] == '0000-00-00':
       <br />Checklist must be completed before the workshop can be published.<br />
    % endif
</%def>


<%def name="basic()">

    <%
      if c.w['startTime'] == '0000-00-00':
        wstarted = 0
      else:
        wstarted = 1
    %>
    <div class="well">
    <h3>Setup Your Workshop</h3>
    Describe your workshop topic and goals here, and configure how members can participate.
    <br /><br />
    <div class="row">
        <div class="span1">
        </div><!-- span1 -->
        <div class="span10">
            <form name="edit_issue" id="edit_issue" class="left form-inline" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configureBasicWorkshopHandler" enctype="multipart/form-data" method="post" >
            <strong>Workshop Name:</strong> <span class="label label-important">Required</span>
            <br />
            The name should act as a short description of the workshop topic. It is displayed in listings and the workshop home page. (70 char max)<br />
            <input type="text" name="title" size="50" maxlength="70" value = "${c.w['title']}"/>
            <br />
            <br />
            <strong>Workshop Goals:</strong> <span class="label label-important">Required</span>
            <br />
            The goals should <strong>briefly</strong> describe what you want to accomplish with the workshop, and what you want from the workshop participants. They are displayed on the workshop home page.<br />
            <textarea name="goals" rows="5" cols="50">${c.w['goals']}</textarea>
            <br /><br />
            <%
                if 'allowSuggestions' in c.w and c.w['allowSuggestions'] == '1':
                    yesChecked = 'checked'
                    noChecked = ''
                elif 'allowSuggestions' in c.w and c.w['allowSuggestions'] == '0':
                    yesChecked = ''
                    noChecked = 'checked'
                else:
                    yesChecked = 'checked'
                    noChecked = ''
            %>
            <strong>What can participants do in your workshop:</strong><br />
            Participants can add ideas: <input type=radio name=allowSuggestions value=1 ${yesChecked}> Yes &nbsp;&nbsp;&nbsp;<input type=radio name=allowSuggestions value=0 ${noChecked}> No<br /><br />
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
            Participants can add information resource links: <input type=radio name=allowResources value=1 ${yesChecked}> Yes &nbsp;&nbsp;&nbsp;<input type=radio name=allowResources value=0 ${noChecked}> No<br />
            <br />
            % if c.w['startTime'] == '0000-00-00':
                <button type="submit" class="btn btn-warning">Save Settings and Continue</button>
            % else:
                <button type="submit" class="btn btn-warning">Save Settings</button>
            % endif
            </form>
        </div><!-- span10 -->
    </div><!-- row -->
    </div><!-- well -->
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
        
    <div class="well">
        <h3>Workshop Scope</h3>
        Specifiy if the workshop is public or private, and who may participate.<br /><br />
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
    </div><!-- well -->               
</%def>

<%def name="tags()">
    <div class="well">
    <h3>Category Tags </h3>
    Tags are descriptive key words used to categorize your workshop.<br />
    <form name="workshop_tags" id="workshop_tags" class="left form-inline" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configureTagsWorkshopHandler" enctype="multipart/form-data" method="post" >
    <div class="row">
        <div class="span1">
        </div><!-- span1 -->

        <div class="span5">
            <% tagList = getCategoryTagList() %>
            <% tags = c.w['categoryTags'] %>
            <% workshopTags = tags.split('|') %>
            <br />
            Choose at least one category: <span class="help-inline"><span class="label label-important">Required</span></span><br />
            % for tag in tagList:
                % if tag in workshopTags:
                    <% checked = 'checked' %>
                % else:
                    <% checked = 'unchecked' %>
                % endif
                <input type="checkbox" name="categoryTags" value="${tag}" ${checked} /> ${tag}<br />
            % endfor
            <br />
            % if c.w['startTime'] == '0000-00-00':
                <button type="submit" class="btn btn-warning">Save Tags and Continue</button>
            % else:
                <button type="submit" class="btn btn-warning">Save Tags</button>
            % endif
        </div><!-- span5 -->
    </div><!-- row -->
    </form>
    </div><!-- well -->

</%def>



<%def name="edit_background()">
    <h3>Summarize Your Workshop</h3>
    Use the wiki editor below to provide introductory background information about your workshop topic and goals. What do participants need to know about the topic? What do you hope to accomplish in this workshop? This information will appear on the workshop home page with the slideshow.  
    <br /><br />
    ${h.form(url(controller = "wiki", action ="handler", id1 = c.w['urlCode'], id2 = c.w['url']),method="put")}
    <% counter = 0 %>
    % for row in c.wikilist:
        <div id="wiki-section-break">
            <% numrows = 10 %>
            <strong>Preview your edits for this section here:</strong><br />
            <div class="well">
            % if c.authuser.id == c.w.owner or int(c.authuser['accessLevel']) >= 200:
                <table><tr><td>
                    <div id = "section${counter}" ondblclick="toggle('textareadiv${counter}', 'edit${counter}', 'edit')">${row[0]}</div>
                </td></tr></table>
            % else:
                <table><tr><td>
                    <div id = "section${counter}" >${row[0]}</div>
                </td></tr></table>
            % endif
            </div><!-- well -->

            <strong>Make edits for this section here:</strong><br />
            <div class="well" id="textareadiv${counter}">
                <textarea rows="${numrows}" id="textarea${counter}" name="textarea${counter}" onkeyup="previewAjax( 'textarea${counter}', 'section${counter}' )" class="markitup">${row[1]}</textarea>
                <div style="text-align:right; padding-right:35px;">
                    <!--
                    <input type="text" id="remark${counter}"  name="remark${counter}" class="text tiny" placeholder="Optional remark"/>
                    ${h.submit('submit', 'Save')}
                    -->
                    <button type="submit" class="btn btn-warning" name="submit">Save Changes</button>
                </div>
            </div>
        </div> <!-- /#wiki-section-break -->
        <% counter += 1 %>
    % endfor
    ${h.hidden("count",counter)}
    ${h.hidden("dashboard","dashboard")}
    ${h.end_form()}
    <br /><br />
</%def>


<%def name="private()">
    <p>Private workshops are not visible to the public.</p>
    % if c.w['type'] == 'personal':
        <p>Up to 10 other members may participate in your personal workshop.</p>
    % elif c.w['public_private'] == 'private':
        <form name="scope" id="scope" class="left form-inline" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configureScopeWorkshopHandler" enctype="multipart/form-data" method="post" >
        You can make this a public workshop if you wish.<br>This means the workshop will be visible to the public, and members residing in the specified geographic area can participate in the workshop.<br />
        <button type="submit" class="btn btn-warning" name="changeScopeToPublic">Change to Public Workshop</button>
        </form>
    % endif
    <form name="private" id="private" class="left form-inline" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configurePrivateWorkshopHandler" enctype="multipart/form-data" method="post" >
    <p>Specify the email addresses of the members you wish to participate in this workshop.</p>
    <p>Members with specified email addresses will see a link to your workshop in their member profiles. They must be registered members using the email address specified here.</p>
    <br /><strong>Manage Workshop Participants List</strong><br />
    % if c.pmembers:        
        <br />${len(c.pmembers)} Private Members in This Workshop &bull; <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/listPrivateMembersHandler" target="_blank">Show List of Private Members</a><br /><br />
    % endif
    <form name="private" id="private" class="left" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configurePrivateWorkshopHandler" enctype="multipart/form-data" method="post" >


        <div class="container-fluid well">
            <strong>Add New Member</strong><br>
            <div class="row-fluid">
                <div class="span6">
                To add new private members to this workshop, enter one or more email addresses, one per line.<br />
                <textarea rows=6 cols=50 name="newMember"/></textarea>
                </div><!-- span6 -->
                <div class="span6">
                Click to email an invitation: <input type=checkbox name=sendInvite value=sendInvite><br />
                Add optional message to invitation: <textarea rows=2 cols=50 name="inviteMsg"/></textarea><br />
                <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/previewInvitation" target="_blank">Preview Invitation</a> (will open in a new window)<br />

                </div><!-- span6 -->
            </div><!-- row-fluid -->
            <br /><button type="submit" class="btn btn-warning" name="addMember">Add Member to List</button>
        </div><!-- container-fluid -->

    % if c.pmembers:
        <div class="container-fluid well">
            <strong>Delete Member</strong><br>
            Delete a private member from this workshop.<br />
            Enter member email address to delete:<br />
            <input type="text" name="removeMember" /><br />
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
    <p>This means the workshop may be browsed by the public, and any members residing in the specificied geographic area may participate.</p>

    <p>Specify the geographic area associated with your workshop: <span class="label label-important">Required</span></span>:</p>
    <% 
        countrySelected = ""
        countyMessage = ""
        cityMessage = ""
        underCityMessage = ""
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
            <option ${countrySelected}>United States</option>
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
            <% underCityMessage = "or leave blank if your workshop is specific to the entire county." %>
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
            <% underCityMessage = "" %>
            ${cityMessage}
        % endif
        </span></div><!-- row-fluid -->
    <div class="row-fluid"><span id="underCity">${underCityMessage}</span><br /></div><!-- row -->
    <br />
    <% 
        if c.w['startTime'] == '0000-00-00':
            buttonMsg = "Save And Continue To Next Step"
        else:
            buttonMsg = "Save Geographic Area"
    %>
    <div class="well">
        <button type="submit" class="btn btn-warning">${buttonMsg}</button>
    </div><!-- well -->
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
