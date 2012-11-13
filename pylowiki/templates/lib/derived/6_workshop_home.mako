<%!
   from pylowiki.lib.db.slideshow import getAllSlides
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

<%def name="showActivity(c)">
   
   <%
      #resources = c.resources
      #suggestions = c.suggestions
      #discussions = c.discussion
   %>
   ${lib_6.userImage(c.authuser, className="avatar small-avatar inline")}
</%def>

<%def name="watchButton()">
   <a class="btn round pull-right" href="#">
      <img class="watch" src="/images/glyphicons_pro/glyphicons/png/glyphicons_051_eye_open.png">
      <span> Watch </span>
   </a>
</%def>

<%def name="workshopNav(w)">
   <div class="btn-group four-up">
      <a class="btn" href="${lib_6.workshopLink(w, embed = True, raw = True) | n}/wiki">
         <img class="workshop-nav-icon" src="/images/glyphicons_pro/glyphicons/png/glyphicons_351_book_open.png"> Wiki
      </a>
      <a class="btn" href="${lib_6.workshopLink(w, embed = True, raw = True) | n}/discussion">
         <img class="workshop-nav-icon" src="/images/glyphicons_pro/glyphicons/png/glyphicons_244_conversation.png"> Discussion
      </a>
      <a class="btn" href="${lib_6.workshopLink(w, embed = True, raw = True) | n}/ideas">
         <img class="workshop-nav-icon" src="/images/glyphicons_pro/glyphicons/png/glyphicons_064_lightbulb.png"> Ideas
      </a>
      <a class="btn" href="${lib_6.workshopLink(w, embed = True, raw = True) | n}/resources">
         <img class="workshop-nav-icon" src="/images/glyphicons_pro/glyphicons/png/glyphicons_050_link.png"> Resources
      </a>
   </div>
</%def>

<%def name="slideshow(w)">
   <% 
      slides = getAllSlides(w['mainSlideshow_id']) 
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