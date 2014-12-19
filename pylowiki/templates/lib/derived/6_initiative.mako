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
<%namespace name="ng_lib" file="/lib/ng_lib.mako" />
<%namespace file="/lib/derived/6_initiative_home.mako" name="ihelpers" />
<%namespace file="/lib/6_comments.mako" name="commentHelpers" />

<%def name="iMenu()">

    <div data-spy="affix" data-offset-top="350">
    % if c.iPrivs and c.editInitiative and c.initiative.objType != 'initiativeUnpublished':
        <ul class="nav nav-pills nav-stacked" style="width: 100%;">
            <li><a href="#info" role="tab" data-toggle="tab">Info</a></li>
            <li><a href="#photos" role="tab" data-toggle="tab">Photos</a></li>
            <li><a href="#users" role="tab" data-toggle="tab">Users</a></li>
            <li><a href="#reporting" role="tab" data-toggle="tab">Reporting</a></li>

            <!--
            <li><a href="#iStats" data-toggle="tab">Stats</a></li>
            <li><a href="#iUpdates" data-toggle="tab">Updates</a></li>
            <li><a href="#iPhotos" data-toggle="tab">Photos</a></li>
            -->
        </ul>
    % elif not (c.editUpdate or c.update or c.resource or c.editResource):
        <!-- direct linking to sections of the page not working due to angular '/' injection after '#' currently no menu visible on sub initiative pages-->
        <ul class="nav nav-pills nav-stacked i-menu" style="width: 100%;">
            <li><a ng-click="scrollTo('summary')">Info</a></li>
            <li><a ng-click="scrollTo('resources')">Resources</a></li>
            <li><a ng-click="scrollTo('updates')">Updates</a></li>
            <li><a ng-click="scrollTo('comments')">Comments</a></li>
        </ul>
    % endif
    </div>

</%def>

<%def name="iTags()">
    <h4> 
        <a href="${c.scopeHref}"><img class="thumbnail span flag small-flag border right-space" style="margin-bottom: 0;" src="${c.scopeFlag}"></a>
        ${lib_6.showTags(c.initiative)}
        %if 'subcategory_tags' in c.initiative:
        ${lib_6.showSubcategoryTags(c.initiative)}
        %endif
        % if 'workshopCode' in c.initiative and c.initiative['workshopCode']:
            <a class="no-highlight overlay parent-title" href="/workshop/${c.initiative['workshopCode']}/${c.initiative['workshop_url']}"> / ${c.initiative['workshop_title']}</a>
        % endif
        
    </h4>
</%def>

