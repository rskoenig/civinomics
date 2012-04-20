<%inherit file="/base/base.mako"/>
<%namespace file="/lib/mako_lib.mako" import="gravatar" />
<%namespace file="/derived/events.mako" import="events" />

<h1>${c.user.name}'s stats</h1>

${gravatar(c.user.email, 128, float = "left" )}

<ul style="padding-left: 170px;">
% for z in c.statzip:
    <li>${z[1]} ${z[0]}'s</li>
% endfor  
</ul>
<b style="padding-left: 10px;">Member since:</b> ${c.user.regdate.strftime("%B %d, %Y")} 

<br><br>

<a href="http://gravatar.com/" target="_blank">What is a gravatar?</a>

<br><br>

<a href="/login/changepass">Change password?</a>


<h1>${c.user.name}'s events</h1>

${events()}
