<%!
   import pylowiki.lib.db.slideshow as slideshowLib
   from pylowiki.lib.db.user import getUserByID
   import pylowiki.lib.db.activity as activityLib
   import pylowiki.lib.db.facilitator   as facilitatorLib
   import misaka as m
   
   import logging
   log = logging.getLogger(__name__)
%>

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="whoListening()">
    <%
        users = []
        pending = []
        for listener in c.listeners:
            if 'userCode' in listener:
                users.append(listener)
            else:
                pending.append(listener)
    %>
    <h4 class="section-header smaller section-header-inner">Listeners</h4>
    % if users:
        <div class="green"><p>Participating</p></div>
        <ul class="media-list" id="workshopNotables">
        % for person in users:
            <%
                personTitle = person['title']
                personClass = 'listener'
            %>
            <li class="media notables-item">
                ${lib_6.userImage(person, className="avatar med-avatar media-object", linkClass="pull-left")}
                <div class="media-body">
                    ${lib_6.userLink(person, className="orange orange-hover listener-name")}<br />
                    <small>${personTitle}</small>
                </div>
            </li>
            
        % endfor
        </ul>
     % endif
    % if pending:
        <hr>
        <div class="orange"><p>Not yet participating. Invite them to join in.</p></div>
        <ul class="media-list" id="workshopNotables">
        % for person in pending:
            <%
                lName = person['name']
                lTitle = person['title']
                listenerCode = person['urlCode']
                personClass = 'pendingListener'
                if person['invites'] != '':
                    inviteList = person['invites'].split(',')
                    numInvites = str(len(inviteList))
                else:
                    numInvites = '0'
            %>
            <li class="media notables-item">
                % if 'user' in session and c.authuser:
                    <div class="pull-left rightbuttonspacing"><a href="#invite${listenerCode}" class="btn btn-primary btn-mini" data-toggle="modal"><i class="icon-envelope icon-white"></i> Invite</a></div>
                % else:
                    <div class="pull-left rightbuttonspacing"><a href="/workshop/${c.w['urlCode']}/${c.w['url']}/login/idea" class="btn btn-primary btn-mini"><i class="icon-envelope icon-white"></i> Invite</a></div>
                % endif
                <div class="media-body">
                    <span class="listener-name">${lName}</span><br />
                    <small>${lTitle}</small> 
                </div>
                % if 'user' in session and c.authuser:
                    <%
                        memberMessage = "Please join me and participate in this online Civinomics workshop.\nThere are good ideas and informed discussions, please login and listen in!"
                    %>
                    <div id="invite${listenerCode}" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="invite${listenerCode}Label" aria-hidden="true">
                        <div class="modal-header">
                            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                            <h3 id="invite${listenerCode}Label">Invite ${lName} to Listen</h3>
                        </div><!-- modal-header -->
                        <div class="modal-body"> 
                            <form ng-controller="listenerController" ng-init="code='${c.w['urlCode']}'; url='${c.w['url']}'; user='${c.authuser['urlCode']}'; listener='${listenerCode}'; memberMessage='${memberMessage}'" id="inviteListener" ng-submit="emailListener()" class="form-inline" name="inviteListener">
                            Add your message to the listener invitation:<br />
                            <textarea rows="6" class="field span12" ng-model="memberMessage" name="memberMessage">{{memberMessage}}</textarea>
                            <br />
                            <button class="btn btn-warning" data-dismiss="modal" aria-hidden="true">Close</button>
                            <button type="submit" class="btn btn-warning">Send Invitation</button>
                            <br />
                            <span ng-show="emailListenerShow">{{emailListenerResponse}}</span>
                            </form>
                        </div><!-- modal-footer -->
                    </div><!-- modal -->
                % endif
            </li>
        % endfor
        </ul>
     % endif
     % if 'user' in session and c.authuser:
        <hr>
        <ul class="media-list centered">
            <li class="media pendingListener notables-item">
            <small>Know somebody who should be listening?</small><br />
                <form ng-controller="listenerController" ng-init="code='${c.w['urlCode']}'; url='${c.w['url']}'; user='${c.authuser['urlCode']}'; suggestListenerText='';" id="suggestListenerForm" ng-submit="suggestListener()" class="form-inline" name="suggestListenerForm">
                <div class="pull-right">
                <input type="text" ng-model="suggestListenerText" name="suggestListenerText" placeholder="Suggest a Listener"  required>
                <button type="submit" class="btn btn-success btn-small">Submit</button>
                </div>
                <br />
                <span ng-show="suggestListenerShow">{{suggestListenerResponse}}</span>
                </form>
            </li>
        </ul><!-- media-list -->
    % endif
</%def>

<%def name="showFacilitators()">
    % for facilitator in c.facilitators:
        Facilitator: ${lib_6.userLink(facilitator)}<br />
    % endfor
