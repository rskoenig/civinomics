<%!
    from pylowiki.lib.db.flag import checkFlagged, getFlags
    from pylowiki.lib.db.event import getParentEvents
    from pylowiki.lib.db.user import getUserByID
    import pylowiki.lib.db.discussion       as discussionLib
    import pylowiki.lib.db.idea             as ideaLib
    import pylowiki.lib.db.comment          as commentLib
%>  
<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="admin_show()">
	<div class="left well">
    <h3>Facilitator Tools</h3>
    <br />
	<form name="admin_issue" id="admin_issue" class="form-inline" action="/workshop/${c.w['urlCode']}/${c.w['url']}/adminWorkshopHandler" enctype="multipart/form-data" method="post" >
    <strong>Message to Participants:</strong>
    <br />
    This is displayed on the workshop landing page. Use this to welcome members to the workshop or to make announcements.<br />
    <textarea name="motd" rows="2" cols="80">${c.motd['data']}</textarea>
    &nbsp; &nbsp;
    <% 
      if c.motd['enabled'] == '1':
        pChecked = 'checked'
        uChecked = ''
      else:
        pChecked = ''
        uChecked = 'checked'
    %>
    <input type="radio" name="enableMOTD" value="1" ${pChecked}> Publish Message&nbsp;&nbsp;&nbsp;<input type="radio" name="enableMOTD" value="0" ${uChecked}> Unpublish Message
    <br /><br />
    % if c.w['startTime'] != '0000-00-00':
        % if c.w['deleted'] == '1':
           <strong>Publish Workshop</strong><br />
           This republishes the workshop, displaying it in lists of active workshops. It may be unpublished again later.<br />
           <% eAction = 'Publish' %>
        % else:
           <strong>Unpublish Workshop</strong><br />
           This unpublishes the workshop, removing it from lists of active workshops. It may be republished again later.<br />
           <% eAction = 'Unpublish' %>
        % endif
        Reason: <input type="text" name="eventReason" id="eventReason"> &nbsp; &nbsp;
        <input type="radio" name="enableWorkshop" value="1"> ${eAction}&nbsp;&nbsp;&nbsp;<input type="radio" name="verifyEnableWorkshop" value="0"> Verify ${eAction}
    % endif
    <br /><br />
    <button type="submit" class="btn btn-warning">Save All Changes</button>
    </form>
    </div>
</%def>

<%def name="admin_event_log()">
    <h3>Event Log</h3>
    A record of configuration and administrative changes to the workshop.<br />
    <% wEvents = getParentEvents(c.w) %>
    <table class="table table-bordered">
    <thead>
    <tr><th>Workshop Events</th></tr>
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
    % if c.w['public_private'] != 'trial':
        <table class="table table-bordered">
        <thead>
        <tr><th>Current Facilitators</th></tr>
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
            % if len(c.f) > 1 and fUser.id == c.authuser.id:
                <form id="resignFacilitator" name="resignFacilitator" action="/workshop/${c.w['urlCode']}/${c.w['url']}/resignFacilitator" method="post">
                    &nbsp; &nbsp; &nbsp;Note: <input type="text" name="resignReason"> &nbsp;&nbsp;&nbsp;
                    <button type="submit" class="gold" value="Resign">Resign</button>
                    <br />
                </form>
            % endif
            </td></tr>
        % endfor
        </tbody>
        </table>
        <p>To invite an active member to co-facilitate this workshop, visit their profile page and look for the "Invite to co-facilitate" button!</p>
        % if len(c.df) > 0:
            <table class="table table-bordered">
            <thead>
            <tr><th>Disabled Facilitators</th></tr>
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
        % endif
    % endif
</%def>


<%def name="admin_info()">
    <% wEvents = getParentEvents(c.w) %>
    <table class="table table-bordered">
    <thead>
    <tr><th>Workshop Events</th></tr>
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
    <tr><th>Current Facilitators</th></tr>
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
               &nbsp; &nbsp; &nbsp;Note: <input type="text" name="resignReason"> &nbsp;&nbsp;&nbsp;
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
    <tr><th>Disabled Facilitators</th></tr>
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

