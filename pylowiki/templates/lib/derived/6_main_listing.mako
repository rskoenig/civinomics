<%! 
   from pylowiki.lib.db.user import getUserByID
   import pylowiki.lib.db.workshop      as workshopLib
   import pylowiki.lib.db.initiative    as initiativeLib
   import pylowiki.lib.db.follow        as followLib
   import pylowiki.lib.db.activity      as activityLib
   import pylowiki.lib.db.goal          as goalLib
   import pylowiki.lib.db.mainImage     as mainImageLib
%>
<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="show_workshop(w)">
   <% 
      goals = goalLib.getGoalsForWorkshop(w) 
      mainImage = mainImageLib.getMainImage(w)
   %>
   <div class="viewport">
      <a ${lib_6.workshopLink(w)}>
         <span class="dark-background">
            % if not goals:
               This workshop has no goals!
            % else:
               <div class="goals-preview">
                  Goals:
                  <br>
                  <ul>
                  <% count = 0 %>
                  % for goal in goals:
                     % if count <= 2:
                        % if goal['status'] == u'100':
                           <li class="done-true">${goal['title']}</li>
                        % else:
                           <li>${goal['title']}</li>
                        % endif
                        <% count += 1%>
                     % endif
                  % endfor
                  </ul>
                  % if len(goals) > 3:
                     <% moreGoals = len(goals) - 3 %>
                     <p class="centered more">${moreGoals} more</p>
                  % endif
               </div>
            % endif
         </span>
         <% 
            if mainImage['pictureHash'] == 'supDawg':
               imgSrc="/images/slide/thumbnail/supDawg.thumbnail"
            elif 'format' in mainImage.keys():
                imgSrc="/images/mainImage/%s/listing/%s.%s" %(mainImage['directoryNum'], mainImage['pictureHash'], mainImage['format'])
            else:
               imgSrc="/images/mainImage/%s/listing/%s.jpg" %(mainImage['directoryNum'], mainImage['pictureHash'])
         %>
         <div style="background-image:url('${imgSrc}');"></div>
      </a>
   </div>
   <div class="span workshop-listingTitle">
      <strong><a ${lib_6.workshopLink(w)}> ${lib_6.ellipsisIZE(w['title'], 60)} </a></strong>
   </div>
   <div class="workshop-listing-info">
      <%
        if 'numBookmarks' in w:
            numBookmarks = w['numBookmarks']
        else:
            numBookmarks = len(followLib.getWorkshopFollowers(w))
            
        if 'numPosts' in w:
            numPosts = w['numPosts']
        else:
            numPosts = len(activityLib.getActivityForWorkshop(w['urlCode']))
      %>
      <span class="workshop-listing-info-icons"> 
         <img class="small-bookmark" data-toggle="tooltip" title="Members who have bookmarked this workshop" src="/images/glyphicons_pro/glyphicons/png/glyphicons_072_bookmark.png">
         <a ${lib_6.workshopLink(w)}> <!-- Num watchers -->
            <strong>${str(numBookmarks)}</strong>
         </a><span>BOOKMARKS</span> <!-- /Num watchers -->
      </span>
      <span class="workshop-listing-info-icons"> 
         <img class="small-bulb" data-toggle="tooltip" title="Ideas, conversations, resources, comments" src="/images/glyphicons_pro/glyphicons/png/glyphicons_150_edit.png">
         <a ${lib_6.workshopLink(w)}> <!-- Num inputs -->
            <strong>${str(numPosts)}</strong>
         </a><span>POSTS</span> <!-- /Num inputs -->
      </span>
   </div>
</%def>

<%def name="showActivity(item, **kwargs)">
   <div class="media">
      <%
        if 'workshopCode' in item:
            parent = workshopLib.getWorkshopByCode(item['workshopCode'])
        elif 'initiativeCode' in item:
            parent = initiativeLib.getInitiative(item['initiativeCode'])
        else:
            parent = item
        
        thisUser = getUserByID(item.owner)
      %>
      <div class="pull-left"> ${lib_6.userImage(thisUser, className = 'avatar', linkClass = 'media-object')}</div> 
      <div class="media-body">
         ${lib_6.userLink(thisUser, className = 'green green-hover', maxChars = 25)} 
         ${lib_6.showItemInActivity(item, parent, **kwargs)}
      </div>
   </div>
</%def>
