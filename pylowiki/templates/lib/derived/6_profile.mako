<%!
    import pylowiki.lib.db.workshop     as workshopLib
    import pylowiki.lib.db.initiative   as initiativeLib
    import pylowiki.lib.db.facilitator  as facilitatorLib
    import pylowiki.lib.db.listener     as listenerLib
    import pylowiki.lib.db.discussion   as discussionLib
    import pylowiki.lib.db.follow       as followLib
    import pylowiki.lib.db.user         as userLib
    import pylowiki.lib.db.pmember      as pmemberLib
    import pylowiki.lib.db.generic      as genericLib
    import pylowiki.lib.utils           as utils
    import pylowiki.lib.fuzzyTime       as fuzzyTime
    import misaka as misaka
    
    import logging, os
    log = logging.getLogger(__name__)
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

<%def name="showInitiative(item, **kwargs)">
    <div class="media profile-workshop">
        <a class="pull-left" href="/initiative/${item['urlCode']}/${item['url']}/show">
        % if 'directoryNum_photos' in item and 'pictureHash_photos' in item:
            <% thumbnail_url = "/images/photos/%s/thumbnail/%s.png"%(item['directoryNum_photos'], item['pictureHash_photos']) %>
        % else:
            <% thumbnail_url = "/images/slide/thumbnail/supDawg.thumbnail" %>
        % endif
        <div class="thumbnail tight media-object" style="height: 60px; width: 90px; margin-bottom: 5px; background-image:url(${thumbnail_url}); background-size: cover; background-position: center center;"></div>
        </a>
        <%
            if 'imageOnly' in kwargs:
                if kwargs['imageOnly'] == True:
                    return
        %>
        <div class="media-body">
            <span class="label label-info">Initiative</span> <a href="/initiative/${item['urlCode']}/${item['url']}/show" class="listed-item-title media-heading lead bookmark-title">${item['title']}</a>
            % if 'user' in session:
                % if c.user.id == c.authuser.id or userLib.isAdmin(c.authuser.id):
                    <a href="/initiative/${item['urlCode']}/${item['url']}/edit">Edit</a> &nbsp;
                    % if item['public'] == '0':
                        Not yet public
                    % else:
                        Public
                    % endif
                % endif
            % endif
            <br />
            Description: ${lib_6.ellipsisIZE(item['description'], 135)}
        </div><!-- media-body -->
    </div><!-- media -->
</%def>

