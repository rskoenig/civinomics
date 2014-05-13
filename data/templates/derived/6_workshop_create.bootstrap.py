# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398493464.600148
_template_filename = '/home/maria/civinomics/pylowiki/templates/derived/6_workshop_create.bootstrap'
_template_uri = '/derived/6_workshop_create.bootstrap'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = []


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

    # SOURCE LINE 3
    ns = runtime.TemplateNamespace(u'helpers', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_workshop_create.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'helpers')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base/base_indented.bootstrap', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        helpers = _mako_get_namespace(context, 'helpers')
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n')
        # SOURCE LINE 3
        __M_writer(u'\n\n<div class="row">\n    <div class="span12">\n        <div class="section-wrapper">\n            <div class="browse">\n                <h3 class="section-header centered">Create A New Workshop</h3>\n')
        # SOURCE LINE 10
        if c.conf['read_only.value'] == 'true':
            # SOURCE LINE 11
            __M_writer(u'                    <!-- read only -->\n                    <p>Sorry, Civinomics is in read-only mode right now!</p>\n')
            # SOURCE LINE 13
        else:
            # SOURCE LINE 14
            __M_writer(u'                    ')
            __M_writer(escape(helpers.createWorkshop()))
            __M_writer(u'\n')
            pass
        # SOURCE LINE 16
        __M_writer(u'            </div><!-- browse -->\n        </div><!-- section-wrapper -->\n    </div>\n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


