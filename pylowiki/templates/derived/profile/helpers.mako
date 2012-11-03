<%!
    from pylowiki.lib.db.suggestion import getSuggestionByID, getSuggestion
    from pylowiki.lib.db.resource import getResource
    from pylowiki.lib.db.workshop import getWorkshop, getWorkshopsByOwner, getWorkshopByID, getWorkshopPostsSince
    from pylowiki.lib.db.facilitator import isFacilitator, isPendingFacilitator
    from pylowiki.lib.db.user import isAdmin, getUserPosts
    from pylowiki.lib.db.activity import getMemberPosts
    from pylowiki.lib.db.discussion import getDiscussionByID
    from pylowiki.lib.db.flag import getFlags
    from pylowiki.lib.fuzzyTime import timeSince
    import textwrap
%>


<%def name="iconPath()">
  /images/glyphicons_pro/glyphicons/png/
</%def>

<%def name="displayProfilePicture()">
        <% 
            if c.revision:
                pictureHash = c.revision['pictureHash']
                name = c.revision['data']
                directoryNumber = c.revision['directoryNumber']
            else:
                pictureHash = c.user['pictureHash']
                name = c.user['name']
                if pictureHash != 'flash':
                  directoryNumber = c.user['directoryNumber']
         %>

        % if pictureHash == 'flash':
            <img src="/images/avatars/flash.profile" alt="${name}" title="${name}" class="thumbnail" style="display: block; margin-left: auto; margin-right: auto;">
        % else:
            <img src="/images/avatar/${directoryNumber}/profile/${pictureHash}.profile" alt="${name}" title="${name}" class="thumbnail" style="display: block; margin-left: auto; margin-right: auto;">
        % endif
        </li>
        </ul>
</%def>

