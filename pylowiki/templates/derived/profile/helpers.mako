<%!
    from pylowiki.lib.db.suggestion import getSuggestionByID
    from pylowiki.lib.db.workshop import getWorkshop, getWorkshopsByOwner, getWorkshopByID
    from pylowiki.lib.db.facilitator import isFacilitator, isPendingFacilitator
    from pylowiki.lib.db.user import isAdmin, getUserLastPost
    from pylowiki.lib.fuzzyTime import timeSince
%>


<%def name="iconPath()">
	/images/glyphicons_pro/glyphicons/png/
</%def>

<%def name="displayProfilePicture()">
        <ul class="thumbnails">
        <li>
        <div class="thumbnail">
        % if c.user['pictureHash'] == 'flash':
                <img src="/images/avatars/flash.profile" alt="${c.user['name']}" title="${c.user['name']}">
        % else:
            <img src="/images/avatar/${c.user['directoryNumber']}/profile/${c.user['pictureHash']}.profile" alt="${c.user['name']}" title="${c.user['name']}">
        % endif
        </div>
        </li>
        </ul>
        ${memberAdminControls()}
</%def>

<%def name="listUser(user)">
        <tr>
        <td>
           <ul class="thumbnails">
           <li>
	   % if user['pictureHash'] == 'flash':
<a href="/profile/${user['urlCode']}/${user['url']}" class="thumbnail"><img src="/images/avatars/flash.profile" style="width:30px;" alt="${user['name']}" title="${user['name']}"/></a>
	   % else:
<a href="/profile/${user['urlCode']}/${user['url']}" class="thumbnail"><img src="/images/avatar/${user['directoryNumber']}/profile/${user['pictureHash']}.profile" style="width:30px;" alt="${user['name']}" title="${user['name']}"/></a>
	   % endif
           </li>
           </ul>
        </td>
        <td>
           <% mObj = getUserLastPost(user) %>
           <ul class="unstyled">
           <li><a href="/profile/${user['urlCode']}/${user['url']}">${user['name']}</a></li>
           % if mObj:
               % if mObj.objType == 'comment':
                   <% iType = "comment" %>
                   <% w = 0 %>
               % elif mObj.objType == 'resource':
                   <% w = getWorkshopByID(mObj['workshop_id']) %>
                   <% oLink = "/workshop/" + w['urlCode'] + "/" + w['url'] + "/resource/" + mObj['urlCode'] + "/" + mObj['url'] %>
                   <% wLink = "/workshop/" + w['urlCode'] + "/" + w['url'] %>
                   <% iType = "book" %>
               % elif mObj.objType == 'suggestion':
                   <% iType = "pencil" %>
                   <% oLink = "/workshop/" + mObj['workshopCode'] + "/" + mObj['workshopURL'] + "/suggestion/" + mObj['urlCode'] + "/" + mObj['url'] %>
                   <% wLink = "/workshop/" + mObj['workshopCode'] + "/" + mObj['workshopURL'] %>
                   <% w = getWorkshop(mObj['workshopCode'], mObj['workshopURL']) %>
               % endif
               % if w and w != 0:
                   %if len(mObj['title']) > 20:
                       <% oTitle = mObj['title'][0:16] + '...' %>
                   %else:
                       <% oTitle = mObj['title'] %>
                   %endif
                   %if len(w['title']) > 20:
                       <% wTitle = w['title'][0:16] + '...' %>
                   %else:
                       <% wTitle = w['title'] %>
                   %endif
                   <li><i class="icon-cog"></i><a href="${wLink}">${wTitle}</a></li>
                   <li><i class="icon-${iType}"></i><a href="${oLink}">${oTitle}</a></li>
               % endif
               % if mObj.objType == 'comment':
                   <li><i class="icon-${iType}"></i> New comment</a></li>
               % endif
                    <li><i class="icon-time"></i> ${timeSince(mObj.date)} ago</li>
                % endif
            </ul>
        </td>
        </tr>
</%def>

<%def name="displayFollowingUsers()">
    <% fNum = len(c.followingUsers) %>
    <h2 class="civ-col">Following (${fNum})</h2>
    <table class="table table-striped table-condensed">
    <tbody>
    % for user in c.followingUsers:
        ${listUser(user)}
    % endfor
    </tbody>
    </table>
</%def>

