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

<%def name="createWorkshop()">
    
    <div class="row-fluid">
        <form id="create_issue" action = "/newWorkshop" class="form-vertical" method = "post">
        <div class="well">
            <h3>A Personal Workshop</h3>
            <ul>
            <li>It's Free!</li>
            <li>It's limited to private, invitation only.  Not visible to the public.</li> 
            <li>Invite up to 10 people to participate!</li>
            <li>You can upgrade it to a professional workshop at any time! (Good for trying things out, first)
            </ul>
            <button type="submit" name="createPersonal" class="btn btn-warning">Create Personal Workshop</button> 
        </div><!-- well -->
        <div class="well">
            <h3>A Professional Workshop</h3>
            <ul>
            <li>It costs $25 per month, cancel at any time.</li>
            <li>Unlimited participants!</li> 
            <li>You can make it private by invitation only or available for public participation.</li>
            </ul>
            <button type="submit" name="createProfessional" class="btn btn-warning">Create Professional Workshop</button> 
        </div><!-- well -->
        </form>
    </div>
</%def>

<%def name='inlineSpacer(amount)'>
    <div class="span${amount}">
        <p></p>
    </div>
</%def>
