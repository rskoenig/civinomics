<%!
   import pylowiki.lib.db.workshop     as workshopLib
   import pylowiki.lib.db.slideshow as slideshowLib
   from pylowiki.lib.db.user import getUserByID
   import pylowiki.lib.db.activity as activityLib
   import pylowiki.lib.db.facilitator   as facilitatorLib
   import pylowiki.lib.utils   as utils
   import pylowiki.lib.graphData       as graphData
   import misaka as m
   
   import logging
   log = logging.getLogger(__name__)

%>

<%namespace name="lib_6" file="/lib/6_lib.mako" />
<%namespace name="ng_helpers" file="/lib/ng_lib.mako" />
<%namespace name="d3Lib" file="/lib/d3_lib.mako"/>

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
          for slide in slides[0:4]:
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
        ${m.html(c.information['data']) | n}
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

<%def name="showGoals2(goals)">
    % if len(goals) == 0:
        <p>This workshop has no goals!</p>
    % else:
        <div class="well goals" id="workshopGoals">
          <% goalNum = 1 %>
          % for goal in goals:
            <h4>Goal ${goalNum}</h4>
            <p>${goal['title']}</p>
            <% goalNum += 1 %>
          % endfor
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

<%def name="metaData()">
  <h4 class="inline">${displayWorkshopFlag(c.w, size='small-flag', noTitle = True)} ${lib_6.showTags(c.w)}</h4>
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
    <a href="${href}"><img class="thumbnail flag ${flagSize} no-bottom" src="${workshopFlag}"></a>
    % if not 'noTitle' in kwargs:
      % if name == 'Earth':
        <a href="${href}">${name}</a>
      % else:
        <a href="${href}">${level} of ${name}</a>
      % endif
    % endif
</%def>

<%def name="workshopTitle()"> 
    <h1 class="workshop-title"> 
      <a class="no-highlight" href="${lib_6.workshopLink(c.w, embed=True, raw=True)}" id="workshopTitle" ng-init=" workshopTitle='${c.w['title'].replace("'", "\\'")}' " ng-cloak>
        {{workshopTitle}}
      </a>
      %if c.display:
        <a ng-click="toggleBrief()" class="brief"><span class="label label-info">Read the Intro</span></a>
      %endif
    </h1>
</%def>

<%def name="workshopHero()">
  <div class="well well workshop-hero">
    <div class="workshop-hero-image" style="background-image: url(${c.backgroundImage})">
      <div>
        <span class="link-span med-gradient-workshop"></span><!-- used to make entire div a link -->
        <div class="workshop-title-group">
          ${workshopTitle()}
        </div>

      </div>
    </div><!-- background-image -->
    <div class="hero-bottom">

      ${workshopActions()}

      ${workshopMetrics()}

    </div><!-- workshopIdeasCtrl -->
  </div><!-- workshop-hero -->
</%def>

<%def name="workshopAddForm()">
  <div ng-show="showAddForm" ng-cloak>
    <table class="addNewObj">
      <tr>
        <td class="well" style="padding: 10px;">
          % if c.privs and not c.privs['provisional']:
            <form class="no-bottom" ng-submit="submitNewObj()">
                <div class="form-group">
                  <select name="thing" ng-model="addThing">
                    % if c.w['allowIdeas'] == '1' or (c.privs and (c.privs['admin'] or c.privs['facilitator'])):
                      <option value="idea">Idea</option>
                      <option value="initiative">Initiative</option>
                    % endif
                    <option value="discussion">Discussion</option>
                    % if c.w['allowResources'] == '1' or (c.privs and (c.privs['admin'] or c.privs['facilitator'])):
                      <option value="resource">Resource</option>
                    % endif
                  </select>
                </div>
                <div class="form-group">
                  <label for="newObjTitle">Title</label>
                  <input type="text" class="form-control" ng-submit="submitNewObj()" name="newObjTitle" ng-model="newObjTitle" placeholder="Enter title...">
                </div>
                <div class="form-group" ng-show="addThing == 'resource'">
                  <label for="newObjLink">Link</label>
                  <input type="text" class="form-control" name="newObjLink" ng-model="newObjLink" placeholder="http://">
                </div>
                <div class="form-group">
                  <label for="newObjText">Additional Info</label>
                  <textarea class="form-control" ng-submit="submitNewObj()" name="newObjText" ng-model="newObjText" placeholder="Enter additional info..."></textarea>
                </div>
                <div class="form-group">
                  <button type="submit" class="btn btn-success pull-right" style="vertical-align: top;">Submit</button>
                  <button class="btn btn-default pull-right right-space" style="vertical-align: top;" ng-click="cancelAddForm()">Cancel</button>
                </div>
            </form>
          % endif
        </td>
      </tr>
    </table>
  </div>
