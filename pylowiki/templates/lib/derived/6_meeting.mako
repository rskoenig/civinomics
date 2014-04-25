<%!
    import pylowiki.lib.db.user         as userLib
    import pylowiki.lib.db.workshop     as workshopLib
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

<%def name="showInfo()">
    <div class="row-fluid">
        <h3>${c.meeting['title']}</h3>
    </div><!-- row-fluid -->
    <div class="row-fluid">
        <ul>
        <li>Who is meeting: ${c.meeting['group']}</li>
        <li>Location: ${c.meeting['location']}</li>
        <li>Meeting Date: ${c.meeting['meetingDate']}</li>
        % if c.meeting['agendaPostDate'] != '0000-00-00':
            <li>Date Agenda Is Posted: ${c.meeting['agendaPostDate']}</li>
        % endif
        </ul>
    </div><!-- row-fluid -->
    
    <div class="row-fluid">
        ${m.html(c.meeting['text'], render_flags=m.HTML_SKIP_HTML) | n}
    </div><!-- row-fluid -->
    
    <div class="row-fluid">
        <span class="grey">Posted by: </span>
        ${lib_6.userImage(author, className="avatar small-avatar")} ${lib_6.userLink(author)}
    </div><!-- row-fluid -->
</%def>

<%def name="editMeeting()">
    <% 
        tagList = workshopLib.getWorkshopTagCategories()
        postalCodeSelected = ""
        citySelected = ""
        countySelected = ""
        if c.meeting:
            mScope = c.meeting['scope']
            title = c.meeting['title']
            group = c.meeting['group']
            tag = c.meeting['tag']
            text = c.meeting['text']
            location = c.meeting['location']
            meetingDate = c.meeting['meetingDate']
            meetingTime = c.meeting['meetingTime']
            agendaPostDate = c.meeting['agendaPostDate']
        else:
            mScope = "0|0|0|0|0|0|0|0|0|0"
            title = ""
            group = ""
            tag = ""
            text = ""
            location = ""
            meetingDate = ""
            meetingTime = ""
            agendaPostDate = ""
            
        scopeList = mScope.split('|')
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
    <div class="row-fluid>
        <div class="span12">
            % if c.editMeeting:
                <form method="POST" name="edit_meeting" id="edit_meeting" action="/meeting/${c.meeting['urlCode']}/${c.meeting['url']}/meetingEditHandler">
            % else:
                <form method="POST" name="edit_meeting" id="edit_meeting" action="/meeting/${c.authuser['urlCode']}/${c.authuser['url']}/meetingNewHandler">
            % endif
            <div class="row-fluid">
                <h3>Meeting Information</h3>
            </div><!-- row-fluid -->
            <br>
            
            <div class="row-fluid">
                <div class="span6">
                    <label for="title" class="control-label" required><strong>Meeting Title:</strong></label>
                    <input type="text" name="meetingTitle" class="span12" value="${title}" required>
                </div><!-- span6 -->
                <div class="span6">
                    <div class="alert alert-info">
                        Keep it short and descriptive.
                    </div><!-- alert -->
                </div><!-- span6 -->
            </div><!-- row-fluid -->
            
            <div class="row-fluid">
                <div class="span6">
                    <label for="title" class="control-label" required><strong>Meeting Date:</strong></label>
                    <input type="text" name="meetingDate" id="meetingDate" class="span6" value="${meetingDate}" required>
                </div><!-- span6 -->
                <div class="span6">
                    <div class="alert alert-info">
                        Date of meeting.
                    </div><!-- alert -->
                </div><!-- span6 -->
            </div><!-- row-fluid -->
            
            <div class="row-fluid">
                <div class="span6">
                    <label for="meetingTime" class="control-label" required><strong>Meeting Time:</strong></label>
                    <input type="text" name="meetingTime" class="span6" value="${meetingTime}" required>
                </div><!-- span6 -->
                <div class="span6">
                    <div class="alert alert-info">
                        Time of meeting.
                    </div><!-- alert -->
                </div><!-- span6 -->
            </div><!-- row-fluid -->
            
            <div class="row-fluid">
                <div class="span6">
                    <label for="title" class="control-label" required><strong>Name of group:</strong></label>
                    <input type="text" name="meetingGroup" class="span12" value="${group}" required>
                </div><!-- span6 -->
                <div class="span6">
                    <div class="alert alert-info">
                        The name of the group which is meeting.
                    </div><!-- alert -->
                </div><!-- span6 -->
            </div><!-- row-fluid -->
            
            <div class="row-fluid">
                <div class="span6">
                    <label for="title" class="control-label" required><strong>Meeting location:</strong></label>
                    <input type="text" name="meetingLocation" class="span12" value="${location}" required>
                </div><!-- span6 -->
                <div class="span6">
                    <div class="alert alert-info">
                        Where the meeting is to be held.
                    </div><!-- alert -->
                </div><!-- span6 -->
            </div><!-- row-fluid -->
            
            <div class="row-fluid">
                <div class="span6">
                    <label for="title" class="control-label" required><strong>Public Jurisdiction:</strong></label>
                    ${geoSelect()}
                </div><!-- span6 -->
                <div class="span6">
                    <div class="alert alert-info">
                        The region or legal jurisdiction associated with the meeting.
                    </div><!-- alert -->
                </div><!-- span6 -->
            </div><!-- row-fluid -->
            
            <div class="row-fluid">
                <div class="span6">
                    <label for="tag" class="control-label" required><strong>Meeting category:</strong></label>
                    <div class="span3"></div>
                    <div class="span8 no-left">
                        <select name="tag" id="tag">
                        % if (c.meeting and c.meeting['public'] == '0') or not c.meeting:
                            <option value="">Choose one</option>
                        % endif
                        % for mtag in tagList:
                            <% 
                                selected = ""
                                if tag == mtag:
                                    selected = "selected"
                            %>
                            <option value="${mtag}" ${selected}/> ${mtag}</option>
                        % endfor
                        </select>
                    </div><!-- span8 -->
                </div><!-- span6 -->
                <div class="span6">
                    <div class="alert alert-info">
                        The topic area associated with the meeting.
                    </div><!-- alert -->
                </div><!-- span6 -->
            </div><!-- row-fluid -->
            
            <div class="row-fluid">
                <div class="span3">
                    <label for="text" class="control-label" required><strong>Description:</strong></label>
                    ${lib_6.formattingGuide()}
                </div>
                <div class="span9">
                    <div class="alert alert-info">
                        A short description about the meeting.
                    </div>
                </div><!-- span6 -->
            </div><!-- row-fluid -->
            <textarea rows="10" id="meetingText" name="meetingText" class="span12" required>${text}</textarea>

            <button type="submit" class="btn btn-warning btn-large pull-right" name="submit_summary">Save Changes</button>
        </form>
        </div><!-- span12 -->
    </div><!-- row-fluid -->
