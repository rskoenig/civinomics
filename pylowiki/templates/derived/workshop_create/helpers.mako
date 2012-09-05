<%!
    import logging
    log = logging.getLogger(__name__)
%>

<%def name="showTitle(title)">
    <h1 style="text-align:left;">${title}</h1>
</%def>

<%def name='spacer()'>
    ## A spacer
    <div class="row-fluid">
        <br />
    </div>
</%def>

<%def name="addWorkshop()">
    <div class="fluid-row">
        <div class="span4">
            <form id="create_issue" action = "${c.site_secure_url}/workshop/addWorkshopHandler" class="form-vertical" method = "post">
            <input type="hidden" name="publicPrivate" value="public">
                <fieldset>
                    <div class="control-group">
                        <label class="control-label">Workshop Name (70 char. max.):</label>
                        <div class="controls docs-input-sizes">
                            <input type="text" name = "workshopName" maxlength="70"/>
                        </div>
                    </div>
                    <div class="form-actions">
                        <button type="submit" class="btn btn-success">Next Page</button>
                    </div>
                </fieldset>
            </form>
        </div>
    </div>
</%def>

<%def name='inlineSpacer(amount)'>
    <div class="span${amount}">
        <p></p>
    </div>
</%def>