<%def name="showWorkshop(workshop, **kwargs)">
    <div class="media profile-workshop">
        <a class="pull-left" href="${lib_6.workshopLink(workshop)}">
          <div class="thumbnail tight media-object" style="height: 60px; width: 90px; margin-bottom: 5px; background-image:url(${lib_6.workshopImage(workshop, raw=True) | n}); background-size: cover; background-position: center center;"></div>
        </a>
        <%
            if 'imageOnly' in kwargs:
                if kwargs['imageOnly'] == True:
                    return
            if 'role' in kwargs:
                role = kwargs['role']
            else:
                role = ''
        %>
        <div class="media-body">
            <a href="${lib_6.workshopLink(workshop)}" class="listed-item-title media-heading lead bookmark-title">${workshop['title']}</a>
            <span class="label label-info pull-right">${role}</span>
            % if 'user' in session:
                % if c.user.id == c.authuser.id or userLib.isAdmin(c.authuser.id):
                    % if role == 'Facilitating':
                        <div style="margin-top: 10px;">
                            <%
                                f = facilitatorLib.getFacilitatorsByUserAndWorkshop(c.user, workshop)[0]
                                itemsChecked = ''
                                flagsChecked = ''
                                digestChecked = ''
                                if 'itemAlerts' in f and f['itemAlerts'] == '1':
                                    itemsChecked = 'checked'
                                if 'flagAlerts' in f and f['flagAlerts'] == '1':
                                    flagsChecked = 'checked'
                                if 'digest' in f and f['digest'] == '1':
                                    digestChecked = 'checked'
                            %>
                            <div class="row" ng-controller="facilitatorController">
                                <div class="col-sm-3">Email when:</div>
                                <div class="col-sm-3">
                                    <form ng-init="code='${workshop['urlCode']}'; url='${workshop['url']}'; user='${c.user['urlCode']}'" class="no-bottom form-inline">
                                        New Items: <input type="checkbox" name="flagAlerts" value="flags" ng-click="emailOnAdded()" ${itemsChecked}>
                                        <span ng-show="emailOnAddedShow">{{emailOnAddedResponse}}</span>
                                    </form>
                                </div><!-- col-sm-3 -->
                                <div class="col-sm-3">
                                    <form ng-init="code='${workshop['urlCode']}'; url='${workshop['url']}'; user='${c.user['urlCode']}'" class="no-bottom form-inline">
                                        New Flags: <input type="checkbox" name="itemAlerts" value="items" ng-click="emailOnFlagged()" ${flagsChecked}>
                                        <span ng-show="emailOnFlaggedShow">{{emailOnFlaggedResponse}}</span>
                                    </form>
                                </div><!-- col-sm-3 -->
                                <div class="col-sm-3">
                                    <form ng-init="code='${workshop['urlCode']}'; url='${workshop['url']}'; user='${c.user['urlCode']}'" class="no-bottom form-inline">
                                        Weekly Digest: <input type="checkbox" name="digest" value="items" ng-click="emailDigest()" ${digestChecked}>
                                        <span ng-show="emailDigestShow">{{emailDigestResponse}}</span>
                                    </form>
                                </div><!-- col-sm-3 -->
                            </div><!-- row -->
                        </div><!-- margin-top -->
                    % endif
                    % if role == 'Listening':
                        <div style="margin-top: 10px;">
                            <%
                                l = listenerLib.getListener(c.user['email'], workshop)
                                itemsChecked = ''
                                digestChecked = ''
                                if l:
                                    if 'itemAlerts' in l and l['itemAlerts'] == '1':
                                        itemsChecked = 'checked'
                                    if 'digest' in l and l['digest'] == '1':
                                        digestChecked = 'checked'
                            %>
                            <div class="row" ng-controller="listenerController">
                                <div class="col-sm-3">Email when:</div>
                                <div class="col-sm-3">
                                    <form ng-init="code='${workshop['urlCode']}'; url='${workshop['url']}'; user='${c.user['urlCode']}'" class="no-bottom form-inline">
                                        New Items: <input type="checkbox" name="itemAlerts" value="items" ng-click="emailOnAdded()" ${itemsChecked}>
                                        <span ng-show="emailOnAddedShow">{{emailOnAddedResponse}}</span>
                                    </form>
                                </div><!-- col-sm-3 -->
                                <div class="col-sm-3">
                                    <form ng-init="code='${workshop['urlCode']}'; url='${workshop['url']}'; user='${c.user['urlCode']}'" class="no-bottom form-inline">
                                        Weekly Digest: <input type="checkbox" name="digest" value="items" ng-click="emailDigest()" ${digestChecked}>
                                        <span ng-show="emailDigestShow">{{emailDigestResponse}}</span>
                                    </form>
                                </div><!-- col-sm-3 -->
                            </div><!-- row -->
                        </div><!-- margin-top -->
                    % endif
                    % if role == 'Bookmarked': 
                        <% f = followLib.getFollow(c.user, workshop) %>
                        % if f:
                            <div style="margin-top: 10px;">
                                <%
                                    itemsChecked = ''
                                    digestChecked = ''
                                    if 'itemAlerts' in f and f['itemAlerts'] == '1':
                                        itemsChecked = 'checked'
                                    if 'digest' in f and f['digest'] == '1':
                                        digestChecked = 'checked'
                                %>
                                <div class="row" ng-controller="followerController">
                                    <div class="col-sm-3">Email when:</div>
                                    <div class="col-sm-3">
                                        <form ng-init="code='${workshop['urlCode']}'; url='${workshop['url']}'; user='${c.user['urlCode']}'" class="no-bottom form-inline">
                                            New Items: <input type="checkbox" name="itemAlerts" value="items" ng-click="emailOnAdded()" ${itemsChecked}>
                                            <span ng-show="emailOnAddedShow">{{emailOnAddedResponse}}</span>
                                        </form>
                                    </div><!-- col-sm-3 -->
                                    <div class="col-sm-3">
                                        <form ng-init="code='${workshop['urlCode']}'; url='${workshop['url']}'; user='${c.user['urlCode']}'" class="no-bottom form-inline">
                                            Weekly Digest: <input type="checkbox" name="digest" value="items" ng-click="emailDigest()" ${digestChecked}>
                                            <span ng-show="emailDigestShow">{{emailDigestResponse}}</span>
                                        </form>
                                    </div><!-- col-sm-3 -->
                                </div><!-- row -->
                            </div><!-- margin-top -->
                        % endif
                    % endif
                    % if role == 'Private':
                        <div style="margin-top: 10px;">
                            <% 
                                p = pmemberLib.getPrivateMember(workshop['urlCode'], c.user['email'])
                                itemsChecked = ''
                                digestChecked = ''
                                if 'itemAlerts' in p and p['itemAlerts'] == '1':
                                        itemsChecked = 'checked'
                                if 'digest' in p and p['digest'] == '1':
                                        digestChecked = 'checked'
                            %>
                            <div class="row" ng-controller="pmemberController">
                                <div class="col-sm-3">Email when:</div>
                                <div class="col-sm-3">
                                    <form ng-init="code='${workshop['urlCode']}'; url='${workshop['url']}'; user='${c.user['urlCode']}'" class="no-bottom form-inline">
                                        New Items: <input type="checkbox" name="itemAlerts" value="items" ng-click="emailOnAdded()" ${itemsChecked}>
                                        <span ng-show="emailOnAddedShow">{{emailOnAddedResponse}}</span>
                                    </form>
                                </div><!-- col-sm-3 -->
                                <div class="col-sm-3">
                                    <form ng-init="code='${workshop['urlCode']}'; url='${workshop['url']}'; user='${c.user['urlCode']}'" class="no-bottom form-inline">
                                        Weekly Digest: <input type="checkbox" name="digest" value="items" ng-click="emailDigest()" ${digestChecked}>
                                        <span ng-show="emailDigestShow">{{emailDigestResponse}}</span>
                                    </form>
                                </div><!-- col-sm-3 -->
                            </div><!-- row -->
                        </div><!-- margin-top -->
                    % endif
                % endif
            % endif
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
                        % if 'workshopCode' in thing:
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
                            % if thing.objType == 'idea':
                                % if thing['adopted'] == '1':
                                    <br/><i class="icon-star"></i> This idea adopted!
                                % endif
                            % endif
                            <br />
                            Description: ${lib_6.ellipsisIZE(descriptionText, 135)}
                        % elif 'initiativeCode' in thing and thing.objType == 'resource':
                            <%
                                initiative = initiativeLib.getInitiative(thing['initiativeCode'])
                                initiativeLink = "/initiative/" + initiative['urlCode'] + "/" + initiative['url']
                                thingLink = initiativeLink + "/resource/" + thing['urlCode'] + "/" + thing['url']
                            %>
                            ${showInitiative(initiative, imageOnly = True)}
                            <a href="${thingLink}"> ${lib_6.ellipsisIZE(thing['title'], 60)} </a> in initiative <a href="${initiativeLink}"> ${initiative['title']} </a> on <span class="green">${thing.date.strftime('%b %d, %Y')}</span>
                        % endif
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
                % if c.listingType == 'watching' or c.listingType == 'listening' or c.listingType == 'facilitating':
                    <table class="table table-condensed table-hover user-thing-listing">
                        <tbody>
                            <% counter = 0 %>
                            % for thing in things:
                                % if counter == 0:
                                    <tr> <td class="no-border">
                                % else:
                                    <tr> <td>
                                % endif
                                %if thing.objType == 'workshop':
                                    ${showWorkshop(thing, imageOnly = True)}
                                    <span class="label label-info">Workshop</span> <a ${lib_6.workshopLink(thing, embed=True) | n}> ${lib_6.ellipsisIZE(thing['title'], 60)} </a>
                                    <br />
                                    Description: ${lib_6.ellipsisIZE(thing['description'], 135)}
                                % elif thing.objType == 'initiative':
                                    ${showInitiative(thing)}
                                % endif

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
            <button data-URL-list="profile_${c.user['urlCode']}_${c.user['url']}" class="btn btn-success  followButton following">
            <span><i class="icon-user icon-white"></i><strong> Following </strong></span>
            </button>
        % else:
            <button data-URL-list="profile_${c.user['urlCode']}_${c.user['url']}" class="btn btn-default followButton unfollow">
            <span><i class="icon-user med-green"></i><strong> Follow </strong></span>
            </button>
        % endif
        </span>
    % endif
