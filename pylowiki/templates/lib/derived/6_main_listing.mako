<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="show_workshop(w)">
   <div class="viewport">
      <a ${lib_6.workshopLink(w)}>
         <span class="dark-background"> ${w['mainImage_caption']} </span>
         % if w['mainImage_hash'] == 'supDawg':
            <img src="/images/${w['mainImage_identifier']}/slideshow/${w['mainImage_hash']}.slideshow" alt="${w['title']}" title="${w['title']}">
         % else:
            <img src="/images/${w['mainImage_identifier']}/${w['mainImage_directoryNum']}/slideshow/${w['mainImage_hash']}.slideshow" alt="${w['title']}" title="${w['title']}">
         % endif
      </a>
   </div>
   <span>
      <p class="pull-left orange">
         <a ${lib_6.workshopLink(w)}> ${w['title']} </a>
      </p>
      <p class="pull-right orange workshop-listing-info"> 
         <a ${lib_6.workshopLink(w)}> <!-- Num watchers -->
            42 
            <img class="small-eye" src="/images/glyphicons_pro/glyphicons/png/glyphicons_051_eye_open.png">
         </a> <!-- /Num watchers -->
         <a ${lib_6.workshopLink(w)}> <!-- Num inputs -->
            303 
            <img class="small-bulb" src="/images/glyphicons_pro/glyphicons/png/glyphicons_064_lightbulb.png">
         </a> <!-- /Num inputs -->
      </p>
   </span>
</%def>