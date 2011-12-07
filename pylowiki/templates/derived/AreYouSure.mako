<%inherit file="/base/base.mako"/>

<h2 style="color: #E7B01E;">${c.heading}</h2>

% if c.action == "revert":
    ${h.form( "/AreYouSure/handler/" + c.revid, method='put')}
% else:
    ${h.form( "/AreYouSure/handler/" + c.url, method='put')}
% endif

Optional Remark:
<input type="text" id="remark" name="remark" class="text" placeholder="optional remark"/> 
<input type="text" id="sremark" name="sremark" class="text" />

${ h.submit('submit', 'Yes') }
<INPUT TYPE='BUTTON' VALUE='No' ONCLICK='history.go(-1)'>

${ h.hidden( "action", c.action ) }

${ h.end_form() }