</%def>

<%def name="showMemberPosts(activity)">
    <%
        actionMapping = {   'resource': 'added the resource',
                            'discussion': 'started the conversation',
                            'idea': 'posed the idea',
                            'photo': 'added the picture',
                            'initiative': 'launched the initiative',
                            'comment': 'commented on a'}

        objTypeMapping = {  'resource':'resource',
                            'discussion':'conversation',
                            'idea':'idea',
                            'photo':'photo',
                            'initiative':'initiative',
                            'comment':'comment'}
    %>
    <table class="table table-hover table-condensed">
        <tbody>
        
        % for item in activity:
            <% 
                origObjType = item.objType
                objType = item.objType.replace("Unpublished", "")
                activityStr = actionMapping[objType]
                
                if 'workshopCode' in item:
                    workshopLink = "/workshop/" + item['workshopCode'] + "/" + item['workshop_url']
                else:
                    workshopCode = "photo"
                    workshopLink = "/foo/photo"
                parent = False

                if objType == 'comment':
                    if 'workshopCode' in item:
                        if 'ideaCode' in item:
                            parentCode = item['ideaCode']
                            parentURL = item['parent_url']
                            parentObjType = 'idea'
                        elif 'resourceCode' in item:
                            parentCode = item['resourceCode']
                            parentURL = item['parent_url']
                            parentObjType = 'resource'
                        elif 'discussionCode' in item:
                            parentCode = item['discussionCode']
                            parentURL = item['parent_url']
                            parentObjType = 'discussion'
                        parentLink = workshopLink + "/" + parentObjType + "/" + parentCode + "/" + parentURL
                    elif 'photoCode' in item:
                        parentCode = item['photoCode']
                        parentURL = item['parent_url']
                        parentObjType = 'photo'
                        parentLink = "/profile/" + item['profileCode'] + "/" + item['profile_url'] + "/photo/show/" + parentCode
                    elif 'initiativeCode' in item and 'resourceCode' in item:
                        parentCode = item['resourceCode']
                        parentURL = item['parent_url']
                        parentObjType = 'resource'
                        parentLink = "/initiative/" + item['initiativeCode'] + "/" + item['initiative_url'] + "/resource/"+ parentCode + "/" + parentURL
                    elif 'initiativeCode' in item:
                        parentCode = item['initiativeCode']
                        parentURL = item['parent_url']
                        parentObjType = 'initiative'
                        parentLink = "/initiative/" + parentCode + "/" + parentURL + "/show/"
                    elif 'meetingCode' in item:
                        parentCode = item['meetingCode']
                        parentURL = item['meeting_url']
                        parentObjType = 'meeting'
                        parentLink = "/meeting/" + parentCode + "/" + parentURL + "/show/"
                    elif 'profileCode' in item:
                        # not a photo, must be an organization discussion
                        parentLink = "/profile/" + item['profileCode'] + "/" + item['profile_url'] + "/discussion/show/" + item['discussionCode']
                        parentCode = item['discussionCode']
                        parentObjType = 'discussion'
                        parentURL = item['parent_url']
                    else:
                        log.info("no parentObjType item is %s"%item.keys())
                        parentObjType = ""
                        parentURL = ""
                        parentCode = ""
                        parentLink = workshopLink + "/" + parentObjType + "/" + parentCode + "/" + parentURL
                        
                    title = lib_6.ellipsisIZE(item['data'], 40)
                    itemLink = parentLink + '?comment=' + item['urlCode']
                elif objType == 'resource' and 'initiativeCode' in item:
                        parentCode = item['initiativeCode']
                        parentURL = item['initiative_url']
                        parentObjType = 'initiative'
                        title = lib_6.ellipsisIZE(item['title'], 40)
                else:
                    parentCode = False
                    title = lib_6.ellipsisIZE(item['title'], 40)
                    itemLink = workshopLink + "/" + objType + "/" + item['urlCode'] + "/" + item['url']
            %>

            % if objType == 'photo':
                <% 
                    link = "/profile/" + item['userCode'] + "/" + item['user_url'] + "/photo/show/" + item['urlCode']
                    activityStr = "added the picture <a href=\"" + link + "\">" + title + "</a>"
                
                %>
                % if item['deleted'] == '0':
                    <tr><td>${activityStr | n}</td></tr>
                % endif
            % elif objType == 'initiative':
                <% 
                    link = "/initiative/" + item['urlCode'] + "/" + item['url'] + "/show"
                    activityStr = "launched the initiative <a href=\"" + link + "\">" + title + "</a>"
                
                %>
                % if (item['deleted'] == '0' and item['public'] == '1') or 'Unpublished' in origObjType:
                    <tr><td>${activityStr | n}</td></tr>
                % endif
            % elif objType == 'resource' and 'initiativeCode' in item:
                <% 
                    link = "/initiative/" + parentCode + "/" + parentURL + "/resource/" + item['urlCode'] + "/" + item['url']
                    activityStr = "added the resource <a href=\"" + link + "\">" + title + "</a>"
                
                %>
                % if item['deleted'] == '0' and item['initiative_public'] == '1':
                    <tr><td>${activityStr | n}</td></tr>
                % endif
            % elif objType == 'comment' and 'initiativeCode' in item and 'resourceCode' in item:
                <% 
                        activityStr = "commented on a <a href=\"" + parentLink + "\">resource</a>, saying"
                        activityStr += " <a href=\"" + itemLink + "\" class=\"expandable\">" + title + "</a>"
                %>
                % if item['deleted'] == '0' and item['initiative_public'] == '1':
                    <tr><td>${activityStr | n} </td></tr>
                % endif
            % elif objType == 'comment' and 'discType' in item and item['discType'] == 'organization_position':
                <% 
                    if 'initiativeCode' in item:
                        pItem = 'initiative'
                    else:
                        pItem = 'idea'
                    link = "/profile/" + item['userCode'] + "/" + item['user_url'] + "/position/show/" + item['discussionCode']
                    activityStr = "commented on an organization <a href=\"" + link + "\">position</a>, saying"
                    activityStr += " <a href=\"" + link + "\" class=\"expandable\">" + title + "</a>"
                %>
                % if item['deleted'] == '0':
                    <tr><td>${activityStr | n} </td></tr>
                % endif
            % elif objType == 'comment' and 'initiativeCode' in item:
                <% 
                        activityStr = "commented on an <a href=\"" + parentLink + "\">initiative</a>, saying"
                        activityStr += " <a href=\"" + itemLink + "\" class=\"expandable\">" + title + "</a>"
                %>
                % if item['deleted'] == '0' and ('initiative_public' in item and item['initiative_public'] == '1'):
                    <tr><td>${activityStr | n} </td></tr>
                % endif
            % elif objType == 'comment' and 'meetingCode' in item:
                <% 
                        activityStr = "commented on a <a href=\"" + parentLink + "\">meeting agenda item</a>, saying"
                        activityStr += " <a href=\"" + itemLink + "\" class=\"expandable\">" + title + "</a>"
                %>
                % if item['deleted'] == '0':
                    <tr><td>${activityStr | n} </td></tr>
                % endif
            
            % elif objType == 'comment' and 'photoCode' in item:
                <% 
                    activityStr = "commented on a <a href=\"" + parentLink + "\">picture</a>, saying"
                    activityStr += " <a href=\"" + itemLink + "\" class=\"expandable\">" + title + "</a>"
                %>
                % if item['deleted'] == '0':
                    <tr><td>${activityStr | n} </td></tr>
                % endif
            % elif objType == 'discussion' and item['discType'] == 'organization_general':
                <% 
                    link = "/profile/" + item['userCode'] + "/" + item['user_url'] + "/discussion/show/" + item['urlCode']
                    activityStr = "started the organization forum topic "
                    activityStr += " <a href=\"" + link + "\" class=\"expandable\">" + title + "</a>"
                %>
                % if item['deleted'] == '0':
                    <tr><td>${activityStr | n} </td></tr>
                % endif
            % elif objType == 'discussion' and item['discType'] == 'organization_position':
                <% 
                    if 'initiativeCode' in item:
                        pItem = 'initiative'
                        pTitle = item['initiative_title']
                    else:
                        pItem = 'idea'
                        pTitle = item['idea_title']
                    link = "/profile/" + item['userCode'] + "/" + item['user_url'] + "/position/show/" + item['urlCode']
                    activityStr = "took a position to %s the %s "%(item['position'], pItem)
                    activityStr += " <a href=\"" + link + "\" class=\"expandable\">" + pTitle + "</a>"
                %>
                % if item['deleted'] == '0':
                    <tr><td>${activityStr | n} </td></tr>
                % endif
            % elif objType == 'comment' and 'profileCode' in item:
                <% 
                    activityStr = "commented on an organization forum <a href=\"" + parentLink + "\">discussion</a>, saying"
                    activityStr += " <a href=\"" + itemLink + "\" class=\"expandable\">" + title + "</a>"
                %>
                % if item['deleted'] == '0':
                    <tr><td>${activityStr | n} </td></tr>
                % endif
            % elif 'workshopCode' in item:
                % if item['workshop_searchable'] == '1' or (c.browser == False or c.isAdmin == True or c.isUser == True):
                    % if item['deleted'] == '0':
                        <% 
                            if objType == 'comment':
                                if parentObjType == 'idea':
                                    activityStr += 'n'
                                activityStr += ' <a href="' + parentLink + '">' + objTypeMapping[parentObjType] + '</a>, saying'
                                activityStr += ' <a href="' + itemLink + '" class="expandable">' + title + '</a>'
                            else:
                                activityStr += ' <a href="' + itemLink + '" class="expandable">' + title + '</a>'
                        %>
                        <tr><td>${activityStr | n}</td></tr>
                    % endif
                % endif
            % endif
        % endfor
        </tbody>
    </table>