</%def>

<%def name="workshopListFilters()">
  <div class="row" ng-show="!showStats" ng-cloak>
    <div class="col-xs-12">
      <table>
        <tr>
        
          <!--<td style="vertical-align: middle;">
            <span class="lead grey expl-phrase right-indent" style="text-transform: capitalize;"><span ng-if="showSummary">All Activity</span><span ng-if="!showSummary">{{thing}}s</span></span>
          </td>-->

          <td style="padding-bottom: 10px;">
            <ul class="nav nav-pills" ng-cloak>
              <li ng-class="{active : orderProp == ''}"><a ng-click="orderProp = ''">Recent</a></li>
              <li ng-class="{active : orderProp == '-netVotes'}"><a ng-click="orderProp = '-netVotes'">Top Rated</a></li>
              <li ng-class="{active : orderProp == '-voteCount'}"><a ng-click="orderProp = '-voteCount'">Most Votes</a></li>
              <li ng-class="{active : orderProp == '-numComments'}"><a ng-click="orderProp = '-numComments'">Most Comments</a></li>
              <li class="dropdown">
                <a class="dropdown-toggle" data-toggle="dropdown" href="#">
                    Status <b class="caret"></b>
                </a>
                <ul class="dropdown-menu">
                    <li ng-class="{active : query2 = {status:'proposed'}">
                        <a ng-click="query2 = {status:'proposed'}">Proposed</a>
                    </li>
                    <li ng-class="{active : query2 = {status:'adopted'}">
                        <a ng-click="query2 = {status:'adopted'}">Adopted</a>
                    </li>
                    <li ng-class="{active : query2 = {status:'disabled'}">
                        <a ng-click="query2 = {status:'disabled'}">Disabled</a>
                    </li>
                    <li class="search-right-column-link" ng-class="showingPhotos.class">
                        <a href="#photos" data-toggle="tab" ng-click="searchPhotos()">
                            Photos <span class="pull-right">(${c.numPhotos}) </span>
                        </a>
                    </li>
                </ul>
            </li>
            </ul>
          </td>
        </tr>
      </table>
    </div>
  </div>
</%def>

<%def name="workshopList()">
  <div infinite-scroll='getActivitySlice()' infinite-scroll-disabled='activityLoading' infinite-scroll-distance='3' ng-show="showList">

    <div ng-if="thisPhaseStatus == 'past'" class="alert alert-warning" ng-cloak>This phase has concluded.</div>
    <div ng-if="thisPhaseStatus == 'future'" class="alert alert-warning" ng-cloak>This phase has not started yet.</div>
    <div class="alert alert-info" ng-class="alertType" ng-if="((alertMsg && !(alertMsg == '')) || (activity | filter:query).length == 0) && thisPhaseStatus == 'present'" ng-cloak>
      <span ng-show="query == ''">{{alertMsg}}</span>
      <span ng-show="!(query == '') && (activity | filter:query).length == 0">There are no {{thing}}s. Be the first to add one!</span>
    </div>

    <table ng-if="thisPhaseStatus != 'future'" ng-repeat="item in activity | filter:query | filter:query2 | orderBy:orderProp" id="{{item.urlCode}}"  class="activity-item" ng-show="!activityLoading && !showStats" ng-cloak>
      <tr>
        <td ng-if="item.objType == 'initiative'">
          ${ng_helpers.initiative_listing()}
        </td>

        <td ng-if="item.objType == 'idea'">
          ${ng_helpers.idea_listing()}
        </td>

        <td ng-if="item.objType == 'resource'">
          ${ng_helpers.resource_listing()}
        </td>

        <td ng-if="item.objType == 'discussion' || item.objType == 'update' ">
          ${ng_helpers.discussion_listing()}
        </td>

        <td ng-if="item.objType == 'photo'">
          ${ng_helpers.photo_listing()}
        </td>

      </tr>
    </table>

    <div class="centered" ng-show="activityLoading || activitySliceLoading" ng-cloak>
        <i class="icon-spinner icon-spin icon-4x"></i>
    </div>

  </div><!-- infinite-scroll -->
