<%inherit file = '/base/template.html' />

<h1> Add an issue </h1>

${h.form(url(controller = 'addIssue', action = 'addIssue'), method = 'put')}
    Title <input type = 'text' id = 'issue_url' name = 'issue_url' class = 'text'placeholder = 'eg: Water Issues'>

<textarea rows = '50' id = 'textarea' name = 'textarea' onkeyup = "previewAjax('textarea', 'preview')" class = 'markitup'>${c.rST}</textarea>

<div align = 'right'>
    <span style = 'float:left;'>You should <a href = '#preview'>preview below</a> before saving.</span>
    Optional remark: <input type = 'text' id = 'remark' name = 'remark' class = 'text' placeholder = 'optional remark' />
    <input type = 'text' id = 'sremark' name = 'sremark' class = 'text' />
    <INPUT TYPE = 'BUTTON' VALUE = 'Cancel' ONCLICK = 'history.go(-1)'>
    ${h.submit('submit', 'Save')}
</div>

${h.end_form()}

<div id = 'preview' name = 'preview'></div>

<%def name = 'extraStyles()'>
    <link type = 'text/css' rel = 'stylesheet' href = '${h.url_for('/styles/stylePylo.css')}' />
</%def>

<%def name = 'extraScripts()'>
    <script src = "${h.url_for('/js/markitup/jquery.markitup.js')}" type = "text/javascript"></script>
    <script src = "${h.url_for('/js/javascript.js')}" type = "text/javascript"></script>

    <script language="javascript">
        $(document).ready(function()    {
            $('.markitup').markItUp(mySettings);
        });
    </script>
</%def>

<%def name = 'extraHTML()'>
    ##do nothing
</%def>
