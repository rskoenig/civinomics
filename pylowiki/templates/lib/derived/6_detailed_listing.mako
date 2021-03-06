<%!
   import pylowiki.lib.db.user          as userLib
   import pylowiki.lib.db.discussion    as discussionLib
   import pylowiki.lib.db.event         as eventLib
   import pylowiki.lib.db.facilitator   as facilitatorLib
%>

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="showListing(thing, *args)">
   <%
      target = "_self"
      if c.paginator != '':
         renderList = c.paginator
      else:
         if thing == 'discussion':
            renderList = c.discussions
         elif thing == 'resources':
            if 'condensed' in args:
                renderList = c.resources[0:5]
            else:
                renderList = c.resources
            target = "_blank"
         elif thing == 'ideas':
            renderList = c.ideas
            
   %>
   <ul class="unstyled">
      <% itemCounter = 0 %>
      % for item in renderList:
         <% 
            if c.demo:
               author = userLib.getUserByID(item.owner)
               if not c.privs['admin']:
                  if 'user' in session:
                     if ((author['accessLevel'] != '300' and not facilitatorLib.isFacilitator(author, c.w)) and author.id != c.authuser.id):
                        continue
                  else:
                     if author['accessLevel'] != '300' and not facilitatorLib.isFacilitator(author, c.w):
                        continue
            author = userLib.getUserByID(item.owner)
            
            authorClass = 'row-fluid list-item'
            addedAs = ''
            if item['addedAs'] == 'admin':
                authorClass += ' admin'
                addedAs += '(admin) '
            if item['addedAs'] == 'facilitator':
                authorClass += ' facilitator'
                addedAs += '(facilitator) '
            if item['addedAs'] == 'listener':
                authorClass += ' listener'
                addedAs += '(listener) '
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
                                    % if thing != 'resources':
                                        <div class="span2 offset1">
                                            ${lib_6.userImage(author, className = 'avatar')}
                                        </div> <!--/.span2-->
                                    % endif
                                    <div class="span9 list-item-text" id="content_${itemCounter}">
                                        <% itemTitle = '<h5 class="no-bottom"><a %s class="listed-item-title">%s</a></h5>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=False), lib_6.ellipsisIZE(item['title'], 150)) %>
                                        ${itemTitle | n}
                                        % if item.objType == 'resource':
                                            <p>
                                            <% itemLink = '<small>(<a %s>%s</a>)</small>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=True), lib_6.ellipsisIZE(item['link'], 75)) %>
                                            ${itemLink | n}
                                            </p>
                                        % endif
                                        <p class="no-bottom">
                                            <small>Posted by ${lib_6.userLink(item.owner)} ${addedAs}from ${lib_6.userGeoLink(item.owner)} ${item.date}</small>
                                        </p>
                                            <% 
                                                comments = '<a %s>%s</a>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=False), 'comments') 
                                                numComments = discussionLib.getDiscussionForThing(item)['numComments']
                                            %>
                                            % if c.demo:
                                                See ${comments | n}
                                            % else:
                                                See ${comments | n} (${numComments}) 
                                            % endif
                                    </div><!--/.span9-->
                                    <%doc>
                                    <div class="span9 list-item-text">
                                        <% itemTitle = '<h5><a %s class="listed-item-title" target="%s">%s</a></h5>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=True), target, lib_6.ellipsisIZE(item['title'], 150)) %>
                                        ${itemTitle | n}
                                        Posted by ${lib_6.userLink(item.owner)} from ${lib_6.userGeoLink(item.owner)} ${item.date}
                                            <br />
                                            <% 
                                                comments = '<a %s>%s</a>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=False), 'comments') 
                                                numComments = discussionLib.getDiscussionForThing(item)['numComments']
                                            %>
                                            See ${comments | n} (${numComments})
                                    </div><!--/.span9-->
                                    </%doc>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            % else:
                <div class="row-fluid list-item border-bottom">
                    % if not 'condensed' in args:
                        <div class="span1 voteBlock" id="vote_${itemCounter}">
                            ${lib_6.upDownVote(item)}
                        </div>
                    % endif
                    <%
                        if 'condensed' in args:
                            spanX = "span2"
                        else:
                            spanX = "span1"
                    %>
                    % if thing == 'resources':
                        <% 
                            iconClass = ""
                            if item['type'] == 'link' or item['type'] == 'general':
                                iconClass="icon-link"
                            elif item['type'] == 'photo':
                                iconClass="icon-picture"
                            elif item['type'] == 'video':
                                iconClass="icon-youtube-play"
                            elif item['type'] == 'rich':
                                iconClass="icon-file"
                            endif
                        %>
                        <div class="${spanX}">
                            <div class="spacer"></div>
                            <i class="${iconClass} icon-3x"></i>
                        </div>
                    % elif not 'condensed' in args:
                        <div class="${spanX}">
                            <div class="spacer"></div>
                            <i class="icon-comments icon-3x"></i>
                        </div> <!--/.span2-->
                    % endif
                    <%
                        spanY = "span10"
                        discStyle = ''
                        if thing == 'discussion':
                            discStyle = "forum-topic"
                            if 'condensed' in args:
                                spanY = "span12"
                    %>
                    <div class="${spanY} list-item-text" id="content_${itemCounter}">
                        <h4 class="media-heading ${discStyle}">
                            <% itemTitle = '<a %s class="listed-item-title">%s</a>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=False), lib_6.ellipsisIZE(item['title'], 150)) %>
                            ${itemTitle | n}
                        </h4>

                        % if item.objType == 'resource':
                            <% 
                                if 'condensed' in args:
                                    chars = 35
                                else:
                                    chars = 70
                                itemLink = '<a %s>%s</a>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=True), lib_6.ellipsisIZE(item['link'], chars)) %>

                            ${itemLink | n}
                        % endif

                            <% 
                                comments = '<a %s class="listed-item-title"><i class="icon-comments"></i> %s</a>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=False), ' Comments') 
                                numComments = discussionLib.getDiscussionForThing(item)['numComments']
                                if 'views' in item:
                                    numViews = str(item['views'])
                                else:
                                    numViews = "0"
                            %>
                            <br />
                            <ul class="horizontal-list iconListing">
                                <li>
                                    % if c.demo:
                                        ${comments | n}
                                    % else:
                                        ${comments | n} (${numComments})
                                    % endif
                                </li>
                                <li>
                                    <i class="icon-eye-open"></i> Views ${numViews}
                                </li>

                            % if item.objType != 'resource':
                                % if not 'condensed' in args:
                                    <li><span id="author_${itemCounter}" class="left-space">${lib_6.userImage(author, className = 'avatar topbar-avatar')}</span><small> Posted by ${lib_6.userLink(item.owner)} ${addedAs} from ${lib_6.userGeoLink(item.owner)} ${item.date}</small></li>
                                % endif
                            % endif
                            </ul>
                    </div><!--/.span9-->
                </div><!--/.row-fluid-->
            % endif
         </li>
         <% itemCounter += 1 %>
      % endfor
   </ul>