<%def name="admin_items(itemlist, type, action)">
    % if itemlist:
        % for item in itemlist:
            % if action == 'flagged':
                % if checkFlagged(item) and item['disabled'] == '0' and item['deleted'] == '0': 
    		        <tr><td>(${r['numFlags']})
                    ${type.title()}: <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/${type}/${item['urlCode']}/${item['url']}">${item['title']}</a>
                    </td></tr>
                % endif
            % endif
            <% 
                if type != 'discussion':
                    discussion = discussionLib.getDiscussionForThing(item)
                else:
                    discussion = item
                cList = []
                if discussion:
                    if action == 'flagged':
                        cList = commentLib.getFlaggedCommentsInDiscussion(discussion)
            %>
            % if cList:
                <% numcomments = len(cList) %>
                % if numcomments > 1:
                    <% cString = 'Comments' %>
                %else:
                    <% cString = 'Comment' %>
                % endif

                <tr><td>${cString} In ${type.title()} <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/${type}/${item['urlCode']}/${item['url']}">${item["title"]}</a></br>
		 	    % for com in cList:
                    + 
                    % if action == 'flagged':
				        (${com['numFlags']}) 
				    % endif
					<a href="/workshop/${c.w['urlCode']}/${c.w['url']}/${type}/${item['urlCode']}/${item['url']}#accordion-${com['urlCode']}">${com['data'][:20]}</a><br />
          	    % endfor
                </td></tr>
            % endif
        % endfor
    % endif
</%def>

<%def name="admin_flagged()">
    <h3>Flagged Items</h3>
    These are items in the workshop which have been flagged by members. Each flagged item needs to be examined by the facilitator and some action taken, even if it is only clearing the flags.<br />
    <br /><br />
    <table class="table table-bordered">
    <thead>
    <tr><th>Flagged Resources and Comments</th</tr>
    </thead>
    <tbody>
    ${admin_items(c.r, 'resource', 'flagged')}
    </tbody>
    </table>
    <br /><br />
    <table class="table table-bordered">
    <thead>
    <tr><th>Flagged Ideas and Comments:</td><tr>
    </thead>
    <tbody>
    ${admin_items(c.i, 'idea', 'flagged')}
    </tbody>
    </table>
    <br /><br />
    <table class="table table-bordered">
    <thead>
    <tr><th>Flagged Discussions and Comments:</td><tr>
    </thead>
    <tbody>
    ${admin_items(c.d, 'discussion', 'flagged')}
    </tbody>
    </table>
</%def>

