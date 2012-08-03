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

<%def name="configure()">

% if c.w['startTime'] == '0000-00-00':
     <% wstarted = 0 %>
% else:
     <% wstarted = 1 %>
% endif
    <h1><a href = "/workshop/${c.w['urlCode']}/${c.w['url']}">${c.title}</a></h1>
    <h2 class="civ-col">Configure Workshop</h2>
<form name="edit_issue" id="edit_issue" class="left" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configureWorkshopHandler" enctype="multipart/form-data" method="post" >

    <br /><br />
    Workshop Name: <span class="darkorange">*</span>
    <br />
    <input type="text" name="title" size="50" maxlength="50" value = "${c.title}"/>
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
    Allow members to add suggestions: <input type=radio name=allowSuggestions value=1 ${yesChecked}> Yes &nbsp;&nbsp;&nbsp;<input type=radio name=allowSuggestions value=0 ${noChecked}> No<br />
    <br /><br />
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
    <br /><br />
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
       <input type="checkbox" name="publicTags" value="Environment" ${checked} /> Environment &nbsp;&nbsp;&nbsp;
       % if 'Government' in workshopTags:
           <% checked = 'checked' %>
        % else:
           <% checked = 'unchecked' %>
        % endif
       <input type="checkbox" name="publicTags" value="Government" ${checked} /> Government &nbsp;&nbsp;&nbsp;
       % if 'Municipal Services' in workshopTags:
           <% checked = 'checked' %>
        % else:
           <% checked = 'unchecked' %>
        % endif
       <input type="checkbox" name="publicTags" value="Municipal Services" ${checked} /> Municipal Services &nbsp;&nbsp;&nbsp;
       <input type="checkbox" name="publicTags" value="Economy" ${checked} /> Economy &nbsp;&nbsp;&nbsp;
       % if 'Economy' in workshopTags:
           <% checked = 'checked' %>
        % else:
           <% checked = 'unchecked' %>
        % endif
       <input type="checkbox" name="publicTags" value="Infrastructure" ${checked} /> Infrastructure &nbsp;&nbsp;&nbsp;
       % if 'Civil Rights' in workshopTags:
           <% checked = 'checked' %>
        % else:
           <% checked = 'unchecked' %>
        % endif
       <input type="checkbox" name="publicTags" value="Civil Rights" ${checked} /> Civil Rights &nbsp;&nbsp;&nbsp;
       <input type="checkbox" name="publicTags" value="Civic Response" ${checked} /> Civic Response &nbsp;&nbsp;&nbsp;
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
       Enter at least one, separate multiple tags with a comma:<br />
       <input type="text" name = "memberTags" size="50" maxlength="50" value = "${c.w['memberTags']}"/>
       <br /><br />
    % if wstarted == 0:
    <br /><br />
    <strong>Workshop Eligiblity</strong>
    <p>This establishes the geographic jurisdiction, or public sphere, in which people need to reside to participate in this workshop.</p>
    <p>The public sphere can be expressed either as a jurisdiction with a single "home" postal code in the middle, or as a set of different postal codes.</p>
    Who is eligible to participate in the workshop:
    <table class="table table-striped table-bordered">
    <tbody>
    <tr>
    <td>
    <% titles = getGeoTitles(c.w['publicPostal'], 'united-states') %>
    <% sList = titles.split('|') %>
    Workshop Home Postal Code: <input type="text" id="publicPostal" name="publicPostal" value="${c.w['publicPostal']}"> <button class="btn btn-primary btn-mini geoButton">Set New Postal Code</button>
    <br />
    <span id="werror"></span>
    <br /><br />
    People in:<br/>
    % if c.w['publicScope'] == '10':
        <% checked = 'checked' %>
    % else:
        <% checked = 'unchecked' %>
    % endif
    <input type="radio" name = "publicScope" value = "10" ${checked} onClick="clearZipList()" /> <span id="wpostal">${sList[9]}</span><br>
     % if c.w['publicScope'] == '09':
         <% checked = 'checked' %>
     % else:
         <% checked = 'unchecked' %>
     % endif
     <input type="radio" name = "publicScope" value = "09" ${checked} onClick="clearZipList()" /> <span id="wcity">${sList[8]}</span><br> 
     % if c.w['publicScope'] == '07':
         <% checked = 'checked' %>
     % else:
         <% checked = 'unchecked' %>
     % endif
     <input type="radio" name = "publicScope" value = "07" ${checked} onClick="clearZipList()" /> <span id="wcounty">${sList[6]}</span><br>
     % if c.w['publicScope'] == '05':
         <% checked = 'checked' %>
     % else:
         <% checked = 'unchecked' %>
     % endif
     <input type="radio" name = "publicScope" value = "05" ${checked} onClick="clearZipList()" /> <span id="wstate">${sList[4]}</span><br>
     % if c.w['publicScope'] == '03':
         <% checked = 'checked' %>
     % else:
         <% checked = 'unchecked' %>
     % endif
     <input type="radio" name = "publicScope" value = "03" ${checked} onClick="clearZipList()" /> <span id="wcountry">${sList[2]}</span><br>
     % if c.w['publicScope'] == '01':
         <% checked = 'checked' %>
     % else:
         <% checked = 'unchecked' %>
     % endif
     <input type="radio" name = "publicScope" value = "01" ${checked} onClick="clearZipList()" /> The Planet<br>
       </td>
       <td>
       People in these postal codes (enter at least one): <span class="darkorange">*</span>
       <br />
       <textarea name = "publicPostalList" onClick="clearEligibleCheckboxes(document.edit_issue.publicScope)" rows="2" cols="50">${c.w['publicPostalList']}</textarea>
       </td>
       </tr>
       </tbody>
       </table>
    
       <br /><br />
       When you have completed all the information above, and are <strong>sure</strong> it is correct and complete, check the two boxes below to start your workshop. 
   Once a workshop has started, it is available for visiting and reading by the public, and contributions by members who are logged in and eligible to participate. 
       <br />
       <br />
   Note that once a workshop has started, you may not change the workshop participant eligibility or tags. 
       <br />
       <input type="checkbox" name="startWorkshop" value="Start" /> Start Workshop &nbsp; &nbsp; &nbsp; <input type="checkbox" name="startWorkshop" value="VerifyStart" /> Verify Start Workshop
       <br />
       <br />
       <br />
       <br />
   % else:
     Members eligible to participate in this workshop: residents of ${c.w['publicScopeTitle']}
     <br />
     Workshop Tags: ${c.w['publicTags']} ${c.w['memberTags']}
     <br />
     <br />

   % endif
    <button type="submit" class="btn btn-warning">Save Changes</button>
</form>

</%def>