</%def>

<%def name="workshopStats()">
  <div class="well" ng-show="showStats" ng-cloak>
    <span class="grey" ng-if="activity.length == 0"> There are no stats yet...</span>

    <% c.blank, c.jsonConstancyDataIdeas, c.jsonConstancyDataDiscussions, c.jsonConstancyDataResources = graphData.buildConstancyData(c.w, c.activity, typeFilter='all', cap=56) %>

    ${d3Lib.includeD3()}
    % if len(c.jsonConstancyDataIdeas) > 2:
      ${d3Lib.constancyChart(c.jsonConstancyDataIdeas, "ideaChart", "Ideas", "ForestGreen", "DarkSlateGrey")}
    % endif
    % if len(c.jsonConstancyDataResources) > 2:
      ${d3Lib.constancyChart(c.jsonConstancyDataResources, "resourceChart", "Resources", "MidnightBlue", "DarkSlateGrey")}
    % endif
    % if len(c.jsonConstancyDataDiscussions) > 2:
      ${d3Lib.constancyChart(c.jsonConstancyDataDiscussions, "discussionChart", "Discussions", "DarkOrange", "DarkSlateGrey")}
    % endif

  </div>
</%def>

<%def name="workshopBrief()">
  <div class="well wiki-well" ng-show="showBrief" ng-cloak>
    <div ng-cloak>
      <p class="workshop-metrics-lg">Intro</p>
      <div class="row">
        <div class="col-xs-12">
          ${slideshow(c.w, 'listing')}
        </div>
      </div>
      <p class="description">
        ${c.w['description']}
      </p>
      <hr class="list-header">
      ${showInfo(c.w)}
      <a href="#top" class="green green-highlight" ng-click=" showInfo = false ">less</a>
    </div>
  </div>
</%def>

<%def name="workshopMenu()">
  <ul class="nav nav-pills workshop-menu">
    <li ng-class="{active: showSummary == true}">
      <a ng-click="toggleSummary()">Summary</a>
    </li>
    <li ng-class="{active : showInfo == true}"><a ng-click="toggleInfo()">Info</a></li>
    <li ng-class="{active: showIdeas == true}"><a ng-click="toggleIdeas()">Ideas</a></li>
    <li ng-class="{active: showDiscussions == true}"><a ng-click="toggleDiscussions()">Discussions</a></li>
    <li ng-class="{active: showResources == true}"><a ng-click="toggleResources()">Resources</a></li>
    <li ng-class="{active: showStats == true}"><a ng-click="toggleStats()">Stats</a></li>
  </ul>
</%def>

<%def name="addBtn()">
  <%
    if 'readOnly' in c.w and c.w['readOnly'] == '1':
      readonly = '1'
    else:
      readonly = '0'
  %>
  % if readonly == '0':
    % if c.authuser:
      % if c.privs and not c.privs['provisional']:
        <button class="btn btn-lg btn-block btn-success addBtn" ng-show="showAddBtn" ng-click="toggleAddForm()" ng-cloak>Add {{addThing}}</button>
      % else:
        <a class="btn btn-lg btn-block btn-success addBtn" href="#activateAccountModal" data-toggle='modal' ng-show="showAddBtn"  ng-cloak>Add {{addThing}}</a>
      % endif
    % else:
      <a class="btn btn-lg btn-block btn-success addBtn" href="#signupLoginModal" data-toggle='modal' ng-show="showAddBtn"  ng-cloak>Add {{addThing}}</a>
    % endif
  % endif