<%def name="iControlPanel()">
    <div class="i-control-panel">
        <div class="well initiative-well">
            <div class="row">
                <div class="col-xs-12">

                    % if c.initiative.objType == 'revision':
                        <div class="centered">
                            <a class="btn btn-default" href="/initiative/${c.initiative['initiativeCode']}/${c.initiative['initiative_url']}/show"><strong>View Current Version</strong></a>
                        </div>
                    % else:

                        % if c.initiative['public'] == '0' and c.iPrivs:
                            <form method="POST" name="publish" id="publish" action="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/edit">
                                <button type="submit" class="btn btn-lg btn-success btn-block" name="public" value="publish">Publish</button>
                            </form>
                            <div class="alert alert-warning top-space">
                                This initiative is not yet published. It does not show up in searches or public listings.
                            </div>
                        % elif c.initiative['public'] == '1' and c.iPrivs and c.editInitiative:
                            <form method="POST" name="publish" id="publish" action="/unpublish/initiative/${c.initiative['urlCode']}">
                                <button type="submit" class="btn btn-lg btn-warning btn-block" name="public" value="unpublish">Unpublish</button>
                            </form>
                            <div class="alert alert-warning top-space" style="margin-bottom: 0;">Unpublished initiatives don't show up in searches or public listings.</div>
                        % elif c.initiative['public'] == '1':

                            <a class="visible-xs-inline hidden-sm hidden-md hidden-lg" data-toggle="collapse" href="#iControlCollapse" aria-expanded="false" aria-controls="iControlCollapse"><h4 class="text-center">Vote and Comment</h4></a>

                            <div id="iControlCollapse" ng-class="{in: !xs}" class="panel-collapse collapse" role="tabpanel" aria-labelledby="iControlCollapse">
                                ${iControlPanelInner()}

                        % endif

                                <hr class="narrow">
                                <div class="centered">
                                    % if c.editInitiative:
                                        <a class="btn btn-default" target="civ-preview-${c.initiative['urlCode']}" href="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/show"><strong>View Initiative</strong></a>
                                    % elif c.iPrivs:
                                        <a class="btn btn-default" href="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/edit"><strong>Edit Initiative</strong></a>
                                        <a class="btn btn-default" href="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/updateEdit/new"><strong>Add Update</strong></a>
                                    % endif
                                    % if c.initiative['public'] == '1' and not c.editInitiative:
                                        ${ihelpers.watchButton(c.initiative)}
                                        <br>
                                        <span class="share-icon-group">    

                                            ${lib_6.facebookDialogShare2(shareOnWall=True, circle=True)}

                                            <!--
                                            <span class="icon-stack">
                                              <i class="icon-circle icon-stack-base twitter"></i>
                                              <i class="icon-twitter icon-light"></i>
                                            </span>
                                            -->

                                            % if not c.privs['provisional'] and c.initiative:
                                                <%
                                                    subj = 'Vote on "' + c.initiative['title'] + '"'
                                                    subj = subj.replace(' ','%20')
                                                    body = lib_6.initiativeLink(c.initiative, embed=True, noHref=True, fullURL=True)
                                                %>
                                                <a href="mailto:?subject=${subj}&body=${body}"><span class="icon-stack">
                                                  <i class="icon-circle icon-stack-base"></i>
                                                  <i class="icon-envelope icon-light"></i>
                                                </span></a>
                                            % endif

                                            <!--
                                            <span class="icon-stack">
                                              <i class="icon-circle icon-stack-base rss"></i>
                                              <i class="icon-code icon-light"></i>
                                            </span>
                                            -->
                                        </span>
                                    % endif
                                </div>

                        % if c.initiative['public'] == '1':
                            </div>
                        % endif

                    % endif

                </div><!-- col-xs-12 -->
            </div><!-- row -->
        </div><!-- initiative-well -->
    </div> <!-- i-control-panel -->
</%def>

