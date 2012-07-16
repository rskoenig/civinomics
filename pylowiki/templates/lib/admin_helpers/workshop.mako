<%!
    from pylowiki.lib.db.flag import checkFlagged
    from pylowiki.lib.db.event import getParentEvents
    from pylowiki.lib.db.user import getUserByID
    from pylowiki.lib.db.comment import getPureFlaggedDiscussionComments, getComment, getDisabledComments, getDeletedComments
%>  

<%def name="banner_name()">
    <br /><br />
    <br /><br />
    <div class="page-header"><h1><a href = "/workshop/${c.w['urlCode']}/${c.w['url']}">${c.title}</a></h1>
    </div>
</%def>

<%def name="admin_show()">
	<div class=left>
	<form name="admin_issue" id="admin_issue" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/adminWorkshopHandler" enctype="multipart/form-data" method="post" >
    <strong class="gray">Administrate Workshop</strong>
    <br /><br />
    Message to Participants:
    <br />
    <textarea name="motd" rows="5" cols="50">${c.motd['data']}</textarea>
    <br /><br />
    % if c.motd['enabled'] == '1':
       <% pChecked = 'checked' %>
       <% uChecked = '' %>
    % else:
       <% pChecked = '' %>
       <% uChecked = 'checked' %>
    % endif
    <input type=radio name="enableMOTD" value="1" ${pChecked}> Publish&nbsp;&nbsp;&nbsp;<input type=radio name="enableMOTD" value="0" ${uChecked}> Unpublish
    <br /><br />
    <br /><br />
    % if c.w['deleted'] == '1':
       <strong>Enable Workshop</strong>
       <% eAction = 'Enable' %>
    % else:
       <strong>Disable Workshop</strong>
       <% eAction = 'Disable' %>
    % endif
    <br />
    Reason: <input type=text name=eventReason id=eventReason>
    <br />
    <input type=radio name="enableWorkshop" value="1"> ${eAction}&nbsp;&nbsp;&nbsp;<input type=radio name="verifyEnableWorkshop" value="0"> Verify ${eAction}
    <br /><br />
    <br /><br />
    <button type="submit" class="btn btn-warning">Save Changes</button>
    </form>
</%def>

<%def name="admin_info()">
    <% wEvents = getParentEvents(c.w) %>
    % if wEvents:
        <br /><br />
        <strong>Workshop Events</strong>
        <br /><br />
        % for wE in wEvents:
            &nbsp; &nbsp; &nbsp; <strong>${wE.date} ${wE['title']}</strong>  ${wE['data']}<br />
        % endfor
    % endif
    <br /><br />
    <br /><br />
    <strong class="gray">Facilitators</strong>
    <br /><br />
    % for f in c.f:
       <% fUser = getUserByID(f.owner) %>
       <% fEvents = getParentEvents(f) %>
       <% fPending = "" %>
       % if pending in f and f['pending'] == '1':
          <% fPending = "(Pending)" %>
       % endif
       <a href="/profile/${fUser['urlCode']}/${fUser['url']}">${fUser['name']}</a> ${fPending}<br />
       % if fEvents:
          % for fE in fEvents:
          &nbsp; &nbsp; &nbsp; <strong>${fE.date} ${fE['title']}</strong>  ${fE['data']}<br />
          % endfor
       % endif
       % if c.authuser.id == f.owner and c.authuser.id != c.w.owner:
           <form id="resignFacilitator" name="resignFacilitator" action="/workshop/${c.w['urlCode']}/${c.w['url']}/resignFacilitator" method="post">
               &nbsp; &nbsp; &nbsp;Note: <input type=text name=resignReason> &nbsp;&nbsp;&nbsp;
               <button type="submit" class="gold" value="Resign">Resign</button>
           <br />
           </form>
       % endif
    % endfor
    % for f in c.df:
       <% fUser = getUserByID(f.owner) %>
       <% fEvents = getParentEvents(f) %>
       <a href="/profile/${fUser['urlCode']}/${fUser['url']}">${fUser['name']}</a> (Disabled)<br />
       % if fEvents:
          % for fE in fEvents:
          &nbsp; &nbsp; &nbsp; <strong>${fE.date} ${fE['title']}</strong>  ${fE['data']}<br />
          % endfor
       % endif
    % endfor
    <br /><br />
</%def>

