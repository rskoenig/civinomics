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
    </div>
</%def>

