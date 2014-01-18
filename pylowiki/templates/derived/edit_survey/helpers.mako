<%def name='surveyName(survey)'>
    <label class="control-label" for="surveyName">Survey name: </label>
    <div class="controls">
        <input type="text" class="input-xxlarge" id="surveyName" name="surveyName" placeholder = "${survey['title']}">
        <p class="help-block">Try to keep this concise!</p>
    </div>
</%def>

<%def name='description(survey)'>
    <label class="control-label" for="surveyName">Description: </label>
    <div class="controls">
        <textarea rows="3" id="textarea" class="input-xxlarge" name="description" placeholder = "${survey['description']}"></textarea>
    </div>
</%def>

<%def name='geoScope(survey)'>
    <label class="control-label" for="geoScopeText">Geographic Scope: </label>
    <div class="controls">
        <input type="text" class="input-xxlarge" id="geoScopeText" name="geoScope" placeholder = "${survey['publicPostalList']}">
        <p class="help-block">Comma separated list of zip codes</p>
    </div>
</%def>

<%def name='estimatedTime(survey)'>
    <label class="control-label" for="estimatedTime">Estimated Time: </label>
    <div class="controls">
        <input type="text" class="input-xxlarge" id="estimatedTime" name="estimatedTime" placeholder="${survey['estimatedTime']}">
        <p class="help-block">How long the survey should take, in minutes</p>
    </div>
</%def>

<%def name='submitButton()'>
    <div class="form-actions" style="background-color:white;">
        <button class="btn btn-primary btn-large" type="submit">Submit</button>
    </div>
</%def>

<%def name="publishMessage(survey)">
    % if survey['hash'] == 'flash':
        You cannot activate a survey until you have uploaded a survey
    % else:
        If everything looks good, click on this stupidly large button to:
    % endif
</%def>

<%def name="publishButton(survey, state)">
    % if survey['hash'] == 'flash':
        ## Do nothing
        <p></p>
    % else:
        <div class="form-actions" style="background-color:white;">
            <button class="btn btn-success btn-large" type="submit" style="padding:20px 20px; font-size:40px;">
                % if state == 0:
                    Activate
                % else:
                    Deactivate
                % endif
            </button>
        </div>
    % endif
</%def>

<%def name="addFacilitator(survey)">
    <form id="addFacilitator" action="/survey/${survey['urlCode']}/${survey['url']}/addFacilitator" method="POST" enctype="multipart/form-data" class="form-horizontal">
        <fieldset>
            <legend style="text-align:center;">
                Add an existing facilitator to this survey
            </legend>
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
