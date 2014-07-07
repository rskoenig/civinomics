<%!
    import logging
    log = logging.getLogger(__name__)
%>

<%def name="createWorkshop()">
    <div class="row-fluid">
        <form id="CreateWorkshop" action = "/workshop/create/handler" class="form-vertical" method = "post">
            <div class="span6">
                <ul class="well orange pricing-table">
                    <li class="title"><h3>Private</h3><i class="icon-group icon-4x"></i></li>
                    <li class="price">Only people you invite can participate</li>
                    <li class="description"> Totally free! </li>
                    <li class="bullet-item"> Unlimited members </li>
                    <li class="cta-button"> 
                        <button type="submit" name="createPrivate" class="btn btn-large btn-civ">Go Private</button>
                    </li>
                </ul>
            </div> <!-- /.span6 -->
            <div class="span6">
                <ul class="well purple pricing-table ">
                    <li class="title"><h3>Public</h3><i class="icon-globe icon-4x"></i></li>
                    <li class="price">Anyone can participate</li>
                    <li class="description"> Totally free! </li>
                    <li class="bullet-item"> Unlimited members </li>
                    <li class="cta-button"> 
                        <button type="submit" name="createPublic" class="btn btn-large btn-civ">Go Public</button>
                    </li>
                </ul>
            </div> <!-- /.span6 -->
        </form>
    </div>
</%def>

