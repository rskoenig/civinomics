<%! 
   from pylowiki.lib.db.suggestion import getSuggestionsForWorkshop
   from pylowiki.lib.db.follow import getWorkshopFollowers
   from pylowiki.lib.db.geoInfo import getGeoInfo
   from pylowiki.lib.db.tag import getPublicTagCount, getMemberTagCount
   #from pylowiki.lib.fuzzyTime import timeUntil
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
		<li>
				<img src="${c.geoInfo[0]['countryFlagThumb']}" alt="${c.geoInfo[0]['countryTitle']}" style="max-width: 70px"> ${c.geoInfo[0]['countryTitle']}
		</li>
	</ul> <!-- /.civ-col-list -->
</%def>

<%def name="show_me()">
	<form action="/searchName/" method="post" id="searchWorkshops">
		<fieldset>
			<div class="control-group">
				<div class="controls">
                                        <select class="span8" name="searchType" id="searchType"> named
						<option value="Workshops">Workshops named</option>
						<option value="Members">Members named</option>
					</select>
				</div>
			</div>
			<div class="control-group">
				<div class="controls">
					<div class="input-append">
						<input type="text" name="searchString" class="span8"><button class="btn" type="submit">Search</button>
					</div>
				</div>
			</div>
		</fieldset>
	</form>
        <form class="left" id="searchGeoUsers" action="/searchGeoUsers/" method = "post">
                     Members in my <select name="scopeLevel">
                     <option value=8>City</option>
                     <option value=6>County</option>
                     <option value=4>State</option>
                     <option value=2>Country</option>
                     </select>
                     <button class="btn" type="submit">Search</button>
                     </form>
                     <form class="left" id="searchGeoWorkshops" action="/searchGeoWorkshops/" method = "post">
                     Workshops in my <select name="scopeLevel">
                     <option value=8>City</option>
                     <option value=6>County</option>
                     <option value=4>State</option>
                     <option value=2>Country</option>
                     </select>
                     <button class="btn" type="submit">Search</button>
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