<%def name="iControlPanelInner()">
    % if c.authuser and c.authuser['memberType'] == 'organization':
        <h3 class="i-control-panel-header hidden-xs">Position</h3>
        <hr class="narrow">
        <!-- this is the second call to positionsCtrl on the initative page - would be better to use a service -->
        <div ng-init="code = '${c.initiative['urlCode']}'; objType = 'initiative'"></div>
        <div ng-controller="positionsCtrl">
            ${lib_6.orgPosition(c.initiative)}
        </div>

    % elif 'workshopCode' in c.initiative:
        <div ng-controller="ratingsController" ng-cloak>
            {{getCriteriaList('${"/workshop/" + c.initiative['workshopCode'] + "/" + c.initiative['workshop_url']}', '${c.initiative['urlCode']}')}}

            <div ng-switch="rating.type">
                <h3 ng-switch-when="criteria" class="i-control-panel-header hidden-xs">Rate</h3>

                <h3 ng-switch-when="yesno" class="i-control-panel-header hidden-xs">Vote</h3>

                <hr class="narrow">

                <div ng-init="inPage = true;" ng-cloak></div>
                <div ng-switch-when="criteria" ng-controller="demographicsController">
                    %if 'user' in session:
                        <div ng-hide="inDemographics" >
                            <div class="row">
                                <div class="col-xs-10 col-xs-offset-1">
                                    ${ng_lib.rateCriteria(type = 'sidebar')}
                                </div>
                            </div>
                        </div>
                         <div ng-if="hasVoted">
                            <div ng-show="demographics.required != ''">
                                {{checkDemographics(item.parentHref)}}
                                ${ng_lib.demographics()}
                            </div>
                        </div>
                     %else:
                        <div class="row">
                            <div class="col-xs-10 col-xs-offset-1">
                                ${ng_lib.rateCriteria(readOnly = "1", type = 'sidebar')}
                            </div>
                        </div>
                     %endif
                </div><!-- close criteria inner-->
                <div ng-switch-when="yesno">
                    <div ng-controller="yesNoVoteCtrl">
                        ${ng_lib.yesNoVoteBlock()}
                    </div>
                </div> <!-- close yesno inner-->
            </div> <!-- close default inner-->
        </div> <!-- close switch inner-->

    %else:

        <h3 class="i-control-panel-header hidden-xs">Vote</h3>
        <hr class="narrow">
        <div ng-init="inPage = true;" ng-cloak>
            <div ng-controller="yesNoVoteCtrl">
                ${ng_lib.yesNoVoteBlock()}
            </div>
        </div>

    %endif

    ${commentHelpers.justComment(c.initiative, c.discussion)}

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
            countyMessage = "Leave 'State' blank if your initiative applies to the entire country."
        endif
    %>
    <div class="row"><span id="planetSelect">
        <div class="col-sm-3">Planet:</div>
        <div class="col-sm-8">
            <select name="geoTagPlanet" id="geoTagPlanet" class="geoTagCountry">
                <option value="0">Earth</option>
            </select>
        </div><!-- col-sm-8 -->
    </span><!-- countrySelect -->
    </div><!-- row -->     
    <div class="row"><span id="countrySelect">
        <div class="col-sm-3">Country:</div>
        <div class="col-sm-8">
            <select name="geoTagCountry" id="geoTagCountry" class="geoTagCountry">
                <option value="0">Select a country</option>
                <option value="United States" ${countrySelected}>United States</option>
            </select>
        </div><!-- col-sm-8 -->
    </span><!-- countrySelect -->
    </div><!-- row -->
    <div class="row"><span id="stateSelect">
        % if c.country != "0":
            <div class="col-sm-3">State:</div><div class="col-sm-8">
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
            </div><!-- col-sm-8 -->
        % else:
            Leave 'Country' blank if your initiative applies to the entire planet.
        % endif
    </span></div><!-- row -->
    <div class="row"><span id="countySelect">
        % if c.state != "0":
            <% counties = getCountyList("united-states", c.state) %>
            <% cityMessage = "Leave blank 'County' blank if your initiative applies to the entire state." %>
            <div class="col-sm-3">County:</div><div class="col-sm-8">
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
            </div><!-- col-sm-8 -->
        % else:
            <% cityMessage = "" %>
            ${countyMessage}
        % endif
    </span></div><!-- row -->
    <div class="row"><span id="citySelect">
        % if c.county != "0":
            <% cities = getCityList("united-states", c.state, c.county) %>
            <% postalMessage = "Leave 'City' blank if your initiative applies to the entire county." %>
            <div class="col-sm-3">City:</div><div class="col-sm-8">
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
            </div><!-- col-sm-8 -->
        % else:
            <% postalMessage = "" %>
            ${cityMessage}
        % endif
        </span></div><!-- row -->
    <div class="row">
        <span id="postalSelect">
        % if c.city != "0":
            <% postalCodes = getPostalList("united-states", c.state, c.county, c.city) %>
                <% underPostalMessage = "or leave blank if your initiative is specific to the entire city." %>
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
        </span>
    </div><!-- row -->
    <div class="row">
        <div class="col-xs-9 col-xs-offset-3">
            <span class="help-block" id="underPostal">${underPostalMessage}</span>
        </div>
    </div><!-- row -->
    <br/>
</%def>


