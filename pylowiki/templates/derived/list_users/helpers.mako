<%! 
   from pylowiki.lib.db.suggestion import getSuggestionsForWorkshop
   from pylowiki.lib.db.follow import getWorkshopFollowers
   from pylowiki.lib.db.geoInfo import getGeoInfo
   from pylowiki.lib.db.tag import getPublicTagCount, getMemberTagCount
%>
<%namespace file="/lib/mako_lib.mako" name="lib" />

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
