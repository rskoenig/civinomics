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
    ######################
    ##
    ## Add a comment to the root of the discussion tree
    ##
    ######################
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
    ######################
    ##
    ## Fun way of increasing stickiness and cultivating the right atmosphere
    ##
    ######################
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

<%def name="commentHeader(comment)">
    ## TODO
</%def>

<%def name="sortComments(commentList)">
    <% return commentList %>
</%def>

<%def name="displayDiscussion(thing, discussion)">
    <%
        maxDepth = 4
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
    %>
    <div class="accordion" id="${accordionID}">
        ${commentHeading(comment, author, accordionID, collapseID)}
        ${commentContent(comment, author, accordionID, collapseID)}
    </div>
</%def>

<%def name="commentHeading(comment, author, accordionID, collapseID)">
    <div class="accordion-heading">
        <button class="accordion-toggle inline" data-toggle="collapse" data-parent="#${accordionID}" href="#${collapseID}">
            Hide
        </button>
        ${lib_6.userImage(author, className="inline avatar small-avatar comment-avatar", linkClass="inline")}
        ${lib_6.userLink(author, className="inline")}
        from ${lib_6.userGeoLink(author)}
    </div> <!--/.accordion-heading-->
</%def>

<%def name="commentContent(comment, author, accordionID, collapseID)">
    <%
        thisClass = 'accordion-body collapse'
        if comment['disabled'] == '0' and comment['deleted'] == '0':
            thisClass += ' in'
    %>
    <div id="${collapseID}" class="${thisClass}">
        <div class="accordion-inner">
            ${comment['data']}
        </div>
    </div>
</%def>