<%def name="coAuthorInvite()">
    <h2 class="no-top">Users</h2>
    % if 'user' in session and c.authuser:
        <div ng-init="urlCode = '${c.initiative['urlCode']}'; url = '${c.initiative['url']}'; authuserCode = '${c.authuser['urlCode']}'">
            <div ng-controller="userLookupCtrl">

                <label>Author and Coauthors:</label>
                <!-- 
                <div class="centered" ng-show="loading" ng-cloak>
                    <i class="icon-spinner icon-spin icon-4x" style="color: #333333"></i>
                </div>
                <div class="row" ng-show="!loading"> -->
                    <table class="table-striped full-width" ng-cloak>
                        <tr>
                            <td>
                                ${lib_6.userImage(c.user, className="avatar med-avatar")}
                            </td>
                            <td>
                                <a class="green green-hover" href="/profile/${c.user['urlCode']}/${c.user['url']}">${c.user['name']}</a>
                                <span class="grey">from <a href="${c.authorGeo['cityURL']}" class="orange oreange-hover">${c.authorGeo['cityTitle']}</a>, <a href="${c.authorGeo['stateURL']}" class="orange orange-hover">${c.authorGeo['stateTitle']}</a></span>
                            </td>
                            <td>
                                <span class="badge badge-inverse">Original Author</span>
                            </td>
                            <td></td>
                            <td></td>
                        </tr>
                        <tr ng-repeat="a in authors">
                            <td>
                                <a class="pull-left" href="/profile/{{a.urlCode}}/{{a.url}}">
                                    <img class="media-object avatar med-avatar" ng-src="{{a.photo}}" alt="{{a.name}}" title="{{a.name}}">
                                </a>
                            </td>
                            <td>
                                <a class="green green-hover" href="/profile/{{a.urlCode}}/{{a.url}}">{{a.name}}</a>
                                <span class="grey">from <a href="{{a.cityURL}}" class="orange oreange-hover">{{a.cityTitle}}</a>, <a href="{{a.stateURL}}" class="orange orange-hover">{{a.stateTitle}}</a></span>
                            </td>
                            <td>
                                <span ng-if="a.pending == '1'"  class="badge badge-info">Invitation Pending</span>
                            </td>
                            <td>
                                <button type="button" ng-if="a.pending == '1'" ng-click="resendInvite(a.urlCode)" class="btn btn-primary pull-right">Resend Invite</button>
                            </td>
                            <td ng-if="a.urlCode != authuserCode">
                                <button type="button" ng-click="removeCoA(a.urlCode)" class="btn btn-danger pull-right">Remove</button>
                            </td>
                            <td ng-if="a.urlCode == authuserCode">
                                <form class="no-bottom" action="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/{{a.urlCode}}/facilitate/resign/handler" ng-cloak>
                                    <input type="hidden" name="resign" value="resign">
                                    <button type="submit" class="btn btn-danger pull-right">Resign</button>
                                </form>
                            </td>
                        </tr>
                    </table>
                <!-- ng-loading </div> -->

                <div class="spacer"></div>

                <form class="form-inline" ng-submit="lookup()">
                    <label>Invite CoAuthors:</label>
                    <div class="form-group">
                        <input class="form-control col-sm-8" type="text" ng-submit="lookup()" name="userValue" ng-model="userValue" placeholder="Type a user's name...">
                    </div>
                    <button type="submit" class="btn btn-default"><i class="icon-search"></i></button>
                </form>
                <table class="table-striped full-width" ng-cloak>
                    <tr ng-repeat="user in users | limitTo:10">
                        <td>
                            <a href="/profile/{{user.urlCode}}/{{user.url}}">
                                <img class="media-object avatar med-avatar" ng-src="{{user.photo}}" alt="{{user.name}}" title="{{user.name}}">
                            </a>
                        </td>
                        <td class="col-sm-8 grey"><a class="green green-hover" href="/profile/{{user.urlCode}}/{{user.url}}">{{user.name}}</a> from <a href="{{user.cityURL}}">{{user.cityTitle}}</a>, <a href="{{user.stateURL}}">{{user.stateTitle}}</a></td>
                        <td>
                            <button ng-click="submitInvite(user.urlCode)" class="btn btn-primary pull-right">Invite to Coauthor</button>
                        </td>
                    </tr>
                </table>

                <div ng-if="alertMsg != ''" class="alert alert-{{alertType}} {{alertDisplay}}" ng-cloak>
                    <button type="button" class="close" ng-click="hideShowAlert()">&times;</button>
                    {{alertMsg}}
                </div>
            </div><!-- ng-controller -->
        </div><!-- ng-init -->
    %endif   
</%def>

<%def name="preview()">
    <a class="btn btn-default" id="previewBtn" target="_blank" href="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/show"><strong>Preview</strong></a>
</%def>


