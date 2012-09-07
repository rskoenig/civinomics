<%def name='showFacilitator(facilitator, counter)'>
    <%
        if int(facilitator['accessLevel']) not in [100, 200, 300]:
            return
    %>
    <div class="accordion-heading">
        <a href="#collapse${counter}" data-parent="#accordion" data-toggle="collapse" class="accordion-toggle">
            % if int(facilitator['accessLevel']) == 300:
                <span class="label label-important">Superuser</span>
            % elif int(facilitator['accessLevel']) == 200:
                <span class="label label-warning">Admin</span>
            % elif int(facilitator['accessLevel']) == 100:
                <span class="label">Facilitator</span>
            % endif
            ${facilitator['name']} (${facilitator['email']})
        </a>
    </div>
    <div class="accordion-body collapse" id="collapse${counter}">
        <table class="table table-striped">
            <tbody>
                <tr>
                    <td>Name: </td>
                    <td>
                        <a href="/profile/${facilitator['urlCode']}/${facilitator['url']}">${facilitator['name']}</a>
                    </td>
                </tr>
                <tr>
                    <td>Access Level: </td>
                    % if ${facilitator['accesslevel']} == '100':
                        <td>facilitator</td>
                    % elif ${facilitator['accesslevel']} == '200':
                        <td>administrator</td>
                    % elif ${facilitator['accesslevel']} == '300':
                        <td>superuser</td>
                    % else:
                        <td>${facilitator['accessLevel']}</td>
                    % endif
                </tr>
            </tbody>
        </table>
    </div>
</%def>

<%def name="showTitle(title)">
    <h1 style="text-align:center;">${title}</h1>
</%def>

<%def name="showFacilitators(facilitators)">
<% facilitatorNumber = 0 %>
    % for item in c.facilitators:
        <div id="accordion" class="accordion">
            <div class="accordion-group">
                ${showFacilitator(item, facilitatorNumber)}
            </div>
        </div>
        <% facilitatorNumber += 1 %>
    % endfor
</%def>

<%def name="addFacilitatorForm()">
    <form id="addFacilitator" action="/survey/addFacilitator" method="POST" enctype="multipart/form-data" class="form-horizontal">
        <fieldset>
            <div class="control-group">
                <label class="control-label" for="emailInput">Enter email:</label>
                <input type="text" placeholder="email address" class="input-large offset1" id="emailInput" name='email'>
            </div>
            
            <div class="form-actions" style="background-color:white;">
                <button class="btn btn-primary btn-large" type="submit">Add</button>
            </div>
        </fieldset>
    </form>
</%def>

<%def name="addAdminForm()">
    <form id="addFacilitator" action="/survey/addAdmin" method="POST" enctype="multipart/form-data" class="form-horizontal">
        <fieldset>
            <div class="control-group">
                <label class="control-label" for="emailInput">Enter email:</label>
                <input type="text" placeholder="email address" class="input-large offset1" id="emailInput" name='email'>
            </div>
            
            <div class="form-actions" style="background-color:white;">
                <button class="btn btn-primary btn-large" type="submit">Add</button>
            </div>
        </fieldset>
    </form>
</%def>

<%def name="setFeaturedSurvey(surveys)">
    <form class="form-horizontal" id="radioForm" action="/surveyAdmin/setFeaturedSurvey">
        <fieldset>
            <div class="control-group">
                <div class="controls" style="float:left;">
                    % for survey in surveys:
                        <label class="radio">
                            <input type = "radio" value = "${survey['urlCode']}_${survey['url']}" name="radioButton" id="option_${survey['urlCode']}_${survey['url']}" class="radioButton">
                            ${survey['title']}
                        </label>
                    % endfor
                </div>
            </div>
            
            <div class="form-actions" style="background-color:white;">
                <button class="btn btn-primary btn-large" type="submit">Set</button>
            </div>
        </fieldset>
    </form>
</%def>


<%def name='spacer()'>
    ## A spacer
    <div class="row-fluid">
        <br />
    </div>
</%def>