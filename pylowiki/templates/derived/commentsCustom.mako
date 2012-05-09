<%!
    from pylowiki.lib.fuzzyTime import timeSince
    from pylowiki.lib.db.user import getUserByID
    from pylowiki.lib.db.comment import getComment
    import logging
    from datetime import datetime
    log = logging.getLogger(__name__)
%>

## The header for the comment - has user's name, avatar
<%def name="userSays(comment, author)">
	<span><img src="/images/avatars/${author['pictureHash']}.thumbnail" /> <a href = "/profile/${author['urlCode']}/${author['url']}" style="color:#86945A;">${author['name']}</a> says: </span>
</%def>

## Assumes the user is already authenticated for comment editing
## Passes info to the comment controller, edit function, with the comment id as the only argument
<%def name="editComment(comment, counter)">
    <% thisID = comment.id + counter %>
    ${ h.form( url( controller = "comment", action ="edit", id = comment.id ), method="put" ) }
        <table style="width: 100%; padding: 0px; border-spacing: 0px; border: 0px; margin: 0px;"><tr><td>
        <div id = "section${thisID}" ondblclick="toggle('textareadiv${thisID}', 'edit${thisID}')">${comment['data']}</div>
        </td></tr></table>
        <div style="display:none; text-align:center;" id="textareadiv${thisID}">
            <br />
            <textarea rows="4" id="textarea${thisID}" name="textarea${thisID}" onkeyup="previewAjax( 'textarea${thisID}', 'section${thisID}' )" class="markitup">${comment.data}</textarea>
            <div style="align:right;text-align:right;">
                Optional remark: <input type="text" id="remark${thisID}"  name="remark${thisID}" class="text tiny" placeholder="optional remark"/> 
            
                <button type="submit" name = "submit" value = "submit" class="right green">Submit</button>
                ##${h.submit('submit', 'Save')}
                <input type="text" id="sremark"  name="sremark" class="text" />
                <input type="hidden" name = "discussionID" value = "${c.discussion.id}" />
            </div>
        </div>
        <div style="align:left;text-align:left;">
            <a href="javascript: toggle('textareadiv${thisID}', 'edit${thisID}', 'edit')" id="edit${thisID}" style="font-size: 12px; color:#86945A;">
                edit
            </a>
        </div>
    ${h.end_form()}
</%def>

## Displays the content of the comment
<%def name="commentContent(comment, counter)">
    <br />
        
        % if c.authuser['accessLevel'] >= 200:
            ${editComment(comment, counter)}
        % else:
            ${h.literal(h.reST2HTML(comment['data']))}
        % endif
        
</%def>

## Sets up the rating system
<%def name="displayRating(comment, counter, commentType)">
    
</%def>

## Displays the footer of the comment (post date, flag, reply, rate)
<%def name="commentMetaData(comment, counter, commentType)">
    <div class="gray comment_data left">
        <p class="time">Posted ${timeSince(datetime.strptime(comment['lastModified'], '%a %b %d %H:%M:%S %Y'))} ago </p>
        % if "user" in session:
            <p>
                <a href="#" class="gray flag">Flag comment</a>
                <a href="#" class="gray reply">Reply</a>
            </p>
            
            </div><!-- comment_data -->
            <div class="flag content left">
                ##<form action="/flagComment/${comment.id}" class="left wide">
                    <span class="dark-text">Are you sure? </span>
                    <span>
                        <a href="/flagComment/${comment.id}" style="color:red;" class = "flagComment">
                            Yes
                        </a>
                    </span>
                    <span id = 'flagged_${comment.id}'>
                        
                    </span>
                ##</form>
            </div><!-- flag_content -->
            <div class="reply content left">
                <form action="/addComment">
                    <textarea name="comment-textarea" class="content_feedback"></textarea>
                    
                    <input type="hidden" id="type" name="type" value=${commentType} />
                    <input type="hidden" name="discussionID" value=${c.discussion.id} />
                    <input type="hidden" name="parentID" value=${comment.id} />
                    <input type="hidden" name="workshopCode" value=${c.w['urlCode']} />
                    <input type="hidden" name="workshopURL" value=${c.w['url']} />
                    % if commentType == 'suggestionMain':
                        <input type="hidden" name = "suggestionCode" value = "${c.s['urlCode']}" />
                        <input type="hidden" name = "suggestionURL" value = "${c.s['url']}" />
                    % elif commentType == 'resource':
                        <input type="hidden" name = "resourceCode" value = "${c.resource['urlCode']}" />
                        <input type="hidden" name = "resourceURL" value = "${c.resource['url']}" />
                    % endif
                    
                    <button type="submit" class="green" name = "submit" value = "reply">Submit</button>
                </form>
            </div>
            ${displayRating(comment, counter, commentType)}
    % else:
        </div><!-- comment_data -->
    % endif
