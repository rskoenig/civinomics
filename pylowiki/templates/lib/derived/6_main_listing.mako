<%! 
   from pylowiki.lib.db.user import getUserByID
   import pylowiki.lib.db.workshop      as workshopLib
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
         <% 
            if mainImage['pictureHash'] == 'supDawg':
               imgSrc="/images/slide/thumbnail/supDawg.thumbnail"
            else:
               imgSrc="/images/mainImage/%s/listing/%s.jpg" %(mainImage['directoryNum'], mainImage['pictureHash'])
         %>
         <div style="width:100%; height:190px; background-image:url('${imgSrc}'); background-repeat:no-repeat; background-size:cover; background-position:center;"></div>
      </a>
   </div>
      <p class="orange centered">
         <strong><a ${lib_6.workshopLink(w)}> ${lib_6.ellipsisIZE(w['title'], 50)} </a></strong>
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
               <img class="small-bookmark" data-toggle="tooltip" title="Followers" src="/images/glyphicons_pro/glyphicons/png/glyphicons_003_user.png">
            </a> <!-- /Num watchers -->
            <a ${lib_6.workshopLink(w)}> <!-- Num inputs -->
               ${len(activityLib.getActivityForWorkshop(w['urlCode']))}
               <img class="small-bulb" data-toggle="tooltip" title="Ideas, conversations, resources, comments" src="/images/glyphicons_pro/glyphicons/png/glyphicons_030_pencil.png">
            </a> <!-- /Num inputs -->
         </span>
      </div>
</%def>

<%def name="showActivity(item)">
   <div class="media">
      <%
         w = workshopLib.getWorkshopByCode(item['workshopCode'])
         thisUser = getUserByID(item.owner)
      %>
      <div class="pull-left"> ${lib_6.userImage(thisUser, className = 'avatar', linkClass = 'media-object')}</div> 
      <div class="media-body">
         ${lib_6.userLink(thisUser, className = 'green green-hover', maxChars = 25)} 
         ${lib_6.showItemInActivity(item, w)}
      </div>
   </div>
</%def>