</%def>

<%def name="showActivity(activity)">
    <%
        numItems = 5
        shownItems = 0
    %>
    
    <ul class="activity"  id="workshopActivity">
        % for item in activity:
            <%
                if c.demo:
                    author = getUserByID(item.owner)
                    if not c.privs['admin']:
                        if 'user' in session:
                            if ((author['accessLevel'] != '300' and not facilitatorLib.isFacilitator(author, c.w)) and author.id != c.authuser.id):
                                continue
                        else:
                            if author['accessLevel'] != '300' and not facilitatorLib.isFacilitator(author, c.w):
                                continue
                if shownItems >= numItems:
                    break
            %>
            <li>
                <%
                    lib_6.userImage(getUserByID(item.owner), className="avatar small-avatar inline")
                    lib_6.userLink(item.owner, className = "green green-hover")
                    lib_6.showItemInActivity(item, c.w, expandable = True)
                %>
            </li>
        % endfor
    </ul>
</%def>

<%def name="watchButton()">
    % if 'user' in session:
        % if c.isFollowing:
            <button class="btn round btn-civ pull-right followButton following" data-URL-list="workshop_${c.w['urlCode']}_${c.w['url']}" rel="tooltip" data-placement="bottom" data-original-title="this workshop" id="workshopBookmark"> 
            <span><i class="icon-bookmark icon-white pull-left"></i> Bookmarked </span>
            </button>
        % else:
            <button class="btn round pull-right followButton" data-URL-list="workshop_${c.w['urlCode']}_${c.w['url']}" rel="tooltip" data-placement="bottom" data-original-title="this workshop" id="workshopBookmark"> 
             <span><i class="icon-bookmark pull-left"></i> Bookmark </span>
            </button>
        % endif
    % endif
</%def>

<%def name="watchButtonListing(w)">
    % if 'user' in session:
        <button class="btn round btn-civ pull-right followButton following" data-URL-list="workshop_${w['urlCode']}_${w['url']}" rel="tooltip" data-placement="bottom" data-original-title="this workshop" id="workshopBookmark"> 
        <span><i class="icon-bookmark icon-white pull-left"></i> Bookmarked </span>
        </button>
    % endif
</%def>

<%def name="configButton(w)">
   <% workshopLink = "%s/preferences" % lib_6.workshopLink(w, embed = True, raw = True) %>
   <a class="btn round btn-civ pull-right preferencesLink" href="${workshopLink | n}" rel="tooltip" data-placement="bottom" data-original-title="workshop moderation and configuration"><span><i class="icon-wrench icon-white pull-left"></i>Admin</span></a>
</%def>

<%def name="previewButton()">
  <a class="btn round btn-civ pull-right" href="${lib_6.workshopLink(c.w, embed=True, raw=True)}"><span><i class="icon-eye-open icon-white pull-left"></i> Preview </span></a>
</%def>

<%def name="viewButton()">
  <a class="btn round btn-civ pull-right" href="${lib_6.workshopLink(c.w, embed=True, raw=True)}"><span><i class="icon-eye-open icon-white pull-left"></i> View </span></a>
</%def>

<%def name="workshopNavButton(workshop, count, objType, active = False)">
    <%
        imageMap = {'discussion':'/images/glyphicons_pro/glyphicons/png/glyphicons_244_conversation.png',
                    'idea':'/images/glyphicons_pro/glyphicons/png/glyphicons_064_lightbulb.png',
                    'resource':'/images/glyphicons_pro/glyphicons/png/glyphicons_050_link.png',
                    'home':'/images/glyphicons_pro/glyphicons/png/glyphicons_020_home.png',
                    'information':'/images/glyphicons_pro/glyphicons/png/glyphicons_318_more_items.png',
                    'activity':'/images/glyphicons_pro/glyphicons/png/glyphicons_057_history.png'}
        titleMap = {'discussion':' Forum',
                    'idea':' Vote',
                    'resource':' Links',
                    'home':' Home',
                    'information':' Information',
                    'activity':'Activity'}
        linkHref = lib_6.workshopLink(workshop, embed = True, raw = True)
        if objType != 'home':
            linkHref += '/' + objType
        linkClass = 'btn workshopNav'
        if active:
            linkClass += ' selected-nav'
        linkID = objType + 'Button'
    %>
    <a class="${linkClass}" id="${linkID}" href = "${linkHref | n}"> <img class="workshop-nav-icon" src="${imageMap[objType] | n}"> ${titleMap[objType]}
    (${count})
    </a>
</%def>

