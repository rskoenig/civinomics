<%!
   import pylowiki.lib.db.workshop     as workshopLib
   import pylowiki.lib.db.slideshow as slideshowLib
   from pylowiki.lib.db.user import getUserByID
   import pylowiki.lib.db.activity as activityLib
   import pylowiki.lib.db.facilitator   as facilitatorLib
   import pylowiki.lib.utils   as utils
   import misaka as m
   
   import logging
   log = logging.getLogger(__name__)
%>

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="whoListening()">
    % if c.activeListeners:
        <ul class="media-list" id="workshopNotables">
        % for listener in c.activeListeners:
            % if listener['ltype'] == 'elected':
                <% scopeInfo = utils.getPublicScope(listener['scope']) %>
                <li class="media notables-item">
                    <div class="row">
                        <div class="col-xs-3"><img src="${scopeInfo['flag']}" class="thumbnail small-flag tight"></div><div class="col-xs-9"><a href="/listener/${listener['urlCode']}/listenerShow">${listener['name']}</a></br> <small>${listener['title']}, ${listener['group']}</small></div>
                    </div>
                </li>
            % else:
                <li class="media notables-item">
                    <div class="row">
                        <div class="col-xs-3"></div><div class="col-xs-9"><a href="/listener/${listener['urlCode']}/listenerShow">${listener['name']}</a></br> <small>${listener['title']}, ${listener['group']}</small>
                        </div>
                    </div>
                </li>
            % endif
        % endfor
        </ul>
     % endif
</%def>

<%def name="whoListeningModals()">
  % if c.pendingListeners:
    % for person in c.pendingListeners:
      % if 'user' in session and c.authuser:
        <%
            memberMessage = "Please join me and participate in this Civinomics workshop. There are good ideas and informed discussions that I think you should be a part of."

            if person['invites'] != '':
                inviteList = person['invites'].split(',')
                numInvites = str(len(inviteList))
            else:
                numInvites = '0'
                
        %>
        <div id="invite${person['urlCode']}" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="invite${person['urlCode']}Label" aria-hidden="true">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                <h3 id="invite${person['urlCode']}Label">Invite ${person['name']} to Listen</h3>
            </div><!-- modal-header -->
            <div class="modal-body"> 
              <div class="well">
                <form ng-controller="listenerController" ng-init="code='${c.w['urlCode']}'; url='${c.w['url']}'; user='${c.authuser['urlCode']}'; listener='${person['urlCode']}'; memberMessage='${memberMessage}'" id="inviteListener" ng-submit="emailListener()" class="form-inline" name="inviteListener">
                <div class="alert" ng-show="emailListenerShow">{{emailListenerResponse}}</div>
                Add a personalized message to the listener invitation:<br />
                <textarea rows="6" class="field span12" ng-model="memberMessage" name="memberMessage">{{memberMessage}}</textarea>
                <br />
                <div class="spacer"></div>
                <button class="btn btn-danger" data-dismiss="modal" aria-hidden="true">Close</button>
                <button type="submit" class="btn btn-success">Send Invitation</button>
                <br />
                </form>
              </div><!-- well -->
            </div><!-- modal-footer -->
        </div><!-- modal -->
      % endif
    % endfor
  % endif
</%def>

<%def name="showFacilitators()">
    <ul class="media-list" id="workshopNotables">
      % for facilitator in c.facilitators:
          <li class="media notables-item">
              ${lib_6.userImage(facilitator, className="avatar media-object", linkClass="pull-left")}
              <div class="media-body">
                  ${lib_6.userLink(facilitator, className="listener-name")}<br />
                  <small>${lib_6.userGreetingMsg(facilitator)} <strong class="grey">Facilitator</strong></small>
              </div>
          </li>
      % endfor
      </ul>
</%def>

<%def name="showActivity(activity)">
    <%
        numItems = 5
        shownItems = 0
    %>
    
    % for item in activity:
      <div class="media"  id="workshopActivity">
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
        <div class="pull-left">
          ${lib_6.userImage(getUserByID(item.owner), className="avatar small-avatar inline")}
        </div>
        <div class="media-body">
          ${lib_6.userLink(item.owner, className = "green green-hover", maxChars = 25)}
          ${lib_6.showItemInActivity(item, c.w, expandable = True)}
        </div>
      </div>
    % endfor
    
