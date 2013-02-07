<%!
    import pylowiki.lib.db.workshop as workshopLib
    import pylowiki.lib.db.facilitator as facilitatorLib
    import pylowiki.lib.db.listener as listenerLib
%>

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="thingCount(user, things, title)">
    <% 
        thisTitle = title
        if title == 'conversations':
            thisTitle = 'discussions'
        elif title == 'bookmarks':
            thisTitle = 'watching'
        thingListingURL = "/profile/%s/%s/%s" %(user['urlCode'], user['url'], thisTitle)
    %>
    <h3 class="profile-count centered">
        <a class="black" href="${thingListingURL}">${len(things)}</a>
    </h3>
    <div class="centered"><p><a class="green green-hover" href="${thingListingURL}">${title}</a></p></div>
</%def>

<%def name="showWorkshop(workshop, **kwargs)">
    <div class="media profile-workshop">
        <a class="pull-left" ${lib_6.workshopLink(workshop)}>
            <img class="media-object" src="${lib_6.workshopImage(workshop, raw=True) | n}">
        </a>
        <%
            if 'imageOnly' in kwargs:
                if kwargs['imageOnly'] == True:
                    return
        %>
        <div class="media-body">
            <a ${lib_6.workshopLink(workshop)}><h5 class="media-heading">${workshop['title']}</h5></a>
            ${workshop['description']}
        </div>
    </div>
</%def>

<%def name="listCreatedThings(user, things, title)">
    <div class="section-wrapper">
        <div class="browse">
            <h3 class="centered section-header"> ${title} </h3>
            <table class="table table-condensed table-hover user-thing-listing">
                <tbody>
                    <% counter = 0 %>
                    % for thing in things:
                        % if counter == 0:
                            <tr> <td class="no-border">
                        % else:
                            <tr> <td>
                        % endif
                            <%
                                workshop = workshopLib.getWorkshopByCode(thing['workshopCode'])
                                thingLink = lib_6.thingLinkRouter(thing, workshop, raw=True, embed=True)
                                workshopLink = lib_6.workshopLink(workshop, embed=True)
                                descriptionText = 'No description'
                                if 'comment' in thing.keys():
                                    if thing['comment'] != '':
                                        descriptionText = thing['comment']
                                elif 'text' in thing.keys():
                                    if thing['text'] != '':
                                        descriptionText = thing['text']
                            %>
                            ${showWorkshop(workshop, imageOnly = True)}
                            <a ${thingLink | n}> ${lib_6.ellipsisIZE(thing['title'], 60)} </a> in workshop <a ${workshopLink | n}> ${workshop['title']} </a> on <span class="green">${thing.date.strftime('%b %d, %Y')}</span>
                            <br />
                            Description: ${lib_6.ellipsisIZE(descriptionText, 135)}
                        </td> </tr>
                        <% counter += 1 %>
                    % endfor
                </tbody>
            </table>
        </div>
    </div>
</%def>

<%def name="listInterestedThings(user, things, title)">
    <div class="section-wrapper">
        <div class="browse">
            <h3 class="centered section-header"> ${title} </h3>
            % if len(things) == 0:
                There doesn't seem to be anything here!
            % else:
                % if c.listingType == 'watching':
                    <table class="table table-condensed table-hover user-thing-listing">
                        <tbody>
                            <% counter = 0 %>
                            % for thing in things:
                                % if counter == 0:
                                    <tr> <td class="no-border">
                                % else:
                                    <tr> <td>
                                % endif
                                
                                ${showWorkshop(thing, imageOnly = True)}
                                <a ${lib_6.workshopLink(thing, embed=True) | n}> ${lib_6.ellipsisIZE(thing['title'], 60)} </a>
                                <br />
                                Description: ${lib_6.ellipsisIZE(thing['description'], 135)}
                            % endfor
                        </tbody>
                    </table>
                % else:
                    <% objType = things[0].objType %>
                    <ul class="thumbnails">
                        % for thing in things:
                            <li class="follow">
                                ${lib_6.userImage(thing, className="avatar hoverTip", rel="tooltip", placement="bottom")}
                            </li>
                        % endfor
                    </ul>
                % endif
            % endif
        </div>
    </div>
</%def>

<%def name="followButton(user)">
    % if c.conf['read_only.value'] == 'true':
          <% pass %>
    % else:
        <span class="button_container">
        % if c.isFollowing:
            <button rel="profile_${c.user['urlCode']}_${c.user['url']}" class="btn round pull-right followButton following">
            <img class="watch" src="/images/glyphicons_pro/glyphicons/png/glyphicons_051_eye_open.png">
            <span> Unfollow </span>
            </button>
        % else:
            <button rel="profile_${c.user['urlCode']}_${c.user['url']}" class="btn round pull-right followButton unfollow">
            <img class="watch" src="/images/glyphicons_pro/glyphicons/png/glyphicons_051_eye_open.png">
            <span> Follow </span>
            </button>
        % endif
        </span>
    % endif
</%def>

