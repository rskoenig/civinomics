<%!
    import datetime
    from pylowiki.lib.db.user import getUserByID
    from pylowiki.lib.db.facilitator import isFacilitator
    from pylowiki.lib.db.discussion import getDiscussionByID
    from pylowiki.lib.db.comment import getFlaggedDiscussionComments
    from pylowiki.lib.db.resource import getResourcesByParentID
    from pylowiki.lib.db.flag import getFlags
    from pylowiki.lib.fuzzyTime import timeSince, timeUntil
%>

<%def name="at_a_glance()">
    <% numComments = 0 %>
    <% numFlags = 0 %>
    % for item in c.resources:
        <% d = getDiscussionByID(item['discussion_id']) %>
        <% cF = getFlaggedDiscussionComments(d.id) %>
        % if cF:
            <% numFlags = numFlags + len(cF) %>
        % endif
        <% numComments = numComments + int(d['numComments']) %>
        <% nF = getFlags(item.id) %>
        % if nF:
            <% numFlags = numFlags + len(nF) %>
        % endif
    % endfor
    % for item in c.suggestions:
        <% d = getDiscussionByID(item['discussion_id']) %>
        <% cF = getFlaggedDiscussionComments(d.id) %>
        % if cF:
            <% numFlags = numFlags + len(cF) %>
        % endif
        <% numComments = numComments + int(d['numComments']) %>
        <% sResources = getResourcesByParentID(item.id) %>
        <% nF = getFlags(item.id) %>
        % if nF:
            <% numFlags = numFlags + len(nF) %>
        % endif
        % for sR in sResources:
           <% d = getDiscussionByID(sR['discussion_id']) %>
           <% cF = getFlaggedDiscussionComments(d.id) %>
           % if cF:
               <% numFlags = numFlags + len(cF) %>
           % endif
           <% numComments = numComments + int(d['numComments']) %>
           <% nF = getFlags(sR.id) %>
           % if nF:
               <% numFlags = numFlags + len(nF) %>
           % endif
        % endfor
    % endfor
    <% numComments = numComments + int(c.discussion['numComments']) %>
    <% cF = getFlaggedDiscussionComments(c.discussion.id) %>
    % if cF:
        <% numFlags = numFlags + len(cF) %>
    % endif
        
    <div class="container-fluid well" style="border:1px solid;">
    <table>
    <thead>
    <tr>
    <td><img src="/images/glyphicons_pro/glyphicons/png/glyphicons_019_cogwheel.png"></td><td><strong>Name</strong>: ${c.w['title']}</td>
    </tr>
    <tr><td>&nbsp;</td></tr>
    <tr>
    <td><img src="/images/glyphicons_pro/glyphicons/png/glyphicons_025_binoculars.png"></td><td><strong>Goals</strong>: ${c.w['goals']}</td>
    </tr>
    <tr><td>&nbsp;</td></tr>
    <tr>
    <td><img src="/images/glyphicons_pro/glyphicons/png/glyphicons_066_tags.png"></td><td><strong>Tags</strong>: ${c.w['publicTags']}, ${c.w['memberTags']}</td>
    </tr>
    <tr><td>&nbsp;</td></tr>
    <tr>
    <td><img src="/images/glyphicons_pro/glyphicons/png/glyphicons_340_globe.png"></td><td><strong>Public Sphere</strong>: ${c.w['publicScopeTitle']}</td>
    </tr>
    <tr><td>&nbsp;</td></tr>
    <tr>
    <td><img src="/images/glyphicons_pro/glyphicons/png/glyphicons_054_clock.png"></td>

    % if c.w['startTime'] != '0000-00-00': 
        <td><strong>Started:</strong> <span class="recent">${timeSince(c.w['startTime'])}</span> ago<br />
        <strong>Ends:</strong> <span class="old">${timeUntil(c.w['endTime'])}</span> from now</td>
    % else:
        <td><strong>Started:</strong> <span class="recent">Not yet started.</span><br />
        <strong>Ends:</strong> <span class="old">Not yet started.</span></td>
    % endif
    <tr><td>&nbsp;</td></tr>
    </tr>
    <tr>
    <td><img src="/images/glyphicons_pro/glyphicons/png/glyphicons_280_settings.png"></td>
    <td><strong>Activity</strong>: <span class="badge badge-success"><i class="icon-white icon-pencil"></i>${len(c.suggestions)}</span> &nbsp; <span class="badge badge-success"><i class="icon-white icon-book"></i>${len(c.resources)}</span> &nbsp; <span class="badge badge-success"><i class="icon-white icon-comment"></i>${numComments}</span> &nbsp; <span class="badge badge-info"><i class="icon-white icon-user"></i>${len(c.followers)}</span> &nbsp; <span class="badge badge-important"><i class="icon-white icon-flag"></i>${numFlags}</span></td>
    </tr>
    <tr><td>&nbsp;</td></tr>
    <tr>
    % if len(c.facilitators) == 1:
        <% fTitle = "Facilitator" %>
    % else:
        <% fTitle = "Facilitators" %>
    % endif

    <td><img src="/images/glyphicons_pro/glyphicons/png/glyphicons_029_notes_2.png"></td><td><table><thead><tr><td><strong>${fTitle}</strong>:</td>
                <td>&nbsp;&nbsp;</td>
                % for facilitator in c.facilitators:
                        <td>
                        <% fuser = getUserByID(facilitator.owner) %>
                        % if fuser['pictureHash'] == 'flash':
                            <a href="/profile/${fuser['urlCode']}/${fuser['url']}"><img src="/images/avatars/flash.thumbnail" alt="${fuser['name']}" title="${fuser['name']}" class="thumbnail"></a>
                        % else:
                            <a href="/profile/${fuser['urlCode']}/${fuser['url']}"><img src="/images/avatar/${fuser['directoryNumber']}/thumbnail/${fuser['pictureHash']}.thumbnail" alt="${fuser['name']}" title="${fuser['name']}" class="thumbnail"></a>
                        % endif
                        </td>
                        <td>&nbsp;&nbsp;</td>
                %endfor
                </tr>
                </thead>
                </table>
    </td>
    </tr>
    <tr><td>&nbsp;</td></tr>
    </thead>
    </table>
    <br /><br />
    % if not c.isFacilitator:
	    % if c.isFollowing:
		    <button class="btn btn-primary followButton following" rel="workshop_${c.w['urlCode']}_${c.w['url']}">Following</button>
		% else:
			<button class="btn btn-primary followButton" rel="workshop_${c.w['urlCode']}_${c.w['url']}">Follow</button>
		% endif
	% endif
    </div><!-- container-fluid -->
</%def>

<%def name="motd()">
    % if c.motd:
        <h2 class="civ-col"><i class="icon-list-alt"></i> Facilitator Message</h2>
        <p>${c.motd['data']}</p>
    % endif
</%def>

<%def name="info_and_feedback()">
	<p>
		<a href = "/workshop/${c.w['urlCode']}/${c.w['url']}/feedback">Learn more</a> about the workshop and facilitation process.
	</p>
	<p>
		<a href = "/workshop/${c.w['urlCode']}/${c.w['url']}/feedback"><span class="badge badge-info"><i class="icon-white icon-comment"></i>${c.discussion['numComments']}</span></a> | <a href = "/workshop/${c.w['urlCode']}/${c.w['url']}/feedback">Give feedback</a>
	</p>
</%def>