</%def>

<%def name="itemEdit()">
    <%
        if not c.update:
            updateTitle = ""
            updateText = ""
            updateCode = "new"
        else:
            updateTitle = c.update['title']
            updateText = c.update['text']
            updateCode = c.update['urlCode']
            
    %>
    % if not c.update:
        <form id="addUpdateForm" name="addUpdateForm">
            <fieldset>
                <label>Progress Report Title</label><span class="help-block"> (Try to keep your title informative, but concise.) </span>
                <input type="text" class="input-block-level" name="title" ng-model="title" maxlength = "120" required>
                <span ng-show="addUpdateTitleShow"><div class="alert alert-danger" ng-cloak>{{addUpdateTitleResponse}}</div></span>
            </fieldset>
            <fieldset>
                <label><strong>Progress Report Text</strong>
                <a href="#" class="btn btn-mini btn-info" onclick="window.open('/help/markdown.html','popUpWindow','height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');"><i class="icon-list"></i> <i class="icon-photo"></i> View Formatting Guide</a></label>
                <textarea name="text" rows="3" class="input-block-level" ng-model="text" required></textarea>
                <span ng-show="addUpdateTextShow"><div class="alert alert-danger" ng-cloak>{{addUpdateTextResponse}}</div></span>
                <span class="help-block"> (A description of the progress made on implementing the initiative since the last progress report.) </span>
            </fieldset>
            <fieldset>
                <button class="btn btn-large btn-civ pull-right" type="submit" name="submit">Submit</button>
            </fieldset>
        </form>
    % endif
