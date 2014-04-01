<%def name='surveyName()'>
    <label class="control-label" for="surveyName">Survey name: </label>
    <div class="controls">
        <input type="text" class="input-xxlarge" id="surveyName" name="surveyName">
        <p class="help-block">Try to keep this concise!</p>
    </div>
</%def>

<%def name='description()'>
    <label class="control-label" for="surveyName">Description: </label>
    <div class="controls">
        <textarea rows="3" id="textarea" class="input-xxlarge" name="description"></textarea>
    </div>
</%def>

<%def name='geoScope()'>
    <label class="control-label" for="geoScopeText">Geographic Scope: </label>
    <div class="controls">
        <input type="text" class="input-xxlarge" id="geoScopeText" name="geoScope">
        <p class="help-block">Comma separated list of zip codes</p>
    </div>
</%def>

<%def name='estimatedTime()'>
    <label class="control-label" for="estimatedTime">Estimated Time: </label>
    <div class="controls">
        <input type="text" class="input-xxlarge" id="estimatedTime" name="estimatedTime">
        <p class="help-block">How long the survey should take, in minutes</p>
    </div>
</%def>

<%def name='submitButton()'>
    <div class="form-actions" style="background-color:white;">
        <button class="btn btn-primary btn-large" type="submit">Create</button>
    </div>
</%def>