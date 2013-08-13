<%!
    import pylowiki.lib.db.workshop     as workshopLib
    import pylowiki.lib.db.facilitator  as facilitatorLib
    import pylowiki.lib.db.listener     as listenerLib
    import pylowiki.lib.db.follow       as followLib
    import pylowiki.lib.db.user         as userLib
    import pylowiki.lib.db.pmember      as pmemberLib
    import pylowiki.lib.utils           as utils
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
            if 'role' in kwargs:
                role = kwargs['role']
            else:
                role = ''
        %>
        <div class="media-body">
            <a ${lib_6.workshopLink(workshop)}><h5 class="media-heading"><span class="label label-inverse">${role}</span> ${workshop['title']}</h5></a>
            ${workshop['description']}<br />
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
                                        Daily Digest: <input type="checkbox" name="digest" value="items" ng-click="emailDigest()" ${digestChecked}>
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
                                        Daily Digest: <input type="checkbox" name="digest" value="items" ng-click="emailDigest()" ${digestChecked}>
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
                                            Daily Digest: <input type="checkbox" name="digest" value="items" ng-click="emailDigest()" ${digestChecked}>
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
                                        Daily Digest: <input type="checkbox" name="digest" value="items" ng-click="emailDigest()" ${digestChecked}>
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
            <button data-URL-list="profile_${c.user['urlCode']}_${c.user['url']}" class="btn-civ btn round pull-right followButton following">
            <span><i class="icon-user icon-white"></i> Following </span>
            </button>
        % else:
            <button data-URL-list="profile_${c.user['urlCode']}_${c.user['url']}" class="btn round pull-right followButton unfollow">
            <span><i class="icon-user"></i> Follow </span>
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
            %if ('user' in session and c.user.id == c.authuser.id) or c.isAdmin:
                <div ng-init="updateGeoLinks(); dashboardFullName='${c.user['name']}'">
                    <h3 class="section-header">{{fullName}}</h3>
                    <p><a href="{{cityURL}}">{{cityTitle}}</a>, <a href="{{stateURL}}">{{stateTitle}}</a>, <a href="{{countryURL}}">{{countryTitle}}</a>
                </div>
            %else:
                <h3 class="section-header">${c.user['name']}</h3>
                <p>${lib_6.userGeoLink(c.user)}</p>
            %endif
            
            <p>Joined ${c.user.date.strftime('%b %d, %Y')}</p>
            % if c.user['greetingMsg'] != '':
                %if ('user' in session and c.user.id == c.authuser.id) or c.isAdmin:
                    <div ng-init="dashboardGreetingMsg='${c.user['greetingMsg']}'">
                    <small class="muted expandable">{{greetingMsg}}</small>
                %else:
                    <small class="muted expandable">${c.user['greetingMsg']}</small>
                %endif
            % endif
            % if c.user['websiteLink'] != '':
                %if ('user' in session and c.user.id == c.authuser.id) or c.isAdmin:
                    <div ng-init="dashboardWebsiteLink='${c.user['websiteLink']}'">
                    <p class = "expandable no-bottom"><a href="{{dashboardWebsiteLink}}" target="_blank">{{dashboardWebsiteLink}}</a></p>
                %else:
                    <p class = "expandable no-bottom"><a href="${c.user['websiteLink']}" target="_blank">${c.user['websiteLink']}</a></p>
                % endif
                % if c.user['websiteDesc'] != '':
                    %if ('user' in session and c.user.id == c.authuser.id) or c.isAdmin:
                        <div ng-init="dashboardWebsiteDesc='${c.user['websiteDesc']}'">
                            <small class="muted expandable">{{websiteDesc}}</small>
                        </div>
                    %else:
                        <small class="muted expandable">${c.user['websiteDesc']}</small>
                    %endif
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
        </div><!--/.browse-->
    </div><!--/.section-wrapper-->
</%def>