<%def name="profileDashboard()">
    <div class="centered">
        ${lib_6.userImage(c.user, className="avatar avatar-large")}
    </div>
    <div class="section-wrapper">
        <div class="browse">
            <h3 class="section-header">${c.user['name']}</h3>
            <p>${lib_6.userGeoLink(c.user)}</p>
            <p>Joined ${c.user.date.strftime('%b %d, %Y')}</p>
            % if c.user['greetingMsg'] != '':
                <small class="muted expandable">${c.user['greetingMsg']}</small>
            % endif
            % if c.user['websiteLink'] != '':
                <p class = "expandable no-bottom"><a href="${c.user['websiteLink']}">${c.user['websiteLink']}</a></p>
                % if c.user['websiteDesc'] != '':
                    <small class="muted expandable">${c.user['websiteDesc']}</small>
                % endif
            % endif
            <hr>
            <div class="row-fluid">
                <div class="span4">
                    ${thingCount(c.user, c.resources, 'resources')}
                </div>
                <div class="span4">
                    ${thingCount(c.user, c.ideas, 'ideas')}
                </div>
                <div class="span4">
                    ${thingCount(c.user, c.discussions, 'conversations')}
                </div>
            </div> <!--/.row-fluid-->
            <hr>
            <div class="row-fluid">
                <div class="span4">
                    ${thingCount(c.user, c.followers, 'followers')}
                </div>
                <div class="span4">
                    ${thingCount(c.user, c.following, 'following')}
                </div>
                <div class="span4">
                    ${thingCount(c.user, c.watching, 'bookmarks')}
                </div>
            </div> <!--/.row-fluid-->
            <hr>
            Placeholder for listing organizations
        </div><!--/.browse-->
    </div><!--/.section-wrapper-->
</%def>

<%def name="showActivity(activity)">
    <table class="table table-hover table-condensed">
        <tbody>
        % for item in activity:
            <%
                workshop = workshopLib.getWorkshopByCode(item['workshopCode'])
                if item.objType == 'comment':
                    activityStr = 'Commented on a'
                    if 'ideaCode' in item.keys():
                        activityStr += 'n'
                else:
                    activityStr = 'Added a'
                if item.objType == 'idea':
                    activityStr += 'n'
                if item.objType == 'comment':
                    activityStr += ' <a ' + lib_6.thingLinkRouter(item, workshop, embed = True, id='accordion-%s'%item['urlCode']) + '>'
                else:
                    activityStr += ' <a ' + lib_6.thingLinkRouter(item, workshop, embed = True) + '>'
                if item.objType != 'comment':
                    if item.objType == 'discussion':
                        activityStr += "conversation </a>"
                    else:
                        activityStr += item.objType + "</a>"
                else:
                    if 'ideaCode' in item.keys():
                        activityStr += 'idea </a>'
                    elif 'resourceCode' in item.keys():
                        activityStr += 'resource </a>'
                    else:
                        activityStr += 'conversation </a>'
                activityStr += ' in <a ' + lib_6.workshopLink(workshop, embed = True) + '>'
                activityStr += lib_6.ellipsisIZE(workshop['title'], 25) + '</a>'
                if item.objType == 'comment':
                    activityStr += ' : <span class="expandable">%s</span>' % item['data']
            %>
            <tr> <td>${activityStr | n} </td></tr>
        % endfor
        </tbody>
    </table>
</%def>

<%def name="inviteCoFacilitate()">
    %if 'user' in session and c.authuser:
        <% 
            fList = facilitatorLib.getFacilitatorsByUser(c.authuser.id)
            wListF = []
            wListL = []
            for f in fList:
                w = workshopLib.getWorkshopByID(f['workshopID'])
                if w['deleted'] == '0' and w['type'] != 'personal':
                    wlisten = listenerLib.getListener(c.user, w)
                    if not facilitatorLib.isFacilitator(c.user.id, w.id) and not facilitatorLib.isPendingFacilitator(c.user.id, w.id):
                        wListF.append(w)
                    if not wlisten:
                        wListL.append(w)
                    elif wlisten['pending'] == '0':
                        wListL.append(w)
                        
        %>
        % if c.authuser.id != c.user.id and wListF:
            <div class="row">
                <div class="centered">
                <form method="post" name="inviteFacilitate" id="inviteFacilitate" action="/profile/${c.user['urlCode']}/${c.user['url']}/facilitate/invite/handler/" class="form-inline">
                    <br />
                    <button type="submit" class="btn btn-mini btn-warning" title="Click to invite this member to cofacilitate the selected workshop">Invite</button> to co-facilitate <select name="inviteToFacilitate">
                    % for myW in wListF:
                        <option value="${myW['urlCode']}/${myW['url']}">${myW['title']}</option>
                    % endfor                       
                    </select>
                </form>
                </div>
            </div><!-- row -->
        % endif
        % if wListL:
            <div class="row">
                <div class="centered">
                <form method="post" name="inviteListen" id="inviteListen" action="/profile/${c.user['urlCode']}/${c.user['url']}/listener/invite/handler" class="form-inline">
                    <br />
                    <button type="submit" class="btn btn-mini btn-warning" title="Click to invite this member to be a listener of the selected workshop">Invite</button> to be a listener <select name="workshopCode">
                    % for myW in wListL:
                        <option value="${myW['urlCode']}">${myW['title']}</option>
                    % endfor                       
                    </select>
                </form>
                </div>
            </div><!-- row -->
        % endif
    %endif
</%def>


