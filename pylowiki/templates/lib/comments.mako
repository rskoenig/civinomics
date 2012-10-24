<%!
    from pylowiki.lib.fuzzyTime import timeSince
    from pylowiki.lib.db.user import getUserByID, isAdmin
    from pylowiki.lib.db.facilitator import isFacilitator
    from pylowiki.lib.db.comment import getComment
    from pylowiki.lib.db.event import getParentEvents
    from pylowiki.lib.db.revision import get_revision
    import logging
    from datetime import datetime
    log = logging.getLogger(__name__)
%>

<%namespace name="lib" file="/lib/mako_lib.mako" />

## The header for the comment - has user's name, avatar
<%def name="userSays(comment, author)">
    <%
        points = "point"
        replies = "repl"
        if int(author['totalPoints']) != 1:
            points += "s"
        numReplies = len([child for child in comment['children'].split(',') if int(child) != 0])
        if numReplies == 1:
            replies += "y"
        else:
            replies += "ies"
        c.author = author
    %>
    <p>
    <div class="row-fluid">
        <div class="span2"> 
        <button class="btn btn-mini" id="hide${comment['urlCode']}" title="Hide comment and any replies" alt="Hide comment and any replies"><i class="icon-minus"></i> hide</button>
        </div><!-- span2 -->
        <div class="span1">
        % if author['pictureHash'] == 'flash':
            <a href="/profile/${c.author['urlCode']}/${c.author['url']}"><img src="/images/avatars/flash.profile" alt="${c.author['name']}" title="${c.author['name']}" class="thumbnail" width="20" /></a>
        % else:
            <a href="/profile/${c.author['urlCode']}/${c.author['url']}"><img src="/images/avatar/${c.author['directoryNumber']}/thumbnail/${c.author['pictureHash']}.thumbnail" class="thumbnail" alt="${c.author['name']}" title="${c.author['name']}" class="thumbnail" /></a>
        % endif
        </div><!-- span1 -->
        <div class="span8 pull-left">
        <a href = "/profile/${author['urlCode']}/${author['url']}">${author['name']}</a> &mdash;
        <span class="recent">${timeSince(datetime.strptime(comment['lastModified'], '%a %b %d %H:%M:%S %Y'))}</span> ago &mdash; ${numReplies} ${replies}
        </div><!-- span8 -->
    </div><!-- row-fluid -->
    </p>
</%def>

## Assumes the user is already authenticated for comment editing
## Passes info to the comment controller, edit function, with the comment id as the only argument
<%def name="editComment(comment, counter)">
    <% thisID = comment['urlCode'] %>
    <form action="/comment/edit/${comment['urlCode']}" method="post" class="form form-horizontal"><div style="display:none"><input name="_method" type="hidden" value="put" /></div>
        <table><tr><td>
        <div id = "section${thisID}" ondblclick="toggle('textareadiv${thisID}', 'edit${thisID}')" style="color:black;">${h.literal(h.reST2HTML(comment['data']))}</div>
        </td></tr></table>
        <div class="collapse" id="textareadiv${thisID}">
            <br />
            <textarea rows="4" id="textarea${thisID}" name="textarea${thisID}" onkeyup="previewAjax( 'textarea${thisID}', 'section${thisID}' )" class="markitup">${comment['data']}</textarea>
            <div class="control-group">
                <input type="hidden" id="sremark"  name="sremark" class="text" />
                <input type="hidden" name = "discussionID" value = "${c.discussion.id}" />
                % if '/thread/' in session['return_to']:
                    <input type="hidden" name="discType" value="thread" />
                % endif
            </div>
            <button type="submit" name="submit" value="submit" class="btn" id="remark${thisID}" name="remark${thisID}">Save changes</button>
        </div>
    </form>
</%def>

## Displayed 'deleted' to the user
<%def name="showDeleted()">
    ##<em> This comment has been deleted </em>
</%def>

## Shows the comment.  Used when called from within a python block.
<%def name="showComment(comment)">
    ${h.literal(h.reST2HTML(comment['data']))}
</%def>