<%def name="displayUserFollows()">
    <% fNum = len(c.userFollowers) %>
    <h2 class="civ-col">Followers (${fNum})</h2>
    <table class="table table-striped table-condensed">
    <tbody>
    % for user in c.userFollowers:
        ${listUser(user)}
    % endfor
    </tbody>
    </table>
</%def>

<%def name="displayConnections()">
	<h6>Mutual connections:</h6>
	% if 'connectionList' not in c.user.keys():
		<div class="alert alert-warning">
			No connections!
		</div> <!-- /.alert-warning -->
	% else:
		<% counter = 1 %>
		% for item in c.user['connectionList']:
			% if counter < 6:
				<% comma = "," %>
			% elif counter == 6:
				<% comma = "" %>
			% else:
				<% break %>
			% endif
			<a href="${item['profileURL']}" alt="${item['name']}">${item['name']}</a>${comma} 
			<% counter += 1 %>
		% endfor
		% if len(c.user['connectionList']) > 6:
			and ${len(c.user['connectionList']) - 6} others.
		% endif
	% endif
</%def>

<%def name="sidebar()">
	${displayProfilePicture()}
	% if c.followingUsers:
		${displayFollowingUsers()}
	% endif
	% if c.userFollowers:
		${displayUserFollows()}
	% endif
	% if c.authuser['email'] != c.user['email']:
		<div class="civ-col">
			<h2 class="civ-col">Connections</h2>
			<div class="civ-col-inner">
				${displayConnections()}
			</div> <!-- /.civ-col-inner -->
		</div> <!-- /.civ-col -->
	% endif
</%def>

<%def name="summary()">
	<div class="civ-col-inner">
		<h1>${c.user['name']}</h1>
		<p>
			% if 'tagline' in c.user.keys():
				${c.user['tagline']}
			% else:
				No tagline.
			% endif
			<% mStart = c.user.date.strftime('%B %d, %Y') %>
			<br>
			User since <span class="recent">${mStart}</span>
		</p>
	</div> <!-- /.civ-col-inner -->
</%def>

<%def name="followButton()">
	<div class="civ-col-inner">
		<ul class="unstyled civ-col-list">
			<li>
				<img src="${iconPath()}/glyphicons_006_user_add.png"> ${len(c.userFollowers)} followers
			</li>
			<li>
				<%
					if int(c.user['totalPoints']) == 1:
						s = ""
					else:
						s = "s"
				%>
				<img src="${iconPath()}/glyphicons_037_credit.png"> ${c.user['totalPoints']} point${s}
			</li>
		</ul> <!-- /.civ-col-list -->
		% if c.authuser['email'] != c.user['email']:
                        <div class="button_container">
			% if c.isFollowing:
				<button rel="profile_${c.user['urlCode']}_${c.user['url']}" class="btn btn-primary followButton following">+Following</button>
			% else:
				<button rel="profile_${c.user['urlCode']}_${c.user['url']}" class="btn btn-primary followButton unfollow">+Follow</button>
			% endif
                        </div>
		% endif
	</div> <!-- /.civ-col-inner -->
</%def>

<%def name="geoInfo()">
	<div class="civ-col-inner">
		<ul class="unstyled civ-col-list">
			<li>
				<a href="${c.geoInfo[0]['cityURL']}"><img src="${c.geoInfo[0]['cityFlagThumb']}" width="60" />${c.geoInfo[0]['cityTitle']}</a>
			</li>
			<li>
				<a href="${c.geoInfo[0]['countyURL']}"><img src="${c.geoInfo[0]['countyFlagThumb']}" width="60" />${c.geoInfo[0]['countyTitle']}</a>
			</li>
			<li>
				<a href="${c.geoInfo[0]['stateURL']}"><img src="${c.geoInfo[0]['stateFlagThumb']}" width="60" />${c.geoInfo[0]['stateTitle']}</a>
			</li>
			<li>
				<img src="/images/flags/country/united-states/united-states_thumb.gif" width="60" />United States</a>
			</li>
			<li>
				<img src="/images/flags/earth_thumb.gif" width="60" />Earth</a>
			</li>
		</ul> <!-- /.unstyled -->
	</div> <!-- /.civ-col-inner -->
</%def>

