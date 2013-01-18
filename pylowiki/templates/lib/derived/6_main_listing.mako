<%! 
   from pylowiki.lib.db.user import getUserByID
   from pylowiki.lib.db.workshop import getWorkshopByID, getWorkshopByCode
   import pylowiki.lib.db.follow as followLib
   import pylowiki.lib.db.activity as activityLib
%>
<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="show_workshop(w)">
<div class="wrap-workshop">
   <div class="viewport">
      <a ${lib_6.workshopLink(w)}>
         <span class="dark-background"> ${lib_6.ellipsisIZE(w['description'], 150)} </span>
         % if w['mainImage_hash'] == 'supDawg':
            <img src="/images/${w['mainImage_identifier']}/slideshow/${w['mainImage_hash']}.slideshow" alt="${w['title']}" title="${w['title']}">
         % else:
            <img src="/images/${w['mainImage_identifier']}/${w['mainImage_directoryNum']}/slideshow/${w['mainImage_hash']}.slideshow" alt="${w['title']}" title="${w['title']}">
         % endif
      </a>
   </div>
      <p class="centered orange">
         <a ${lib_6.workshopLink(w)}> ${w['title']} </a>
      </p>
      <small>
          ${lib_6.ellipsisIZE(w['description'], 100)}
      </small>
      <p class="pull-right orange workshop-listing-info"> 
         <a ${lib_6.workshopLink(w)}> <!-- Num watchers -->
            ${len(followLib.getWorkshopFollowers(w))}
            <img class="small-eye" src="/images/glyphicons_pro/glyphicons/png/glyphicons_051_eye_open.png">
         </a> <!-- /Num watchers -->
         <a ${lib_6.workshopLink(w)}> <!-- Num inputs -->
            ${len(activityLib.getActivityForWorkshop(w['urlCode']))}
            <img class="small-bulb" src="/images/glyphicons_pro/glyphicons/png/glyphicons_064_lightbulb.png">
         </a> <!-- /Num inputs -->
      </p>
</div>
</%def>

<%def name="showActivity(item)">
   <%
      thisUser = getUserByID(item.owner)
   %>
   <div class="span4 avatar"> <!-- avatar -->
      ${lib_6.userImage(thisUser, className = 'avatar')}
   </div> <!-- /avatar -->
   
   <div class="span8 avatar"> <!-- information -->
      <p class="feed">
         <%
            lib_6.userLink(thisUser, className = 'green green-hover', maxChars = 25)
            activityStr = ''
            title = lib_6.ellipsisIZE(item['title'], 40)
            w = getWorkshopByCode(item['workshopCode'])
            if item.objType == 'resource':
               activityStr += 'added the resource '
               activityStr += '<a %s>%s</a>' % (lib_6.resourceLink(item, w, embed=True), title)
            elif item.objType == 'suggestion':
               activityStr += 'suggested '
               activityStr += '<a %s>%s</a>' %(lib_6.suggestionLink(item, w, embed=True), title)
            elif item.objType == 'discussion':
               activityStr += 'started the discussion '
               activityStr += '<a %s>%s</a>' %(lib_6.discussionLink(item, w, embed=True), title)
            elif item.objType == 'idea':
                activityStr += 'posed the idea '
                activityStr += '<a %s>%s</a>' %(lib_6.ideaLink(item, w, embed=True), title)
            else:
               activityStr += 'fucked up'
         %>
         ${activityStr | n}
      </p>
   </div> <!-- /information -->
</%def>