<%def name="listUser(user, wide)">
    <%
      if wide == 1:
          pixels = 60
          maxlen = 40
      else:
          pixels = 30
          maxlen = 20
    %>
    <li>
    <div class="row-fluid">
        <div class="span3">
            <ul class="unstyled">
            <li>
                % if user['pictureHash'] == 'flash':
                    <a href="/profile/${user['urlCode']}/${user['url']}"><img src="/images/avatars/flash.profile" style="width:${pixels}px;" alt="Click to view profile of member ${user['name']}" title="Click to view profile of member ${user['name']}" class="thumbnail"/></a>
         % else:
                <a href="/profile/${user['urlCode']}/${user['url']}"><img src="/images/avatar/${user['directoryNumber']}/profile/${user['pictureHash']}.profile" style="width:${pixels}px;" alt="Click to view profile of member ${user['name']}" title="Click to view profile of member ${user['name']}" class="thumbnail"/></a>
         % endif
           </li>
           </ul>
        </div><!-- span2 -->
        <div class="span9">
            <% mList = getMemberPosts(user, 1) %>
            % if mList:
               <% mObj = mList[0] %>
           % else:
               <% mObj = False %>
           %endif 
           <a href="/profile/${user['urlCode']}/${user['url']}" title="Click to view profile of member ${user['name']}">${user['name']}</a><br />
           % if mObj:
               % if mObj.objType == 'comment':
                   <% ooTitle = "New Comment" %>
                   <% oLink = "/comment/" + mObj['urlCode'] %>
                   <% oiType = "comment" %>
                   <% d = getDiscussionByID(mObj['discussion_id']) %>
                   <% w = getWorkshop(d['workshopCode'], d['workshopURL']) %>
                   <% wLink = "/workshop/" + d['workshopCode'] + "/" + d['workshopURL'] %>
                   <% parentTitle = d['discType'] %>
                   <% ooLink = "foo" %>
                   <% ooiType = "comment" %>

                   % if d['discType'] == 'background':
                       <% ooLink = "/workshop/" + d['workshopCode'] + "/" + d['workshopURL'] + "/background" %>
                       <% ooTitle = "Workshop Background" %>
                       <% ooiType = "comment" %>
                   % elif d['discType'] == 'suggestion':
                       <% s = getSuggestion(d['suggestionCode'], d['suggestionURL']) %>
                       <% ooTitle = s['title'] %>
                       <% ooLink = "/workshop/" + d['workshopCode'] + "/" + d['workshopURL'] + "/suggestion/" + d['suggestionCode'] + "/" + d['suggestionURL'] %>
                       <% ooiType = "pencil" %>
                   % elif d['discType'] == 'general':
                       <% ooTitle = d['title'] %>
                       <% ooLink = "/workshop/" + d['workshopCode'] + "/" + d['workshopURL'] + "/discussion/" + d['urlCode'] + "/" + d['url'] %>
                       <% ooiType = "folder-open" %>
                   % elif d['discType'] == 'resource':
                       <% r = getResource(d['resourceCode'], d['resourceURL']) %>
                       <% ooTitle = r['title'] %>
                       <% ooLink = "/workshop/" + d['workshopCode'] + "/" + d['workshopURL'] + "/resource/" + d['resourceCode'] + "/" + d['resourceURL'] %>
                       <% ooiType = "book" %>
                   % elif d['discType'] == 'sresource':
                       <% r = getResource(d['resourceCode'], d['resourceURL']) %>
                       <% ooTitle = r['title'] %>
                       <% ooLink = "/workshop/" + d['workshopCode'] + "/" + d['workshopURL'] + "/resource/" + d['resourceCode'] + "/" + d['resourceURL'] %>

                   % endif
               % elif mObj.objType == 'resource':
                   <% w = getWorkshopByID(mObj['workshop_id']) %>
                   <% oLink = "/workshop/" + w['urlCode'] + "/" + w['url'] + "/resource/" + mObj['urlCode'] + "/" + mObj['url'] %>
                   <% wLink = "/workshop/" + w['urlCode'] + "/" + w['url'] %>
                   <% oiType = "book" %>
               % elif mObj.objType == 'suggestion':
                   <% oiType = "pencil" %>
                   <% oLink = "/workshop/" + mObj['workshopCode'] + "/" + mObj['workshopURL'] + "/suggestion/" + mObj['urlCode'] + "/" + mObj['url'] %>
                   <% wLink = "/workshop/" + mObj['workshopCode'] + "/" + mObj['workshopURL'] %>
                   <% w = getWorkshop(mObj['workshopCode'], mObj['workshopURL']) %>
               % elif mObj.objType == 'discussion':
                   <% oiType = "comment" %>
                   <% oLink = "/workshop/" + mObj['workshopCode'] + "/" + mObj['workshopURL'] + "/discussion/" + mObj['urlCode'] + "/" + mObj['url'] %>
                   <% wLink = "/workshop/" + mObj['workshopCode'] + "/" + mObj['workshopURL'] %>
                   <% w = getWorkshop(mObj['workshopCode'], mObj['workshopURL']) %>
               % endif
               %if len(w['title']) > maxlen:
                   <% wTitle = w['title'][0:(maxlen - 4)] + '...' %>
               %else:
                   <% wTitle = w['title'] %>
               %endif

               %if mObj.objType == 'comment':
                   %if ooTitle and len(ooTitle) > maxlen:
                       <% ooTitle = ooTitle[0:(maxlen - 4)] + '...' %>
                   %endif:
                   %if len(mObj['data']) > maxlen:
                       <% oTitle = mObj['data'][0:(maxlen - 4)] + '...' %>
                   %else:
                       <% oTitle = mObj['data'] %>
                   %endif
                   New <a href="${oLink}" title="Click to view new ${mObj.objType}"><i class="icon-${oiType}"></i> ${oTitle}</a><br />
                   in <a href="${ooLink}" title="Click to view ${parentTitle} discussion"><i class="icon-${ooiType}"></i> ${ooTitle}</a><br />
                   <% newTitle = "in" %>
               % else:
                   %if len(mObj['title']) > maxlen:
                      <% oTitle = mObj['title'][0:(maxlen - 4)] + '...' %>
                   %else:
                      <% oTitle = mObj['title'] %>
                   %endif
                   New <a href="${oLink}" title="Click to view new ${mObj.objType}"><i class="icon-${oiType}"></i> ${oTitle}</a><br />
               %endif
               in <a href="${wLink}" title="Click to view workshop"><i class="icon-cog"></i> ${wTitle}</a><br />
               <i class="icon-time"></i> <span class="recent">${timeSince(mObj.date)}</span> ago<br />
            % endif
        </div><!-- span10 --> 
    </div><!-- row-fluid -->
    </li>
</%def>

<%def name="displayFollowingUsers(numDisplay)">
    % if numDisplay == 0:
        <% fNum = len(c.paginator) %>
        <ul class="unstyled civ-col-list">
        % for user in c.paginator:
            ${listUser(user, 1)}
        % endfor
        </ul>
        % if c.paginator and (len(c.paginator) != len(c.listFollowingUsers)):
            <% state = True %>
            % for p in c.paginator:
                <% state = not state %>
            % endfor
            Total Following: ${c.count} | View ${ c.paginator.pager('~3~') }
        % endif
    % else:
        <% fNum = len(c.followingUsers) %>
        <h2 class="civ-col"><i class="icon-user"></i> Following ${fNum}
        % if numDisplay < fNum:
            <div class="pull-right section_header">
            ${numDisplay} of ${fNum} | <strong><a href="/profile/${c.user['urlCode']}/${c.user['url']}/following">View All</a></strong>
            </div>
        % endif
        </h2>
        <% fCount = 1 %>
        <ul class="unstyled civ-col-list">
        <%
          for user in c.followingUsers:
            listUser(user, 0)
            if fCount == numDisplay:
              break
            fCount += 1
        %>
        </ul>
    % endif
</%def>

