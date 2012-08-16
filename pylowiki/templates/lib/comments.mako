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
        <button class="btn btn-mini" id="hide${comment.id}" title="Hide comment and any replies" alt="Hide comment and any replies"><i class="icon-minus"></i> hide</button>
        
        % if author['pictureHash'] == 'flash':
            <a href="/profile/${c.author['urlCode']}/${c.author['url']}"><img src="/images/avatars/flash.profile" alt="avatar" width="20" /></a>
        % else:
            <a href="/profile/${c.author['urlCode']}/${c.author['url']}"><img src="/images/avatar/${c.author['directoryNumber']}/thumbnail/${c.author['pictureHash']}.thumbnail" alt="avatar" /></a>
        % endif

        <a href = "/profile/${author['urlCode']}/${author['url']}">${author['name']}</a> &mdash;
        <span class="recent">${timeSince(datetime.strptime(comment['lastModified'], '%a %b %d %H:%M:%S %Y'))}</span> ago &mdash; ${numReplies} ${replies}
    </p>
</%def>

## Assumes the user is already authenticated for comment editing
## Passes info to the comment controller, edit function, with the comment id as the only argument
<%def name="editComment(comment, counter)">
    <% thisID = counter + comment.id %>
    ##${ h.form( url( controller = "comment", action ="edit", id = comment.id ), method="put" ) }
    <form action="/comment/edit/${comment.id}" method="post" class="form form-horizontal"><div style="display:none"><input name="_method" type="hidden" value="put" /></div>
    ## style="width: 100%; padding: 0px; border-spacing: 0px; border: 0px; margin: 0px;"
        <table><tr><td>
        <div id = "section${thisID}" ondblclick="toggle('textareadiv${thisID}', 'edit${thisID}')">${comment['data']}</div>
        </td></tr></table>
        <div class="collapse" id="textareadiv${thisID}">
            <br />
            <textarea rows="4" id="textarea${thisID}" name="textarea${thisID}" onkeyup="previewAjax( 'textarea${thisID}', 'section${thisID}' )" class="markitup">${comment['data']}</textarea>
            <div class="control-group">
                <label class="control-label" for="remark${thisID}">
                    Optional remark
                </label>

                <div class="controls">
                    <div class="input-append">
                        <input type="text" id="remark${thisID}" name="remark${thisID}" placeholder="optional remark" class="span7"/><button type="submit" name="submit" value="submit" class="btn">Submit</button>
                    </div>
                </div>
            
                ##${h.submit('submit', 'Save')}
                <input type="hidden" id="sremark"  name="sremark" class="text" />
                <input type="hidden" name = "discussionID" value = "${c.discussion.id}" />
            </div>
        </div>
        ${displayButtons(comment, counter)}
    ##${h.end_form()}
    </form>
</%def>

## Displays the content of the comment
<%def name="commentContent(comment, counter)">
    <div class="collapse in hide${comment.id}">
        % if c.authuser['accessLevel'] >= 200:
            ${editComment(comment, counter)}
        % elif "user" in session:
            ${h.literal(h.reST2HTML(comment['data']))}
            ${displayButtons(comment, counter)}
        % else:
            ${h.literal(h.reST2HTML(comment['data']))}
        % endif
    </div> <!-- /.collapse.in.hide${comment.id} -->
</%def>

## Sets up the rating system
<%def name="displayRating(comment, commentType)">
    <a href="/rateComment/${comment.id}/1" class="upVote voted">
        <i class="icon-chevron-up"></i>
    </a>    <div>${int(comment['ups']) - int(comment['downs'])}</div>
    <a href="/rateComment/${comment.id}/-1" class="downVote voted">
        <i class="icon-chevron-down"></i>
    </a>
</%def>

<%def name="displayButtons(comment, counter)">
    <br>
    <p class="btn-group pull-right">
        % if int(comment['parent']) != 0:
            <% 
                parent = getComment(comment['parent'])
                parentOwner = getUserByID(parent.owner)
            %>
            <a class="btn btn-mini thepopover" rel="popover" data-title="${parentOwner['name']} said:" data-content="${h.literal(h.reST2HTML(parent['data']))}"><i class="icon-comment"></i> parent</a>
        % endif
        <a data-toggle="collapse" data-target=".reply${comment.id}" class="btn btn-mini" title="Reply to comment" alt="Reply to comment"><i class="icon-repeat"></i> reply</a>
        <a data-toggle="collapse" data-target=".flag${comment.id}" class="btn btn-mini" title="Flag this comment" alt="Flag this comment"><i class="icon-flag"></i> flag</a>
        % if c.authuser['accessLevel'] >= 200:
            <a id="edit${counter + comment.id}" class="btn btn-mini pull-right" data-toggle="collapse" data-target="#textareadiv${counter + comment.id}">
                <i class="icon-edit"></i> edit
            </a>
        % endif
    </p> <!-- /.btn-group -->
</%def>

