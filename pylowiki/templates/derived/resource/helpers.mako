<%!
	from pylowiki.lib.fuzzyTime import timeSince
	from pylowiki.lib.db.user import getUserByID
	from pylowiki.lib.db.flag import getFlags
%>

<%def name="nav_thing()">
    % if c.suggestion or c.s:
        <%
          if c.s:
            s = c.s
          else:
            s = c.suggestion
        %>
        <br />
        <p>
        <strong><i class="icon-pencil"></i> <a href="/workshop/${s['workshopCode']}/${s['workshopURL']}/suggestion/${s['urlCode']}/${s['url']}">${s['title']}</a></strong>
        </p>
    % endif
</%def>

<%def name="displayRating()">
    <% rating = int(c.resource['ups']) - int(c.resource['downs']) %>
    % if 'user' in session and c.isScoped and c.conf['read_only.value'] != 'true': 
        <a href="/rateResource/${c.resource['urlCode']}/${c.resource['url']}/1" class="upVote voted">
            <i class="icon-chevron-up"></i>
        </a>
        <div>${rating}</div>
        <a href="/rateResource/${c.resource['urlCode']}/${c.resource['url']}/-1" class="downVote voted">
            <i class="icon-chevron-down"></i>
        </a>
    % else:
        <div>${rating}</div>
    % endif
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
        &nbsp;By <a href="/profile/${author['urlCode']}/${author['url']}">${author['name']}</a> <span class="recent">${timeSince(c.lastmoddate)}</span> ago
        </li>
</%def>

<%def name="displayResourceComment()">
  <div id="resource-comment">
      % if c.content:
        <p>${c.content}</p>
      % else:
        <p>${c.resource['comment']}</p>
      % endif
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

    % if c.conf['read_only.value'] == 'true':
      <% pass %>
    % else:
      <div class="row-fluid">
        <div class="span12">
          % if c.isFacilitator or c.isAdmin:
              <% rFlags = getFlags(c.resource) %>
              % if rFlags and len(rFlags) > 0:
                  <span class="badge badge-inverse" title="Flags on this resource"><i class="icon-white icon-flag"></i> ${len(rFlags)}</span>&nbsp;&nbsp;
              % endif
              <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${c.resource['urlCode']}/${c.resource['url']}/modResource" class="btn btn-mini btn-warning" title="Administrate Resource"><i class="icon-white icon-list-alt"></i> Admin</a>&nbsp;&nbsp;
          % endif
          % if (c.authuser and c.authuser.id == c.poster.id) or c.isAdmin or c.isFacilitator:
              <a href="/editResource/${c.resource['urlCode']}/${c.resource['url']}" class="btn btn-mini btn-primary" title="Edit Resource"><i class="icon-white icon-edit"></i> Edit</a>&nbsp;&nbsp;
          % endif
          % if 'user' in session:
              <a href="/flagResource/${c.resource['urlCode']}/${c.resource['url']}" class="btn btn-mini btn-inverse flagButton" title="Flag Resource"><i class="icon-white icon-flag"></i> Flag</a> &nbsp; 
              <span id="flag_0"></span>
          % endif
          % if c.revisions and len(c.revisions) > 1:
              <br />
              <strong>Edit log:</strong><br />
              % for rev in c.revisions:
                  <% ruser = getUserByID(rev.owner) %>
                  <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${c.resource['urlCode']}/${c.resource['url']}/${rev['urlCode']}/">${rev.date}</a> by <a href="/profile/${ruser['urlCode']}/${ruser['url']}">${ruser['name']}</a><br />

              % endfor
          % endif
        </div> <!-- .span12 -->
      </div> <!-- .row-fluid -->
    % endif
  </div> <!-- /.span11 -->
</%def>