</%def>

<%def name="watchButton(w, **kwargs)">
    % if 'user' in session:
        % if c.isFollowing or 'following' in kwargs:
            <button class="btn btn-default pull-right followButton following" data-URL-list="workshop_${w['urlCode']}_${w['url']}" rel="tooltip" data-placement="bottom" data-original-title="this workshop" id="workshopBookmark"> 
            <span><i class="icon-bookmark btn-height icon-light"></i><strong> Following </strong></span>
            </button>
        % else:
            <button class="btn btn-default pull-right followButton" data-URL-list="workshop_${w['urlCode']}_${w['url']}" rel="tooltip" data-placement="bottom" data-original-title="this workshop" id="workshopBookmark"> 
             <span><i class="icon-bookmark med-green"></i><strong> Follow </strong></span>
            </button>
        % endif
    % endif
</%def>

<%def name="configButton(w)">
   <% workshopLink = "%s/preferences" % lib_6.workshopLink(w, embed = True, raw = True) %>
   <a class="btn btn-default pull-right followButton" href="${workshopLink | n}" rel="tooltip" data-placement="bottom" data-original-title="workshop moderation and configuration"> 
    <span><strong style="letter-spacing: normal;"> Admin </strong></span>
  </a>
</%def>

<%def name="previewButton()">
  <a class="btn btn-default pull-right" href="${lib_6.workshopLink(c.w, embed=True, raw=True)}"><span><i class="icon-eye-open icon-white pull-left"></i> Preview </span></a>
</%def>

<%def name="viewButton()">
  <a class="btn btn-default pull-right left-space" href="${lib_6.workshopLink(c.w, embed=True, raw=True)}"><strong>View</strong></a>
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

<%def name="imagePreviewer(w)">
  <!-- using the data-clearing twice on a page leads to slide skipping this function allows a preview but will not launch slideshow -->
  <% 
    images = slideshowLib.getSlidesInOrder(slideshowLib.getSlideshow(w))
    count = 0
  %>
  <div class="row">
    <ul class="gallery thumbnails no-bottom">
      % for image in images:
        <% 
          imageFormat = 'jpg'
          if 'format' in image.keys():
            imageFormat = image['format']

          spanX = 'noShow'
          if count <= 5:
            spanX = 'col-xs-4'
        %>
        % if image['deleted'] != '1':
          <li class="${spanX} slideListing">
            % if image['pictureHash'] == 'supDawg':
               <a href="#moreimages" data-toggle="tab" ng-click="switchImages()">
                  <img src="/images/slide/slideshow/${image['pictureHash']}.slideshow"/>
               </a>
            % else:
              <a href="#moreimages" data-toggle="tab" ng-click="switchImages()">
                <!-- div with background-image needed to appropirately size and scale image in workshop_home template -->
                <div class="slide-preview" style="background-image:url('/images/slide/${image['directoryNum']}/slideshow/${image['pictureHash']}.${imageFormat}');"/>
                </div>
              </a>
            % endif
          </li>
        % endif
        <% count += 1 %>
      % endfor
    </ul>
  </row>
</%def>


<%def name="slideshow(w, *args)">
    <% 
        slides = slideshowLib.getSlidesInOrder(slideshowLib.getSlideshow(w)) 
        slideNum = 0
        spanX = ""
        if 'hero' in args:
          spanX = "col-xs-8"
    %>
    <div class="${spanX}">
        <ul class="gallery thumbnails no-bottom" data-clearing>
        <%
          for slide in slides:
            if slide['deleted'] != '1':
              if 'hero' in args:
                _slideListing(slide, slideNum, 'hero')
              else:
                _slideListing(slide, slideNum)
              slideNum += 1
        %>
        </ul>
    </div>
    % if 'hero' in args:
        <% infoHref = lib_6.workshopLink(c.w, embed = True, raw = True) + '/information' %>
        <div class="col-xs-4">
          <p class="description" style="color: #FFF; padding-top: 15px;">
            ${lib_6.ellipsisIZE(c.w['description'], 285)}
            <a href="${infoHref}">read more</a>
          </p>
        </div>
    % endif
</%def>

