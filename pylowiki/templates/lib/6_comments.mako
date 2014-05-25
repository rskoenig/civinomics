<%!
    from pylowiki.lib.db.user import getUserByID, isAdmin
    import pylowiki.lib.db.user         as userLib
    import pylowiki.lib.db.revision     as revisionLib
    from pylowiki.lib.db.facilitator import isFacilitator
    from pylowiki.lib.db.comment import getComment
    from pylowiki.lib.fuzzyTime import timeSince
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
        #if 'user' in session and discussion.objType != 'comment' and not c.privs['provisional']:
        #    if thing['disabled'] != '1':
        addCommentToDiscussion(thing, discussion)
        #elif 'user' not in session and discussion.objType != 'comment':
        #        loginToAddComment(thing)
        #elif c.privs['provisional']:
        #        activateToAddComment(thing)
        displayDiscussion(thing, discussion)
    %>
</%def>

<%def name="loginToAddComment(thing)">
    ########################################################################
    ##
    ## Display a button to login to add a comment
    ##
    ########################################################################

    <div class="row">
        <div class="col-sm-1">
            <img src="/images/hamilton.png" class="avatar med-avatar">
        </div>
        <div class="col-sm-11">
            <a href="#signupLoginModal" data-toggle='modal'><textarea rows="2" class="col-sm-12 form-control" name="comment-textarea" placeholder="Add a comment..."></textarea></a>
        </div>
        <div class="col-sm-11 col-sm-offset-1">
            <span class="help-block pull-right right-space">Please keep comments civil and on-topic.
            <a href="#signupLoginModal" data-toggle='modal' title="Login to comment." class="btn btn-primary" type="button">Submit</a>
        </div>
    </div>


</%def>

<%def name="activateToAddComment(thing)">
    ########################################################################
    ##
    ## Display a button to activate account to add a comment
    ##
    ########################################################################

    <div class="row">
        <div class="col-sm-1">
            ${lib_6.userImage(c.authuser, className="avatar med-avatar", linkClass="topbar-avatar-link")}
        </div>
        <div class="col-sm-11">
            <a href="#activateAccountModal" data-toggle='modal'><textarea rows="2" class="col-sm-11 form-control" name="comment-textarea" placeholder="Add a comment..."></textarea></a>
        </div>
        <div class="col-sm-11 col-sm-offset-1">
            <span class="help-block pull-right right-space">Please keep comments civil and on-topic.
            <a href="${url}" title="Login to comment." class="btn btn-primary" type="button">Submit</a>
        </div>
    </div>


</%def>

<%def name="addCommentToDiscussion(thing, discussion)">
    ########################################################################
    ##
    ## Add a comment to the root of the discussion tree
    ##
    ########################################################################
    <div class="spacer"></div>
    <form action="/comment/add/handler" id="commentAddHandler_root">
        <input type="hidden" id="type" name="type" value="${thing.objType}" />
        <input type="hidden" name="discussionCode" value="${discussion['urlCode']}" />
        <input type="hidden" name="parentCode" value="0" />
        <input type="hidden" name="thingCode" value = "${c.thing['urlCode']}" />
        <div class="row">
            <div class="col-sm-1">
                ${lib_6.userImage(c.authuser, className="avatar med-avatar", linkClass="topbar-avatar-link")}
            </div>
            <div class="col-sm-11">
                <textarea rows="2" class="col-sm-12 form-control" name="comment-textarea" placeholder="Add a comment..."></textarea>
            </div>
        </div><!-- row -->
        % if thing.objType == 'idea' or thing.objType == 'initiative':
            <% log.info("thing type is %s"%thing.objType) %>
            <div class="row top-space">
                <div class="col-sm-1">
                </div>
                <div class="col-sm-11">
                    <small>
                        <span class="radio inline right-space">
                            <input type=radio name="commentRole" value="yes"> Pro
                        </span>
                        <span class="radio inline right-space">
                            <input type=radio name="commentRole" value="neutral" checked> Neutral
                        </span>
                        <span class="radio inline right-space">
                            <input type=radio name="commentRole" value="no"> Con
                        </span>
                    </small>
                    <button type="submit" class="btn btn-primary pull-right" name = "submit" value = "reply">Submit</button></span>
                </div><!- col-sm-11 -->
            </div><!-- row -->
        % else:
        <div class="row">
            <span class="help-block pull-right right-space">Please keep comments civil and on-topic.
            <button type="submit" class="btn btn-primary" name = "submit" value = "reply">Submit</button></span>
        </div><!-- row -->
        % endif
    </form>
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
        panelID = 'panel-%s' % comment['urlCode']
        collapseID = 'collapse-%s' % comment['urlCode']
        
        if curDepth % 2 == 1:
            backgroundShade = ' oddComment'
        else:
            backgroundShade = ' evenComment'
        
    %>
    <div class="panel panel-default" id="${panelID}">
        <div class="${backgroundShade}">
            ${commentHeading(comment, author, panelID, collapseID, parent)}
            ${commentContent(comment, commentType, curDepth, maxDepth, author, panelID, collapseID)}
        </div>
    </div>
