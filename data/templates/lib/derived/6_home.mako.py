# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398492171.7219081
_template_filename = u'/home/maria/civinomics/pylowiki/templates/lib/derived/6_home.mako'
_template_uri = u'/lib/derived/6_home.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['homeSlide']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 1
    ns = runtime.TemplateNamespace(u'workshopHelpers', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_workshop_home.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'workshopHelpers')] = ns

def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_homeSlide(context,item):
    context.caller_stack._push_frame()
    try:
        workshopHelpers = _mako_get_namespace(context, 'workshopHelpers')
        __M_writer = context.writer()
        # SOURCE LINE 4
        __M_writer(u'\n\t<div class="span wrap-voting-group-slide" style="background-image:url(\'')
        # SOURCE LINE 5
        __M_writer(escape(item['photo']))
        __M_writer(u'\'); background-size: cover; background-position: center center;">\n\t  <a href="')
        # SOURCE LINE 6
        __M_writer(escape(item['link']))
        __M_writer(u'">\n\t    <span class="link-span dark-gradient"></span><!-- used to make entire div a link -->\n\t    <div class="row-fluid tile-title lead">Featured Workshop</div>\n\t    <div class="row-fluid featured">\n\t    \t<table class="featured-title">\n\t            <tr>\n\t              <td>\n\t                <span>')
        # SOURCE LINE 13
        __M_writer(escape(item['title']))
        __M_writer(u'</span><br>\n\t     \t\t\t')
        # SOURCE LINE 14
        __M_writer(escape(workshopHelpers.displayWorkshopFlag(item['item'], 'small')))
        __M_writer(u'<span class="featured-scope-title lead">')
        __M_writer(escape(item['scopeTitle']))
        __M_writer(u'</span>\n\t              </td>\n\t            </tr>\n\t         </table>\n\t    </div>\n\t  </a>\n\t</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


