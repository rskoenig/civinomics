<%! 
   from pylowiki.lib.db.suggestion import getSuggestionByID, getSuggestionsForWorkshop
   from pylowiki.lib.db.follow import getWorkshopFollowers
   from pylowiki.lib.db.geoInfo import getGeoInfo
   from pylowiki.lib.db.tag import getPublicTagCount, getMemberTagCount
   from pylowiki.lib.db.workshop import getRecentMemberPosts, getWorkshopByID, getWorkshop
   from pylowiki.lib.db.user import getUserByID
   from pylowiki.lib.fuzzyTime import timeSince, timeUntil

   import logging
   log = logging.getLogger(__name__)
%>
## -*- coding: utf-8 -*-
<%namespace file="/lib/mako_lib.mako" name="lib" />

<%def name='draw_avatar()'>
	${lib.displayProfilePicture()}
	<a href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}">
	</a>
	<br>
</%def>

<%def name='list_public_spheres()'>
	<% c.geoInfo = getGeoInfo(c.authuser.id) %>
        <p class="zip">
            <a 
            % if c.geoType == "none":
                    class ="active"
            %endif 
            href="/workshops">All </a>/
            <a 
            % if c.geoType == "planet":
                class ="active"
            %endif 
            href="/geo/planet/earth">Earth </a>/
            <a 
            % if c.geoType == "country":
                class ="active"
            %endif
            href="${c.geoInfo[0]['countryURL']}">${c.geoInfo[0]['countryTitle']}  </a>/
            <a 
            % if c.geoType == "state":
                class ="active"
            %endif
            href="${c.geoInfo[0]['stateURL']}">  ${c.geoInfo[0]['stateTitle']}  </a>/
            <a 
            % if c.geoType == "county":
                class ="active"
            %endif
            href="${c.geoInfo[0]['countyURL']}">  ${c.geoInfo[0]['countyTitle']}, Co.  </a>/
            <a 
            % if c.geoType == "city":
                class ="active"
            %endif
            href="${c.geoInfo[0]['cityURL']}">  ${c.geoInfo[0]['cityTitle']}, City  </a>/
            <a 
            % if c.geoType == "postal":
                class ="active"
            %endif
            href="${c.geoInfo[0]['postalURL']}">  ${c.geoInfo[0]['postalCode']}</a>
        </p>
</%def>

<%def name='list_public_spheres_suggestions()'>
    <% c.geoInfo = getGeoInfo(c.authuser.id) %>
        <p class="zip">
            <a 
            % if c.geoType == "none":
                class ="active"
            %endif
            href="/suggestions">All </a>/
            <a 
            % if c.geoType == "planet":
                class ="active"
            %endif
            href="/suggestions/geo/planet/earth">Earth </a>/
            <a 
            % if c.geoType == "country":
                class ="active"
            %endif
            href="/suggestions${c.geoInfo[0]['countryURL']}">${c.geoInfo[0]['countryTitle']}  </a>/
            <a 
            % if c.geoType == "state":
                class ="active"
            %endif
            href="/suggestions${c.geoInfo[0]['stateURL']}">  ${c.geoInfo[0]['stateTitle']}  </a>/
            <a 
            % if c.geoType == "county":
                class ="active"
            %endif
            href="/suggestions${c.geoInfo[0]['countyURL']}">  ${c.geoInfo[0]['countyTitle']}, Co.  </a>/
            <a 
            % if c.geoType == "city":
                class ="active"
            %endif
            href="/suggestions${c.geoInfo[0]['cityURL']}">  ${c.geoInfo[0]['cityTitle']}, City  </a>/
            <a 
            % if c.geoType == "postal":
                class ="active"
            %endif
            href="/suggestions${c.geoInfo[0]['postalURL']}">  ${c.geoInfo[0]['postalCode']}</a>
        </p>
</%def>

