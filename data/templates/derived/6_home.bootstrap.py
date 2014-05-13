# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398542482.4056921
_template_filename = '/home/maria/civinomics/pylowiki/templates/derived/6_home.bootstrap'
_template_uri = '/derived/6_home.bootstrap'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['headScripts', 'extraScripts']


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

    # SOURCE LINE 6
    ns = runtime.TemplateNamespace(u'ihelpers', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_initiative_home.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'ihelpers')] = ns

    # SOURCE LINE 5
    ns = runtime.TemplateNamespace(u'listingHelpers', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_main_listing.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'listingHelpers')] = ns

    # SOURCE LINE 4
    ns = runtime.TemplateNamespace(u'profileHelpers', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_profile.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'profileHelpers')] = ns

    # SOURCE LINE 7
    ns = runtime.TemplateNamespace(u'ng_helpers', context._clean_inheritance_tokens(), templateuri=u'/lib/ng_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'ng_helpers')] = ns

    # SOURCE LINE 3
    ns = runtime.TemplateNamespace(u'helpers', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_home.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'helpers')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base/base_indented.bootstrap', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        ng_helpers = _mako_get_namespace(context, 'ng_helpers')
        c = context.get('c', UNDEFINED)
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
        __M_writer(u'\n')
        # SOURCE LINE 7
        __M_writer(u'\n\n\n<div class="spacer"></div>\n<div class="row" ng-controller = "activityController">\n\n')
        # SOURCE LINE 16
        __M_writer(u'\n  <div class="span8">\n    <div infinite-scroll=\'getActivitySlice()\' infinite-scroll-disabled=\'activityLoading\' infinite-scroll-distance=\'3\'>\n\n      <div class="alert" ng-class="alertType" ng-if="alertMsg && !(alertMsg == \'\') " ng-cloak>\n          {{alertMsg}}\n      </div>\n\n      <table ng-repeat="item in activity" id="{{item.urlCode}}"  class="activity-item" ng-show="!activityLoading" ng-cloak>\n        <tr>\n          <td class="avatar-cell" rowspan="3"><img class="avatar" ng-src="{{item.authorPhoto}}" alt="{{item.authorName}}" title="{{item.authorName}}"></td>\n          <td></td>\n        </tr>\n        <tr>\n          <td>\n            <div class="activity-item-content-header">\n              <small>\n                <a href="{{item.authorHref}}" class="no-highlight"><strong>{{item.authorName}}</strong></a> \n                <span class="date">{{item.fuzzyTime}} ago</span>\n              </small>\n            </div>\n          </td>\n        </tr>\n        <tr>\n          <td ng-if="item.objType == \'initiative\'">\n            ')
        # SOURCE LINE 41
        __M_writer(escape(ng_helpers.initiative_listing()))
        __M_writer(u'\n          </td>\n\n          <td ng-if="item.objType == \'idea\'">\n            ')
        # SOURCE LINE 45
        __M_writer(escape(ng_helpers.idea_listing()))
        __M_writer(u'\n          </td>\n\n          <td ng-if="item.objType == \'resource\'">\n            ')
        # SOURCE LINE 49
        __M_writer(escape(ng_helpers.resource_listing()))
        __M_writer(u'\n          </td>\n\n          <td ng-if="item.objType == \'discussion\' || item.objType == \'update\' ">\n            ')
        # SOURCE LINE 53
        __M_writer(escape(ng_helpers.discussion_listing()))
        __M_writer(u'\n          </td>\n\n          <td ng-if="item.objType == \'photo\'">\n            ')
        # SOURCE LINE 57
        __M_writer(escape(ng_helpers.photo_listing()))
        __M_writer(u'\n          </td>\n\n        </tr>\n      </table>\n\n      <div class="centered" ng-show="activityLoading || activitySliceLoading" ng-cloak>\n          <i class="icon-spinner icon-spin icon-4x"></i>\n      </div>\n\n    </div><!-- infinite-scroll -->\n\n  </div><!-- /span8 -->\n  <div class="span4">\n\n')
        # SOURCE LINE 72
        if c.authuser and c.authuser['activated'] == '0':
            # SOURCE LINE 73
            __M_writer(u'      <div class="alert alert-success">\n        <h4>Welcome!</h4> \n        Check your email to finish setting up your account. If you don\'t see an email from us in your inbox, try checking your junk mail folder.\n        <p>You can\'t add comments or ideas until you complete setup.</p>\n\n        <button class="btn btn-success resendActivateEmailButton" data-URL-list="user_')
            # SOURCE LINE 78
            __M_writer(escape(c.authuser['urlCode']))
            __M_writer(u'_')
            __M_writer(escape(c.authuser['url']))
            __M_writer(u'">Resend Activation Email</button>\n        <div class="top-space" id="resendMessage"></div>\n      </div>\n')
            pass
        # SOURCE LINE 82
        __M_writer(u'\n')
        # SOURCE LINE 86
        __M_writer(u'    <div>\n      <ul class="nav nav-tabs nav-stacked" style="width: 100%; margin-top: 0;">\n        <li ng-class="{\'active\' : activityType == \'/all\'}"><a ng-click="getAllActivity()"> All Activity </a></li>\n')
        # SOURCE LINE 89
        if c.authuser:
            # SOURCE LINE 90
            __M_writer(u'          <li ng-class="{\'active\' : activityType == \'/following\'}"><a ng-click="getFollowingActivity()"> Following </a></li>\n          <li ng-class="{\'active\' : activityType == \'/geo\'}"><a ng-click="getGeoActivity()"> My County </a></li>\n')
            pass
        # SOURCE LINE 93
        __M_writer(u'      </ul>\n    </div>\n\n\n')
        # SOURCE LINE 100
        __M_writer(u'    <div ng-init="zipValue = ')
        __M_writer(escape(c.postalCode))
        __M_writer(u'">\n      <div class="well well-splash-content" ng-controller="zipLookupCtrl" ng-cloak>\n          <h4>Zip Code Lookup</h4>\n          <form class="form-inline" name="zipForm">\n              <div ng-class=" {\'error\': zipForm.zipValue.$error.pattern} " ng-cloak>\n                  <input class="input-small" type="number" name="zipValue" id="zipValue" ng-model="zipValue" ng-pattern="zipValueRegex" ng-minlength="5" ng-maxlength="5" placeholder="{{zipValue}}" ng-cloak>\n                  <button class="btn btn-primary" ng-click="lookup()">Search</button><br>\n                  <span class="error help-block" ng-show="zipForm.zipValue.$error.pattern" ng-cloak>Invalid zip code!</span>\n              </div>\n          </form>\n          <div class="loading-civ" ng-show="loading" ng-cloak>\n              <i class="icon-spinner icon-spin icon-4x" style="color: #333333;"></i>\n          </div>\n          <table ng-show="!loading">\n              <tr ng-repeat="geo in geos">\n                  <td><a href="{{geo.href}}"><img class="thumbnail flag small-flag border" src="{{geo.flag}}"></a></td>\n                  <td><a class="green green-hover left-space" href="{{geo.href}}" ng-cloak><span ng-show="!(geo.level == \'Country\' || geo.level == \'Postalcode\' || geo.level == \'County\')">{{geo.level}} of</span> {{geo.name}} <span ng-show="geo.level == \'County\'">{{geo.level}}</span></a></td>\n              </tr>\n          </table>\n      </div>\n    </div>\n\n  </div><!-- /span4 -->\n</div><!-- /row -->\n\n\n')
        # SOURCE LINE 130
        __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headScripts(context):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 126
        __M_writer(u'\n  <script type="text/javascript" src="')
        # SOURCE LINE 127
        __M_writer(escape(lib_6.fingerprintFile('/js/ng/zipLookup.js')))
        __M_writer(u'"></script>\n  <script type="text/javascript" src="')
        # SOURCE LINE 128
        __M_writer(escape(lib_6.fingerprintFile('/js/ng/activity.js')))
        __M_writer(u'"></script>\n  <script type="text/javascript" src="')
        # SOURCE LINE 129
        __M_writer(escape(lib_6.fingerprintFile('/js/ng/yesno_vote.js')))
        __M_writer(u'"></script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraScripts(context):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 132
        __M_writer(u'\n   <script type="text/javascript" src="/js/vendor/jquery.autosize.js"></script>\n    <script>\n      $(document).ready(function(){\n        $(\'textarea\').autosize();   \n      });\n    </script>\n   <script type="text/javascript">\n   $(document).ready(function() {\n       $(\'.viewport\').mouseenter(function(e) {\n           $(this).children(\'a\').children(\'span\').fadeIn(200);\n       }).mouseleave(function(e) {\n           $(this).children(\'a\').children(\'span\').fadeOut(200);\n       });\n       \n       $(".small-bulb, .small-bookmark").tooltip({delay:500});\n   });\n   </script>\n    <script src="')
        # SOURCE LINE 150
        __M_writer(escape(lib_6.fingerprintFile('/js/follow.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script src="')
        # SOURCE LINE 151
        __M_writer(escape(lib_6.fingerprintFile('/js/activate.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script src="')
        # SOURCE LINE 152
        __M_writer(escape(lib_6.fingerprintFile('/js/ng/alerts_admin.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script src="')
        # SOURCE LINE 153
        __M_writer(escape(lib_6.fingerprintFile('/js/bootstrap/bootstrap-carousel.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script type="text/javascript">\n      $(\'.carousel\').carousel({\n        interval: 4500\n      })\n    </script>\n    <script>\n      // prevents bookmark options dropdown menu from closing when checkboxes are clicked \n      $(\'.dropdown-menu input, .dropdown-menu label\').click(function(e) {\n        e.stopPropagation();\n      });\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


