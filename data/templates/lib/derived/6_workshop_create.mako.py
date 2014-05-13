# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398493464.606811
_template_filename = u'/home/maria/civinomics/pylowiki/templates/lib/derived/6_workshop_create.mako'
_template_uri = u'/lib/derived/6_workshop_create.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['createWorkshop']


# SOURCE LINE 1

import logging
log = logging.getLogger(__name__)


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 4
        __M_writer(u'\n\n')
        # SOURCE LINE 33
        __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_createWorkshop(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 6
        __M_writer(u'\n    <div class="row-fluid">\n        <form id="CreateWorkshop" action = "/workshop/create/handler" class="form-vertical" method = "post">\n            <div class="span6">\n                <ul class="well orange pricing-table">\n                    <li class="title"><h3>Private</h3><i class="icon-group icon-4x"></i></li>\n                    <li class="price">Only people you invite can participate</li>\n                    <li class="description"> Totally free! </li>\n                    <li class="bullet-item"> Unlimited members </li>\n                    <li class="cta-button"> \n                        <button type="submit" name="createPrivate" class="btn btn-large btn-civ">Go Private</button>\n                    </li>\n                </ul>\n            </div> <!-- /.span6 -->\n            <div class="span6">\n                <ul class="well purple pricing-table ">\n                    <li class="title"><h3>Public</h3><i class="icon-globe icon-4x"></i></li>\n                    <li class="price">Anyone can participate</li>\n                    <li class="description"> Totally free! </li>\n                    <li class="bullet-item"> Unlimited members </li>\n                    <li class="cta-button"> \n                        <button type="submit" name="createPublic" class="btn btn-large btn-civ">Go Public</button>\n                    </li>\n                </ul>\n            </div> <!-- /.span6 -->\n        </form>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


