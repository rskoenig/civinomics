<%!
    from pylowiki.lib.db.geoInfo import getGeoTitles, getWScopesByWorkshopID
    from pylowiki.lib.db.user import getUserByEmail
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
    % if c.w['startTime'] == '0000-00-00' and c.account['type'] != 'trial' and c.basicConfig and c.slideConfig and c.backConfig and c.scopeConfig:
       <br />
       <strong>Your Workshop is Ready to Publish</strong>
        <form name="edit_issue" id="edit_issue" class="left" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configureStartWorkshopHandler" enctype="multipart/form-data" method="post" >
       <br />
       <button type="submit" class="btn btn-warning" name="startWorkshop" value="Start" >Publish Workshop</button> &nbsp; &nbsp; &nbsp; <input type="checkbox" name="startWorkshop" value="VerifyStart" /> Verify Publish Workshop
       </form>
    % endif

    <form name="edit_issue" id="edit_issue" class="left" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configureBasicWorkshopHandler" enctype="multipart/form-data" method="post" >
    <table class="table">
    <tbody>
    <tr>
    <td>
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
        <br /><br />
    % else:
        <strong>Workshop Type:</strong><br />
        ${c.w['public_private']}
        <br /><br />
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
    </td>
    <td>
    % if c.account['type'] != 'trial' and c.w['public_private'] == 'public':

        % if wstarted == 0: 
            <strong>Workshop Tags:</strong>  <span class="help-inline"><span class="label label-important">Required</span></span>
            <br />
            <% tags = c.w['publicTags'] %>
            <% workshopTags = tags.split(',') %>
            Choose at least one from the list below<br /> 
            <%
                if 'Environment' in workshopTags:
                    checked = 'checked'
                else:
                    checked = 'unchecked'
            %>
            <input type="checkbox" name="publicTags" value="Environment" ${checked} /> Environment<br />
            <%
                if 'Government' in workshopTags:
                    checked = 'checked'
                else:
                    checked = 'unchecked'
            %>
            <input type="checkbox" name="publicTags" value="Government" ${checked} /> Government <br />
            <%
                if 'Municipal Services' in workshopTags:
                    checked = 'checked'
                else:
                    checked = 'unchecked'
            %>
            <input type="checkbox" name="publicTags" value="Municipal Services" ${checked} /> Municipal Services<br />
            <%
                if 'Economy' in workshopTags:
                    checked = 'checked'
                else:
                    checked = 'unchecked'
            %>
            <input type="checkbox" name="publicTags" value="Economy" ${checked} /> Economy <br />

            <%
                if 'Infrastructure' in workshopTags:
                    checked = 'checked'
                else:
                    checked = 'unchecked'
            %>
            <input type="checkbox" name="publicTags" value="Infrastructure" ${checked} /> Infrastructure <br />

            <%
                if 'Civil Rights' in workshopTags:
                    checked = 'checked'
                else:
                    checked = 'unchecked'
            %>
            <input type="checkbox" name="publicTags" value="Civil Rights" ${checked} /> Civil Rights<br /> 

            <%
                if 'Civic Response' in workshopTags:
                    checked = 'checked'
                else:
                    checked = 'unchecked'
            %>
            <input type="checkbox" name="publicTags" value="Civic Response" ${checked} /> Civic Response<br /> 

            <%
                if 'Business' in workshopTags:
                    checked = 'checked'
                else:
                    checked = 'unchecked'
            %>
            <input type="checkbox" name="publicTags" value="Business" ${checked} /> Business
            <br />
            <br />
            <strong>Additional Workshop Tags:</strong>  <span class="help-inline"><span class="label label-important">Required</span></span>
            <br />
            Enter at least one, separate multiple tags with a comma (140 char. max.):<br />
            <input type="text" name = "memberTags" size="50" maxlength="140" value = "${c.w['memberTags']}"/>
            <br /><br />
        % else:
            <p><strong>Tags</strong>: ${c.w['publicTags']}, ${c.w['memberTags']}</p>
            <p><strong>Public Sphere</strong>: ${c.w['publicScopeTitle']}</p>
        % endif

    % endif
    <br />
    </td>
    
    </tr>
    </tbody>
    </table>
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
    % elif wstarted == 0 and c.account['type'] == 'trial':
        <strong>Workshop Type:</strong><br />
        <input type="radio" name="publicPrivate" value="public" ${publicChecked} /> Public<br />
        This means the workshop may be browsed by the public, and any members residing in the specificied geographic area may participate.<br /><br />
        <input type="radio" name="publicPrivate" value="private" ${privateChecked} /> Private<br />
        This means the workshop is not visible to the public, and any only members on the private email address or email domain list may browse and participate in the workshop.<br /><br />
        <br /><br />
    % endif
</%def>

<%def name="intro()">
    Use these tools to configure your workshop before publishing.<br />
    % if c.w['startTime'] == '0000-00-00':
       <br />Complete the checklist below.<br />
       Required information marked with * <br />
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

