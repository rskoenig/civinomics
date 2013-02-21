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

<%def name="admin_slideshow()">    
    <div class="section-wrapper">
        <div class="browse">
            <h4 class="section-header" style="text-align: center"><br />Slideshow</h4>
            Use one or more images with titles and captions to help educate and inform participants about the workshop topic.<br />
            Upload at least one image for your workshop. The first image of a slideshow is displayed in workshop listings, and the slideshow is displayed on the workshop home page.
            <br /><br />
            ${add_slides()}
            ${edit_slideshow()}
        </div><!-- browse -->
    </div><!-- section-wrapper -->
</%def>

<%def name="add_slides()">
    <!-- The file upload form used as target for the file upload widget -->
    <form id="fileupload" action="/workshop/${c.w['urlCode']}/${c.w['url']}/addImages/handler" method="POST" enctype="multipart/form-data">
    <p><strong>Add slides to slideshow</strong></p>
    <p>You may only upload images you own or have permission to upload to this site.<p>
    <p>Make sure to upload images larger than 640 pixels wide by 480 pixels high! Small images or thumbnails will look terrible in the slide show! Images oriented in "landscape" mode (wider than higher) are best.</p>
    <!-- The fileupload-buttonbar contains buttons to add/delete files and start/cancel the upload -->
    <div class="row-fluid">
        <div class="span1">
        </div>
        <div class="span7 fileupload-buttonbar">
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
            </form>
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
        <table class="table" >
        <thead>
        <tr><td>
        <script language="javascript">
            $(function() {
       
                $(".column").sortable(
                    { items: ".portlet" },
                    { connectWith: ".column" },
                    { update: function(event, ui) {
                        $.post("/workshop/${c.w['urlCode']}/${c.w['url']}/slide/edit/position", { slides: $(this).sortable('serialize') + "_" + $(this).attr('id')} );
                    }
                });

                $( ".portlet" ).addClass( "ui-widget ui-widget-content ui-helper-clearfix ui-corner-all" )
                    .find( ".portlet-header" )
                    .addClass( "ui-widget-header ui-corner-all" )
                    .prepend( "<span class='ui-icon ui-icon-minusthick'></span>")
                    .end()
                    .find( ".portlet-content" );

                $( ".portlet-title .ui-icon" ).click(function() {
                    $( this ).toggleClass( "ui-icon-minusthick" ).toggleClass( "ui-icon-plusthick" );
                    $( this ).parents( ".portlet:first" ).find( ".portlet-content" ).toggle();
                });
            });
        </script>
        <p><strong>Edit Slideshow</strong></p>
        <p>Click and drag to re-arrange a slideshow's order.</p>
        <br />
        <p>Click on a title or a caption to edit it.  Press enter to save your title or caption
        edits, press escape to cancel an edit.</p>
        <div class="demo">
            <div class="column" id="published">
                <h4 style="text-align:center;">Published slides</h4 >
                % for slide in c.published_slides:
                    % if int(slide['deleted']) == 0:
                        <div class="portlet" id = "portlet_${slide.id}">
                            <div class = "portlet-title edit" id = "${slide.id}_title">${slide['title']}</div>
                            <div class = "portlet-image">
                                % if slide['pictureHash'] == 'supDawg':
                                    <img src = "/images/slide/thumbnail/supDawg.thumbnail">
                                % else:
                                    <img src = "/images/slide/${slide['directoryNumber']}/thumbnail/${slide['pictureHash']}.jpg">
                                % endif
                            </div><!-- portlet-image -->
                        </div><!-- portlet -->
                    % endif
                % endfor
            </div><!-- column -->
            <div class="column" id="unpublished">
                <h4 style="text-align:center;" class="unsortable">Unpublished slides</h4>
                % for slide in c.slideshow:
                    % if int(slide['deleted']) == 1:
                        <div class="portlet" id = "portlet_${slide.id}">
                            <div class = "portlet-title edit" id = "${slide.id}_title">${slide['title']}</div>
                            <div class = "portlet-image">
                                % if slide['pictureHash'] == 'supDawg':
                                    <img src = "/images/slide/thumbnail/supDawg.thumbnail">
                                % else:
                                    <img src = "/images/slide/${slide['directoryNumber']}/thumbnail/${slide['pictureHash']}.jpg">
                                % endif
                            </div><!-- portlet-image -->
                        </div><!-- portlet -->
                    % endif
                % endfor
            </div><!-- column -->
        </div><!-- End demo -->
        </td></tr>
        </thead>
        </table>
        % if c.w['startTime'] == '0000-00-00':
            <form name="continueToNext" id="continueToNext" action="/workshop/${c.w['urlCode']}/${c.w['url']}/configureContinueHandler" method="POST">
                <button type="submit" class="btn btn-warning" name="continueToNext">Continue To Next Step</button>
            </form>
        % endif
    </div><!-- row-fluid -->
</%def>
