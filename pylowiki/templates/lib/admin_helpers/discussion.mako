<%!
    from pylowiki.lib.db.user import getUserByID
%>

<%def name="dis_admin_header()">
    <div class="page-header">
        <h1><a href="/workshop/${c.w['urlCode']}/${c.w['url']}/discussion/${c.discussion['urlCode']}/${c.discussion['url']}/">${c.discussion['title']}</a></h1>
    </div>  
</%def>

<%def name="discussion_admin_options()">
    <br /><br />
##    <strong>Post Event Note on Discussion</strong>
##    <form name="note_discussion" id="note_discussion" class="left" action = "/adminDiscussionHandler" enctype="multipart/form-data" method="post" >
##    <input type=hidden name=workshopCode value="${c.w['urlCode']}">
##    <input type=hidden name=workshopURL value="${c.w['url']}">
##    <input type=hidden name=discussionCode value="${c.discussion['urlCode']}">
##    <input type=hidden name=discussionURL value="${c.discussion['url']}">
##    <br />
##    Note: &nbsp;
##    <input type=text name=noteDiscussionText><br /><br />
##    <button type="submit" class="btn btn-warning">Save Note</button>
    </form>
        <strong>Moderate Discussion</strong>
    	% if c.discussion['deleted'] == '0':
    		<form name="moderate_discussion" id="moderate_discussion" class="left" action = "/adminDiscussionHandler" enctype="multipart/form-data" method="post" >
    	    <input type=hidden name=workshopCode value="${c.w['urlCode']}">
    	    <input type=hidden name=workshopURL value="${c.w['url']}">
    	    <input type=hidden name=discussionCode value="${c.discussion['urlCode']}">
    	    <input type=hidden name=discussionURL value="${c.discussion['url']}">
    	    <br /><br />
    	    Reason for action: &nbsp;
    	    <input type=text name=modDiscussionReason><br /><br />
    	    Click to verify&nbsp;<input type=radio name=verifyModDiscussion> &nbsp; &nbsp;
    	    % if c.discussion['disabled'] == '0':
    	       <button type="submit" name=modType value="disable" class="btn btn-warning">
    	       		<i class="icon-ban-circle icon-white"></i> Disable Discussion
    	       </button>
    	    % else:
    	       <button type="submit" name=modType value="disable" class="btn btn-warning">
    	           <i class="icon-ok icon-white"></i> Enable Discussion
    	       </button>
            % endif
           <button type="submit" name=modType value="delete" class="btn btn-danger">
           	   <i class="icon-trash icon-white"></i> Delete Discussion
           </button>
    	% else:
    		<br /><br />
    		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    		<code><strong>Discussion Deleted</strong></code>
    	% endif
    </form>

</%def>
