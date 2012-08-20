<%!
    from pylowiki.lib.db.user import getUserByID
%>

<%def name="comment_admin()">
    % if c.commentType == 'suggestion':
       Back to <a href="/workshop/${c.wCode}/${c.wURL}/suggestion/${c.oCode}/${c.oURL}">Suggestion</a>
    % elif c.commentType == 'resource':
       Back to <a href="/workshop/${c.wCode}/${c.wURL}/resource/${c.oCode}/${c.oURL}">Resource</a>
    % elif c.commentType == 'background':
       Back to <a href="/workshop/${c.wCode}/${c.wURL}/background">Background</a>
    % elif c.commentType == 'feedback':
       Back to <a href="/workshop/${c.wCode}/${c.wURL}/feedback">Feedback</a>
    % endif
    <br /><br />
    Added ${c.comment['lastModified']} by ${c.user['name']}
    <br /><br />
    ${c.comment['data']}
    <br /><br />
    <% fString = "Flags" %>
    % if len(c.flags) == '1':
       <% fString = "Flag" %>
    % endif
    <strong>${len(c.flags)} ${fString}:</strong>
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

<%def name="moderateComments()">
    <p>
    % if c.comment['deleted'] == '0':
	    <form name="moderate_comment" id="moderate_comment" class="left" action = "/modCommentHandler/${c.comment['urlCode']}" enctype="multipart/form-data" method="post" >
	    <input type=hidden name=commentID value="${c.commentID}">
	    <input type=hidden name=commentType value="${c.commentType}">
	    <input type=hidden name=workshopCode value="${c.wCode}">
	    <input type=hidden name=workshopURL value="${c.wURL}">
	    <input type=hidden name=otherCode value="${c.oCode}">
	    <input type=hidden name=otherURL value="${c.oURL}">
	    <br /><br />
	    Reason for action: &nbsp;
	    <input type=text name=modCommentReason><br /><br />
	    Click to verify&nbsp;<input type=radio name=verifyModComment> &nbsp; &nbsp;
	    % if c.comment['disabled'] == '0':
	       <button type="submit" name=modType value="disable" class="btn btn-warning">
	       		<i class="icon-ban-circle icon-white"></i> Disable Comment
	       </button>
	       <button type="submit" name=modType value="delete" class="btn btn-danger">
	       	   <i class="icon-trash icon-white"></i> Delete Comment
	       </button>
	    % else:
	       <button type="submit" name=modType value="disable" class="btn btn-warning">
	           <i class="icon-ok icon-white"></i>Enable Comment
	       </button>
	       <button type="submit" name=modType value="delete" class="btn btn-danger">
	       		<i class="icon-trash icon-white"></i> Delete Comment
	       </button>
		% endif
	% else:
		<br /><br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
		<code><strong>Comment Deleted</strong></code>
    % endif
	</form>
</%def>