</%def>

<%def name="geoSelect()">
    <!-- need to get the c.initiative['scope'] and update the selects accordingly -->
    <% 
        countrySelected = ""
        countyMessage = ""
        cityMessage = ""
        postalMessage = ""
        underPostalMessage = ""
        if c.country!= "0":
            countrySelected = "selected"
            states = c.states
            countyMessage = "Leave 'State' blank if the meeting jurisdiction applies to the entire country."
        endif
    %>
    <div class="row-fluid"><span id="planetSelect">
        <div class="span3">Planet:</div>
        <div class="span8">
            <select name="geoTagPlanet" id="geoTagPlanet" class="geoTagCountry">
                <option value="0">Earth</option>
            </select>
        </div><!-- span8 -->
    </span><!-- countrySelect -->
    </div><!-- row-fluid -->     
    <div class="row-fluid"><span id="countrySelect">
        <div class="span3">Country:</div>
        <div class="span8">
            <select name="geoTagCountry" id="geoTagCountry" class="geoTagCountry">
                <option value="0">Select a country</option>
                <option value="United States" ${countrySelected}>United States</option>
            </select>
        </div><!-- span8 -->
    </span><!-- countrySelect -->
    </div><!-- row-fluid -->
    <div class="row-fluid"><span id="stateSelect">
        % if c.country != "0":
            <div class="span3">State:</div><div class="span8">
            <select name="geoTagState" id="geoTagState" class="geoTagState" onChange="geoTagStateChange(); return 1;">
            <option value="0">Select a state</option>
            % for state in states:
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
            </div><!-- span8 -->
        % else:
            Leave 'Country' blank if the meeting jurisdiction applies to the entire planet.
        % endif
    </span></div><!-- row-fluid -->
    <div class="row-fluid"><span id="countySelect">
        % if c.state != "0":
            <% counties = getCountyList("united-states", c.state) %>
            <% cityMessage = "Leave blank 'County' blank if the meeting jurisdiction applies to the entire state." %>
            <div class="span3">County:</div><div class="span8">
            <select name="geoTagCounty" id="geoTagCounty" class="geoTagCounty" onChange="geoTagCountyChange(); return 1;">
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
            </div><!-- span8 -->
        % else:
            <% cityMessage = "" %>
            ${countyMessage}
        % endif
    </span></div><!-- row -->
    <div class="row-fluid"><span id="citySelect">
        % if c.county != "0":
            <% cities = getCityList("united-states", c.state, c.county) %>
            <% postalMessage = "Leave 'City' blank if the meeting jurisdiction applies to the entire county." %>
            <div class="span3">City:</div><div class="span8">
            <select name="geoTagCity" id="geoTagCity" class="geoTagCity" onChange="geoTagCityChange(); return 1;">
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
            </div><!-- span8 -->
        % else:
            <% postalMessage = "" %>
            ${cityMessage}
        % endif
        </span></div><!-- row-fluid -->
    <div class="row-fluid"><span id="postalSelect">
        % if c.city != "0":
            <% postalCodes = getPostalList("united-states", c.state, c.county, c.city) %>
            <% underPostalMessage = "or leave blank if your the meeting jurisdiction is specific to the entire city." %>
            <div class="span3">Zip Code:</div><div class="span8">
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
            </div><!-- span8 -->
        % else:
            <% underPostalMessage = "" %>
            ${postalMessage}
        % endif
        </span></div><!-- row-fluid -->
    <div class="row-fluid"><span id="underPostal">${underPostalMessage}</span><br /></div><!-- row -->
    <br/>
</%def>