<%def name="displayUserFollows(numDisplay)">
    % if numDisplay == 0:
        <% fNum = len(c.paginator) %>
        <ul class="unstyled civ-col-list">
        % for user in c.paginator:
            ${listUser(user, 1)}
        % endfor
        </ul>
        % if c.paginator and (len(c.paginator) != len(c.listUserFollowers)):
            <% state = True %>
            % for p in c.paginator:
                <% state = not state %>
            % endfor
            Total Followers: ${c.count} | View ${ c.paginator.pager('~3~') }
        % endif
    % else:
        % if c.userFollowers:
            <% fNum = len(c.userFollowers) %>
            <h2 class="civ-col"><i class="icon-user"></i> Followers ${fNum}
            % if numDisplay < fNum:
                <div class="pull-right section_header">
                    ${numDisplay} of ${fNum} | <strong><a href="/profile/${c.user['urlCode']}/${c.user['url']}/followers">View All</a></strong>
                </div>
            % endif
            </h2>
            <% fCount = 1 %>
            <ul class="unstyled civ-col-list">
            <%
              for user in c.userFollowers:
                listUser(user, 0)
                if fCount == numDisplay:
                  break
                fCount += 1
            %>
            </ul>
            % if numDisplay < len(c.userFollowers):
                <strong><a href="/profile/${c.user['urlCode']}/${c.user['url']}/followers">View All Followers</a></strong>
            % endif
        % endif
    % endif
</%def>

<%def name="displayConnections()">
  <h6>Mutual connections:</h6>
  % if 'connectionList' not in c.user.keys():
    <div class="alert alert-warning">
      No connections!
    </div> <!-- /.alert-warning -->
  % else:
    <% counter = 1 %>
    % for item in c.user['connectionList']:
      % if counter < 6:
        <% comma = "," %>
      % elif counter == 6:
        <% comma = "" %>
      % else:
        <% break %>
      % endif
      <a href="${item['profileURL']}" alt="${item['name']}">${item['name']}</a>${comma} 
      <% counter += 1 %>
    % endfor
    % if len(c.user['connectionList']) > 6:
      and ${len(c.user['connectionList']) - 6} others.
    % endif
  % endif
</%def>

<%def name="sidebar()">
  <%
    if c.followingUsers:
      displayFollowingUsers(5)
    if c.userFollowers:
      displayUserFollows(5)
  %>
</%def>

<%def name="summary()">
    <% 
        if c.revision:
            name = c.revision['data']
            tagline = c.revision['tagline']
        else:
            name = c.user['name']
            if 'tagline' in c.user.keys():
                tagline = c.user['tagline']
            else:
                tagline = 'No tagline.'
        endif
    %>
    <div class="civ-col-inner">
    <h1>${name}</h1>
    <p>
      ${tagline}
      <% mStart = c.user.date.strftime('%B %d, %Y') %>
      <br /> <br />
      Member since <span class="recent">${mStart}</span>
    </p>
    % if c.revisions:
         <strong>Edit log:</strong><br />
         % for rev in c.revisions:
              <a href="/profile/${c.user['urlCode']}/${c.user['url']}/revision/${rev['urlCode']}">${rev.date}</a><br />  
         % endfor
    % endif
  </div> <!-- /.civ-col-inner -->
</%def>

<%def name="badgesButtons()">
  <div class="civ-col-inner">
        <p>
  <span class="badge badge-success" title="Followers"><i class="icon-white icon-user"></i> ${len(c.userFollowers)}</span> <span class="badge badge-info" title="Total ups - downs of contributed resources, comments and discussions"><i class="icon-white icon-ok"></i> ${c.totalPoints}</span> <span class="badge badge-info" title="Resource and suggestion contributions"><i class="icon-white icon-file"></i> ${c.posts}</span> <span class="badge badge-inverse" title="Flags on contributions"><i class="icon-white icon-flag"></i> ${c.flags}</span>
                </p>
                <br />
                % if 'user' in session and c.authuser.id == c.user.id:
                    <a href="/profile/edit"><button class="btn btn-mini btn-primary" title="Click to edit profile information"><i class="icon-edit icon-white"></i> Edit Profile</button></a>
                % endif
                % if 'user' in session and isAdmin(c.authuser.id):
                   <a href="/profile/${c.user['urlCode']}/${c.user['url']}/admin"><button class="btn btn-mini btn-warning" title="Click to administrate this member"><i class="icon-list-alt icon-white"></i> Admin</button></a>
                % endif
    % if 'user' in session and c.authuser['email'] != c.user['email']:
      <span class="button_container">
        % if c.conf['read_only.value'] == 'true':
          <% pass %>
        % else:
          % if c.isFollowing:
            <button rel="profile_${c.user['urlCode']}_${c.user['url']}" class="btn btn-mini btn-primary followButton following" title="Click to follow/unfollow this member">+Following</button>
          % else:
            <button rel="profile_${c.user['urlCode']}_${c.user['url']}" class="btn btn-mini btn-info followButton unfollow" title="Click to follow/unfollow this member">+Follow</button>
          % endif
        % endif
      </span>
    % endif
  </div> <!-- /.civ-col-inner -->
</%def>

