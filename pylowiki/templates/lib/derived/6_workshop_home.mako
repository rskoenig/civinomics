<%namespace name="lib_6" file="/lib/6_lib.mako" />

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