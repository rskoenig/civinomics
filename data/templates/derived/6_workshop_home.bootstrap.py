# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398544344.9187591
_template_filename = '/home/maria/civinomics/pylowiki/templates/derived/6_workshop_home.bootstrap'
_template_uri = '/derived/6_workshop_home.bootstrap'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['headScripts', 'extraScripts2']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 6
    ns = runtime.TemplateNamespace(u'ngHelpers', context._clean_inheritance_tokens(), templateuri=u'/lib/ng_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'ngHelpers')] = ns

    # SOURCE LINE 2
    ns = runtime.TemplateNamespace(u'lib_6', context._clean_inheritance_tokens(), templateuri=u'/lib/6_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib_6')] = ns

    # SOURCE LINE 3
    ns = runtime.TemplateNamespace(u'helpers', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_workshop_home.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'helpers')] = ns

    # SOURCE LINE 4
    ns = runtime.TemplateNamespace(u'listingHelpers', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_detailed_listing.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'listingHelpers')] = ns

    # SOURCE LINE 5
    ns = runtime.TemplateNamespace(u'lib', context._clean_inheritance_tokens(), templateuri=u'/lib/mako_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base/base_workshop.bootstrap', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        ngHelpers = _mako_get_namespace(context, 'ngHelpers')
        listingHelpers = _mako_get_namespace(context, 'listingHelpers')
        len = context.get('len', UNDEFINED)
        helpers = _mako_get_namespace(context, 'helpers')
        str = context.get('str', UNDEFINED)
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
        # SOURCE LINE 6
        __M_writer(u'\n\n')
        # SOURCE LINE 8
        numIdeas = str(len(c.ideas)) 
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['numIdeas'] if __M_key in __M_locals_builtin_stored]))
        __M_writer(u'\n<div class="row-fluid" ng-init="code = \'')
        # SOURCE LINE 9
        __M_writer(escape(c.w['urlCode']))
        __M_writer(u"'; url = '")
        __M_writer(escape(c.w['url']))
        __M_writer(u'\'">\n   <div class="span8" ng-controller="workshopIdeasCtrl">\n      <div class="section-wrapper slideshow">\n        <div id="workshopSlideshow">\n          ')
        # SOURCE LINE 13
        __M_writer(escape(helpers.slideshow(c.w, 'hero')))
        __M_writer(u'\n        </div>\n      </div> <!-- /.section-wrapper -->\n\n      <div class="browse" id="vote">\n        <h4 class="summary"> Vote ')
        # SOURCE LINE 18
        __M_writer(escape(lib_6.createNew("ideas", 'small')))
        __M_writer(u'</h4>\n      </div><!--/.browse-->\n\n      <div class="row-fluid helper-sort">\n        <div class="span9">\n          <form class="form-search inline">\n            Sort by: \n            <select class="med-width" ng-model="orderProp" ng-cloak>\n              <option value="-date">Recent</option>\n              <option value="-voteRatio">Highest Rated</option>\n              <option value="-voteCount">Most Votes</option>\n              <option value="-numComments">Most Comments</option>\n            </select>\n            Filter:\n            <select class="med-width" ng-model="filterProp" ng-cloak>\n              <option value="!disabled">Show All</option>\n              <option value="proposed">Proposed</option>\n              <option value="adopted">Adopted</option>\n              <option value="disabled">Disabled</option>\n            </select>\n          </form> \n        </div><!-- span9 -->\n        <div class="span3"><strong class="orange"> Vote <img class="helper-text-img" alt="yes vote" src="/images/yes_selected.png"> or <img class="helper-text-img" alt="no vote" src="/images/no_selected.png"> to view ratings.</strong></div>\n      </div><!-- helper-sort -->\n\n      <div class="centered" ng-show="ideasLoading" ng-cloak>\n          <i class="icon-spinner icon-spin icon-4x"></i>\n      </div>\n\n      <div class="alert alert-info" ng-show="noResult" ng-cloak>\n          There are no ideas for this workshop. Be the first to add one!\n      </div>\n\n      <div class="row-fluid" ng-repeat="item in ideas | orderBy:orderProp | filter:filterProp " ng-cloak>\n          ')
        # SOURCE LINE 52
        __M_writer(escape(ngHelpers.idea_listing()))
        __M_writer(u'\n      </div>\n\n   </div> <!-- /.span8 -->\n\n   <div class="span4">\n    <!--\n      <div class="section-wrapper metrics" ng-controller="workshopIdeasCtrl" ng-cloak>\n        <div class="row-fluid">\n          <div class="span3 offset3 centered">\n            <i class="icon-lightbulb icon-3x"></i><br>\n            {{numIdeas}}<br>\n            Ideas\n          </div>\n          <div class="span3 centered">\n            <a class="no-highlight" ng-click="switchAdopted()">\n              <i class="icon-star icon-3x"></i><br>\n              {{numAdopted}}<br>\n              Adopted\n              {{filterProp}}\n            </a>\n          </div>\n          <div class="span3 centered">\n            <i class="icon-eye-open icon-3x"></i><br>\n            ')
        # SOURCE LINE 76
        __M_writer(escape(c.numViews))
        __M_writer(u'<br>\n            Views\n          </div>\n          <div class="span3 centered">\n            <i class="icon-share icon-3x"></i><br>\n            {{numAdopted}}<br>\n            Shares\n          </div>\n        </div>\n      </div>\n          -->\n      <div class="section-wrapper overview">\n         <div class="browse">\n            <h4 class="section-header smaller"> \n            Goals\n            </h4>\n            ')
        # SOURCE LINE 92
        __M_writer(escape(helpers.showGoals(c.goals)))
        __M_writer(u'\n            ')
        # SOURCE LINE 93
        __M_writer(escape(helpers.whoListening()))
        __M_writer(u'\n         </div> <!--/.browse-->\n      </div> <!-- /.section-wrapper -->\n      <div class="section-wrapper overview">\n         <div class="browse">\n            <h4 class="section-header smaller"> \n            Forum\n            <span class="pull-right" style="margin-left: -50px;">')
        # SOURCE LINE 100
        __M_writer(escape(lib_6.createNew('discussion', 'small')))
        __M_writer(u'</span>\n            </h4>\n')
        # SOURCE LINE 102
        if len(c.discussions) == 0:
            # SOURCE LINE 103
            __M_writer(u'              <div class="alert alert-info no-bottom">There are no forum topics here yet. Be the first to add one!</div>\n')
            # SOURCE LINE 104
        else:
            # SOURCE LINE 105
            __M_writer(u'              ')
            __M_writer(escape(listingHelpers.showListing('discussion', 'condensed')))
            __M_writer(u'\n')
            pass
        # SOURCE LINE 107
        __M_writer(u'         </div> <!--/.browse-->\n      </div> <!-- /.section-wrapper -->\n      <div class="section-wrapper overview">\n         <div class="browse">\n            <h4 class="section-header smaller"> \n            Recent Activity\n            </h4>\n            ')
        # SOURCE LINE 114
        __M_writer(escape(helpers.showActivity(c.activity[0:5])))
        __M_writer(u'\n         </div> <!--/.browse-->\n      </div> <!-- /.section-wrapper -->\n   </div> <!-- /.span4 -->\n</div> <!-- /.row -->\n\n\n')
        # SOURCE LINE 139
        __M_writer(u'\n\n')
        # SOURCE LINE 146
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headScripts(context):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 141
        __M_writer(u'\n    <script src="')
        # SOURCE LINE 142
        __M_writer(escape(lib_6.fingerprintFile('/js/ng/listeners.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script src="')
        # SOURCE LINE 143
        __M_writer(escape(lib_6.fingerprintFile('/js/ng/workshop_ideas.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script src="')
        # SOURCE LINE 144
        __M_writer(escape(lib_6.fingerprintFile('/js/ng/yesno_vote.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script type="text/javascript" src="')
        # SOURCE LINE 145
        __M_writer(escape(lib_6.fingerprintFile('/js/ng/activity.js')))
        __M_writer(u'"></script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraScripts2(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 121
        __M_writer(u'\n')
        # SOURCE LINE 122
        if c.demo:
            # SOURCE LINE 123
            __M_writer(u'        <script type="text/javascript" src="/js/vendor/guiders-1.3.0.js"></script>\n        <script type="text/javascript" src="/js/guiders/workshop_home.js"></script>\n')
            pass
        # SOURCE LINE 126
        __M_writer(u'    <script src="/js/bootstrap/bootstrap-tooltip.js"></script>\n    <script type="text/javascript">\n        $(\'.nullvote\').tooltip();\n    </script>\n    <script type="text/javascript" src="/js/vendor/jquery.foundation.clearing.js"></script>\n    <script>\n      var $doc = $(document);\n      $(document).ready(function() {\n         $.fn.foundationClearing         ? $doc.foundationClearing() : null;\n      });\n    </script>\n    <script src="')
        # SOURCE LINE 137
        __M_writer(escape(lib_6.fingerprintFile('/js/upDown.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script src="')
        # SOURCE LINE 138
        __M_writer(escape(lib_6.fingerprintFile('/js/yesNo.js')))
        __M_writer(u'" type="text/javascript"></script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