<%def name="geoInfo()">
        <table>
        <tbody>
        <tr>
        <td><a href="${c.geoInfo[0]['cityURL']}"><img src="${c.geoInfo[0]['cityFlagThumb']}" width="60" / class="thumbnail" alt="Click to list workshops scoped within the City of ${c.geoInfo[0]['cityTitle']}" title="Click to list workshops scoped within the City of ${c.geoInfo[0]['cityTitle']}"></a></td><td><a href="${c.geoInfo[0]['cityURL']}">City of ${c.geoInfo[0]['cityTitle']}</a></td>
        </tr>
        <tr>
        <td><a href="${c.geoInfo[0]['countyURL']}"><img src="${c.geoInfo[0]['countyFlagThumb']}" width="60" class="thumbnail" alt="Click to list workshops scoped within the County of ${c.geoInfo[0]['countyTitle']}" title="Click to list workshops scoped within the County of ${c.geoInfo[0]['countyTitle']}"/></a></td><td><a href="${c.geoInfo[0]['countyURL']}">County of ${c.geoInfo[0]['countyTitle']}</a></td>
        </tr>
        <tr>
        <td><a href="${c.geoInfo[0]['stateURL']}"><img src="${c.geoInfo[0]['stateFlagThumb']}" width="60" class="thumbnail" alt="Click to list workshops scoped within the State of ${c.geoInfo[0]['stateTitle']}" title="Click to list workshops scoped within the State of ${c.geoInfo[0]['stateTitle']}"/></a></td><td><a href="${c.geoInfo[0]['stateURL']}">State of ${c.geoInfo[0]['stateTitle']}</a></td>
        </tr>
        <tr>
        <td><a href="${c.geoInfo[0]['countryURL']}"><img src="${c.geoInfo[0]['countryFlagThumb']}" width="60" class="thumbnail" alt="Click to list workshops scoped within the Country of ${c.geoInfo[0]['countryTitle']}" title="Click to list workshops scoped within the Country of ${c.geoInfo[0]['countryTitle']}"/></a></td><td><a href="${c.geoInfo[0]['countryURL']}">${c.geoInfo[0]['countryTitle']}</a></td>
        </tr>
        <tr>
        <td><img src="/images/flags/earth_thumb.gif" width="60" class="thumbnail"/></td><td>Planet Earth</td>
        </tr>
        </tbody>
        </table>
</%def>

<%def name="displayWorkshop(workshop)">
    <%
      if 'user' in session and c.authuser and 'previous' in c.authuser:
          aList = getWorkshopPostsSince(workshop['urlCode'], workshop['url'], c.authuser['previous'])
          if aList:
              sinceNumber = len(aList)
          else:
              sinceNumber = 0
      else:
          sinceNumber = 0
    %>

  % if workshop['mainImage_hash'] == 'supDawg':
    <a href="/workshop/${workshop['urlCode']}/${workshop['url']}"><img src="/images/${workshop['mainImage_identifier']}/thumbnail/${workshop['mainImage_hash']}.thumbnail" alt="Click to view ${workshop['title']}" title="Click to view ${workshop['title']}" width="120" height="80" class="thumbnail"></a>
  % else:
    <a href="/workshop/${workshop['urlCode']}/${workshop['url']}"><img src="/images/${workshop['mainImage_identifier']}/${workshop['mainImage_directoryNum']}/thumbnail/${workshop['mainImage_hash']}.thumbnail" width="120" height="80" class="thumbnail" alt="Click to view ${workshop['title']}" title="Click to view ${workshop['title']}"></a>
  % endif
        <% wcounter = 0 %>
        <a href="/workshop/${workshop['urlCode']}/${workshop['url']}" title="Click to view workshop.">
        % for line in textwrap.wrap(workshop['title'], 18):
            <% wcounter = wcounter + 1 %>
            ${line}<br />
            % if wcounter == 3:
                <% break %>
            % endif            
        % endfor

        % if wcounter == 1:
           <br /><br /><br />
        % elif wcounter == 2:
           <br /><br />
        % elif wcounter == 3:
           <br />
        % endif
        % if sinceNumber:
            % if sinceNumber > 1:
                <span class="label-success" style="color:white;"><strong>&nbsp;${sinceNumber} new posts!&nbsp;</strong></span>
            % else:
                <span class="label-success" style="color:white;"><strong>&nbsp;${sinceNumber} new post!&nbsp;</strong></span>
            % endif
        % endif
           <br />
        </a>
</%def>

<%def name="listWorkshops(set)">
    <ul class="unstyled civ-block-list">
    % for workshop in set:
        <li>
        <p>${displayWorkshop(workshop)}</p>
        </li>
    % endfor
    </ul>
</%def>

<%def name="accounts()">
    % if 'user' in session and c.accounts and (c.authuser.id == c.user.id or isAdmin(c.authuser.id)):
        <h2 class="civ-col"><i class="icon-list-alt"></i> Accounts I am Administrating</h2>
        <div class="civ-col-inner">
        <ul class="unstyled civ-block-list">
        % for account in c.accounts:
            <li>
            <p><a href="/account/${account['urlCode']}">${account['orgName']}</a></p>
            </li>
        % endfor
        </div> <!-- /.civ-col-inner -->
    </ul>
    % elif ('user' in session and c.authuser.id == c.user.id) and not c.accounts:
        <h2 class="civ-col"><i class="icon-list-alt"></i> Create a Free Trial Workshop!</h2>
        Create a free trial Civinomics workshop. The workshop is private, and you can have up to 10 other Civinomics members participate.
        <form method="post" name="userAccount" id="userAccount" action="/profile/${c.user['urlCode']}/${c.user['url']}/account/">
        <br />
        <button type="submit" class="btn btn-warning">Create Workworkshop</button>
        <br /><br />
  % endif