<%def name="flagged()">
	<br />
    <strong>Flagged Objects</strong>
    <br /><br />
    <strong>Resources and Comments:</strong>
    <br />
    % if c.r:
       % for r in c.r:
          % if checkFlagged(r) and r['disabled'] == '0' and r['deleted'] == '0': 
			  ${r['numFlags']}
	          % if int(r['numFlags']) > 1:
	          	 Flags:
	          % else:
	             Flag:
	          % endif
             Resource: <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}">${r['title']}</a>
             <a class="btn btn-mini" href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}/modResource/"> Admin Resource </a><br />
          % endif
          <% cList = getPureFlaggedDiscussionComments(r['discussion_id']) %>
          % if cList:
             <% cFlagCount = len(cList) %>
             % if cFlagCount > 1:
                <% cString = 'Comments' %> 
             % else:
                <% cString = 'Comment' %> 
             % endif
             ${cString} In Resource <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}">${r["title"]}</a></br>
		 	 % for comID in cList:
			      <% com = getComment(comID) %>
			      &nbsp&nbsp&nbsp&nbsp&nbsp
			      % if int(com['numFlags']) is 1:
				      ${com['numFlags']} flag:
				  % else:
				      ${com['numFlags']} flags:
				  % endif
			      % if len(com['data']) > 20:
					  <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}/modComment/${comID}">${com['data'][:20]}...</a>
				  % else:
					  <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}/modComment/${comID}">${com['data']}</a>
			      % endif
	             <br />
          	 % endfor
          % endif
       % endfor
    % endif
    <br /><br />
    <strong>Suggestions and Comments:</strong>
    <br />
    % for s in c.s:
       % if checkFlagged(s) and s['disabled'] == '0' and s['deleted'] == '0': 
		  ${s['numFlags']}
          % if int(s['numFlags']) > 1:
          	 Flags:
          % else:
             Flag:
          % endif
          Suggestion <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${s['urlCode']}/${s['url']}">${s["title"]}</a>
          <a class="btn btn-mini" href="/modSuggestion/${s['urlCode']}/${s['url']}/">Admin Suggestion </a><br />
       % endif
       <% cList = getPureFlaggedDiscussionComments(s['discussion_id']) %>
       % if cList:
          <% cFlagCount = len(cList) %>
          % if cFlagCount > 1:
             <% cString = 'Comments' %> 
          % else:
             <% cString = 'Comment' %> 
          % endif
          ${cString} In Suggestion <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${s['urlCode']}/${s['url']}">${s["title"]}</a></br>
		  % for comID in cList:
		      <% com = getComment(comID) %>
		      &nbsp&nbsp&nbsp&nbsp&nbsp
		      % if int(com['numFlags']) is 1:
			      ${com['numFlags']} Flag:
			  % else:
			      ${com['numFlags']} Flags:
			  % endif
		      % if len(com['data']) > 20:
				  <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${s['urlCode']}/${s['url']}/modComment/${comID}">${com['data'][:20]}...</a>
			  % else:
				  <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${s['urlCode']}/${s['url']}/modComment/${comID}">${com['data']}</a>
		      % endif
             <br />
          % endfor
       % endif
    % endfor
</%def>

<%def name="disabled()">
    <br /><br />
    <strong class="gray">Disabled Objects</strong>
    <br /><br />
    <strong>Resources and Comments:</strong>
    <br />
    % if c.disabledRes:
       % for r in c.disabledRes:
	      % if checkFlagged(r): 
			  ${r['numFlags']}
	          % if int(r['numFlags']) > 1:
	          	 Flags:
	          % else:
	             Flag:
	          % endif
          % endif
         Resource: <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}">${r['title']}</a>
         <a class="btn btn-mini" href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}/modResource/"> Admin Resource </a><br />
       % endfor
    % endif
	% for r in c.r:
    	<% disabledComments = getDisabledComments(r['discussion_id']) %>
    	% if disabledComments:
          <% cFlagCount = len(disabledComments) %>
          % if cFlagCount > 1:
             <% cString = 'Comments' %> 
          % else:
             <% cString = 'Comment' %> 
          % endif
          ${cString} In Resource <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}">${r["title"]}</a></br>    	    
	    	% for comID in disabledComments:
	    	  <% com = getComment(comID) %>
		      &nbsp&nbsp&nbsp&nbsp&nbsp
	    	  % if checkFlagged(com):
			      % if int(com['numFlags']) is 1:
				      ${com['numFlags']} flag:
				  % else:
				      ${com['numFlags']} flags:
				  % endif
			  % else:
			  	  0 flags:
			  % endif
		      % if len(com['data']) > 20:
				  <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}/modComment/${comID}">${com['data'][:20]}...</a>
			  % else:
				  <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}/modComment/${comID}">${com['data']}</a>
		      % endif
	          </br>
			% endfor
		% endif
	% endfor
    <br /><br />
    <strong>Suggestions and Comments:</strong>
    <br />
    % if c.disabledSug:
       % for s in c.disabledSug:
	      % if checkFlagged(s): 
			  ${s['numFlags']}
	          % if int(s['numFlags']) > 1:
	          	 Flags:
	          % else:
	             Flag:
	          % endif
          % endif
         Suggestion: <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${s['urlCode']}/${s['url']}">${s["title"]}</a>
         <a class="btn btn-mini" href="/modSuggestion/${s['urlCode']}/${s['url']}/">Admin Suggestion </a><br />
       % endfor
    % endif
    % for s in c.s:
    	<% disabledComments = getDisabledComments(s['discussion_id']) %>
    	% if disabledComments:
          <% cFlagCount = len(disabledComments) %>
          % if cFlagCount > 1:
             <% cString = 'Comments' %> 
          % else:
             <% cString = 'Comment' %> 
          % endif
          ${cString} In Suggestion <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${s['urlCode']}/${s['url']}">${s["title"]}</a></br>    	    
	    	% for comID in disabledComments:
	    	  <% com = getComment(comID) %>
		      &nbsp&nbsp&nbsp&nbsp&nbsp
	    	  % if checkFlagged(com):
			      % if int(com['numFlags']) is 1:
				      ${com['numFlags']} flag:
				  % else:
				      ${com['numFlags']} flags:
				  % endif
			  % else:
			  	  0 flags:
			  % endif
		      % if len(com['data']) > 20:
				  <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${s['urlCode']}/${s['url']}/modComment/${comID}">${com['data'][:20]}...</a>
			  % else:
				  <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${s['urlCode']}/${s['url']}/modComment/${comID}">${com['data']}</a>
		      % endif
	          </br>
			% endfor
		% endif
	% endfor
