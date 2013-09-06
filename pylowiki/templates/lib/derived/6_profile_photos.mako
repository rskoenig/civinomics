<%!
    import pylowiki.lib.db.workshop     as workshopLib
    import pylowiki.lib.db.facilitator  as facilitatorLib
    import pylowiki.lib.db.listener     as listenerLib
    import pylowiki.lib.db.follow       as followLib
    import pylowiki.lib.db.user         as userLib
    import pylowiki.lib.db.pmember      as pmemberLib
    import pylowiki.lib.db.photo        as photoLib
    import pylowiki.lib.db.event        as eventLib
    import pylowiki.lib.utils           as utils
    import pylowiki.lib.db.geoInfo      as geoLib
%>

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="editPhoto()">
    <div class="row-fluid">
        <div class="span8">
            % if not c.photo:
                <a data-ng-href="{{file.url}}" title="{{file.name}}" data-gallery="gallery" download="{{file.name}}"><img data-ng-src="{{file.thumbnail_url}}"></a>
                <br />1/3 size thumbnail
                <div class="spacer"></div>
            % endif
            <fieldset>
            <label for="title" class="control-label" required>Title:</label>
            <input type="text" name="title" value="${c.title}">
            <label for="description" class="control-label" required>Description:</label>
            <textarea name="description">${c.description}</textarea>

            <label for="scope" class="control-label" required>Where was picture taken:</label>
            <% 
                countyMessage = ""
                cityMessage = ""
                postalMessage = ""
                underPostalMessage = ""
            %>
            <div class="row-fluid"><span id="countrySelect">
                <div class="span1"></div>
                <div class="span2">Country:</div>
                <div class="span9">
                    <select name="geoTagCountry" id="geoTagCountry" class="geoTagCountry" onChange="geoTagCountryChange(); return 1;">
                    <option value="0" selected>Select a country</option>
                    % if c.country == '0':
                        <option value="United States">United States</option>
                    % else:
                        <option value="United States" selected>United States</option>
                    % endif
                    </select>
                </div><!-- span9 -->
                </span><!-- countrySelect -->
            </div><!-- row-fluid -->
            <div class="row-fluid"><span id="stateSelect">
                % if c.country != "0":
                    <% states = geoLib.getStateList(c.country) %>
                    <div class="span1"></div>
                    <div class="span2">State:</div>
                    <div class="span9">
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
                    </div><!-- span9 -->
                % else:
                    or leave blank if your photo is specific to the entire planet.
                % endif
            </span></div><!-- row-fluid -->
            <div class="row-fluid"><span id="countySelect">
                % if c.state != "0":
                    <% counties = geoLib.getCountyList("united-states", c.state) %>
                    <% cityMessage = "or leave blank if your photo is specific to the entire state." %>
                    <div class="span1"></div>
                    <div class="span2">County:</div>
                    <div class="span9">
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
                    </div><!-- span9 -->
                % else:
                    <% cityMessage = "" %>
                    ${countyMessage}
                % endif
            </span></div><!-- row -->
            <div class="row-fluid"><span id="citySelect">
                % if c.county != "0":
                    <% cities = geoLib.getCityList("united-states", c.state, c.county) %>
                    <% postalMessage = "or leave blank if your photo is specific to the entire county." %>
                    <div class="span1"></div>
                    <div class="span2">City:</div>
                    <div class="span9">
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
                    </div><!-- span9 -->
                % else:
                    <% postalMessage = "" %>
                    ${cityMessage}
                % endif
            </span></div><!-- row-fluid -->
            <div class="row-fluid"><span id="postalSelect">
                % if c.city != "0":
                    <% postalCodes = geoLib.getPostalList("united-states", c.state, c.county, c.city) %>
                    <% underPostalMessage = "or leave blank if your photo is specific to the entire city." %>
                    <div class="span1"></div>
                    <div class="span2">Postal Code:</div>
                    <div class="span9">
                        <select name="geoTagPostal" id="geoTagPostal" class="geoTagPostal">
                        <option value="0">Select a postal code</option>
                        % for pCode in postalCodes:
                            % if c.postal == str(pCode['ZipCode']):
                                <% postalSelected = "selected" %>
                            % else:
                                <% postalSelected = "" %>
                            % endif
                            <option value="${pCode['ZipCode']}" ${postalSelected}>${pCode['ZipCode']}</option>
                        % endfor
                        </select>
                    </div><!-- span9 -->
                % else:
                    <% underPostalMessage = "" %>
                    ${postalMessage}
                % endif
            </span></div><!-- row-fluid -->
            <div class="row-fluid">
                <span id="underPostal">${underPostalMessage}</span><br />
            </div><!-- row-fluid -->
        </fieldset>
        </div><!-- span8 -->
        <div class="span4">
            <% tagList = workshopLib.getWorkshopTagCategories() %>
            <fieldset>
            Category Tags
            % for tag in tagList:
                <label class="checkbox">
                % if tag in c.categories:
                    <input type="checkbox" name="categoryTags" value="${tag}" checked /> ${tag}
                % else:
                    <input type="checkbox" name="categoryTags" value="${tag}" /> ${tag}
                % endif
                </label>
            % endfor
            </fieldset>
        </div><!-- span4 -->
    </div><!-- row-fluid -->