</%def>


<%def name="workshops()">
  % if c.facilitatorWorkshops:
    <h2 class="civ-col"><i class="icon-list-alt"></i> Workshops I am facilitating</h2>
    <div class="civ-col-inner">
      ${listWorkshops(c.facilitatorWorkshops)}
    </div> <!-- /.civ-col-inner -->
  % endif
  % if c.followingWorkshops:
    <h2 class="civ-col"><i class="icon-cog"></i> Workshops I am following</h2>
    <div class="civ-col-inner">
      ${listWorkshops(c.followingWorkshops)}
    </div> <!-- /.civ-col-inner -->
  % endif
        % if 'user' in session and c.pendingFacilitators and c.authuser.id == c.user.id:
            ${pendingFacilitateInvitations()}
        % endif
</%def>

<%def name="totalComments()">
    <%
      if c.comments:
         total = len(c.comments)
         if total > 1:
             title = "comments"
         else:
             title = "comment"
      else:
         title = "comments"
         total = 0
    %>
  <p class="total">
    ${total}<br>
    <span>${title}</span>
  </p>
    % if c.comments:
        <center><b><font size="2" color="DarkGrey"> Up Votes vs. Down Votes </font></b></center>
        <div class="progress progress-success" id="ComBar">
          <div class="bar" style="width: ${c.comUpsPercent}%;"></div>
        </div>
    % endif
</%def>

<%def name="latestComments(numDisplay)">
    <ul class="unstyled civ-col-list">
        <% cList = c.comments %>
        % if numDisplay == 0:
            <% cList = c.paginator %>
            <h4>All comments:</h4>
            <a href="/profile/${c.user['urlCode']}/${c.user['url']}"><strong>Back to Profile</strong></a>
            <br />
        % else:
            % if numDisplay > len(cList):
                <% cTotal = len(cList) %>
            % else:
                <% cTotal = numDisplay %>
            % endif
            <h4>${cTotal} most recent comments:</h4>
            % if numDisplay < len(cList):
                <a href="/profile/${c.user['urlCode']}/${c.user['url']}/comments"><strong>View All Comments</strong></a>
            % endif
        % endif
        <% comCount = 1 %>
        % for comment in cList:
            <%
                d = getDiscussionByID(int(comment['discussion_id']))
                w = getWorkshop(d['workshopCode'], d['workshopURL'])
            %>
            % if 'ups' in comment and 'downs' in comment:
                <% cRating = int(comment['ups']) - int(comment['downs']) %>
            % else:
                <% cRating = 0 %>
            % endif
            % if len(comment['data']) <= 25:
                <% cString = comment['data'] %>
            % else:
                <% cString = comment['data'][:25] %>
            % endif
            % if d['discType'] == 'suggestion':
                <% dParent = getSuggestion(d['suggestionCode'], d['suggestionURL']) %>
                <% oURL = "/workshop/" + w['urlCode'] + "/" + w['url'] + "/suggestion/" + d['suggestionCode'] + "/" + d['suggestionURL'] %>
                <% oIcon = "pencil" %>
                <% oTitle = dParent['title'] %>
            % elif d['discType'] == 'resource' or d['discType'] == 'sresource':
                <% dParent = getResource(d['resourceCode'], d['resourceURL']) %>
                <% oURL = "/workshop/" + w['urlCode'] + "/" + w['url'] + "/resource/" + d['resourceCode'] + "/" + d['resourceURL'] %>
                <% oIcon = "book" %>
                <% oTitle = dParent['title'] %>
            % elif d['discType'] == 'general':
                <% oURL = "/workshop/" + w['urlCode'] + "/" + w['url'] + "/discussion/" + d['urlCode'] + "/" + d['url'] %>
                <% oIcon = "folder-open" %>
                <% oTitle = d['title'] %>
            % elif d['discType'] == 'background':
                <% oURL = "/workshop/" + w['urlCode'] + "/" + w['url'] + "/background" %>
                <% oIcon = "book" %>
                <% oTitle = "Workshop Background" %>
            % else:
                <% oURL = "" %>
                <% oTitle = "" %>
                <% oIcon = "" %>
            % endif
            <% cFlags = getFlags(comment) %>
            % if cFlags:
                <% numFlags = len(cFlags) %>
            % else:
                <% numFlags = 0 %>
            % endif

            <li>
            <span class="badge badge-info" title="Rating for this comment (ups - downs)"><i class="icon-white icon-ok"></i>${cRating}</span> 
            <span class="badge badge-inverse" title="Number of flags on this comment"><i class="icon-white icon-flag"></i>${numFlags}</span> 
            <span class="recent" title="When this comment was written"><i class="icon-time"></i> ${timeSince(comment.date)} ago</span><br />
            <i class="icon-comment"></i> ${cString}<br />
            <i class="icon-${oIcon}"></i> <a href="${oURL}">${oTitle}</a><br />
            <i class="icon-cog"></i> <a href="/workshop/${w['urlCode']}/${w['url']}">${w["title"]}</a>
            <br /><br />
            </li>
            % if numDisplay != 0:
                % if comCount >= numDisplay:
                    <% break %>
                % endif 
                <% comCount += 1 %>
            % endif
        %endfor              
        </ul>
        % if c.paginator and (len(c.paginator) != len(c.comments)):
            <% state = True %>
            % for p in c.paginator:
                <% state = not state %>
            % endfor
            Total Comments: ${c.count} | View ${ c.paginator.pager('~3~') }
        % endif
