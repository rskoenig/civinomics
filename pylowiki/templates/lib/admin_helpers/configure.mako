<%!
    from pylowiki.lib.db.geoInfo import getGeoTitles
%>

<%def name="fields_alert()">
	% if 'alert' in session:
		<% alert = session['alert'] %> 
        <div class="alert alert-${alert['type']}">
            <button data-dismiss="alert" class="close">×</button>
            <strong>${alert['title']}</strong>
            ##${alert['content']}
        </div>
        <% 
           session.pop('alert')
           session.save()
        %>
	% endif
</%def>


<%def name="edit_background()">
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

<%def name="configure()">

    % if c.w['startTime'] == '0000-00-00':
         <% wstarted = 0 %>
    % else:
         <% wstarted = 1 %>
    % endif
    ${fields_alert()}
<form name="edit_issue" id="edit_issue" class="left" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configureBasicWorkshopHandler" enctype="multipart/form-data" method="post" >
    <table class="table well">
    <tbody>
    <tr>
    <td>
    Workshop Name: <span class="darkorange">*</span>
    <br />
    <input type="text" name="title" size="50" maxlength="70" value = "${c.w['title']}"/>
    <br />
    <br />
    Workshop Goals: <span class="darkorange">*</span>
    <br />
    <textarea name="goals" rows="5" cols="50">${c.w['goals']}</textarea>
    <br /><br />
    % if 'allowSuggestions' in c.w and c.w['allowSuggestions'] == '1':
        <% yesChecked = 'checked' %>
        <% noChecked = '' %>
    % elif 'allowSuggestions' in c.w and c.w['allowSuggestions'] == '0':
        <% yesChecked = '' %>
        <% noChecked = 'checked' %>
    % else:
        <% yesChecked = 'checked' %>
        <% noChecked = '' %>
    % endif
    Allow members to add suggestions: <input type=radio name=allowSuggestions value=1 ${yesChecked}> Yes &nbsp;&nbsp;&nbsp;<input type=radio name=allowSuggestions value=0 ${noChecked}> No<br /><br />
    % if 'allowResources' in c.w and c.w['allowResources'] == '1':
        <% yesChecked = 'checked' %>
        <% noChecked = '' %>
    % elif 'allowResources' in c.w and c.w['allowResources'] == '0':
        <% yesChecked = '' %>
        <% noChecked = 'checked' %>
    % else:
        <% yesChecked = 'checked' %>
        <% noChecked = '' %>
    % endif
    Allow members to add resource links: <input type=radio name=allowResources value=1 ${yesChecked}> Yes &nbsp;&nbsp;&nbsp;<input type=radio name=allowResources value=0 ${noChecked}> No<br />
    <br />
    <button type="submit" class="btn btn-warning">Save Basic Information</button>
    </td>
    <td>
    % if wstarted == 0: 
       Workshop Tags: <span class="darkorange">*</span>
       <br />
       <% tags = c.w['publicTags'] %>
       <% workshopTags = tags.split(',') %>
       Choose at least one from the list below<br /> 
       % if 'Environment' in workshopTags:
           <% checked = 'checked' %>
        % else:
           <% checked = 'unchecked' %>
        % endif
       <input type="checkbox" name="publicTags" value="Environment" ${checked} /> Environment<br />
       % if 'Government' in workshopTags:
           <% checked = 'checked' %>
        % else:
           <% checked = 'unchecked' %>
        % endif
       <input type="checkbox" name="publicTags" value="Government" ${checked} /> Government <br />
       % if 'Municipal Services' in workshopTags:
           <% checked = 'checked' %>
        % else:
           <% checked = 'unchecked' %>
        % endif
       <input type="checkbox" name="publicTags" value="Municipal Services" ${checked} /> Municipal Services<br />

       % if 'Economy' in workshopTags:
           <% checked = 'checked' %>
        % else:
           <% checked = 'unchecked' %>
        % endif
       <input type="checkbox" name="publicTags" value="Economy" ${checked} /> Economy <br />

       % if 'Infrastructure' in workshopTags:
           <% checked = 'checked' %>
        % else:
           <% checked = 'unchecked' %>
        % endif
       <input type="checkbox" name="publicTags" value="Infrastructure" ${checked} /> Infrastructure <br />

       % if 'Civil Rights' in workshopTags:
           <% checked = 'checked' %>
        % else:
           <% checked = 'unchecked' %>
        % endif
       <input type="checkbox" name="publicTags" value="Civil Rights" ${checked} /> Civil Rights<br /> 

       % if 'Civic Response' in workshopTags:
           <% checked = 'checked' %>
        % else:
           <% checked = 'unchecked' %>
        % endif
       <input type="checkbox" name="publicTags" value="Civic Response" ${checked} /> Civic Response<br /> 

       % if 'Business' in workshopTags:
           <% checked = 'checked' %>
        % else:
           <% checked = 'unchecked' %>
        % endif
       <input type="checkbox" name="publicTags" value="Business" ${checked} /> Business
       <br />
       <br />
       Additional Workshop Tags: <span class="darkorange">*</span>
       <br />
       Enter at least one, separate multiple tags with a comma (140 char. max.):<br />
       <input type="text" name = "memberTags" size="50" maxlength="140" value = "${c.w['memberTags']}"/>
       <br /><br />
    % else:
      <p><strong>Tags</strong>: ${c.w['publicTags']}, ${c.w['memberTags']}</p>
      <p><strong>Public Sphere</strong>: ${c.w['publicScopeTitle']}</p>
    % endif
    <br />
    </td>
    </tr>
    </tbody>
    </table>
    </form>
    <br /><br />

    % if wstarted == 0:
    <strong>Workshop Eligiblity</strong>
    <p>This establishes the geographic area, or <em>public sphere</em>, in which people need to reside to participate in this workshop.</p>
    <p>The public sphere for this workshop can be defined either as a single jurisdiction with a central "home" postal, or as a set of multiple postal codes.</p>
    Choose which method of public sphere to use for this workshop, Single Jurisdiction or Multiple Postal Codes, then fill out the information in the appropriate form below and save it.
    % if c.w['scopeMethod'] == 'publicScope':
        <% sActive = "active" %>
        <% mActive = "inactive" %>
    % else:
        <% sActive = "inactive" %>
        <% mActive = "active" %>
    % endif
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
                % if c.w['publicScope'] == '10':
                    <% checked = 'checked' %>
                % else:
                    <% checked = 'unchecked' %>
                % endif
                <input type="radio" name = "publicScope" value = "10" ${checked} onClick="clearZipList()" /> Postal Code <span id="wpostal">${sList[9]}</span><br>
                 % if c.w['publicScope'] == '09':
                     <% checked = 'checked' %>
                 % else:
                     <% checked = 'unchecked' %>
                 % endif
                 <input type="radio" name = "publicScope" value = "09" ${checked} onClick="clearZipList()" /> City of <span id="wcity">${sList[8]}</span><br> 
                 % if c.w['publicScope'] == '07':
                     <% checked = 'checked' %>
                 % else:
                     <% checked = 'unchecked' %>
                 % endif
                 <input type="radio" name = "publicScope" value = "07" ${checked} onClick="clearZipList()" /> County of <span id="wcounty">${sList[6]}</span><br>
                 % if c.w['publicScope'] == '05':
                     <% checked = 'checked' %>
                 % else:
                     <% checked = 'unchecked' %>
                 % endif
                 <input type="radio" name = "publicScope" value = "05" ${checked} onClick="clearZipList()" /> State of <span id="wstate">${sList[4]}</span><br>
                 % if c.w['publicScope'] == '03':
                     <% checked = 'checked' %>
                 % else:
                     <% checked = 'unchecked' %>
                 % endif
                 <input type="radio" name = "publicScope" value = "03" ${checked} onClick="clearZipList()" /> Country of <span id="wcountry">${sList[2]}</span><br>
                 % if c.w['publicScope'] == '01':
                     <% checked = 'checked' %>
                 % else:
                     <% checked = 'unchecked' %>
                 % endif
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
    
       <br /><br />
       When you have completed all the information above, and are <strong>sure</strong> it is correct and complete, check the two boxes below to start your workshop. 
   Once a workshop has started, it is available for visiting and reading by the public, and contributions by members who are logged in and eligible to participate. 
       <br /><br />
   Note that once a workshop has started, you may not change the workshop participant eligibility or tags. 
       <div class="well">
        <form name="edit_issue" id="edit_issue" class="left" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configureStartWorkshopHandler" enctype="multipart/form-data" method="post" >
       <br />
       <input type="checkbox" name="startWorkshop" value="Start" /> Start Workshop &nbsp; &nbsp; &nbsp; <input type="checkbox" name="startWorkshop" value="VerifyStart" /> Verify Start Workshop
       <br /><br />
       <button type="submit" class="btn btn-warning">Start Workshop</button>
       </form>
       </div>
   % endif

</%def>
