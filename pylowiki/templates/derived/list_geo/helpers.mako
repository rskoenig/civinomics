<%!
   from pylons import request
%>
<%def name='show_geo()'>
    <table class="table">
    <body>
    <tr>
    <td>
    <ul class="unstyled">
    % if c.geoType == 'postal':
        <li><img src="${c.cityFlag}"> City is <a href="${c.cityLink}">${c.city}</a></li>
        <li><img src="${c.countyFlag}"> County is <a href="${c.countyLink}">${c.county}</a></li>
        <li><img src="${c.stateFlag}"> State is <a href="${c.stateLink}">${c.state}</a></li>
    % elif c.geoType == 'city':
        <li><img src="${c.cityFlag}"> City of ${c.city}</li>
        <li><img src="${c.countyFlag}"> County is <a href="${c.countyLink}">${c.county}</a></li>
        <li><img src="${c.stateFlag}"> State is <a href="${c.stateLink}">${c.state}</a></li>
    % elif c.geoType == 'county':
        <li><img src="${c.countyFlag}"> County of ${c.county}</li>
        <li><img src="${c.stateFlag}"> State is <a href="${c.stateLink}">${c.state}</a></li>
    % elif c.geoType == 'state':
        <li><img src="${c.stateFlag}"> State of ${c.state}</li>
    %endif
    </ul>
    </td>
    <td>
    <ul>
    <li>Population is ${c.population}</li>
    <li>Median Age is ${c.medianAge}</li>
    <li>Number of Households is ${c.numberHouseholds}</li>
    <li>Persons per Household is ${c.personsHousehold}</li>
    </td>
    </tr>
    </tbody>
    </table>
</%def>