</%def>

<%def name="showMemberActivity(activity)">
    <%
        actionMapping = {   'resource': 'added the resource',
                            'discussion': 'started the conversation',
                            'idea': 'posed the idea',
                            'photo': 'added the picture',
                            'comment': 'commented on a'}
        objTypeMapping = {  'resource':'resource',
                            'discussion':'conversation',
                            'idea':'idea',
                            'photo':'photo',
                            'comment':'comment'}
    %>
    <table class="table table-hover table-condensed">
        <tbody>
        
        % for itemCode in activity['itemList']:
            <% 
                objType = activity['items'][itemCode]['objType']
                activityStr = actionMapping[objType]
                
                if 'workshopCode' in activity['items'][itemCode]:
                    workshopCode = activity['items'][itemCode]['workshopCode']
                    workshopLink = "/workshop/" + activity['workshops'][workshopCode]['urlCode'] + "/" + activity['workshops'][workshopCode]['url']
                else:
                    workshopCode = "photo"
                    workshopLink = "/foo/photo"
                parent = False
                if activity['items'][itemCode]['objType'] == 'comment':
                    parentCode = activity['items'][itemCode]['parentCode']
                    parentObjType = activity['parents'][parentCode]['objType']
                    if parentObjType == 'photo':
                        ownerID = activity['parents'][parentCode]['owner']
                        owner = userLib.getUserByID(ownerID)
                        parentLink = "/profile/" + owner['urlCode'] + "/" + owner['url'] + "/photo/show/" + parentCode
                    else:
                        parentLink = workshopLink + "/" + parentObjType + "/" + activity['parents'][parentCode]['urlCode'] + "/" + activity['parents'][parentCode]['url']
                    title = lib_6.ellipsisIZE(activity['items'][itemCode]['data'], 40)
                    itemLink = parentLink + '?comment=' + itemCode
                else:
                    parentCode = False
                    title = lib_6.ellipsisIZE(activity['items'][itemCode]['title'], 40)
                    itemLink = workshopLink + "/" + activity['items'][itemCode]['objType'] + "/" + activity['items'][itemCode]['urlCode'] + "/" + activity['items'][itemCode]['url']

                
            %>

            % if objType == 'photo':
                <% 
                    ownerID = activity['items'][itemCode]['owner']
                    owner = userLib.getUserByID(ownerID)
                    title = activity['items'][itemCode]['title']
                    urlCode = activity['items'][itemCode]['urlCode']
                    link = "/profile/" + owner['urlCode'] + "/" + owner['url'] + "/photo/show/" + urlCode
                    activityStr = "added the picture <a href=\"" + link + "\">" + title + "</a>"
                
                %>
                % if activity['items'][itemCode]['deleted'] == '0':
                    <tr><td>${activityStr | n}</td></tr>
                % endif
            % elif objType == 'comment' and workshopCode == 'photo':
                <% 
                    if parentCode and activity['parents'][parentCode]['deleted'] != '1':
                        activityStr = "commented on a <a href=\"" + parentLink + "\">picture</a>, saying"
                        activityStr += " <a href=\"" + itemLink + "\" class=\"expandable\">" + title + "</a>"
                %>
                <tr><td>${activityStr | n} </td></tr>
            % else:
                % if activity['workshops'][workshopCode]['public_private'] == 'public' or (c.browser == False or c.isAdmin == True or c.isUser == True):
                    % if activity['items'][itemCode]['deleted'] == '0':
                        <% 
                            if parentCode and activity['parents'][parentCode]['deleted'] == '1':
                                continue
                            
                            if objType == 'comment':
                                if parentObjType == 'idea':
                                    activityStr += 'n'
                                activityStr += ' <a href="' + parentLink + '">' + objTypeMapping[parentObjType] + '</a>, saying'
                                activityStr += ' <a href="' + itemLink + '" class="expandable">' + title + '</a>'
                            else:
                                activityStr += ' <a href="' + itemLink + '" class="expandable">' + title + '</a>'
                        %>
                        <tr><td>${activityStr | n}</td></tr>
                    % endif
                % endif
            % endif
        % endfor
        </tbody>
    </table>