<%def name="workshopNav(w, listingType)">
   <% 
      activity = activityLib.getActivityForWorkshop(w['urlCode'])
      discussionCount = 0
      ideaCount = 0
      resourceCount = 0
      activityCount = len(activity)
      for item in activity:
         if c.demo:
            author = getUserByID(item.owner)
            if not c.privs['admin']:
               if 'user' in session:
                  if ((author['accessLevel'] != '300' and not facilitatorLib.isFacilitator(author, c.w)) and author.id != c.authuser.id):
                     continue
               else:
                  if author['accessLevel'] != '300' and not facilitatorLib.isFacilitator(author, c.w):
                     continue
         
         if item.objType == 'discussion':
            discussionCount += 1
         elif item.objType == 'idea':
            ideaCount += 1
         elif item.objType == 'resource':
            resourceCount += 1
   %>
   <div class="btn-group four-up">
   <% 
      if listingType == 'resources' or listingType == 'resource':
         workshopNavButton(w, ideaCount, 'home')
         workshopNavButton(w, resourceCount, 'information', active = True)
         workshopNavButton(w, discussionCount, 'discussion')
         workshopNavButton(w, activityCount, 'activity')
      elif listingType == 'discussion':
         workshopNavButton(w, ideaCount, 'home')
         workshopNavButton(w, resourceCount, 'information')
         workshopNavButton(w, discussionCount, 'discussion', active = True)
         workshopNavButton(w, activityCount, 'activity')
      elif listingType == 'ideas' or listingType == 'idea':
         workshopNavButton(w, ideaCount, 'home', active = True)
         workshopNavButton(w, resourceCount, 'information')
         workshopNavButton(w, discussionCount, 'discussion')
         workshopNavButton(w, activityCount, 'activity')
      elif listingType == 'activity':
         workshopNavButton(w, ideaCount, 'home')
         workshopNavButton(w, resourceCount, 'information')
         workshopNavButton(w, discussionCount, 'discussion')
         workshopNavButton(w, activityCount, 'activity', active = True)
      else:
         workshopNavButton(w, ideaCount, 'home')
         workshopNavButton(w, resourceCount, 'information')
         workshopNavButton(w, discussionCount, 'discussion')
         workshopNavButton(w, activityCount, 'activity')
   %>
   </div>
</%def>

<%def name="slideshow(w, *args)">
    <% 
        slides = slideshowLib.getSlidesInOrder(slideshowLib.getSlideshow(w)) 
        slideNum = 0
      
        if 'large' in args:
            spanX = "span8"
        else:
            spanX = "span12"

    %>
    <div class="${spanX}">
        <ul class="gallery thumbnails no-bottom" data-clearing>
        <%
           numSlides = len(slides)

           for slide in slides:
              if slide['deleted'] != '1':
                if 'large' in args:
                  _slideLarge(slide, slideNum)
                  if slideNum == 0:
                    slideCaption = slide['title']  
                elif 'listing' in args:
                  _slideListing(slide, slideNum, numSlides)
                else:
                  _slide(slide, slideNum, numSlides)
                slideNum += 1
        %>
        </ul>
    </div>
    % if 'large' in args:
        <div class="span4">
            <p style="color: #FFF; padding-top: 15px;"><strong>Click Image To View Slideshow (1 of ${slideNum})</strong><br>
            <small><br>${lib_6.ellipsisIZE(slideCaption, 214)}</small><br></p>
        </div>
    % endif
</%def>

<%def name="_slideLarge(showSlide, slideNum)">
    <%
        if slideNum == 0:
            spanX = "span12"
        else:
            spanX = "noShow"
        slideFormat = 'jpg'
        if 'format' in showSlide.keys():
            slideFormat = showSlide['format']
    %>

    <li class="${spanX} no-bottom">
    % if showSlide['pictureHash'] == 'supDawg':
        <a href="/images/slide/slideshow/${showSlide['pictureHash']}.slideshow">
        <div style="width:100%; height:240px; background-image:url('/images/slide/slideshow/${showSlide['pictureHash']}.slideshow'); background-repeat:no-repeat; background-size:cover; background-position:center;" data-caption="${showSlide['title']}"/></div>
        </a>
    % else:
        <a href="/images/slide/${showSlide['directoryNum']}/slideshow/${showSlide['pictureHash']}.${slideFormat}">
        <!-- img class is needed by data-clearing to assemble the slideshow carousel-->
        <img class="noShow"src="/images/slide/${showSlide['directoryNum']}/slideshow/${showSlide['pictureHash']}.${slideFormat}" data-caption="${showSlide['title']}"/>
        <!-- div with background-image needed to appropirately size and scale image in workshop_home template -->
        <div style="width:100%; height:240px; background-image:url('/images/slide/${showSlide['directoryNum']}/slideshow/${showSlide['pictureHash']}.${slideFormat}'); background-repeat:no-repeat; background-size:cover; background-position:center;" data-caption="${showSlide['title']}"/></div>
        </a>
    % endif
    </li>
