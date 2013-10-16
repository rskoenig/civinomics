<%!
    import pylowiki.lib.db.user         as userLib
    import pylowiki.lib.db.workshop     as workshopLib
    import pylowiki.lib.db.generic      as genericLib
    import pylowiki.lib.utils           as utils
    import misaka as m
    
    import logging
    log = logging.getLogger(__name__)
%>

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="showAuthor(item)">
    ${lib_6.userImage(item.owner, className="avatar med-avatar")} ${lib_6.userLink(item.owner)}<span class="grey">${lib_6.userGreetingMsg(item.owner)}</span> from ${lib_6.userGeoLink(item.owner)}
</%def>

<%def name="showScope(item)">
    <% 
        scopeList = item['scope'].split('|')
        country = scopeList[2].replace("-", " ")
        state = scopeList[4].replace("-", " ")
        county = scopeList[6].replace("-", " ")
        city = scopeList[8].replace("-", " ")
        postalCode = scopeList[9]
        scopeString = "%s, State of %s"%(country.title(), state.title())
        if city == '0':
            scopeString += ', <span class="badge badge-info">County of %s</span>'%county.title()
        else:
            scopeString += ', County of %s'%county.title()
        if postalCode == '0':
            scopeString += ', <span class="badge badge-info">City of %s</span>'%city.title()
        else:
            scopeString += ", City of %s"%city.title()
        if postalCode != '0':
            scopeString += ', <span class="badge badge-info">Zip code of %s</span>'%postalCode
    %>
    ${scopeString | n}
</%def>

<%def name="showInfo()">
    <h4>Introduction</h4>
    ${m.html(c.initiative['background'], render_flags=m.HTML_SKIP_HTML) | n}
    </div>
</%def>

<%def name="watchButton()">
    % if 'user' in session:
        % if c.isFollowing:
            <button class="btn round btn-civ pull-right followButton following" data-URL-list="workshop_${c.w['urlCode']}_${c.w['url']}" rel="tooltip" data-placement="bottom" data-original-title="this workshop" id="workshopBookmark">
            <span><i class="icon-bookmark icon-white pull-left"></i> Bookmarked </span>
            </button>
        % else:
            <button class="btn round pull-right followButton" data-URL-list="workshop_${c.w['urlCode']}_${c.w['url']}" rel="tooltip" data-placement="bottom" data-original-title="this workshop" id="workshopBookmark">
             <span><i class="icon-bookmark pull-left"></i> Bookmark </span>
            </button>
        % endif
    % endif
</%def>

<%def name="iResources()">
    Resources go here
</%def>

<%def name="listInitiative(item)">
    <div class="media profile-workshop">
        <a class="pull-left" href="/initiative/${item['urlCode']}/${item['url']}/show">
        % if 'directoryNum_photos' in item and 'pictureHash_photos' in item:
            <% thumbnail_url = "/images/photos/%s/thumbnail/%s.png"%(item['directoryNum_photos'], item['pictureHash_photos']) %>
        % else:
            <% thumbnail_url = "/images/slide/thumbnail/supDawg.thumbnail" %>
        % endif
        <div class="thumbnail tight media-object" style="height: 60px; width: 90px; margin-bottom: 5px; background-image:url(${thumbnail_url}); background-size: cover; background-position: center center;"></div>
        </a>
        <div class="media-body">
            <a href="/initiative/${item['urlCode']}/${item['url']}/show" class="listed-item-title media-heading lead bookmark-title">${item['title']}</a>
            % if 'user' in session:
                % if c.user.id == c.authuser.id or userLib.isAdmin(c.authuser.id):
                    <a href="/initiative/${item['urlCode']}/${item['url']}/edit">Edit</a> &nbsp;
                    % if item['public'] == '0':
                        Not yet public
                    % else:
                        Public
                    % endif
                % endif
            % endif
            <br />
            ${showScope(item) | n}
        </div><!-- media-body -->
    </div><!-- media -->
</%def>

