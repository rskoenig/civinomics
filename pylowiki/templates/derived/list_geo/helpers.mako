<%!
   from pylons import request
%>

<%def name='show_geo_info()'>
    <ul class="unstyled">
    <li>Population is ${c.population}</li>
    <li>Median Age is ${c.medianAge}</li>
    <li>Number of Households is ${c.numberHouseholds}</li>
    <li>Persons per Household is ${c.personsHousehold}</li>
    </ul>
</%def>

<%def name='show_geo()'>
    <div class="well">
    <table width="100%">
    <body>
    % if c.geoType == 'postal':
        <tr><td><img src="${c.cityFlag}" class="thumbnail"></td><td>City is <a href="${c.cityLink}">${c.city}</a></td><td rowspan=4>${show_geo_info()}</td><tr>
        <tr><td><img src="${c.countyFlag}" class="thumbnail"></td><td>County is <a href="${c.countyLink}">${c.county}</a></td></tr>
        <tr><td><img src="${c.stateFlag}" class="thumbnail"></td><td>State is <a href="${c.stateLink}">${c.state}</a></td></tr>
    % elif c.geoType == 'city':
        <tr><td><img src="${c.cityFlag}" class="thumbnail"></td><td>City of ${c.city}</td><td rowspan=3>${show_geo_info()}</td><tr>
        <tr><td><img src="${c.countyFlag}" class="thumbnail"></td><td>County is <a href="${c.countyLink}">${c.county}</a></td></tr>
        <tr><td><img src="${c.stateFlag}" class="thumbnail"></td><td>State is <a href="${c.stateLink}">${c.state}</a></td></tr>
    % elif c.geoType == 'county':
        <tr><td><img src="${c.countyFlag}" class="thumbnail"></td><td>County of ${c.county}</td><td rowspan=2>${show_geo_info()}</td></tr>
        <tr><td><img src="${c.stateFlag}" class="thumbnail"></td><td>State is <a href="${c.stateLink}">${c.state}</a></td></tr>
    % elif c.geoType == 'state':
        <tr><td><img src="${c.stateFlag}" class="thumbnail"></td><td>State of ${c.state}</td><td>${show_geo_info()}</td><tr>
    %endif
    </tbody>
    </table> 
    </div>
</%def>