<%def name="displayWorkshop(workshop)">
	% if workshop['mainImage_hash'] == 'supDawg':
		<a href="/workshop/${workshop['urlCode']}/${workshop['url']}"><img src="/images/${workshop['mainImage_identifier']}/thumbnail/${workshop['mainImage_hash']}.thumbnail" alt="${workshop['mainImage_hash']}" width="120" height="80"/></a><br>
		<p><a href="/workshop/${workshop['urlCode']}/${workshop['url']}">${workshop['title']}</a></p>
	% else:
		<a href="/workshop/${workshop['urlCode']}/${workshop['url']}"><img src="/images/${workshop['mainImage_identifier']}/${workshop['mainImage_directoryNum']}/thumbnail/${workshop['mainImage_hash']}.thumbnail" alt="${workshop['mainImage_hash']}" width="120" height="80"/>
		<p><a href="/workshop/${workshop['urlCode']}/${workshop['url']}">${workshop['title']}</a></p>
	% endif
</%def>

<%def name="listWorkshops(set)">
		<% wNum = 0 %>
		% for workshop in set:
			% if wNum % 6 == 0: ## begin a new row
			<ul class="unstyled civ-block-list">
				<li>
					${displayWorkshop(workshop)}
				</li>
			% elif wNum % 6 == 5: ## end a row
				<li>
					${displayWorkshop(workshop)}
				</li>
			</ul> <!-- /.unstyled -->
			% else: ## somewhere in between
				<li>
					${displayWorkshop(workshop)}
				</li>
			% endif
			<% wNum += 1 %>
		% endfor
</%def>

<%def name="workshops()">
	% if c.facilitatorWorkshops:
		<h2 class="civ-col">Workshops I am facilitating</h2>
		<div class="civ-col-inner">
			${listWorkshops(c.facilitatorWorkshops)}
		</div> <!-- /.civ-col-inner -->
	% endif
	% if c.followingWorkshops:
		<h2 class="civ-col">Workshops I am following</h2>
		<div class="civ-col-inner">
			${listWorkshops(c.followingWorkshops)}
		</div> <!-- /.civ-col-inner -->
	% endif
        % if c.pendingFacilitators and c.authuser.id == c.user.id:
            ${pendingFacilitateInvitations()}
        % endif
</%def>

<%def name="totalComments()">
	<%
		if 'numComments' in c.user.keys():
			total = int(c.user['numComments'])
		else:
			total = 0
		s = ""
		if total != 1:
			s += "s"
	%>
	<p class="total">
		${total}<br>
		<span>comment${s} made</span>
	</p>
</%def>

<%def name="latestComments()">
	% if 'numComments' in c.user.keys():
		<% count = 1 %>
		<ul class="unstyled civ-col-list">
		% for comment in c.user['comments']:
			% if count > 3:
				<% break %>
			% endif
			% if not comment['disabled'] and not comment['pending']:
				<li>
					<h4>Here is a comment summary.</h4>
					<span class="recent">one hour ago</span> in
					<a href="#">workshop</a>
				</li>
				<% count += 1 %>
			% endif
		% endfor
	</ul> <!-- /.civ-col-list -->
	% else:
		<div class="alert alert-warning">No comments to show.</div>
	% endif

</%def>

<%def name="totalSuggestions()">
	<%
		total = c.user['numSuggestions']
		s = ""
		if int(total) != 1:
			s += "s"
	%>
	<p class="total">
		${total}
		<br>
		<span>suggestion${s} made</span>
	</p>
</%def>

<%def name="latestSuggestions()">
	% if int(c.user['numSuggestions']) > 0:
		<% count = 1 %>
		<ul class="unstyled civ-col-list">
		% for item in c.user['suggestionList'].split(','):
			% if count > 3:
				<% break %>
			% endif
			<%
				s = getSuggestionByID(int(item))
				w = getWorkshop(s['workshopCode'], s['workshopURL'])
			%>
			<li>
				<a href = "/workshop/${w['urlCode']}/${w['url']}/suggestion/${s['urlCode']}/${s['url']}"><h4>${s["title"]}</h4></a>
				 in <a href="/workshop/${w['urlCode']}/${w['url']}">${w["title"]}</a>
			</li>
			<% count += 1 %>
		% endfor
	</ul> <!-- /.unstyled -->
	% else:
		<div class="alert alert-warning">No suggestions to show.</div>
	% endif
</%def>

<%def name="totalResources()">
	<%
		total = int(c.user['numReadResources'])
		s = ""
		if total != 1:
			s += "s"
	%>
	<p class="total">
		${total}
		<br>
		<span>resource${s} read</span>
	</p>
</%def>

