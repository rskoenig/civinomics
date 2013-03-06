<%! 
   from pylowiki.lib.db.suggestion import getSuggestionsForWorkshop
   from pylowiki.lib.db.follow import getWorkshopFollowers
   from pylowiki.lib.db.geoInfo import getGeoInfo
   from pylowiki.lib.db.tag import getPublicTagCount, getMemberTagCount
%>
<%namespace file="/lib/mako_lib.mako" name="lib" />
<%namespace name="profile_helpers" file="/derived/profile/helpers.mako" />

<%def name="list_users()">
    <ul class="unstyled civ-col-list">
    % for item in c.paginator:
        ${profile_helpers.listUser(item, 1)}
    % endfor
    </ul>
</%def>

<%def name="list_total_users()">
    <% 
        state = True
        for p in c.paginator:
            state = not state
    %>
	Total Users: ${c.count} | View ${ c.paginator.pager('~3~') }
</%def>

<%def name='list_news()'>
    ## Seems deprecated
</%def>
