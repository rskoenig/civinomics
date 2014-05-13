# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398538074.176877
_template_filename = '/home/maria/civinomics/pylowiki/templates/derived/6_workshop_preferences.bootstrap'
_template_uri = '/derived/6_workshop_preferences.bootstrap'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['headScripts', 'extraStyles', 'extraScripts2']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 2
    ns = runtime.TemplateNamespace(u'lib_6', context._clean_inheritance_tokens(), templateuri=u'/lib/6_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib_6')] = ns

    # SOURCE LINE 6
    ns = runtime.TemplateNamespace(u'slide_helpers', context._clean_inheritance_tokens(), templateuri=u'/lib/admin_helpers/slideshow.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'slide_helpers')] = ns

    # SOURCE LINE 3
    ns = runtime.TemplateNamespace(u'lib', context._clean_inheritance_tokens(), templateuri=u'/lib/mako_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib')] = ns

    # SOURCE LINE 7
    ns = runtime.TemplateNamespace(u'home_helpers', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_workshop_home.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'home_helpers')] = ns

    # SOURCE LINE 4
    ns = runtime.TemplateNamespace(u'helpers', context._clean_inheritance_tokens(), templateuri=u'/lib/admin_helpers/configure.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'helpers')] = ns

    # SOURCE LINE 5
    ns = runtime.TemplateNamespace(u'admin_helpers', context._clean_inheritance_tokens(), templateuri=u'/lib/admin_helpers/workshop.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'admin_helpers')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base/base_workshop.bootstrap', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        slide_helpers = _mako_get_namespace(context, 'slide_helpers')
        lib = _mako_get_namespace(context, 'lib')
        home_helpers = _mako_get_namespace(context, 'home_helpers')
        helpers = _mako_get_namespace(context, 'helpers')
        admin_helpers = _mako_get_namespace(context, 'admin_helpers')
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n')
        # SOURCE LINE 3
        __M_writer(u'\n')
        # SOURCE LINE 4
        __M_writer(u'\n')
        # SOURCE LINE 5
        __M_writer(u'\n')
        # SOURCE LINE 6
        __M_writer(u'\n')
        # SOURCE LINE 7
        __M_writer(u'\n\n')
        # SOURCE LINE 9

        lib.return_to()
        
        basicInfo_active = ""
        participants_active = ""
        tags_active = ""
        slideshow_active = ""
        background_active = ""
        notables_active = ""
        manageWs_active = ""
        eventLog_active = ""
        
        
        if c.tab == "tab1":
            basicInfo_active = "active"
        elif c.tab == "participants":
            participants_active = "active"
        elif c.tab == "tags":
            tags_active = "active"
        elif c.tab == "slideshow":
            slideshow_active = "active"
        elif c.tab == "background":
            background_active = "active"
        elif c.tab == "notables":
            notables_active = "active"
        elif c.tab == "manageWs":
            manageWs_active = "active"
        elif c.tab == "eventLog":
            eventLog_active = "active"
        else:
            if c.w['startTime'] == '0000-00-00':
                basicInfo_active = "active"
            else:
                manageWs_active = "active"
        
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['basicInfo_active','slideshow_active','background_active','notables_active','manageWs_active','eventLog_active','tags_active','participants_active'] if __M_key in __M_locals_builtin_stored]))
        # SOURCE LINE 43
        __M_writer(u'\n<div class="row-fluid">\n    <div class="span9">\n        ')
        # SOURCE LINE 46
        __M_writer(escape(home_helpers.workshopHero()))
        __M_writer(u'\n')
        # SOURCE LINE 47
        if c.conf['read_only.value'] == 'true':
            # SOURCE LINE 48
            __M_writer(u'            <!-- read only -->\n')
            # SOURCE LINE 49
        else:
            # SOURCE LINE 50
            __M_writer(u'            ')
            __M_writer(escape(helpers.fields_alert()))
            __M_writer(u'\n            <div class="tabbable">\n                <div class="tab-content">\n                    <div class="tab-pane ')
            # SOURCE LINE 53
            __M_writer(escape(basicInfo_active))
            __M_writer(u' edit-workshop-pane" id="basicInfo">\n                        ')
            # SOURCE LINE 54
            __M_writer(escape(helpers.basic()))
            __M_writer(u'\n                    </div><!-- tab-pane template basicInfo -->\n                    <div class="tab-pane ')
            # SOURCE LINE 56
            __M_writer(escape(participants_active))
            __M_writer(u' edit-workshop-pane" id="participants">\n                        ')
            # SOURCE LINE 57
            __M_writer(escape(helpers.scope()))
            __M_writer(u'\n                    </div><!-- tab-pane template participants -->\n                    <div class="tab-pane ')
            # SOURCE LINE 59
            __M_writer(escape(tags_active))
            __M_writer(u' edit-workshop-pane" id="tags">\n                        ')
            # SOURCE LINE 60
            __M_writer(escape(helpers.tags()))
            __M_writer(u'\n                    </div><!-- tab-pane template tags -->\n                    <div class="tab-pane ')
            # SOURCE LINE 62
            __M_writer(escape(slideshow_active))
            __M_writer(u' edit-workshop-pane" id="slideshow">\n                        ')
            # SOURCE LINE 63
            __M_writer(escape(slide_helpers.workshop_admin_slideshow()))
            __M_writer(u'\n                    </div><!-- tab-pane template slideshow -->\n                    <div class="tab-pane ')
            # SOURCE LINE 65
            __M_writer(escape(background_active))
            __M_writer(u' edit-workshop-pane" id="background">\n                        ')
            # SOURCE LINE 66
            __M_writer(escape(helpers.edit_background()))
            __M_writer(u'\n                    </div><!-- tab-pane template background -->\n                    <div class="tab-pane ')
            # SOURCE LINE 68
            __M_writer(escape(notables_active))
            __M_writer(u' edit-workshop-pane" id="notables">\n                        <div class="section-wrapper">\n                            <div class="browse">\n                                <h4 class="section-header smaller">Facilitators and Officials</h4>\n                                ')
            # SOURCE LINE 72
            __M_writer(escape(admin_helpers.admin_facilitators()))
            __M_writer(u'\n                                ')
            # SOURCE LINE 73
            __M_writer(escape(admin_helpers.admin_listeners()))
            __M_writer(u'\n                            </div>\n                        </div>\n                    </div><!-- notables -->\n                    <div class="tab-pane ')
            # SOURCE LINE 77
            __M_writer(escape(manageWs_active))
            __M_writer(u'" id="manageWs">\n                        ')
            # SOURCE LINE 78
            __M_writer(escape(admin_helpers.marked_items()))
            __M_writer(u'\n                    </div><!-- manageWs -->\n                    <div class="tab-pane ')
            # SOURCE LINE 80
            __M_writer(escape(eventLog_active))
            __M_writer(u'" id="eventLog">    \n                        ')
            # SOURCE LINE 81
            __M_writer(escape(admin_helpers.admin_event_log()))
            __M_writer(u'\n                    </div><!-- eventLog -->\n')
            # SOURCE LINE 83
            if c.privs['admin']:
                # SOURCE LINE 84
                __M_writer(u'                        <div class="tab-pane" id="admin">\n                            ')
                # SOURCE LINE 85
                __M_writer(escape(admin_helpers.admin()))
                __M_writer(u'\n                        </div>\n')
                pass
            # SOURCE LINE 88
            __M_writer(u'                </div><!-- tab-content -->\n            </div>\n')
            pass
        # SOURCE LINE 91
        __M_writer(u'    </div><!-- span9 -->\n    <div class="span3">\n        <ul class="nav nav-tabs nav-stacked" style="margin-top: 12px; margin-right:0; width: 100%">\n            <li class="')
        # SOURCE LINE 94
        __M_writer(escape(basicInfo_active))
        __M_writer(u'"><a href="#basicInfo" data-toggle="tab">Basic Info\n')
        # SOURCE LINE 95
        if c.basicConfig:
            # SOURCE LINE 96
            __M_writer(u'                <i class="icon-ok pull-right"></i>\n')
            pass
        # SOURCE LINE 98
        __M_writer(u'            </a></li>\n            <li class="')
        # SOURCE LINE 99
        __M_writer(escape(tags_active))
        __M_writer(u'"><a href="#tags" data-toggle="tab">Tags\n')
        # SOURCE LINE 100
        if c.tagConfig:
            # SOURCE LINE 101
            __M_writer(u'                <i class="icon-ok pull-right"></i>\n')
            pass
        # SOURCE LINE 103
        __M_writer(u'            </a></li>\n            <li class="')
        # SOURCE LINE 104
        __M_writer(escape(slideshow_active))
        __M_writer(u'"><a href="#slideshow" data-toggle="tab">Slideshow\n')
        # SOURCE LINE 105
        if c.slideConfig:
            # SOURCE LINE 106
            __M_writer(u'                <i class="icon-ok pull-right"></i>\n')
            pass
        # SOURCE LINE 108
        __M_writer(u'            </a></li>\n            <li class="')
        # SOURCE LINE 109
        __M_writer(escape(background_active))
        __M_writer(u'"><a href="#background" data-toggle="tab">Information\n')
        # SOURCE LINE 110
        if c.backConfig:
            # SOURCE LINE 111
            __M_writer(u'                <i class="icon-ok pull-right"></i>\n')
            pass
        # SOURCE LINE 113
        __M_writer(u'            </a></li>\n            <li class="')
        # SOURCE LINE 114
        __M_writer(escape(participants_active))
        __M_writer(u'"><a href="#participants" data-toggle="tab">Participants\n')
        # SOURCE LINE 115
        if c.participantsConfig:
            # SOURCE LINE 116
            __M_writer(u'                <i class="icon-ok pull-right"></i>\n')
            pass
        # SOURCE LINE 118
        __M_writer(u'            </a></li>\n        </ul>\n')
        # SOURCE LINE 120
        if c.w['startTime'] != '0000-00-00':
            # SOURCE LINE 121
            __M_writer(u'            <ul class="nav nav-tabs nav-stacked" style="margin-top: 10px; margin-right:0; width: 100%">\n                <li class="')
            # SOURCE LINE 122
            __M_writer(escape(manageWs_active))
            __M_writer(u'"><a href="#manageWs" data-toggle="tab">Manage Workshop\n                </a></li>\n                <li class="')
            # SOURCE LINE 124
            __M_writer(escape(notables_active))
            __M_writer(u'"><a href="#notables" data-toggle="tab">Facilitators and Officials\n                </a></li>\n                <li class="')
            # SOURCE LINE 126
            __M_writer(escape(eventLog_active))
            __M_writer(u'"><a href="#eventLog" data-toggle="tab">Event Log\n                </a></li>\n')
            # SOURCE LINE 128
            if c.w['type'] == 'professional' and c.accounts:
                # SOURCE LINE 129
                __M_writer(u'                <!-- <li><a href="/workshop/')
                __M_writer(escape(c.w['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.w['url']))
                __M_writer(u'/manage/account/">Account Management</a></li> -->\n')
                pass
            # SOURCE LINE 131
            if c.privs['admin']:
                # SOURCE LINE 132
                __M_writer(u'                    <li><a href="#admin" data-toggle="tab">Civ admin</a></li>\n')
                pass
            # SOURCE LINE 134
            __M_writer(u'            </ul>\n')
            pass
        # SOURCE LINE 136
        __M_writer(u'        ')
        __M_writer(escape(helpers.publish()))
        __M_writer(u'\n    </div><!-- span3 -->\n</div><!-- row-fluid -->\n    \n\n')
        # SOURCE LINE 145
        __M_writer(u'\n\n')
        # SOURCE LINE 236
        __M_writer(u'\n\n')
        # SOURCE LINE 243
        __M_writer(u'\n\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headScripts(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 238
        __M_writer(u'\n')
        # SOURCE LINE 239
        if c.privs['admin'] or c.privs['facilitator']:
            # SOURCE LINE 240
            __M_writer(u'        <script src="')
            __M_writer(escape(lib_6.fingerprintFile('/js/ng/workshop_admin.js')))
            __M_writer(u'" type="text/javascript"></script>\n        <script src="')
            # SOURCE LINE 241
            __M_writer(escape(lib_6.fingerprintFile('/js/ng/listeners.js')))
            __M_writer(u'" type="text/javascript"></script>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraStyles(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 141
        __M_writer(u'\n    <link type="text/css" rel="stylesheet" href="/styles/vendor/blueimp-bootstrap-image-gallery.min.css">\n    <link type="text/css" rel="stylesheet" href="/styles/jquery.fileupload-ui.css" />\n    <link type="text/css" rel="stylesheet" href="/styles/editSlideshow.css">\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraScripts2(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 147
        __M_writer(u'\n    <script src="/js/bootstrap/bootstrap-collapse.js"></script>\n    <script src="/js/vendor/jquery.ui.widget.js"></script>\n    <script src="/js/vendor/jquery-ui.min.js" type="text/javascript"></script>\n    <script src="/js/jquery.jeditable.mini.js" type="text/javascript"></script>\n    <script src = "/js/jquery.touchwipe.min.js" type="text/javascript"></script>\n    <script src = "')
        # SOURCE LINE 153
        __M_writer(escape(lib_6.fingerprintFile('/js/geo.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <!-- The Templates plugin is included to render the upload/download listings -->\n    <script src="/js/vendor/blueimp-tmpl.min.js"></script>\n    <!-- The Load Image plugin is included for the preview images and image resizing functionality -->\n    <script src="/js/vendor/blueimp-load-image.min.js"></script>\n    <!-- The Canvas to Blob plugin is included for image resizing functionality -->\n    <script src="/js/vendor/blueimp-canvas-to-blob.min.js"></script>\n    <!-- Bootstrap JS and Bootstrap Image Gallery are not required, but included for the demo -->\n    <!-- The Iframe Transport is required for browsers without support for XHR file uploads -->\n    <script src="/js/vendor/blueimp-jquery.iframe-transport.js"></script>\n    <!-- The basic File Upload plugin -->\n    <script src="/js/vendor/blueimp-jquery.fileupload.js"></script>\n    <!-- The File Upload image processing plugin -->\n    <script src="/js/vendor/blueimp-jquery.fileupload-fp.js"></script>\n    <!-- The File Upload user interface plugin -->\n    <script src="/js/vendor/blueimp-jquery.fileupload-ui.js"></script>\n    <!-- The localization script -->\n    <script src="')
        # SOURCE LINE 170
        __M_writer(escape(lib_6.fingerprintFile('/js/locale.js')))
        __M_writer(u'"></script>\n    <!-- The main application script -->\n    <script src="')
        # SOURCE LINE 172
        __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp-main.js')))
        __M_writer(u'"></script>\n    <!-- The XDomainRequest Transport is included for cross-domain file deletion for IE8+ -->\n    <!--[if gte IE 8]><script src="js/cors/jquery.xdr-transport.js"></script><![endif]-->\n    \n    <script language="javascript">\n        $(document).ready(function()\t{\n            $(\'.edit\').editable("/workshop/')
        # SOURCE LINE 178
        __M_writer(escape(c.w['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.w['url']))
        __M_writer(u'/slide/edit", {\n                indicator : \'Saving...\',\n                tooltip   : \'Click to edit...\',\n                submit    : \'OK\',\n                cssclass  : \'editable\'\n            });\n        });\n    </script>\n    <script language="javascript">\n    $(function() {\n        $(".column").sortable(\n            { items: ".portlet" },\n            { connectWith: ".column" },\n            { update: function(event, ui) {\n                $.post("/workshop/')
        # SOURCE LINE 192
        __M_writer(escape(c.w['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.w['url']))
        __M_writer(u'/slide/edit/position", { slides: $(this).sortable(\'serialize\') + "_" + $(this).attr(\'id\')} );\n                if($(this).attr(\'id\') === "unpublished") {\n                    var portletStr = $(this).sortable(\'serialize\');\n                    if(portletStr != "") {\n                        var portletList = portletStr.split("&");\n                        for (var i = 0; i < portletList.length; i++) {\n                            var thisStr = portletList[i];\n                            var portletStrList = thisStr.split("=");\n                            var portletID = "portlet_" + portletStrList[1];\n                            var num_published = document.getElementById("num_published_slides").getAttribute("rel");\n                            if(num_published != "1") {\n                                pElement = document.getElementById(portletID);\n                                pElement.parentNode.removeChild(pElement);\n                                document.getElementById("num_published_slides").setAttribute("rel", num_published - 1);\n                            }\n                        }\n                    }\n                }\n            }\n        });\n\n        $( ".portlet" ).addClass( "ui-widget ui-widget-content ui-helper-clearfix ui-corner-all" )\n            .find( ".portlet-header" )\n                .addClass( "ui-widget-header ui-corner-all" )\n                .prepend( "<span class=\'ui-icon ui-icon-minusthick\'></span>")\n                .end()\n            .find( ".portlet-content" );\n\n        $( ".portlet-title .ui-icon" ).click(function() {\n            $( this ).toggleClass( "ui-icon-minusthick" ).toggleClass( "ui-icon-plusthick" );\n            $( this ).parents( ".portlet:first" ).find( ".portlet-content" ).toggle();\n        });\n\n    });\n    </script>\n    <script type="text/javascript" src="/js/vendor/jquery.foundation.clearing.js"></script>\n    <script>\n      var $doc = $(document);\n      $(document).ready(function() {\n         $.fn.foundationClearing         ? $doc.foundationClearing() : null;\n      });\n    </script>\n    <script src="')
        # SOURCE LINE 234
        __M_writer(escape(lib_6.fingerprintFile('/js/vendor/markdown.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script src="')
        # SOURCE LINE 235
        __M_writer(escape(lib_6.fingerprintFile('/js/markdown_preview.js')))
        __M_writer(u'" type="text/javascript"></script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