</%def>

<%def name="commentHeading(comment, author, panelID, collapseID, parent)">
    <%
        headerClass = "panel-heading"
        if comment['addedAs'] == 'admin':
            headerClass += " admin"
        elif comment['addedAs'] == 'facilitator':
            headerClass += " facilitator"
        elif comment['addedAs'] == 'listener':
            headerClass += " listener"

        roleClass = ''
        roleLabel = ''

        try:
            if comment['commentRole']:
                roleClass = 'commentRole '
                roleLabel = ''
                if comment['commentRole'] == 'no':
                    roleClass += "red"
                    roleLabel += 'Con'
                    headerClass += " against"

                elif comment['commentRole'] == 'yes':
                    roleClass += "green"
                    roleLabel += "Pro"
                    headerClass += " favor"

                else:
                    roleClass +="grey"
                    roleLabel = "Neutral"
                    headerClass += " neutral"
        except:
            roleClass = ''
            roleLabel = ''

    %>
    <div class="${headerClass}" style="border-bottom: 1px solid #ddd">
        <!--<button class="panel-toggle inline btn btn-mini" data-toggle="collapse" data-parent="#${panelID}" href="#${collapseID}">
            Hide
        </button> -->
        <%
            lib_6.userImage(author, className="inline avatar small-avatar comment-avatar no-bottom no-top", linkClass="inline")
            lib_6.userLink(author, className="inline")
            role = ''
            roles = ['admin', 'facilitator', 'listener']
            if comment['addedAs'] in roles:
                role = '(%s)' % comment['addedAs']
        %>
        ${role} from ${lib_6.userGeoLink(author, comment=True)}
        <small class="grey">
            <% date = timeSince(comment.date) %>
            ${date} ago
        </small>
        
        % if roleClass != '':
            <span class="pull-right ${roleClass}">${roleLabel}</span>
        % endif
        <span class="pull-right disabledComment-notice">
            <small>
            % if parent:
                % if parent.objType == 'comment':
                    % if parent['urlCode'] != comment['urlCode']:
                        <% 
                            if c.w:
                                dparent = c.w
                            elif c.user:
                                dparent = c.user
                            elif c.initiative:
                                dparent = c.initiative
                        %>
                        <a ${lib_6.thingLinkRouter(comment, dparent, embed=True, commentCode=parent['urlCode']) | n}>Parent</a>
                    % endif
                % endif
            % endif
            % if comment['disabled'] == '1':
                (comment disabled)
            % endif
            </small>
        </span>
    </div> <!--/.panel-heading-->
</%def>