</%def>

<%def name="showActivity(activity)">
    <table class="table table-hover table-condensed">
        <tbody>
        
        % for item in activity:
            <% workshop = workshopLib.getWorkshopByCode(item['workshopCode']) %>
            % if workshop['public_private'] == 'public' or (c.browser == False or c.isAdmin == True or c.isUser == True): 
                <tr><td>${lib_6.showItemInActivity(item, workshop, expandable = True)}</td></tr>
            % endif
        % endfor
        </tbody>
    </table>
</%def>

<%def name="inviteCoFacilitate()">
    % if 'user' in session and c.authuser:
        <%
            fList = facilitatorLib.getFacilitatorsByUser(c.authuser)
            wListF = []
            wListL = []
            for f in fList:
                if not 'initiativeCode' in f:
                    w = workshopLib.getWorkshopByCode(f['workshopCode'])
                    if w['deleted'] == '0':
                        wlisten = listenerLib.getListener(c.user['email'], w)
                        if not facilitatorLib.isFacilitator(c.user, w) and not facilitatorLib.isPendingFacilitator(c.user, w):
                            wListF.append(w)
                        if (not wlisten or wlisten['disabled'] == '1') and w['type'] != 'personal':
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
                    <input type="text" name="lTitle" placeholder="Title or Description" required>
                </form>
                </div>
            </div><!-- row -->
        % endif
    %endif
