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


<%def name="edit_background()">
    <h3>Background Information</h3>
    <br /><br />
    ${h.form(url(controller = "wiki", action ="handler", id1 = c.w['urlCode'], id2 = c.w['url']),method="put")}
    <% counter = 0 %>
    % for row in c.wikilist:
        <div id="wiki-section-break">
            <% numrows = 10 %>
            % if c.authuser.id == c.w.owner or int(c.authuser['accessLevel']) >= 200:
                <table style="width: 100%; padding: 0px; border-spacing: 0px; border: 0px; margin: 0px;"><tr><td>
                    <div id = "section${counter}" ondblclick="toggle('textareadiv${counter}', 'edit${counter}', 'edit')">${row[0]}</div>
                </td></tr></table>
            % else:
                <table style="width: 100%; padding: 0px; border-spacing: 0px; border: 0px; margin: 0px;"><tr><td>
                    <div id = "section${counter}" >${row[0]}</div>
                </td></tr></table>
            % endif


            <div class="well" id="textareadiv${counter}">
                <br />
                <textarea rows="${numrows}" id="textarea${counter}" name="textarea${counter}" onkeyup="previewAjax( 'textarea${counter}', 'section${counter}' )" class="markitup">${row[1]}</textarea>
                <div style="text-align:right; padding-right:35px;">
                    <input type="text" id="remark${counter}"  name="remark${counter}" class="text tiny" placeholder="Optional remark"/>

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
    <button type="submit" class="btn btn-warning">Save Basic Information</button>
    </form>
    </div><!-- well -->
</%def>

<%def name="tags()">
    <div class="well">
    <h3>Tags</h3>
    <br />
    Tags are descriptive key words used to categorize your workshop.<br />
    <form name="workshop_tags" id="workshop_tags" class="left form-inline" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configureTagsWorkshopHandler" enctype="multipart/form-data" method="post" >
    <div class="row">
        <div class="span1">
        </div><!-- span1 -->
        <div class="span5">
            <br />
            <strong>Workshop Geo Tags:</strong>  <span class="help-inline"><span class="label label-important">Required</span></span>
            <br /><br />
            Specify the geographic area associated with your workshop:<br /><br />
            <% 
                countrySelected = ""
                countyMessage = ""
                cityMessage = ""
                underCityMessage = ""
                if c.country != "0":
                    countrySelected = "selected"
                    states = getStateList("united-states")
                    countyMessage = "or leave blank if your workshop is specific to the entire country."
                else:
                    countrySelected = ""
                endif
            %>

            <div class="row"><span id="countrySelect">
                <div class="span2">Country:</div><!-- span2 -->
                <div class="span10"><select name="geoTagCountry" id="geoTagCountry" class="geoTagCountry">
                <option value="0">Select a country</option>
                <option ${countrySelected}>United States</option>
                </select>
                </div><!-- span10 -->
            </span>
            </div><!-- row -->
            <div class="row"><br /><span id="stateSelect">
            % if c.country != "0":
                <div class="span2">State:</div><div class="span10">
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
                </div><!-- span10 -->
            % else:
                or leave blank if your workshop is specific to the entire planet.
            % endif
            </span><br /></div><!-- row-fluid -->
            <div class="row"><br /><span id="countySelect">
            % if c.state != "0":
                <% counties = getCountyList("united-states", c.state) %>
                <% cityMessage = "or leave blank if your workshop is specific to the entire state." %>
                <div class="span2">County:</div><div class="span10">
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
                </div><!-- span10 -->
            % else:
                <% cityMessage = "" %>
                ${countyMessage}
            % endif
            </span><br /></div><!-- row -->
            <div class="row"><br /><span id="citySelect">
            % if c.county != "0":
                <% cities = getCityList("united-states", c.state, c.county) %>
                <% underCityMessage = "or leave blank if your workshop is specific to the entire county." %>
                <div class="span2">City:</div><div class="span10">
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
                </div><!-- span10 -->
            % else:
                <% underCityMessage = "" %>
                ${cityMessage}
            % endif
            </span><br /></div><!-- row -->
            <div class="row"><br /><span id="underCity">${underCityMessage}</span><br /></div><!-- row -->
            <br />
            <button type="submit" class="btn btn-warning">Save All Tags</button>

        </div><!-- span5 -->
        <div class="span5">
            <strong>Workshop Category Tags:</strong>  <span class="help-inline"><span class="label label-important">Required</span></span>
            <br />
            <% tagList = getCategoryTagList() %>
            <% tags = c.w['categoryTags'] %>
            <% workshopTags = tags.split('|') %>
           Choose at least one category:<br />
            % for tag in tagList:
                % if tag in workshopTags:
                    <% checked = 'checked' %>
                % else:
                    <% checked = 'unchecked' %>
                % endif
                <input type="checkbox" name="categoryTags" value="${tag}" ${checked} /> ${tag}<br />
            % endfor

            <br /><br />
            <strong>Additional Workshop Tags:</strong>  <span class="help-inline"><span class="label label-important">Required</span></span>
            <br />
            Enter at least one, separate multiple tags with a comma (140 char. max.):<br />
            <input type="text" name = "memberTags" size="50" maxlength="140" value = "${c.w['memberTags']}"/>
            <br /><br />
        </div><!-- span6 -->
    </div><!-- row -->
    </form>
    </div><!-- well -->