<%def name='ws_toggle()'>
        <p class="zip">
            <a 
            % if c.objecttype == "workshop":
                class ="active"
            %endif
            href="/workshops">Workshops</a>
            <a 
            % if c.objecttype == "suggestion":
                class ="active"
            %endif
            href="/suggestions">Suggestions</a>
        </p>
</%def>

<%def name="show_me()">
    <script type="text/javascript">
    function setAction()
    {
        var searchType = document.getElementById('searchType').value;
        var searchString = document.getElementById('searchString').value;
        if (searchString == null || searchString == '')
        {
            document.getElementById('searchWorkshops').action = '/workshops';
        } else {
            document.getElementById('searchWorkshops').action = '/searchName/' + searchType + '/' + searchString + '/';
        }
    }
    function setScope()
    {
        var scopeList = document.getElementById('scopeLevel');
        var scopeLevel = scopeList.options[scopeList.selectedIndex].value;
        if (scopeLevel == null || scopeLevel == '')
        {
            var scopeLevel = "03";
        }
        document.getElementById('searchGeoUsers').action = '/searchGeoUsers/' + scopeLevel;
    }
    </script>
    <br />
    <span class="pull-right">
    <form action="/searchName/" method="post" id="searchWorkshops" onsubmit="setAction(); return true;" class="form-search">
        <select name="searchType" id="searchType" class="input-small" style="font-size:12px;">
            <option value="Workshops">Workshops named</option>
            <option value="Members">Members named</option>
        </select> <input type="text" name="searchString" id="searchString" class="input-small search-query"> <button class="btn btn-primary btn-mini" type="submit" title="Click to search"><i class="icon-white icon-search"></i></button>
    </form><br />
    </span><!-- pull-right -->
    % if 'user' in session:
        <span class="pull-right">
        <form id="searchGeoUsers" action="/searchGeoUsers/" method = "post" onsubmit="setScope(); return true;" class="form-search" >
            Members in my &nbsp;<select name="scopeLevel" id="scopeLevel" class="input-small" style="font-size:12px;">
            <option value="09">City</option>
            <option value="07">County</option>
            <option value="05">State</option>
            <option value="03">Country</option>
            </select> <button class="btn btn-primary btn-mini" type="submit" title="Click to search"><i class="icon-white icon-search"></i></button>
        </form><br />
        </span><!-- pull-right -->
    % endif            
</%def>

<%def name="public_tags()">
	<% pTags = getPublicTagCount() %>
	<ul class="unstyled">
		% for pT in sorted(pTags.keys()):
			<% fixedpT = pT.replace(" ", "_") %>
			<li><a href="/searchTags/${fixedpT}/" title="Click to view workshops with this tag">${pT}</a>: ${pTags[pT]}</li>
		% endfor
	</ul> <!-- /.unstyled -->
</%def>

<%def name="member_tags()">
	<% mTags = getMemberTagCount() %>
	% if len(mTags.keys()) > 0:
		<ul class="unstyled">
			% for mT in sorted(mTags.keys()):
				<% fixedmT = mT.replace(" ", "_") %>
				<li><a href="/searchTags/${fixedmT}/" title="Click to view workshops with this tag">${mT}</a>: ${mTags[mT]}</li>
			% endfor
		</ul>
	% else:
		<p>No member tags.</p>
	% endif
</%def>