</%def>

<%def name="showDiscussions()">
    <% discussions = discussionLib.getDiscussionsForOrganization(c.user) %>
    % for d in discussions:
        <% url = "/profile/" + c.user['urlCode'] + "/" + c.user['url'] + "/discussion/show/" + d['urlCode'] %>
        <div class="row-fluid">
            <h3><a href="${url}" class="listed-item-title">${d['title']}</a></h3>
            ${lib_6.userLink(d.owner)} from ${lib_6.userGeoLink(d.owner)}${lib_6.userImage(d.owner, className="avatar med-avatar")}</br>
            posted ${fuzzyTime.timeSince(d.date)} ago ${str(d['numComments'])} comments <i class="icon-eye-open"></i> ${str(d['views'])} views</br>
        </div><!-- row-fluid -->
    % endfor        
</%def>

<%def name="showDiscussion()">
    <%
        url = "/profile/" + c.user['urlCode'] + "/" + c.user['url'] + "/discussion/show/" + c.discussion['urlCode']
        role = ''
        if 'addedAs' in c.discussion.keys():
            roles = ['admin', 'facilitator', 'listener']
            if c.discussion['addedAs'] in roles:
                role = ' (%s)' % c.discussion['addedAs']
    %>
    <div class="row-fluid">
        <div class="span2">
            ${lib_6.upDownVote(c.discussion)}
        </div><!-- span2 -->
        <div class="span10">
            <h3><a href="${url}" class="listed-item-title">${c.discussion['title']}</a></h3>
            % if 'text' in c.discussion.keys():
                ${misaka.html(c.discussion['text']) | n}
            % endif
            ${lib_6.userLink(c.discussion.owner)}${role} from ${lib_6.userGeoLink(c.discussion.owner)}${lib_6.userImage(c.discussion.owner, className="avatar med-avatar")}
            % if c.discussion.objType == 'discussion':
                <br />Originally posted  ${c.discussion.date}
                <i class="icon-eye-open"></i> ${str(c.discussion['views'])} views
            % endif 
        </div><!-- span10 -->
    </div><!-- row-fluid -->
</%def>