## Displays the content of the comment
<%def name="commentContent(comment, counter, **kwargs)">
    <div class="collapse in hide${comment['urlCode']}" style="color:black;">
        <%
            if "user" in session:
                if 'deleted' in comment.keys():
                    if comment['deleted'] == '1':
                        showDeleted()
                    else:
                        if isAdmin(c.authuser.id) or isFacilitator(c.authuser.id, c.w.id):
                            editComment(comment, counter)
                        else:
                            showComment(comment)
                else:
                    if isAdmin(c.authuser.id) or isFacilitator(c.authuser.id, c.w.id):
                            editComment(comment, counter)
                    else:
                        showComment(comment)
                if 'comType' in kwargs:
                    if kwargs['comType'] == 'thread':
                        displayButtons(comment, counter, comType = 'thread')
                    else:
                        displayButtons(comment, counter)
                else:
                    displayButtons(comment, counter)
            else:
                if 'deleted' in comment.keys():
                    if comment['deleted'] == '1':
                        showDeleted()
                    else:
                        showComment(comment)
                else:
                    showComment(comment)
        %>
    </div>
</%def>

## Sets up the rating system
<%def name="displayRating(comment, commentType)">
    % if 'user' in session and c.isScoped and comment['deleted'] == '0' and comment['disabled'] == '0':
    <a href="/rateComment/${comment.id}/1" class="upVote">
        <i class="icon-chevron-up"></i>
    </a>    
    <div class="chevron-score">${int(comment['ups']) - int(comment['downs'])}</div>
    <a href="/rateComment/${comment.id}/-1" class="downVote">
        <i class="icon-chevron-down"></i>
    </a>
    % else:
        <div class="chevron-score">${int(comment['ups']) - int(comment['downs'])}</div>
    % endif
</%def>

<%def name="displayButtons(comment, counter, **kwargs)">
    <br>
    <% 
        if 'deleted' in comment.keys():
            if comment['deleted'] == '1':
                return
    %>
    <p class="btn-group pull-right">
        % if int(comment['parent']) != 0:
            <% 
                parent = getComment(comment['parent'])
                parentOwner = getUserByID(parent.owner)
            %>
            % if 'comType' in kwargs:
                % if kwargs['comType'] == 'thread':
                    <a class="btn btn-mini btn-primary thepopover" rel="popover" data-title="${parentOwner['name']} said:" data-content="${h.literal(h.reST2HTML(parent['data']))}" data-placement="left"><i class="icon-white icon-comment"></i> parent</a>
                % else:
                    <a class="btn btn-mini btn-primary thepopover" rel="popover" data-title="${parentOwner['name']} said:" data-content="${h.literal(h.reST2HTML(parent['data']))}"><i class="icon-white icon-comment"></i> parent</a>
                % endif
            % else:
                <a class="btn btn-mini btn-primary thepopover" rel="popover" data-title="${parentOwner['name']} said:" data-content="${h.literal(h.reST2HTML(parent['data']))}"><i class="icon-white icon-comment"></i> parent</a>
            % endif
        % endif
        <a data-toggle="collapse" data-target=".reply${comment['urlCode']}" class="btn btn-mini btn-primary" title="Reply to comment" alt="Reply to comment"><i class="icon-white icon-repeat"></i> reply</a>
        % if isAdmin(c.authuser.id) or isFacilitator(c.authuser.id, c.w.id):
            <a id="edit${comment['urlCode']}" class="btn btn-mini btn-primary  pull-right" data-toggle="collapse" title="Edit comment" data-target="#textareadiv${comment['urlCode']}">
                <i class="icon-white icon-edit"></i> edit
            </a>
            <a href="/adminComment/${comment['urlCode']}" class="btn btn-mini btn-warning pull-right" title="Admin comment">
                <i class="icon-white icon-list-alt"></i> admin
            </a>
        % endif
        <a data-toggle="collapse" data-target=".flag${comment['urlCode']}" class="btn btn-mini btn-inverse" title="Flag this comment" alt="Flag this comment"><i class="icon-white icon-flag"></i> flag</a>
    </p> <!-- /.btn-group -->
</%def>