<%def name="showMemberActivity(activity)">
    <%
        actionMapping = {   'resource': 'added the resource',
                            'discussion': 'started the conversation',
                            'idea': 'posed the idea',
                            'comment': 'commented on a'}
        objTypeMapping = {  'resource':'resource',
                            'discussion':'conversation',
                            'idea':'idea',
                            'comment':'comment'}
    %>
    <table class="table table-hover table-condensed">
        <tbody>
        
        % for itemCode in activity['itemList']:
            <% 
                workshopCode = activity['items'][itemCode]['workshopCode']
                workshopLink = "/workshop/" + activity['workshops'][workshopCode]['urlCode'] + "/" + activity['workshops'][workshopCode]['url']
                parent = False
                if activity['items'][itemCode]['objType'] == 'comment':
                    parentCode = activity['items'][itemCode]['parentCode']
                    parentObjType = activity['parents'][parentCode]['objType']
                    parentLink = workshopLink + "/" + parentObjType + "/" + activity['parents'][parentCode]['urlCode'] + "/" + activity['parents'][parentCode]['url']
                    title = lib_6.ellipsisIZE(activity['items'][itemCode]['data'], 40)
                    itemLink = parentLink + '?comment=' + itemCode
                else:
                    parentCode = False
                    title = lib_6.ellipsisIZE(activity['items'][itemCode]['title'], 40)
                    itemLink = workshopLink + "/" + activity['items'][itemCode]['objType'] + "/" + activity['items'][itemCode]['urlCode'] + "/" + activity['items'][itemCode]['url']

                
            %>
            % if activity['workshops'][workshopCode]['public_private'] == 'public' or (c.browser == False or c.isAdmin == True or c.isUser == True):
                % if activity['items'][itemCode]['deleted'] == '0':
                    <% 
                        if parentCode and activity['parents'][parentCode]['deleted'] == '1':
                            continue
                            
                        objType = activity['items'][itemCode]['objType']
                        activityStr = actionMapping[objType]
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

<%def name="showProfilePhotos()">
    % if 'user' in session and c.authuser.id == c.user.id:
        <% tagCategories = workshopLib.getWorkshopTagCategories() %>
        <button type="button" class="btn btn-success pull-right" data-toggle="collapse" data-target="#uploadPhoto">
        + Photo
        </button>
        <div id="uploadPhoto" class="collapse">
            <form id="photoupload" name="photoupload" ng-controller="photoUploadController" ng-init="userCode='${c.user['urlCode']}'; userURL='${c.user['url']}';" ng-submit="validateForm(photoupload)" enctype="multipart/form-data">
            <div class="row-fluid">
                <div class="span10">
                    <fieldset>
                    <label>Title</label>
                    <input type="text" ng-model="name" name="title" id="title" maxlength="120" required>
                    <label>Description</label>
                    <textarea name="text" ng-model="text" rows="3" class="input-block-level" required></textarea>
                    <label>Category</label>
                    <select name="categoryTag" ng-model="categoryTag" id="categoryTag">
                    <option value="choose" selected>Choose a category</option>
                    % for category in tagCategories:
                        <option value="${category}">${category.title()}</option>
                    % endfor
                    </select>
                    <div class="spacer"></div>
                    <label>Select picture to upload</label>
                    <input type="file" ng-model="file" name="files[]">
                    <div class="spacer"></div>
                    <div class="control-group">
                        <div class="controls">
                            <button class="btn btn-success disabled" ng-show="photoupload.$invalid" onClick="event.preventDefault(); return 0;">Save and Upload</button>
                            <button type="submit" class="btn btn-success" ng-show="photoupload.$valid">Save and Upload</button>
                        </div><!-- controls -->
                    </div><!-- control-group -->
                    </fieldset>
                    <div id="photoUploadResult"></div>
                </div><!-- span10 -->
            </div><!-- row-fluid -->
            </form>
        
     <div class="section-wrapper" ng-init="code='${c.user['urlCode']}'; url='${c.user['url']}'; uploadImage = 'true'; imageSource = 'civ';">
        <div class="browse">
            <form id="fileupload" action="/profile/${c.authuser['urlCode']}/${c.authuser['url']}/picture/upload/handler" method="POST" enctype="multipart/form-data" data-ng-app="demo" data-fileupload="options" ng-class="{true: 'fileupload-processing'}[!!processing() || loadingFiles]" class = "civAvatarUploadForm">
                <!-- Redirect browsers with JavaScript disabled to the origin page -->
                <noscript>&lt;input type="hidden" name="redirect" value="http://blueimp.github.com/jQuery-File-Upload/"&gt;</noscript>
                <!-- The fileupload-buttonbar contains buttons to add/delete files and start/cancel the upload -->
                <div class="row-fluid fileupload-buttonbar">
                    <div class="span10 offset1">
                        <!-- The fileinput-button span is used to style the file input field as button -->
                        <span class="btn btn-success fileinput-button span6 offset3">
                            <i class="icon-plus icon-white"></i>
                            <span>Select your picture</span>
                            <input type="file" name="files[]">
                        </span>
                        <!-- The loading indicator is shown during file processing -->
                        <div class="fileupload-loading"></div>
                    </div>
                    <!-- The global progress information -->
                </div>
                <div class="row-fluid">
                    <div class="span10 offset1 fade" data-ng-class="{true: 'in'}[!!active()]">
                        <!-- The global progress bar -->
                        <div class="progress progress-success progress-striped active" data-progress="progress()"><div class="bar" ng-style="{width: num + '%'}"></div></div>
                        <!-- The extended global progress information -->
                        <div class="progress-extended">&nbsp;</div>
                    </div>
                </div>
                <!-- The table listing the files available for upload/download -->
                <table class="table table-striped files ng-cloak" data-toggle="modal-gallery" data-target="#modal-gallery">
                    <tbody><tr data-ng-repeat="file in queue">
                        <td data-ng-switch="" on="!!file.thumbnail_url">
                            <div class="preview" data-ng-switch-when="true">
                                <a data-ng-href="{{file.url}}" title="{{file.name}}" data-gallery="gallery" download="{{file.name}}"><img data-ng-src="{{file.thumbnail_url}}"></a>
                            </div>
                            <div class="preview" data-ng-switch-default="" data-preview="file" id="preview"></div>
                        </td>
                        <td>
                            <div ng-show="file.error"><span class="label label-important">Error</span> {{file.error}}</div>
                        </td>
                        <td>
                            <button type="button" class="btn btn-primary start" data-ng-click="file.$submit()" data-ng-hide="!file.$submit">
                                <i class="icon-upload icon-white"></i>
                                <span>Start</span>
                            </button>
                            <button type="button" class="btn btn-warning cancel" data-ng-click="file.$cancel()" data-ng-hide="!file.$cancel">
                                <i class="icon-ban-circle icon-white"></i>
                                <span>Cancel</span>
                            </button>
                        </td>
                    </tr>
                </tbody></table>
            </form>
        </div><!-- browse -->
    </div><!-- section-wrapper -->
    </div>
    % endif