</%def>

<%def name="eligibility()">
    <%
        if c.w['startTime'] == '0000-00-00':
            wstarted = 0
        else:
            wstarted = 1

        if 'public_private' in c.w and (c.w['public_private'] == 'public' or c.w['public_private'] == 'trial'):
            publicChecked = 'checked'
            privateChecked = ''
        else:
            publicChecked = ''
            privateChecked = 'checked'
    %>

    % if c.account['type'] != 'trial' and c.w['public_private'] == 'public':
        ${public()}
    % elif c.w['public_private'] == 'private':
        ${private()}
    % elif wstarted == 0 and c.account['type'] == 'zippy':
        <strong>Workshop Type:</strong><br />
        <input type="radio" name="publicPrivate" value="public" ${publicChecked} /> Public<br />
        This means the workshop may be browsed by the public, and any members residing in the specificied geographic area may participate.<br /><br />
        <input type="radio" name="publicPrivate" value="private" ${privateChecked} /> Private<br />
        This means the workshop is not visible to the public, and any only members on the private email address or email domain list may browse and participate in the workshop.<br /><br />
        <br /><br />
    % elif wstarted == 0 and c.account['type'] == 'trial':
        <h3>Participants: Trial Workshop</h3>
        <p>Participation in trial workshops is limited to 10 Associates.<p>
    % endif
</%def>

<%def name="intro()">
    Use these forms to configure your workshop.<br />
    % if c.w['startTime'] == '0000-00-00' and c.account['type'] != 'trial' and c.basicConfig and c.slideConfig and c.backConfig and c.tagConfig:
       <br />
       <strong>Workshop Ready to Publish</strong>
        <form name="edit_issue" id="edit_issue" class="left" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configureStartWorkshopHandler" enctype="multipart/form-data" method="post" >
       <br />
       <button type="submit" class="btn btn-warning" name="startWorkshop" value="Start" >Publish Workshop</button><br />
       </form>
    % elif c.w['startTime'] == '0000-00-00':
       <br />Checklist must be completed before the workshop can be published.<br />
    % endif
</%def>

<%def name="private()">
    <h3>Participants: Private</h3>
    <p>Private workshops are not visible to the public.</p>
    <p>This establishes the list of email addresses and email domains for members eligible to browse and participate in this private workshop.<p>
    % if c.pmembers:        
        <br /><br />${len(c.pmembers)} Private Members in This Workshop<br /><br />
    % endif
    <form name="private" id="private" class="left" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configurePrivateWorkshopHandler" enctype="multipart/form-data" method="post" >
        Add new private members to this workshop:<br />
        Enter one or more email addresses, one per line:<br />
        <textarea rows=6 cols=50 name="newMember"/></textarea>
        <br /><br />
        <button type="submit" class="btn btn-warning" name="addMember">Add Member</button>
  
    % if c.pmembers:
        <br /><br />
        Delete a private member from this workshop:<br />
        Email Address: <input type="text" name = "removeMember" size="50" maxlength="140""/>
        <br /><br />
        <button type="submit" class="btn btn-warning" name="deleteMember">Delete Member</button>

    % endif
    </form>
</%def>