<%def name="_slideListing(showSlide, slideNum, *args)">
    <%
      if slideNum == 0:
          spanX = "col-xs-12"
      else:
          spanX = "noShow"
      slideFormat = 'jpg'
      if 'format' in showSlide.keys():
          slideFormat = showSlide['format']
    %>
    % if slideNum == 0 and 'hero' in args:
      <li class="${spanX} no-bottom">
      % if showSlide['pictureHash'] == 'supDawg':
          <a href="/images/slide/slideshow/${showSlide['pictureHash']}.slideshow">
          <div class="slide-hero" style="background-image:url('/images/slide/slideshow/${showSlide['pictureHash']}.slideshow');" data-caption="${showSlide['title']}"/></div>
          </a>
      % else:
          <a href="/images/slide/${showSlide['directoryNum']}/slideshow/${showSlide['pictureHash']}.${slideFormat}">
          <!-- img class is needed by data-clearing to assemble the slideshow carousel-->
          <img class="noShow"src="/images/slide/${showSlide['directoryNum']}/slideshow/${showSlide['pictureHash']}.${slideFormat}" data-caption="${showSlide['title']}"/>
          <!-- div with background-image needed to appropirately size and scale image in workshop_home template -->
          <div class="slide-hero" style=" background-image:url('/images/slide/${showSlide['directoryNum']}/slideshow/${showSlide['pictureHash']}.${slideFormat}');" data-caption="${showSlide['title']}"/>
              <div class="well slide-hero-caption">
                  <i class="icon-play"></i> Slideshow
              </div>
          </div>
          </a>
      % endif
      </li>
    % elif not slideNum >= 6:
      <li class="col-xs-4 slideListing">
        % if showSlide['pictureHash'] == 'supDawg':
           <a href="/images/slide/slideshow/${showSlide['pictureHash']}.slideshow">
              <img src="/images/slide/slideshow/${showSlide['pictureHash']}.slideshow" data-caption="${showSlide['title']}"/>
           </a>
        % else:
          <a href="/images/slide/${showSlide['directoryNum']}/slideshow/${showSlide['pictureHash']}.${slideFormat}">
            <!-- img class is needed by data-clearing to assemble the slideshow carousel-->
            <img class="noShow" src="/images/slide/${showSlide['directoryNum']}/slideshow/${showSlide['pictureHash']}.${slideFormat}" data-caption="${showSlide['title']}"/>
            <!-- div with background-image needed to appropirately size and scale image in workshop_home template -->
              <div class="slide-preview" style="background-image:url('/images/slide/${showSlide['directoryNum']}/slideshow/${showSlide['pictureHash']}.${slideFormat}');" data-caption="${showSlide['title']}"/>
            </div>
          </a>
        % endif
      </li>
    % else:
      <li class="noShow slideListing">
        <a href="/images/slide/${showSlide['directoryNum']}/slideshow/${showSlide['pictureHash']}.${slideFormat}">
          <!-- img class is needed by data-clearing to assemble the slideshow carousel-->
          <img class="noShow" src="/images/slide/${showSlide['directoryNum']}/slideshow/${showSlide['pictureHash']}.${slideFormat}" data-caption="${showSlide['title']}"/>
          <div class="slide-preview" style="background-image:url('/images/slide/${showSlide['directoryNum']}/slideshow/${showSlide['pictureHash']}.${slideFormat}');" data-caption="${showSlide['title']}"/>
            </div>
        </a>
      </li>
    % endif
</%def>

<%def name="_slide(slide, slideNum, numSlides)">
  <!-- original code -->
   <% 
      if slideNum == 0:
         spanX = "span12"
      else:
         if slideNum <= 3:
            if numSlides == 2:
               spanX = "col-xs-4 col-xs-offset-4 thumbnail-gallery"
            elif numSlides == 3:
               spanX = "col-xs-4 col-xs-offset-1 thumbnail-gallery"
            elif numSlides >= 4:
               spanX = "col-xs-4 thumbnail-gallery"
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

<%def name="showInfo(workshop)">
    <div>
    % if c.information and 'data' in c.information: 
        ${m.html(c.information['data'], render_flags=m.HTML_SKIP_HTML) | n}
    % endif
    </div>
</%def>

