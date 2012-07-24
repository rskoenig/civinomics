<%!
    from pylowiki.lib.db.suggestion import getSuggestionByID
    from pylowiki.lib.db.workshop import getWorkshop
    from pylowiki.lib.db.user import isAdmin
%>


<%def name="iconPath()">
	/images/glyphicons_pro/glyphicons/png/
</%def>

<%def name="displayProfilePicture()">
	% if c.user['pictureHash'] == 'flash':
		<img src="/images/avatars/flash.profile" width="200"/>
	% else:
		<img src="/images/avatar/${c.user['directoryNumber']}/profile/${c.user['pictureHash']}.profile" width="200"/>
	% endif
	% if c.authuser['email'] == c.user['email']:
		<br>
		<a href="/profile/edit" alt="edit profile">Edit my profile</a>
	% endif
</%def>

<%def name="listUser(user)">
	% if user['pictureHash'] == 'flash':
		<a href="/profile/${user['urlCode']}/${user['url']}"><img src="/images/avatars/flash.profile" style="width:50px;"/>${user['name']}</a>
	% else:
		<a href="/profile/${user['urlCode']}/${user['url']}"><img src="/images/avatar/${user['directoryNumber']}/profile/${user['pictureHash']}.profile" style="width:50px;"/></a>
		<a href="/profile/${user['urlCode']}/${user['url']}">${user['name']}</a>
	% endif
</%def>

<%def name="displayFollowingUsers()">
	<div class="civ-col">
		<% fNum = len(c.followingUsers) %>
		<h2 class="civ-col">Following (${fNum})</h2>
		<div class="civ-col-inner">
			<ul class="unstyled civ-block-list">
				% for user in c.followingUsers:
					<li>
						${listUser(user)}
					</li>
				% endfor
			</ul> <!-- /.civ-block-list -->
		</div> <!-- /.civ-col-inner -->
	</div> <!-- /.civ-col -->
</%def>

<%def name="displayUserFollows()">
	<% fNum = len(c.userFollowers) %>
	<div class="civ-col">
		<h2 class="civ-col">Followers (${fNum})</h2>
		<div class="civ-col-inner">
			<ul class="unstyled civ-block-list">
				% for user in c.userFollowers:
					<li>
						${listUser(user)}
					</li>
				% endfor
			</ul> <!-- /.civ-block-list -->
		</div> <!-- /.civ-col-inner -->
	</div> <!-- /.civ-col -->
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
				<button rel="profile_${c.user['urlCode']}_${c.user['url']}" class="btn btn-primary followButton following">Following</button>
			% else:
				<button rel="profile_${c.user['urlCode']}_${c.user['url']}" class="btn btn-primary followButton unfollow">Follow</button>
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
		<a href="/workshops/${workshop['urlCode']}/${workshop['url']}"><img src="/images/${workshop['mainImage_identifier']}/thumbnail/${workshop['mainImage_hash']}.thumbnail" alt="${workshop['mainImage_hash']}" width="120" height="80"/></a><br>
		<p><a href="/workshops/${workshop['urlCode']}/${workshop['url']}">${workshop['title']}</a></p>
	% else:
		<a href="/workshops/${workshop['urlCode']}/${workshop['url']}"><img src="/images/${workshop['mainImage_identifier']}/${workshop['mainImage_directoryNum']}/thumbnail/${workshop['mainImage_hash']}.thumbnail" alt="${workshop['mainImage_hash']}" width="120" height="80"/>
		<p><a href="/workshops/${workshop['urlCode']}/${workshop['url']}">${workshop['title']}</a></p>
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
        <a href="/profile/${c.user['urlCode']}/${c.user['url']}/admin"><button class="btn btn-warning">Admin Member</button></a>
    % endif
</%def>

<%def name="pendingFacilitateInvitations()">
</%def>
