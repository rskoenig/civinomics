<%inherit file="/base/base.mako"/>

<h2>${c.heading}</h2>

${h.form(h.url( controller="search", action="handler"), method='put')}

<input type="text" id="needle"  name="needle" /> 
${h.submit('submit', 'Search')}

${h.end_form()}
