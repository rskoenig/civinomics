<%! 
   from pylowiki.lib.db.suggestion import getActiveSuggestionsForWorkshop, getAdoptedSuggestionsForWorkshop
   from pylowiki.lib.db.resource import getResourcesByWorkshopID
   from pylowiki.lib.db.follow import getWorkshopFollowers
   from pylowiki.lib.db.geoInfo import getGeoInfo
   from pylowiki.lib.db.tag import getPublicTagCount, getMemberTagCount
   from pylowiki.lib.fuzzyTime import timeUntil
%>
<%namespace file="/lib/mako_lib.mako" name="lib" />

<%def name="featured_workshop()">
	% if len(c.list) > 0 and c.list[0]['urlCode'] == c.paginator[0]['urlCode'] and c.action == 'sitemapIssues':
		<div class="civ-img-cap" style="border:1px solid black;">
		    <% mainWorkshop = c.paginator.pop(0) %>
		    % if mainWorkshop['mainImage_hash'] == 'supDawg':
		        <a href = '/workshops/${mainWorkshop['urlCode']}/${mainWorkshop['url']}'>
				    <img src="/images/${mainWorkshop['mainImage_identifier']}/slideshow/${mainWorkshop['mainImage_hash']}.slideshow" style="max-width: 100%" alt="${mainWorkshop['title']}" title="${mainWorkshop['title']}">
				</a>
			% else:
				<a href = '/workshops/${mainWorkshop['urlCode']}/${mainWorkshop['url']}'>
					<img src="/images/${mainWorkshop['mainImage_identifier']}/${mainWorkshop['mainImage_directoryNum']}/slideshow/${mainWorkshop['mainImage_hash']}.slideshow" style="max-width: 100%" alt="${mainWorkshop['title']}" title="${mainWorkshop['title']}">
				</a>
			% endif
			<div class="cap">
				<h5>Latest Workshop: ${mainWorkshop['title']}</h5>
				Public Sphere: ${mainWorkshop['publicScopeTitle']}<br>
				Tags: ${mainWorkshop['publicTags']}, ${mainWorkshop['memberTags']}<br>
				<a href="/workshops/${mainWorkshop['urlCode']}/${mainWorkshop['url']}">View Workshop</a>
			</div> <!-- /.cap -->
		</div> <!-- /.civ-img-cap -->
	% else:
                <!--
		<p>
			No featured workshops.
		</p>
                -->
	% endif
</%def>

<%def name="list_workshops()">
    <table>
    <tbody>
    % for item in c.paginator:
        <tr>
        <td>
        % if item['mainImage_hash'] == 'supDawg':
            <a href="/workshops/${item['urlCode']}/${item['url']}"><img src="/images/${item['mainImage_identifier']}/thumbnail/${item['mainImage_hash']}.thumbnail" class="thumbnail" alt="${item['title']}" title="${item['title']}" style="width: 120px; height: 80px;"/></a>
        % else:
            <a href="/workshops/${item['urlCode']}/${item['url']}"><img src="/images/${item['mainImage_identifier']}/${item['mainImage_directoryNum']}/thumbnail/${item['mainImage_hash']}.thumbnail" alt="${item['title']}" title="${item['title']}" class="thumbnail left" style = "width: 120px; height: 80px;"/></a>
        % endif
        </td>
        <td>
            <ul class="unstyled">
            <li><h4><a href="/workshops/${item['urlCode']}/${item['url']}">${item['title']}</a></h4></li>
            <li>Public Sphere: ${item['publicScopeTitle']}</li>
            <li><span class="badge badge-info" alt="Suggestions in workshop" title="Suggestions in workshop"><i class="icon-white icon-pencil"></i> ${len(getActiveSuggestionsForWorkshop(item['urlCode'], item['url']))}</span> <span class="badge badge-info" alt="Information resources in workshop" title="Information resources in workshop"><i class="icon-white icon-book"></i> ${len(getResourcesByWorkshopID(item.id))}</span> <span class="badge badge-success" alt="Following workshop" title="Following workshop"><i class="icon-white icon-user"></i> ${len(getWorkshopFollowers(item.id))}</span> <span class="badge badge-success" alt="Adopted Suggestions in workshop" title="Adopted Suggestions in workshop"><i class="icon-white icon-heart"></i> ${len(getAdoptedSuggestionsForWorkshop(item['urlCode'], item['url']))}</span></li>
            <li>Ends: <span class="old">${timeUntil(item['endTime'])}</span> from now</li>
            </ul>
        </td>
        </tr>
    % endfor
    </tbody>
    </table>
</%def>

<%def name="list_total_workshops()">
	<% state = True %>
	% for p in c.paginator:
	    <% state = not state %>
	% endfor
	Total Workshops: ${c.count} | View ${ c.paginator.pager('~3~') }
</%def>

<%def name='list_news()'>
	##<ul class="unstyled civ-col-list">
		##<li>
			##<img src="/home/evante/civinomics/civinomics-bootstrap/bootstrapped/bootstrap with docs/docs/assets/img/bird.png" width="30">
			##<a href="#">Bird</a> did something with another animal.
		##</li>
	##</ul>
</%def>
