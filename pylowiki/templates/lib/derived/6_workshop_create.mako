<%!
    import logging
    log = logging.getLogger(__name__)
%>

<%def name="createWorkshop()">
    <div class="row-fluid">
        <form id="CreateWorkshop" action = "/workshop/create/handler" class="form-vertical" method = "post">
            <div class="span6">
                <ul class="well orange pricing-table">
                    <li class="title"><h3>Free</h3><img style="height: 48px" src="/images/glyphicons_pro/glyphicons/png/glyphicons_024_parents@2x.png" alt="couple icon"></li>
                    <li class="price">$0 per month</li>
                    <li class="description"> Totally free! </li>
                    <li class="bullet-item"> Private </li>
                    <li class="bullet-item"> Limited to 20 people </li>
                    <li class="cta-button"> 
                        <button type="submit" name="createPersonal" class="btn btn-large btn-civ">Go Free</button>
                    </li>
                </ul>
            </div> <!-- /.span6 -->
            <div class="span6">
                <ul class="well purple pricing-table ">
                    <li class="title"><h3>Pro</h3><img src="/images/glyphicons_pro/glyphicons/png/glyphicons_024_parents@2x.png" alt="group icon"><em class="lead" style="padding: 0 10px;">   or   </em><img src="/images/glyphicons_pro/glyphicons/png/glyphicons_340_globe@2x.png" alt="globe icon"></li>
                    <li class="price">$15 per month</li>
                    <li class="description"> Best for community builders </li>
                    <li class="bullet-item"> Public or private</li>
                    <li class="bullet-item"> Unlimited private members </li>
                    <li class="cta-button"> 
                        <button type="submit" name="createProfessional" class="btn btn-large btn-civ">Go Pro</button>
                    </li>
                </ul>
            </div> <!-- /.span6 -->
        </form>
    </div>
</%def>

