<%! 
   from pylowiki.lib.db.suggestion import getSuggestionsForWorkshop
   from pylowiki.lib.db.follow import getWorkshopFollowers
   from pylowiki.lib.db.geoInfo import getGeoInfo
   from pylowiki.lib.db.tag import getPublicTagCount, getMemberTagCount
%>
<%namespace file="/lib/mako_lib.mako" name="lib" />

<%def name='draw_avatar()'>
	${lib.displayProfilePicture()}
	<br>
	<a href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}">
		<strong>${c.authuser['name']}</strong>
	</a>
	<br>
	<a href="/profile/edit">Edit my profile</a>
</%def>

<%def name='list_public_spheres()'>
	<% c.geoInfo = getGeoInfo(c.authuser.id) %>
	<ul class="unstyled civ-col-list">
		<li>
	        <a href="${c.geoInfo[0]['cityURL']}">
	        	<img src="${c.geoInfo[0]['cityFlagThumb']}" alt="${c.geoInfo[0]['cityTitle']}" style="max-width: 70px;"> ${c.geoInfo[0]['cityTitle']}
	        </a>
		</li>
		<li>
			<a href="${c.geoInfo[0]['countyURL']}">
				<img src="${c.geoInfo[0]['countyFlagThumb']}" alt="${c.geoInfo[0]['countyTitle']}" style="max-width: 70px"> ${c.geoInfo[0]['countyTitle']}
			</a>
		</li>
		<li>
			<a href="${c.geoInfo[0]['stateURL']}">
				<img src="${c.geoInfo[0]['stateFlagThumb']}" alt="${c.geoInfo[0]['stateTitle']}" style="max-width: 70px"> ${c.geoInfo[0]['stateTitle']}
			</a>
		</li>
	</ul> <!-- /.civ-col-list -->
</%def>

<%def name="show_me()">
	<form action="/searchName/" method="post" id="searchWorkshops">
		<fieldset>
			<div class="control-group">
				<div class="controls">
					<select name="searchType" id="searchType">
						<option value="Workshops">Workshops</option>
						<option value="Members">Members</option>
					</select>
				</div>
			</div>
			<div class="control-group">
				<div class="controls">
					<div class="input-prepend">
						<span class="add-on">named</span><input type="text" name="searchString" class="span9">
					</div>
				</div>
			</div>
			<button class="btn" type="submit">Search</button>
		</fieldset>
	</form>
</%def>

<%def name="public_tags()">
	<% pTags = getPublicTagCount() %>
	<ul class="unstyled">
		% for pT in pTags.keys():
			<% fixedpT = pT.replace(" ", "_") %>
			<li><a href="/searchTags/${fixedpT}/">${pT}</a>: ${pTags[pT]}</li>
		% endfor
	</ul> <!-- /.unstyled -->
</%def>

<%def name="member_tags()">
	<% mTags = getMemberTagCount() %>
	% if len(mTags.keys()) > 0:
		<ul class="unstyled">
			% for mT in mTags.keys():
				<% fixedmT = mT.replace(" ", "_") %>
				<li><a href="/searchTags/${fixedmT}/">${mT}</a>: ${mTags[mT]}</li>
			% endfor
		</ul>
	% else:
		<p>No member tags.</p>
	% endif
</%def>

<%def name="list_users()">
	<ul class="unstyled civ-col-list">
		% for item in c.paginator:
			<li>
                       % if item['pictureHash'] == 'flash':
                         <a href="/profile/${item['urlCode']}/${item['url']}"><img src="/images/avatars/flash.profile" style="width:50px;"/> ${item['name']}</a>
                       % else:
                         <div class="blockthumb"><a href="/profile/${item['urlCode']}/${item['url']}"><img src="/images/avatar/${item['directoryNumber']}/profile/${item['pictureHash']}.profile" style="width:50px;"/></a></div><a href="/profile/${item['urlCode']}/${item['url']}"> ${item['name']}</a>
                       % endif
			</li>
		% endfor
	</ul> <!-- /.civ-col-list -->
</%def>

<%def name="list_total_users()">
	<% state = True %>
	% for p in c.paginator:
	    <% state = not state %>
	% endfor
	Total Users: ${c.count} | View ${ c.paginator.pager('~3~') }
</%def>

<%def name='list_news()'>
	##<ul class="unstyled civ-col-list">
		##<li>
			##<img src="/home/evante/civinomics/civinomics-bootstrap/bootstrapped/bootstrap with docs/docs/assets/img/bird.png" width="30">
			##<a href="#">Bird</a> did something with another animal.
		##</li>
	##</ul>
</%def>
