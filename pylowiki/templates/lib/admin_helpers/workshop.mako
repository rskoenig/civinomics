<%!
    from pylowiki.lib.db.flag import checkFlagged
    from pylowiki.lib.db.event import getParentEvents
    from pylowiki.lib.db.user import getUserByID
    from pylowiki.lib.db.comment import getPureFlaggedDiscussionComments, getComment, getDisabledComments, getDeletedComments
%>  

<%def name="banner_name()">
    <h1><a href = "/workshop/${c.w['urlCode']}/${c.w['url']}">${c.title}</a></h1>
</%def>

<%def name="admin_show()">
        <br />
	<div class="left well">
	<form name="admin_issue" id="admin_issue" action = "/workshop/${c.w['urlCode']}/${c.w['url']}/adminWorkshopHandler" enctype="multipart/form-data" method="post" >
    <strong>Message to Participants:</strong>
    <br />
    <textarea name="motd" rows="5" cols="50">${c.motd['data']}</textarea>
    <br />
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
    </div>
</%def>

<%def name="admin_event_log()">
    <% wEvents = getParentEvents(c.w) %>
    <br /><br />
    <table class="table table-bordered">
    <thead>
    <tr><th><i class="icon-bookmark"></i>Workshop Events</th></tr>
    </thead>
    <tbody>
    % if wEvents:
        <br /><br />
        % for wE in wEvents:
            <tr><td><strong>${wE.date} ${wE['title']}</strong> ${wE['data']}</td></tr>
        % endfor
    % endif
    </tbody>
    </table>
</%def>


<%def name="admin_facilitators()">
    <br /><br />
    <table class="table table-bordered">
    <thead>
    <tr><th><i class="icon-user"></i>Current Facilitators</th></tr>
    </thead>
    <tbody>
    % for f in c.f:
       <% fUser = getUserByID(f.owner) %>
       <% fEvents = getParentEvents(f) %>
       <% fPending = "" %>
       % if pending in f and f['pending'] == '1':
          <% fPending = "(Pending)" %>
       % endif
       <tr><td><a href="/profile/${fUser['urlCode']}/${fUser['url']}">${fUser['name']}</a> ${fPending}<br />
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
       </td></tr>
    % endfor
    </tbody>
    </table>
    <table class="table table-bordered">
    <thead>
    <tr><th><i class="icon-user"></i>Disabled Facilitators</th></tr>
    </thead>
    <tbody>
    % for f in c.df:
       <% fUser = getUserByID(f.owner) %>
       <% fEvents = getParentEvents(f) %>
       <tr><td><a href="/profile/${fUser['urlCode']}/${fUser['url']}">${fUser['name']}</a> (Disabled)<br />
       % if fEvents:
          % for fE in fEvents:
          &nbsp; &nbsp; &nbsp; <strong>${fE.date} ${fE['title']}</strong>  ${fE['data']}<br />
          % endfor
       % endif
       </tr></td>
    % endfor
    </tbody>
    </table>

</%def>


<%def name="admin_info()">
    <% wEvents = getParentEvents(c.w) %>
    <br /><br />
    <table class="table table-bordered">
    <thead>
    <tr><th><i class="icon-bookmark"></i>Workshop Events</th></tr>
    </thead>
    <tbody>
    % if wEvents:
        <br /><br />
        % for wE in wEvents:
            <tr><td><strong>${wE.date} ${wE['title']}</strong> ${wE['data']}</td></tr>
        % endfor
    % endif
    </tbody>
    </table>
    <br /><br />
    <br /><br />
    <table class="table table-bordered">
    <thead>
    <tr><th><i class="icon-user"></i>Current Facilitators</th></tr>
    </thead>
    <tbody>
    % for f in c.f:
       <% fUser = getUserByID(f.owner) %>
       <% fEvents = getParentEvents(f) %>
       <% fPending = "" %>
       % if pending in f and f['pending'] == '1':
          <% fPending = "(Pending)" %>
       % endif
       <tr><td><a href="/profile/${fUser['urlCode']}/${fUser['url']}">${fUser['name']}</a> ${fPending}<br />
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
       </td></tr>
    % endfor
    </tbody>
    </table>
    <table class="table table-bordered">
    <thead>
    <tr><th><i class="icon-user"></i>Disabled Facilitators</th></tr>
    </thead>
    <tbody>
    % for f in c.df:
       <% fUser = getUserByID(f.owner) %>
       <% fEvents = getParentEvents(f) %>
       <tr><td><a href="/profile/${fUser['urlCode']}/${fUser['url']}">${fUser['name']}</a> (Disabled)<br />
       % if fEvents:
          % for fE in fEvents:
          &nbsp; &nbsp; &nbsp; <strong>${fE.date} ${fE['title']}</strong>  ${fE['data']}<br />
          % endfor
       % endif
       </tr></td>
    % endfor
    </tbody>
    </table>
    <br /><br />
</%def>

