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

<%def name="comments(thing, **kwargs)">
    <%
        addCommentToDiscussion(thing)
    %>
</%def>

<%def name="addCommentToDiscussion(thing)">
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

<%def name="sortCommentTree(tree)">
    ## TODO
</%def>