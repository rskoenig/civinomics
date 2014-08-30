<%!
    import pylowiki.lib.db.user         as userLib
    import pylowiki.lib.db.generic      as genericLib
    import pylowiki.lib.utils           as utils
    import misaka as m

    import locale
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')
    
    import logging
    log = logging.getLogger(__name__)

    from pylowiki.lib.db.geoInfo import getGeoTitles, getStateList, getCountyList, getCityList, getPostalList
%>

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="showInfo(listener, scopeInfo)">
    <div class="spacer"></div>
    <div class="page-header">
        <h2>${c.listener['name']}</h2>
        <p>${c.listener['title']}</p>
        <img src="${scopeInfo['flag']}" class="thumbnail small-flag tight"> ${scopeInfo['level']} of ${scopeInfo['name']}
    </div>
    <table class="info-table">
        % if 'group' in c.listener and c.listener['group'] != '':
            <tr>
                <td class="left">Group:</td>
                <td class="right">${c.listener['group']}</td>
            </tr>
        % endif
        % if 'lurl' in c.listener and c.listener['lurl'] != '':
            <tr>
                <td class="left">Web Site</td>
                <td class="right"><a href="${c.listener['lurl']}" target="_blank">${c.listener['lurl']}</a></td>
            </tr>
        % endif
        % if 'text' in c.listener and c.listener['text'] != '':
            <tr>
                <td colspan=2>
                    ${m.html(c.listener['text'], render_flags=m.HTML_SKIP_HTML) | n}
                </td>
            </tr>
        % endif
        % if 'term_end' in c.listener and c.listener['term_end'] != '':
            <tr>
                <td class="left">Term Ends:</td>
                <td class="right">${c.listener['term_end']}</td>
            </tr>
        % endif
    </table>
    % if 'views' in c.listener:
        <i class="icon-eye-open"></i> Views (${c.listener['views']})
    % endif
    % if listener.objType == 'revision':
        <div class="alert alert-error">
            This is a revision dated ${listener.date}
        </div>
    % endif
</%def>


