<%def name="events()">
<%namespace file="/lib/mako_lib.mako" import="gravatar" />

<table width='95%' align="center" class="event">

<% 
    daybr = state = True
%>

% for e in c.paginator:

    % if daybr != e.date.strftime("%m-%d-%Y"):
    <% state = True %>
    <tr><td colspan="2" class="daybr">${e.date.strftime("%m-%d-%Y")}</td></tr>
    % endif

    <% state = not state %>
    <tr class="event ${state}">

        <td style="width: 90%;" class="event">
	<a href="/account/${e.user.name}">${gravatar(e.user.email, 22, float="left")} ${e.user.name}</a>
        <% e.type = e.type.lower()%>
        % if e.type == "attach":
        uploaded an attachment ...
        % elif e.type == "user":
	    has joined the wiki
        % else:
            % if e.type == "edit" or e.type == "revert" or e.type == "revert" or e.type == "comment":
                ${e.type}ed
            % elif e.type == "create" or e.type == "delete" or e.type == "restore":
                ${e.type}d
            % endif
            the
            % try:
                <% e.page.url %>
                <a href="/${e.page.url}">${e.page.url}</a>
            % except:
                &nbsp;
            % endtry
            page            
            % try:
	            <% e.revision.id  %>
                - <a href='/revision/number/${e.revision.id}'>revision ${e.revision.id}</a>
            % except:
                &nbsp;
            % endtry
        % endif

	</td>
       
        <td style="text-align: right;" class="event">${e.date.strftime("%I:%M %p")}</td>
	% if e.remark:
		</tr>
        <tr class="event ${state}">
		  <td style="text-align: right;" colspan="2" class="event">
		    ${e.remark}
	% endif
	</td>
    </tr>
    <% daybr = e.date.strftime("%m-%d-%Y") %>
% endfor
</table>

<br />

<div style="text-align: center;">${ c.paginator.pager('~3~') }</div>

</%def>
