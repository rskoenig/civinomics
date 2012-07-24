<%inherit file="/base/base.mako"/>

<h1>${c.heading}</h1>

% if c.controller == "create":
    ${ h.form( url( controller = c.controller, action ='handler' ), method='put' ) }
    URL <input type="text" id="page_url"  name="page_url" class="text" value="${c.url}" placeholder="eg: os/linux/ubuntu"/>
% elif c.controller == "edit":
    ${ h.form( url( controller = c.controller, action ='handler', id = c.url ), method='put' ) }
% endif

<textarea rows="17" id="textarea" name="textarea" onkeyup="previewAjax( 'textarea', 'preview' )" class="markitup">${c.rST}</textarea>

<div align="right">
    <span style="float:left;">You should <a href="#preview">preview below</a> before saving.</span>
    Optional remark: <input type="text" id="remark"  name="remark" class="text" placeholder="optional remark"/>
    <input type="text" id="sremark"  name="sremark" class="text" />
    <INPUT TYPE='BUTTON' VALUE='Cancel' ONCLICK='history.go(-1)'>
    ${h.submit('submit', 'Save')}
</div>

${h.end_form()}

<div id='preview' name='preview'></div>
