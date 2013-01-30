<%!
   import pylowiki.lib.db.slideshow as slideshowLib
   from pylowiki.lib.db.user import getUserByID
   import pylowiki.lib.db.activity as activityLib
   import misaka as misaka
   
   import logging
   log = logging.getLogger(__name__)
%>

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="whoListening(people)">
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
    <%
        numItems = 5
        if len(activity) > numItems:
            showMore = True
            activity = activity[0:numItems]
        else:
            showMore = False
    %>
    % for item in activity:
        <div class="row-fluid">
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
            %>
            ${activityStr | n}
        </div>
    % endfor
</%def>
##<a href="#" rel="tooltip" data-placement="bottom" data-original-title="Tooltip on bottom">Tooltip on bottom</a>
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
   <% workshopLink = "%s/dashboard" % lib_6.workshopLink(w, embed = True, raw = True) %>
   <a class="pull-right" href="${workshopLink | n}">
      <img class="config" src="/images/glyphicons_pro/glyphicons/png/glyphicons_019_cogwheel.png">
   </a>
</%def>


<%def name="workshopNav(w, listingType)">
   ## Brute forced and inelegant =(
   <% 
      activity = activityLib.getActivityForWorkshop(w['urlCode'])
      discussionCount = 0
      ideaCount = 0
      resourceCount = 0
      for item in activity:
         if item.objType == 'discussion':
            discussionCount += 1
         elif item.objType == 'idea':
            ideaCount += 1
         elif item.objType == 'resource':
            resourceCount += 1
            
      discussionTitle = 'Conversations'
      ideaTitle = 'Ideas'
      resourceTitle = 'Resources'
   %>
   <div class="btn-group four-up">
   % if listingType == None:
      ##<a class="btn" href="${lib_6.workshopLink(w, embed = True, raw = True) | n}/wiki">
      ##   <img class="workshop-nav-icon" src="/images/glyphicons_pro/glyphicons/png/glyphicons_351_book_open.png"> Wiki
      ##</a>
      <a class="btn" ${'href="' + lib_6.workshopLink(w, embed = True, raw = True) + '/discussion"' | n}>
         <img class="workshop-nav-icon" src="/images/glyphicons_pro/glyphicons/png/glyphicons_244_conversation.png"> ${discussionTitle} (${discussionCount})
      </a>
      <a class="btn" ${'href="' + lib_6.workshopLink(w, embed = True, raw = True) + '/ideas"' | n}>
         <img class="workshop-nav-icon" src="/images/glyphicons_pro/glyphicons/png/glyphicons_064_lightbulb.png"> ${ideaTitle} (${ideaCount})
      </a>
      <a class="btn" ${'href="' + lib_6.workshopLink(w, embed = True, raw = True) + '/resources"' | n}>
         <img class="workshop-nav-icon" src="/images/glyphicons_pro/glyphicons/png/glyphicons_050_link.png"> ${resourceTitle} (${resourceCount})
      </a>
   % elif listingType == 'discussion':
      ##<a class="btn" href="${lib_6.workshopLink(w, embed = True, raw = True) | n}/wiki">
      ##   <img class="workshop-nav-icon" src="/images/glyphicons_pro/glyphicons/png/glyphicons_351_book_open.png"> Wiki
      ##</a>
      <a class="btn selected-nav" ${'href="' + lib_6.workshopLink(w, embed = True, raw = True) + '/discussion"' | n}>
         <img class="workshop-nav-icon" src="/images/glyphicons_pro/glyphicons/png/glyphicons_244_conversation.png"> ${discussionTitle} (${discussionCount})
      </a>
      <a class="btn" href="${lib_6.workshopLink(w, embed = True, raw = True) | n}/ideas">
         <img class="workshop-nav-icon" src="/images/glyphicons_pro/glyphicons/png/glyphicons_064_lightbulb.png"> ${ideaTitle} (${ideaCount})
      </a>
      <a class="btn" ${'href="' + lib_6.workshopLink(w, embed = True, raw = True) + '/resources"' | n}>
         <img class="workshop-nav-icon" src="/images/glyphicons_pro/glyphicons/png/glyphicons_050_link.png"> ${resourceTitle} (${resourceCount})
      </a>
   % elif listingType == 'wiki':
      ##<a class="btn selected-nav" href="${lib_6.workshopLink(w, embed = True, raw = True) | n}/wiki">
      ##   <img class="workshop-nav-icon" src="/images/glyphicons_pro/glyphicons/png/glyphicons_351_book_open.png"> Wiki
      ##</a>
      <a class="btn" ${'href="' + lib_6.workshopLink(w, embed = True, raw = True) + '/discussion"' | n}>
         <img class="workshop-nav-icon" src="/images/glyphicons_pro/glyphicons/png/glyphicons_244_conversation.png"> ${discussionTitle} (${discussionCount})
      </a>
      <a class="btn" href="${lib_6.workshopLink(w, embed = True, raw = True) | n}/ideas">
         <img class="workshop-nav-icon" src="/images/glyphicons_pro/glyphicons/png/glyphicons_064_lightbulb.png"> ${ideaTitle} (${ideaCount})
      </a>
      <a class="btn" ${'href="' + lib_6.workshopLink(w, embed = True, raw = True) + '/resources"' | n}>
         <img class="workshop-nav-icon" src="/images/glyphicons_pro/glyphicons/png/glyphicons_050_link.png"> ${resourceTitle} (${resourceCount})
      </a>
   % elif listingType == 'ideas' or listingType == 'idea':
      ##<a class="btn" href="${lib_6.workshopLink(w, embed = True, raw = True) | n}/wiki">
      ##   <img class="workshop-nav-icon" src="/images/glyphicons_pro/glyphicons/png/glyphicons_351_book_open.png"> Wiki
      ##</a>
      <a class="btn" ${'href="' + lib_6.workshopLink(w, embed = True, raw = True) + '/discussion"' | n}>
         <img class="workshop-nav-icon" src="/images/glyphicons_pro/glyphicons/png/glyphicons_244_conversation.png"> ${discussionTitle} (${discussionCount})
      </a>
      <a class="btn selected-nav" ${'href="' + lib_6.workshopLink(w, embed = True, raw = True) + '/ideas"' | n}>
         <img class="workshop-nav-icon" src="/images/glyphicons_pro/glyphicons/png/glyphicons_064_lightbulb.png"> ${ideaTitle} (${ideaCount})
      </a>
      <a class="btn" ${'href="' + lib_6.workshopLink(w, embed = True, raw = True) + '/resources"' | n}>
         <img class="workshop-nav-icon" src="/images/glyphicons_pro/glyphicons/png/glyphicons_050_link.png"> ${resourceTitle} (${resourceCount})
      </a>
   % elif listingType == 'resources' or listingType == 'resource':
      ##<a class="btn" href="${lib_6.workshopLink(w, embed = True, raw = True) | n}/wiki">
      ##   <img class="workshop-nav-icon" src="/images/glyphicons_pro/glyphicons/png/glyphicons_351_book_open.png"> Wiki
      ##</a>
      <a class="btn" ${'href="' + lib_6.workshopLink(w, embed = True, raw = True) + '/discussion"' | n}>
         <img class="workshop-nav-icon" src="/images/glyphicons_pro/glyphicons/png/glyphicons_244_conversation.png"> ${discussionTitle} (${discussionCount})
      </a>
      <a class="btn" ${'href="' + lib_6.workshopLink(w, embed = True, raw = True) + '/ideas"' | n}>
         <img class="workshop-nav-icon" src="/images/glyphicons_pro/glyphicons/png/glyphicons_064_lightbulb.png"> ${ideaTitle} (${ideaCount})
      </a>
      <a class="btn selected-nav" ${'href="' + lib_6.workshopLink(w, embed = True, raw = True) + '/resources"' | n}>
         <img class="workshop-nav-icon" src="/images/glyphicons_pro/glyphicons/png/glyphicons_050_link.png"> ${resourceTitle} (${resourceCount})
      </a>
   % endif
   </div>
