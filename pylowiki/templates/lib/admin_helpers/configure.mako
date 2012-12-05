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
    <h3>Settings</h3>
    <br />
    <div class="row">
        <div class="span1">
        </div><!-- span1 -->
        <div class="span6">
            <form name="edit_issue" id="edit_issue" class="left form-inline" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configureBasicWorkshopHandler" enctype="multipart/form-data" method="post" >
            <strong>Workshop Name:</strong>
            <br />
            <input type="text" name="title" size="50" maxlength="70" value = "${c.w['title']}"/>  <span class="help-inline"><span class="label label-important">Required</span></span>
            <br />
            <br />
            <strong>Workshop Goals:</strong>
            <br />
            <textarea name="goals" rows="5" cols="50">${c.w['goals']}</textarea>  <span class="help-inline"><span class="label label-important">Required</span></span>
            <br /><br />
            % if wstarted == 0 and c.account and c.account['type'] != 'trial': 
                <%
                    if 'public_private' in c.w and (c.w['public_private'] == 'public' or c.w['public_private'] == 'trial'):
                        publicChecked = 'checked'
                        privateChecked = ''
                    else:
                        publicChecked = ''
                        privateChecked = 'checked'
                %>

                <strong>Workshop Type:</strong><br />
                <input type="radio" name="publicPrivate" value="public" ${publicChecked} /> Public<br />
                This means the workshop may be browsed by the public, and any members residing in the specificied geographic area may participate.<br /><br />
                <input type="radio" name="publicPrivate" value="private" ${privateChecked} /> Private<br />
                This means the workshop is not visible to the public, and any only members on the private email address or email domain list may browse and participate in the workshop.<br /><br />
            % else:
                <p><strong>Workshop Type</strong>: ${c.w['public_private']}<p>
            % endif
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
            <strong>Workshop Suggestions and Resources:</strong><br />
            Allow members to add suggestions: <input type=radio name=allowSuggestions value=1 ${yesChecked}> Yes &nbsp;&nbsp;&nbsp;<input type=radio name=allowSuggestions value=0 ${noChecked}> No<br /><br />
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
            Allow members to add resource links: <input type=radio name=allowResources value=1 ${yesChecked}> Yes &nbsp;&nbsp;&nbsp;<input type=radio name=allowResources value=0 ${noChecked}> No<br />
            <br />
            <button type="submit" class="btn btn-warning">Save Settings</button>
            </form>
        </div><!-- span5 -->
    </div><!-- row -->
    </div><!-- well -->
</%def>

<%def name="scope()">
    <div class="well">
    % if c.w['public_private'] == 'public':
        <h3>Public Workshop</h3>
    % elif c.w['public_private'] == 'private':
        <h3>Private Workshop</h3>
    % else:
        <h3>Private Trial Workshop</h3>
    % endif
    % if c.w['public_private'] != 'public':
        ${private()}
    % else:
        ${public()}
    % endif
    </div><!-- well -->
</%def>

<%def name="tags()">
    <div class="well">
    <h3>Category Tags </h3>
    <br />
    Tags are descriptive key words used to categorize your workshop. <br />
    <form name="workshop_tags" id="workshop_tags" class="left form-inline" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configureTagsWorkshopHandler" enctype="multipart/form-data" method="post" >
    <div class="row">
        <div class="span1">
        </div><!-- span1 -->

        <div class="span5">
            <% tagList = getCategoryTagList() %>
            <% tags = c.w['categoryTags'] %>
            <% workshopTags = tags.split('|') %>
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
            <button type="submit" class="btn btn-warning">Save Tags</button>
        </div><!-- span5 -->
    </div><!-- row -->
    </form>
    </div><!-- well -->

</%def>



<%def name="edit_background()">
    <h3>Summarize</h3>
    Use the wiki editor below to provide introductory background information about your workshop topic and goals. What do participants need to know about the topic? What do you hope to accomplish in this workshop?  
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
                    -->
                    ${h.submit('submit', 'Save')}
                </div>
            </div>
        </div> <!-- /#wiki-section-break -->
        <% counter += 1 %>
    % endfor
    ${h.hidden("count",counter)}
    ${h.hidden("configure","configure")}
    ${h.end_form()}
    <br /><br />
</%def>


<%def name="private()">
    <form name="private" id="private" class="left form-inline" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configurePrivateWorkshopHandler" enctype="multipart/form-data" method="post" >
    <strong>Manage Workshop Participants List</strong>
    % if c.w['public_private'] == 'trial':
        <p>Trial workshops are not visible to the public.</p>
        <p>Up to 10 other members may participate in your trial workshop. Enter the email address of members you wish to participate in this workshop.<p>
    % else:
        <p>Private workshops are not visible to the public.</p>
        <p>Specify the email addresses of the members you wish to participate in this workshop.</p>
        <p>Members with specified email addresses will see a link to your workshop in their member profiles. They must be registered members using the email address specified here.</p>
    % endif
    % if c.pmembers:        
        <br /><br />${len(c.pmembers)} Private Members in This Workshop<br /><br />
    % endif
    <form name="private" id="private" class="left" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configurePrivateWorkshopHandler" enctype="multipart/form-data" method="post" >
        To add new private members to this workshop,
        enter one or more email addresses, one per line. This does not send an email invitation:<br />
        <textarea rows=6 cols=50 name="newMember"/></textarea>
        <br /><br />
        <button type="submit" class="btn btn-warning" name="addMember">Add Member to List</button>
  
    % if c.pmembers:
        <br /><br />
        Delete a private member from this workshop:<br />
        Email Address: <input type="text" name = "removeMember" size="50" maxlength="140""/>
        <br /><br />
        <button type="submit" class="btn btn-warning" name="deleteMember">Delete Member from List</button>

    % endif
    </form>
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
    <button type="submit" class="btn btn-warning">Save Scope</button>
    </form>
</%def>

<%def name="publish()">
    % if c.w['startTime'] == '0000-00-00' and c.account['type'] != 'trial' and c.basicConfig and c.slideConfig and c.backConfig and c.tagConfig:
        <div class="well">
            <form name="edit_issue" id="edit_issue" class="left form-inline" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configureStartWorkshopHandler" enctype="multipart/form-data" method="post" >
            <strong>Your workshop is ready to publish: </strong> <button type="submit" class="btn btn-warning" name="startWorkshop" value="Start" >Publish Workshop</button>
            </form>
        </div><!-- well -->
    % endif
</%def>
