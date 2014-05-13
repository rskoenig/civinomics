# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398538074.2162941
_template_filename = u'/home/maria/civinomics/pylowiki/templates/lib/admin_helpers/slideshow.mako'
_template_uri = u'/lib/admin_helpers/slideshow.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['add_slides', 'edit_slideshow', 'workshop_admin_slideshow']


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<!--\n/*\n * jQuery File Upload Plugin Demo 6.5.1\n * https://github.com/blueimp/jQuery-File-Upload\n *\n * Copyright 2010, Sebastian Tschan\n * https://blueimp.net\n *\n * Licensed under the MIT license:\n * http://www.opensource.org/licenses/MIT\n */\n-->\n\n')
        # SOURCE LINE 29
        __M_writer(u'\n\n')
        # SOURCE LINE 160
        __M_writer(u'\n\n')
        # SOURCE LINE 213
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_add_slides(context,parent):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 31
        __M_writer(u'\n    <!-- The file upload form used as target for the file upload widget -->\n    <form id="fileupload" action="/workshop/')
        # SOURCE LINE 33
        __M_writer(escape(c.w['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.w['url']))
        __M_writer(u'/addImages/handler" method="POST" enctype="multipart/form-data">\n    <!-- The fileupload-buttonbar contains buttons to add/delete files and start/cancel the upload -->\n    <div class="row-fluid">\n        <div class="span7 fileupload-buttonbar">\n            <!-- The fileinput-button span is used to style the file input field as button -->\n            <span class="btn btn-success fileinput-button">\n                <i class="icon-plus icon-white"></i>\n                <span>Add images...</span>\n                <input type="file" name="files[]" multiple>\n            </span>\n            <button type="submit" class="btn btn-primary start">\n                <i class="icon-upload icon-white"></i>\n                <span>Start upload</span>\n            </button>\n            <button type="reset" class="btn btn-danger cancel">\n                <i class="icon-ban-circle icon-white"></i>\n                <span>Cancel upload</span>\n            </button>\n        </div><!-- span7 -->\n        <div class="span4">\n            <!-- The global progress bar -->\n            <div class="progress progress-success progress-striped active fade">\n                <div class="bar" style="width:0%;"></div>\n            </div><!-- progress -->\n        </div><!-- span4 -->\n    </div><!-- row-fluid -->\n    <div class="row-fluid">\n        <div class="span12">\n            <!-- The loading indicator is shown during image processing -->\n            <div class="fileupload-loading"></div>\n            <br>\n            <!-- The table listing the files available for upload/download -->\n            <table class="table table-striped"><tbody class="files" data-toggle="modal-gallery" data-target="#modal-gallery"></tbody></table>\n            <br />\n        </div><!-- span12 -->\n    </div><!-- row-fluid -->\n\n    <!-- modal-gallery is the modal dialog used for the image gallery -->\n    <div id="modal-gallery" class="modal modal-gallery hide fade">\n        <div class="modal-header">\n            <a class="close" data-dismiss="modal">&times;</a>\n            <h3 class="modal-title"></h3>\n        </div><!-- modal-header -->\n        <div class="modal-body"><div class="modal-image"></div></div>\n        <div class="modal-footer">\n            <a class="btn modal-download" target="_blank">\n                <i class="icon-download"></i>\n                <span>Download</span>\n            </a>\n            <a class="btn btn-success modal-play modal-slideshow" data-slideshow="5000">\n                <i class="icon-play icon-white"></i>\n                <span>Slideshow</span>\n            </a>\n            <a class="btn btn-info modal-prev">\n                <i class="icon-arrow-left icon-white"></i>\n                <span>Previous</span>\n            </a>\n            <a class="btn btn-primary modal-next">\n                <span>Next</span>\n                <i class="icon-arrow-right icon-white"></i>\n            </a>\n        </div><!-- modal-footer -->\n    </div><!-- modal-gallery -->\n    </form>\n\n<!-- The template to display files available for upload -->\n<script id="template-upload" type="text/x-tmpl">\n{% for (var i=0, file; file=o.files[i]; i++) { %}\n    <tr class="template-upload fade">\n        <td class="preview"><span class="fade"></span></td>\n        <td class="name"><span>{%=file.name%}</span></td>\n        <td class="size"><span>{%=o.formatFileSize(file.size)%}</span></td>\n        {% if (file.error) { %}\n            <td class="error" colspan="2"><span class="label label-important">{%=locale.fileupload.error%}</span> {%=locale.fileupload.errors[file.error] || file.error%}</td>\n        {% } else if (o.files.valid && !i) { %}\n            <td>\n                <div class="progress progress-success progress-striped active"><div class="bar" style="width:0%;"></div></div>\n            </td>\n            <td class="start">{% if (!o.options.autoUpload) { %}\n                <!-- <button class="btn btn-primary">\n                    <i class="icon-upload icon-white"></i>\n                    <span>{%=locale.fileupload.start%}</span>\n                </button> -->\n            {% } %}</td>\n        {% } else { %}\n            <td colspan="2"></td>\n        {% } %}\n        <td class="cancel">{% if (!i) { %}\n            <button class="btn btn-danger">\n                <i class="icon-ban-circle icon-white"></i>\n                <span>{%=locale.fileupload.cancel%}</span>\n            </button>\n        {% } %}</td>\n    </tr>\n{% } %}\n</script>\n\n<!-- The template to display files available for download -->\n<script id="template-download" type="text/x-tmpl">\n{% for (var i=0, file; file=o.files[i]; i++) { %}\n    <tr class="template-download fade">\n        {% if (file.error) { %}\n            <td></td>\n            <td class="name"><span>{%=file.name%}</span></td>\n            <td class="size"><span>{%=o.formatFileSize(file.size)%}</span></td>\n            <td class="error" colspan="2"><span class="label label-important">{%=locale.fileupload.error%}</span> {%=locale.fileupload.errors[file.error] || file.error%}</td>\n        {% } else { %}\n            <td class="preview">{% if (file.thumbnail_url) { %}\n                <a href="{%=file.url%}" title="{%=file.name%}" rel="gallery" download="{%=file.name%}"><img src="{%=file.thumbnail_url%}"></a>\n            {% } %}</td>\n            <td class="name">\n                <a href="{%=file.url%}" title="{%=file.name%}" rel="{%=file.thumbnail_url&&\'gallery\'%}" download="{%=file.name%}">{%=file.name%}</a>\n            </td>\n            <td class="size"><span>{%=o.formatFileSize(file.size)%}</span></td>\n            <td colspan="2"></td>\n        {% } %}\n        <td class="delete">\n            <button class="btn btn-danger" data-type="{%=file.delete_type%}" data-url="{%=file.delete_url%}">\n                <i class="icon-trash icon-white"></i>\n                <span>{%=locale.fileupload.destroy%}</span>\n            </button>\n            <input type="checkbox" name="delete" value="1">\n        </td>\n    </tr>\n{% } %}\n</script>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_edit_slideshow(context):
    context.caller_stack._push_frame()
    try:
        int = context.get('int', UNDEFINED)
        c = context.get('c', UNDEFINED)
        str = context.get('str', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 162
        __M_writer(u'\n    <div class="row-fluid">\n        <p><strong>Edit Slideshow</strong></p>\n        <ul>\n            <li>Click and drag to rearrange images</li>\n            <li>Add captions</li>\n            <li>Drag images to Trash to delete</li>\n        </ul>\n')
        # SOURCE LINE 170
        if c.w['startTime'] == '0000-00-00':
            # SOURCE LINE 171
            __M_writer(u'            <form name="continueToNext" id="continueToNext" action="/workshop/')
            __M_writer(escape(c.w['urlCode']))
            __M_writer(u'/')
            __M_writer(escape(c.w['url']))
            __M_writer(u'/configureContinueHandler" method="POST">\n                <button type="submit" class="btn btn-warning" name="continueToNext">Save Slideshow and Continue</button>\n            </form>\n')
            pass
        # SOURCE LINE 175
        __M_writer(u'        <div class="demo">\n            <div class="column" id="published">\n                <h4 class="centered">Published slides</h4 >\n                <div id="num_published_slides" rel="')
        # SOURCE LINE 178
        __M_writer(escape(str(len(c.published_slides))))
        __M_writer(u'"></div>\n')
        # SOURCE LINE 179
        for slide in c.published_slides:
            # SOURCE LINE 180
            if int(slide['deleted']) == 0:
                # SOURCE LINE 181
                __M_writer(u'                        <div class="portlet" id = "portlet_')
                __M_writer(escape(slide.id))
                __M_writer(u'">\n                            <div class = "portlet-title edit" id = "')
                # SOURCE LINE 182
                __M_writer(escape(slide.id))
                __M_writer(u'_title">')
                __M_writer(escape(slide['title']))
                __M_writer(u'</div>\n                            <div class = "portlet-image">\n')
                # SOURCE LINE 184
                if slide['pictureHash'] == 'supDawg':
                    # SOURCE LINE 185
                    __M_writer(u'                                    <img src = "/images/slide/thumbnail/supDawg.thumbnail">\n')
                    # SOURCE LINE 186
                else:
                    # SOURCE LINE 187
                    __M_writer(u'                                    <img src = "/images/slide/')
                    __M_writer(escape(slide['directoryNum']))
                    __M_writer(u'/thumbnail/')
                    __M_writer(escape(slide['pictureHash']))
                    __M_writer(u'.png" class="image-thumbnail">\n')
                    pass
                # SOURCE LINE 189
                __M_writer(u'                            </div><!-- portlet-image -->\n                        </div><!-- portlet -->\n')
                pass
            pass
        # SOURCE LINE 193
        __M_writer(u'            </div><!-- column -->\n            <div class="column trashbasket" id="unpublished">\n                <h4 class="unsortable centered">Trash</h4>\n')
        # SOURCE LINE 196
        for slide in c.deleted_slides:
            # SOURCE LINE 197
            if int(slide['deleted']) == 1:
                # SOURCE LINE 198
                __M_writer(u'                        <div class="portlet" id = "portlet_')
                __M_writer(escape(slide.id))
                __M_writer(u'">\n                            <div class = "portlet-title edit" id = "')
                # SOURCE LINE 199
                __M_writer(escape(slide.id))
                __M_writer(u'_title">')
                __M_writer(escape(slide['title']))
                __M_writer(u'</div>\n                            <div class = "portlet-image">\n')
                # SOURCE LINE 201
                if slide['pictureHash'] == 'supDawg':
                    # SOURCE LINE 202
                    __M_writer(u'                                    <img src = "/images/slide/thumbnail/supDawg.thumbnail">\n')
                    # SOURCE LINE 203
                else:
                    # SOURCE LINE 204
                    __M_writer(u'                                    <img src = "/images/slide/')
                    __M_writer(escape(slide['directoryNum']))
                    __M_writer(u'/thumbnail/')
                    __M_writer(escape(slide['pictureHash']))
                    __M_writer(u'.jpg" class="image-thumbnail">\n')
                    pass
                # SOURCE LINE 206
                __M_writer(u'                            </div><!-- portlet-image -->\n                        </div><!-- portlet -->\n')
                pass
            pass
        # SOURCE LINE 210
        __M_writer(u'            </div><!-- column -->\n        </div><!-- End demo -->\n    </div><!-- row-fluid -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_workshop_admin_slideshow(context):
    context.caller_stack._push_frame()
    try:
        def add_slides(parent):
            return render_add_slides(context,parent)
        c = context.get('c', UNDEFINED)
        def edit_slideshow():
            return render_edit_slideshow(context)
        __M_writer = context.writer()
        # SOURCE LINE 14
        __M_writer(u'    \n    <div class="section-wrapper">\n        <div class="browse">\n            <h4 class="section-header smaller">Slideshow</h4>\n            ')
        # SOURCE LINE 18
        __M_writer(escape(add_slides(c.w)))
        __M_writer(u'\n            ')
        # SOURCE LINE 19
        __M_writer(escape(edit_slideshow()))
        __M_writer(u'\n')
        # SOURCE LINE 20
        if c.w['startTime'] == '0000-00-00':
            # SOURCE LINE 21
            __M_writer(u'                <div class="row-fluid">\n                    <form name="continueToNext" id="continueToNext" action="/workshop/')
            # SOURCE LINE 22
            __M_writer(escape(c.w['urlCode']))
            __M_writer(u'/')
            __M_writer(escape(c.w['url']))
            __M_writer(u'/configureContinueHandler" method="POST">\n                    <button type="submit" class="btn btn-warning" name="continueToNext">Continue To Next Step</button>\n                    </form>\n                </div><!-- row-fluid -->\n')
            pass
        # SOURCE LINE 27
        __M_writer(u'        </div><!-- browse -->\n    </div><!-- section-wrapper -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


