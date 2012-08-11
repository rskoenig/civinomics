<%!
    from pylowiki.lib.db.user import getUserByID, isAdmin
    from pylowiki.lib.db.facilitator import isFacilitator
    from pylowiki.lib.fuzzyTime import timeSince

    import logging
    log = logging.getLogger(__name__)
%>

<%def name='spacer()'>
    ## A spacer
    <div class="row-fluid">
        <br />
    </div>
</%def>

<%def name='inlineSpacer(amount)'>
    <div class="span${amount}">
        <p></p>
    </div>
</%def>

<%def name="workshopTitle()">
    <h1><a href = "/workshop/${c.w['urlCode']}/${c.w['url']}">${c.w['title']}</a></h1>
</%def>

<%def name="showTitle(title)">
    <h1 style="text-align:center;">${title}</h1>
</%def>

<%def name="suggestionInfo()">
    <% author = getUserByID(c.s.owner) %>
    % if isAdmin(c.s.owner):
       <% uTitle = ' (Admin)' %>
    % elif isFacilitator(c.s.owner, c.w.id):
       <% uTitle = ' (Facilitator)' %>
    % else:
       <% uTitle = '' %>
    % endif
    <h3><a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${c.s['urlCode']}/${c.s['url']}">${c.s['title']}</a></h3>
    <ul class="unstyled civ-col-list">
    <li class="post">
    % if author['pictureHash'] == 'flash':
        <a href="/profile/${author['urlCode']}/${author['url']}"><img src="/images/avatars/flash.thumbnail" alt="${author['name']}" title="${author['name']}" class="thumbnail" style="width:30px;}"/></a>
    % else:
        <a href="/profile/${author['urlCode']}/${author['url']}"><img src="/images/avatar/${author['directoryNumber']}/thumbnail/${author['pictureHash']}.thumbnail" lt="${author['name']}" title="${author['name']}" class="thumbnail"/></a>
    % endif
            &nbsp;By <a href="/profile/${author['urlCode']}/${author['url']}">${author['name']}</a>${uTitle} <span class="recent">${timeSince(c.lastmoddate)}</span> ago</li>
    </li>
    <ul>
</%def>

<%def name="suggestionContent(content)">
    <p>
        ${content}
    </p>
</%def>

<%def name="suggestionEditAdminRating(cAuthuser, cwOwner, cs, cIsAdmin, session, cRating)">
    <div class="row">
        <div class="span4 offset4">
            <table>
                <tbody>
                    <tr>
                        <td>
                            % if cAuthuser and (cAuthuser.id == cwOwner or cIsAdmin):
                                <a href="/modSuggestion/${cs['urlCode']}/${cs['url']}">admin suggestion</a>&nbsp;&nbsp;
                            % endif
                        </td>
                        <td>
                            % if cAuthuser and (cAuthuser.id == csOwner or cIsAdmin):
                                <a href="/editSuggestion/${cs['urlCode']}/${cs['url']}">edit suggestion</a>
                            % endif
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2">
                            % if "user" in session:
                                % if cRating:
                                    <div class = "gray rating wide">
                                        <div id="overall_slider" class="ui-slider-container">
                                            <div id="${cs['urlCode']}_${cs['url']}" class="normal_slider" data1="0_${cs['urlCode']}_${cRating['rating']}_overall_true_rateSuggestion" data2="${cs['url']}"></div>
                                        </div>
                                    </div>
                                % else:
                                    <div class = "gray rating wide">
                                        <div id="overall_slider" class="ui-slider-container">
                                            <div id="${cs['urlCode']}_${cs['url']}" class="normal_slider" data1="0_${cs['urlCode']}_0_overall_false_rateSuggestion" data2="${cs['url']}"></div>
                                        </div>
                                    </div>
                                % endif
                            % endif
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</%def>

<%def name="showSuggestions()">
    % if len(c.resources) < 3:
        <h2 class="civ-col"><i class="icon-pencil"></i> Other Suggestions</h2>
        <ul id="show_suggestions" class="unstyled civ-col-list">
        % if len(c.suggestions) == 0:
            <li>
                No suggestions!
            </li>
        % else:
            % for suggestion in c.suggestions:
                <% author = getUserByID(suggestion.owner)%>
                <li class="post">
                    <strong class="issue_name"><a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${suggestion['urlCode']}/${suggestion['url']}">${suggestion['title']}</a></strong>
                    <br />
                    % if author['pictureHash'] == 'flash':
                        <a href="/profile/${author['urlCode']}/${author['url']}"><img src="/images/avatars/flash.thumbnail" lt="${author['name']}" title="${author['name']}" class="thumbnail" style="width:30px;}"/></a>
                    % else:
                        <a href="/profile/${author['urlCode']}/${author['url']}"><img src="/images/avatar/${author['directoryNumber']}/thumbnail/${author['pictureHash']}.thumbnail" lt="${author['name']}" title="${author['name']}" class="thumbnail"/></a>
                    % endif
                    &nbsp;By <a href="/profile/${author['urlCode']}/${author['url']}">${author['name']}</a>
                </li>
            % endfor
        % endif
        </ul> <!-- show_suggestion -->
    % endif <!-- resources less than 3 -->
</%def>

<%def name="showResources()">
        <h2 class="civ-col"><i class="icon-book"></i> Suggestion Resources <span class="pull-right"><a href="/newSResource/${c.s['urlCode']}/${c.s['url']}" title="Add a resource with information about this suggestion"><i class="icon-plus"></i></a></span></h2>
	% if len(c.resources) == 0:
		<div class="alert alert-warning">
			No information resources for this suggestion found. Be the first to add one!
		</div> <!-- /.alert.alert-danger -->
	% else:
		<ul class="unstyled civ-col-list">
		% for resource in c.resources:
			<% author = getUserByID(resource.owner) %>
			% if resource['type'] == "post":
				<li class="post">
					<h3>
						<a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${resource['urlCode']}/${resource['url']}">
							${resource['title']}
						</a>
					</h3>
					<p>
						<i class="icon-book"></i>${resource['comment'][:40]}...<a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${resource['urlCode']}/${resource['url']}">more</a></p>
					<p>
                                         % if author['pictureHash'] == 'flash':
                                             <a href="/profile/${author['urlCode']}/${author['url']}"><img src="/images/avatars/flash.profile" style="width:30px;" class="thumbnail" alt="${author['name']}" title="${author['name']}"></a>
                                         % else:
                                             <a href="/profile/${author['urlCode']}/${author['url']}"><img src="/images/avatar/${author['directoryNumber']}/profile/${author['pictureHash']}.profile" class="thumbnail" style="width:30px;" alt="${author['name']}" title="${author['name']}"></a>
                                         % endif

						&nbsp;by <a href="/profile/${author['urlCode']}/${author['url']}">${author['name']}</a>
						<span class="old">${timeSince(resource.date)}</span> ago
					</p>
				</li>
			% endif
		% endfor
		</ul>
	% endif
</%def>
