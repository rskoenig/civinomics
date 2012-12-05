<%!
    from pylowiki.lib.db.user import getUserByID, isAdmin
    from pylowiki.lib.db.facilitator import isFacilitator
    from pylowiki.lib.db.comment import getComment
    import logging, random
    from datetime import datetime
    log = logging.getLogger(__name__)
%>

<%namespace name="lib" file="/lib/mako_lib.mako" />
<%namespace name="lib_6" file="/lib/6_lib.mako" />

########################################################################
##
## comments() is the only function called from outside of this library.
##
########################################################################
<%def name="comments(thing, discussion, **kwargs)">
    <%
        if 'user' in session:
            addCommentToDiscussion(thing)
        displayDiscussion(thing, discussion)
    %>
</%def>


<%def name="addCommentToDiscussion(thing)">
    ########################################################################
    ##
    ## Add a comment to the root of the discussion tree
    ##
    ########################################################################
    <div class="row-fluid">
        <div class="span12">
            <form action="/addComment">
                <input type="hidden" id="type" name="type" value="${thing.objType}" />
                <input type="hidden" name="discussionCode" value="${thing['urlCode']}" />
                <input type="hidden" name="parentCode" value="0" />
                <fieldset>
                    <legend>Add comment</legend>
                    <textarea rows="4" class="span12"></textarea>
                    <span class="help-block">${commentClubRule()}</span>
                    <button type="submit" class="btn">Submit</button>
                </fieldset>
            </form>
        </div>
    </div>
</%def>

<%def name="commentClubRule()">
    ########################################################################
    ##
    ## Fun way of increasing stickiness and cultivating the right atmosphere
    ##
    ########################################################################
    <%
        rules = []
        rules.append("Rule #1 of comment club: Don't call people Hitler.")
        rules.append("Rule #2 of comment club: Do you talk to your mother with that voice?")
        rules.append("Rule #3 of comment club: You do not talk about comment club.")
        rules.append("Rule #4 of comment club: Gold Five: Stay on <del>target</del> topic!")
        ruleNum = random.randint(0, len(rules) - 1)
    %>
    ${rules[ruleNum] | n}
</%def>

<%def name="sortComments(commentList)">
    <% return commentList %>
</%def>

<%def name="displayDiscussion(thing, discussion)">
    <%
        maxDepth = 8
        curDepth = 0
        if 'children' in discussion.keys():
            recurseCommentTree(discussion, thing.objType, maxDepth, curDepth)
    %>
</%def>

<%def name="recurseCommentTree(node, commentType, maxDepth, curDepth)">
    <%
        if not node: # if node == 0
            return
        if type(node) == int:
            node = getComment(node)
        if curDepth >= maxDepth or node['children'] == 0:
            return

        if commentType == 'thread':
            if curDepth == 0:
                childList = [int(node.id)]
            else:
                childList = map(int, node['children'].split(','))
        else:
            childList = map(int, node['children'].split(','))

        childList = sortComments(childList)

        for child in childList:
            # Hack to resolve slight difference between discussion objects and comment objects
            if type(child) == type(1L):
                child = node.children[child]
            if child == 0:
                pass
            try:
                displayComment(child, commentType, maxDepth, curDepth)
            except:
                raise
    %>
</%def>

<%def name="displayComment(comment, commentType, maxDepth, curDepth)">
    <%
        comment = getComment(comment)
        if comment:
            author = getUserByID(comment.owner)
        else:
            return
        accordionID = 'accordion-%s' % comment['urlCode']
        collapseID = 'collapse-%s' % comment['urlCode']
        
        if curDepth % 2 == 1:
            backgroundShade = ' oddComment'
        else:
            backgroundShade = ' evenComment'
        
    %>
    <div class="accordion" id="${accordionID}">
        <div class="accordion-group ${backgroundShade}">
            ${commentHeading(comment, author, accordionID, collapseID)}
            ${commentContent(comment, commentType, curDepth, author, accordionID, collapseID)}
        </div>
    </div>
</%def>

