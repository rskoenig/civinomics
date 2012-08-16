<%!
	from pylowiki.lib.fuzzyTime import timeSince
	from pylowiki.lib.db.user import getUserByID
	from pylowiki.lib.db.flag import getFlags
%>

<%def name="nav_thing()">
    % if c.suggestion or c.s:
        % if c.s:
            <% s = c.s %>
        % else:
            <% s = c.suggestion %>
        % endif
        <br />
        <p>
        <strong><i class="icon-pencil"></i> <a href="/workshop/${s['workshopCode']}/${s['workshopURL']}/suggestion/${s['urlCode']}/${s['url']}">${s['title']}</a></strong>
        </p>
    % endif
</%def>

<%def name="displayRating()">
    <a href="/rateResource/${c.resource['urlCode']}/${c.resource['url']}/1" class="upVote voted">
        <i class="icon-chevron-up"></i>
    </a>
    <% rating = int(c.resource['ups']) - int(c.resource['downs']) %>
    <div>${rating}</div>
    <a href="/rateResource/${c.resource['urlCode']}/${c.resource['url']}/-1" class="downVote voted">
        <i class="icon-chevron-down"></i>
    </a>
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
		<div class="row-fluid">
			<div class="span12">
                           % if c.isFacilitator or c.isAdmin:
                               <% rFlags = getFlags(c.resource) %>
                               % if rFlags and len(rFlags) > 0:
                                   <span class="badge badge-important"><i class="icon-white icon-flag"></i> ${len(rFlags)}</span>&nbsp;&nbsp;
                               % endif
                               <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${c.resource['urlCode']}/${c.resource['url']}/modResource" class="btn btn-mini" title="Administrate Resource"><i class="icon-list-alt"></i> Admin</a>&nbsp;&nbsp;
                           % endif
                           % if (c.authuser and c.authuser.id == c.poster.id) or c.isAdmin or c.isFacilitator:
                               <a href="/editResource/${c.resource['urlCode']}/${c.resource['url']}" class="btn btn-mini" title="Edit Resource"><i class="icon-edit"></i> Edit</a>&nbsp;&nbsp;
                           % endif
                           <a href="/flagResource/${c.resource['urlCode']}/${c.resource['url']}" class="btn btn-mini flagButton" title="Flag Resource"><i class="icon-flag"></i> Flag</a> &nbsp; 
                        <span id="flag_0"></span>
			</div> <!-- .span12 -->
		</div> <!-- .row-fluid -->

	</div> <!-- /.span11 -->
</%def>
