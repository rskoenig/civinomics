<%!
    from pylowiki.lib.db.user import getUserByID, isAdmin
    import pylowiki.lib.db.user         as userLib
    import pylowiki.lib.db.revision     as revisionLib
    from pylowiki.lib.db.facilitator import isFacilitator
    from pylowiki.lib.db.comment import getComment
    import logging, random
    from datetime import datetime
    import misaka as misaka
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
        if 'user' in session and discussion.objType != 'comment':
            if thing['disabled'] != '1':
                addCommentToDiscussion(thing, discussion)
        elif 'user' not in session and discussion.objType != 'comment':
                loginToAddComment(thing)
        displayDiscussion(thing, discussion)
    %>
</%def>

<%def name="loginToAddComment(thing)">
    ########################################################################
    ##
    ## Display a button to login to add a comment
    ##
    ########################################################################
    <% url = '/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/clogin/' + thing.objType + '/' + thing['urlCode'] + '/' + thing['url'] %>
    <div class="row-fluid">
        <div class="span12">
            <a href="${url}" title="Login to comment." class="pull-right btn btn-success" type="button">Login to Comment</a>
            <br /><br />
        </div><!- span12 -->
    </div><!-- row-fluid -->
</%def>

<%def name="addCommentToDiscussion(thing, discussion)">
    ########################################################################
    ##
    ## Add a comment to the root of the discussion tree
    ##
    ########################################################################
    <div class="row-fluid">
        <div class="span12">
            <form action="/comment/add/handler" id="commentAddHandler_root">
                <input type="hidden" id="type" name="type" value="${thing.objType}" />
                <input type="hidden" name="discussionCode" value="${discussion['urlCode']}" />
                <input type="hidden" name="parentCode" value="0" />
                <input type="hidden" name="thingCode" value = "${c.thing['urlCode']}" />
                <fieldset>
                    <legend>Add comment</legend>
                    <textarea rows="4" class="span12" name="comment-textarea"></textarea>
                    <span class="help-block">${commentClubRule()}</span>
                    <button type="submit" class="btn" name = "submit" value = "reply">Submit</button>
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
        rules.append("Rule #2 of comment club: Do you talk to your mother with that voice?")
        rules.append("Rule #3 of comment club: You do not talk about comment club.")
        rules.append("Rule #4 of comment club: Gold Five: Stay on <del>target</del> topic!")
        ruleNum = random.randint(0, len(rules) - 1)
    %>
    ${rules[ruleNum] | n}
</%def>

<%def name="sortComments(commentIDs)">
    <%
        commentList = [getComment(commentID) for commentID in commentIDs]
        return sorted(commentList, cmp = commentComparison)
    %>
</%def>

<%def name="commentComparison(com1, com2)">
    <%
        rating1 = int(com1['ups']) - int(com1['downs'])
        rating2 = int(com2['ups']) - int(com2['downs'])
        return rating2 - rating1
    %>
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
        if not node:
            return
        if type(node) == int:
            node = getComment(node)
        if curDepth >= maxDepth or node['children'] == 0:
            return
        parent = node
        if node.objType == 'comment':
            if curDepth == 0:
                if node.objType == 'discussion':
                    parent = node
                else:
                    parent = getComment(node['parent'])
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
                displayComment(child, commentType, maxDepth, curDepth, parent)
            except:
                raise
    %>
</%def>

<%def name="displayComment(comment, commentType, maxDepth, curDepth, parent = None)">
    <%
        if comment:
            author = getUserByID(comment.owner)
            if comment['deleted'] == u'1':
                if 'user' in session:
                    if not isAdmin(c.authuser.id):
                        return
                else:
                    return
            if c.demo:
                if 'user' in session:
                    if ((author['accessLevel'] != '300' and not isFacilitator(author, c.w)) and author.id != c.authuser.id):
                        return
                else:
                    if author['accessLevel'] != '300' and not isFacilitator(author, c.w):
                        return
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
            ${commentHeading(comment, author, accordionID, collapseID, parent)}
            ${commentContent(comment, commentType, curDepth, maxDepth, author, accordionID, collapseID)}
        </div>
    </div>
</%def>