<%def name="latestResources()">
	<%
		total = int(c.user['numReadResources'])
	%>
	% if total > 0:
		<% count = 1 %>
		% for item in reversed(c.user['articles']):
			% if count > 3:
				<% break %>
			% endif
			% if item["type"] == "background":
				<li><h4>Background wiki</h4> in<a href = "/issue/${item['articleURL']}/background">${item["articleTitle"]}</li></a>
			% else:
				<li><a href = "${item['articleURL']}"><h4>${item["articleTitle"]}</h4></a> in <a href="/issue/${item['issueURL']}">${item["issueTitle"]}</a></li>
			% endif
			<% count += 1 %>
		%endfor
	% else:
		<div class="alert alert-warning">No resources read.</div>
	% endif
</%def>

<%def name="memberAdminControls()">
    % if isAdmin(c.authuser.id):
        <a href="/profile/${c.user['urlCode']}/${c.user['url']}/admin"><button class="btn btn-warning"><i class="icon-user icon-white"></i> Admin Member</button></a>
    % endif
</%def>

<%def name="pendingFacilitateInvitations()">
% if c.pendingFacilitators and c.authuser.id == c.user.id:      
    <h2 class="civ-col">Invitations to CoFacilitate Workshops</h2>
    <% fNum = len(c.pendingFacilitators) %>
    <% wNum = 0 %>
    % for f in c.pendingFacilitators:
        % if wNum % 6 == 0 or wNum == 0: ## begin a new row
           <ul class="unstyled civ-block-list">
        % elif wNum % 6 == 5: ## end a row
           </ul>
           <ul class="unstyled civ-block-list">
        % endif
        <li>
        <% workshop = getWorkshopByID(f['workshopID']) %>
        <form method="post" name="inviteFacilitate" id="inviteFacilitate" action="/profile/${c.user['urlCode']}/${c.user['url']}/coFacilitateHandler/">
        <input type=hidden name=workshopCode value="${workshop['urlCode']}">
        <input type=hidden name=workshopURL value="${workshop['url']}">
        % if workshop['mainImage_hash'] == 'supDawg':
            <a href="/workshops/${workshop['urlCode']}/${workshop['url']}"><img src="/images/${workshop['mainImage_identifier']}/thumbnail/${workshop['mainImage_hash']}.thumbnail" alt="mtn" class="block" style = "margin: 5px; width: 120px; height: 80px;"/><br>
            <a href="/workshops/${workshop['urlCode']}/${workshop['url']}">${workshop['title']}</a>
        % else:
            <a href="/workshops/${workshop['urlCode']}/${workshop['url']}"><img src="/images/${workshop['mainImage_identifier']}/${workshop['mainImage_directoryNum']}/thumbnail/${workshop['mainImage_hash']}.thumbnail" alt="mtn" class="block" style = "margin: 5px; width: 120px; height: 80px;"/><br>
            <a href="/workshops/${workshop['urlCode']}/${workshop['url']}">${workshop['title']}</a>
        % endif
        <br /> <br />
        <button type="submit" name=acceptInvite class="btn btn-success">Accept</button>
        <button type="submit" name=declineInvite class="btn btn-danger">Decline</button>
        </form>
        <li>
        <% wNum = wNum + 1 %>
        %if wNum == 6:
            <% wNum = 0 %>
        %endif
    % endfor
    </ul>
% endif
</%def>

<%def name="inviteCoFacilitate()">
%if c.authuser:
    <% checkW = getWorkshopsByOwner(c.authuser.id) %>
    <% wList = [] %>
    % for w in checkW:
        % if w['deleted'] == '0':
            % if not isFacilitator(c.user.id, w.id) and not isPendingFacilitator(c.user.id, w.id):
                <% wList.append(w) %>
            % endif 
        % endif
    % endfor
    % if c.authuser.id != c.user.id and wList:
        <h2 class="civ-col">Invite This Member to Facilitate</h2>
        <form method="post" name="inviteFacilitate" id="inviteFacilitate" action="/profile/${c.user['urlCode']}/${c.user['url']}/coFacilitateInvite/" class="form-inline">
        <br />
        <button type="submit" class="btn btn-warning"><i class="icon-envelope icon-white"></i> Invite</button> to co-facilitate <select name=inviteToFacilitate>
        % for myW in wList:
            <br />
            <option value="${myW['urlCode']}/${myW['url']}">${myW['title']}</option>
            <br /><br />
        % endfor                       
        </select>
        </form>
    % endif
%endif
</%def>