<%def name="showGoals(goals)">
    % if len(goals) == 0:
        <p>This workshop has no goals!</p>
    % else:
        <div id="workshopGoals">
        <ol class="workshop-goals">
        % for goal in goals:
            % if goal['status'] == '100':
                <li class="done-true"><span>${goal['title']}</span></li>
            % else:
                <li><span>${goal['title']}</span></li>
            % endif
        % endfor
        </ul>
        </div><!-- workshopGoals -->
    % endif
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

<%def name="displayWorkshopFlag(w, **kwargs)">
    <%
        workshopFlag = '/images/flags/generalFlag.gif'
        href = '#'
        if w['public_private'] == 'public':
            scope = utils.getPublicScope(w)
            href = scope['href']
            workshopFlag = scope['flag']
            level = scope['level']
            name = scope['name']
        else:
            workshopFlag = '/images/flags/generalGroup.gif'
        flagSize = 'med-flag'
        if 'size' in kwargs:
          flagSize = kwargs['size']

        if 'objType' in kwargs:
          obj = kwargs['objType'].title()
        else:
          obj = 'Workshop'

    %>
    <a href="${href}"><img class="thumbnail flag ${flagSize}" src="${workshopFlag}"></a>
    % if 'workshopFor' in kwargs and w['public_private'] == 'public':
        ${obj} for
        % if name == 'Earth':
          <a href="${href}">${name}</a>
        % else:
          the <a href="${href}">${level} of ${name}</a>
        % endif
    % endif
</%def>


<%def name="workshopHero()">
  <div class="well well workshop-hero">
    <div class="workshop-hero-image" style="background-image: url(${c.backgroundImage})">
      <div>
        <span class="link-span med-gradient-workshop"></span><!-- used to make entire div a link -->
        
        <div class="workshop-title-group">
          <h1 class="workshop-title"> 
            <a href="${lib_6.workshopLink(c.w, embed=True, raw=True)}" id="workshopTitle" class="workshop-title" ng-init=" workshopTitle='${c.w['title'].replace("'", "\\'")}' " ng-cloak>
              {{workshopTitle}}
            </a>
          </h1>
          <h4 style="color: #fff">${displayWorkshopFlag(c.w, size='small-flag', workshopFor=True)} ${lib_6.showTags(c.w)}</h4>
        </div>
      </div>
    </div><!-- background-image -->
    <div class="hero-bottom">
      % if 'user' in session:
        <span class="pull-right">
          ${watchButton(c.w)}
          % if c.adminPanel:
            ${viewButton()}
          % else:
            % if c.privs['admin'] or c.privs['facilitator']: 
              ${configButton(c.w)}
            % endif
          % endif
        </span>
      % endif
      <span class = "share-icons pull-right">
        ${lib_6.facebookDialogShare2(shareOnWall=True, sendMessage=True)}
        ${lib_6.mailToShare(c.w)}
        % if c.w['public_private'] == 'public':
          <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/rss" target="_blank"><i class="icon-rss icon-2x"></i></a>
        %endif
      </span>
      <table id="metrics">
        <tr>
          <td class="clickable" style="padding-left: 0px;" ng-click="toggleIdeas()">
            <span class="workshop-metrics">Ideas</span><br>
              <strong ng-cloak>${c.numIdeas}</strong>
          </td>
          <td class="clickable" ng-click="toggleAdopted()">
            <span class="workshop-metrics">Adopted</span><br>
              <strong ng-cloak>${c.numAdopted}</strong>
          </td>
          <td class="clickable" ng-click="toggleDiscussions()">
            <span class="workshop-metrics">discussions</span><br>
              <strong ng-cloak>${c.numDiscussions}</strong>
          </td>
          <td class="clickable" ng-click="toggleResources()">
            <span class="workshop-metrics">Resources</span><br>
              <strong ng-cloak>${c.numResources}</strong>
          </td>

          <!--
          <td>
            <span class="workshop-metrics">Views</span><br>
              <strong ng-cloak>{{numViews}}</strong>
          </td>
          -->
          <!--
          <td>
            <span class="workshop-metrics">Participants</span><br>
              <strong ng-cloak>{{numParticipants}}</strong>
          </td>
          -->
        </tr>
      </table>
    </div><!-- workshopIdeasCtrl -->
  </div><!-- workshop-hero -->
</%def>
