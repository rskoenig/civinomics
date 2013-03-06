<%!
    import logging
    log = logging.getLogger(__name__)
%>

<%def name="createWorkshop()">
    <div class="row-fluid">
        <form id="CreateWorkshop" action = "/workshop/create/handler" class="form-vertical" method = "post">
        <div class="span6">
            <ul class="pricing-table">
                <li class="title">Free</li>
                <li class="price">$0 per month</li>
                <li class="description"> Totally free! </li>
                <li class="bullet-item"> Private and invite-only </li>
                <li class="bullet-item"> Limited to 20 people </li>
                <li class="cta-button"> 
                    <button type="submit" name="createPersonal" class="btn btn-warning">Go free!</button>
                </li>
            </ul>
        </div> <!-- /.span6 -->
        <div class="span6">
            <ul class="pricing-table">
                <li class="title">Pro</li>
                <li class="price">$100 per month</li>
                <li class="description"> Best for community builders </li>
                <li class="bullet-item"> Private or public </li>
                <li class="bullet-item"> Unlimited members </li>
                <li class="cta-button"> 
                    <button type="submit" name="createProfessional" class="btn btn-warning">Go paid!</button>
                </li>
            </ul>
        </div> <!-- /.span6 -->
        <%doc>
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
        </%doc>
    </div>
</%def>

