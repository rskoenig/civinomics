<%!
    from pylowiki.lib.fuzzyTime import timeSince
    from pylowiki.lib.db.user import getUserByID
%>

<%def name="addTopic()">
    <span class="pull-right topic"><a href="/workshop/${c.w['urlCode']}/${c.w['url']}/addDiscussion" title="Add a topic"><i class="icon-plus"></i></a></span>
</%def>

<%def name="displayDiscussionRating(discussion)">
    <a href="/rateDiscussion/${discussion['urlCode']}/${discussion['url']}/1" class="upVote voted">
        <i class="icon-chevron-up"></i>
    </a>
    <% rating = int(discussion['ups']) - int(discussion['downs']) %>
    <div>${rating}</div>
    <a href="/rateDiscussion/${discussion['urlCode']}/${discussion['url']}/-1" class="downVote voted">
        <i class="icon-chevron-down"></i>
    </a>
</%def>

<%def name="userphoto(discussion)">
    <% owner = getUserByID(discussion.owner) %>
    % if owner['pictureHash'] == 'flash':
        <a href="/profile/${owner['urlCode']}/${owner['url']}"><img src="/images/avatars/flash.profile" width="35" ></a>
    % else:
        <a href="/profile/${owner['urlCode']}/${owner['url']}">
            <img src="/images/avatar/${owner['directoryNumber']}/profile/${owner['pictureHash']}.profile" width="35">
        </a>
    % endif
</%def>

<%def name="displayDiscussionTitle(discussion)">
    <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/discussion/${discussion['urlCode']}/${discussion['url']}">${discussion['title']}</a></p>    
</%def>

<%def name="discussionMetaData(discussion)">
    <% owner = getUserByID(discussion.owner) %>
    <p>Posted <span class="recent">${timeSince(discussion.date)}</span> ago by <a href="/profile/${owner['urlCode']}/${owner['url']}">${owner['name']}</a></p>
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
                                ${discussionComments(discussion)}
                        </div>     
                    </div> <!-- /.row-fluid -->
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