</%def>

<%def name="workshopActions()">
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
</%def>

<%def name="workshopMetrics()">
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
</%def>

<%def name="workshopTimeline()">
  <div class="btn-group btn-group-justified timeline">
    <div class="btn-group" ng-click="toggleResources()">
      <button type="button" class="btn btn-default {{researchClass}}" ng-click="toggleResearch()">
        <span class="workshop-metrics">Research</span><br>
        <strong ng-cloak>${c.numResources}</strong>
      </button>
    </div>
    <div class="btn-group">
      <button type="button" class="btn btn-default {{ideasClass}}" ng-click="toggleIdeas()">
        <span class="workshop-metrics">Ideas</span><br>
        <strong ng-cloak>${c.numIdeas}</strong>
      </button>
    </div>
    <div class="btn-group">
      <button type="button" class="btn btn-default {{initiativesClass}}" ng-click="toggleInitiatives()">
        <span class="workshop-metrics">Initiatives</span><br>
        <strong ng-cloak>${c.numInitiatives}</strong>
      </button>
    </div>
    <div class="btn-group">
      <button type="button" class="btn btn-default {{finalClass}}" ng-click="toggleFinal()">
        <span class="workshop-metrics">Final Rating</span><br>
        <strong ng-cloak>${c.numFinal}</strong>
      </button>
    </div>
    <div class="btn-group">
      <button type="button" class="btn btn-default {{adoptedClass}}" ng-click="toggleAdopted()">
        <span class="workshop-metrics">Winners Announced</span><br>
        <strong ng-cloak>${c.numAdopted}</strong>
      </button>
    </div>
    <div class="btn-group">
      <button type="button" class="btn btn-default {{impactClass}}" ng-click="toggleImpact()">
        <span class="workshop-metrics">Impact</span><br>
        <strong ng-cloak>${c.numUpdates}</strong>
      </button>
    </div>
  </div>

</%def>


<%def name="workshopOfficials()">
  <div class="well well-subMenu" >
    <span>Officials</span>
    <hr class="subMenu">
    ${showFacilitators()}
    ${whoListening()}
  </div> <!--/.browse-->
</%def>

<%def name="workshopPhaseDescriptions()">
  <div class="well" ng-show="showResearch" ng-cloak>
      <p class="workshop-metrics-lg">Research</p>
      <p>In the research phase we collect data, stories, news, and any other information that will help us learn about the problem.
      </p>
    </div>

    <div class="well" ng-show="showIdeas" ng-cloak>
      <p class="workshop-metrics-lg">Ideas</p>
      <p>In the ideas phase we brainstorm solutions to the problem using everything we learned during the research phase.</p>
    </div>

    <div class="well" ng-show="showInitiatives" ng-cloak>
      <p class="workshop-metrics-lg">Initiatives</p>
      <p>In the initiatives phase we take the best solutions from the ideas phase and continue to build on them. This is the time to build teams, collaborate, challenge each other with questions and think about concrete next steps.
      </p>
    </div>

    <div class="well" ng-show="showFinal" ng-cloak>
      <p class="workshop-metrics-lg">Final Rating</p>
      <p>In the final rating phase you cast your vote for the best initiatives - additional edits to the initiatives are not allowed at this time.
      </p>
    </div>

    <div class="well" ng-show="showAdopted" ng-cloak>
      <p class="workshop-metrics-lg">Winning Initiatives</p>
      <p>Winning initiatives announced. How the winners are determined depends on the workshop facilitators. Some may choose to use voting as the only factor. Others may include their own assessment of factors such as how well an initiative meets the workshop goals or its feasibility.
      </p>
    </div>

    <div class="well" ng-show="showImpact" ng-cloak>
      <p class="workshop-metrics-lg">Impact</p>
      <p>In the impact phase we follow the progress of each of the winning initiatives to see how they're doing and continue learning and refinement.
      </p>
    </div>
</%def>




