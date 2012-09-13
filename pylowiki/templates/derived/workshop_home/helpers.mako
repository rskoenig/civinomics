<%!
    import datetime
    from pylowiki.lib.db.user import getUserByID
    from pylowiki.lib.db.facilitator import isFacilitator
    from pylowiki.lib.db.discussion import getDiscussionByID, getActiveDiscussionsForWorkshop
    from pylowiki.lib.db.comment import getFlaggedDiscussionComments
    from pylowiki.lib.db.resource import getResourcesByParentID
    from pylowiki.lib.db.flag import getFlags
    from pylowiki.lib.fuzzyTime import timeSince, timeUntil
%>
<%namespace file="/lib/mako_lib.mako" name="lib" />

<%def name="at_a_glance()">
    <%
        numComments = 0
        numResources = len(c.resources)
        numFlags = 0
        t = getActiveDiscussionsForWorkshop(c.w['urlCode'], c.w['url'])
        for d in t:
            cF = getFlaggedDiscussionComments(d.id)
            if cF:
                numFlags = numFlags + len(cF)
            
            numComments = numComments + int(d['numComments'])
        
        for item in c.resources:
            d = getDiscussionByID(item['discussion_id'])
            cF = getFlaggedDiscussionComments(d.id)
            if cF:
                numFlags = numFlags + len(cF)
            
            numComments = numComments + int(d['numComments'])
            nF = getFlags(item.id)
            if nF:
                numFlags = numFlags + len(nF)
        
        for item in c.suggestions:
            d = getDiscussionByID(item['discussion_id'])
            cF = getFlaggedDiscussionComments(d.id)
            if cF:
                numFlags = numFlags + len(cF)
            
            numComments = numComments + int(d['numComments'])
            sResources = getResourcesByParentID(item.id)
            numResources = numResources + len(sResources)
            nF = getFlags(item.id)
            if nF:
                numFlags = numFlags + len(nF)
            
            for sR in sResources:
               d = getDiscussionByID(sR['discussion_id'])
               cF = getFlaggedDiscussionComments(d.id)
               if cF:
                   numFlags = numFlags + len(cF)
               
               numComments = numComments + int(d['numComments'])
               nF = getFlags(sR.id)
               if nF:
                   numFlags = numFlags + len(nF)
        
        numComments = numComments + int(c.discussion['numComments'])
        cF = getFlaggedDiscussionComments(c.discussion.id)
        if cF:
            numFlags = numFlags + len(cF)
    %>

    <dl class="dl-horizontal" style="font-size:large;">
    <dt>Name:</dt><dd><strong>${c.w['title']}</strong><br /><br /></dd>
    <dt>Goals:</dt><dd>${c.w['goals']}<br /><br /></dd>
    <dt>Tags:</dt><dd>${c.w['publicTags']}, ${c.w['memberTags']}<br /><br /></dd>
    <dt>Public<br />Sphere:</dt><dd>${c.w['publicScopeTitle']}<br /><br /><br /></dd>
    % if c.w['startTime'] != '0000-00-00': 
        <dt>Started:</dt><dd><span class="recent">${timeSince(c.w['startTime'])}</span> ago</dd>
        <dt>Ends:</dt><dd><span class="old">${timeUntil(c.w['endTime'])}</span> from now<br /><br /></dd>
    % else:
        <dt>Started:</dt><dd><span class="recent">Not yet started.</span><br /></dd>
        <dt>Ends:</dt><dd><span class="old">Not yet started.</span><br /><br /></dd>
    % endif
    <dt>Activity:</dt>
    <dd><span class="badge badge-info" title="Suggestions in workshop"><i class="icon-white icon-pencil"></i>${len(c.suggestions)}</span> <span class="badge badge-info" title="Information resources in workshop"><i class="icon-white icon-book"></i>${numResources}</span> <span class="badge badge-info" title="Discussion topics in workshop"><i class="icon-white icon-folder-open"></i> ${len(t)}</span> <span class="badge badge-info" title="Comments in workshop"><i class="icon-white icon-comment"></i>${numComments}</span> <span class="badge badge-success" title="Workshop followers"><i class="icon-white icon-user"></i>${len(c.followers)}</span> <span class="badge badge-success" title="Adopted suggestions in workshop"><i class="icon-white icon-heart"></i>${len(c.asuggestions)}</span> <span class="badge badge-inverse" title="Flags in workshop"><i class="icon-white icon-flag"></i>${numFlags}</span><br /><br /></dd>

    % if 'user' in session:
        % if c.conf['read_only.value'] == 'true':
            <% pass %>
        % else:
	    <dt>Participate:</dt><dd>
            ${lib.add_a("resource")}
            ${lib.add_a("suggestion")}
            ${lib.add_a("feedback")}
            ${lib.add_a("discussion")}
            % if not c.isFacilitator:
                % if c.isFollowing:
                    <button class="btn btn-primary btn-mini followButton following" rel="workshop_${c.w['urlCode']}_${c.w['url']}" title="Click to follow/unfollow this workshop">+Following</button>
                % else:
                    <button class="btn btn-primary btn-mini followButton" rel="workshop_${c.w['urlCode']}_${c.w['url']}" title="Click to follow/unfollow this workshop">+Follow</button>
                % endif
            % endif 
            <br /><br />
            </dd>
        % endif
    % endif
    % if len(c.facilitators) == 1:
        <% fTitle = "Facilitator" %>
    % else:
        <% fTitle = "Facilitators" %>
    % endif

    <dt>${fTitle}:</dt><dd>
                <table><thead><tr>
                % for facilitator in c.facilitators:
                        <td>
                        <% fuser = getUserByID(facilitator.owner) %>
                        % if fuser['pictureHash'] == 'flash':
                            <a href="/profile/${fuser['urlCode']}/${fuser['url']}"><img src="/images/avatars/flash.thumbnail" alt="${fuser['name']}" title="${fuser['name']}" class="thumbnail"></a> &nbsp; &nbsp;
                        % else:
                            <a href="/profile/${fuser['urlCode']}/${fuser['url']}"><img src="/images/avatar/${fuser['directoryNumber']}/thumbnail/${fuser['pictureHash']}.thumbnail" alt="${fuser['name']}" title="${fuser['name']}" class="thumbnail"></a> &nbsp; &nbsp;
                        % endif
                        </td>
                %endfor
                </tr></thead></table>
                </dd>
    </dl>
    <br /><br />
</%def>

<%def name="motd()">
    % if c.motd:
        <h2 class="civ-col"><i class="icon-list-alt"></i> Facilitator Message</h2>
        <p>${c.motd['data']}</p>
    % endif
</%def>

<%def name="info_and_feedback()">
	<p>
		<a href = "/help">Learn more</a> about the workshop and facilitation process.
	</p>
	<p>
                % if 'user' in session and c.isScoped:
                    <a href = "/workshop/${c.w['urlCode']}/${c.w['url']}/discussion">Give feedback</a> to the workshop Facilitators.
                % endif
	</p>
</%def>
