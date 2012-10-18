<%! 
   from pylowiki.lib.db.suggestion import getActiveSuggestionsForWorkshop, getAdoptedSuggestionsForWorkshop
   from pylowiki.lib.db.resource import getResourcesByWorkshopID
   from pylowiki.lib.db.discussion import getActiveDiscussionsForWorkshop
   from pylowiki.lib.db.follow import getWorkshopFollowers
   from pylowiki.lib.db.geoInfo import getGeoInfo
   from pylowiki.lib.db.workshop import isScoped
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
            <a href="/workshops/${mainWorkshop['urlCode']}/${mainWorkshop['url']}" title="Click to view workshop" style="color:white"><strong>View Workshop</strong></a>
            </div> <!-- /.cap -->
        </div> <!-- /.civ-img-cap -->
    % else:
        <!--Nothing here-->
    % endif
</%def>

<%def name="list_workshops()">
    <ul class="unstyled civ-col-list">
    % for item in c.paginator:
        <%
            if 'user' in session:
                if isScoped(c.authuser, item):
                    participate = 1
                else:
                    participate = 0
            else:
                participate = 0
        %>
        <li>
        <div class="row-fluid">
            <div class="span3">
        % if item['mainImage_hash'] == 'supDawg':
            <a href="/workshops/${item['urlCode']}/${item['url']}"><img src="/images/${item['mainImage_identifier']}/thumbnail/${item['mainImage_hash']}.thumbnail" class="thumbnail" alt="${item['title']}" title="Click to view ${item['title']}" style="width: 120px; height: 80px;"/></a>
        % else:
            <a href="/workshops/${item['urlCode']}/${item['url']}"><img src="/images/${item['mainImage_identifier']}/${item['mainImage_directoryNum']}/thumbnail/${item['mainImage_hash']}.thumbnail" alt="${item['title']}" title="Click to view ${item['title']}" class="thumbnail left" style = "width: 120px; height: 80px;"/></a>
        % endif
            </div><!-- span3 -->
            <div class="span9">
            <h4><a href="/workshops/${item['urlCode']}/${item['url']}" title="Click to view ${item['title']}">${item['title']}</a></h4>
            Public Sphere: ${item['publicScopeTitle']}
            % if participate and participate == 1:
                <span class="pull-right label label-success"><a href="/workshops/${item['urlCode']}/${item['url']}" style="color:white;text-decoration:none;" title="This workshop is within your Public Sphere. Click to participate!">Participate!</a></span>
            % else:
                % if 'user' not in session:
                    <span class="pull-right label label-success"><a href="/" style="color:white;text-decoration:none;" title="This workshop is within your Public Sphere. Click to participate!" target="_blank">Participate!</a></span>
                % endif
            % endif
            <br />
            <span class="badge badge-info" alt="Suggestions in workshop" title="Suggestions in workshop"><i class="icon-white icon-pencil"></i> ${len(getActiveSuggestionsForWorkshop(item['urlCode'], item['url']))}</span> <span class="badge badge-info" alt="Information resources in workshop" title="Information resources in workshop"><i class="icon-white icon-book"></i> ${len(getResourcesByWorkshopID(item.id))}</span> <span class="badge badge-info" alt="Discussion topics in workshop" title="Discussion topics in workshop"><i class="icon-white icon-folder-open"></i> ${len(getActiveDiscussionsForWorkshop(item['urlCode'], item['url']))}</span> <span class="badge badge-success" alt="Following workshop" title="Following workshop"><i class="icon-white icon-user"></i> ${len(getWorkshopFollowers(item.id))}</span> <span class="badge badge-success" alt="Adopted Suggestions in workshop" title="Adopted Suggestions in workshop"><i class="icon-white icon-heart"></i> ${len(getAdoptedSuggestionsForWorkshop(item['urlCode'], item['url']))}</span><br />
            % if item['endTime'] == '0000-00-00':
                Not started yet<br />
            % else:
                Ends: <span class="old">${timeUntil(item['endTime'])}</span> from now<br />
            % endif
        </div><!-- span9 -->
        </div><!-- row-fluid -->
        </li>
    % endfor
    </ul>
</%def>

<%def name="list_total_workshops()">
    <%
        state = True
        for p in c.paginator:
            state = not state
    %>
	Total Workshops: ${c.count} | View ${ c.paginator.pager('~3~') }
</%def>

<%def name='surveys()'>
    <h2 class="civ-col">Surveys</h2>
    <div class="civ-col-inner">
        <div class="well" style="background-color:#40A361;">
            <a href="/surveys" style="color:white;" title="Click to view and participate in surveys"><img src="/images/glyphicons_pro/glyphicons/png/glyphicons_029_notes_2.png"> View Surveys</a>
        </div><!-- well -->
    </div><!-- civ-col-inner -->
</%def>


<%def name='list_news()'>
	## This seems to be deprecated
</%def>
