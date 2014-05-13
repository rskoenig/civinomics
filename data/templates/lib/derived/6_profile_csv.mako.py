# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398640207.954622
_template_filename = u'/home/maria/civinomics/pylowiki/templates/lib/derived/6_profile_csv.mako'
_template_uri = u'/lib/derived/6_profile_csv.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['uploadCsv', 'showCsv']


# SOURCE LINE 1

import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.facilitator  as facilitatorLib
import pylowiki.lib.db.listener     as listenerLib
import pylowiki.lib.db.follow       as followLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.pmember      as pmemberLib
import pylowiki.lib.db.photo        as photoLib
import pylowiki.lib.db.event        as eventLib
import pylowiki.lib.utils           as utils
import pylowiki.lib.db.geoInfo      as geoLib


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 14
    ns = runtime.TemplateNamespace(u'lib_6', context._clean_inheritance_tokens(), templateuri=u'/lib/6_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib_6')] = ns

def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 12
        __M_writer(u'\n\n')
        # SOURCE LINE 14
        __M_writer(u'\n\n')
        # SOURCE LINE 60
        __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_uploadCsv(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 16
        __M_writer(u'\n')
        # SOURCE LINE 17
        if 'user' in session and (c.authuser.id == c.user.id) and not c.privs['provisional']:
            # SOURCE LINE 18
            __M_writer(u'        <form id="fileupload" action="/profile/')
            __M_writer(escape(c.authuser['urlCode']))
            __M_writer(u'/')
            __M_writer(escape(c.authuser['url']))
            __M_writer(u'/csv/upload/handler" method="POST" enctype="multipart/form-data">\n            <div id="fileinput-button-div" class="row-fluid fileupload-buttonbar collapse in">\n                <div class="span10 offset1">\n                    <!-- The fileinput-button span is used to style the file input field as button -->\n                    <span class="pull-left">Upload the CSV with the information on the users.  (5MB max, please)</span>\n                    <span class="btn btn-success fileinput-button pull-right">\n                        <i class="icon-plus icon-white"></i>\n                        <span>CSV</span>\n                        <input id="fileUploadButton" type="file" name="files[]">\n                    </span>\n                    \n                    <!-- The loading indicator is shown during file processing -->\n                    <div class="fileupload-loading">\n\t                    \n                    </div>\n                </div><!-- span10 -->\n                <!-- The global progress information -->\n            </div><!-- row-fluid -->\n            <div class="row-fluid">\n                <div class="span10 offset1 fade">\n                    <!-- The global progress bar -->\n                    <div class="progress progress-success progress-striped"><div class="bar" ng-style="{width: num + \'%\'}"></div></div>\n                    <!-- The extended global progress information -->\n                    <div class="progress-extended">&nbsp;</div>\n                </div><!- span10 -->\n            </div><!-- row-fluid -->\n            <div id="progressbox" >\n            <div id="file_accepted" style="display:none">\n            \t\t\t<button type="submit" id="submit_button" type="submit" class="btn btn-primary start" value="process">\n                        <i class="icon-upload icon-white"></i>\n                        <span>Process</span>\n                        </button>\n\n\t\t\t\t\t\t<button id="cancel_button" type="button" class="btn btn-warning cancel" >\n                        <i class="icon-ban-circle icon-white"></i>\n                        <span>Cancel</span>\n                        </button>\n            <div id="progressbar"></div >\n\t\t\t</div>\n            </div><!--file_accepted-->\n        </form>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showCsv(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 62
        __M_writer(u'\n\t<div ng-app="myApp">\n\t\t<div ng-controller="MyCtrl">\n\t\t\t<div ng-grid="gridOptions">\n\t\t\t</div>\n\t\t</div>\n\t</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