</%def>

<%def name="uploadPhoto()">
    % if 'user' in session and (c.authuser.id == c.user.id):
        <form id="fileupload" action="/profile/${c.authuser['urlCode']}/${c.authuser['url']}/photo/upload/handler" method="POST" enctype="multipart/form-data" data-ng-app="demo" data-fileupload="options" ng-class="{true: 'fileupload-processing'}[!!processing() || loadingFiles]" class = "civAvatarUploadForm" ng-show="true">
            <div class="row-fluid fileupload-buttonbar">
                <div class="span10 offset1">
                    <!-- The fileinput-button span is used to style the file input field as button -->
                    <span class="pull-left">Document your community with pictures.  (5MB max, please)</span>
                    <span class="btn btn-success fileinput-button pull-right">
                        <i class="icon-plus icon-white"></i>
                        <span>Picture</span>
                        <input type="file" name="files[]">
                    </span>
                    <!-- The loading indicator is shown during file processing -->
                    <div class="fileupload-loading"></div>
                </div><!-- span10 -->
                <!-- The global progress information -->
            </div><!-- row-fluid -->
            <div class="row-fluid">
                <div class="span10 offset1 fade" data-ng-class="{true: 'in'}[!!active()]">
                    <!-- The global progress bar -->
                    <div class="progress progress-success progress-striped active" data-progress="progress()"><div class="bar" ng-style="{width: num + '%'}"></div></div>
                    <!-- The extended global progress information -->
                    <div class="progress-extended">&nbsp;</div>
                </div><!- span10 -->
            </div><!-- row-fluid -->
            <!-- The table listing the files available for upload/download -->
            <table class="table table-striped files ng-cloak" data-toggle="modal-gallery" data-target="#modal-gallery">
                <tbody><tr data-ng-repeat="file in queue">
                    <td data-ng-switch="" on="!!file.thumbnail_url">
                        <div class="preview" data-ng-switch-when="true">
                            <script type="text/javascript">
                                function setAction(imageHash) {
                                    actionURL = "/profile/${c.user['urlCode']}/${c.user['url']}/photo/" + imageHash + "/update/handler";
                                    document.getElementById('fileupload').action = actionURL;
                                }
                            </script>
                            ${editPhoto()}
                            <div class="row-fluid">
                                <button class="btn btn-success" type="Submit" onClick="setAction('{{file.image_hash}}'); return 1;">Submit</button>
                            </div><!-- row-fluid -->
                            </form>
                        </div><!-- preview -->
                        <div class="preview" data-ng-switch-default="" data-preview="file" id="preview"></div>
                    </td>
                    <td>
                        <div ng-show="file.error"><span class="label label-important">Error</span> {{file.error}}</div>
                    </td>
                    <td>
                        <button type="button" class="btn btn-primary start" data-ng-click="file.$submit()" data-ng-hide="!file.$submit">
                        <i class="icon-upload icon-white"></i>
                        <span>Save</span>
                        </button>
                        <button type="button" class="btn btn-warning cancel" data-ng-click="file.$cancel()" data-ng-hide="!file.$cancel">
                        <i class="icon-ban-circle icon-white"></i>
                        <span>Cancel</span>
                        </button>
                    </td>
                </tr>
            </tbody></table>
        </form>
    % endif