</%def>

## Used to create a zebra-like colorization scheme to add readability to comments
<%def name="getBackgroundColor(n)">
    % if n % 2 == 0:
        <% color = 'green' %>
    % else:
        <% color = 'white' %>
    % endif
</%def>

## Main function that gets called by the template
<%def name="comments( type )">
 % if type == "background" or type == "feedback":
    <% 
        discussion = c.discussion
    %>
 % elif type == "suggestionMain" or type == "resource":
    <%  
        discussion = c.discussion
        workshop = c.w
    %>
 % endif
 %if c.conf['allow.comments'] == 'true':

  ##<span class="gray"><a href="#">${discussion['numComments']} comments</a> | Last edited on ${c.lastmoddate} by ${c.lastmoduser['name']} | <a href="#">Suggest edits</a></span>
  % if discussion['numComments'] == '1':
     <% commentString = 'comment' %>
  % else:
     <% commentString = 'comments' %>
  % endif
  % if type == 'resource':
    <span class="gray"><a href="#" style="color:#86945A;">${discussion['numComments']} ${commentString}</a> | Last edited <span class="time">${timeSince(c.lastmoddate)}</span> ago by <a style="color:#86945A;" href = "/profile/${c.lastmoduser['urlCode']}/${c.lastmoduser['url']}">${c.lastmoduser['name']}</a></span>
  % elif type == 'suggestionMain' and "user" in session:
    <div class="gray comment_data left"><span class="gray"><a href="#">${discussion['numComments']} ${commentString}</a> | Last edited <span class="time">${timeSince(c.lastmoddate)}</span> ago by <a href = "/profile/${c.lastmoduser['urlCode']}/${c.lastmoduser['url']}">${c.lastmoduser['name']}</a> <a href="#" class="gray flag">Flag suggestion</a></span></div>

    <div class="flag content left">
       <span class="dark-text">Are you sure? </span>
       <span>
          <a href="/flagSuggestion/${c.s.id}" style="color:red;" class = "flagComment">
                            Yes
          </a>
        </span>
        <span id = 'flagged_${c.s.id}'>

        </span>
    </div><!-- flag_content -->
  % else:
    <span class="gray"><a href="#">${discussion['numComments']} ${commentString}</a> | Last edited <span class="time">${timeSince(c.lastmoddate)}</span> ago by <a href = "/profile/${c.lastmoduser['urlCode']}/${c.lastmoduser['url']}">${c.lastmoduser['name']}</a></span>
  % endif

    <div id="comments" class="left">
  <h3>Comments</h3>
        <form action="/addComment" method="post">
            <input type="hidden" id="type" name="type" value=${type} />
            <input type="hidden" name="discussionID" value=${discussion.id} />
            <input type="hidden" name="parentID" value=0 />
            % if type == "suggestionMain":
                <input type="hidden" id="url" name="suggestionURL" value="${c.s['url']}" />
                <input type="hidden" id="url" name="suggestionCode" value="${c.s['urlCode']}" />
                <input type="hidden" id="url" name="workshopCode" value="${c.w['urlCode']}" />
                <input type="hidden" id="url" name="workshopURL" value="${c.w['url']}" />
            % elif type == "background" or type == "feedback":
                <input type="hidden" id="url" name="workshopCode" value="${c.w['urlCode']}" />
                <input type="hidden" id="url" name="workshopURL" value="${c.w['url']}" />
            % elif type == "resource":
                <input type="hidden" id="url" name="workshopCode" value="${c.w['urlCode']}" />
                <input type="hidden" id="url" name="workshopURL" value="${c.w['url']}" />
                <input type="hidden" id="url" name="resourceCode" value="${c.resource['urlCode']}" />
                <input type="hidden" id="url" name="resourceURL" value="${c.resource['url']}" />
            % endif
            % if "user" in session:
            add a comment
            <br />
            
            <textarea rows="4" id="comment-textarea" name="comment-textarea" onkeyup="previewAjax( 'comment-textarea', 'comment-preview-div' )" class="markitup" style="width:500px;"></textarea>  
            <div id="comment-preview-div"></div>
            <div style="align:right; text-align:right; padding-right:10px;">
                ##${h.submit('submit', 'Comment')}
                <button type="submit" name = "submit" value = "submit" class="right green">Submit</button>
            </div>
            <br />
            % else:
            <h3 class="utility"> 
              Please <a href="/login">login</a> or <a href="/register">register</a> to leave a comment!
              </h3>
            %endif
        </form>
        
        <h4>Comments</h4>
        <ul id="featuredComments">
            <% 
                counter = 1000
                maxDepth = 4
                curDepth = 0
                if 'children' in discussion.keys():
                    recurseCommentTree(discussion, counter, type, maxDepth, curDepth)
                    
            %>
        </ul>
  ##<div id="show-comment"><a href="javascript: toggle('comment-section', 'show-comment-link', 'Show all ${discussion['numComments']} comments')" id="show-comment-link" style="font-size: 12px;">Show all ${discussion['numComments']} comments</a></div>
 
 %endif