</%def>

<%def name="deleted()">
    <br /><br />
    <strong class="gray">Deleted Objects</strong>
    <br /><br />
    <strong>Resources and Comments:</strong>
    <br />
    % if c.deletedRes:
       % for r in c.deletedRes:
	      % if checkFlagged(r): 
			  ${r['numFlags']}
	          % if int(r['numFlags']) > 1:
	          	 Flags:
	          % else:
	             Flag:
	          % endif
          % endif
         Resource: <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}">${r['title']}</a>
         <a class="btn btn-mini" href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}/modResource/"> Admin Resource </a><br />
       % endfor
    % endif
	% for r in c.r:
    	<% deletedComments = getDeletedComments(r['discussion_id']) %>
    	% if deletedComments:
          <% cFlagCount = len(deletedComments) %>
          % if cFlagCount > 1:
             <% cString = 'Comments' %> 
          % else:
             <% cString = 'Comment' %> 
          % endif
          ${cString} In Suggestion <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}">${r["title"]}</a></br>    	    
	    	% for comID in deletedComments:
	    	  <% com = getComment(comID) %>
		      &nbsp&nbsp&nbsp&nbsp&nbsp
	    	  % if checkFlagged(com):
			      % if int(com['numFlags']) is 1:
				      ${com['numFlags']} flag:
				  % else:
				      ${com['numFlags']} flags:
				  % endif
			  % else:
			  	  0 flags:
			  % endif
		      % if len(com['data']) > 20:
				  <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}/modComment/${comID}">${com['data'][:20]}...</a>
			  % else:
				  <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}/modComment/${comID}">${com['data']}</a>
		      % endif
	          </br>
			% endfor
		% endif
	% endfor
    <br /><br />
    <strong>Suggestions and Comments:</strong>
    <br />
    % if c.deletedSug:
       % for s in c.deletedSug:
	      % if checkFlagged(s): 
			  ${s['numFlags']}
	          % if int(s['numFlags']) > 1:
	          	 Flags:
	          % else:
	             Flag:
	          % endif
          % endif
         Suggestion: <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${s['urlCode']}/${s['url']}">${s["title"]}</a>
         <a class="btn btn-mini" href="/modSuggestion/${s['urlCode']}/${s['url']}/">Admin Suggestion </a><br />
       % endfor
    % endif
    % for s in c.s:
    	<% deletedComments = getDeletedComments(s['discussion_id']) %>
    	% if deletedComments:
          <% cFlagCount = len(deletedComments) %>
          % if cFlagCount > 1:
             <% cString = 'Comments' %> 
          % else:
             <% cString = 'Comment' %> 
          % endif
          ${cString} In Suggestion <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${s['urlCode']}/${s['url']}">${s["title"]}</a></br>    	    
	    	% for comID in deletedComments:
	    	  <% com = getComment(comID) %>
		      &nbsp&nbsp&nbsp&nbsp&nbsp
	    	  % if checkFlagged(com):
			      % if int(com['numFlags']) is 1:
				      ${com['numFlags']} flag:
				  % else:
				      ${com['numFlags']} flags:
				  % endif
			  % else:
			  	  0 flags:
			  % endif
		      % if len(com['data']) > 20:
				  <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${s['urlCode']}/${s['url']}/modComment/${comID}">${com['data'][:20]}...</a>
			  % else:
				  <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${s['urlCode']}/${s['url']}/modComment/${comID}">${com['data']}</a>
		      % endif
	          </br>
			% endfor
		% endif
	% endfor
</%def>