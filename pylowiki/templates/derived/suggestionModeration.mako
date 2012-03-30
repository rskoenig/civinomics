<%inherit file = "/base/template.html"/>

% if c.type != "pending" and c.type != "disabled":
    Incorrect moderation type!
% else:
    <% session['suggestions'] = [] %>
    ${ h.form( url( controller = 'moderation', action ='handler', id = 'suggestion'), method='put' ) }
        ${self.suggestions()}
        ${h.submit('submit', 'Submit')}
    ${h.end_form()}
% endif

<%def name = 'suggestions()'>
    % for suggestion in c.suggestions:
        <% titleFlag = False %>
        % if c.type == "disabled":
            % if suggestion.disabled:
                % if not titleFlag:
                    <% titleFlag = True %>
                    <h3> Issue title: ${suggestion.issue.name} </h3>
                    <h4> Suggestion title: ${suggestion.title} </h4>
                % endif
                ${session['suggestions'].append(suggestion.id)}
                <span><img src="/images/avatars/${suggestion.events[0].user.pictureHash}.thumbnail" /> <a href = "/account/${suggestion.events[0].user.name}">${suggestion.events[0].user.name}</a> suggests:</span>
                
                <p>
                <br />
                    ${h.literal(h.reST2HTML(suggestion.revisions[0].data))}
                </p>
                <br />
                <span class="time">${suggestion.events[0].date.strftime("%I:%M %p   %m-%d-%Y")}</span>
                <br />
                ${h.radio(suggestion.id, '0')} Allow <br />
                ${h.radio(suggestion.id, '1')} Deny <br />
                ${h.radio(suggestion.id, '2', checked = True)} Leave alone <br />
            % endif
        % elif c.type == "pending":
            % if suggestion.pending:
                % if not titleFlag:
                    <% titleFlag = True %>
                    <h3> Issue title: ${suggestion.issue.name} </h3>
                    <h4> Suggestion title: ${suggestion.title} </h4>
                % endif
                ${session['suggestions'].append(suggestion.id)}
                <span><img src="/images/avatars/${suggestion.events[0].user.pictureHash}.thumbnail" /> <a href = "/account/${suggestion.events[0].user.name}">${suggestion.events[0].user.name}</a> suggests:</span>
                
                <p>
                <br />
                    ${h.literal(h.reST2HTML(suggestion.revisions[0].data))}
                </p>
                <br />
                <span class="time">${suggestion.events[0].date.strftime("%I:%M %p   %m-%d-%Y")}</span>
                <br />
                ${h.radio(suggestion.id, '0')} Allow <br />
                ${h.radio(suggestion.id, '1')} Deny <br />
                ${h.radio(suggestion.id, '2', checked = True)} Leave alone <br />
            % endif
        % else:
            Incorrect moderation type!
        % endif
    % endfor
</%def>


<%def name = 'extraStyles()'>
	
</%def>

<%def name = 'extraScripts()'>
	
</%def>

<%def name = 'extraHTML()'>

</%def>