<%def name="editListener()">
    <% 
        postalCodeSelected = ""
        citySelected = ""
        countySelected = ""
        if c.listener:
            scope = c.listener['scope']
            name = c.listener['name']
            title = c.listener['title']
            group = c.listener['group']
            text = c.listener['text']
            email = c.listener['email']
            lurl = c.listener['lurl']
            termEnd = c.listener['term_end']

        else:
            scope = "0|0|0|0|0|0|0|0|0|0"
            name = ""
            title = ""
            group = ""
            text = ""
            email = ""
            lurl = ""
            termEnd = ""
            
        scopeList = scope.split('|')
        if scopeList[9] == '0' and scopeList[8] == '0':
            countySelected = "selected"
        elif scopeList[9] == '0' and scopeList[8] != '0':
            citySelected = "selected"
        else:
            postalCodeSelected = "selected"

    %>
    % if c.saveMessage and c.saveMessage != '':
        <div class="alert ${c.saveMessageClass}">
        <button type="button" class="close" data-dismiss="alert">&times;</button>
        ${c.saveMessage}
        </div>
    % endif
    <div class="row>
        <div class="col-sm-12">
            % if c.listener:
                <form method="POST" name="edit_listener" id="edit_listener" action="/listener/${c.listener['urlCode']}/listenerEditHandler">
            % else:
                <form method="POST" name="edit_listener" id="edit_listener" action="/listener/new/listenerEditHandler">
            % endif
            <div class="row">
                <h3>Listener Information</h3>
            </div><!-- row -->
            <br>
            
            <div class="row">
                <div class="col-sm-6">
                    <label for="title" class="control-label" required><strong>Listener Name:</strong></label>
                    <input type="text" name="listenerName" class="col-sm-12 form-control" value="${name}" required>
                </div><!-- col-sm-6 -->
                <div class="col-sm-6">
                    <div class="alert alert-info">
                        Keep it short and descriptive.
                    </div><!-- alert -->
                </div><!-- col-sm-6 -->
            </div><!-- row -->
            
            <div class="row">
                <div class="col-sm-6">
                    <label for="title" class="control-label" required><strong>Listener Title:</strong></label>
                    <input type="text" name="listenerTitle" class="col-sm-12 form-control" value="${title}" required>
                </div><!-- col-sm-6 -->
                <div class="col-sm-6">
                    <div class="alert alert-info">
                        Keep it short and descriptive.
                    </div><!-- alert -->
                </div><!-- col-sm-6 -->
            </div><!-- row -->
            
            <div class="row">
                <div class="col-sm-6">
                    <label for="title" class="control-label" required><strong>Listener Email:</strong></label>
                    <input type="text" name="listenerEmail" class="col-sm-12 form-control" value="${email}" required>
                </div><!-- col-sm-6 -->
                <div class="col-sm-6">
                    <div class="alert alert-info">
                        This needs to be a valid email address.
                    </div><!-- alert -->
                </div><!-- col-sm-6 -->
            </div><!-- row -->
            
            <div class="row">
                <div class="col-sm-6">
                    <label for="title" class="control-label" required><strong>Name of group:</strong></label>
                    <input type="text" name="listenerGroup" class="col-sm-12 form-control" value="${group}" required>
                </div><!-- col-sm-6 -->
                <div class="col-sm-6">
                    <div class="alert alert-info">
                        The name of the listener group or organization.
                    </div><!-- alert -->
                </div><!-- col-sm-6 -->
            </div><!-- row -->
            
            <div class="row">
                <div class="col-sm-6">
                    <label for="title" class="control-label" required><strong>URL of web site:</strong></label>
                    <input type="text" name="listenerURL" class="col-sm-12 form-control" value="${lurl}">
                </div><!-- col-sm-6 -->
                <div class="col-sm-6">
                    <div class="alert alert-info">
                        A web site with more information about the listener.
                    </div><!-- alert -->
                </div><!-- col-sm-6 -->
            </div><!-- row -->
            
            <div class="row spacer">
                <div class="col-sm-6">
                    <label for="scope" class="control-label" required><strong>Public Jurisdiction:</strong></label>
                    ${geoSelect()}
                </div><!-- col-sm-6 -->
                <div class="col-sm-6">
                    <div class="alert alert-info">
                        The region or legal jurisdiction associated with the listener.
                    </div><!-- alert -->
                </div><!-- col-sm-6 -->
            </div><!-- row -->
            
            <div class="row spacer">
                <div class="col-sm-6">
                    <label for="title" class="control-label" required><strong>Term End Date:</strong></label>
                    <input type="text" name="termEnd" id="termEnd" class="col-sm-6 form-control" value="${termEnd}">
                </div><!-- col-sm-6 -->
                <div class="col-sm-6">
                    <div class="alert alert-info">
                        Date term ends for this listener.
                    </div><!-- alert -->
                </div><!-- col-sm-6 -->
            </div><!-- row -->
            
            
            <div class="row spacer">
                <div class="col-sm-6">
                    <label for="text" class="control-label" required><strong>Listener Description:</strong></label>
                    ${lib_6.formattingGuide()}
                </div>
                <div class="col-sm-6">
                    <div class="alert alert-info">
                        A short description of the listener.
                    </div>
                </div><!-- col-sm-6 -->
            </div><!-- row -->
            <textarea rows="10" id="meetingText" name="listenerText" class="col-sm-12 form-control">${text}</textarea>
            

            <button type="submit" class="btn btn-warning btn-large pull-right" name="submit_summary">Save Changes</button>
        </form>
        </div><!-- col-sm-12 -->
    </div><!-- row -->
</%def>

