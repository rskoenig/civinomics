<%! 
   from pylowiki.lib.db.suggestion import getSuggestionsForWorkshop
   from pylowiki.lib.db.follow import getWorkshopFollowers
   from pylowiki.lib.db.geoInfo import getGeoInfo
   from pylowiki.lib.db.tag import getPublicTagCount, getMemberTagCount
%>
<%namespace file="/lib/mako_lib.mako" name="lib" />
<%namespace name="profile_helpers" file="/derived/profile/helpers.mako" />

<%def name="list_users()">
    <table class="table table-striped table-condensed">
    <tbody>
    % for item in c.paginator:
        ${profile_helpers.listUser(item)}
    % endfor
    </tbody>
    </table>
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