</%def>

<%def name="totalSuggestions()">
        <%
          if c.suggestions:
            total = len(c.suggestions)
            if total > 1:
                title = "suggestions"
            else:
                title = "suggestion"
          else:
            title = "suggestions"
            total = 0
        %>
  <p class="total">
    ${total}<br>
    <span>${title}</span>
  </p>
        % if c.suggestions:
            <center><b><font size="2" color="DarkGrey"> Average Rating</font></b></center>
            <div class="progress progress-success" id="SugBar">
              <div class="bar" style="width: ${c.sugRateAvg}%;"></div>
            </div>
        % endif

</%def>

<%def name="latestSuggestions(numDisplay)">
    % if c.suggestions:
        <% sList = c.suggestions %>
        % if numDisplay == 0:
            <% sList = c.paginator %>
            <h4>All Suggestions:</h4>
            <a href="/profile/${c.user['urlCode']}/${c.user['url']}"><strong>Back to Profile</strong></a>
        % else:
            % if numDisplay > len(sList):
                <% sTotal = len(sList) %>
            % else:
                <% sTotal = numDisplay %>
            % endif
            <h4>${sTotal} most recent suggestions:</h4>
            % if numDisplay < len(c.suggestions):
                <a href="/profile/${c.user['urlCode']}/${c.user['url']}/suggestions"><strong>View All Suggestions</strong></a>
            % endif
            <br />
        % endif
        <% count = 1 %>
        <ul class="unstyled civ-col-list">
        % for s in sList:
            % if numDisplay != 0:
                % if count > numDisplay:
                    <% break %>
                % endif
            % endif
            <%
                w = getWorkshop(s['workshopCode'], s['workshopURL'])
                sFlags = getFlags(s)
                if sFlags:
                    numFlags = len(sFlags)
                else:
                    numFlags = 0
                sAvg = int(float(s['ratingAvg_overall'])) 
            %>
            
            <li>
            <span class="badge badge-info" title="0 - 100 Average rating for this suggestion (Sum of all ratings / number of ratings)"><i class="icon-white icon-ok-circle"></i>${sAvg}</span>
            <span class="badge badge-inverse" title="Number of flags on this suggestion"><i class="icon-white icon-flag"></i>${numFlags}</span>
            <i class="icon-time"></i><span class="recent" title="When this suggestion was added">${timeSince(s.date)} ago</span><br />
            <i class="icon-pencil"></i> <a href = "/workshop/${w['urlCode']}/${w['url']}/suggestion/${s['urlCode']}/${s['url']}"><strong>${s["title"]}</strong></a><br />
            <i class="icon-cog"></i> <a href="/workshop/${w['urlCode']}/${w['url']}">${w["title"]}</a>
            </li>
            <% count += 1 %>
        % endfor
        </ul> <!-- /.unstyled -->
        % if c.paginator and (len(c.paginator) != len(c.suggestions)):
            <% state = True %>
            % for p in c.paginator:
                <% state = not state %>
            % endfor
            Total Suggestions: ${c.count} | View ${ c.paginator.pager('~3~') }
        % endif
    % else:
        <div class="alert alert-warning">No suggestions to show.</div>
    % endif
</%def>

<%def name="totalResources()">
        % if c.resources:
           <% total = len(c.resources) %>
           % if total > 1:
               <% title = "resources" %>
           % else:
               <% title = "resource" %>
           % endif
        % else:
           <% title = "resources" %>
           <% total = 0 %>
        % endif
  <p class="total">
    ${total}<br>
    <span>${title}</span>
  </p>
        % if c.resources:
            <center><b><font size="2" color="DarkGrey"> Up Votes vs. Down Votes </font></b></center>
            <div class="progress progress-success" id="ResBar">
              <div class="bar" style="width: ${c.resUpsPercent}%;"></div>
            </div>
        % endif
</%def>