</%def>

<%def name="editProfile()">
    <%namespace file="/lib/derived/6_profile_edit.mako" name="helpersEdit" />
    <%
        tab1active = ""
        tab2active = ""
        tab3active = ""
        tab4active = ""
        tab5active = ""
        tab6active = ''
        prefactive = ''
                    
        if c.tab == "tab1":
            tab1active = "active"
        elif c.tab == "tab2":
            tab2active = "active"
        elif c.tab == "tab3":
            tab3active = "active"
        elif c.tab == "tab4":
            tab4active = "active"
        elif c.tab == "tab5":
            tab5active = "active"
        elif c.tab == 'tab6':
            tab6active = 'tab6'
        else:
            tab1active = "active"
    
        msgString = ''
        if c.unreadMessageCount != 0:
            msgString = ' (' + str(c.unreadMessageCount) + ')'
    %>
    <div class="row-fluid">
        % if c.conf['read_only.value'] == 'true':
            <h1> Sorry, Civinomics is in read only mode right now </h1>
        % else:
            <div class="tabbable">
                <div class="span3">
                    <div class="section-wrapper">
                        <div class="browse">
                            <div style="text-align: center">
                                <h4 class="section-header smaller">Edit Profile</h4>
                            </div><!-- center -->
                            <ul class="nav nav-pills nav-stacked">
                            <li class="${tab1active}"><a href="#tab1" data-toggle="tab">1. Info
                            </a></li>
                            <li class="${tab6active}"><a href="#tab6" data-toggle="tab">2. Picture
                            </a></li>
                            <li class="${tab4active}"><a href="#tab4" data-toggle="tab">3. Password
                            </a></li>
                            <li class="${prefactive}"><a href="#pref" data-toggle="tab">4. Preferences
                            </a></li>
                            % if c.admin:
                            <li class="${tab5active}"><a href="#tab5" data-toggle="tab">5. Administrate
                            Admin only - shhh!.</a></li>
                            % endif
                            </ul>
                            <div>
                                <form method="post" name="CreateWorkshop" id="CreateWorkshop" action="/workshop/display/create/form">
                                <button type="submit" class="btn btn-warning">Create a Workshop!</button>
                                </form>
                            </div><!-- center -->
                        </div><!-- browse -->
                    </div><!-- section-wrapper -->
                </div> <!-- /.span3 -->
                <div class="span9">
                    ${lib_6.fields_alert()}
                    % if c.conf['read_only.value'] == 'true':
                        <!-- read only -->
                    % else:
                        <div class="tab-content">
                            <div class="tab-pane ${tab1active}" id="tab1">
                                ${helpersEdit.profileInfo()}
                            </div><!-- tab1 -->
                            <div class="tab-pane ${tab4active}" id="tab4">
                                ${helpersEdit.changePassword()}
                            </div><!-- tab4 -->
                            <div class="tab-pane ${tab6active}" id="tab6">
                                ${helpersEdit.profilePicture()}
                            </div><!-- tab4 -->
                            <div class="tab-pane ${prefactive}" id="pref">
                                ${helpersEdit.preferences()}
                            </div><!-- preferences -->
                            % if c.admin:
                                <div class="tab-pane ${tab5active}" id="tab5">
                                    ${helpersEdit.memberAdmin()}
                                    ${helpersEdit.memberEvents()}
                                </div><!-- tab5 -->
                            % endif
                        </div><!-- tab-content -->
                    % endif
                </div> <!-- /.span9 -->
            </div><!-- tabbable -->
        % endif
    </div> <!-- /.row-fluid -->
</%def>