<%def name="photosEdit()">

    <div class="row" id="photo">
        <div class="col-xs-12"><h2 class="no-top">Photos</h2></div>
    </div><!-- row -->

    <form id="fileupload" action="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/photo/upload/handler" method="POST" enctype="multipart/form-data" data-fileupload="options" ng-class="{true: 'fileupload-processing'}[!!processing() || loadingFiles]" ng-show="true">
        <label>ID Photo:</label>
        <div id="fileinput-button-div">
            <!-- The fileinput-button span is used to style the file input field as button -->
            %if 'directoryNum_photos' in c.initiative and 'pictureHash_photos' in c.initiative:
                <% thumbnail_url = "/images/photos/%s/thumbnail/%s.png"%(c.initiative['directoryNum_photos'], c.initiative['pictureHash_photos']) %>
                <span class="pull-left">Current Initiative Picture
                <div class="spacer"></div>
                <img src="${thumbnail_url}">
                </span>
            % else:
                <span class="pull-left">Upload a Picture (Required)</span>
            % endif
            <input class="fileinput-button pull-right" type="file" name="files[]">
            </span>
            <!-- The loading indicator is shown during file processing -->
            <div class="fileupload-loading"></div>
            <!-- The global progress information -->
        </div><!-- fileinput-button-div -->

        <div class="row">
            <div class="col-sm-10 col-sm-offset-1 fade" data-ng-class="{true: 'in'}[!!active()]">
                <!-- The global progress bar -->
                <div class="progress progress-success progress-striped active" data-progress="progress()"><div class="bar" ng-style="{width: num + '%'}"></div></div>
                <!-- The extended global progress information -->
                <div class="progress-extended">&nbsp;</div>
            </div><!-- col-sm-10 -->
        </div><!-- row -->
        <!-- The table listing the files available for upload/download -->
         
        <table class="table table-striped files ng-cloak" data-toggle="modal-gallery" data-target="#modal-gallery" ng-if="fuType === 'files[]'">
            <tbody>
                <tr data-ng-repeat="file in queue">
                    <td data-ng-switch="" on="!!file.thumbnail_url">
                        <div class="preview" data-ng-switch-when="true">
                            <script type="text/javascript">
                                function setAction(imageHash) {
                                    actionURL = "/profile/${c.user['urlCode']}/${c.user['url']}/photo/" + imageHash + "/update/handler";
                                    document.getElementById('fileupload').action = actionURL;
                                }
                            </script>
                            <div class="row">
                                <img src="{{file.thumbnail_url}}">
                                New Picture Uploaded and Saved
                                <a href="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/editHandler" class="btn btn-warning btn-large pull-right" name="submit_photo">Save Changes</a>
                            </div><!-- row -->
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
                        <button type="button" class="btn btn-warning cancel" data-ng-click="file.$cancel()" data-ng-hide="!file.$cancel"  data-toggle="collapse" data-target="#fileinput-button-div">
                        <i class="icon-ban-circle icon-white"></i>
                        <span>Cancel</span>
                        </button>
                    </td>
                </tr>
            </tbody>
        </table> 

    <!-- BACKGROUND PHOTO UPLOAD-->
<form action="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/photo/upload/handler" method="POST" enctype="multipart/form-data"  ng-class="{true: 'fileupload-processing'}[!!processing() || loadingFiles]" ng-show="true" data-fileuploadcover="options">
        <label>Cover Photo:</label>
        <div id="fileinput-button-div">
            <!-- The fileinput-button span is used to style the file input field as button -->
            %if 'directoryNum_photos' in c.initiative and 'pictureHash_cover' in c.initiative:
                <% thumbnail_url = "/images/cover/%s/thumbnail/%s.png"%(c.initiative['directoryNum_cover'], c.initiative['pictureHash_cover']) %>
                <span class="pull-left">Current Cover Picture
                <div class="spacer"></div>
                <img src="${thumbnail_url}">
                </span>
            % else:
                <span class="pull-left">Upload a Picture (Required)</span>
            % endif
            <input class="fileinput-button pull-right" type="file" name="cover[]" id="fileCover">
            <input type="hidden" name="cover" value="True">
            </span>
            <!-- The loading indicator is shown during file processing -->
            <div class="fileupload-loading"></div>
            <!-- The global progress information -->
        </div><!-- row -->
        
</form>

<table class="table table-striped files ng-cloak" data-toggle="modal-gallery" data-target="#modal-gallery">
            <tbody><tr data-ng-repeat="file in queue" ng-if="fuType === 'cover[]'">
                <td data-ng-switch="" on="!!file.thumbnail_url">
                    <div class="preview" data-ng-switch-when="true">
                        <script type="text/javascript">
                            function setAction(imageHash) {
                                actionURL = "/profile/${c.user['urlCode']}/${c.user['url']}/photo/" + imageHash + "/update/handler";
                                document.getElementById('fileupload').action = actionURL;
                            }
                        </script>
                        <div class="row">
                            <img src="{{file.thumbnail_url}}">
                            New Picture Uploaded and Saved
                            <a href="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/editHandler" class="btn btn-warning btn-large pull-right" name="submit_photo">Save Changes</a>
                        </div><!-- row -->
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
                            <button type="button" class="btn btn-warning cancel" data-ng-click="file.$cancel()" data-ng-hide="!file.$cancel"  data-toggle="collapse" data-target="#fileinput-button-div">
                            <i class="icon-ban-circle icon-white"></i>
                            <span>Cancel</span>
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>   
    <form></form>
</%def>

