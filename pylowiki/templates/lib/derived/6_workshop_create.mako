<%!
    import logging
    log = logging.getLogger(__name__)
%>

<%def name="createWorkshop()">
    <div class="row-fluid">
        <strong>What kind of workshop do you want to create?</strong><br /><br />
        <form id="CreateWorkshop" action = "/workshop/create/handler" class="form-vertical" method = "post">
        <div class="well">
            <h4>A Personal Workshop</h4>
            <ul>
            <li>It's Free!</li>
            <li>It's limited to private, invitation only.  Not visible to the public.</li> 
            <li>Invite up to 10 people to participate!</li>
            <li>You can upgrade it to a professional workshop at any time! (Good for trying things out, first)
            </ul>
            <button type="submit" name="createPersonal" class="btn btn-warning">Create Personal Workshop</button> 
        </div><!-- well -->
        <div class="well">
            <h4>A Professional Workshop</h4>
            <ul>
            <li>It costs $99 per month, cancel at any time.</li>
            <li>Unlimited participants!</li> 
            <li>You can make it private by invitation only or available for public participation.</li>
            </ul>
            <button type="submit" name="createProfessional" class="btn btn-warning">Create Professional Workshop</button> 
        </div><!-- well -->
        </form>
    </div>
</%def>

