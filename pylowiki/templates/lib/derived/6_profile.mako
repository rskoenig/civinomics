<%!
    import pylowiki.lib.db.workshop     as workshopLib
    import pylowiki.lib.db.initiative   as initiativeLib
    import pylowiki.lib.db.facilitator  as facilitatorLib
    import pylowiki.lib.db.listener     as listenerLib
    import pylowiki.lib.db.follow       as followLib
    import pylowiki.lib.db.user         as userLib
    import pylowiki.lib.db.pmember      as pmemberLib
    import pylowiki.lib.db.generic      as genericLib
    import pylowiki.lib.utils           as utils
    
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
            <span class="label label-inverse">Initiative</span> <a href="/initiative/${item['urlCode']}/${item['url']}/show" class="listed-item-title media-heading lead bookmark-title">${item['title']}</a>
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
        <a class="pull-left" ${lib_6.workshopLink(workshop)}>
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
            <a ${lib_6.workshopLink(workshop)} class="listed-item-title media-heading lead bookmark-title">${workshop['title']}</a>
            <span class="label label-inverse pull-right">${role}</span>
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
                            <div class="row-fluid" ng-controller="facilitatorController">
                                <div class="span3">Email when:</div>
                                <div class="span3">
                                    <form ng-init="code='${workshop['urlCode']}'; url='${workshop['url']}'; user='${c.user['urlCode']}'" class="no-bottom form-inline">
                                        New Items: <input type="checkbox" name="flagAlerts" value="flags" ng-click="emailOnAdded()" ${itemsChecked}>
                                        <span ng-show="emailOnAddedShow">{{emailOnAddedResponse}}</span>
                                    </form>
                                </div><!-- span3 -->
                                <div class="span3">
                                    <form ng-init="code='${workshop['urlCode']}'; url='${workshop['url']}'; user='${c.user['urlCode']}'" class="no-bottom form-inline">
                                        New Flags: <input type="checkbox" name="itemAlerts" value="items" ng-click="emailOnFlagged()" ${flagsChecked}>
                                        <span ng-show="emailOnFlaggedShow">{{emailOnFlaggedResponse}}</span>
                                    </form>
                                </div><!-- span3 -->
                                <div class="span3">
                                    <form ng-init="code='${workshop['urlCode']}'; url='${workshop['url']}'; user='${c.user['urlCode']}'" class="no-bottom form-inline">
                                        Weekly Digest: <input type="checkbox" name="digest" value="items" ng-click="emailDigest()" ${digestChecked}>
                                        <span ng-show="emailDigestShow">{{emailDigestResponse}}</span>
                                    </form>
                                </div><!-- span3 -->
                            </div><!-- row-fluid -->
                        </div><!-- margin-top -->
                    % endif
                    % if role == 'Listening':
                        <div style="margin-top: 10px;">
                            <%
                                l = listenerLib.getListener(c.user['email'], workshop)
                                itemsChecked = ''
                                digestChecked = ''
                                if 'itemAlerts' in l and l['itemAlerts'] == '1':
                                    itemsChecked = 'checked'
                                if 'digest' in l and l['digest'] == '1':
                                    digestChecked = 'checked'
                            %>
                            <div class="row-fluid" ng-controller="listenerController">
                                <div class="span3">Email when:</div>
                                <div class="span3">
                                    <form ng-init="code='${workshop['urlCode']}'; url='${workshop['url']}'; user='${c.user['urlCode']}'" class="no-bottom form-inline">
                                        New Items: <input type="checkbox" name="itemAlerts" value="items" ng-click="emailOnAdded()" ${itemsChecked}>
                                        <span ng-show="emailOnAddedShow">{{emailOnAddedResponse}}</span>
                                    </form>
                                </div><!-- span3 -->
                                <div class="span3">
                                    <form ng-init="code='${workshop['urlCode']}'; url='${workshop['url']}'; user='${c.user['urlCode']}'" class="no-bottom form-inline">
                                        Weekly Digest: <input type="checkbox" name="digest" value="items" ng-click="emailDigest()" ${digestChecked}>
                                        <span ng-show="emailDigestShow">{{emailDigestResponse}}</span>
                                    </form>
                                </div><!-- span3 -->
                            </div><!-- row-fluid -->
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
                                <div class="row-fluid" ng-controller="followerController">
                                    <div class="span3">Email when:</div>
                                    <div class="span3">
                                        <form ng-init="code='${workshop['urlCode']}'; url='${workshop['url']}'; user='${c.user['urlCode']}'" class="no-bottom form-inline">
                                            New Items: <input type="checkbox" name="itemAlerts" value="items" ng-click="emailOnAdded()" ${itemsChecked}>
                                            <span ng-show="emailOnAddedShow">{{emailOnAddedResponse}}</span>
                                        </form>
                                    </div><!-- span3 -->
                                    <div class="span3">
                                        <form ng-init="code='${workshop['urlCode']}'; url='${workshop['url']}'; user='${c.user['urlCode']}'" class="no-bottom form-inline">
                                            Weekly Digest: <input type="checkbox" name="digest" value="items" ng-click="emailDigest()" ${digestChecked}>
                                            <span ng-show="emailDigestShow">{{emailDigestResponse}}</span>
                                        </form>
                                    </div><!-- span3 -->
                                </div><!-- row-fluid -->
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
                            <div class="row-fluid" ng-controller="pmemberController">
                                <div class="span3">Email when:</div>
                                <div class="span3">
                                    <form ng-init="code='${workshop['urlCode']}'; url='${workshop['url']}'; user='${c.user['urlCode']}'" class="no-bottom form-inline">
                                        New Items: <input type="checkbox" name="itemAlerts" value="items" ng-click="emailOnAdded()" ${itemsChecked}>
                                        <span ng-show="emailOnAddedShow">{{emailOnAddedResponse}}</span>
                                    </form>
                                </div><!-- span3 -->
                                <div class="span3">
                                    <form ng-init="code='${workshop['urlCode']}'; url='${workshop['url']}'; user='${c.user['urlCode']}'" class="no-bottom form-inline">
                                        Weekly Digest: <input type="checkbox" name="digest" value="items" ng-click="emailDigest()" ${digestChecked}>
                                        <span ng-show="emailDigestShow">{{emailDigestResponse}}</span>
                                    </form>
                                </div><!-- span3 -->
                            </div><!-- row-fluid -->
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
                                    <span class="label label-inverse">Workshop</span> <a ${lib_6.workshopLink(thing, embed=True) | n}> ${lib_6.ellipsisIZE(thing['title'], 60)} </a>
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
            <button data-URL-list="profile_${c.user['urlCode']}_${c.user['url']}" class="btn-civ btn pull-right followButton following">
            <span><i class="icon-user icon-white"></i><strong> Following </strong></span>
            </button>
        % else:
            <button data-URL-list="profile_${c.user['urlCode']}_${c.user['url']}" class="btn pull-right followButton unfollow">
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
                    elif 'profileCode' in item:
                        parentLink = "/profile/" + item['profileCode'] + "/" + item['profile_url'] + "/photo/show/" + parentCode
                    else:
                        log.info("no parentObjType item is %s"%item.keys())
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
                % if item['deleted'] == '0' and item['public'] == '1':
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
            % elif objType == 'comment' and 'initiativeCode' in item:
                <% 
                        activityStr = "commented on an <a href=\"" + parentLink + "\">initiative</a>, saying"
                        activityStr += " <a href=\"" + itemLink + "\" class=\"expandable\">" + title + "</a>"
                %>
                % if item['deleted'] == '0' and item['initiative_public'] == '1':
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
    %if 'user' in session and c.authuser:
        <% 
            fList = facilitatorLib.getFacilitatorsByUser(c.authuser)
            wListF = []
            wListL = []
            for f in fList:
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