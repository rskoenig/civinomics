<%! 
   from pylowiki.lib.db.suggestion import getSuggestionsForWorkshop
   from pylowiki.lib.db.follow import getWorkshopFollowers
   from pylowiki.lib.db.geoInfo import getGeoInfo
   from pylowiki.lib.db.suggestion import getSuggestionByID
   from pylowiki.lib.db.tag import getPublicTagCount, getMemberTagCount
   from pylowiki.lib.db.workshop import getRecentMemberPosts, getWorkshopByID, getWorkshop
   from pylowiki.lib.db.user import getUserByID
   from pylowiki.lib.fuzzyTime import timeSince, timeUntil
%>
<%namespace file="/lib/mako_lib.mako" name="lib" />

<%def name='draw_avatar()'>
	${lib.displayProfilePicture()}
	<a href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}">
		<strong>${c.authuser['name']}</strong>
	</a>
	<br>
	<a href="/profile/edit">Edit my profile</a>
</%def>

<%def name='list_public_spheres()'>
	<% c.geoInfo = getGeoInfo(c.authuser.id) %>
        <table>
        <tbody>
        <tr>
        <td><a href="${c.geoInfo[0]['cityURL']}"><img src="${c.geoInfo[0]['cityFlagThumb']}" alt="${c.geoInfo[0]['cityTitle']}" class="thumbnail" style="max-width: 70px;"></a></td><td><a href="${c.geoInfo[0]['cityURL']}">${c.geoInfo[0]['cityTitle']}</a></td>
        </tr>
        <tr>
        <td><a href="${c.geoInfo[0]['countyURL']}"><img src="${c.geoInfo[0]['countyFlagThumb']}" alt="${c.geoInfo[0]['countyTitle']}" class="thumbnail" style="max-width: 70px"></a></td><td><a href="${c.geoInfo[0]['countyURL']}">${c.geoInfo[0]['countyTitle']}</a></td>
        </tr>
        <tr>
        <td><a href="${c.geoInfo[0]['stateURL']}"><img src="${c.geoInfo[0]['stateFlagThumb']}" alt="${c.geoInfo[0]['stateTitle']}" class="thumbnail" style="max-width: 70px"></a></td><td><a href="${c.geoInfo[0]['stateURL']}">${c.geoInfo[0]['stateTitle']}</a></td>
        </tr>
        <tr>
        <td><img src="${c.geoInfo[0]['countryFlagThumb']}" alt="${c.geoInfo[0]['countryTitle']}" class="thumbnail" style="max-width: 70px"></td><td>${c.geoInfo[0]['countryTitle']}</td>
        </tr>
        </tbody>
        </table>
</%def>

<%def name="show_me()">
    <script type="text/javascript">
    function setAction()
    {
        var searchType = document.getElementById('searchType').value;
        var searchString = document.getElementById('searchString').value;
        if (searchString == null || searchString == '')
        {
            var searchString = "%";
        }
        document.getElementById('searchWorkshops').action = '/searchName/' + searchType + '/' + searchString + '/';
    }
    </script>
    <form action="/searchName/" method="post" id="searchWorkshops" onsubmit="setAction(); return true;">
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
                    <input type="text" name="searchString" class="span8" id="searchString"><button class="btn" type="submit">Search</button>
                </div>
            </div>
        </div>
        </fieldset>
    </form>
    % if 'user' in session:
        <form class="left" id="searchGeoUsers" action="/searchGeoUsers/" method = "post">
            Members in my <select name="scopeLevel">
            <option value="09">City</option>
            <option value="07">County</option>
            <option value="05">State</option>
            <option value="03">Country</option>
            </select>
            <button class="btn" type="submit">Search</button>
        </form>
        <form class="left" id="searchGeoWorkshops" action="/searchGeoWorkshops/" method = "post">
            Workshops in my <select name="scopeLevel">
            <option value="09">City</option>
            <option value="07">County</option>
            <option value="05">State</option>
            <option value="03">Country</option>
            </select>
            <button class="btn" type="submit">Search</button>
        </form>
    % endif            
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

