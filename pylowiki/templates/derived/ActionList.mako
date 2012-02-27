##<%inherit file="/base/base.mako"/>
<%inherit file="/base/template.html"/>
<h1> ${c.heading} </h1>

Results: ${c.count}

<br > <br>

<table width='100%'>
   
<% state = True %>

% for p in c.paginator:

    <% state = not state %>
    
    <tr class="list ${state}">
	
    <% url = p.url %>

	    <td width="100%"> <a href='/issue/${url}'> ${url} </a> </td>
            <td > <a href="/${c.action}/${url}"> ${c.action} </a> </td>

    </tr>

% endfor

</table>

<br />

<div style="text-align: center;">${ c.paginator.pager('~3~') }</div>


<%def name = 'extraStyles()'>

</%def>

<%def name = 'extraScripts()'>

</%def>

<%def name = 'extraHTML()'>

</%def>