<%def name="showPositions()">
    <% discussions = discussionLib.getPositionsForOrganization(c.user) %>
    % for d in discussions:
        <% url = "/profile/" + c.user['urlCode'] + "/" + c.user['url'] + "/position/show/" + d['urlCode'] %>
        <div class="well">
            <div class="row">
                <div class="col-xs-12">
                    <h3><a href="${url}" class="listed-item-title">${d['title']}</a></h3>
                    <p>posted ${fuzzyTime.timeSince(d.date)} ago | ${str(d['numComments'])} comments | <i class="icon-eye-open"></i> ${str(d['views'])} views</p>
                </div>
            </div><!-- row -->
        </div>
    % endfor        
</%def>

<%def name="showPosition()">
    <%
        url = "/profile/" + c.user['urlCode'] + "/" + c.user['url'] + "/position/show/" + c.discussion['urlCode']
        role = ''
        if 'addedAs' in c.discussion.keys():
            roles = ['admin', 'facilitator', 'listener']
            if c.discussion['addedAs'] in roles:
                role = ' (%s)' % c.discussion['addedAs']

        if 'initiativeCode' in c.discussion:
            parentType = 'initiative'
            parentURL = "/initiative/%s/%s/show"%(c.discussion['initiativeCode'], c.discussion['initiative_url'])
            parentTitle = c.discussion['initiative_title']
        else:
            parentType = 'idea'
            if 'workshopCode' in c.discussion:
                parentURL = "/workshop/%s/%s/idea/%s/%s"%(c.discussion['workshopCode'], c.discussion['workshop_url'], c.discussion['ideaCode'], c.discussion['idea_url'])
            else:
                parentURL = "/idea/%s/%s"%(c.discussion['ideaCode'], c.discussion['idea_url'])
            parentTitle = c.discussion['idea_title']
    %>
    <div class="row">
        <div class="col-xs-12">
            <h3><a href="${url}" class="listed-item-title">${c.discussion['title']}</a></h3>
            View ${parentType}: <a href="${parentURL}">${parentTitle}</a>
            <div class="spacer"></div>
            % if 'text' in c.discussion.keys():
                ${misaka.html(c.discussion['text']) | n}
            % endif
            ${lib_6.userLink(c.discussion.owner)}${role} from ${lib_6.userGeoLink(c.discussion.owner)}${lib_6.userImage(c.discussion.owner, className="avatar med-avatar")}
            % if c.discussion.objType == 'discussion':
                <br />Originally posted  ${c.discussion.date}
                <i class="icon-eye-open"></i> ${str(c.discussion['views'])} views
            % endif 
        </div><!-- col-xs-11 -->
    </div><!-- row -->
</%def>

<%def name="addTopic()">
    <div class="row">
        <div class="col-xs-12">
            <form class="well" ng-controller="topicController" ng-init="userCode = '${c.user['urlCode']}'; userURL = '${c.user['url']}'; topicCode = 'new'; addTopicTitleResponse=''; addUpdateTextResponse=''; addTopicResponse='';"  id="addTopicForm" name="addTopicForm" ng-submit="submitTopicForm(addTopicForm)">
                <div class="row">
                    <div class="col-xs-1 form-group">
                        ${lib_6.userImage(c.authuser, className="avatar med-avatar", linkClass="topbar-avatar-link")}
                    </div>
                    <div class="col-xs-11">
                        <div class="form-group">
                            <label><strong ng-cloak>Title</strong></label>
                            <input type="text" class="input-block-level form-control" name="title" ng-model="title" maxlength = "120" placeholder="Start a discussion topic..." required>
                            <span ng-show="addTopicTitleShow"><div class="alert alert-danger" ng-cloak>{{addTopicTitleResponse}}</div></span>
                        </div>
                        <div class="form-group"ng-cloak>
                            <label ><strong>Topic Description</strong>
                            <a href="#" class="btn btn-xs btn-info" onclick="window.open('/help/markdown.html','popUpWindow','height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');"><i class="icon-list"></i> <i class="icon-photo"></i> View Formatting Guide</a></label>
                            <textarea name="text" rows="3" class="input-block-level form-control" ng-model="text" placeholder="Describe the topic you wish to discuss in the forum."></textarea>
                            <span ng-show="addTopicTextShow"><div class="alert alert-danger" ng-cloak>{{addTopicTextResponse}}</div></span>
                        </div>
                        <div class="form-group">
                            <button class="btn btn-success pull-right" type="submit" name="submit">Submit</button>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </div>
</%def>

