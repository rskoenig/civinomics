<%!
	from pylowiki.lib.fuzzyTime import timeSince
	from pylowiki.lib.db.user import getUserByID
%>

<%def name="nav_thing()">
    % if c.suggestion:
        <br />
        <p>
        <strong><i class="icon-pencil"></i> <a href="/workshop/${c.suggestion['workshopCode']}/${c.suggestion['workshopURL']}/suggestion/${c.suggestion['urlCode']}/${c.suggestion['url']}">${c.suggestion['title']}</a></strong>
        </p>
    % endif
</%def>

<%def name="displayRating()">
		<a href="#"><i class="icon-chevron-up"></i></a>
		<div>rating</div>
		<a href="#"><i class="icon-chevron-down"></i></a>
</%def>

<%def name="displayMetaData()">
	<h3><a href="${c.resource['link']}" target="_blank" alt="${c.resource['title']}">${c.resource['title']}</a></h3>
	(${c.resource['domain']}.${c.resource['tld']})
	<br>
        <% author = c.poster %>
        <ul class="unstyled civ-col-list">
        <li class="post">
        % if author['pictureHash'] == 'flash':
            <a href="/profile/${author['urlCode']}/${author['url']}"><img src="/images/avatars/flash.thumbnail" lt="${author['name']}" title="${author['name']}" class="thumbnail" style="width:30px;}"/></a>
        % else:
            <a href="/profile/${author['urlCode']}/${author['url']}"><img src="/images/avatar/${author['directoryNumber']}/thumbnail/${author['pictureHash']}.thumbnail" lt="${author['name']}" title="${author['name']}" class="thumbnail"/></a>
        % endif
        &nbsp;By <a href="/profile/${author['urlCode']}/${author['url']}">${author['name']}</a> <span class="recent">${timeSince(c.resource.date)}</span> ago
        </li>
</%def>

<%def name="displayResourceComment()">
	<div id="resource-comment">
		<p>${c.resource['comment']}</p>
	</div>
</%def>

<%def name="displayResource()">
	<div class="span1 civ-votey">
		${displayRating()}
	</div> <!-- .span1.civ-votey -->

	<div class="span11">
		<div class="row-fluid">
			<div class="span12">
				${displayMetaData()}
			</div>
		</div>

		<div class="row-fluid resource-comment">
			<div class="span12">
				${displayResourceComment()}
			</div> <!-- .span12 -->
		</div> <!-- .row-fluid -->
	</div> <!-- /.span11 -->
</%def>
