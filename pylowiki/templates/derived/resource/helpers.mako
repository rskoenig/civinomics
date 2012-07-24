<%!
	from pylowiki.lib.fuzzyTime import timeSince
	from pylowiki.lib.db.user import getUserByID
%>

<%def name="displayType()">
	Resource &mdash; ${c.resource['type']}
</%def>

<%def name="displayRating()">
		<a href="#"><i class="icon-chevron-up"></i></a>
		<div>rating</div>
		<a href="#"><i class="icon-chevron-down"></i></a>
</%def>

<%def name="displayMetaData()">
	<h3><a href="${c.resource['link']}" target="_blank" alt="${c.resource['title']}">${c.resource['title']}</a></h3>
	(${c.resource['domain']}.${c.resource['tld']})
	<br>
	Posted <span class="recent">${timeSince(c.resource.date)}</span> by <a href="/profile/${c.poster['urlCode']}/${c.poster['url']}">${c.poster['name']}</a>
</%def>

<%def name="displayResourceComment()">
	<div id="resource-comment">
		<p>${c.resource['comment']}</p>
	</div>
</%def>

<%def name="displayResource()">
	<div class="span1 civ-votey">
		${displayRating()}
	</div> <!-- .span1.civ-votey -->

	<div class="span11">
		<div class="row-fluid">
			<div class="span12">
				${displayMetaData()}
			</div>
		</div>

		<div class="row-fluid resource-comment">
			<div class="span12">
				${displayResourceComment()}
			</div> <!-- .span12 -->
		</div> <!-- .row-fluid -->
	</div> <!-- /.span11 -->
</%def>

<%def name="displayOtherResources()">
	% if len(c.otherResources) == 0:
		<div class="alert alert-danger">
			No other resources found.
		</div> <!-- /.alert.alert-danger -->
	% else:
		<ul class="unstyled civ-col-list">
		% for resource in c.otherResources:
			<% author = getUserByID(resource.owner) %>
			% if resource['type'] == "post":
				<li class="post">
					<h3>
						<a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${resource['urlCode']}/${resource['url']}">
							${resource['title']}
						</a>
					</h3>
					<p>
						<img src="/images/glyphicons_pro/glyphicons/png/glyphicons_039_notes@2x.png" height="50" width="40" style="float: left; margin-right: 5px;">${resource['comment'][:50]}...
					</p>
					<p><a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${resource['urlCode']}/${resource['url']}">more</a></p>
					<p>
						posted by 
						<a href="/profile/${author['urlCode']}/${author['url']}">${author['name']}</a>
						<span class="old">${timeSince(resource.date)}</span> ago
					</p>
				</li>
			% endif
		% endfor
		</ul>
	% endif
</%def>