<%!
   from pylowiki.lib.db.user import getUserByID
%>

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="showListing(thing)">
   <%
      if c.paginator != '':
         renderList = c.paginator
      else:
         if thing == 'discussion':
            renderList = c.discussions
         elif thing == 'resource':
            renderList = c.resources
         elif thing == 'ideas':
            renderList = c.ideas
   %>
   <ul class="unstyled">
      % for item in renderList:
         <% author = getUserByID(item.owner) %>
         <li>
            <div class="row-fluid list-item">
               <div class="span1 voteBlock">
                  ${lib_6.upDownVote(item)}
               </div>
               <div class="span2">
                  ${lib_6.userImage(author, className = 'avatar')}
               </div> <!--/.span2-->
               <div class="span9 list-item-text">
                  <% itemTitle = '<h5><a %s>%s</a></h5>' %(lib_6.discussionLink(item, c.w, embed=True), item['title']) %>
                  ${itemTitle | n}
               </div><!--/.span9-->
            </div><!--/.row-fluid-->
         </li>
      % endfor
   </ul>
</%def>