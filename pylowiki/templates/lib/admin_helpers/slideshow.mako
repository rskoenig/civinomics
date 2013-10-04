<!--
/*
 * jQuery File Upload Plugin Demo 6.5.1
 * https://github.com/blueimp/jQuery-File-Upload
 *
 * Copyright 2010, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 */
-->

<%def name="workshop_admin_slideshow()">    
    <div class="section-wrapper">
        <div class="browse">
            <h4 class="section-header smaller">Slideshow</h4>
            ${add_slides(c.w)}
            ${edit_slideshow()}
            % if c.w['startTime'] == '0000-00-00':
                <div class="row-fluid">
                    <form name="continueToNext" id="continueToNext" action="/workshop/${c.w['urlCode']}/${c.w['url']}/configureContinueHandler" method="POST">
                    <button type="submit" class="btn btn-warning" name="continueToNext">Continue To Next Step</button>
                    </form>
                </div><!-- row-fluid -->
            % endif
        </div><!-- browse -->
    </div><!-- section-wrapper -->
</%def>

<%def name="add_slides(parent)">
    <!-- The file upload form used as target for the file upload widget -->
    <form id="fileupload" action="/${parent.objType}/${parent['urlCode']}/${parent['url']}/addImages/handler" method="POST" enctype="multipart/form-data">
    <p><strong>Add images</strong></p>
    <ul>
        <li>Slideshow looks best with 6 or more images</li>
        <li>Make sure you have permission to use the images</li>
        <li>Avoid images smaller than 640 pixels wide by 480 pixels high</li>
    </ul>
    <!-- The fileupload-buttonbar contains buttons to add/delete files and start/cancel the upload -->
    <div class="row-fluid">
        <div class="span7 offset1 fileupload-buttonbar">
            <!-- The fileinput-button span is used to style the file input field as button -->
            <span class="btn btn-success fileinput-button">
                <i class="icon-plus icon-white"></i>
                <span>Add images...</span>
                <input type="file" name="files[]" multiple>
            </span>
            <button type="submit" class="btn btn-primary start">
                <i class="icon-upload icon-white"></i>
                <span>Start upload</span>
            </button>
            <button type="reset" class="btn btn-warning cancel">
                <i class="icon-ban-circle icon-white"></i>
                <span>Cancel upload</span>
            </button>
        </div><!-- span7 -->
        <div class="span4">
            <!-- The global progress bar -->
            <div class="progress progress-success progress-striped active fade">
                <div class="bar" style="width:0%;"></div>
            </div><!-- progress -->
        </div><!-- span4 -->
    </div><!-- row-fluid -->
    <div class="row-fluid">
        <div class="span12">
            <!-- The loading indicator is shown during image processing -->
            <div class="fileupload-loading"></div>
            <br>
            <!-- The table listing the files available for upload/download -->
            <table class="table table-striped"><tbody class="files" data-toggle="modal-gallery" data-target="#modal-gallery"></tbody></table>
            <br />
        </div><!-- span12 -->
    </div><!-- row-fluid -->

    <!-- modal-gallery is the modal dialog used for the image gallery -->
    <div id="modal-gallery" class="modal modal-gallery hide fade">
        <div class="modal-header">
            <a class="close" data-dismiss="modal">&times;</a>
            <h3 class="modal-title"></h3>
        </div><!-- modal-header -->
        <div class="modal-body"><div class="modal-image"></div></div>
        <div class="modal-footer">
            <a class="btn modal-download" target="_blank">
                <i class="icon-download"></i>
                <span>Download</span>
            </a>
            <a class="btn btn-success modal-play modal-slideshow" data-slideshow="5000">
                <i class="icon-play icon-white"></i>
                <span>Slideshow</span>
            </a>
            <a class="btn btn-info modal-prev">
                <i class="icon-arrow-left icon-white"></i>
                <span>Previous</span>
            </a>
            <a class="btn btn-primary modal-next">
                <span>Next</span>
                <i class="icon-arrow-right icon-white"></i>
            </a>
        </div><!-- modal-footer -->
    </div><!-- modal-gallery -->
    </form>