<%def name="latestResources(numDisplay)">
    % if c.resources:
        <% rList = c.resources %>
        % if numDisplay == 0:
            <% rList = c.paginator %>
            <h4>All Resources:</h4>
            <a href="/profile/${c.user['urlCode']}/${c.user['url']}"><strong>Back to Profile</strong></a>
            <br />
        % else:
            % if numDisplay > len(rList):
                <% rTotal = len(rList) %>
            % else:
                <% rTotal = numDisplay %>
            % endif
            <h4>${rTotal} most recent resources:</h4>
            % if numDisplay < len(c.resources):
                <a href="/profile/${c.user['urlCode']}/${c.user['url']}/resources"><strong>View All Resources</strong></a>
            % endif
            <br />
        % endif
        <% count = 1 %>
        <ul class="unstyled civ-col-list">
        % for r in rList:
            % if numDisplay != 0:
                % if count > numDisplay:
                    <% break %>
                % endif
            % endif
            <%
                w = getWorkshopByID(r['workshop_id'])
                rFlags = getFlags(r)
                if rFlags:
                    numFlags = len(rFlags)
                else:
                    numFlags = 0
                if 'ups' in r and 'downs' in r:
                    rRating = int(r['ups']) - int(r['downs'])
                else:
                    rRating = 0
            %>
            
            <li>
            <span class="badge badge-info" title="Rating for this resource (ups - downs)"><i class="icon-white icon-ok"></i>${rRating}</span>
            <span class="badge badge-inverse" title="Number of flags on this resource"><i class="icon-white icon-flag"></i>${numFlags}</span>
            <i class="icon-time"></i><span class="recent" title="When this resource was added">${timeSince(r.date)} ago</span><br />
            <i class="icon-book"></i> <a href = "/workshop/${w['urlCode']}/${w['url']}/resource/${r['urlCode']}/${r['url']}"><strong>${r["title"]}</strong></a><br />
            % if r['parent_id'] != '0' and r['parent_type'] == 'suggestion':
                <% s = getSuggestionByID(r['parent_id']) %>
                <i class="icon-pencil"></i> <a href = "/workshop/${w['urlCode']}/${w['url']}/suggestion/${s['urlCode']}/${s['url']}"><strong>${s["title"]}</strong></a><br />
            % endif
            <i class="icon-cog"></i> <a href="/workshop/${w['urlCode']}/${w['url']}">${w["title"]}</a>
            </li>
            <% count += 1 %>
        % endfor
        % if c.paginator and (len(c.paginator) != len(c.resources)):
            <% state = True %>
            % for p in c.paginator:
                <% state = not state %>
            % endfor
            Total Resources: ${c.count} | View ${ c.paginator.pager('~3~') }
        % endif
        </ul> <!-- /.unstyled -->
    % else:
        <div class="alert alert-warning">No resources to show.</div>
    % endif
</%def>

<%def name="totalDiscussions()">
    <%
      if c.discussions:
         total = len(c.discussions)
         if total > 1:
             title = "discussions"
         else:
             title = "discussion"
      else:
         title = "discussions"
         total = 0
    %>
  <p class="total">
    ${total}<br>
    <span>${title}</span>
  </p>
        % if c.discussions:
            <center><b><font size="2" color="DarkGrey"> Up Votes vs. Down Votes </font></b></center>
            <div class="progress progress-success" id="DisBar">
              <div class="bar" style="width: ${c.disUpsPercent}%;"></div>
            </div>
        % endif
</%def>

<%def name="latestDiscussions(numDisplay)">
    % if c.discussions:
        <% dList = c.discussions %>
        % if numDisplay == 0:
            <% dList = c.paginator %>
            <h4>All discussions:</h4>
            <a href="/profile/${c.user['urlCode']}/${c.user['url']}"><strong>Back to Profile</strong></a>
            <br />
        % else:
            <%
              if numDisplay > len(dList):
                  dTotal = len(dList)
              else:
                  dTotal = numDisplay
            %>
            <h4>${dTotal} most recent discussions:</h4>
            % if numDisplay < len(dList):
                <a href="/profile/${c.user['urlCode']}/${c.user['url']}/discussions"><strong>View All Discussions</strong></a>
            % endif
            <br />
        % endif
        <% count = 1 %>
        <ul class="unstyled civ-col-list">
        % for d in dList:
            % if numDisplay != 0:
                % if count > numDisplay:
                    <% break %>
                % endif
            % endif
            <%
                w = getWorkshop(d['workshopCode'], d['workshopURL'])
                dFlags = getFlags(d)
                if dFlags:
                    numFlags = len(dFlags)
                else:
                    numFlags = 0
                if 'ups' in d and 'downs' in d:
                    dRating = int(d['ups']) - int(d['downs'])
                else:
                    dRating = 0
            %>
            
            <li>
            <span class="badge badge-info" title="Rating for this discussion (ups - downs)"><i class="icon-white icon-ok"></i>${dRating}</span>
            <span class="badge badge-inverse" title="Number of flags on this discussion"><i class="icon-white icon-flag"></i>${numFlags}</span>
            <i class="icon-time"></i><span class="recent" title="When this discussion topic was added">${timeSince(d.date)} ago</span><br />
            <i class="icon-folder-open"></i> <a href = "/workshop/${w['urlCode']}/${w['url']}/discussion/${d['urlCode']}/${d['url']}"><strong>${d["title"]}</strong></a><br />
            <i class="icon-cog"></i> <a href="/workshop/${w['urlCode']}/${w['url']}">${w["title"]}</a>
            </li>
            <% count += 1 %>
        % endfor
        % if c.paginator and (len(c.paginator) != len(c.discussions)):
            <% state = True %>
            % for p in c.paginator:
                <% state = not state %>
            % endfor
            Total Discussions: ${c.count} | View ${ c.paginator.pager('~3~') }
        % endif
        </ul> <!-- /.unstyled -->
    % else:
        <div class="alert alert-warning">No resources to show.</div>
    % endif