</%def>

<%def name="slideshow(w)">
   <% 
      slides = slideshowLib.getSlidesInOrder(w['mainSlideshow_id']) 
      slideNum = 0
   %>
   <ul class="block-grid gallery" data-clearing>
      % for slide in slides:
         %if slide['deleted'] != '1':
            ${_slide(slide, slideNum)}
            <% slideNum += 1 %>
         % endif
      % endfor
   </ul>
</%def>

<%def name="_slide(slide, slideNum)">
   % if slideNum == 0:
      <li class="clearing-feature">
   % else:
      <li>
   % endif
      % if slide['pictureHash'] == 'supDawg':
         <a href="/images/slide/slideshow/${slide['pictureHash']}.slideshow">
            <img src="/images/slide/slideshow/${slide['pictureHash']}.slideshow" data-caption="${slide['caption']}"/>
         </a>
      % else:
         <a href="/images/slide/${slide['directoryNumber']}/slideshow/${slide['pictureHash']}.slideshow">
            <img src="/images/slide/${slide['directoryNumber']}/slideshow/${slide['pictureHash']}.slideshow" data-caption="${slide['caption']}"/>
         </a>
      % endif
   </li>
</%def>

<%def name="showInfo(workshop)">
    % if c.information and 'data' in c.information:
        ${misaka.html(c.information['data']) | n}
    % endif
</%def>