<%def name="recent_posts()">
	<% mPosts = getRecentMemberPosts(23) %>
	% if mPosts and len(mPosts) > 0:
            <ul class="unstyled civ-col-list">
			% for mObj in mPosts:
        <li>
        <% 
          ooTitle = False
          muser = getUserByID(mObj.owner)
          mname = muser['name']
          if mObj.objType == 'resource':
              linkTitle = "Click to view new resource"
              w = getWorkshopByID(mObj['workshop_id'])
              oLink = "/workshop/" + w['urlCode'] + "/" + w['url'] + "/resource/" + mObj['urlCode'] + "/" + mObj['url']
              wLink = "/workshop/" + w['urlCode'] + "/" + w['url']
              iType = "book"
              if mObj['parent_id'] != '0':
                  s = getSuggestionByID(mObj['parent_id'])
                  ooTitle = mObj['parent_id']
                  oolinkTitle = "Click to view suggestion"
                  if len(s['title']) > 20:
                      ooTitle = s['title'][0:16] + '...'
                  else:
                      ooTitle = s['title']
                  ooLink = "/workshop/" + w['urlCode'] + "/" + w['url'] + "/suggestion/" + s['urlCode'] + "/" + s['url']
                  ooiType = "pencil"
              oLink = "/workshop/" + w['urlCode'] + "/" + w['url'] + "/resource/" + mObj['urlCode'] + "/" + mObj['url']
          elif mObj.objType == 'suggestion':
              linkTitle = "Click to view new suggestion"
              iType = "pencil"
              oLink = "/workshop/" + mObj['workshopCode'] + "/" + mObj['workshopURL'] + "/suggestion/" + mObj['urlCode'] + "/" + mObj['url']
              wLink = "/workshop/" + mObj['workshopCode'] + "/" + mObj['workshopURL']
              w = getWorkshop(mObj['workshopCode'], mObj['workshopURL'])
          elif mObj.objType == 'event':
              iType = "heart"
              linkTitle = "Click to view adopted suggestion"
              s = getSuggestionByID(mObj['parent_id'])
              muser = getUserByID(s.owner)
              oLink = "/workshop/" + s['workshopCode'] + "/" + s['workshopURL'] + "/suggestion/" + s['urlCode'] + "/" + s['url']
              wLink = "/workshop/" + s['workshopCode'] + "/" + s['workshopURL']
              w = getWorkshop(s['workshopCode'], s['workshopURL'])
          elif mObj.objType == 'discussion':
              linkTitle = "Click to view new discussion"
              iType = "folder-open"
              oLink = "/workshop/" + mObj['workshopCode'] + "/" + mObj['workshopURL'] + "/discussion/" + mObj['urlCode'] + "/" + mObj['url']
              wLink = "/workshop/" + mObj['workshopCode'] + "/" + mObj['workshopURL']
              w = getWorkshop(mObj['workshopCode'], mObj['workshopURL'])
          else:
              iType = "comment"
              oLink = ""
          endif
          if len(w['title']) > 20:
              wTitle = w['title'][0:16] + '...'
          else:
              wTitle = w['title']
          endif
          if len(mObj['title']) > 20:
              oTitle = mObj['title'][0:16] + '...'
          else:
              oTitle = mObj['title']
        %>

         <div class="row-fluid">
             <div class="span3">
         % if muser['pictureHash'] == 'flash':
             <a href="/profile/${muser['urlCode']}/${muser['url']}"><img src="/images/avatars/flash.profile" alt="${mname}" title="Click to view profile of ${mname}" style="width:40px;" alt="${mname}"/ class="thumbnail"></a> 
         % else:
             <a href="/profile/${muser['urlCode']}/${muser['url']}"><img src="/images/avatar/${muser['directoryNumber']}/profile/${muser['pictureHash']}.profile" alt="${mname}" title="Click to view profile of ${mname}" style="width:40px;"/ class="thumbnail"></a>
         % endif
             </div><!-- span3 -->
             <div class="span9">
             ${log.info(oTitle)}
            New <a href="${oLink}" title="${linkTitle}"><i class="icon-${iType}"></i> ${oTitle}</a><br />
            % if ooTitle:
                in <a href="${ooLink}" title="${oolinkTitle}"><i class="icon-${ooiType}"></i> ${ooTitle}</a><br />
            % endif
            in <a href="${wLink}" title="Click to view workshop"><i class="icon-cog"></i> ${wTitle}</a><br />
            <i class="icon-time"></i> <span class="recent">${timeSince(mObj.date)}</span> ago<br />
            <ul>
            </div><!-- cpan9 -->
         </div><!-- row-fluid -->
         </li>
			% endfor
      </ul>
	% else:
		<p>No member posts.</p>
	% endif
</%def>
