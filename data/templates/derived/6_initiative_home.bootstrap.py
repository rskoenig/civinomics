# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398492321.05358
_template_filename = '/home/maria/civinomics/pylowiki/templates/derived/6_initiative_home.bootstrap'
_template_uri = '/derived/6_initiative_home.bootstrap'
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
    # SOURCE LINE 4
    ns = runtime.TemplateNamespace('__anon_0x4200b10', context._clean_inheritance_tokens(), templateuri=u'/lib/6_comments.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, '__anon_0x4200b10')] = ns

    # SOURCE LINE 2
    ns = runtime.TemplateNamespace(u'lib_6', context._clean_inheritance_tokens(), templateuri=u'/lib/6_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib_6')] = ns

    # SOURCE LINE 3
    ns = runtime.TemplateNamespace(u'ihelpers', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_initiative_home.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'ihelpers')] = ns

    # SOURCE LINE 5
    ns = runtime.TemplateNamespace(u'lib', context._clean_inheritance_tokens(), templateuri=u'/lib/mako_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base/base_initiative.bootstrap', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x4200b10')._populate(_import_ns, [u'comments'])
        c = _import_ns.get('c', context.get('c', UNDEFINED))
        ihelpers = _mako_get_namespace(context, 'ihelpers')
        comments = _import_ns.get('comments', context.get('comments', UNDEFINED))
        lib = _mako_get_namespace(context, 'lib')
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
        __M_writer(u'\n\n')
        # SOURCE LINE 7
        lib.return_to() 
        
        __M_writer(u'\n    <h4 class="initiative-title">Summary</h4>\n    ')
        # SOURCE LINE 9
        __M_writer(escape(ihelpers.showDescription()))
        __M_writer(u'\n    ')
        # SOURCE LINE 10
        __M_writer(escape(ihelpers.showUpdateList()))
        __M_writer(u'\n    <h4 class="initiative-title">Estimate Net Fiscal Impact</h4>\n    ')
        # SOURCE LINE 12
        __M_writer(escape(ihelpers.showFunding_Summary()))
        __M_writer(u'\n    ')
        # SOURCE LINE 13
        __M_writer(escape(ihelpers.showCost(c.initiative)))
        __M_writer(u'\n    <br>\n    <hr>\n    <h4 class="initiative-title">Background</h4>\n    ')
        # SOURCE LINE 17
        __M_writer(escape(ihelpers.showBackground()))
        __M_writer(u'\n    <h4 class="initiative-title">Proposal</h4>\n    ')
        # SOURCE LINE 19
        __M_writer(escape(ihelpers.showProposal()))
        __M_writer(u'\n\n\n')
        # SOURCE LINE 22
        if c.initiative.objType == 'revision':
            # SOURCE LINE 23
            __M_writer(u'        This is a revision dated ')
            __M_writer(escape(c.initiative.date))
            __M_writer(u'<br />\n')
            # SOURCE LINE 24
        else:
            # SOURCE LINE 25
            __M_writer(u'        ')
            __M_writer(escape(ihelpers.initiativeModerationPanel(c.initiative)))
            __M_writer(u'\n        <hr>\n        <h4 class="initiative-title">Informational Resources')
            # SOURCE LINE 27
            __M_writer(escape(ihelpers.addResourceButton()))
            __M_writer(u'</h4>\n        ')
            # SOURCE LINE 28
            __M_writer(escape(ihelpers.listResources()))
            __M_writer(u'\n        <br>\n')
            # SOURCE LINE 30
            if c.initiative.objType != 'initiativeUnpublished':
                # SOURCE LINE 31
                __M_writer(u'            <hr>\n            <h4 class="initiative-title">Arguments</h4>\n            ')
                # SOURCE LINE 33
                __M_writer(escape(comments(c.initiative, c.discussion)))
                __M_writer(u'\n')
                pass
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