<%def name="commentHeading(comment, author, accordionID, collapseID, parent)">
    <%
        headerClass = "accordion-heading"
        if comment['addedAs'] == 'admin':
            headerClass += " admin"
        elif comment['addedAs'] == 'facilitator':
            headerClass += " facilitator"
        elif comment['addedAs'] == 'listener':
            headerClass += " listener"
    %>
    <div class="${headerClass}">
        <button class="accordion-toggle inline btn btn-mini" data-toggle="collapse" data-parent="#${accordionID}" href="#${collapseID}">
            Hide
        </button>
        <%
            lib_6.userImage(author, className="inline avatar small-avatar comment-avatar", linkClass="inline")
            lib_6.userLink(author, className="inline")
            role = ''
            roles = ['admin', 'facilitator', 'listener']
            if comment['addedAs'] in roles:
                role = '(%s)' % comment['addedAs']
        %>
        ${role} from ${lib_6.userGeoLink(author, comment=True)}
        
        <span class="pull-right disabledComment-notice">
            <small>
            <a ${lib_6.thingLinkRouter(comment, c.w, embed=True, commentCode=comment['urlCode']) | n} class="green green-hover">Link</a>
            % if parent:
                % if parent.objType == 'comment':
                    % if parent['urlCode'] != comment['urlCode']:
                        | <a ${lib_6.thingLinkRouter(comment, c.w, embed=True, commentCode=parent['urlCode']) | n} class="green green-hover">Parent</a>
                    % endif
                % endif
            % endif
            % if comment['disabled'] == '1':
                (comment disabled)
            % endif
            </small>
        </span>
    </div> <!--/.accordion-heading-->
</%def>

<%def name="commentContent(comment, commentType, curDepth, maxDepth, author, accordionID, collapseID)">
    <%
        thisClass = 'accordion-body collapse'
        if comment['disabled'] == '0' and comment['deleted'] == '0':
            thisClass += ' in'
    %>
    <div id="${collapseID}" class="${thisClass}">
        <div class="accordion-inner">
            <div class="row-fluid">
                <div class="span1">
                    <%
                        if c.thing['disabled'] == '0':
                            lib_6.upDownVote(comment)
                    %>
                </div> <!--/.span1-->
                <div class="span11 comment-data">
                    ##${comment['data']}
                    ${misaka.html(comment['data']) | n}
                    % if curDepth + 1 == maxDepth and comment['children'] != '0':
                        ${continueThread(comment)}
                    % endif
                </div> <!--/.span11-->
            </div> <!--/.row-fluid-->
            <%
                revisions = revisionLib.getRevisionsForThing(comment)
                lib_6.revisionHistory(revisions, comment)
                if 'user' in session:
                    if c.thing['disabled'] == '0':
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
                % if c.privs['facilitator'] or c.privs['admin'] or c.authuser.id == comment.owner:
                    <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${editID}">edit</a>>
                % endif
                % if c.privs['facilitator'] or c.privs['admin']:
                    <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${adminID}">admin</a>
                % endif
            </div>
        </div><!--/.span11.offset1-->
    </div><!--/.row-fluid-->
    
    ## Reply
    <div class="row-fluid collapse" id="${replyID}">
        <div class="span11 offset1">
            <form action="/comment/add/handler" method="post" id="commentAddHandler_reply">
                <label>reply</label>
                <textarea name="comment-textarea" class="comment-reply span12"></textarea>
                <input type="hidden" name="parentCode" value="${comment['urlCode']}" />
                <input type="hidden" name="thingCode" value = "${c.thing['urlCode']}" />
                <button type="submit" class="btn" name = "submit" value = "reply">Submit</button>
            </form>
        </div>
    </div>
    
    ## Flag
    ${lib_6.flagThing(comment)}
    
    ## Edit
    % if c.privs['admin'] or c.authuser.id == comment.owner or c.privs['facilitator']:
        ${lib_6.editThing(comment)}
    % endif
    
    ## Admin
    % if c.privs['facilitator'] or c.privs['admin']:
        ${lib_6.adminThing(comment)}
    % endif
</%def>


<%def name="continueThread(comment)">
    <br />
    <%
        continueStr = '<a %s>%s</a>' %(lib_6.thingLinkRouter(comment, c.w, embed=True, commentCode=comment['urlCode']), "Continue this thread -->")
    %>
    ${continueStr | n}
</%def>