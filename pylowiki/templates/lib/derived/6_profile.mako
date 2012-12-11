<%def name="commentCount(comments)">
    <h1 class="profile-count">${len(comments)}</h1>
    <div class="green">comments</div>
</%def>

<%def name="resourceCount(resources)">
    <h1 class="profile-count">${len(resources)}</h1>
    <div class="green">resources</div>
</%def>

<%def name="ideaCount(ideas)">
    <h1 class="profile-count">${len(ideas)}</h1>
    <div class="green">ideas</div>
</%def>

<%def name="discussionCount(discussions)">
    <h1 class="profile-count">${len(discussions)}</h1>
    <div class="green">discussions</div>
</%def>