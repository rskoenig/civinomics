<%!
    from pylowiki.lib.db.user import getUserByID, isAdmin
    from pylowiki.lib.db.facilitator import isFacilitator

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

<%def name="suggestionAuthor(directoryNumber, cAuthor, wId)">
    <div class="row-fluid">
        <div class="span4">
            % if cAuthor['pictureHash'] == 'flash':
                <a href="/profile/${cAuthor['urlCode']}/${cAuthor['url']}"><img src="/images/avatars/flash.profile" alt="avatar" class="right" style="width:50px;}"/></a>
            % else:
                <a href="/profile/${cAuthor['urlCode']}/${cAuthor['url']}"><img src="/images/avatar/${directoryNumber}/thumbnail/${cAuthor['pictureHash']}.thumbnail" alt="avatar" class="right"/></a>
            % endif
        </div>
    </div>
    % if isAdmin(cAuthor.id):
       <% uTitle = ' (Admin)' %>
    % elif isFacilitator(cAuthor.id, wId):
       <% uTitle = ' (Facilitator)' %>
    % else:
       <% uTitle = '' %>
    % endif
    <div class="row-fluid">
        <span style="text-align:right;">
            Author: <a href="/profile/${cAuthor['urlCode']}/${cAuthor['url']}">${cAuthor['name']}</a>${uTitle}
        </span>
    </div>
</%def>

<%def name="suggestionContent(content)">
    <p>
        ${content}
    </p>
</%def>

<%def name="suggestionEditAdminRating(cAuthuser, cwOwner, cs, cIsAdmin, session, cRating)">
    <div class="row">
        <div class="span4 offset4">
            <table>
                <tbody>
                    <tr>
                        <td>
                            % if cAuthuser and (cAuthuser.id == cwOwner or cIsAdmin):
                                <a href="/modSuggestion/${cs['urlCode']}/${cs['url']}">admin suggestion</a>&nbsp;&nbsp;
                            % endif
                        </td>
                        <td>
                            % if cAuthuser and (cAuthuser.id == csOwner or cIsAdmin):
                                <a href="/editSuggestion/${cs['urlCode']}/${cs['url']}">edit suggestion</a>
                            % endif
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2">
                            % if "user" in session:
                                % if cRating:
                                    <div class = "gray rating wide">
                                        <div id="overall_slider" class="ui-slider-container">
                                            <div id="${cs['urlCode']}_${cs['url']}" class="normal_slider" data1="0_${cs['urlCode']}_${cRating['rating']}_overall_true_rateSuggestion" data2="${cs['url']}"></div>
                                        </div>
                                    </div>
                                % else:
                                    <div class = "gray rating wide">
                                        <div id="overall_slider" class="ui-slider-container">
                                            <div id="${cs['urlCode']}_${cs['url']}" class="normal_slider" data1="0_${cs['urlCode']}_0_overall_false_rateSuggestion" data2="${cs['url']}"></div>
                                        </div>
                                    </div>
                                % endif
                            % endif
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
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