<%def name="public()">
    <h3>Participants: Public</h3>
    <% 
        if c.w['scopeMethod'] == 'publicScope':
            sActive = "active"
            mActive = "inactive"
        else:
            sActive = "inactive"
            mActive = "active"
    %>
    % if c.w['startTime'] == '0000-00-00':
    <p>This establishes the geographic area, or <em>public sphere</em>, in which people need to reside to participate in this workshop.</p>
    <p>The public sphere for this workshop can be defined either as a single jurisdiction with a central "home" postal, or as a set of multiple postal codes.</p>
    Choose which method of public sphere to use for this workshop, Single Jurisdiction or Multiple Postal Codes, then fill out the information in the appropriate form below and save it.

        <div class="tabbable">
        <ul class="nav nav-tabs">
        <li class="${sActive}">
            <a href="#tab11" data-toggle="tab">Single Jurisdiction</a>
        </li>
        <li class="${mActive}">
            <a href="#tab12" data-toggle="tab">Multiple Postal Codes</a>
        </li>
        </ul>
        <div class="tab-content">
            <div class="tab-pane ${sActive} well" id="tab11">
                <form name="edit_issue" id="edit_issue" class="left" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configureSingleWorkshopHandler" enctype="multipart/form-data" method="post" >
                <% titles = getGeoTitles(c.w['publicPostal'], 'united-states') %>
                <% sList = titles.split('|') %>
                <br /> <br />
                Enter New Home Postal Code: <input type="text" id="publicPostal" name="publicPostal" value="${c.w['publicPostal']}" style="width:60px;"> <button class="btn btn-primary btn-mini geoButton">Check New Postal Code</button>
                <br />
                <span id="werror"></span>
                <br />
                Public Sphere: (choose one)<br><br>
                <% 
                    if c.w['publicScope'] == '10':
                        checked = 'checked'
                    else:
                        checked = 'unchecked'
                %>
                <input type="radio" name = "publicScope" value = "10" ${checked} onClick="clearZipList()" /> Postal Code <span id="wpostal">${sList[9]}</span><br>
                <%
                    if c.w['publicScope'] == '09':
                       checked = 'checked'
                    else:
                       checked = 'unchecked'
                %>
                <input type="radio" name = "publicScope" value = "09" ${checked} onClick="clearZipList()" /> City of <span id="wcity">${sList[8]}</span><br> 
                <% 
                    if c.w['publicScope'] == '07':
                       checked = 'checked'
                    else:
                       checked = 'unchecked'
                %>
                <input type="radio" name = "publicScope" value = "07" ${checked} onClick="clearZipList()" /> County of <span id="wcounty">${sList[6]}</span><br>
                <%
                    if c.w['publicScope'] == '05':
                       checked = 'checked'
                    else:
                       checked = 'unchecked'
                %>
                <input type="radio" name = "publicScope" value = "05" ${checked} onClick="clearZipList()" /> State of <span id="wstate">${sList[4]}</span><br>
                <%
                    if c.w['publicScope'] == '03':
                       checked = 'checked'
                    else:
                       checked = 'unchecked'
                %>
                 <input type="radio" name = "publicScope" value = "03" ${checked} onClick="clearZipList()" /> Country of <span id="wcountry">${sList[2]}</span><br>
                <%
                    if c.w['publicScope'] == '01':
                       checked = 'checked'
                    else:
                       checked = 'unchecked'
                %>
                <input type="radio" name = "publicScope" value = "01" ${checked} onClick="clearZipList()" /> The Planet<br>
                <br />
                <button type="submit" class="btn btn-warning">Save Single Jurisdiction</button>
                </form>
            </div><!-- tab-pane tab11 configure -->
            <div class="tab-pane well ${mActive}" id="tab12">
                <form name="edit_issue" id="edit_issue" class="left" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configureMultipleWorkshopHandler" enctype="multipart/form-data" method="post" >
                <br /><br />
                Enter at least one postal code. Separate multiple postal codes with a comma.<br>
                <textarea name = "publicPostalList" onClick="clearEligibleCheckboxes(document.edit_issue.publicScope)" rows="4" cols="60">${c.w['publicPostalList']}</textarea><br /><br />
                <button type="submit" class="btn btn-warning">Save Multiple Postal Codes</button>
                </form>
            </div><!-- tab-pane tab12 configure -->
        </div><!-- tab-content configure -->
        </div><!-- tabbable configure -->
    % else:
        This workshop is visible to the public.<br /> 
        Civinomics members residing within the public sphere of the <strong>${c.w['publicScopeTitle']}</strong> may participate in this workshop.<br />
        
    % endif
</%def>

<%def name="associates()">
    <%
        associates = []
        emails = []
        all = []
        if 'associates' in c.w:
            aList = c.w['associates'].split('|')
            for a in aList:
                if a and a != '':
                    all.append(a)
                    user = getUserByEmail(a)
                    if user:
                        associates.append(user)
                    else:
                        emails.append(a)
    %>
    <div class="well">
    <h3>Associates</h3>
    <form name="associates" id="associates" class="form-inline" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configureAssociatesWorkshopHandler" enctype="multipart/form-data" method="post" >
    You can designate up to 10 private associates to participate in this workhop</strong><br /><br />
    % if len(all) < 10:
        <br /><br />
        <strong>Add a new associate:</strong><br /><br />
        Email Address: <input type="text" name = "newAssociate" size="50" maxlength="140""/> &nbsp; &nbsp;
        <button type="submit" class="btn btn-warning" name="addAssociate">Add Associate</button>
    % endif
    % if len(associates) > 0 or len(emails) > 0:
        <ul class="unstyled">
        % for user in associates:
            <li>        
            <a href="/profile/${user['urlCode']}/${user['url']}">${user['name']}</a> &nbsp; &nbsp; <button type="submit" class="btn btn-danger" name="deleteAssociate" value="${user['email']}">Delete Associate</button> <input type=checkbox name="confirmDelete|${user['email']}"> confirm
            </li>
        % endfor
        % for email in emails:
            <li>
            <button type="submit" class="btn btn-danger" name="deleteAssociate" value="${email}">Delete Associate</button> <input type=checkbox name="confirmDelete|${email}"> confirm &nbsp; &nbsp; &nbsp;
            ${email} </li>
        % endfor
        </ul>
    % endif
    </form>
    </div><!-- well -->
</%def>
