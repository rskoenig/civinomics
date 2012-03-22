<%!
    from pylowiki.lib.fuzzyTime import timeSince
    #from pylowiki.model import getRatingForComment
    import logging
    log = logging.getLogger(__name__)
%>

## The header for the comment - has user's name, avatar
<%def name="userSays(comment)">
	<span><img src="/images/avatars/${comment.user.pictureHash}.thumbnail" /> <a href = "/account/${comment.user.name}">${comment.user.name}</a> says: </span>
</%def>

## Assumes the user is already authenticated for comment editing
## Passes info to the comment controller, edit function, with the comment id as the only argument
<%def name="editComment(comment, counter)">
    <% thisID = comment.id + counter %>
    ${ h.form( url( controller = "comment", action ="edit", id = comment.id ), method="put" ) }
        <table style="width: 100%; padding: 0px; border-spacing: 0px; border: 0px; margin: 0px;"><tr><td>
        <div id = "section${thisID}" ondblclick="toggle('textareadiv${thisID}', 'edit${thisID}')">${comment.data}</div>
        </td></tr></table>
        <div style="display:none; text-align:center;" id="textareadiv${thisID}">
            <br />
            <textarea rows="4" id="textarea${thisID}" name="textarea${thisID}" onkeyup="previewAjax( 'textarea${thisID}', 'section${thisID}' )" class="markitup">${comment.data}</textarea>
            <div style="align:right;text-align:right;">
                Optional remark: <input type="text" id="remark${thisID}"  name="remark${thisID}" class="text tiny" placeholder="optional remark"/> 
            
                ${h.submit('submit', 'Save')}
                <input type="text" id="sremark"  name="sremark" class="text" />
                <input type="hidden" name = "discussionID" value = "${c.i.mainDiscussion}" />
            </div>
        </div>
        <div style="align:left;text-align:left;"><a href="javascript: toggle('textareadiv${thisID}', 'edit${thisID}', 'edit')" id="edit${thisID}" style="font-size: 12px;">edit</a></div>
    ${h.end_form()}
</%def>

## Displays the content of the comment
<%def name="commentContent(comment, counter)">
    <br />
        
        % if c.authuser.accessLevel >= 200:
            ${editComment(comment, counter)}
        % else:
            ${h.literal(h.reST2HTML(comment.data))}
        % endif
        
</%def>

## Sets up the rating system
<%def name="displayRating(comment, counter, commentType)">
    ## data: "<average>_<commentID>_<userRating>"
    <%
        userRating = getRatingForComment(comment.id, c.authuser.id)
        if userRating == False:
            userRating = 0
        else:
            userRating = userRating.rating
        if comment.avgRating == None:
            avgRating = 0
        else:
            avgRating = comment.avgRating
    %>
    <div class="basic_${counter + comment.id}" data="${avgRating}_${comment.id}_${userRating}"></div> 
    <script type="text/javascript">
    $(document).ready(function(){
        $(".basic_${counter + comment.id}").jRating({
            ratingType: "comment",
            type: "small"
        });
    });
    </script>
    % if comment.avgRating != None:
        <div class = "avgRating_${comment.id}">Average rating: ${avgRating}</div>
        <div class = "yourRating_${comment.id}">Your rating: ${userRating} </div>
    % endif
    <br/>
</%def>

## Displays the footer of the comment (post date, flag, reply, rate)
<%def name="commentMetaData(comment, counter, commentType)">
    <div class="gray comment_data left">
        <p class="time">Posted ${timeSince(comment.lastModified)} ago </p>
        % if "user" in session:
            <p>
                <a href="#" class="gray flag">Flag comment</a>
                <a href="#" class="gray reply">Reply</a>
            </p>
            
            </div><!-- comment_data -->
            <div class="flag content left">
                <form action="" class="left wide">
                    <span class="dark-text">Please explain why you are flagging this content:</span>
                    <br />
                    <textarea name="flag" class="content_feedback"></textarea>
                    <button type="submit" class="green">Submit</button>
                </form>
            </div><!-- flag_content -->
            <div class="reply content left">
                <form action="/comment/${c.url}">
                    <textarea name="comment-textarea" class="content_feedback"></textarea>
                    
                    <input type="hidden" id="type" name="type" value=${commentType} />
                    <input type="hidden" name="discussionID" value=${c.i.mainDiscussion.id} />
                    <input type="hidden" name="parentID" value=${comment.id} />
                    
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
 % if type == "background":
    <% 
        discussion = c.backgroundDiscussion
    %>
 % elif type == "suggestionMain":
    <%  
        discussion = c.s.mainDiscussion
        issueID = c.i.id
    %>
 % endif
 %if c.conf['allow.comments'] == 'true':

  <span class="gray"><a href="#">${discussion['numComments']} comments</a> | Last edited on ${c.lastmoddate} by ${c.lastmoduser} | <a href="#">Suggest edits</a></span>
  
  <h3>Comments</h3>
    <div id="comments" class="left">
        <form action="/comment/${c.url}" method="post">
            <input type="hidden" id="type" name="type" value=${type} />
            <input type="hidden" name="discussionID" value=${discussion.id} />
            <input type="hidden" name="parentID" value=0 />
            % if type == "suggestionMain":
                <input type="hidden" id="url" name="url" value="${c.s.url}" />
            % endif
            % if "user" in session:
            add a comment
            <br />
            
            <textarea rows="4" id="comment-textarea" name="comment-textarea" onkeyup="previewAjax( 'comment-textarea', 'comment-preview-div' )" class="markitup"></textarea>  
            <div id="comment-preview-div"></div>
            <div style="align:right;text-align:right;">${h.submit('submit', 'Comment')}</div>
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
        if curDepth >= maxDepth or tree['children'] == None or len(tree['children'].split(',')) < 1:
            return
        for child in tree.children:
            # Hack to resolve slight difference between discussion objects and comment objects
            if type(child) == type(1L):
                child = tree.children[child]
            try:
                displayComment(child, counter, commentType, curDepth)
                recurseCommentTree(child, counter, commentType, maxDepth, curDepth + 1)
            except:
                log.info('Error with comment %s, it has children %s'%(tree.id, tree.children[0].id))
    %>
</%def>

<%def name="displayComment(comment, counter, commentType, curDepth)">
    <li>
        ## This can be refactored into one set of function calls
        % if comment.parent == None:
            ${userSays(comment)}
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
                ${userSays(comment)}
                ${commentContent(comment, counter)}
                ${commentMetaData(comment, counter, commentType)}
            </div>
        % endif
    </li>
</%def>
