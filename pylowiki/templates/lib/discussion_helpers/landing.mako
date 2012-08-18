<%!
    from pylowiki.lib.fuzzyTime import timeSince
    from pylowiki.lib.db.user import getUserByID
    from pylowiki.lib.db.flag import getFlags
    from pylowiki.lib.db.comment import getComment, getFlaggedDiscussionComments
%>

<%def name="addTopic()">
    <span class="pull-right topic"><a href="/workshop/${c.w['urlCode']}/${c.w['url']}/addDiscussion" title="Add a topic"><i class="icon-plus"></i></a></span>
</%def>


<%def name="displayDiscussionRating(discussion)">
    <% rating = int(discussion['ups']) - int(discussion['downs']) %>
    % if 'user' in session and c.isScoped:
        <a href="/rateDiscussion/${discussion['urlCode']}/${discussion['url']}/1" class="upVote voted">
        <i class="icon-chevron-up"></i>
        </a>
        <div>${rating}</div>
        <a href="/rateDiscussion/${discussion['urlCode']}/${discussion['url']}/-1" class="downVote voted">
        <i class="icon-chevron-down"></i>
        </a>
    % else:
        <div>${rating}</div>
    % endif
</%def>

<%def name="userphoto(discussion)">
    <% owner = getUserByID(discussion.owner) %>
    % if owner['pictureHash'] == 'flash':
        <a href="/profile/${owner['urlCode']}/${owner['url']}"><img src="/images/avatars/flash.profile" width="35" class="thumbnail" alt="${owner['name']}" title="${owner['name']}"></a>
    % else:
        <a href="/profile/${owner['urlCode']}/${owner['url']}">
            <img src="/images/avatar/${owner['directoryNumber']}/profile/${owner['pictureHash']}.profile" width="35" class="thumbnail" alt="${owner['name']}" title="${owner['name']}">
        </a>
    % endif
</%def>

<%def name="displayDiscussionTitle(discussion)">
    <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/discussion/${discussion['urlCode']}/${discussion['url']}">${discussion['title']}</a></p>    
</%def>

<%def name="discussionPostedDate(discussion)">
    <br />
    <p><i class="icon-time"></i> <span class="recent">${timeSince(discussion.date)}</span> ago 
    % if ('user' in session and c.isScoped) or c.isAdmin or c.isFacilitator:
        | <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/discussion/${discussion['urlCode']}/${discussion['url']}"> Leave comment</a></p>
    % endif

</%def>

<%def name="discussionMetaData(discussion)">
    <% owner = getUserByID(discussion.owner) %>
    <% fComments = getFlaggedDiscussionComments(discussion.id) %>
    <% numFlags = 0 %>
    % for commentID in fComments:
        <% comment = getComment(commentID) %>
        <% flags = getFlags(comment) %>
        % if flags:
            <% numFlags += len(flags) %>
        % endif
    % endfor
    <a href="/profile/${owner['urlCode']}/${owner['url']}">${owner['name']}</a><br>
    <span class="badge badge-info" title="Comments in discussion"><i class="icon-white icon-comment"></i> ${discussion['numComments']}</span>
    <span class="badge badge-important" title="Flagged comments in discussion"><i class="icon-white icon-flag"></i> ${numFlags}</span>
    <br />
</%def>

<%def name="discussionComments(discussion)">
    <p>
        <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/discussion/${discussion['urlCode']}/${discussion['url']}">
            ${discussion['numComments']} comments
        </a>
    </p>
</%def>

<%def name="listDiscussions()">
    % if c.discussions:
        <ul class="unstyled civ-col-list">
            % for discussion in c.discussions:
                <li>
                    <div class="row-fluid">
                        <div class="span1 civ-votey">
                            ${displayDiscussionRating(discussion)}
                        </div> <!-- /.civ-votey -->
                        <div class="span1">
                            ${userphoto(discussion)}
                        </div> <!-- /.civ-votey -->    
                        <div class="span8">        
                                <h4>${displayDiscussionTitle(discussion)}</h4>
                                ${discussionMetaData(discussion)}
                        </div><!-- span8 -->
                    </div> <!-- /.row-fluid -->
                    <div class="row-fluid">
                        <div class="span1">
                        </div>
                        <div class="span8">
                            ${discussionPostedDate(discussion)}
                        </div><!-- span9 -->
                    </div><!-- row-fluid -->
                </li>
            % endfor
        </ul>
    % else:
        <div class="alert alert-warning">No discussions to show.</div>
    % endif
</%def>

<%def name="displayMOTD()">
    Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.
</%def>
