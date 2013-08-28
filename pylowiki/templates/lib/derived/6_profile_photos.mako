<%!
    import pylowiki.lib.db.workshop     as workshopLib
    import pylowiki.lib.db.facilitator  as facilitatorLib
    import pylowiki.lib.db.listener     as listenerLib
    import pylowiki.lib.db.follow       as followLib
    import pylowiki.lib.db.user         as userLib
    import pylowiki.lib.db.pmember      as pmemberLib
    import pylowiki.lib.utils           as utils
%>

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="uploadPhoto()">
    % if 'user' in session and (c.authuser.id == c.user.id):
        <form id="fileupload" action="/profile/${c.authuser['urlCode']}/${c.authuser['url']}/photo/upload/handler" method="POST" enctype="multipart/form-data" data-ng-app="demo" data-fileupload="options" ng-class="{true: 'fileupload-processing'}[!!processing() || loadingFiles]" class = "civAvatarUploadForm" ng-show="true">
            <div class="row-fluid fileupload-buttonbar">
                <div class="span10 offset1">
                    <!-- The fileinput-button span is used to style the file input field as button -->
                    <span class="btn btn-success fileinput-button pull-right">
                        <i class="icon-plus icon-white"></i>
                        <span>Photo</span>
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
                            <% tagList = workshopLib.getWorkshopTagCategories() %>
                            <form action="/profile/${c.user['urlCode']}/${c.user['url']}/photo/{{file.image_hash}/update/handler" method="POST">
                            <div class="row-fluid">
                                <div class="span3">
                                    <a data-ng-href="{{file.url}}" title="{{file.name}}" data-gallery="gallery" download="{{file.name}}"><img data-ng-src="{{file.thumbnail_url}}"></a>
                                </div><!-- span4 -->
                                <div class="span4">

                                    <fieldset>
                                    <label for="title" class="control-label" required>Title:</label>
                                    <input type="text" name="title" value="Sample Title">
                                    <label for="description" class="control-label" required>Description:</label>
                                    <textarea name="description">Sample Description</textarea>

                                    <label for="scope" class="control-label" required>Scope:</label>
                                    <input type="text" name="scope" value="||0||0||0||0|0">
                                    <fieldset>
                                </div><!-- span4 -->
                                <div class="span4">
                                    <fieldset>
                                    Category Tags
                                    % for tag in tagList:
                                        <label class="checkbox">
                                        <input type="checkbox" name="categoryTags" value="${tag}" /> ${tag}
                                        </label>
                                    % endfor
                                    </fieldset>
                                </div><!-- span4 -->
                            </div><!-- row-fluid -->
                            <div class="row-fluid">
                                <button class="btn btn-success" type="Submit">Submit</button>
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

<%def name="showPhoto()">
    <div class="row-fluid">
        <div class="span8 offset2">
            <% imgSrc = "/images/photos/" + c.photo['directoryNum_photos'] + "/photo/" + c.photo['pictureHash_photos'] + ".png" %>
            <img src="${imgSrc}" class="wrap-photo"><br />
            <div class="spacer"></div>
            <div class="centered">
                ${c.photo['title']}<br />
            </div><!-- centered -->
            <div class="spacer"></div>
            ${c.photo['description']}
        </div>
    </div>
</%def>