## Displays the footer of the comment (post date, flag, reply, rate)
<%def name="commentFeedback(comment, commentType)">
    <div class="buttons collapse in hide${comment['urlCode']}">
        % if "user" in session:
        </div><!-- /.buttons -->
        ## Must be wrapped or a tiny bit will show
        <div class="collapse flag${comment['urlCode']}">
            <div class="alert">
                    <strong>Are you sure you want to flag this comment?</strong>
                    <br>
                    <a href="/flagComment/${comment.id}" class="btn btn-danger flagCommentButton">Yes</a>
                    <a class="btn" id="flag${comment['urlCode']}">No</a>
                    <span id = 'flagged_${comment['urlCode']}'></span>
            </div> <!-- /.alert -->
        </div> <!-- /.collapse.flag -->
        <div class="reply textarea collapse reply${comment['urlCode']}">
            <form action="/addComment" method="post">
                <textarea name="comment-textarea" style="width: 85%" rows="4"></textarea>
                
                <input type="hidden" id="type" name="type" value="${commentType}" />
                <input type="hidden" name="discussionID" value="${c.discussion.id}" />
                <input type="hidden" name="parentID" value="${comment['urlCode']}" />
                <input type="hidden" name="workshopCode" value="${c.w['urlCode']}" />
                <input type="hidden" name="workshopURL" value="${c.w['url']}" />
                % if commentType == 'suggestionMain':
                    <input type="hidden" name = "suggestionCode" value = "${c.s['urlCode']}" />
                    <input type="hidden" name = "suggestionURL" value = "${c.s['url']}" />
                % elif commentType == 'resource':
                    <input type="hidden" name = "resourceCode" value = "${c.resource['urlCode']}" />
                    <input type="hidden" name = "resourceURL" value = "${c.resource['url']}" />
                % endif
                <br />
                <button type="submit" class="btn" name = "submit" value = "reply">Submit</button>
            </form>
        </div> <!-- /.reply.textarea -->
    % else:
        </div> <!-- /.buttons -->
    % endif
</%def>

## Main function that gets called by the template
<%def name="comments( type, **kwargs )">
    % if type == "background" or type == "feedback" or type == "discussion":
        <% 
            discussion = c.discussion
            allowComments = '1'
        %>
    % elif type == "suggestionMain" or type == "resource":
        <%  
            discussion = c.discussion
            workshop = c.w
            allowComments = c.allowComments
        %>
    % elif type == "thread":
        <%
            maxDepth = kwargs['maxDepth']
            rootComment = kwargs['rootComment']
            c.discussion = discussion = kwargs['discussion']
            allowComments = '1'
        %>
    % endif

    % if c.conf['read_only.value'] == 'true':
        <% return %>
    % endif
    % if c.conf['allow.comments'] == 'false' or allowComments == '0':
        <% return %>
    % endif
    % if type != "thread":
        % if discussion['numComments'] == '1':
            <% commentString = 'comment' %>
        % else:
            <% commentString = 'comments' %>
        % endif
    % endif
    ${lib.fields_alert()}
    <div class="civ-col-inner">
        <div class="row-fluid">
            <div class="span12">
                <form action="/addComment" method="post">
                    <input type="hidden" id="type" name="type" value="${type}" />
                    <input type="hidden" name="discussionID" value="${discussion.id}" />
                    <input type="hidden" name="parentID" value="0" />
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
                    % elif type == "discussion":
                        <input type="hidden" id="url" name="workshopCode" value="${c.w['urlCode']}" />
                        <input type="hidden" id="url" name="workshopURL" value="${c.w['url']}" />
                    % endif
                    % if "user" in session and c.isScoped or (c.isAdmin or c.isFacilitator):
                        % if type != 'thread':
                            <textarea rows="4" placeholder="What do you think?" id="comment-textarea" name="comment-textarea" onkeyup="previewAjax( 'comment-textarea', 'comment-preview-div' )" class="markitup span6"></textarea>
                            <div id="comment-preview-div"></div>
                                <button type="submit" name = "submit" value = "submit" class="btn">Submit</button>
                            <br />
                        % endif
                    % else:
                        <!--Register to leave a comment-->
                    %endif
                </form>
            </div> <!-- /.span12 -->
        </div> <!-- /.row-fluid -->
        
        <div id="featured_comments">
            <% 
                if type != 'thread':
                    maxDepth = 4
                counter = 1000
                curDepth = 0

                if 'children' in discussion.keys():
                    if type == 'thread':
                        recurseCommentTree(rootComment, type, maxDepth, curDepth, counter)
                    else:
                        recurseCommentTree(discussion, type, maxDepth, curDepth, counter)
            %>
        </div> <!-- /#featured_comments -->
    </div> <!-- /.civ-col-inner -->
</%def>

<%def name="recurseCommentTree(node, commentType, maxDepth, curDepth, counter)">
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

        for child in childList:
            # Hack to resolve slight difference between discussion objects and comment objects
            if type(child) == type(1L):
                child = node.children[child]
            if child == 0:
                pass
            try:
                displayComment(child, commentType, maxDepth, curDepth, counter)
            except:
                raise
    %>
</%def>

