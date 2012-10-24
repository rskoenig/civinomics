<%!
	from pylowiki.lib.db.facilitator import isFacilitator
%>

<%namespace file="/derived/commentsCustom.mako" import="comments" />

<%def name="summary()">
	% if 'user' in session:
		% if c.conf['read_only.value'] == 'true':
			${c.content}
		% else:
			${h.form(url(controller = "wiki", action ="handler", id1 = c.w['urlCode'], id2 = c.w['url']),method="put")}
			<% counter = 0 %>
			% for row in c.wikilist:
				<div id="wiki-section-break">
				<% numrows = 10 %>
				% if c.authuser.id == c.w.owner or int(c.authuser['accessLevel']) >= 200:
					<table style="width: 100%; padding: 0px; border-spacing: 0px; border: 0px; margin: 0px;"><tr><td>
					<div id = "section${counter}" ondblclick="toggle('textareadiv${counter}', 'edit${counter}', 'edit')">${row[0]}</div>
					</td></tr></table>
				% else:
					<table style="width: 100%; padding: 0px; border-spacing: 0px; border: 0px; margin: 0px;"><tr><td>
					<div id = "section${counter}" >${row[0]}</div>
					</td></tr></table>
				% endif


				<div class="collapse" id="textareadiv${counter}">
					<br />
					<textarea rows="${numrows}" id="textarea${counter}" name="textarea${counter}" onkeyup="previewAjax( 'textarea${counter}', 'section${counter}' )" class="markitup">${row[1]}</textarea>
					<div style="text-align:right; padding-right:35px;">
						<input type="text" id="remark${counter}"  name="remark${counter}" class="text tiny" placeholder="Optional remark"/> 

						${h.submit('submit', 'Save')}
					</div>
				</div>
				% if c.authuser.id == c.w.owner or int(c.authuser['accessLevel']) >= 200:
					<a id="edit${counter}" class="btn btn-mini pull-right" data-toggle="collapse" data-target="#textareadiv${counter}"><i class="icon-edit"></i> edit</a>
				% endif
				
				</div> <!-- /#wiki-section-break -->
				<% counter += 1 %>
			% endfor
			${h.hidden("count",counter)}
			${h.end_form()}
		% endif
	% else:
		${c.content}
	% endif
        Last updated ${c.lastmoddate} by <a href="/profile/${c.lastmoduser['urlCode']}/${c.lastmoduser['url']}">${c.lastmoduser['name']}</a>
</%def>
