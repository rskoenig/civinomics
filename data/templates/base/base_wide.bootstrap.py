# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398492171.7257619
_template_filename = u'/home/maria/civinomics/pylowiki/templates/base/base_wide.bootstrap'
_template_uri = u'/base/base_wide.bootstrap'
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
    ns = runtime.TemplateNamespace(u'helpers', context._clean_inheritance_tokens(), templateuri=u'/lib/template_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'helpers')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base/base.bootstrap', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        helpers = _mako_get_namespace(context, 'helpers')
        next = context.get('next', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n\n<div id="wrap-wide">\n   ')
        # SOURCE LINE 5
        __M_writer(escape(helpers.mainNavbar()))
        __M_writer(u'\n   <div class="container wide slate">\n      ')
        # SOURCE LINE 7
        __M_writer(escape(next.body()))
        __M_writer(u'\n   </div>\n</div><!-- close wrap -->\n')
        # SOURCE LINE 10
        __M_writer(escape(helpers.signupLoginModal()))
        return ''
    finally:
        context.caller_stack._pop_frame()