<%def name="editInfo()">
    <% 
        tagList = tagLib.getTagCategories()
        postalCodeSelected = ""
        citySelected = ""
        countySelected = ""
        if c.initiative:
            iScope = c.initiative['scope']
            if 'workshop_subcategory_tags' in c.initiative:
                subcategoryTags = c.initiative['workshop_subcategory_tags'].split("|")
            else:
                subcategoryTags = False
        else:
            iScope = "0|0|0|0|0|0|0|0|0|0"
        scopeList = iScope.split('|')
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

    <h2 class="no-top">Info</h2>
    <form method="POST" name="edit_initiative_summary" id="edit_initiative_summary" action="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/editHandler" ng-controller="showThingCtrl" ng-init="cost = '${c.initiative['cost']}'">

        <div class="form-group">
            <label for="title" class="control-label" required><strong>Initiative Title:</strong></label>
            <input type="text" name="title" class="input-lg form-control" value="${c.initiative['title']}">
            <p class="text-info">
                Keep it short and descriptive. 10 words or less.
            </p>
        </div><!-- form-group -->

        <div class="form-group">
            <label for="title" class="control-label" required><strong>Geographic Region:</strong></label>
            <p class="text-info">
                The region or legal jurisdiction associated with your initiative.
            </p>
            ${geoSelect()}
        </div><!-- form-group -->

        <div class="form-group">
            <label for="tag" class="control-label" required><strong>Category Tag:</strong></label>
            <select name="tag" id="tag">
            % if c.initiative['public'] == '0':
                <option value="">Choose one</option>
            % endif
            % for tag in tagList:
                <% 
                    selected = ""
                    if c.initiative['tags'] == tag:
                        selected = "selected"
                %>
                <option value="${tag}" ${selected}/> ${tag}</option>
            % endfor
            </select>
            <p class="text-info">The topic area associated with your initiative.</p>
        </div><!-- form-group -->

         %if subcategoryTags:
        <div class="form-group">
            <label for="subcategory" class="control-label" required><strong>Subcategory Tag:</strong></label><br/>
            % for tag in subcategoryTags:
                <% 
                    selected = ""
                    if 'subcategory_tags' in c.initiative and c.initiative['subcategory_tags'] is not None:
                        if tag in c.initiative['subcategory_tags']:
                            selected = "checked"
                %>
                <input type="checkbox" name="subcategory" value="${tag}" ${selected}/> ${tag}</option><br/>
            % endfor
            <p class="text-info">The particular topic area associated with your initiative.</p>
        </div><!-- row -->
        %endif


        <div class="form-group">
            <label for="description" class="control-label" required><strong>Cost Estimate:</strong></label>
            <div class="input-group" ng-cloak>
              <span class="input-group-addon">$</span>
              <input type="text" class="form-control" name="cost" value="{{cost}}" ng-model="cost" ng-pattern="costRegex">
              <span class="input-group-addon">.00</span>
            </div>
            <span class="error help-text" ng-show="edit_initiative_summary.cost.$error.pattern" ng-cloak>Invalid cost value</span>
                            <p class="text-info">
                Acceptable formats include: 500,000  or  500000.
            </p>
        </div>
        <div class="form-group">
            <label class="control-label" required>Summary:</label>
            <div class="text-info">
                <p>This is a concise description that should be easy for anyone who might rate your initiative to understand. The summary must be no longer than 100 words. <strong ng-class="{red: wordCount >= 101}" ng-cloak>{{wordCount}}</span> words</strong>
                </p>
            </div>
            <textarea rows="8" type="text" name="description" class="form-control" ng-model="summary" ng-keydown="getWordCount()"></textarea>
        </div>
        <div class="form-group">
            <label class="control-label" required>Full Text:</label>
            <div class="text-info">
                <p>The full text of your initiative can be as long as needed and should touch on the background and details of what you are proposing. This section uses markdown and accepts html (like youtube iframes) as well. For example, to insert an image, make sure the file is uploaded to the internet somewhere and then insert the image URL into the info sectionlike so:</p>
                <pre>![The Civinomics Logo](https://civinomics.com/images/logo.png "Civinomics Logo")</pre>
                <p>For more... 
                    ${lib_6.formattingGuide()}
                </p>
            </div>
            <textarea rows="8" type="text" name="proposal" class="form-control">${c.initiative['proposal']}</textarea>
        </div>
        <button type="submit" class="btn btn-success btn-block btn-lg top" name="submit_summary">Save Changes</button>
    </form>
</%def>

<%def name="reporting()">
    <h2 class="no-top">Reporting</h2>
    <div class="spacer"></div>
    <a class="btn btn-default btn-lg" target="_blank" href="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/printComments">Print Comments</a>
</%def>