<%def name="profileModerationPanel(thing)">
    <%
        if 'user' not in session or thing.objType == 'revision':
            return
        flagID = 'flag-%s' % thing['urlCode']
        editID = 'edit-%s' % thing['urlCode']
        adminID = 'admin-%s' % thing['urlCode']
        publishID = 'publish-%s' % thing['urlCode']
        unpublishID = 'unpublish-%s' % thing['urlCode']
    %>
    <div class="btn-group">
        % if thing['disabled'] == '0':
            <a class="btn btn-default btn-sm accordion-toggle" data-toggle="collapse" data-target="#${flagID}">flag</a>
        % endif
        % if c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id):
            <a class="btn btn-default btn-sm accordion-toggle" data-toggle="collapse" data-target="#${editID}">edit</a>
        % endif
        % if userLib.isAdmin(c.authuser.id):
            <a class="btn btn-default btn-sm accordion-toggle" data-toggle="collapse" data-target="#${adminID}">admin</a>
        % endif

    </div>
    
    % if thing['disabled'] == '0':
        ${lib_6.flagThing(thing)}
        % if (c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id)):
            ${lib_6.editThing(thing)}
            % if userLib.isAdmin(c.authuser.id):
                ${lib_6.adminThing(thing)}
            % endif
        % endif
    % else:
        % if userLib.isAdmin(c.authuser.id):
            ${lib_6.editThing(thing)}
        % endif
        % if userLib.isAdmin(c.authuser.id):
            ${lib_6.adminThing(thing)}
        % endif
    % endif
</%def>

<%def name="horizontalDashboard()">
    <div class="well">
        <div ng-init="dashboardFullName='${c.user['name']}'; greetingMsg='${c.user['greetingMsg']}'; fullName='${c.user['name']}'; websiteDesc='${c.user['websiteDesc']}'; websiteLink='${c.user['websiteLink']}'; zipValue='${c.user['postalCode']}'; postalCode='${c.user['postalCode']}'; updateGeoLinks();">
            <div class="row">
                % if c.user['memberType'] != 'organization':
                <div class="col-sm-7">
                    <h1 ng-cloak>{{fullName}}</h1>
                    <p class="grey" ng-cloak>{{greetingMsg}}</p>
                </div>
                <div class="col-sm-5 top-space-md">
                    <!-- user flags -->
                    <div ng-controller="zipLookupCtrl" style="float: right;">
                        <table ng-show="!loading">
                            <tr>
                                <td ng-repeat="geo in geos">
                                    <a href="{{geo.href}}" tooltip-placement="right" tooltip="{{geo.name}}"><img class="thumbnail flag med-flag bottom-space border" src="{{geo.flag}}" ng-cloak></a>
                                </td>
                            </tr>
                        </table>
                        <p>${lib_6.userGeoLink(c.user)}</p>
                    </div><!-- ng-controller -->
                </div>
                % else:
                <div class="col-sm-12">
                    <h1 ng-cloak>{{fullName}}</h1>
                    <p class="grey" ng-cloak>
                        {{greetingMsg}}
                        <span ng-if="greetingMsg != ''"> | </span>
                        <a ng-href="websiteLink" ng-cloak>{{websiteLink}}</a>
                    </p>
                </div>
                % endif
            </div>
            <hr>
            <div class="row">
                <div class="col-xs-12">
                    <span class="profile-dash-button pull-right">
                        % if c.user['email'] == c.authuser['email']:
                            <a class="btn btn-default" href="/profile/${c.user['urlCode']}/${c.user['url']}/edit"><strong>Edit Profile</strong></a>
                        % else:
                            ${followButton(c.user)}
                        % endif
                    </span>

                    % if c.user['memberType'] != 'organization':
                        <table id="metrics" class="table-inline">
                            <tr>
                                <td style="padding-left: 0px;">
                                    <% 
                                        thingListingURL = "/profile/%s/%s/ideas" %(c.user['urlCode'], c.user['url'])
                                        if 'idea_counter' in c.user:
                                            numThings = c.user['idea_counter']
                                        else:
                                            numThings = '0'
                                    %>
                                    <span class="workshop-metrics">Ideas</span><br>
                                      <strong ng-cloak><span class="black">${numThings}</span></strong>
                                </td>
                                <td>
                                    <% 
                                        thingListingURL = "/profile/%s/%s/discussions" %(c.user['urlCode'], c.user['url'])
                                        if 'discussion_counter' in c.user:
                                            numThings = c.user['discussion_counter']
                                        else:
                                            numThings = '0'
                                    %>
                                    <span class="workshop-metrics">Discussions</span><br>
                                      <strong ng-cloak><span class="black">${numThings}</span></strong>
                                </td>
                                <td>
                                    <% 
                                        thingListingURL = "/profile/%s/%s/resources" %(c.user['urlCode'], c.user['url'])
                                        if 'resource_counter' in c.user:
                                            numThings = c.user['resource_counter']
                                        else:
                                            numThings = '0'
                                    %>
                                    <span class="workshop-metrics">Resources</span><br>
                                      <strong ng-cloak><span class="black">${numThings}</span></strong>
                                </td>
                                <td>
                                    <% 
                                        thingListingURL = "/profile/%s/%s/followers" %(c.user['urlCode'], c.user['url'])
                                        if 'follower_counter' in c.user:
                                            numThings = c.user['follower_counter']
                                        else:
                                            numThings = '0'
                                    %>
                                    <span class="workshop-metrics">Followers</span><br>
                                      <strong ng-cloak><span class="black">${numThings}</span></strong>
                                </td>
                            </tr>
                        </table>
                    % endif
                </div><!-- col-xs-12 -->
            </div><!-- row -->
        </div>
    </div>
</%def>

