<%!
    from pylowiki.lib.db.user import getUserByID

    import logging
    log = logging.getLogger(__name__)
%>

<%namespace name="lib" file="/lib/mako_lib.mako" />

<%def name="addResourceForm(c)">
    ${lib.fields_alert()}
    % if c.r:
        <form id="edit_resource" action = "${c.site_secure_url}/saveResource/${c.r['urlCode']}/${c.r['url']}" class="form-vertical" method = "post">
        <% linkValue = c.r['link'] %>
        <% titleValue = c.r['title'] %>
        <% commentValue = c.r['comment'] %>
    % else:
        <form id="add_resource" action = "${c.site_secure_url}/addResource/${c.w['urlCode']}/${c.w['url']}" class="form-vertical" method = "post">
        % if c.resourceTitle:
            <% titleValue = c.resourceTitle %>
        % else:
            <% titleValue = '' %>
        % endif
        % if c.resourceComment:
            <% commentValue = c.resourceComment %>
        % else:
            <% commentValue = '' %>
        % endif
        % if c.resourceLink:
            <% linkValue = c.resourceLink %>
        % else:
            <% linkValue = '' %>
        % endif
    % endif
    % if c.s:
        <input type="hidden" name="suggestionCode" value="${c.s['urlCode']}">
        <input type="hidden" name="suggestionURL" value="${c.s['url']}">
    % endif

    <fieldset>
    <br />
    <div class="control-group">
        <label class="control-label"><strong>Resource URL:</strong></label>
        <div class="controls docs-input-sizes">
            <input type="text" id="resourceurl" name = "link" value="${linkValue}"/>
        </div><!-- controls -->
    </div><!-- control-group -->
                   
    <div class="control-group">
        <label class="control-label"><strong>Resource Title:</strong></label>
        <label class="control-label">Keep the title short and informative as possible.</label>
        <div class="controls docs-input-sizes">
            <input type="text" id="resourcetitle" name = "title" value="${titleValue}"/>
        </div><!-- controls -->
    </div><!-- control-group -->

    <div class="control-group">
        <label class="control-label"><strong>Description:</strong></label>
        <label class="control-label">Please provide a complete description of your information resource.</label>
        <div class="controls docs-input-sizes">
            <textarea id="resourcetext" name="comment" rows=8 cols=50 onkeyup="previewAjax( 'resourcetext', 'resource-preview-div' )" class="markitup">${commentValue}</textarea>
            <div id="resource-preview-div"></div>
        </div><!-- controls -->
    </div><!-- control-group -->

    <div class="control-group">
        % if c.r and 'allowComments' in c.r and c.r['allowComments'] == '0':
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
        </div><!-- controls -->
    </div><!-- controls -->
    <div class="form-actions">
        <button type="submit" class="btn btn-success">Submit</button>
    </div>
    </fieldset>
    </form>
</%def>

<%def name="listOtherResources(c, author)">
    <ul id="related_resource" class="unstyled">
        % if len(c.otherResources) == 0:
            <li>No other resources!</li>
        % else:
            % for resource in c.otherResources:
                <% author = getUserByID(resource.owner)%>
                <li>
                    <strong class="issue_name"><a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${resource['urlCode']}/${resource['url']}">${resource['title']}</a></strong>
                    <br />
                    <span class="gray">By <a href="/profile/${author['urlCode']}/${author['url']}">${author['name']}</a></span>
                </li>
            % endfor
        % endif
    </ul> <!-- related_resource -->
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

<%def name="relatedSuggestions(cSuggestions, cW, author)">
    <ul id="related_suggestion" class="unstyled">
        % if len(cSuggestions) == 0:
            <li>
                No other suggestions!
            </li>
        % else:
            % for suggestion in cSuggestions:
                <% author = getUserByID(suggestion.owner)%>
                <li>
                    <strong class="issue_name"><a href="/workshop/${cW['urlCode']}/${cW['url']}/suggestion/${suggestion['urlCode']}/${suggestion['url']}">${suggestion['title']}</a></strong>
                    <br />
                    <span class="gray">By <a href="/profile/${author['urlCode']}/${author['url']}">${author['name']}</a></span>
                </li>
            % endfor
        % endif
    </ul> <!-- related_suggestion -->
    <ul class="unstyled share suggest invite">
        <li>
            <img src="/images/handdove.png" />
            <a href="#">
                Invite to Civinomics
            </a>
        </li>
        <li>
            <img src="/images/suggest_an_issue.png" /> 
            <a href="#">
                Suggest a workshop
            </a>
        </li>
    </ul>
</%def>