<%def name="geoSelect()">
    <% 
        countrySelected = ""
        countyMessage = ""
        cityMessage = ""
        postalMessage = ""
        underPostalMessage = ""
        if c.country!= "0":
            countrySelected = "selected"
            states = c.states
            countyMessage = "Leave 'State' blank if the listener jurisdiction applies to the entire country."
        endif
    %>
    <div class="row"><span id="planetSelect">
        <div class="col-sm-3">Planet:</div>
        <div class="col-sm-8">
            <input type="hidden" name="geoTagPlanet" value="Earth">
            Earth
        </div><!-- col-sm-8 -->
    </span><!-- countrySelect -->
    </div><!-- row -->     
    <div class="row"><span id="countrySelect">
        <div class="col-sm-3">Country:</div>
        <div class="col-sm-8">
            <input type="hidden" name="geoTagCountry" value="United States">
            United States
        </div><!-- col-sm-8 -->
    </span><!-- countrySelect -->
    </div><!-- row -->
    <div class="row"><span id="stateSelect">
        % if c.country != "0":
            <div class="col-sm-3">State:</div>
            <div class="col-sm-8">
            
            <% 
                if c.state != "0" and 'curateLevel' in c.authuser and int(c.authuser['curateLevel']) >= 4:
                    disabled = "disabled"
                    fieldName = "geoTagStateDisabled"
                else:
                    disabled = ""
                    fieldName = "geoTagState"
            %>
            % if disabled == "disabled":
                <input type=hidden name="geoTagState" value="${c.state}">
            % endif
            <select name="${fieldName}" id="geoTagState" class="geoTagState" ${disabled} onChange="geoTagStateChange(); return 1;">
                <option value="0">Select a state</option>
                % for state in c.states:
                    % if state != 'District of Columbia':
                        % if c.state == state['StateFullName']:
                            <% stateSelected = "selected" %>
                        % else:
                            <% stateSelected = "" %>
                        % endif
                        <option value="${state['StateFullName']}" ${stateSelected}>${state['StateFullName']}</option>
                    % endif
                % endfor
                </select>
            </div><!-- col-sm-8 -->
        % else:
            Leave 'Country' blank if the listener jurisdiction applies to the entire planet.
        % endif
    </span></div><!-- row -->
    <div class="row"><span id="countySelect">
        % if c.state != "0":
            <% counties = getCountyList("united-states", c.state) %>
            <% cityMessage = "Leave blank 'County' blank if the listener jurisdiction applies to the entire state." %>
            <div class="col-sm-3">County:</div>
            <div class="col-sm-8">
                <% 
                    if c.county != "0" and 'curateLevel' in c.authuser and int(c.authuser['curateLevel']) >= 6:
                        disabled = "disabled"
                        fieldName = "geoTagCountyDisabled"
                    else:
                        disabled = ""
                        fieldName = "geoTagCounty"
                %>
                % if disabled == "disabled":
                    <input type=hidden name="geoTagCounty" value="${c.county}">
                % endif
                <select name="${fieldName}" id="geoTagCounty" class="geoTagCounty" ${disabled} onChange="geoTagCountyChange(); return 1;">
                    <option value="0">Select a county</option>
                    % for county in counties:
                        % if c.county == county['County'].title():
                            <% countySelected = "selected" %>
                        % else:
                            <% countySelected = "" %>
                        % endif
                        <option value="${county['County'].title()}" ${countySelected}>${county['County'].title()}</option>
                    % endfor
                </select>
            </div><!-- col-sm-8 -->
        % else:
            <% cityMessage = "" %>
            ${countyMessage}
        % endif
    </span></div><!-- row -->
    <div class="row"><span id="citySelect">
        % if c.county != "0":
            <% cities = getCityList("united-states", c.state, c.county) %>
            <% postalMessage = "Leave 'City' blank if the listener jurisdiction applies to the entire county." %>
            <div class="col-sm-3">City:</div>
            <div class="col-sm-8">
                <% 
                    if c.city != "0" and 'curateLevel' in c.authuser and int(c.authuser['curateLevel']) >= 8:
                        disabled = "disabled"
                        fieldName = "geoTagCityDisabled"
                    else:
                        disabled = ""
                        fieldName = "geoTagCity"
                %>
                % if disabled == "disabled":
                    <input type=hidden name="geoTagCounty" value="${c.city}">
                % endif
                <select name="${fieldName}" id="geoTagCity" class="geoTagCity" ${disabled} onChange="geoTagCityChange(); return 1;">
                <option value="0">Select a city</option>
                    % for city in cities:
                        % if c.city == city['City'].title():
                            <% citySelected = "selected" %>
                        % else:
                            <% citySelected = "" %>
                        % endif
                        <option value="${city['City'].title()}" ${citySelected}>${city['City'].title()}</option>
                    % endfor
                </select>
            </div><!-- col-sm-8 -->
        % else:
            <% postalMessage = "" %>
            ${cityMessage}
        % endif
        </span></div><!-- row -->
    <div class="row"><span id="postalSelect">
        % if c.city != "0":
            <% postalCodes = getPostalList("united-states", c.state, c.county, c.city) %>
            <% underPostalMessage = "or leave blank if the listener jurisdiction is specific to the entire city." %>
            <div class="col-sm-3">Zip Code:</div><div class="col-sm-8">
            <select name="geoTagPostal" id="geoTagPostal" class="geoTagPostal" onChange="geoTagPostalChange(); return 1;">
            <option value="0">Select a zip code</option>
                % for pCode in postalCodes:
                    % if c.postal == str(pCode['ZipCode']):
                        <% postalSelected = "selected" %>
                    % else:
                        <% postalSelected = "" %>
                    % endif
                    <option value="${pCode['ZipCode']}" ${postalSelected}>${pCode['ZipCode']}</option>
                % endfor
            </select>
            </div><!-- col-sm-8 -->
        % else:
            <% underPostalMessage = "" %>
            ${postalMessage}
        % endif
        </span></div><!-- row -->
    <div class="row"><span id="underPostal">${underPostalMessage}</span><br /></div><!-- row -->
    <br/>
