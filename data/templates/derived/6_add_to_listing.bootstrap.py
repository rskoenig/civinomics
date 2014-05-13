# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398544350.619761
_template_filename = '/home/maria/civinomics/pylowiki/templates/derived/6_add_to_listing.bootstrap'
_template_uri = '/derived/6_add_to_listing.bootstrap'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['additionalInfo', 'headScripts', 'addResource', 'addDiscussion', 'addListing', 'addIdea', 'submitButton', 'extraScripts2']


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
    ns = runtime.TemplateNamespace(u'helpers', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_detailed_listing.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'helpers')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base/base_workshop.bootstrap', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n')
        # SOURCE LINE 3
        __M_writer(u'\n\n')
        # SOURCE LINE 5
 
        self.addListing(c.listingType)
        
        
        # SOURCE LINE 7
        __M_writer(u'\n\n')
        # SOURCE LINE 33
        __M_writer(u'\n\n')
        # SOURCE LINE 46
        __M_writer(u'\n\n')
        # SOURCE LINE 72
        __M_writer(u'\n\n')
        # SOURCE LINE 84
        __M_writer(u'\n\n')
        # SOURCE LINE 90
        __M_writer(u'\n\n')
        # SOURCE LINE 99
        __M_writer(u'\n\n')
        # SOURCE LINE 119
        __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_additionalInfo(context,name='text'):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 92
        __M_writer(u'\n   <fieldset>\n      <label><strong>Additional information</strong><br>\n      <a href="#" class="btn btn-mini btn-info" onclick="window.open(\'/help/markdown.html\',\'popUpWindow\',\'height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes\');"><i class="icon-list"></i> <i class="icon-photo"></i> View Formatting Guide</a></label>\n      <textarea name="')
        # SOURCE LINE 96
        __M_writer(escape(name))
        __M_writer(u'" rows="3" class="input-block-level" ng-model="')
        __M_writer(escape(name))
        __M_writer(u'"></textarea>\n      <span class="help-block"> (Any additional information you want to include.  This is optional.) </span>\n   </fieldset>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headScripts(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 121
        __M_writer(u'\n    <script src="/js/ng/resource.js" type="text/javascript"></script> \n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_addResource(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 48
        __M_writer(u'\n    ')
        # SOURCE LINE 49
 
        if c.w:
            type = "workshop"
            parent = c.w
        elif c.initiative:
            type = 'initiative'
            parent = c.initiative
            
        
        # SOURCE LINE 56
        __M_writer(u'\n    <form ng-controller="resourceController" ng-init="rType = \'')
        # SOURCE LINE 57
        __M_writer(escape(type))
        __M_writer(u"'; parentCode = '")
        __M_writer(escape(parent['urlCode']))
        __M_writer(u"'; parentURL = '")
        __M_writer(escape(parent['url']))
        __M_writer(u'\'; addResourceURLResponse=\'\'; addResourceResponse=\'\';"  id="addResourceForm" name="addResourceForm" ng-submit="submitResourceForm(addResourceForm)">\n        <fieldset>\n            <label>Resource title</label><span class="help-block"> (Try to keep your title informative, but concise.) </span>\n            <input type="text" class="input-block-level" name="title" ng-model="title" maxlength = "120" required>\n            <span ng-show="addResourceTitleShow"><div class="alert alert-danger" ng-cloak>{{addResourceTitleResponse}}</div></span>\n        </fieldset>\n        <fieldset>\n            <label>Resource URL</label>\n            <input type="url" class="input-block-level" name="link" ng-model="link" placeholder="http://" required>\n            <span ng-show="addResourceURLShow"><div class="alert alert-danger" ng-cloak>{{addResourceURLResponse}}</div></span>\n        </fieldset>\n        ')
        # SOURCE LINE 68
        __M_writer(escape(self.additionalInfo(name="text")))
        __M_writer(u'\n        <span ng-show="addResourceShow">{{addResourceResponse}}</span>\n        ')
        # SOURCE LINE 70
        __M_writer(escape(self.submitButton()))
        __M_writer(u'\n   </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_addDiscussion(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 35
        __M_writer(u'\n   <form action="/workshop/')
        # SOURCE LINE 36
        __M_writer(escape(c.w['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.w['url']))
        __M_writer(u'/add/discussion/handler" id="addDiscussion" method="post">\n      <fieldset>\n         <label>Title</label>\n         <input type="text" class="input-block-level" name="title" id = "title" maxlength = "120">\n         <span class="help-block"> (Try to keep your title informative, but concise.) </span>\n      </fieldset>\n      <hr/>\n      ')
        # SOURCE LINE 43
        __M_writer(escape(self.additionalInfo()))
        __M_writer(u'\n      ')
        # SOURCE LINE 44
        __M_writer(escape(self.submitButton()))
        __M_writer(u'\n   </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_addListing(context,listingType):
    context.caller_stack._push_frame()
    try:
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 9
        __M_writer(u'\n   <div class="row-fluid">\n      <div class="span12">\n         <div class="section-wrapper">\n            <div class="browse">\n')
        # SOURCE LINE 14
        if listingType.startswith(('a', 'e', 'i', 'o', 'u')):
            # SOURCE LINE 15
            __M_writer(u'                  <h4 class="section-header smaller"> Add an ')
            __M_writer(escape(listingType))
            __M_writer(u' </h3>\n')
            # SOURCE LINE 16
        else:
            # SOURCE LINE 17
            __M_writer(u'                  <h4 class="section-header smaller"> Add a ')
            __M_writer(escape(listingType))
            __M_writer(u' </h3>\n')
            pass
        # SOURCE LINE 19
        __M_writer(u'               <div class="add-a-thing-forms">\n               ')
        # SOURCE LINE 20

        if listingType == 'discussion':
           self.addDiscussion()
        elif listingType == 'resource':
           self.addResource()
        elif listingType == 'idea':
           self.addIdea()
                       
        
        # SOURCE LINE 27
        __M_writer(u'\n              </div>\n            </div><!--/.browse-->\n         </div><!--/.section-wrapper-->\n      </div><!--/.span12-->\n   </div><!--/.row-fluid-->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_addIdea(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 74
        __M_writer(u'\n   <form action="/workshop/')
        # SOURCE LINE 75
        __M_writer(escape(c.w['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.w['url']))
        __M_writer(u'/add/idea/handler" id="addIdea" method="post">\n      <fieldset ng-controller="GoalsCtrl">\n         <label>Idea Title</label>\n         <input type="text" class="input-block-level" name="title" id = "title" maxlength = "120"><span class="grey"> characters remaining</span>\n         <span class="help-block">\n      </fieldset>\n      ')
        # SOURCE LINE 81
        __M_writer(escape(self.additionalInfo(name="text")))
        __M_writer(u'\n      ')
        # SOURCE LINE 82
        __M_writer(escape(self.submitButton()))
        __M_writer(u'\n   </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_submitButton(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 86
        __M_writer(u'\n    <fieldset>\n        <button class="btn btn-large btn-civ pull-right" type="submit" name="submit">Submit</button>\n    </fieldset>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraScripts2(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 101
        __M_writer(u'\n    <script type="text/javascript" src="/js/vendor/charCount.js"></script>\n    <script>\n      $("#title").charCount({\n         allowed:120,\n         warning:20,\n         css: \'counter med-green\',\n         counterElement: \'span\'\n      });\n    </script>\n    <script type="text/javascript">\n      function GoalsCtrl($scope, $http) {\n         var getGoalsURL = "/workshop/')
        # SOURCE LINE 113
        __M_writer(escape(c.w['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.w['url']))
        __M_writer(u'/goals/get"\n         $http.get(getGoalsURL).success(function(data){\n            $scope.goals = data;\n         });\n      };\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


