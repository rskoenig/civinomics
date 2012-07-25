<%! 
   from pylowiki.lib.db.suggestion import getSuggestionsForWorkshop
   from pylowiki.lib.db.follow import getWorkshopFollowers
   from pylowiki.lib.db.geoInfo import getGeoInfo
   from pylowiki.lib.db.tag import getPublicTagCount, getMemberTagCount
   from pylowiki.lib.fuzzyTime import timeUntil
%>
<%namespace file="/lib/mako_lib.mako" name="lib" />

<%def name="featured_workshop()">
	% if len(c.list) > 0 and c.list[0]['urlCode'] == c.paginator[0]['urlCode'] and c.action == 'sitemapIssues':
		<div class="civ-img-cap">
		    <% mainWorkshop = c.paginator.pop() %>
		    % if mainWorkshop['mainImage_hash'] == 'supDawg':
		        <a href = '/workshops/${mainWorkshop['urlCode']}/${mainWorkshop['url']}'>
				    <img src="/images/${mainWorkshop['mainImage_identifier']}/slideshow/${mainWorkshop['mainImage_hash']}.slideshow" style="max-width: 100%">
				</a>
			% else:
				<a href = '/workshops/${mainWorkshop['urlCode']}/${mainWorkshop['url']}'>
					<img src="/images/${mainWorkshop['mainImage_identifier']}/${mainWorkshop['mainImage_directoryNum']}/slideshow/${mainWorkshop['mainImage_hash']}.slideshow" style="max-width: 100%">
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
	<ul class="unstyled civ-col-list">
		% for item in c.paginator:
			<li>
                % if item['mainImage_hash'] == 'supDawg':
                    <a href="/workshops/${item['urlCode']}/${item['url']}"><img src="/images/${item['mainImage_identifier']}/thumbnail/${item['mainImage_hash']}.thumbnail" alt="mtn" style="width: 120px; height: 80px;"/></a>
                % else:
                    <a href="/workshops/${item['urlCode']}/${item['url']}"><img src="/images/${item['mainImage_identifier']}/${item['mainImage_directoryNum']}/thumbnail/${item['mainImage_hash']}.thumbnail" alt="mtn" class="left" style = "width: 120px; height: 80px;"/></a>
                % endif
                <h4><a href="/workshops/${item['urlCode']}/${item['url']}">${item['title']}</a></h4>
                Public Sphere: ${item['publicScopeTitle']}<br>
                Suggestions: ${len(getSuggestionsForWorkshop(item['urlCode'], item['url']))}<br>
                Followers: ${len(getWorkshopFollowers(item.id))}<br>
                Ends: <span class="old">${timeUntil(item['endTime'])}</span> from now
			</li>
		% endfor
	</ul> <!-- /.civ-col-list -->
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