<%def name="admin_disabled()">
    <h3>Disabled Items</h3>
    These are items in the workshop which have been disabled by a facilitator or admin. These items are filtered to the bottom of lists 
    or not displayed by default. Items are often disabled for being off-topic, duplicates of existing items, or have been flagged as 
    offensive or otherwise violating the terms of service.
    <table class="table table-bordered">
    <thead>
    <tr><th>Disabled Background Comments</tr></th>
    </thead>
    <tbody>
    <%  
            discussion = discussionLib.getDiscussionForThing(c.w)
            disabledComments = []
            if discussion:
                disabledComments = commentLib.getCommentsInDiscussion(discussion, disabled = '1') 
    %>
    % if disabledComments:
        <% cFlagCount = len(disabledComments) %>
        % if cFlagCount > 1:
            <% cString = 'Comments' %> 
        % else:
            <% cString = 'Comment' %> 
        % endif
        <tr><td>${cString} In <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/background">Background</a></br>    	    
        % for com in disabledComments:
            &nbsp&nbsp&nbsp&nbsp&nbsp
            % if checkFlagged(com):
                % if int(com['numFlags']) == 1:
                    ${com['numFlags']} flag:
                % else:
                    ${com['numFlags']} flags:
                % endif
            % else:
                0 flags:
            % endif
            % if len(com['data']) > 20:
                <a href="/adminComment/${com['urlCode']}">${com['data'][:20]}...</a>
            % else:
                <a href="/adminComment/${com['urlCode']}">${com['data']}</a>
            % endif
            </br>
        % endfor
        </td></tr>
    % endif
    </tbody>
    </table>
    <br /><br />
    <table class="table table-bordered">
    <thead>
    <tr><th>Disabled Resources and Comments</tr></th>
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
    	<%  
            discussion = discussionLib.getDiscussionForThing(r)
            disabledComments = []
            if discussion:
                disabledComments = commentLib.getCommentsInDiscussion(discussion, disabled = '1')
        %>
    	% if disabledComments:
          <% cFlagCount = len(disabledComments) %>
          % if cFlagCount > 1:
             <% cString = 'Comments' %> 
          % else:
             <% cString = 'Comment' %> 
          % endif
          <tr><td>${cString} In Resource <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}">${r["title"]}</a></br>    	    
	    	% for com in disabledComments:
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
				  <a href="/adminComment/${com['urlCode']}">${com['data'][:20]}...</a>
			  % else:
				  <a href="/adminComment/${com['urlCode']}">${com['data']}</a>
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
    <tr><th>Disabled Ideas and Comments:</th></tr>
    </thead>
    <tbody>
    % if c.disabledIdeas:
       % for i in c.disabledIdeas:
	      % if checkFlagged(s): 
			  <tr><td>${i['numFlags']}
	          % if int(i['numFlags']) > 1:
	          	 Flags:
	          % else:
	             Flag:
	          % endif
          % endif
         Suggestion: <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/idea/${i['urlCode']}/${i['url']}">${i["title"]}</a>
         </td></tr>
       % endfor
    % endif
    % for i in c.i:
        <%  
            discussion = discussionLib.getDiscussionForThing(i)
            disabledComments = []
            if discussion:
                disabledComments = commentLib.getCommentsInDiscussion(discussion, disabled = '1') 
        %>
    	% if disabledComments:
          <% cFlagCount = len(disabledComments) %>
          % if cFlagCount > 1:
             <% cString = 'Comments' %> 
          % else:
             <% cString = 'Comment' %> 
          % endif
          <tr><td>${cString} In Suggestion <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${s['urlCode']}/${s['url']}">${s["title"]}</a></br>    	    
	    	% for com in disabledComments:
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
				  <a href="/adminComment/${com['urlCode']}">${com['data'][:20]}...</a>
			  % else:
				  <a href="/adminComment/${com['urlCode']}">${com['data']}</a>
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
    <tr><th>Disabled Discussions and Comments:</th></tr>
    </thead>
    <tbody>
    % if c.disabledDisc:
       % for d in c.disabledDisc:
              <tr><td>
	      % if checkFlagged(d): 
			  ${len(getFlags(d))}
	          % if len(getFlags(d)) > 1:
	          	 Flags:
	          % else:
	             Flag:
	          % endif
          % endif
         Discussion: <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/discussion/${d['urlCode']}/${d['url']}">${d["title"]}</a>
         </td></tr>
       % endfor
    % endif
    % for d in c.d:
    	<% disabledComments = commentLib.getCommentsInDiscussion(d, disabled = '1')  %>
    	% if disabledComments:
          <% cFlagCount = len(disabledComments) %>
          % if cFlagCount > 1:
             <% cString = 'Comments' %> 
          % else:
             <% cString = 'Comment' %> 
          % endif
          <tr><td>${cString} In Discussion <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/discussion/${d['urlCode']}/${d['url']}">${d["title"]}</a></br>    	    
	    	% for com in disabledComments:
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
				  <a href="/adminComment/${com['urlCode']}">${com['data'][:20]}...</a>
			  % else:
				  <a href="/adminComment/${com['urlCode']}">${com['data']}</a>
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
    <h3>Deleted Items</h3>
    These are items in the workshop which have been deleted by a facilitator or admin. These items are filtered to the bottom of lists 
    and their content not displayed to anyone, including members and admins. Items are deleted when they are in violation of the law such 
    as linking to pirated content or child porn or if they are serious breech of the terms of service such as displaying or linking to porn.
    <table class="table table-bordered">
    <thead>
    <tr><th>Deleted Background Comments</tr></th>
    </thead>
    <tbody>
    <% 
        discussion = discussionLib.getDiscussionForThing(c.w)
        deletedComments = []
        if discussion:
            deletedComments = commentLib.getCommentsInDiscussion(discussion, deleted = '1')  
    %>
    % if deletedComments:
        <% cFlagCount = len(deletedComments) %>
        % if cFlagCount > 1:
            <% cString = 'Comments' %> 
        % else:
            <% cString = 'Comment' %> 
        % endif
        <tr><td>${cString} In <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/background">Background</a></br>    	    
        % for com in deletedComments:
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
                <a href="/adminComment/${com['urlCode']}">${com['data'][:20]}...</a>
            % else:
                <a href="/adminComment/${com['urlCode']}">${com['data']}</a>
            % endif
            </br>
        % endfor
        </td></tr>
    % endif
    </tbody>
    </table>
    <br /><br />
    <table class="table table-bordered">
    <thead>
    <tr><th>Deleted Resources and Comments</th></tr>
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
        <% 
            discussion = discussionLib.getDiscussionForThing(r)
            deletedComments = []
            if discussion:
                deletedComments = commentLib.getCommentsInDiscussion(discussion, deleted = '1') 
        %>
    	% if deletedComments:
          <% cFlagCount = len(deletedComments) %>
          % if cFlagCount > 1:
             <% cString = 'Comments' %> 
          % else:
             <% cString = 'Comment' %> 
          % endif
          <tr><td>${cString} In Resource <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${r['urlCode']}/${r['url']}">${r["title"]}</a></br>    	    
	    	% for com in deletedComments:
		      &nbsp&nbsp&nbsp&nbsp&nbsp
	    	  % if checkFlagged(com):
			      % if int(com['numFlags']) == 1:
				      ${com['numFlags']} flag:
				  % else:
				      ${com['numFlags']} flags:
				  % endif
			  % else:
			  	  0 flags:
			  % endif
		      % if len(com['data']) > 20:
				  <a href="/adminComment/${com['urlCode']}">${com['data'][:20]}...</a>
			  % else:
				  <a href="/adminComment/${com['urlCode']}">${com['data']}</a>
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
    <tr><th>Deleted Ideas and Comments</th></tr>
    </thead>
    <tbody>
    % if c.deletedIdeas:
       % for i in c.deletedIdeas:
	      % if checkFlagged(i): 
			  <tr><td>${i['numFlags']}
	          % if int(i['numFlags']) > 1:
	          	 Flags:
	          % else:
	             Flag:
	          % endif
          % endif
         Suggestion: <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/ideas/${i['urlCode']}/${i['url']}">${i["title"]}</a>
         </td></tr>
       % endfor
    % endif
    % for i in c.i:
        <% 
            discussion = discussionLib.getDiscussionForThing(i)
            deletedComments = []
            if discussion:
                deletedComments = commentLib.getCommentsInDiscussion(discussion, deleted = '1') 
        %>
    	% if deletedComments:
          <% cFlagCount = len(deletedComments) %>
          % if cFlagCount > 1:
             <% cString = 'Comments' %> 
          % else:
             <% cString = 'Comment' %> 
          % endif
          <tr><td>${cString} In Idea <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/idea/${s['urlCode']}/${i['url']}">${i["title"]}</a></br>    	    
	    	% for com in deletedComments:
		      &nbsp&nbsp&nbsp&nbsp&nbsp
	    	  % if checkFlagged(com):
			      % if int(com['numFlags']) == 1:
				      ${com['numFlags']} flag:
				  % else:
				      ${com['numFlags']} flags:
				  % endif
			  % else:
			  	  0 flags:
			  % endif
		      % if len(com['data']) > 20:
				  <a href="/adminComment/${com['urlCode']}">${com['data'][:20]}...</a>
			  % else:
				  <a href="/adminComment/${com['urlCode']}">${com['data']}</a>
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
    <tr><th>Deleted Discussions and Comments</th></tr>
    </thead>
    <tbody>
    % if c.deletedDisc:
       % for d in c.deletedDisc:
              <tr><td>
	      % if checkFlagged(d): 
			  ${len(getFlags(d))}
	          % if len(getFlags(d)) > 1:
	          	 Flags:
	          % else:
	             Flag:
	          % endif
          % endif
         Discussion: <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/discussion/${d['urlCode']}/${d['url']}">${d["title"]}</a>
         </td></tr>
       % endfor
    % endif
    % for d in c.d:
    	<% deletedComments = commentLib.getCommentsInDiscussion(discussion, deleted = '1') %>
    	% if deletedComments:
          <% cFlagCount = len(deletedComments) %>
          % if cFlagCount > 1:
             <% cString = 'Comments' %> 
          % else:
             <% cString = 'Comment' %> 
          % endif
          <tr><td>${cString} In Discussion <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/discussion/${d['urlCode']}/${d['url']}">${d["title"]}</a></br>
        	% for com in deletedComments:
		      &nbsp&nbsp&nbsp&nbsp&nbsp
	    	  % if checkFlagged(com):
			      % if int(com['numFlags']) == 1:
				      ${com['numFlags']} flag:
				  % else:
				      ${com['numFlags']} flags:
				  % endif
			  % else:
			  	  0 flags:
			  % endif
		      % if len(com['data']) > 20:
				  <a href="/adminComment/${com['urlCode']}">${com['data'][:20]}...</a>
			  % else:
				  <a href="/adminComment/${com['urlCode']}">${com['data']}</a>
		      % endif
	          </br>
			% endfor
                        </td></tr>
		% endif
	% endfor
        </tbody>
        </table>
</%def>