<%def name="recent_posts()">
	<% mPosts = getRecentMemberPosts(20) %>
	% if mPosts and len(mPosts) > 0:
            <table class="table table-striped">
            <tbody>
			% for mObj in mPosts:
                           <% ooTitle = False %>
                           <% muser = getUserByID(mObj.owner) %>
                           <% mname = muser['name'] %>
                           % if mObj.objType == 'resource':
                               <% w = getWorkshopByID(mObj['workshop_id']) %>
                               <% oLink = "/workshop/" + w['urlCode'] + "/" + w['url'] + "/resource/" + mObj['urlCode'] + "/" + mObj['url'] %>
                               <% wLink = "/workshop/" + w['urlCode'] + "/" + w['url'] %>
                               <% iType = "book" %>
                               % if mObj['parent_id'] != '0':
                                   <% s = getSuggestionByID(mObj['parent_id']) %>
                                   <% ooTitle = mObj['parent_id'] %>
                                   %if len(s['title']) > 20:
                                       <% ooTitle = s['title'][0:16] + '...' %>
                                   %else:
                                       <% ooTitle = s['title'] %>
                                   %endif
                                   <% ooLink = "/workshop/" + w['urlCode'] + "/" + w['url'] + "/suggestion/" + s['urlCode'] + "/" + s['url'] %>
                                   <% ooiType = "pencil" %>
                               % endif
                               <% oLink = "/workshop/" + w['urlCode'] + "/" + w['url'] + "/resource/" + mObj['urlCode'] + "/" + mObj['url'] %>
                           % elif mObj.objType == 'suggestion':
                               <% iType = "pencil" %>
                               <% oLink = "/workshop/" + mObj['workshopCode'] + "/" + mObj['workshopURL'] + "/suggestion/" + mObj['urlCode'] + "/" + mObj['url'] %>
                               <% wLink = "/workshop/" + mObj['workshopCode'] + "/" + mObj['workshopURL'] %>
                               <% w = getWorkshop(mObj['workshopCode'], mObj['workshopURL']) %>
                           %else:
                               <% iType = "comment" %>
                               <% oLink = "" %>
                           %endif
                           %if len(w['title']) > 20:
                               <% wTitle = w['title'][0:16] + '...' %>
                           %else:
                               <% wTitle = w['title'] %>
                           %endif
                           %if len(mObj['title']) > 20:
                               <% oTitle = mObj['title'][0:16] + '...' %>
                           %else:
                               <% oTitle = mObj['title'] %>
                           %endif
                           <tr>
                           <td>
                           % if muser['pictureHash'] == 'flash':
                               <a href="/profile/${muser['urlCode']}/${muser['url']}"><img src="/images/avatars/flash.profile" alt="${mname}" title="${mname}" style="width:40px;" alt="${mname}"/ class="thumbnail"></a> 
                           % else:
                               <a href="/profile/${muser['urlCode']}/${muser['url']}"><img src="/images/avatar/${muser['directoryNumber']}/profile/${muser['pictureHash']}.profile" alt="${mname}" title="${mname}" style="width:40px;"/ class="thumbnail"></a>
                           % endif
                           </td>
                           <td>
                              <ul class="unstyled">
                              <li><a href="${wLink}"><i class="icon-cog"></i> ${wTitle}</a></li>
                              % if ooTitle:
                                  <li><a href="${ooLink}"><i class="icon-${ooiType}"></i> ${ooTitle}</a></li>
                              % endif
                              <li><a href="${oLink}"><i class="icon-${iType}"></i> ${oTitle}</a></li>
                              <li><i class="icon-time"></i> ${timeSince(mObj.date)} ago</li>
                              <ul>
                           </td>
                           </tr>
			% endfor
            </tbody>
            </table>
	% else:
		<p>No member posts.</p>
	% endif
</%def>
