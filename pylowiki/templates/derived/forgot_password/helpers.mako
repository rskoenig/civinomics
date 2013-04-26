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

<%def name="forgotPassword()">
        <p><em>Enter your email to reset your password.</em></p>
        <form id="forgot_password" action="/forgotPasswordHandler" class="form form-horizontal" method="post">
            <div class="control-group">
                <label class="control-label" for="email"> Email: </label>
                <div class="controls">
                    <input type="email" name="email" id="email">
                </div>
            </div>
            <div class="control-group">
                <div class="controls">
                    <button type="submit" class="btn btn-primary"> Submit </button>
                </div>
            </div>
        </form>
</%def>

<%def name='inlineSpacer(amount)'>
    <div class="span${amount}">
        <p></p>
    </div>
</%def>
