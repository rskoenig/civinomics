<%!
    import pylowiki.lib.db.user         as userLib
    import pylowiki.lib.db.tag          as tagLib
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

<%def name="showInfo(meeting, author)">
    <% scopeInfo = utils.getPublicScope(c.meeting['scope']) %>
    <div class="row-fluid">
        <h3>${meeting['title']}</h3>
        <img src="${scopeInfo['flag']}" width="60" height="60"> ${scopeInfo['level']} of ${scopeInfo['name']}
    </div><!-- row-fluid -->
    <div class="spacer"></div>
    <div class="row-fluid"><div class="span2 text-right">Who is meeting:</div><div class="span9 text-left">${meeting['group']}</div></div>
    <div class="row-fluid"><div class="span2 text-right">Location:</div><div class="span9 text-left">${meeting['location']}</div></div>
    <div class="row-fluid"><div class="span2 text-right">Meeting Date:</div><div class="span9 text-left">${meeting['meetingDate']}</div></div>
    <div class="row-fluid"><div class="span2 text-right">Meeting Time:</div><div class="span9 text-left">${meeting['meetingTime']}</div></div>
    <div class="row-fluid"><div class="span2 text-right">Meeting Category:</div><div class="span9 text-left">${meeting['tag']}</div></div>
    % if meeting['agendaPostDate'] != '':
        <div class="row-fluid"><div class="span2 text-right">Date Agenda Is Posted:</div><div class="span9 text-left">${meeting['agendaPostDate']}</div>
    % endif

    
    <div class="row-fluid">
        <div class="span9">
            ${m.html(meeting['text'], render_flags=m.HTML_SKIP_HTML) | n}
        </div>
    </div><!-- row-fluid -->
    
    <div class="row-fluid">
        <span class="grey">Posted by: </span>
        ${lib_6.userImage(author, className="avatar small-avatar")} ${lib_6.userLink(author)}
    </div><!-- row-fluid -->
    % if c.meeting.objType == 'revision':
        <div class="alert alert-error">
            This is a revision dated ${c.meeting.date}
        </div>
    % endif
</%def>


<%def name="editMeeting()">
    <% 
        tagList = tagLib.getTagCategories()
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
            public = c.meeting['public']
            if public == 'on':
                publicChecked = 'checked'
            else:
                publicChecked = ""
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
            public = ""
            publicChecked = ""
            
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
                    <label for="title" class="control-label" required><strong>Agenda Post Date:</strong></label>
                    <input type="text" name="agendaPostDate" id="agendaPostDate" class="span6" value="${agendaPostDate}">
                </div><!-- span6 -->
                <div class="span6">
                    <div class="alert alert-info">
                        Date the meeting agenda will be posted for this meeting.
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
            
            <div class="row-fluid spacer">
                <div class="span6">
                    <label for="scope" class="control-label" required><strong>Public Jurisdiction:</strong></label>
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
            
            <div class="row-fluid spacer">
                <div class="span6">
                    <label for="text" class="control-label" required><strong>Description:</strong></label>
                    ${lib_6.formattingGuide()}
                </div>
                <div class="span6">
                    <div class="alert alert-info">
                        A short description about the meeting.
                    </div>
                </div><!-- span6 -->
            </div><!-- row-fluid -->
            <textarea rows="10" id="meetingText" name="meetingText" class="span12" required>${text}</textarea>
            
            <div class="row-fluid spacer">
                <div class="span6">            
                    <input type="checkbox" name="public" ${publicChecked}> Publish this meeting
                </div><!-- span6 -->
                <div class="span6">
                    <div class="alert alert-info">
                        Makes the meeting viewable by members and the public, with members able to comment and vote (where set).
                    </div><!-- alert -->
                </div><!-- span6 -->
            </div><!-- row-fluid -->

            <button type="submit" class="btn btn-warning btn-large pull-right" name="submit_summary">Save Changes</button>
        </form>
        </div><!-- span12 -->
    </div><!-- row-fluid -->
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

<%def name="addAgendaItem(meeting, author)">
    % if 'user' in session and (c.authuser['email'] == author['email'] or userLib.isAdmin(c.authuser.id)):
        <div class="row-fluid">
            <button type="button" class="btn btn-success" data-toggle="collapse" data-target="#addItem"><i class="icon icon-white icon-plus"></i> Agenda Item</button>
            <div id="addItem" class="collapse">
                <form action="/meeting/${meeting['urlCode']}/${meeting['url']}/meetingAgendaItemAddHandler" method="POST">
                    <fieldset>
                        <label>Item Title</label>
                        <input type="text" name="agendaItemTitle" class="span6" required>
                        <label>Item Text</label>
                        ${lib_6.formattingGuide()}<br>
                        <textarea rows="3" name="agendaItemText" class="span6" required></textarea>
                        <label class="checkbox">
                        <input type="checkbox" name="agendaItemVote" checked> People can vote on this
                        </label>
                        <label class="checkbox">
                        <input type="checkbox" name="agendaItemComment" checked> People can comment on this
                        </label>
                        <button class="btn btn-success" type="submit" class="btn">Save Item</button>
                        <button class="btn btn-danger" type="reset" value="Reset">Cancel</button>
                    </fieldset>
                </form>
            </div>
        </div><!-- row-fluid -->
    % endif
</%def>

<%def name="meetingModeration(thing)">
    <%
        if 'user' not in session or thing.objType == 'revision' or c.privs['provisional']:
            return
        adminID = 'admin-%s' % thing['urlCode']
        publishID = 'publish-%s' % thing['urlCode']
        unpublishID = 'unpublish-%s' % thing['urlCode']
    %>
    <div class="btn-group">
        % if (c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id)) and thing.objType != 'meetingUnpublished':
            <a href="/meeting/${thing['urlCode']}/${thing['url']}/meetingEdit" class="btn btn-mini">Edit</a>
            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${unpublishID}">trash</a>
        % elif thing.objType == 'meetingUnpublished' and thing['unpublished_by'] != 'parent':
            % if thing['unpublished_by'] == 'admin' and userLib.isAdmin(c.authuser.id):
                <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${publishID}">publish</a>
            % elif thing['unpublished_by'] == 'owner' and c.authuser.id == thing.owner:
                <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${publishID}">publish</a>
            % endif
        % endif
        % if c.revisions:
            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#revisions">revisions (${len(c.revisions)})</a>
        % endif

        % if userLib.isAdmin(c.authuser.id):
            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${adminID}">admin</a>
        % endif
    </div>
    
    % if thing['disabled'] == '0':
        % if (c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id)):
            % if thing.objType == 'meetingUnpublished':
                ${lib_6.publishThing(thing)}
            % else:
                ${lib_6.unpublishThing(thing)}
            % endif
            % if userLib.isAdmin(c.authuser.id):
                ${lib_6.adminThing(thing)}
            % endif
        % endif
    % else:
        % if userLib.isAdmin(c.authuser.id):
            ${lib_6.adminThing(thing)}
        % endif
    % endif
    % if c.revisions:
        <div id="revisions" class="collapse">
            <ul class="unstyled">
            % for revision in c.revisions:
                <li>Revision: <a href="/meeting/${revision['urlCode']}/${revision['url']}/show">${revision.date}</a></li>
            % endfor
            </ul>
        </div>
    % endif
</%def>
