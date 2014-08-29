<%!
    from pylowiki.lib.db.user import getUserByID
    from pylowiki.lib.db.flag import getFlags
%>

<%def name="res_admin_header()">
    <div class="page-header">
        <h1><a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${c.resource['urlCode']}/${c.resource['url']}/">${c.resource['title']}</a></h1>
    </div>  
</%def>

<%def name="resource_events()">   
    <p><h3><a href = "/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${c.resource['urlCode']}/${c.resource['url']}">${c.resource['title']}</a></h3></p>
    Added by member <a href="/profile/${c.author['urlCode']}/${c.author['url']}">${c.author['name']}</a> 
    <br /><br />
    Link: ${c.resource['link']}
    <br /><br />
    Text: ${c.resource['comment']}
    <p>
    <br /><br />
    <% fString = "Flags" %>
    % if int(c.resource['numFlags']) == 1:
       <% fString = "Flag" %>
    % endif
    <strong>${c.resource['numFlags']} ${fString}:</strong>
    <br /><br />
    % for flag in c.flags:
       <% user = getUserByID(flag.owner) %>
       Flagged ${flag.date}(PST) by ${user['name']}<br />
    %endfor

    <br /><br />
    % if c.events:
       <% numEvents = len(c.events) %>
       <% eString = "Events" %>
       % if numEvents == 1:
          <% eString = "Event" %>
       % endif
       <strong>${numEvents} ${eString}:</strong>
       <br /><br />
       % for event in c.events:
          <% user = getUserByID(event.owner) %>
          ${event['title']} ${event.date}(PST) by ${user['name']}<br />
          Reason: ${event['data']}
          <br /><br />
       %endfor
    % endif
</%def>

<%def name="resource_admin_options()">
    <p>
    <strong class="gray">Administrate Resource</strong>
    % if len(getFlags(c.resource)) > 0:
        <br /><br /><br />
        <strong>Clear Resource Flags</strong>
        <form name="note_resource" id="note_resource" class="left" action = "/clearResourceFlagsHandler/${c.resource['urlCode']}/${c.resource['url']}" enctype="multipart/form-data" method="post" >
            Reason for clearing flags: &nbsp;
            <input type="text" name="clearResourceFlagsReason">
            <br /><br />
            <button type="submit" class="btn btn-warning">Clear Flags</button>
            <br /><br />
        </form>
    % endif

    <br /><br /><br />
    <strong>Post Event Note on Resource</strong>
    <form name="note_resource" id="note_resource" class="left" action = "/noteResourceHandler" enctype="multipart/form-data" method="post" >
    <input type="hidden" name="workshopCode" value="${c.w['urlCode']}">
    <input type="hidden" name="workshopURL" value="${c.w['url']}">
    <input type="hidden" name="resourceCode" value="${c.resource['urlCode']}">
    <input type="hidden" name="resourceURL" value="${c.resource['url']}">
    <br />
    Note: &nbsp;
    <input type="text" name="noteResourceText"><br /><br />
    <button type="submit" class="btn btn-warning">Save Note</button>
</form>
    <br /><br /><br />
    <strong>Moderate Resource</strong>
	% if c.resource['deleted'] == '0':
		<form name="moderate_resource" id="moderate_resource" class="left" action = "/modResourceHandler" enctype="multipart/form-data" method="post" >
	    <input type="hidden" name="workshopCode" value="${c.w['urlCode']}">
	    <input type="hidden" name="workshopURL" value="${c.w['url']}">
	    <input type="hidden" name="resourceCode" value="${c.resource['urlCode']}">
	    <input type="hidden" name="resourceURL" value="${c.resource['url']}">
	    <br /><br />
	    Reason for action: &nbsp;
	    <input type="text" name="modResourceReason"><br /><br />
	    Click to verify&nbsp;<input type="radio" name="verifyModResource"> &nbsp; &nbsp;
	    % if c.resource['disabled'] == '0':
	       <button type="submit" name="modType" value="disable" class="btn btn-warning">
	       		<i class="icon-ban-circle icon-white"></i> Disable Resource
	       </button>
	       <button type="submit" name="modType" value="delete" class="btn btn-danger">
	       	   <i class="icon-trash icon-white"></i> Delete Resource
	       </button>
	    % else:
	       <button type="submit" name="modType" value="disable" class="btn btn-warning">
	           <i class="icon-ok icon-white"></i> Enable Resource
	       </button>
	       <button type="submit" name="modType" value="delete" class="btn btn-danger">
	       	   <i class="icon-trash icon-white"></i> Delete Resource
	       </button>
	    % endif
	% else:
		<br /><br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
		<code><strong>Resource Deleted</strong></code>
	% endif
</form>

</%def>