</%def>


<%def name="_slide(slide, slideNum, numSlides)">
   <% 
      if slideNum == 0:
         spanX = "span12"
      else:
         if slideNum <= 3:
            if numSlides == 2:
               spanX = "span4 offset4 thumbnail-gallery"
            elif numSlides == 3:
               spanX = "span4 offset1 thumbnail-gallery"
            elif numSlides >= 4:
               spanX = "span4 thumbnail-gallery"
         else:
            spanX = "noShow"
   %>
      <li class="${spanX}">
      % if slide['pictureHash'] == 'supDawg':
         <a href="/images/slide/slideshow/${slide['pictureHash']}.slideshow">
            <img src="/images/slide/slideshow/${slide['pictureHash']}.slideshow" data-caption="${slide['title']}"/>
         </a>
      % elif 'format' in slide.keys():
         <a href="/images/slide/${slide['directoryNum']}/slideshow/${slide['pictureHash']}.${slide['format']}">
            <img src="/images/slide/${slide['directoryNum']}/slideshow/${slide['pictureHash']}.${slide['format']}" data-caption="${slide['title']}"/>
         </a>
      % else:
         <a href="/images/slide/${slide['directoryNum']}/slideshow/${slide['pictureHash']}.jpg">
            <img src="/images/slide/${slide['directoryNum']}/slideshow/${slide['pictureHash']}.jpg" data-caption="${slide['title']}"/>
         </a>
      % endif
      % if slideNum == 0:
         <small class="centered">${slide['title']}</small>
      % endif
   </li>
</%def>

<%def name="_slideListing(slide, slideNum, numSlides)">
  <li class="span4 slideListing">
    % if slide['pictureHash'] == 'supDawg':
       <a href="/images/slide/slideshow/${slide['pictureHash']}.slideshow">
          <img src="/images/slide/slideshow/${slide['pictureHash']}.slideshow" data-caption="${slide['title']}"/>
       </a>
    % elif 'format' in slide.keys():
       <a href="/images/slide/${slide['directoryNum']}/slideshow/${slide['pictureHash']}.${slide['format']}">
          <img src="/images/slide/${slide['directoryNum']}/slideshow/${slide['pictureHash']}.${slide['format']}" data-caption="${slide['title']}"/>
       </a>
    % else:
       <a href="/images/slide/${slide['directoryNum']}/slideshow/${slide['pictureHash']}.jpg">
          <img src="/images/slide/${slide['directoryNum']}/slideshow/${slide['pictureHash']}.jpg" data-caption="${slide['title']}"/>
       </a>
    % endif
  </li>
</%def>

<%def name="showInfo(workshop)">
    <div>
    % if c.information and 'data' in c.information: 
        <p>This introduction was written and is maintained by the workshop facilitator.
        % if c.w['allowResources'] == '1':
            You are encouraged to add links to additional information resources.
        % endif
        </p>
        ${m.html(c.information['data'], render_flags=m.HTML_SKIP_HTML) | n}
    % endif
    </div>
</%def>

<%def name="showGoals(goals)">
    % if len(goals) == 0:
        <p>This workshop has no goals!</p>
    % else:
        <div id="workshopGoals">
        Workshop Goals:
        <ul>
        % for goal in goals:
            % if goal['status'] == '100':
                <li class="done-true">${goal['title']}</li>
            % else:
                <li>${goal['title']}</li>
            % endif
        % endfor
        </ul>
        </div><!-- workshopGoals -->
    % endif
</%def>

<%def name="showTags()">
    <% 
        tagString = ''
        tagList = c.w['workshop_category_tags'].split('|')
        for tag in tagList:
            if tag and tag != '':
                if tagString != '':
                    tagString = tagString + ", " + tag
                else:
                    tagString = tag
        if tagString != '':
            tagString = "Tags: " + tagString
    %>
    ${tagString}<br />
</%def>

<%def name="showScope()">
    <%
        if c.w['public_private'] == 'public':
            scopeName = c.scope['level']
            scopeString = 'Scope: '
            if scopeName == 'earth':
                scopeString += 'the entire planet Earth.'
            else:
                # More mapping for the postal code, this time to display Postal Code instead of just Postal.
                # The real fix for this is through use of message catalogs, which we will need to implement
                # when we support multiple languages in the interface, so for right now this kludge is
                # "good enough"
                if scopeName == 'postalCode':
                    scopeNeme = 'Postal Code '

                scopeString += "the " + scopeName.title() + " of "
                scopeString += c.scope['name']\
                        .replace('-', ' ')\
                        .title()
        else:
            scopeString = "Scope: This is a private workshop."
    %>
    ${scopeString | n}
</%def>
