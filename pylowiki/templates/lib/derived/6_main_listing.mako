<%! 
   from pylowiki.lib.db.user import getUserByID
   from pylowiki.lib.db.workshop import getWorkshopByID, getWorkshopByCode
   import pylowiki.lib.db.follow    as followLib
   import pylowiki.lib.db.activity  as activityLib
   import pylowiki.lib.db.goal      as goalLib
%>
<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="show_workshop(w)">
<% goals = goalLib.getGoalsForWorkshop(w) %>
<div class="wrap-workshop">
   <div class="viewport">
      <a ${lib_6.workshopLink(w)}>
         <span class="dark-background">
            % if not goals:
               This workshop has no goals!
            % else:
               <ul>
               % for goal in goals:
                  % if goal['status'] == u'100':
                     <li class="done-true">${goal['title']}</li>
                  % else:
                     <li>${goal['title']}</li>
                  % endif
               % endfor
               </ul>
            % endif
         </span>
         % if w['mainImage_hash'] == 'supDawg':
            <img src="/images/${w['mainImage_identifier']}/slideshow/${w['mainImage_hash']}.slideshow" alt="${w['title']}" title="${w['title']}">
         % else:
            <img src="/images/${w['mainImage_identifier']}/${w['mainImage_directoryNum']}/slideshow/${w['mainImage_hash']}.slideshow" alt="${w['title']}" title="${w['title']}">
         % endif
      </a>
   </div>
      <p class="centered orange">
         <a ${lib_6.workshopLink(w)}> ${lib_6.ellipsisIZE(w['title'], 50)} </a>
      </p>
      <div class="workshop-listing-info">
         <span>
            <small>
                ${lib_6.ellipsisIZE(w['description'], 100)}
            </small>
         </span>
         <span class="pull-right orange workshop-listing-info-icons"> 
            <a ${lib_6.workshopLink(w)}> <!-- Num watchers -->
               ${len(followLib.getWorkshopFollowers(w))}
               <img class="small-eye" src="/images/glyphicons_pro/glyphicons/png/glyphicons_072_bookmark.png">
            </a> <!-- /Num watchers -->
            <a ${lib_6.workshopLink(w)}> <!-- Num inputs -->
               ${len(activityLib.getActivityForWorkshop(w['urlCode']))}
               <img class="small-bulb" src="/images/glyphicons_pro/glyphicons/png/glyphicons_030_pencil.png">
            </a> <!-- /Num inputs -->
         </span>
      </div>
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