</%def>

<%def name="photoModerationPanel(thing)">
    <%
        if 'user' not in session or thing.objType == 'revision':
            return
        flagID = 'flag-%s' % thing['urlCode']
        editID = 'edit-%s' % thing['urlCode']
        adminID = 'admin-%s' % thing['urlCode']
        publishID = 'publish-%s' % thing['urlCode']
        unpublishID = 'unpublish-%s' % thing['urlCode']
    %>
    <div class="btn-group">
        % if thing['disabled'] == '0' and thing.objType != 'photoUnpublished':
            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${flagID}">flag</a>
        % endif
        % if (c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id)) and thing.objType != 'photoUnpublished':
            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${editID}">edit</a>>
        % endif
        % if (c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id)) and thing.objType != 'photoUnpublished':
            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${unpublishID}">unpublish</a>
        % elif (c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id)) and thing.objType == 'photoUnpublished':
            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${publishID}">publish</a>
        % endif
        % if userLib.isAdmin(c.authuser.id):
            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${adminID}">admin</a>
        % endif

    </div>
    
    % if thing['disabled'] == '0':
        % if thing.objType != 'photoUnpublished':
            ${lib_6.flagThing(thing)}
        % endif
        % if (c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id)):
            % if thing.objType != 'photoUnpublished':
                <% editID = 'edit-%s'%thing['urlCode'] %>
                <div class="row-fluid collapse" id="${editID}">
                    <div class="span11 offset1">
                        <div class="spacer"></div>
                        <form action="/profile/${c.user['urlCode']}/${c.user['url']}/photo/${c.photo['pictureHash_photos']}/update/handler" method="post" class="form">
                            ${self.editPhoto()}
                            <div class="row-fluid">
                                <button class="btn btn-success" type="Submit">Submit</button>
                            </div><!-- row-fluid -->
                        </form>
                    </div><!-- span11 -->
                </div><!-- row-fluid -->
            % endif
            % if thing.objType == 'photoUnpublished':
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
            <% editID = 'edit-%s'%thing['urlCode'] %>
            <div class="row-fluid collapse" id="${editID}">
                <div class="span11 offset1">
                    <div class="spacer"></div>
                    <form action="/profile/${c.user['urlCode']}/${c.user['url']}/photo/${c.photo['pictureHash_photos']}/update/handler" method="post" class="form">
                        ${self.editPhoto()}
                        <div class="row-fluid">
                            <button class="btn btn-success" type="Submit">Submit</button>
                        </div><!-- row-fluid -->
                    </form>
                </div><!-- span11 -->
            </div><!-- row-fluid -->
        % endif
        % if userLib.isAdmin(c.authuser.id):
            ${lib_6.adminThing(thing)}
        % endif
    % endif
</%def>

<%def name="showPhoto()">
    % if c.photo['deleted'] == '0':
        <div class="row-fluid">
            <div class="span8 offset2">
                <% imgSrc = "/images/photos/" + c.photo['directoryNum_photos'] + "/photo/" + c.photo['pictureHash_photos'] + ".png" %>
                <img src="${imgSrc}" class="wrap-photo"><br />
                <div class="spacer"></div>
                <div class="centered">
                    ${c.photo['title']}<br />
                </div><!-- centered -->
                <% tags = c.photo['tags'].split('|') %>
                Tags: 
                % for tag in tags:
                    % if tag != '':
                        <% 
                            tTitle = tag.title()
                        %>
                        <span class="label workshop-tag ${tag}">${tTitle}</span>
                    % endif
                % endfor
                <br />
                Added: ${c.photo.date}
                <br />
                Photo Location: ${photoLib.getPhotoLocation(c.photo)}<br />
                <div class="spacer"></div>
                ${c.photo['description']}
                <div class="spacer"></div>
            </div>
        </div>
    % else:
        <%
            event = eventLib.getEventsWithAction(c.photo, 'deleted')[0]
            deleter = userLib.getUserByID(event.owner)
            reason = event['reason']
        %>
        <div class="row-fluid">
            This picture deleted by ${deleter['name']} because: ${reason}
        </div><!-- row-fluid -->
    % endif
</%def>