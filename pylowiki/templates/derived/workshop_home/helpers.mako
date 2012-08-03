<%!
    import datetime
    from pylowiki.lib.db.user import getUserByID
    from pylowiki.lib.db.facilitator import isFacilitator
    from pylowiki.lib.db.discussion import getDiscussionByID
    from pylowiki.lib.db.resource import getResourcesByParentID
    from pylowiki.lib.db.flag import getFlags
    from pylowiki.lib.fuzzyTime import timeSince, timeUntil
%>

<%def name="at_a_glance()">
    <p><strong>Goals</strong>: ${c.w['goals']}</p>
    <p><strong>Tags</strong>: ${c.w['publicTags']}, ${c.w['memberTags']}</p>
    <p><strong>Public Sphere</strong>: ${c.w['publicScopeTitle']}</p>

        % if c.w['startTime'] != '0000-00-00': 
	     <p><strong>Started:</strong> <span class="recent">${timeSince(c.w['startTime'])}</span> ago<br />
	     <strong>Ends:</strong> <span class="old">${timeUntil(c.w['endTime'])}</span> from now</p>
        % else:
	     <p><strong>Started:</strong> <span class="recent">Not yet published.</span> ago<br />
	     <strong>Ends:</strong> <span class="old">Not yet published.</span> from now</p>
        % endif

    <p><span class="badge badge-success"><i class="icon-white icon-pencil"></i>${len(c.suggestions)}</span> <span class="badge badge-success"><i class="icon-white icon-book"></i>${len(c.resources)}</span> <span class="badge badge-info"><i class="icon-white icon-user"></i>${len(c.followers)}</span></p>
    <p><strong>Participants</strong>: ${len(c.participants)}</p>

    % if not c.isFacilitator:
	    % if c.isFollowing:
		    <button class="btn btn-primary followButton following" rel="workshop_${c.w['urlCode']}_${c.w['url']}">Following</button>
		% else:
			<button class="btn btn-primary followButton" rel="workshop_${c.w['urlCode']}_${c.w['url']}">Follow</button>
		% endif
	% endif
</%def>

<%def name="facilitate()">
    % if c.isAdmin or c.isFacilitator:
	    <div class="pull-right dropdown" id="workshop_config">
	    	<a class="dropdown-toggle" data-toggle="dropdown" href="#workshop_config">
	    		<img src="/images/glyphicons_pro/glyphicons/png/glyphicons_019_cogwheel.png" height="12" width="12">
	    	</a>
	    	<ul class="dropdown-menu normal">
	    		<li>
	    			<a href = "/workshop/${c.w['urlCode']}/${c.w['url']}/addImages">Add slideshow images</a>
	    		</li>
	    		<li>
	    			<a href = "/workshop/${c.w['urlCode']}/${c.w['url']}/editSlideshow">Edit slideshow</a>
	    		</li>
	    		<li>
	    			<a href = "/workshop/${c.w['urlCode']}/${c.w['url']}/configure">Configure workshop</a>
	    		</li>
	    		<li>
	    			<a href = "/workshop/${c.w['urlCode']}/${c.w['url']}/admin">Admin workshop</a>
	    		</li>
	    	</ul>
	    </div>
    % endif
</%def>

<%def name="list_suggestions()">
	% if c.suggestions == None or len(c.suggestions) == 0:
		<p>No suggestions.</p>
	% else:
		<div class="civ-col-list">
                <table>
                <tbody>
		<% counter = 1 %>
		% for suggestion in c.suggestions:
                        <tr>
                        <td colspan=3>
			<% author = getUserByID(suggestion.owner) %>
			<% discussion = getDiscussionByID(suggestion['discussion_id']) %>
                        <% flags = getFlags(suggestion) %>
                        <% resources = getResourcesByParentID(suggestion.id) %>
                        <h3>
                        <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${suggestion['urlCode']}/${suggestion['url']}">${suggestion['title']}</a>
                        </h3>
                        ${suggestion['suggestionSummary']}
                        </td>
                        </tr>
                        <tr>
                        <td valign="top">
                        % if author['pictureHash'] == 'flash':
                            <a href="/profile/${author['urlCode']}/${author['url']}"><img src="/images/avatars/flash.profile" style="width:30px;" class="thumbnail" alt="${author['name']}" title="${author['name']}"></a>
                        % else:
                            <a href="/profile/${author['urlCode']}/${author['url']}"><img src="/images/avatar/${author['directoryNumber']}/profile/${author['pictureHash']}.profile" class="thumbnail" style="width:30px;" alt="${author['name']}" title="${author['name']}"></a>
                        % endif
                        </td>
                        <td valign="top">
                            <i class="icon-pencil"></i><a href="/profile/${author['urlCode']}/${author['url']}">${author['name']}</a><br>
                            <span class="badge badge-info"><i class="icon-white icon-book"></i>${len(resources)}</span> <span class="badge badge-info"><i class="icon-white icon-comment"></i>${discussion['numComments']}</span> <span class="badge badge-important"><i class="icon-white icon-flag"></i>${len(flags)}</span>
                        </td>
                        <td valign="top">

                            % if 'user' in session:
                                <div id="ratings${counter}" class="rating">
                                    <div id="overall_slider" class="ui-slider-container clearfix">
            			    % if suggestion.rating:
                                        <div id="${suggestion['urlCode']}_${suggestion['url']}" class="small_slider" data1="0_${suggestion['urlCode']}_${suggestion.rating['rating']}_overall_true_rateSuggestion" data2="${suggestion['url']}"></div>
                                    % else:
                                        <div id="${suggestion['urlCode']}_${suggestion['url']}" class="small_slider" data1="0_${suggestion['urlCode']}_0_overall_false_rateSuggestion" data2="${suggestion['url']}"></div>
                                    % endif
                                    </div> <!-- /#overall_slider -->
                                </div> <!-- /#ratings${counter} -->
                            % endif
                            </td>
                            </tr>
                            <tr>
                            <td colspan=3>
                	        <i class="icon-time"></i> <span class="recent">${timeSince(suggestion.date)}</span> ago | <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${suggestion['urlCode']}/${suggestion['url']}">Leave a comment</a>
                             </td>
                             </tr>
                             <tr><td colspan=3><hr></td></tr>
			<% counter += 1 %>
		% endfor
                </tbody>
                </table>
		</div>
	% endif
</%def>

<%def name="info_and_feedback()">
	% if c.discussion['numComments'] == 1:
		<% commentString = 'comment' %>
	% else:
		<% commentString = 'comments' %>
	% endif
	<p>
		<a href = "/workshop/${c.w['urlCode']}/${c.w['url']}/feedback">Learn more</a> about the workshop and facilitation process.
	</p>
	<p>
		<a href = "/workshop/${c.w['urlCode']}/${c.w['url']}/feedback">${c.discussion['numComments']} ${commentString}</a> | <a href = "/workshop/${c.w['urlCode']}/${c.w['url']}/feedback">Give feedback</a>
	</p>
</%def>

