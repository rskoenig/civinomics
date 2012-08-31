<%inherit file="/base/base.mako"/>
<%namespace file="/lib/mako_lib.mako" import="gravatar" />

<h1> ${c.heading} </h1>

Results: ${c.count}

<br > <br>

<table width='100%'>
   
<% state = True %>
% for user in c.paginator:
    <% state = not state %>
    
    <tr class="${state}">
        <td width="35%"><a href='/account/${user.name}'>${gravatar(user.email, 22)}${user.name}</a></td>
    </tr>
% endfor

</table>

<br />

<div style="text-align: center;">${ c.paginator.pager('~3~') }</div>
