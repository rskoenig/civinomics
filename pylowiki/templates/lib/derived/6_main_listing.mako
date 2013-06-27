<%! 
   from pylowiki.lib.db.user import getUserByID
   import pylowiki.lib.db.workshop      as workshopLib
   import pylowiki.lib.db.follow        as followLib
   import pylowiki.lib.db.activity      as activityLib
   import pylowiki.lib.db.goal          as goalLib
   import pylowiki.lib.db.mainImage     as mainImageLib
%>
<%namespace name="lib_6" file="/lib/6_lib.mako" />
<%namespace name="helpers" file="/lib/derived/6_profile.mako" />

<%def name="show_workshop(w)">
   <% 
      goals = goalLib.getGoalsForWorkshop(w) 
      mainImage = mainImageLib.getMainImage(w)
   %>
   <div class="viewport">
      <a ${lib_6.workshopLink(w)}>
         <span class="dark-background">
            % if not w['description']:
               <em>This workshop has no description</em>
            % else:
               <small>
                  ${lib_6.ellipsisIZE(w['description'], 100)}
               </small>
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
         <div style="width:100%; height:190px; background-image:url('${imgSrc}'); background-repeat:no-repeat; background-size:cover; background-position:center;"></div>
      </a>
   </div>
      <div class="span workshop-listingTitle">
         <strong><a ${lib_6.workshopLink(w)}> ${lib_6.ellipsisIZE(w['title'], 60)} </a></strong>
      </div>
      <div class="workshop-listing-info">
         <span class="workshop-listing-info-icons">
            <img class="small-bookmark" data-toggle="tooltip" title="Followers" src="/images/glyphicons_pro/glyphicons/png/glyphicons_072_bookmark.png">
            <a ${lib_6.workshopLink(w)}> <!-- Num watchers -->
            <strong>${len(followLib.getWorkshopFollowers(w))}</strong>
            </a><span>BOOKMARKS</span> <!-- /Num watchers -->
         </span>
         <span class="workshop-listing-info-icons">
            <img class="small-bulb" data-toggle="tooltip" title="Ideas, conversations, resources, comments" src="/images/glyphicons_pro/glyphicons/png/glyphicons_030_pencil.png">
            <a ${lib_6.workshopLink(w)}> <!-- Num inputs -->
            <strong>${len(activityLib.getActivityForWorkshop(w['urlCode']))}</strong>
            </a><span>OBJECTS</span> <!-- /Num inputs -->
         </span>
      </div>
</%def>

<%def name="showActivity(item, **kwargs)">
   <div class="media">
      <%
         workshop = workshopLib.getWorkshopByCode(item['workshopCode'])
         workshopLink = lib_6.workshopLink(workshop, embed=True)
         thisUser = getUserByID(item.owner)
      %>
      <table>
         <tr>
            <td class="span2" rowspan="4" style = "vertical-align: top;">${helpers.showWorkshop(workshop, imageOnly = True)}</td>
            <td class="span8"><div class="well" style="margin-bottom: 4px; padding: 4px; background-color: #f3fff2;"><a ${workshopLink | n}> ${workshop['title']}</a></div></td>
         </tr>
         <tr>
            <td class="span8">
               <div class="well" style="margin-bottom: 10px; padding: 4px; min-height: 51px;">
                  <div class="pull-left"> ${lib_6.userImage(thisUser, className = 'avatar med-avatar', linkClass = 'media-object')}</div>
                  <div class="media-body">
                     ${lib_6.userLink(thisUser, className = 'green green-hover', maxChars = 25)} 
                     ${lib_6.showItemInActivity(item, workshop, **kwargs)}
                  </div>
               </div>
            </td>
         </tr>
      </table>
   </div>
</%def>
