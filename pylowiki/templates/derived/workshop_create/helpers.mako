<%!
    import logging
    log = logging.getLogger(__name__)
%>

<%def name="showTitle(title)">
    <h1 style="text-align:center;">${title}</h1>
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
                <fieldset>
                    <div class="control-group">
                        <label class="control-label">Workshop Name:</label>
                        <div class="controls docs-input-sizes">
                            <input type="text" class="span2" placeholder="workshop name" name = "workshopName"/>
                        </div>
                    </div>
                    
                    <div class="control-group">
                        
                        <div class="controls">
                            <label class="radio">
                                <input type="radio" name="publicPrivate" value="public">
                                
                                    Public
                                
                            </label>
                            <label class="radio">
                                <input type="radio" name="publicPrivate" value="private">
                                
                                    Private
                                
                            </label>
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