<!-- The template to display files available for upload -->
<script id="template-upload" type="text/x-tmpl">
{% for (var i=0, file; file=o.files[i]; i++) { %}
    <tr class="template-upload fade">
        <td class="preview"><span class="fade"></span></td>
        <td class="name"><span>{%=file.name%}</span></td>
        <td class="size"><span>{%=o.formatFileSize(file.size)%}</span></td>
        {% if (file.error) { %}
            <td class="error" colspan="2"><span class="label label-important">{%=locale.fileupload.error%}</span> {%=locale.fileupload.errors[file.error] || file.error%}</td>
        {% } else if (o.files.valid && !i) { %}
            <td>
                <div class="progress progress-success progress-striped active"><div class="bar" style="width:0%;"></div></div>
            </td>
            <td class="start">{% if (!o.options.autoUpload) { %}
                <button class="btn btn-primary">
                    <i class="icon-upload icon-white"></i>
                    <span>{%=locale.fileupload.start%}</span>
                </button>
            {% } %}</td>
        {% } else { %}
            <td colspan="2"></td>
        {% } %}
        <td class="cancel">{% if (!i) { %}
            <button class="btn btn-warning">
                <i class="icon-ban-circle icon-white"></i>
                <span>{%=locale.fileupload.cancel%}</span>
            </button>
        {% } %}</td>
    </tr>
{% } %}
</script>

<!-- The template to display files available for download -->
<script id="template-download" type="text/x-tmpl">
{% for (var i=0, file; file=o.files[i]; i++) { %}
    <tr class="template-download fade">
        {% if (file.error) { %}
            <td></td>
            <td class="name"><span>{%=file.name%}</span></td>
            <td class="size"><span>{%=o.formatFileSize(file.size)%}</span></td>
            <td class="error" colspan="2"><span class="label label-important">{%=locale.fileupload.error%}</span> {%=locale.fileupload.errors[file.error] || file.error%}</td>
        {% } else { %}
            <td class="preview">{% if (file.thumbnail_url) { %}
                <a href="{%=file.url%}" title="{%=file.name%}" rel="gallery" download="{%=file.name%}"><img src="{%=file.thumbnail_url%}"></a>
            {% } %}</td>
            <td class="name">
                <a href="{%=file.url%}" title="{%=file.name%}" rel="{%=file.thumbnail_url&&'gallery'%}" download="{%=file.name%}">{%=file.name%}</a>
            </td>
            <td class="size"><span>{%=o.formatFileSize(file.size)%}</span></td>
            <td colspan="2"></td>
        {% } %}
        <td class="delete">
            <button class="btn btn-danger" data-type="{%=file.delete_type%}" data-url="{%=file.delete_url%}">
                <i class="icon-trash icon-white"></i>
                <span>{%=locale.fileupload.destroy%}</span>
            </button>
            <input type="checkbox" name="delete" value="1">
        </td>
    </tr>
{% } %}
</script>

</%def>

<%def name="edit_slideshow()">
    <div class="row-fluid">
        <p><strong>Edit Slideshow</strong></p>
        <ul>
            <li>Click and drag to rearrange images</li>
            <li>Add captions</li>
            <li>Drag images to Trash to delete</li>
        </ul>
        <div class="demo">
            <div class="column" id="published">
                <h4 class="centered">Published slides</h4 >
                <div id="num_published_slides" rel="${str(len(c.published_slides))}"></div>
                % for slide in c.published_slides:
                    % if int(slide['deleted']) == 0:
                        <div class="portlet" id = "portlet_${slide.id}">
                            <div class = "portlet-title edit" id = "${slide.id}_title">${slide['title']}</div>
                            <div class = "portlet-image">
                                % if slide['pictureHash'] == 'supDawg':
                                    <img src = "/images/slide/thumbnail/supDawg.thumbnail">
                                % elif 'format' in slide.keys():
                                    <img src = "/images/slide/${slide['directoryNum']}/thumbnail/${slide['pictureHash']}.${slide['format']}" class="image-thumbnail">
                                % else:
                                    <img src = "/images/slide/${slide['directoryNum']}/thumbnail/${slide['pictureHash']}.jpg" class="image-thumbnail">
                                % endif
                            </div><!-- portlet-image -->
                        </div><!-- portlet -->
                    % endif
                % endfor
            </div><!-- column -->
            <div class="column trashbasket" id="unpublished">
                <h4 class="unsortable centered">Trash</h4>
                % for slide in c.deleted_slides:
                    % if int(slide['deleted']) == 1:
                        <div class="portlet" id = "portlet_${slide.id}">
                            <div class = "portlet-title edit" id = "${slide.id}_title">${slide['title']}</div>
                            <div class = "portlet-image">
                                % if slide['pictureHash'] == 'supDawg':
                                    <img src = "/images/slide/thumbnail/supDawg.thumbnail">
                                % elif 'format' in slide.keys():
                                    <img src = "/images/slide/${slide['directoryNum']}/thumbnail/${slide['pictureHash']}.${slide['format']}" class="image-thumbnail">
                                % else:
                                    <img src = "/images/slide/${slide['directoryNum']}/thumbnail/${slide['pictureHash']}.jpg" class="image-thumbnail">
                                % endif
                            </div><!-- portlet-image -->
                        </div><!-- portlet -->
                    % endif
                % endfor
            </div><!-- column -->
        </div><!-- End demo -->
    </div><!-- row-fluid -->
</%def>