<%def name="displayComment(comment, commentType, maxDepth, curDepth, counter)">
    <% 
        comment = getComment(comment)
        if comment:
            author = getUserByID(comment.owner)
        else:
            return
        reply, moderator = "comment", ""
        if int(comment['parent']) != 0:
            reply += " reply"
        if author['accessLevel'] >= 200:
            moderator += "alert alert-success"
    %>
    <div class="row-fluid ${reply}">
        <div class="span1 civ-votey">
            ${displayRating(comment, commentType)}
        </div> <!-- /.civ-votey -->
        <div class="span11">
            <div class="civ-comment ${moderator}">
                <%
                    userSays(comment, author)
                    if commentType == 'thread':
                        commentContent(comment, counter, comType = commentType)
                    else:
                        commentContent(comment, counter)
                %>
            ${commentFeedback(comment, commentType)}

            ##############################
            ## 
            ## Showing non-edit events
            ## 
            ##############################
            <% events = getParentEvents(comment) %>
            <% eventsList = [] %>
            % for e in events:
                % if not e['title'].startswith('Comment edited'):
                    <% eventsList.append(e) %>
                % endif
            % endfor
            % if len(eventsList) != 0:
                <span style="color:black;">
                    ##<strong>Event log:</strong><br />
                    <ul class="unstyled">
                        % for e in eventsList:
                            <% 
                                eventOwner = getUserByID(e.owner)
                                ownerLinkback = '<a href="/profile/%s/%s">%s</a> ' % (eventOwner['urlCode'], eventOwner['url'], eventOwner['name'])
                            %>
                            <li><strong>${e['title']}</strong> by ${ownerLinkback | n} on ${e.date} (PST): ${e['data']}</li>
                        % endfor
                    </ul>
                </span>
                <br />
            % endif

            ##############################
            ## 
            ## Showing edits
            ## 
            ##############################
            ## Get the revisions
            % if comment['deleted'] == '0':
                <% revisions = map(int, comment['revisionList'].split(','))%>
                % if len(revisions) > 1:
                    <span style="color:black;">
                        <strong>Edit log:</strong><br />
                        <ul class="unstyled">
                            % for revision in revisions:
                                <% 
                                    r = get_revision(revision) 
                                    commenter = getUserByID(r.owner)
                                %>
                                <li>
                                    <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/comment/${r['urlCode']}">${r.date} (PST)</a>
                                </li>
                            % endfor
                        </ul>
                    </span>
                % endif
            % endif

            ##############################
            ## 
            ## Depth-based pagination
            ## 
            ##############################
            ## curDepth starts counting at 0, so subtract 1 from maxDepth
            % if curDepth == maxDepth - 1:
                <% children = map(int, comment['children'].split(',')) %>
                % if children[0] != 0:
                        <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/thread/${comment['urlCode']}" style="float:right;">Continue this thread --></a>
                    <br />
                % endif
            % endif

            </div> <!-- /.civ-comment -->
            <div class="collapse in hide${comment['urlCode']}">
                ${recurseCommentTree(comment, commentType, maxDepth, curDepth + 1, counter)}
            </div>
        </div> <!-- /.span11 -->
    </div> <!-- /.row-fluid -->
</%def>

<%def name="buttonHandler(**kwargs)">
    <script type="text/javascript">
        (function() {
          var handleCollapse, strip,
            __indexOf = Array.prototype.indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

          strip = function(array) {
            var arr, element, _i, _len;
            arr = [];
            for (_i = 0, _len = array.length; _i < _len; _i++) {
              element = array[_i];
              if (__indexOf.call(arr, element) < 0) arr.push(element);
            }
            return arr;
          };

          handleCollapse = function(set, btntext1, btntext2) {
            var element, _i, _len, _results;
            _results = [];
            for (_i = 0, _len = set.length; _i < _len; _i++) {
              element = set[_i];
              _results.push($('#' + element).on('click', function() {
                var Class, Height;
                Class = "." + ($(this).attr('id'));
                Height = $(Class).height();
                if (Height === 0) {
                  $(Class).collapse('show');
                  return $(this).html(btntext1);
                } else {
                  $(Class).collapse('hide');
                  return $(this).html(btntext2);
                }
              }));
            }
            return _results;
          };

          $(function() {
            var flagClasses, hideClasses;
            flagClasses = strip($('html').html().match(/flag\d+/g));
            hideClasses = strip($('html').html().match(/hide\d+/g));
            $('.thepopover').popover();
            
            handleCollapse(flagClasses, "No", "No");
            return handleCollapse(hideClasses, "<i class='icon-minus'></i> hide", "<i class='icon-plus'></i> show");
          });

        }).call(this);
    </script>
</%def>
