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
        people = c.facilitators
        if c.listeners:
            people += c.listeners
    %>
    <h4 class="section-header smaller section-header-inner"> Notables </h4>
    <ul class="media-list centered" id="workshopNotables">
        % for person in people:
            <%
                if person.objType == 'facilitator':
                    personTitle = 'Workshop Facilitator'
                else:
                    personTitle = person['title']
            %>
            <li class="media">
                ${lib_6.userImage(person, className="avatar media-object", linkClass="pull-right")}
                <div class="media-body">
                    <h4 class="media-heading">${lib_6.userLink(person, className="green green-hover")}</h4>
                    ${personTitle}
                </div>
            </li>
        % endfor
    </ul>
</%def>

<%def name="showActivity(activity)">
    <h4 class="section-header smaller section-header-inner"> Activity 
        % if c.w['public_private'] == 'public':
            <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/rss" target="_blank"><img src="/images/feed-icon-14x14.png"></a>
        %endif            
    </h4>
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
                    lib_6.showItemInActivity(item, c.w)
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

<%def name="configButton(w)">
   <% workshopLink = "%s/preferences" % lib_6.workshopLink(w, embed = True, raw = True) %>
   <a class="btn round btn-civ pull-right preferencesLink" href="${workshopLink | n}" rel="tooltip" data-placement="bottom" data-original-title="workshop moderation and configuration">
      <span><i class="icon-wrench icon-white"></i>Admin</span>
   </a>
</%def>

<%def name="workshopNavButton(workshop, count, objType, active = False)">
   <%
      imageMap = {'discussion':'/images/glyphicons_pro/glyphicons/png/glyphicons_244_conversation.png',
                  'idea':'/images/glyphicons_pro/glyphicons/png/glyphicons_064_lightbulb.png',
                  'resource':'/images/glyphicons_pro/glyphicons/png/glyphicons_050_link.png'}
      titleMap = {'discussion':' Talk',
                  'idea':' Vote',
                  'resource':' Learn'}
      linkHref = lib_6.workshopLink(workshop, embed = True, raw = True) + '/' + objType
      linkClass = 'btn workshopNav'
      if active:
         linkClass += ' selected-nav'
      linkID = objType + 'Button'
   %>
   <a class="${linkClass}" id="${linkID}" href = "${linkHref | n}"> <img class="workshop-nav-icon" src="${imageMap[objType] | n}">${titleMap[objType]} (${count})</a>
</%def>

<%def name="workshopNav(w, listingType)">
   <% 
      activity = activityLib.getActivityForWorkshop(w['urlCode'])
      discussionCount = 0
      ideaCount = 0
      resourceCount = 0
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
            
      discussionTitle = 'Talk'
      ideaTitle = 'Vote'
      resourceTitle = 'Learn'
   %>
   <div class="btn-group four-up">
   <% 
      if listingType == None:
         workshopNavButton(w, resourceCount, 'resource')
         workshopNavButton(w, discussionCount, 'discussion')
         workshopNavButton(w, ideaCount, 'idea')
      elif listingType == 'discussion':
         workshopNavButton(w, resourceCount, 'resource')
         workshopNavButton(w, discussionCount, 'discussion', active = True)
         workshopNavButton(w, ideaCount, 'idea')
      elif listingType == 'ideas' or listingType == 'idea':
         workshopNavButton(w, resourceCount, 'resource')
         workshopNavButton(w, discussionCount, 'discussion')
         workshopNavButton(w, ideaCount, 'idea', active = True)
      elif listingType == 'resources' or listingType == 'resource':
         workshopNavButton(w, resourceCount, 'resource', active = True)
         workshopNavButton(w, discussionCount, 'discussion')
         workshopNavButton(w, ideaCount, 'idea')
   %>
   </div>
</%def>

<%def name="slideshow(w)">
   <% 
      slides = slideshowLib.getSlidesInOrder(slideshowLib.getSlideshow(w)) 
      slideNum = 0
   %>
   <ul class="gallery thumbnails" data-clearing>
      <% 
         numSlides = len(slides)
         for slide in slides:
            if slide['deleted'] != '1':
               _slide(slide, slideNum, numSlides)
               slideNum += 1
      %>
   </ul>
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
        if c.tags:
            tagList = []
            tagString = "Tags: "
            for tag in c.tags:
                tagList.append(tag['title'])
            
            tagString += ', '.join(tagList)
    %>
    % if c.tags:
        ${tagString}<br />
    % endif
</%def>
