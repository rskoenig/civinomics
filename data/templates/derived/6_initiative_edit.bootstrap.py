# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398492182.1170261
_template_filename = '/home/maria/civinomics/pylowiki/templates/derived/6_initiative_edit.bootstrap'
_template_uri = '/derived/6_initiative_edit.bootstrap'
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

    # SOURCE LINE 4
    ns = runtime.TemplateNamespace(u'ihelpers', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_initiative_home.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'ihelpers')] = ns

    # SOURCE LINE 3
    ns = runtime.TemplateNamespace(u'dashboard', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_profile_dashboard.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'dashboard')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base/base_initiative.bootstrap', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        ihelpers = _mako_get_namespace(context, 'ihelpers')
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n')
        # SOURCE LINE 3
        __M_writer(u'\n')
        # SOURCE LINE 4
        __M_writer(u'\n\n<div class="row-fluid">\n    ')
        # SOURCE LINE 7
        __M_writer(escape(ihelpers.editInitiative()))
        __M_writer(u'\n</div>\n\n')
        # SOURCE LINE 14
        __M_writer(u'\n\n')
        # SOURCE LINE 31
        __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headScripts(context):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 10
        __M_writer(u'\n    <script src="')
        # SOURCE LINE 11
        __M_writer(escape(lib_6.fingerprintFile('/js/ng/profile_edit.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script src="')
        # SOURCE LINE 12
        __M_writer(escape(lib_6.fingerprintFile('/js/ng/initiative.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script src="')
        # SOURCE LINE 13
        __M_writer(escape(lib_6.fingerprintFile('/js/ng/user_lookup.js')))
        __M_writer(u'" type="text/javascript"></script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraStyles(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 33
        __M_writer(u'\n    <link rel="stylesheet" href="/styles/vendor/jquery.Jcrop.css">\n    <link rel="stylesheet" href="/styles/vendor/blueimp.css">\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraScripts2(context):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 16
        __M_writer(u'\n    <script src="')
        # SOURCE LINE 17
        __M_writer(escape(lib_6.fingerprintFile('/js/vendor/markdown.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script src="')
        # SOURCE LINE 18
        __M_writer(escape(lib_6.fingerprintFile('/js/markdown_preview.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script src="')
        # SOURCE LINE 19
        __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/jquery.ui.widget.js')))
        __M_writer(u'"></script>\n    <script src="')
        # SOURCE LINE 20
        __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/load-image.min.js')))
        __M_writer(u'"></script>\n    <script src="')
        # SOURCE LINE 21
        __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/canvas-to-blob.min.js')))
        __M_writer(u'"></script>\n    <script src="')
        # SOURCE LINE 22
        __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/jquery.iframe-transport.js')))
        __M_writer(u'"></script>\n    <script src="')
        # SOURCE LINE 23
        __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/jquery.fileupload.js')))
        __M_writer(u'"></script>\n    <script src="')
        # SOURCE LINE 24
        __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/jquery.fileupload-process.js')))
        __M_writer(u'"></script>\n    <script src="')
        # SOURCE LINE 25
        __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/jquery.fileupload-resize.js')))
        __M_writer(u'"></script>\n    <script src="')
        # SOURCE LINE 26
        __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/jquery.fileupload-validate.js')))
        __M_writer(u'"></script>\n    <script src="')
        # SOURCE LINE 27
        __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/jquery.fileupload-angular.js')))
        __M_writer(u'"></script>\n    <script src="')
        # SOURCE LINE 28
        __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/app.js')))
        __M_writer(u'"></script>\n    <script src="')
        # SOURCE LINE 29
        __M_writer(escape(lib_6.fingerprintFile('/js/vendor/jquery.Jcrop.js')))
        __M_writer(u'"></script>\n    <script src = "')
        # SOURCE LINE 30
        __M_writer(escape(lib_6.fingerprintFile('/js/geo.js')))
        __M_writer(u'" type="text/javascript"></script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


