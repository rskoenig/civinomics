<%!
    from pylowiki.lib.db.user import getUserByID

    import logging
    log = logging.getLogger(__name__)
%>

<%def name='spacer()'>
    ## A spacer
    <div class="row-fluid">
        <br />
    </div>
</%def>

<%def name='inlineSpacer(amount)'>
    <div class="span${amount}">
        <p></p>
    </div>
</%def>

<%def name="workshopTitle(cW)">
    <ul class="unstyled nav-thing">
        <li class="current">
            <a href = "/workshop/${cW['urlCode']}/${cW['url']}">${cW['title']}</a>
        </li>
    </ul>
</%def>

<%def name="addSuggestionForm(c)">
            % if c.s:
                <form id="edit_suggestion" action = "${c.site_secure_url}/saveSuggestion/${c.s['urlCode']}/${c.s['url']}" class="form-vertical" method = "post">
                    <% dataValue = c.s['data'] %>
                    <% titleValue = c.s['title'] %>
                    <% allowComments = c.s['allowComments'] %>
            % else:
                <form id="add_suggestion" action = "${c.site_secure_url}/addSuggestion/${c.w['urlCode']}/${c.w['url']}" class="form-vertical" method = "post">
                    <% dataValue = '' %>
                    <% titleValue = '' %>
                    <% allowComments = '' %>
            % endif

                <fieldset>
                    <div class="control-group">
                        <label class="control-label"><strong>Suggestion Title:</strong></label>
                        <label class="control-label">Keep the title short and informative as possible.</label>
                        <div class="controls docs-input-sizes">
                            <input type="text" id="suggestiontitle" name = "title" value="${titleValue}"/>
                        </div>
                    </div>

                    <div class="control-group">
                        <label class="control-label"><strong>Suggestion Description:</strong></label>
                        <label class="control-label">Please enter your suggestion here. Please make sure it addresses the goals of this workshop, and is compreshensive and complete.</label>
                        <div class="controls docs-input-sizes">
                            <textarea id="suggestiontext" name="data" rows=8 cols=50 onkeyup="previewAjax( 'suggestiontext', 'suggestion-preview-div' )" class="markitup">${dataValue}</textarea>
                            <div id="suggestion-preview-div"></div>
                        </div>
                    </div>

                    <div class="control-group">
                        % if c.s and 'allowComments' in c.s and c.s['allowComments'] == '0':
                           <% noChecked = 'checked' %>
                           <% yesChecked = '' %>
                        % else:
                           <% yesChecked = 'checked' %>
                           <% noChecked = '' %>
                        % endif

                        <div class="controls">
                            <label class="control-label">
                                Allow member comments:
                            </label>
                            <label class="radio inline">
                                <input type = "radio" name = "allowComments" value = "1" ${yesChecked}> Yes 
                            </label>
                            &nbsp;&nbsp;&nbsp;
                            <label class="radio inline">
                                <input type = "radio" name = "allowComments" value = "0" ${noChecked}> No 
                            </label>
                        </div>
                    </div>
                    <div class="form-actions">
                        <button type="submit" class="btn btn-success">Submit</button>
                    </div>
                </fieldset>
            </form>
</%def>

<%def name="listOtherSuggestions(c, author)">
    <ul id="related_suggestion" class="unstyled">
        % if len(c.suggestions) == 0:
            <li>No other suggestions!</li>
        % else:
            % for suggestion in c.suggestions:
                <% author = getUserByID(suggestion.owner)%>
                <li>
                    <strong><a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${suggestion['urlCode']}/${suggestion['url']}">${suggestion['title']}</a></strong>
                    <br />
                    <span class="gray">By <a href="/profile/${author['urlCode']}/${author['url']}">${author['name']}</a></span>
                </li>
            % endfor
        % endif
    </ul> <!-- related_suggestion -->
</%def>

<%def name="showTitle(title)">
    <h1 style="text-align:center;">${title}</h1>
</%def>

<%def name="suggestionAndWorkshopTitle(cW, cS)">
    <p>
        <strong class="issue_name"><a href="/workshop/${cW['urlCode']}/${cW['url']}/suggestion/${cS['urlCode']}/${cS['url']}">${cS['title']}</a></strong>
        <br />
        Workshop: <a href="/workshop/${cW['urlCode']}/${cW['url']}">${cW['title']}</a>
        <br />
    </p>
</%def>
