<%!
   import pylowiki.lib.db.slideshow as slideshowLib
   from pylowiki.lib.db.user import getUserByID
   import pylowiki.lib.db.activity as activityLib
   import misaka as misaka
   
   import logging
   log = logging.getLogger(__name__)
%>

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="whoListening()">
   <%
       if c.listeners:
           listenOrFacilitate = "Who's listening?"
           people = c.listeners
       else:
           listenOrFacilitate = "Facilitators"
           people = c.facilitators
   %>
   <h4 class="section-header smaller section-header-inner"> ${listenOrFacilitate} </h4>
   <ul class="listeners">
      <% counter = 1 %>
      % for person in people:
         <li>
            ${lib_6.userImage(person, className="avatar")}
            <br>
            ${lib_6.userLink(person)}
         </li>
         <%
            counter += 1
            if counter > 3:
               break
         %>
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
    <ul class="activity">
    % for item in activity:
        <%
            if c.demo:
                author = getUserByID(item.owner)
                if not c.privs['admin']:
                    if 'user' in session:
                        if (author['accessLevel'] != '300' and author.id != c.authuser.id):
                            continue
                    else:
                        if author['accessLevel'] != '300':
                            continue
            if shownItems >= numItems:
                break
        %>
        <li>
        ##<div class="row-fluid">
            ${lib_6.userImage(getUserByID(item.owner), className="avatar small-avatar inline")}
            ${lib_6.userLink(item.owner)}
            <%
                if item.objType == 'comment':
                    activityStr = 'Commented on a'
                    if 'ideaCode' in item.keys():
                        activityStr += 'n'
                else:
                    activityStr = 'Added a'
                if item.objType == 'idea':
                    activityStr += 'n'
                activityStr += ' <a ' + lib_6.thingLinkRouter(item, c.w, embed = True) + '>'
                if item.objType != 'comment':
                    activityStr += item.objType + "</a>"
                else:
                    if 'ideaCode' in item.keys():
                        activityStr += 'idea </a>'
                    elif 'resourceCode' in item.keys():
                        activityStr += 'resource </a>'
                    else:
                        activityStr += 'discussion </a>'
                shownItems += 1
            %>
            ${activityStr | n}
        ##</div>
        </li>
    % endfor
    </ul>
</%def>

<%def name="watchButton()">
    % if 'user' in session:
        % if c.isFollowing:
            <button class="btn round followButton following" data-URL-list="workshop_${c.w['urlCode']}_${c.w['url']}" rel="tooltip" data-placement="bottom" data-original-title="The entire workshop"> 
            <img class="watch" src="/images/glyphicons_pro/glyphicons/png/glyphicons_072_bookmark.png">
            <span> Un-bookmark </span>
            </button>
        % else:
            <button class="btn round followButton" data-URL-list="workshop_${c.w['urlCode']}_${c.w['url']}" rel="tooltip" data-placement="bottom" data-original-title="The entire workshop"> 
            <img class="watch" src="/images/glyphicons_pro/glyphicons/png/glyphicons_072_bookmark.png">
            <span> Bookmark </span>
            </button>
        % endif
    % endif
</%def>

<%def name="configButton(w)">
   <% workshopLink = "%s/preferences" % lib_6.workshopLink(w, embed = True, raw = True) %>
   <a class="pull-right" href="${workshopLink | n}">
      <img class="config" src="/images/glyphicons_pro/glyphicons/png/glyphicons_137_cogwheels.png">
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
                  if (author['accessLevel'] != '300' and author.id != c.authuser.id):
                     continue
               else:
                  if author['accessLevel'] != '300':
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
         workshopNavButton(w, discussionCount, 'discussion')
         workshopNavButton(w, ideaCount, 'idea')
         workshopNavButton(w, resourceCount, 'resource')
      elif listingType == 'discussion':
         workshopNavButton(w, discussionCount, 'discussion', active = True)
         workshopNavButton(w, ideaCount, 'idea')
         workshopNavButton(w, resourceCount, 'resource')
      elif listingType == 'ideas' or listingType == 'idea':
         workshopNavButton(w, discussionCount, 'discussion')
         workshopNavButton(w, ideaCount, 'idea', active = True)
         workshopNavButton(w, resourceCount, 'resource')
      elif listingType == 'resources' or listingType == 'resource':
         workshopNavButton(w, discussionCount, 'discussion')
         workshopNavButton(w, ideaCount, 'idea')
         workshopNavButton(w, resourceCount, 'resource', active = True)
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
         <a href="/images/slide/${slide['directoryNumber']}/slideshow/${slide['pictureHash']}.jpg">
            <img src="/images/slide/${slide['directoryNumber']}/slideshow/${slide['pictureHash']}.jpg" data-caption="${slide['title']}"/>
         </a>
      % endif
      % if slideNum == 0:
         <small class="centered">${slide['title']}</small>
      % endif
   </li>
</%def>

<%def name="showInfo(workshop)">
    <div class="">
    % if c.information and 'data' in c.information:
        ${misaka.html(c.information['data']) | n}
    % endif
    </div>
</%def>

<%def name="showGoals(goals)">
    % if len(goals) == 0:
        <p>This workshop has no goals!</p>
    % else:
        <ul>
        % for goal in goals:
            % if goal['status'] == '100':
                <li class="done-true">${goal['title']}</li>
            % else:
                <li>${goal['title']}</li>
            % endif
        % endfor
        </ul>
    % endif
</%def>
