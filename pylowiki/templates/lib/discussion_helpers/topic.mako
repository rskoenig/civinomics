<%!
    from pylowiki.lib.fuzzyTime import timeSince
    from pylowiki.lib.db.user import getUserByID
%>

<%def name="discTopicPageTitle()">
    <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/discussion">DISCUSSION</a> 
    IN
    <a href="/workshop/${c.w['urlCode']}/${c.w['url']}">${c.w['title']}</a>

</%def>

<%def name="displayTopicContent()">
    <div class="row-fluid">
        <div class="span1 civ-votey">
            <a href="/rateDiscussion/${c.discussion['urlCode']}/${c.discussion['url']}/1" class="upVote voted">
                <i class="icon-chevron-up"></i>
            </a>
            <% rating = int(c.discussion['ups']) - int(c.discussion['downs']) %>
            <div>${rating}</div>
            <a href="/rateDiscussion/${c.discussion['urlCode']}/${c.discussion['url']}/-1" class="downVote voted">
                <i class="icon-chevron-down"></i>
            </a>
        </div>
        <% owner = getUserByID(c.discussion.owner) %>
        <div class="span11">
            <a href="#"><h3>${c.discussion['title']}</h3></a>
            Posted <span class="recent">${timeSince(c.discussion.date)}</span> ago by <a href="/profile/${owner['urlCode']}/${owner['url']}">${getUserByID(c.discussion.owner)['name']}</a>
            <div id="topic-comment" class="span10">
                % if c.discussion['text'] != '':
                    <div class="well">
                        ${c.discussion['text']}
                    </div>
                % endif 
            </div>
        </div>
    </div>
</%def>

<%def name="displayTopics()">
    % if c.otherDiscussions:
        <ul class="civ-col-list unstyled">
            % for discussion in c.otherDiscussions:
            <% owner = getUserByID(discussion.owner) %>
            <li>
                <h3>
                    <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/discussion/${discussion['urlCode']}/${discussion['url']}">${discussion['title']}</a>
                </h3>
                Posted <span class="recent">${timeSince(c.discussion.date)}</span> ago by <a href="/profile/${owner['urlCode']}/${owner['url']}">${owner['name']}</a>
            </li>
            % endfor
        </ul>
    % else:
        <div class="alert alert-danger">
            No other discussions found.
        </div> <!-- /.alert.alert-danger -->
    % endif
</%def>

<%def name="Edit_Admin()">
    <div class="span1"></div>
    <div class="span11">
        <div class="span2">
            <a href="/editDiscussion/${c.discussion['urlCode']}/${c.discussion['url']}">edit discussion </a>
        </div>
        <div class="span3">
            <a href="/adminDiscussion/${c.discussion['urlCode']}/${c.discussion['url']}">admin discussion</a>
        </div>
    </div>
</%def>

<%def name="addTopic()">
    <span class="pull-right topic"><a href="/workshop/${c.w['urlCode']}/${c.w['url']}/addDiscussion" title="Add a topic"><i class="icon-plus"></i></a></span>
</%def>