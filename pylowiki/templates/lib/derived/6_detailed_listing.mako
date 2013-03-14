<%!
   from pylowiki.lib.db.user import getUserByID
   import pylowiki.lib.db.discussion as discussionLib
%>

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="showListing(thing)">
   <%
      target = "_self"
      if c.paginator != '':
         renderList = c.paginator
      else:
         if thing == 'discussion':
            renderList = c.discussions
         elif thing == 'resources':
            renderList = c.resources
            target = "_blank"
         elif thing == 'ideas':
            renderList = c.ideas
   %>
   <ul class="unstyled">
      % for item in renderList:
         <% 
            if c.demo:
               author = getUserByID(item.owner)
               if not c.privs['admin']:
                  if 'user' in session:
                     if (author['accessLevel'] != '300' and author.id != c.authuser.id):
                        continue
                  else:
                     if author['accessLevel'] != '300':
                        continue
            author = getUserByID(item.owner)
         %>
         <li>
            % if item['disabled'] == '1':
                <div class="row-fluid list-item disabled">
            % else:
                <div class="row-fluid list-item">
            % endif
               <div class="span1 voteBlock">
                  ${lib_6.upDownVote(item)}
               </div>
               <div class="span2">
                  ${lib_6.userImage(author, className = 'avatar')}
               </div> <!--/.span2-->
               <div class="span9 list-item-text">
                  <% itemTitle = '<h5><a %s class="listed-item-title" target="%s">%s</a></h5>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=True), target, lib_6.ellipsisIZE(item['title'], 150)) %>
                  ${itemTitle | n}
                  Posted by ${lib_6.userLink(item.owner)} from ${lib_6.userGeoLink(item.owner)}
                     <br />
                     <% 
                        comments = '<a %s>%s</a>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=False), 'comments') 
                        numComments = discussionLib.getDiscussionForThing(item)['numComments']
                     %>
                     See ${comments | n} (${numComments})
                     % if item['disabled'] == '1':
                        <small>(this has been disabled)</small>
                     % endif
               </div><!--/.span9-->
            </div><!--/.row-fluid-->
         </li>
      % endfor
   </ul>
</%def>