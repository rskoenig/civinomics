# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398542813.703161
_template_filename = '/home/maria/civinomics/pylowiki/templates/derived/6_profile_edit.bootstrap'
_template_uri = '/derived/6_profile_edit.bootstrap'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['headScripts', 'extraScripts', 'extraStyles']


# SOURCE LINE 5

from pylowiki.lib.db.user import isAdmin


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 4
    ns = runtime.TemplateNamespace(u'edit', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_profile_edit.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'edit')] = ns

    # SOURCE LINE 2
    ns = runtime.TemplateNamespace(u'lib_6', context._clean_inheritance_tokens(), templateuri=u'/lib/6_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib_6')] = ns

    # SOURCE LINE 3
    ns = runtime.TemplateNamespace(u'dashboard', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_profile_dashboard.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'dashboard')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base/base_indented.bootstrap', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        edit = _mako_get_namespace(context, 'edit')
        c = context.get('c', UNDEFINED)
        dashboard = _mako_get_namespace(context, 'dashboard')
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n')
        # SOURCE LINE 3
        __M_writer(u'\n')
        # SOURCE LINE 4
        __M_writer(u'\n')
        # SOURCE LINE 7
        __M_writer(u'\n')
        # SOURCE LINE 9
        __M_writer(u'    <div class="spacer"></div>\n    <div class="row-fluid" ng-controller="ProfileEditController">\n        <div class="span8">\n            <div class="tabbable">\n                <ul class="nav nav-tabs" id="editTabs">\n                <li class="active"><a href="#tab-edit" data-toggle="tab" class="green green-hover">Edit Profile</a></li>\n                <li class="pull-right"><a href="/profile/')
        # SOURCE LINE 15
        __M_writer(escape(c.user['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.user['url']))
        __M_writer(u'">Back to Profile</a></li>\n                </ul>\n                <div class="tab-content">\n                    <div class="tab-pane active" id="tab-edit">\n                        ')
        # SOURCE LINE 19
        __M_writer(escape(edit.editProfile()))
        __M_writer(u'\n                    </div><!-- tab-edit -->\n                </div><!-- tab-content -->\n            </div><!-- tabbable -->\n        </div><!-- span8 -->\n        <div class="span4">\n            ')
        # SOURCE LINE 25
        __M_writer(escape(dashboard.profileDashboard()))
        __M_writer(u'\n        </div><!--/.span4-->\n    </div>\n')
        # SOURCE LINE 29
        __M_writer(u'\n')
        # SOURCE LINE 66
        __M_writer(u'\n\n')
        # SOURCE LINE 86
        __M_writer(u'\n\n')
        # SOURCE LINE 91
        __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headScripts(context):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 68
        __M_writer(u'\n')
        # SOURCE LINE 69
        if 'user' in session:
            # SOURCE LINE 70
            if c.user.id == c.authuser.id or isAdmin(c.authuser.id):
                # SOURCE LINE 71
                __M_writer(u'            <script src="')
                __M_writer(escape(lib_6.fingerprintFile('/js/ng/alerts_admin.js')))
                __M_writer(u'" type="text/javascript"></script>\n            <script src="')
                # SOURCE LINE 72
                __M_writer(escape(lib_6.fingerprintFile('/js/profile.js')))
                __M_writer(u'" type="text/javascript"></script>\n            <script src="')
                # SOURCE LINE 73
                __M_writer(escape(lib_6.fingerprintFile('/js/ng/profile_edit.js')))
                __M_writer(u'" type="text/javascript"></script>\n')
                pass
            pass
        # SOURCE LINE 76
        __M_writer(u'    <script src="')
        __M_writer(escape(lib_6.fingerprintFile('/js/bootstrap/bootstrap-tab.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script>\n        $(function () {\n            if(location.hash && location.hash.match(/tab-edit/)) {\n                $(\'#profileTabs a[href="#tab-edit"]\').tab(\'show\');\n            } else {\n                $(\'#profileTabs a:first\').tab(\'show\');\n            }\n        });\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraScripts(context):
    context.caller_stack._push_frame()
    try:
        session = context.get('session', UNDEFINED)
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 30
        __M_writer(u'\n    <script src="')
        # SOURCE LINE 31
        __M_writer(escape(lib_6.fingerprintFile('/js/follow.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script src="')
        # SOURCE LINE 32
        __M_writer(escape(lib_6.fingerprintFile('/js/vendor/jquery.expander.min.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script type="text/javascript">\n        $(document).ready(function() {\n            $(\'.expandable\').expander({\n                slicePoint: 55,\n                widow: 2,\n                expandText: \' ...->\',\n                expandPrefix: \'\',\n                userCollapseText: \' <-\',\n                userCollapsePrefix: \'\',\n                preserveWords: true\n            });\n        });\n    </script>\n')
        # SOURCE LINE 46
        if 'user' in session:
            # SOURCE LINE 47
            if c.user.id == c.authuser.id or isAdmin(c.authuser.id):
                # SOURCE LINE 48
                __M_writer(u'            <script src="')
                __M_writer(escape(lib_6.fingerprintFile('/js/geo.js')))
                __M_writer(u'" type="text/javascript"></script>\n            \n            \n            <script src="')
                # SOURCE LINE 51
                __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/jquery.ui.widget.js')))
                __M_writer(u'"></script>\n            <script src="')
                # SOURCE LINE 52
                __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/load-image.min.js')))
                __M_writer(u'"></script>\n            <script src="')
                # SOURCE LINE 53
                __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/canvas-to-blob.min.js')))
                __M_writer(u'"></script>\n')
                # SOURCE LINE 56
                __M_writer(u'            <script src="')
                __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/jquery.fileupload.js')))
                __M_writer(u'"></script>\n            <script src="')
                # SOURCE LINE 57
                __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/jquery.fileupload-process.js')))
                __M_writer(u'"></script>\n            <script src="')
                # SOURCE LINE 58
                __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/jquery.fileupload-resize.js')))
                __M_writer(u'"></script>\n            <script src="')
                # SOURCE LINE 59
                __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/jquery.fileupload-validate.js')))
                __M_writer(u'"></script>\n            <script src="')
                # SOURCE LINE 60
                __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/jquery.fileupload-angular.js')))
                __M_writer(u'"></script>\n            <script src="')
                # SOURCE LINE 61
                __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/app.js')))
                __M_writer(u'"></script>\n            <script src="')
                # SOURCE LINE 62
                __M_writer(escape(lib_6.fingerprintFile('/js/vendor/jquery.Jcrop.js')))
                __M_writer(u'"></script>\n')
                pass
            pass
        # SOURCE LINE 65
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraStyles(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 88
        __M_writer(u'\n    <link rel="stylesheet" href="/styles/vendor/jquery.Jcrop.css">\n    <link rel="stylesheet" href="/styles/vendor/blueimp.css">\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


