<%def name="show_workshop(w)">
   <div class="viewport">
      <a href="/workshops/${w['urlCode']}/${w['url']}">
         <span class="dark-background"> ${w['mainImage_caption']} </span>
         % if w['mainImage_hash'] == 'supDawg':
            <img src="/images/${w['mainImage_identifier']}/slideshow/${w['mainImage_hash']}.slideshow" alt="${w['title']}" title="${w['title']}">
         % else:
            <img src="/images/${w['mainImage_identifier']}/${w['mainImage_directoryNum']}/slideshow/${w['mainImage_hash']}.slideshow" alt="${w['title']}" title="${w['title']}">
         % endif
      </a>
   </div>
</%def>