</%def>

<%def name="memberAdminControls()">
</%def>

<%def name="pendingFacilitateInvitations()">
% if 'user' in session and (c.pendingFacilitators and c.authuser.id == c.user.id):      
    <h2 class="civ-col">Invitations to CoFacilitate Workshops</h2>
    <% fNum = len(c.pendingFacilitators) %>
    <% wNum = 0 %>
    % for f in c.pendingFacilitators:
        % if wNum % 6 == 0 or wNum == 0: ## begin a new row
           <ul class="unstyled civ-block-list">
        % elif wNum % 6 == 5: ## end a row
           </ul>
           <ul class="unstyled civ-block-list">
        % endif
        <li>
        <% workshop = getWorkshopByID(f['workshopID']) %>
        <form method="post" name="inviteFacilitate" id="inviteFacilitate" action="/profile/${c.user['urlCode']}/${c.user['url']}/coFacilitateHandler/">
        <input type=hidden name=workshopCode value="${workshop['urlCode']}">
        <input type=hidden name=workshopURL value="${workshop['url']}">
        % if workshop['mainImage_hash'] == 'supDawg':
            <a href="/workshops/${workshop['urlCode']}/${workshop['url']}"><img src="/images/${workshop['mainImage_identifier']}/thumbnail/${workshop['mainImage_hash']}.thumbnail" alt="mtn" class="block" style = "margin: 5px; width: 120px; height: 80px;"/><br>
            <a href="/workshops/${workshop['urlCode']}/${workshop['url']}">${workshop['title']}</a>
        % else:
            <a href="/workshops/${workshop['urlCode']}/${workshop['url']}"><img src="/images/${workshop['mainImage_identifier']}/${workshop['mainImage_directoryNum']}/thumbnail/${workshop['mainImage_hash']}.thumbnail" alt="mtn" class="block" style = "margin: 5px; width: 120px; height: 80px;"/><br>
            <a href="/workshops/${workshop['urlCode']}/${workshop['url']}">${workshop['title']}</a>
        % endif
        <br /> <br />
        <button type="submit" name=acceptInvite class="btn btn-mini btn-success" title="Accept the invitation to cofacilitate the workshop">Accept</button>
        <button type="submit" name=declineInvite class="btn btn-mini btn-danger" title="Decline the invitation to cofcilitate the workshop">Decline</button>
        </form>
        <li>
        <% 
          wNum = wNum + 1
          if wNum == 6:
              wNum = 0
        %>
    % endfor
    </ul>
% endif
</%def>

<%def name="inviteCoFacilitate()">
  %if 'user' in session and c.authuser:
      <% checkW = getWorkshopsByOwner(c.authuser.id) %>
      <% wList = [] %>
      % for w in checkW:
          % if w['deleted'] == '0':
              % if not isFacilitator(c.user.id, w.id) and not isPendingFacilitator(c.user.id, w.id):
                  <% wList.append(w) %>
              % endif 
          % endif
      % endfor
      % if c.authuser.id != c.user.id and wList:
          <h2 class="civ-col">Invite This Member to Facilitate</h2>
          <form method="post" name="inviteFacilitate" id="inviteFacilitate" action="/profile/${c.user['urlCode']}/${c.user['url']}/coFacilitateInvite/" class="form-inline">
          <br />
          <button type="submit" class="btn btn-mini btn-warning" title="Click to invite this member to cofacilitate the selected workshop"><i class="icon-envelope icon-white"></i> Invite</button> to co-facilitate <select name=inviteToFacilitate>
          % for myW in wList:
              <br />
              <option value="${myW['urlCode']}/${myW['url']}">${myW['title']}</option>
              <br /><br />
          % endfor                       
          </select>
          </form>
      % endif
  %endif
</%def>

<%def name="totalFollowers()">
    <%
      if c.listUserFollowers:
         total = len(c.listUserFollowers)
         if total > 1:
             title = "followers"
         else:
             title = "follower"
      else:
         title = "followers"
         total = 0
    %>
  <p class="total">
    ${total}<br>
    <span>${title}</span><br />
    <span><a href="/profile/${c.user['urlCode']}/${c.user['url']}">Back to Profile</a></span>
  </p>
</%def>

<%def name="totalFollowing()">
        <%
          if c.listFollowingUsers:
             total = len(c.listFollowingUsers)
          else:
             total = 0
        %>
  <p class="total">
    ${total}<br>
    <span>following</span><br />
    <span><a href="/profile/${c.user['urlCode']}/${c.user['url']}">Back to Profile</a></span>
  </p>
</%def>