## Displays the footer of the comment (post date, flag, reply, rate)
<%def name="commentFeedback(comment, commentType)">
	<div class="buttons collapse in hide${comment.id}">
		% if "user" in session:
		</div><!-- /.buttons -->
		## Must be wrapped or a tiny bit will show
		<div class="collapse flag${comment.id}">
			<div class="alert">
				##<form action="/flagComment/${comment.id}" class="left wide">
					<strong>Are you sure you want to flag this comment?</strong>
					<br>
					<a href="/flagComment/${comment.id}"class="btn btn-danger flagCommentButton">Yes</a>
					<a class="btn" id="flag${comment.id}">No</a>
					<span id = 'flagged_${comment.id}'></span>
				##</form>
			</div> <!-- /.alert -->
		</div> <!-- /.collapse.flag${comment.id} -->
		<div class="reply textarea collapse reply${comment.id}">
			<form action="/addComment">
				<textarea name="comment-textarea" style="width: 85%" rows="1"></textarea>
				
				<input type="hidden" id="type" name="type" value="${commentType}" />
				<input type="hidden" name="discussionID" value="${c.discussion.id}" />
				<input type="hidden" name="parentID" value="${comment.id}" />
				<input type="hidden" name="workshopCode" value="${c.w['urlCode']}" />
				<input type="hidden" name="workshopURL" value="${c.w['url']}" />
				% if commentType == 'suggestionMain':
					<input type="hidden" name = "suggestionCode" value = "${c.s['urlCode']}" />
					<input type="hidden" name = "suggestionURL" value = "${c.s['url']}" />
				% elif commentType == 'resource':
					<input type="hidden" name = "resourceCode" value = "${c.resource['urlCode']}" />
					<input type="hidden" name = "resourceURL" value = "${c.resource['url']}" />
				% endif
				<button type="submit" class="btn" name = "submit" value = "reply">Submit</button>
			</form>
		</div> <!-- /.reply.textarea -->
	% else:
		</div> <!-- /.buttons -->
	% endif
</%def>

## Main function that gets called by the template
<%def name="comments( type )">
 % if type == "background" or type == "feedback" or type == "discussion":
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

  % if discussion['numComments'] == '1':
     <% commentString = 'comment' %>
  % else:
     <% commentString = 'comments' %>
  % endif

  ##% if type == 'resource':
    ##${discussion['numComments']} ${commentString} | Last edited <span class="recent">${timeSince(c.lastmoddate)}</span> ago by <a href = "/profile/${c.lastmoduser['urlCode']}/${c.lastmoduser['url']}">${c.lastmoduser['name']}</a>
  ##% else:
    ##${discussion['numComments']} ${commentString} | Last edited <span class="recent">${timeSince(c.lastmoddate)}</span> ago by <a href = "/profile/${c.lastmoduser['urlCode']}/${c.lastmoduser['url']}">${c.lastmoduser['name']}</a>
  ##% endif
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
                    % if "user" in session:
                    <textarea rows="1" placeholder="What do you think?" id="comment-textarea" name="comment-textarea" onkeyup="previewAjax( 'comment-textarea', 'comment-preview-div' )" class="markitup span6"></textarea>
                    <div id="comment-preview-div"></div>
                        <button type="submit" name = "submit" value = "submit" class="btn">Submit</button>
                    <br />
                    % else:
                    <h3 class="utility">
                      Please <a href="/login">login</a> or <a href="/register">register</a> to leave a comment!
                    </h3>
                    %endif
                </form>
            </div> <!-- /.span12 -->
        </div> <!-- /.row-fluid -->
        
        ##<h4>Comments</h4>
        <div id="featured_comments">
            <% 
                counter = 1000
                maxDepth = 4
                curDepth = 0
                if 'children' in discussion.keys():
                    recurseCommentTree(discussion, type, maxDepth, curDepth, counter)
            %>
        </div> <!-- /#featured_comments -->
    </div> <!-- /.civ-col-inner -->
 
 %endif

</%def>

<%def name="recurseCommentTree(node, commentType, maxDepth, curDepth, counter)">
    <%
        log.info("Node is %s" % node.id)
        if not node: # if node == 0
            return
        if type(node) == int:
            log.info('Comment %s being processed now' % node)
            node = getComment(node)
        if curDepth >= maxDepth or node['children'] == 0:
            return
        # children = map(int, node['children'].split(','))
        # for child in children:
        for child in [int(item) for item in node['children'].split(',')]:
            log.info('children: %s' % node['children'])
            # Hack to resolve slight difference between discussion objects and comment objects
            if type(child) == type(1L):
                child = node.children[child]
            if child == 0:
                pass
            try:
                displayComment(child, commentType, maxDepth, curDepth, counter)
            except:
                raise
                #log.info('Error with comment %s, it has children %s'%(tree.id, tree.children[0].id))
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
                ${userSays(comment, author)}
                ${commentContent(comment, counter)}
            </div> <!-- /.civ-comment -->
            ${commentFeedback(comment, commentType)}
            <div class="collapse in hide${comment.id}">
                ${recurseCommentTree(comment, commentType, maxDepth, curDepth + 1, counter)}
            </div> <!-- /.collapse.in.hide${comment.id} -->
        </div> <!-- /.span11 -->
    </div> <!-- /.row-fluid -->
</%def>

<%def name="buttonHandler()">
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
