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
                  <% itemTitle = '<h5><a %s class="listed-item-title">%s</a></h5>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=True), item['title']) %>
                  ${itemTitle | n}
                  Posted by ${lib_6.userLink(item.owner)} from ${lib_6.userGeoLink(item.owner)}
                  % if thing == 'resources':
                     <br />
                     <% comments = '<a %s>%s</a>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=False), 'comments') %>
                     See ${comments | n}
                  % endif
               </div><!--/.span9-->
            </div><!--/.row-fluid-->
         </li>
      % endfor
   </ul>
</%def>