<%inherit file = "/base/template.html"/>

% if c.type != "pending" and c.type != "disabled":
    Incorrect moderation type!
% else:
    <% session['articles'] = [] %>
    % if c.articles:
        ${ h.form( url( controller = 'moderation', action ='handler', id = 'article'), method='put' ) }
            ${self.articles()}
            ${h.submit('submit', 'Submit')}
        ${h.end_form()}
    % else:
        There don't appear to be any ${c.type} articles here for moderation!
    % endif
% endif

<%def name = 'articles()'>
    % for article in c.articles:
        <% titleFlag = False %>
        % if c.type == "disabled":
            % if article.disabled:
                % if not titleFlag:
                    <% titleFlag = True %>
                    <h3> Issue title: ${article.issue.name} </h3>
                % endif
                ${session['articles'].append(article.id)}
                <span><img src="/images/avatars/${article.events[0].user.pictureHash}.thumbnail" /> <a href = "/account/${article.events[0].user.name}">${article.events[0].user.name}</a> suggests:</span>
                
                <p>
                <br />
                    <a href = "${article.url}"> ${article.title} </a>
                </p>
                <br />
                <span class="time">${article.events[0].date.strftime("%I:%M %p   %m-%d-%Y")}</span>
                <br />
                ${h.radio(article.id, '0')} Allow <br />
                ${h.radio(article.id, '1')} Deny <br />
                ${h.radio(article.id, '2', checked = True)} Leave alone <br />
            % endif
        % elif c.type == "pending":
            % if article.pending:
                % if not titleFlag:
                    <% titleFlag = True %>
                    <h3> Issue title: ${article.issue.name} </h3>
                % endif
                ${session['articles'].append(article.id)}
                <span><img src="/images/avatars/${article.events[0].user.pictureHash}.thumbnail" /> <a href = "/account/${article.events[0].user.name}">${article.events[0].user.name}</a> suggests:</span>
                
                <p>
                <br />
                    <a href = "${article.url}"> ${article.title} </a>
                </p>
                <br />
                <span class="time">${article.events[0].date.strftime("%I:%M %p   %m-%d-%Y")}</span>
                <br />
                ${h.radio(article.id, '0')} Allow <br />
                ${h.radio(article.id, '1')} Deny <br />
                ${h.radio(article.id, '2', checked = True)} Leave alone <br />
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