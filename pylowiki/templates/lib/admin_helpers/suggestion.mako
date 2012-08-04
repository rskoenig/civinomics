<%inherit file = "/base/template.html"/>
<%!
    from pylowiki.lib.db.user import getUserByID
%>

<%def name="sug_admin_banner()">
    <div class="page-header">
    	<h1><a href = "/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${c.s['urlCode']}/${c.s['url']}">${c.title}</a></h1>
    </div>   

</%def>

<%def name="suggestion_events_flags()">

    Added by member <a href="/profile/${c.author['urlCode']}/${c.author['url']}">${c.author['name']}</a> 
    <br /><br />
    Last modified date: ${c.lastmoddate}
    <br /><br />
    ${c.content}
    <br /><br />

    <% numFlags = len(c.flags) %>
    <% fString = "Flags" %>
    % if numFlags == 1:
       <% fString = "Flag" %>
    % endif
    <strong>${numFlags} ${fString}:</strong>
    <br /><br />
    % for flag in c.flags:
       <% user = getUserByID(flag.owner) %>
       Flagged ${flag.date} by ${user['name']}<br />
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
          ${event['title']} ${event.date} by ${user['name']}<br />
          Reason: ${event['data']}
          <br /><br />
       %endfor
    % endif
</%def>


<%def name="suggestion_admin()">  
    <p>
    <strong class="gray">Administrate Suggestion</strong>
    <br /><br /><br />
    <strong>Leave Note on Suggetion</strong>
    <form name="note_suggestion" id="note_suggestion" class="left" action = "/noteSuggestionHandler" enctype="multipart/form-data" method="post" >
    <input type=hidden name=workshopCode value="${c.w['urlCode']}">
    <input type=hidden name=workshopURL value="${c.w['url']}">
    <input type=hidden name=suggestionCode value="${c.s['urlCode']}">
    <input type=hidden name=suggestionURL value="${c.s['url']}">
    <br />
    Note text: &nbsp;
    <input type=text name=noteSuggestionText><br /><br />
    <button type="submit" class="btn btn-warning">Save Note</button>
    </form>
    <br /><br />
    % if 'adopted' not in c.s or c.s['adopted'] == '0':
       <% adoptTitle = "Adopt Suggestion" %>
    % else:
       <% adoptTitle = "Unadopt Suggestion" %>
    % endif
    <form name="adopt_suggestion" id="adopt_suggestion" class="left" action = "/adoptSuggestionHandler" enctype="multipart/form-data" method="post" >
    <strong>${adoptTitle}</strong>
    <input type=hidden name=workshopCode value="${c.w['urlCode']}">
    <input type=hidden name=workshopURL value="${c.w['url']}">
    <input type=hidden name=suggestionCode value="${c.s['urlCode']}">
    <input type=hidden name=suggestionURL value="${c.s['url']}">
    <br /><br />
    Reason for action: &nbsp;
    <input type=text name=adoptSuggestionReason><br /><br />
    <button type="submit" class="btn btn-warning">${adoptTitle}</button>
    </form>
	% if c.s['deleted'] == '0':
	    <br /><br />
	    <p>
	    <strong>Moderate Suggestion</strong>
	    <form name="moderate_suggestion" id="moderate_suggestion" class="left" action = "/modSuggestionHandler" enctype="multipart/form-data" method="post" >
	    <input type=hidden name=workshopCode value="${c.w['urlCode']}">
	    <input type=hidden name=workshopURL value="${c.w['url']}">
	    <input type=hidden name=suggestionCode value="${c.s['urlCode']}">
	    <input type=hidden name=suggestionURL value="${c.s['url']}">
	    <br />
	    Reason for action: &nbsp;
	    <input type=text name=modSuggestionReason><br /><br />
	    Click to verify&nbsp;<input type=radio name=verifyModSuggestion> &nbsp; &nbsp;
	    % if c.s['disabled'] == '0':
	       <button type="submit" name=modType value="disable" class="btn btn-warning">
	       		<i class="icon-ban-circle icon-white"></i> Disable Suggestion
	       </button>
	       <button type="submit" name=modType value="delete" class="btn btn-danger">
	       	   <i class="icon-trash icon-white"></i> Delete Suggestion
	       </button>
	    % else:
	       <button type="submit" name=modType value="disable" class="btn btn-warning">
	           <i class="icon-ok icon-white"></i> Enable Suggestion
	       </button>
	       <button type="submit" name=modType value="delete" class="btn btn-danger">
	       	   <i class="icon-trash icon-white"></i> Delete Suggestion
	       </button>
	    % endif
	    </form>
	% else:
		<br /><br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
		<code><strong>Suggestion Deleted</strong></code>
	% endif	    
            
</%def>
