<%!
   import pylowiki.lib.db.user          as userLib
   import pylowiki.lib.db.discussion    as discussionLib
   import pylowiki.lib.db.event         as eventLib
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
               author = userLib.getUserByID(item.owner)
               if not c.privs['admin']:
                  if 'user' in session:
                     if (author['accessLevel'] != '300' and author.id != c.authuser.id):
                        continue
                  else:
                     if author['accessLevel'] != '300':
                        continue
            author = userLib.getUserByID(item.owner)
         %>
         <li>
            % if item['disabled'] == '1':
                <div class="accordion" id="item-${item['urlCode']}">
                    <div class="accordion-group no-border">
                        <div class="accordion-heading disabled">
                            <div class="collapsed-item-header">
                                <button class="accordion-toggle inline btn btn-mini collapsed" data-toggle="collapse" data-parent="#item-${item['urlCode']}" href="#item-body-${item['urlCode']}">Show</button>
                                <%
                                    (disabler, reason) = getDisabledMessage(item)
                                %>
                                <small>This item has been disabled by ${lib_6.userLink(disabler)} because: ${reason}</small>
                            </div>
                            <div class="accordion-body collapse" id="item-body-${item['urlCode']}">
                                <div class="row-fluid list-item">
                                    <div class="span2 offset1">
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
                                    </div><!--/.span9-->
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            % else:
                <div class="row-fluid list-item">
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
                    </div><!--/.span9-->
                </div><!--/.row-fluid-->
            % endif
         </li>
      % endfor
   </ul>
</%def>

<%def name="getDisabledMessage(thing)">
    <%
        event = eventLib.getEventsWithAction(thing, 'disabled')[0]
        disabler = userLib.getUserByID(event.owner)
        reason = event['reason']
        return (disabler, reason)
    %>
</%def>