<%def name="commentContent(comment, commentType, curDepth, maxDepth, author, panelID, collapseID)">
    <%
        thisClass = 'panel-collapse collapse'
        if comment['disabled'] == '0' and comment['deleted'] == '0':
            thisClass += ' in'
    %>
    <div id="${collapseID}" class="${thisClass}">
        <div class="panel-body">
            <div class="row">
                <div class="col-sm-1">
                    <%
                        if c.thing['disabled'] == '0':
                            lib_6.upDownVote(comment)
                    %>
                </div> <!--/.col-sm-1-->
                <div class="col-sm-11 comment-data">
                    ${misaka.html(comment['data'], extensions=misaka.EXT_AUTOLINK, render_flags = misaka.HTML_SKIP_IMAGES) | n}
                    % if curDepth + 1 == maxDepth and comment['children'] != '0':
                        ${continueThread(comment)}
                    % endif
                </div> <!--/.col-sm-11-->
            </div> <!--/.row-->
            <%
                if c.thing['disabled'] == '0':
                    commentFooter(comment, author)
            %>
            ${recurseCommentTree(comment, commentType, maxDepth, curDepth + 1)}
        </div><!--/.panel-inner-->
    </div><!--/.panel-body.collapse-->
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
    <div class="row">
        <div class="col-sm-11 col-sm-offset-1">
            <div class="btn-group">
                % if 'user' in session and not c.privs['provisional']:
                    <a class="btn btn-default btn-xs panel-toggle" data-toggle="collapse" data-target="#${replyID}">reply</a>
                    <a class="btn btn-default btn-xs panel-toggle" data-toggle="collapse" data-target="#${flagID}">flag</a>
                    % if c.privs['facilitator'] or c.privs['admin'] or c.authuser.id == comment.owner:
                        <a class="btn btn-default btn-xs panel-toggle" data-toggle="collapse" data-target="#${editID}">edit</a>
                    % endif
                    % if c.privs['facilitator'] or c.privs['admin']:
                        <a class="btn btn-default btn-xs panel-toggle" data-toggle="collapse" data-target="#${adminID}">admin</a>
                    % endif
                % elif not c.privs['provisional']:
                    <a class="btn btn-default btn-xs panel-toggle" data-toggle="modal" data-target="#signupLoginModal">reply</a>
                    <a class="btn btn-default btn-xs panel-toggle" data-toggle="modal" data-target="#signupLoginModal">flag</a>
                % endif
            </div>
            <%
                revisions = revisionLib.getRevisionsForThing(comment)
                lib_6.revisionHistory(revisions, comment)
            %>
        </div><!--/.col-sm-11.offset1-->
    </div><!--/.row-->
    
    ## Reply
    <div class="row collapse" id="${replyID}">
        <div class="col-sm-11 col-sm-offset-1">
            <form action="/comment/add/handler" method="post" id="commentAddHandler_reply">
                <textarea name="comment-textarea" class="comment-reply col-sm-12 form-control" placeholder="Add a reply..."></textarea>
                <input type="hidden" name="parentCode" value="${comment['urlCode']}" />
                <input type="hidden" name="thingCode" value = "${c.thing['urlCode']}" />
                <button type="submit" class="btn btn-primary left-space" name = "submit" value = "reply">Submit</button>
            </form>
        </div>
    </div>
    
    ## Flag
    ${lib_6.flagThing(comment)}
    
    % if 'user' in session:
        ## Edit
        % if c.privs['admin'] or c.authuser.id == comment.owner or c.privs['facilitator']:
            ${lib_6.editThing(comment)}
        % endif
    
        ## Admin
        % if c.privs['facilitator'] or c.privs['admin']:
            ${lib_6.adminThing(comment)}
        % endif
    % endif
</%def>


<%def name="continueThread(comment)">
    <br />
    <%
        if c.w:
            dparent = c.w
        elif c.user:
            dparent = c.user

        continueStr = '<a %s>%s</a>' %(lib_6.thingLinkRouter(comment, dparent, embed=True, commentCode=comment['urlCode']), "Continue this thread -->")
    %>
    ${continueStr | n}
</%def>