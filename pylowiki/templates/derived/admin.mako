<%inherit file = "/base/template.html"/>

<h1>Add Mod</h1>
${ h.form( url( controller = 'admin', action ='addMod', id = 'email'), method='put' ) }
    Email: <input type="text" name = "email"/>
${h.end_form()}

<%def name = 'extraStyles()'>

</%def>

<%def name = 'extraScripts()'>

</%def>

<%def name = 'extraHTML()'>

</%def>