</%def>

<%def name="showIdeaListing(thing)">
   <%
      target = "_self"
      if c.paginator != '':
         renderList = c.paginator
      else:
         if thing == 'ideas':
            renderList = c.ideas
            
   %>
   <ul class="unstyled">
      <% itemCounter = 0 %>
      % for item in renderList:
         <% 
            if c.demo:
               author = userLib.getUserByID(item.owner)
               if not c.privs['admin']:
                  if 'user' in session:
                     if ((author['accessLevel'] != '300' and not facilitatorLib.isFacilitator(author, c.w)) and author.id != c.authuser.id):
                        continue
                  else:
                     if author['accessLevel'] != '300' and not facilitatorLib.isFacilitator(author, c.w):
                        continue
            author = userLib.getUserByID(item.owner)
            
            authorClass = 'row-fluid list-item'
            addedAs = ''
            if item['addedAs'] == 'admin':
                authorClass += ' admin'
                addedAs += '(admin) '
            if item['addedAs'] == 'facilitator':
                authorClass += ' facilitator'
                addedAs += '(facilitator) '
            if item['addedAs'] == 'listener':
                authorClass += ' listener'
                addedAs += '(listener) '
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
                                <div class="row-fluid list-item border-bottom">
                                    <div class="span9 offset1 list-item-text ideaListing" style="position:relative;" id="content_${itemCounter}">
                                        <% itemTitle = '<p class="ideaListingTitle"><a %s class="listed-item-title">%s</a></p>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=False), lib_6.ellipsisIZE(item['title'], 150)) %>
                                        ${itemTitle | n}
                                        % if item['adopted'] == '1':
                                            <small><i class="icon-star"></i> This idea adopted!</small>
                                        % endif
                                        <p style="margin-top: 10px;">${lib_6.ellipsisIZE(item['text'], 250)}</p>
                                            <% 
                                                comments = '<a %s class="listed-item-title"><i class="icon-comment"></i> %s</a>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=False), 'Comments')
                                                fullText = '<a %s class="listed-item-title"><i class="icon-file-text"></i> %s</a>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=False), 'Read full text') 
                                                numComments = discussionLib.getDiscussionForThing(item)['numComments']

                                                totalVotes = int(item['ups']) + int(item['downs'])
                                            %>
                                            <ul class="horizontal-list iconListing">
                                                <li>${lib_6.userImage(author, className = 'avatar topbar-avatar')}</span> Posted by ${lib_6.userLink(item.owner)} ${addedAs} ${item.date}</li>
                                                <li>${fullText | n}</li>
                                                % if c.demo:
                                                    <li>${comments | n}</li>
                                                % else:
                                                    <li>${comments | n} (${numComments})</li>
                                                % endif
                                            </ul>
                                    </div><!--/.span9-->
                                    <div class="span3 voteBlock ideaListing" id="vote_${itemCounter}">
                                        ${lib_6.yesNoVote(item)}
                                    </div>
                                </div><!--/.row-fluid-->
                            </div><!-- accordion body -->
                        </div><!-- accordion heading -->
                    </div><!-- accordion group -->
                </div><!-- accordion --> 
            % else:
                <div class="row-fluid list-item border-bottom">
                    <div class="span9 list-item-text ideaListing" id="content_${itemCounter}">
                        <% itemTitle = '<p class="ideaListingTitle"><a %s class="listed-item-title">%s</a></p>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=False), lib_6.ellipsisIZE(item['title'], 150)) %>
                        ${itemTitle | n}
                        % if item['adopted'] == '1':
                            <small><i class="icon-star"></i> This idea adopted!</small>
                        % endif
                        <p style="margin-top: 10px;">${lib_6.ellipsisIZE(item['text'], 250)}</p>
                            <% 
                                comments = '<a %s class="listed-item-title"><i class="icon-comment"></i> %s</a>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=False), 'Comments')
                                fullText = '<a %s class="listed-item-title"><i class="icon-file-text"></i> %s</a>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=False), 'Read full text')
                                numComments = "0"
                                if 'numComments' in item:
                                    numComments = item['numComments']
                                    
                                #numComments = discussionLib.getDiscussionForThing(item)['numComments']
                                if 'views' in item:
                                    numViews = str(item['views'])
                                else:
                                    numViews = "0"
                                views = '<i class="icon-eye-open"></i> Views %s</a>'%numViews

                                totalVotes = int(item['ups']) + int(item['downs'])
                            %>
                            <ul class="horizontal-list iconListing">
                                <li>${lib_6.userImage(author, className = 'avatar topbar-avatar')}</span> Posted by ${lib_6.userLink(item.owner)} ${addedAs} on ${item.date}</li>
                            </ul><br />
                            <ul class="horizontal-list iconListing">
                                <li>${fullText | n}</li>
                                % if c.demo:
                                    <li>${comments | n}</li>
                                % else:
                                    <li>${comments | n} (${numComments})</li>
                                % endif
                                <li>${views | n}</li>
                            </ul>
                    </div><!--/.span9-->
                    <div class="span3 voteBlock ideaListing well" style="background-color: whiteSmoke;" id="vote_${itemCounter}">
                        ${lib_6.yesNoVote(item)}
                    </div>
                </div><!--/.row-fluid-->
            % endif
         </li>
         <% itemCounter += 1 %>
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