# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398642614.566797
_template_filename = '/home/maria/civinomics/pylowiki/templates/derived/6_profile_csv.bootstrap'
_template_uri = '/derived/6_profile_csv.bootstrap'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['headScripts', 'extraScripts', 'extraStyles']


# SOURCE LINE 6

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

    # SOURCE LINE 5
    ns = runtime.TemplateNamespace(u'csv', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_profile_csv.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'csv')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base/base_indented.bootstrap', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        csv = _mako_get_namespace(context, 'csv')
        dashboard = _mako_get_namespace(context, 'dashboard')
        len = context.get('len', UNDEFINED)
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
        # SOURCE LINE 8
        __M_writer(u'\n')
        # SOURCE LINE 10
        __M_writer(u'    <div class="spacer"></div>\n    <div class="row-fluid" ng-controller="ProfileCsvController">\n        <div class="span8">\n            <div class="tabbable">\n                <ul class="nav nav-tabs" id="editTabs">\n                <li class="active"><a href="#tab-edit" data-toggle="tab" class="green green-hover">Upload Users</a></li>\n                <li class="pull-right"><a href="/profile/')
        # SOURCE LINE 16
        __M_writer(escape(c.user['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.user['url']))
        __M_writer(u'">Back to Profile</a></li>\n                </ul>\n                <div class="tab-content">\n                    <div class="tab-pane active" id="tab-edit">\n                        <h3>CSV User uploader</h3>\n                        <p>Here is where I\'ll put all the content related to uploading and showing the CSV</p>\n                        ')
        # SOURCE LINE 22
        __M_writer(escape(csv.uploadCsv()))
        __M_writer(u'\n                    </div><!-- tab-edit -->\n                    <div id="output">\n')
        # SOURCE LINE 25
        if len(c.csv) > 0:
            # SOURCE LINE 26
            __M_writer(u'                    \t')
            __M_writer(escape(csv.showCsv()))
            __M_writer(u'\n                    \t<table>\n\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t  <td><b>Name</b></td>\n\t\t\t\t\t\t\t  <td><b>E-mail</b></td> \n\t\t\t\t\t\t\t  <td><b>Zip</b></td>\n\t\t\t\t\t\t\t</tr>\n')
            # SOURCE LINE 33
            for item in c.csv:
                # SOURCE LINE 34
                __M_writer(u'\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t  <td style="padding-right: 25px; padding-top:10px;">')
                # SOURCE LINE 35
                __M_writer(escape(item['name']))
                __M_writer(u'</td>\n\t\t\t\t\t\t\t  <td style="padding-right: 25px; padding-top:10px;">')
                # SOURCE LINE 36
                __M_writer(escape(item['email']))
                __M_writer(u'</td> \n\t\t\t\t\t\t\t  <td style="padding-right: 25px; padding-top:10px;">')
                # SOURCE LINE 37
                __M_writer(escape(item['zip']))
                __M_writer(u'</td>\n\t\t\t\t\t\t\t</tr>\n')
                pass
            # SOURCE LINE 40
            __M_writer(u'\t\t\t\t\t\t</table>    \n')
            pass
        # SOURCE LINE 42
        __M_writer(u'                    </div><!--output-->\n                </div><!-- tab-content -->\n            </div><!-- tabbable -->\n        </div><!-- span8 -->\n        <div class="span4">\n            ')
        # SOURCE LINE 47
        __M_writer(escape(dashboard.profileDashboard()))
        __M_writer(u'\n        </div><!--/.span4-->\n    </div>\n')
        # SOURCE LINE 51
        __M_writer(u'\n')
        # SOURCE LINE 160
        __M_writer(u'\n\n')
        # SOURCE LINE 182
        __M_writer(u'\n\n')
        # SOURCE LINE 187
        __M_writer(u'\n\n\n')
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
        # SOURCE LINE 162
        __M_writer(u'\n')
        # SOURCE LINE 163
        if 'user' in session:
            # SOURCE LINE 164
            if c.user.id == c.authuser.id or isAdmin(c.authuser.id):
                # SOURCE LINE 165
                __M_writer(u'            <script src="')
                __M_writer(escape(lib_6.fingerprintFile('/js/ng/alerts_admin.js')))
                __M_writer(u'" type="text/javascript"></script>\n            <script src="')
                # SOURCE LINE 166
                __M_writer(escape(lib_6.fingerprintFile('/js/profile.js')))
                __M_writer(u'" type="text/javascript"></script>\n            <script src="')
                # SOURCE LINE 167
                __M_writer(escape(lib_6.fingerprintFile('/js/ng/profile_csv.js')))
                __M_writer(u'" type="text/javascript"></script>\n            <script type="text/javascript" src="ng-grid-1.3.2.js"></script>\n\n')
                pass
            pass
        # SOURCE LINE 172
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
        # SOURCE LINE 52
        __M_writer(u'\n    <script src="')
        # SOURCE LINE 53
        __M_writer(escape(lib_6.fingerprintFile('/js/follow.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script src="')
        # SOURCE LINE 54
        __M_writer(escape(lib_6.fingerprintFile('/js/vendor/jquery.expander.min.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script type="text/javascript">\n        $(document).ready(function() {\n            $(\'.expandable\').expander({\n                slicePoint: 55,\n                widow: 2,\n                expandText: \' ...->\',\n                expandPrefix: \'\',\n                userCollapseText: \' <-\',\n                userCollapsePrefix: \'\',\n                preserveWords: true\n            });\n        });\n    </script>\n')
        # SOURCE LINE 68
        if 'user' in session:
            # SOURCE LINE 69
            if c.user.id == c.authuser.id or isAdmin(c.authuser.id):
                # SOURCE LINE 70
                __M_writer(u'            <script>\n            \t$(document).ready(function() { \n\t\t\t\tvar options = { \n\t\t\t\t    target:   \'#output\',   // target element(s) to be updated with server response \n\t\t\t\t    beforeSubmit:  beforeSubmit,  // pre-submit callback \n\t\t\t\t    uploadProgress: OnProgress, //upload progress callback \n\t\t\t\t    resetForm: true        // reset the form after successful submit \n\t\t\t\t}; \n\t\t\t\t        \n\t\t\t\t $(\'input:file\').change(function() {\n\t\t\t\t \t$("#file_accepted").show();\n\t\t\t\t \tvar filename = $(\'input[type=file]\').val().replace(/C:\\\\fakepath\\\\/i, \'\');\n\t\t\t\t \t$( "#file_accepted" ).prepend( "<p> Your selected file is: "+filename+"</p>" );\n\t\t\t\t \t\n\t\t\t\t}); \n\t\t\t\t\n\t\t\t\t$("#submit_button").click(\n\t\t\t\t\tfunction(){\n\t\t\t\t\t\t$("#status_txt").show();\n\t\t\t\t\t    $(this).ajaxSubmit(options);            \n\t\t\t\t\t    return false; \n\t\t\t\t\t}\t\t\t\t\n\t\t\t\t);\n\t\t\t\t\n\t\t\t\t$("#cancel_button").click(\n\t\t\t\t\tfunction(){\n\t\t\t\t\t\t$("#file_accepted").hide();\n\t\t\t\t\t}\n\t\t\t\t);\n\t\t\t\t});\n\t\t\t\t\n\t\t\t\tfunction beforeSubmit(){\n\t\t   //check whether client browser fully supports all File API\n\t\t   if (window.File && window.FileReader && window.FileList && window.Blob)\n\t\t    {\n\t\t       var fsize = $(\'#FileInput\')[0].files[0].size; //get file size\n\t\t           var ftype = $(\'#FileInput\')[0].files[0].type; // get file type\n\t\t        //allow file types \n\t\t      switch(ftype)\n\t\t           {\n\t\t            case \'application/csv\':\n\t\t            break;\n\t\t            default:\n\t\t             $("#output").html("<b>"+ftype+"</b> Unsupported file type!");\n\t\t         return false\n\t\t           }\n\t\t    \n\t\t       //Allowed file size is less than 5 MB (1048576 = 1 mb)\n\t\t       if(fsize>5242880) \n\t\t       {\n\t\t         alert("<b>"+fsize +"</b> Too big file! <br />File is too big, it should be less than 5 MB.");\n\t\t         return false\n\t\t       }\n\t\t        }\n\t\t        else\n\t\t    {\n\t\t       //Error for older unsupported browsers that doesn\'t support HTML5 File API\n\t\t       alert("Please upgrade your browser, because your current browser lacks some new features we need!");\n\t\t           return false\n\t\t    }\n\t\t}\n\t\tfunction OnProgress(event, position, total, percentComplete)\n\t\t{\n\t\t    //Progress bar\n\t\t    $(\'#progressbox\').show();\n\t\t    $(\'#progressbar\').width(percentComplete + \'%\') //update progressbar percent complete\n\t\t    $(\'#statustxt\').html(percentComplete + \'%\'); //update status text\n\t\t    if(percentComplete>50)\n\t\t        {\n\t\t            $(\'#statustxt\').css(\'color\',\'#000\'); //change status text to white after 50%\n\t\t        }\n\t\t}\n            </script>\n            \n            <script>\n\t\t\t\tvar app = angular.module(\'myApp\', [\'ngGrid\']);\n\t\t\t\tapp.controller(\'MyCtrl\', function($scope) {\n\t\t\t\t    $scope.myData = [{name: "Moroni", age: 50},\n\t\t\t\t                     {name: "Tiancum", age: 43},\n\t\t\t\t                     {name: "Jacob", age: 27},\n\t\t\t\t                     {name: "Nephi", age: 29},\n\t\t\t\t                     {name: "Enos", age: 34}];\n\t\t\t\t    $scope.gridOptions = { \n\t\t\t\t        data: \'myData\',\n\t\t\t\t        columnDefs: [{field:\'name\', displayName:\'Name\'}, {field:\'age\', displayName:\'Age\'}]\n\t\t\t\t    };\n\t\t\t\t});\n            </script>\n')
                pass
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraStyles(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 184
        __M_writer(u'\n    <link rel="stylesheet" href="/styles/vendor/jquery.Jcrop.css">\n    <link rel="stylesheet" href="/styles/vendor/blueimp.css">\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