</%def>

<%def name="listenerModeration(thing)">
    <%
        if 'user' not in session or thing.objType == 'revision':
            return
        adminID = 'admin-%s' % thing['urlCode']
        publishID = 'publish-%s' % thing['urlCode']
        unpublishID = 'unpublish-%s' % thing['urlCode']
    %>
    <div class="btn-group btn-group-sm pull-left">
        % if (c.curator or userLib.isAdmin(c.authuser.id)) and thing.objType != 'listenerUnpublished':
            <a href="/listener/${thing['urlCode']}/listenerEdit" class="btn btn-default">Edit</a>
            <a class="btn btn-default accordion-toggle" data-toggle="collapse" data-target="#${unpublishID}">Trash</a>
        % elif thing.objType == 'listenerUnpublished' and thing['unpublished_by'] != 'parent':
            % if thing['unpublished_by'] == 'admin' and userLib.isAdmin(c.authuser.id):
                <a class="btn btn-xs accordion-toggle" data-toggle="collapse" data-target="#${publishID}">Publish</a>
            % elif thing['unpublished_by'] == 'owner' and c.authuser.id == thing.owner:
                <a class="btn btn-default accordion-toggle" data-toggle="collapse" data-target="#${publishID}">Publish</a>
            % endif
        % endif
        % if c.revisions:
            <a class="btn btn-default accordion-toggle" data-toggle="collapse" data-target="#revisions">Revisions (${len(c.revisions)})</a>
        % endif

        % if userLib.isAdmin(c.authuser.id):
            <a class="btn btn-default accordion-toggle" data-toggle="collapse" data-target="#${adminID}">Admin</a>
        % endif
    </div>
    
    % if thing['disabled'] == '0':
        % if (c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id)):
            % if thing.objType == 'listenerUnpublished':
                ${lib_6.publishThing(thing)}
            % else:
                ${lib_6.unpublishThing(thing)}
            % endif
        % endif
    % endif
    % if c.revisions:
        <div id="revisions" class="collapse">
            <ul class="unstyled">
            % for revision in c.revisions:
                <li>Revision: <a href="/listener/${revision['urlCode']}/show">${revision.date}</a></li>
            % endfor
            </ul>
        </div>
    % endif
</%def>