<%def name="editInitiative()">
    <% 
        tagList = workshopLib.getWorkshopTagCategories()
        initiativeTags = c.initiative['tags'].split('|')
        postalCodeSelected = ""
        citySelected = ""
        countySelected = ""
        scopeList = c.initiative['scope'].split('|')
        if scopeList[9] == '0' and scopeList[8] == '0':
            countySelected = "selected"
        elif scopeList[9] == '0' and scopeList[8] != '0':
            citySelected = "selected"
        else:
            postalCodeSelected = "selected"

    %>
    % if c.saveMessage and c.saveMessage != '':
        <div class="spacer"></div>
        <div class="alert alert-success">
        <button type="button" class="close" data-dismiss="alert">&times;</button>
        ${c.saveMessage}
        </div>
    % endif

    <div class="spacer"></div>
    <div class="row-fluid">
        <span class="pull-left"><h4>Edit Initiative</h4></span>
        <span class="pull-right"><a href="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/show">View Initiative</a></span>
    </div><!-- row-fluid -->
    <div class="spacer"></div>
    <div class="row-fluid">
        <div class="span6">
        <form method="POST" name="workshop_background" id="workshop_background" action="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/editHandler">
            <fieldset>
            % if c.complete and c.initiative['public'] == '0':
                <label for="public" class="control-label">
                All of the required information has been added to your initiative. When you are satisfied that it is ready, 
                click on this checkbox to make your initiative public.</label>
                Make Public: <input type="checkbox" name="public" value="yes"><div class="spacer"></div>
            % elif c.initiative['public'] == '0':
                You will be to make this initiative public when all of the required information has been filled out and a 
                picture uploaded.
            % endif

            <label for="title" class="control-label" required>Initiative Title:</label>
            <input type="text" name="title" value="${c.initiative['title']}">
            <label for="description" class="control-label" required>Short Description:</label>
            <input type="text" name="description" value="${c.initiative['description']}">
            <label for="description" class="control-label" required>Estimated cost to complete this initiative:</label>
            <input type="text" name="cost" value="${c.initiative['cost']}">
            <label for="level" class="control-label" required>This initiative is for:</label>
            <select name="level" id="level">
            <option value="postalCode" ${postalCodeSelected}> My Zip Code</option>
            <option value="city" ${citySelected}> My City</option>
            <option value="county" ${countySelected}> My County</option>
            </select>
            </fieldset>
            <label for="tag" class="control-label" required>Initiative category:</label>
            <select name="tag" id="tag">
            % if c.initiative['public'] == '0':
                <option value="choose">Choose one</option>
            % endif
            % for tag in tagList:
                <% 
                    selected = ""
                    if tag in initiativeTags:
                        selected = "selected"
                %>
                <option value="${tag}" ${selected}/> ${tag}</option>
            % endfor
            </select>
            <label for="data" class="control-label" required>Background Info: <a href="#" class="btn btn-mini btn-info" onclick="window.open('/help/markdown.html','popUpWindow','height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');">View Formatting Guide</a></label>
            <textarea rows="10" id="data" name="data" class="span12">${c.initiative['background']}</textarea>
            <div class="background-edit-wrapper">
            </div><!-- background-edit-wrapper -->
            <div class="preview-information-wrapper" id="live_preview">

            </div><!-- preview-information-wrapper -->
            <button type="submit" class="btn btn-warning pull-left" name="submit">Save Changes</button>
            </form>
        </div><!-- span6 -->
        <div class="span6">
            <form id="fileupload" action="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/photo/upload/handler" method="POST" enctype="multipart/form-data" data-ng-app="demo" data-fileupload="options" ng-class="{true: 'fileupload-processing'}[!!processing() || loadingFiles]" class = "civAvatarUploadForm" ng-show="true">
                <div id="fileinput-button-div" class="row-fluid fileupload-buttonbar collapse in">
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
                    <span class="btn btn-success fileinput-button pull-right"  data-toggle="collapse" data-target="#fileinput-button-div">
                    <i class="icon-plus icon-white"></i>
                    <span>Picture</span>
                    <input type="file" name="files[]">
                    </span>
                    <!-- The loading indicator is shown during file processing -->
                    <div class="fileupload-loading"></div>
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
                                <div class="row-fluid">
                                    <img src="{{file.thumbnail_url}}">
                                    New Picture Uploaded and Saved
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
                                    <button type="button" class="btn btn-warning cancel" data-ng-click="file.$cancel()" data-ng-hide="!file.$cancel"  data-toggle="collapse" data-target="#fileinput-button-div">
                                    <i class="icon-ban-circle icon-white"></i>
                                    <span>Cancel</span>
                                    </button>
                                </td>
                            </tr>
                            </tbody></table>
                        </form>
            </div><!-- span6 -->
        </div><!-- row-fluid -->
</%def>