<%def name="commentHeading(comment, author, accordionID, collapseID)">
    <div class="accordion-heading">
        <button class="accordion-toggle inline btn btn-mini" data-toggle="collapse" data-parent="#${accordionID}" href="#${collapseID}">
            Hide
        </button>
        ${lib_6.userImage(author, className="inline avatar small-avatar comment-avatar", linkClass="inline")}
        ${lib_6.userLink(author, className="inline")}
        from ${lib_6.userGeoLink(author)}
    </div> <!--/.accordion-heading-->
</%def>

<%def name="commentContent(comment, commentType, curDepth, author, accordionID, collapseID)">
    <%
        thisClass = 'accordion-body collapse'
        if comment['disabled'] == '0' and comment['deleted'] == '0':
            thisClass += ' in'
    %>
    <div id="${collapseID}" class="${thisClass}">
        <div class="accordion-inner">
            <div class="row-fluid">
                <div class="span1">
                    ${lib_6.upDownVote(comment)}
                </div> <!--/.span1-->
                <div class="span11">
                    ${comment['data']}
                </div> <!--/.span11-->
            </div> <!--/.row-fluid-->
            <%
                if 'user' in session:
                    commentFooter(comment, author)
            %>
            ${recurseCommentTree(comment, commentType, maxDepth, curDepth + 1)}
        </div><!--/.accordion-inner-->
    </div><!--/.accordion-body.collapse-->
</%def>

<%def name="commentFooter(comment, author)">
    ########################################################################
    ##
    ## Displays the {reply, flag, edit, admin} buttons
    ## 
    ## comment          ->  The comment Thing
    ## author           ->  The owner of the comment (a user Thing)
    ##
    ########################################################################
    <%
        replyID = 'reply-%s' % comment['urlCode']
        flagID = 'flag-%s' % comment['urlCode']
        editID = 'edit-%s' % comment['urlCode']
        adminID = 'admin-%s' % comment['urlCode']
    %>
    <div class="row-fluid">
        <div class="span11 offset1">
            <div class="btn-group">
                <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${replyID}">reply</a>
                <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${flagID}">flag</a>
                <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${editID}">edit</a>>
                % if int(c.authuser['accessLevel']) >= 200:
                    <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${adminID}">admin</a>
                % endif
            </div>
        </div><!--/.span11.offset1-->
    </div><!--/.row-fluid-->
    
    ## Reply
    <div class="row-fluid collapse" id="${replyID}">
        <div class="span11 offset1">
            <form action="/addComment" method="post">
                <label>reply</label>
                <textarea name="comment-textarea" class="comment-reply span12"></textarea>
                <input type="hidden" name="parentCode" value="${comment['urlCode']}" />
                <button type="submit" class="btn" name = "submit" value = "reply">Submit</button>
            </form>
        </div>
    </div>
    
    ## Flag
    <div class="row-fluid collapse" id="${flagID}">
        <div class="span11 offset1 alert">
            <strong>Are you sure you want to flag this comment?</strong>
            <br />
            <a href="/flagComment/${comment['urlCode']}" class="btn btn-danger flagCommentButton">Yes</a>
            <a class="btn accordion-toggle" data-toggle="collapse" data-target="#${flagID}">No</a>
            <span id = 'flagged_${comment['urlCode']}'></span>
        </div>
    </div>
    
    ## Edit
    <div class="row-fluid collapse" id="${editID}">
        <div class="span11 offset1">
            <form action="/comment/edit/${comment['urlCode']}" method="post" class="form form-horizontal">
                <label>edit</label>
                <textarea class="comment-reply span12" name="textarea${comment['urlCode']}">${comment['data']}</textarea>
                <button type="submit" class="btn" name = "submit" value = "reply">Submit</button>
            </form>
        </div>
    </div>
    
    ## Admin
    % if int(c.authuser['accessLevel']) >= 200:
        <div class="row-fluid collapse" id="${adminID}">
            <div class="span11 offset1">
                Admin here.
            </div>
        </div>
    % endif
</%def>