<%def name="admin_flagged()">
	<br />
    <table class="table table-bordered">
    <thead>
    <tr><th><i class="icon-flag"></i>Flagged Resources and Comments</th</tr>
    </thead>
    <tbody>
    % if c.r:
       % for r in c.r:
          % if checkFlagged(r) and r['disabled'] == '0' and r['deleted'] == '0': 
			  <tr><td>${r['numFlags']}
	          % if int(r['numFlags']) > 1:
	          	 Flags:
	          % else:
	             Flag:
	          % endif
             Resource: <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}">${r['title']}</a>
             <a class="btn btn-mini" href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}/modResource/"> Admin Resource </a><br />
              </td></tr>
          % endif
          <% cList = getPureFlaggedDiscussionComments(r['discussion_id']) %>
          % if cList:
             <% cFlagCount = len(cList) %>
             % if cFlagCount > 1:
                <% cString = 'Comments' %> 
             % else:
                <% cString = 'Comment' %> 
             % endif
             <tr><td>${cString} In Resource <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}">${r["title"]}</a></br>
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
                </td></tr>
          % endif
       % endfor
    % endif
    </tbody>
    </table>
    <br /><br />
    <table class="table table-bordered">
    <thead>
    <tr><th><i class="icon-flag"></i>Flagged Suggestions and Comments:</td><tr>
    </thead>
    <tbody>
    % for s in c.s:
       % if checkFlagged(s) and s['disabled'] == '0' and s['deleted'] == '0': 
		  ${s['numFlags']}
          % if int(s['numFlags']) > 1:
          	 <tr><td>Flags:
          % else:
             Flag:
          % endif
          Suggestion <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${s['urlCode']}/${s['url']}">${s["title"]}</a>
          <a class="btn btn-mini" href="/modSuggestion/${s['urlCode']}/${s['url']}/">Admin Suggestion </a><br />
          </td></tr>
       % endif
       <% cList = getPureFlaggedDiscussionComments(s['discussion_id']) %>
       % if cList:
          <% cFlagCount = len(cList) %>
          % if cFlagCount > 1:
             <% cString = 'Comments' %> 
          % else:
             <% cString = 'Comment' %> 
          % endif
          <tr><td>${cString} In Suggestion <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${s['urlCode']}/${s['url']}">${s["title"]}</a></br>
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
          </td></tr>
       % endif
    % endfor
    </tbody>
    </table>
</%def>

<%def name="admin_disabled()">
    <br /><br />
    <table class="table table-bordered">
    <thead>
    <tr><th><i class="icon-ban-circle"></i>Disabled Resources and Comments</tr></th>
    </thead>
    <tbody>
    % if c.disabledRes:
       % for r in c.disabledRes:
	      % if checkFlagged(r): 
			  ${r['numFlags']}
	          % if int(r['numFlags']) > 1:
	          	 <tr><td>Flags:
	          % else:
	             Flag:
	          % endif
          % endif
         Resource: <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}">${r['title']}</a>
         <a class="btn btn-mini" href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}/modResource/"> Admin Resource </a><br />
         </td></tr>
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
          <tr><td>${cString} In Resource <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}">${r["title"]}</a></br>    	    
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
                </td></tr>
		% endif
	% endfor
        </tbody>
        </table>
    <br /><br />
    <table class="table table-bordered">
    <thead>
    <tr><th><i class="icon-ban-circle"></i>Disabled Suggestions and Comments:</th></tr>
    </thead>
    <tbody>
    % if c.disabledSug:
       % for s in c.disabledSug:
	      % if checkFlagged(s): 
			  <tr><td>${s['numFlags']}
	          % if int(s['numFlags']) > 1:
	          	 Flags:
	          % else:
	             Flag:
	          % endif
          % endif
         Suggestion: <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${s['urlCode']}/${s['url']}">${s["title"]}</a>
         <a class="btn btn-mini" href="/modSuggestion/${s['urlCode']}/${s['url']}/">Admin Suggestion </a><br />
         </td></tr>
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
          <tr><td>${cString} In Suggestion <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${s['urlCode']}/${s['url']}">${s["title"]}</a></br>    	    
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
                  </td></tr>
		% endif
	% endfor
        </tbody>
        </table>
</%def>

<%def name="admin_deleted()">
    <br /><br />
    <table class="table table-bordered">
    <thead>
    <tr><th><i class="icon-trash"></i>Deleted Resources and Comments</th></tr>
    </thead>
    <tbody>
    % if c.deletedRes:
       % for r in c.deletedRes:
	      % if checkFlagged(r): 
			  <tr><td>${r['numFlags']}
	          % if int(r['numFlags']) > 1:
	          	 Flags:
	          % else:
	             Flag:
	          % endif
          % endif
         Resource: <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}">${r['title']}</a>
         <a class="btn btn-mini" href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}/modResource/"> Admin Resource </a><br />
         </td></tr>
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
          <tr><td>${cString} In Suggestion <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}">${r["title"]}</a></br>    	    
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
                   </td></tr>
		% endif
	% endfor
        </tbody>
        </table>
    <br /><br />
    <table class="table table-bordered">
    <thead>
    <tr><th><i class="icon-trash"></i>Deleted Suggestions and Comments</th></tr>
    </thead>
    <tbody>
    % if c.deletedSug:
       % for s in c.deletedSug:
	      % if checkFlagged(s): 
			  <tr><td>${s['numFlags']}
	          % if int(s['numFlags']) > 1:
	          	 Flags:
	          % else:
	             Flag:
	          % endif
          % endif
         Suggestion: <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${s['urlCode']}/${s['url']}">${s["title"]}</a>
         <a class="btn btn-mini" href="/modSuggestion/${s['urlCode']}/${s['url']}/">Admin Suggestion </a><br />
         </td></tr>
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
          <tr><td>${cString} In Suggestion <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${s['urlCode']}/${s['url']}">${s["title"]}</a></br>    	    
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
                        </td></tr>
		% endif
	% endfor
        </tbody>
        </table>
</%def>
