<%!
    from pylowiki.lib.fuzzyTime import timeSince
    from pylowiki.lib.db.user import getUserByID
%>

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

<%def name="discTopicPageTitle()">
    <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/discussion">DISCUSSION</a> 
    IN
    <a href="/workshop/${c.w['urlCode']}/${c.w['url']}">${c.w['title']}</a>

</%def>

<%def name="displayTopicContent()">
    <div class="row-fluid">
        <div class="span1 civ-votey">
            <% rating = int(c.discussion['ups']) - int(c.discussion['downs']) %>
            % if 'user' in session:
                <a href="/rateDiscussion/${c.discussion['urlCode']}/${c.discussion['url']}/1" class="upVote voted">
                <i class="icon-chevron-up"></i>
                </a>
                <div>${rating}</div>
                <a href="/rateDiscussion/${c.discussion['urlCode']}/${c.discussion['url']}/-1" class="downVote voted">
                <i class="icon-chevron-down"></i>
                </a>
            % else:
                <div>${rating}</div>
            % endif
        </div>
        <% owner = getUserByID(c.discussion.owner) %>
        <div class="span11">
            <a href="#"><h3>${c.discussion['title']}</h3></a>
            <table>
            <thead>
            <tr>
            <td>${userphoto(c.discussion)}</td>
            <td><a href="/profile/${owner['urlCode']}/${owner['url']}">${getUserByID(c.discussion.owner)['name']}</a><br />
            <i class="icon-time"></i> Started <span class="recent">${timeSince(c.discussion.date)}</span> ago 
            </td>
            </tr>
            </thead>
            </table>
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
        <div class="alert alert-warning">
            No other discussion topics found.
        </div> <!-- /.alert.alert-danger -->
    % endif
</%def>

<%def name="Edit_Admin()">
    <span class="badge badge-inverse"><i class="icon-white icon-flag"></i>${len(c.flags)}</span>
    % if c.authuser.id == c.discussion.owner or c.isAdmin or c.isFacilitator:
        <a href="/editDiscussion/${c.discussion['urlCode']}/${c.discussion['url']}" class="btn btn-primary btn-mini"><i class="icon-white icon-edit"></i> edit</a>
    % endif
    % if c.isAdmin or c.isFacilitator:
        <a href="/adminDiscussion/${c.discussion['urlCode']}/${c.discussion['url']}" class="btn btn-warning btn-mini"><i class="icon-white icon-list-alt"></i> admin</a>
    % endif
    <a href="/flagDiscussion/${c.discussion['urlCode']}/${c.discussion['url']}" class="btn btn-inverse btn-mini flagButton"><i class="icon-white icon-flag"></i> Flag</a>
    <span id="flag_0"></span>
</%def>

<%def name="addTopic()">
    <span class="pull-right topic"><a href="/workshop/${c.w['urlCode']}/${c.w['url']}/addDiscussion" title="Add a topic"><i class="icon-plus"></i></a></span>
</%def>
