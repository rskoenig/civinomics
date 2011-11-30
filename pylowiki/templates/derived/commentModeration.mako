<%inherit file = "/base/template.html"/>
##% if c.pages.comments:
% if c.type != "pending" and c.type != "disabled":
    Incorrect moderation type!
% else:
    <% session['comments'] = [] %>
    ${ h.form( url( controller = 'moderation', action ='handler', id = 'comment'), method='put' ) }
        ${self.issues()}
        ${self.suggestions()}
        ${h.submit('submit', 'Submit')}
    ${h.end_form()}
% endif
##% endif

<%def name = 'issues()'>
% for page in c.pages:
    <% titleFlag = 0 %>
    ## There has to be a better way to do this.
    % for comment in page.comments:
        % if c.type == "disabled":
            % if comment.disabled:
                <% titleFlag = 1 %>
                <% break %>
            % endif
        % elif c.type == "pending":
            % if comment.pending:
                <% titleFlag = 1 %>
                <% break %>
            % endif
        % endif
    % endfor
    % if titleFlag:
        <h3> Issue title: ${page.title} </h3>
    % endif
    <br />
    <br />
    %for comment in reversed(page.comments):
        % if c.type == "disabled":
            % if comment.disabled:
                ${session['comments'].append(comment.id)}
                <span><img src="/images/avatars/${comment.event.user.pictureHash}.thumbnail" /> <a href = "/account/${comment.event.user.name}">${comment.event.user.name}</a> said:</span>
                
                <p>
                <br />
                    ${h.literal(h.reST2HTML(comment.data))}
                </p>
                <br />
                <span class="time">${comment.event.date.strftime("%I:%M %p   %m-%d-%Y")}</span>
                <br />
                ${h.radio(comment.id, '0')} Allow <br />
                ${h.radio(comment.id, '1')} Deny <br />
                ${h.radio(comment.id, '2', checked = True)} Leave alone <br />
            % endif
        % elif c.type == "pending":
            % if comment.pending:
                ${session['comments'].append(comment.id)}
                <span><img src="/images/avatars/${comment.event.user.pictureHash}.thumbnail" /> <a href = "/account/${comment.event.user.name}">${comment.event.user.name}</a> said:</span>
                
                <p>
                <br />
                    ${h.literal(h.reST2HTML(comment.data))}
                </p>
                <br />
                <span class="time">${comment.event.date.strftime("%I:%M %p   %m-%d-%Y")}</span>
                <br />
                ${h.radio(comment.id, '0')} Allow <br />
                ${h.radio(comment.id, '1')} Deny <br />
                ${h.radio(comment.id, '2', checked = True)} Leave alone <br />
            % endif
        % else:
            Incorrect moderation type!
        % endif
    % endfor
% endfor
</%def>

<%def name = 'suggestions()'>
% for suggestion in c.suggestions:
    <% titleFlag = 0 %>
    ## There has to be a better way to do this.
    % for comment in suggestion.comments:
        % if c.type == "disabled":
            % if comment.disabled:
                <% titleFlag = 1 %>
                <% break %>
            % endif
        % elif c.type == "pending":
            % if comment.pending:
                <% titleFlag = 1 %>
                <% break %>
            % endif
        % endif
    % endfor
    % if titleFlag:
        <h3> Suggestion title: ${suggestion.title} </h3>
        <h4> In issue: ${suggestion.issue.name}</h4>
    % endif
    <br />
    <br />
    %for comment in reversed(suggestion.comments):
        % if c.type == "disabled":
            % if comment.disabled:
                ${session['comments'].append(comment.id)}
                <span><img src="/images/avatars/${comment.event.user.pictureHash}.thumbnail" /> <a href = "/account/${comment.event.user.name}">${comment.event.user.name}</a> said:</span>
                
                <p>
                <br />
                    ${h.literal(h.reST2HTML(comment.data))}
                </p>
                <br />
                <span class="time">${comment.event.date.strftime("%I:%M %p   %m-%d-%Y")}</span>
                <br />
                ${h.radio(comment.id, '0')} Allow <br />
                ${h.radio(comment.id, '1')} Deny <br />
                ${h.radio(comment.id, '2', checked = True)} Leave alone <br />
            % endif
        % elif c.type == "pending":
            % if comment.pending:
                ${session['comments'].append(comment.id)}
                <span><img src="/images/avatars/${comment.event.user.pictureHash}.thumbnail" /> <a href = "/account/${comment.event.user.name}">${comment.event.user.name}</a> said:</span>
                
                <p>
                <br />
                    ${h.literal(h.reST2HTML(comment.data))}
                </p>
                <br />
                <span class="time">${comment.event.date.strftime("%I:%M %p   %m-%d-%Y")}</span>
                <br />
                ${h.radio(comment.id, '0')} Allow <br />
                ${h.radio(comment.id, '1')} Deny <br />
                ${h.radio(comment.id, '2', checked = True)} Leave alone <br />
            % endif
        % else:
            Incorrect moderation type!
        % endif
    % endfor
% endfor
</%def>


<%def name = 'extraStyles()'>
	
</%def>

<%def name = 'extraScripts()'>
	
</%def>

<%def name = 'extraHTML()'>

</%def>