</%def>

<%def name="recurseCommentTree(tree, counter, commentType, maxDepth, curDepth)">
    <%
        if not tree:
            return
        if type(tree) == type(1):
            tree = getComment(tree)
            log.info('Comment %s being processed now' % tree)
            #return
        #if curDepth >= maxDepth or tree['children'] == 0 or len(tree['children'].split(',')) < 1:
        if curDepth >= maxDepth or tree['children'] == 0:
            return
        for child in [int(item) for item in tree['children'].split(',')]:
            log.info('children: %s' % tree['children'])
            # Hack to resolve slight difference between discussion objects and comment objects
            if type(child) == type(1L):
                child = tree.children[child]
            if child == 0:
                pass
            try:
                displayComment(child, counter, commentType, curDepth)
                recurseCommentTree(child, counter, commentType, maxDepth, curDepth + 1)
            except:
                raise
                #log.info('Error with comment %s, it has children %s'%(tree.id, tree.children[0].id))
    %>
</%def>

<%def name="displayComment(comment, counter, commentType, curDepth)">
    <% 
        comment = getComment(comment)
        if comment:
            author = getUserByID(comment.owner)
        else:
            return
    %>
    <li>
        ## This can be refactored into one set of function calls
        % if int(comment['parent']) == 0:
            ${userSays(comment, author)}
            ${commentContent(comment, counter)}
            ${commentMetaData(comment, counter, commentType)}
        % else:
            <% 
                padding = 10
                indentAmt = 10
                divWidth = 599
                indent = curDepth * indentAmt
                width = divWidth - (2 * padding) - (curDepth * indentAmt) 
            %>
            <div class="comment_reply left clr" style = "margin:10px 0 0 ${indent}px; width: ${width}px;">
                ${userSays(comment, author)}
                ${commentContent(comment, counter)}
                ${commentMetaData(comment, counter, commentType)}
            </div>
        % endif
    </li>
</%def>
