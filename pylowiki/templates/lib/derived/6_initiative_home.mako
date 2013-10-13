<%!
    import pylowiki.lib.db.user         as userLib
    import pylowiki.lib.db.workshop     as workshopLib
    import pylowiki.lib.db.generic      as genericLib
    import pylowiki.lib.utils           as utils
    import misaka as m
    
    import logging
    log = logging.getLogger(__name__)
%>

<%def name="showInfo()">
    <div>
    <h4>Introduction</h4>
    <p>
    This introduction was written and is maintained by the initiative author.
    You are encouraged to add links to additional information resources.
    </p>
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
        <div class="thumbnail tight media-object" style="height: 60px; width: 90px; margin-bottom: 5px; background-image:url("/images/slide/thumbnail/supDawg.thumbnail"); background-size: cover; background-position: center center;"></div>
        </a>
        <div class="media-body">
            <a href="/initiative/${item['urlCode']}/${item['url']}/show" class="listed-item-title media-heading lead bookmark-title">${item['title']}</a>
            % if 'user' in session:
                % if c.user.id == c.authuser.id or userLib.isAdmin(c.authuser.id):
                    <a href="/initiative/${item['urlCode']}/${item['url']}/edit">Edit</a>
                % endif
            % endif
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
            <option value="choose">Choose one</option>
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
            hi
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