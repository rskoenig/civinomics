# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1399412194.7035179
_template_filename = '/home/maria/civinomics/pylowiki/templates/derived/splash.bootstrap'
_template_uri = '/derived/splash.bootstrap'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['bodyTag_extras', 'headScripts', 'extraScripts', 'extraStyles']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 4
    ns = runtime.TemplateNamespace(u'ng_helpers', context._clean_inheritance_tokens(), templateuri=u'/lib/ng_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'ng_helpers')] = ns

    # SOURCE LINE 2
    ns = runtime.TemplateNamespace(u'templateHelpers', context._clean_inheritance_tokens(), templateuri=u'/lib/template_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'templateHelpers')] = ns

    # SOURCE LINE 3
    ns = runtime.TemplateNamespace(u'lib_6', context._clean_inheritance_tokens(), templateuri=u'/lib/6_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib_6')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base/base_splash.bootstrap', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        ng_helpers = _mako_get_namespace(context, 'ng_helpers')
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        templateHelpers = _mako_get_namespace(context, 'templateHelpers')
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\r\n')
        # SOURCE LINE 2
        __M_writer(u'\r\n')
        # SOURCE LINE 3
        __M_writer(u'\r\n')
        # SOURCE LINE 4
        __M_writer(u'\r\n\r\n')
        # SOURCE LINE 8
        __M_writer(u'\r\n\r\n')
        # SOURCE LINE 13
        __M_writer(u'\r\n\r\n\r\n')
        # SOURCE LINE 16
        if not c.success:
            # SOURCE LINE 17
            __M_writer(u'    <div id="splash-bg" style="background-image: url(\'')
            __M_writer(escape(c.backgroundPhotoURL))
            __M_writer(u'\');">\r\n        <div class="darkened-bg"></div>\r\n    </div>\r\n')
            # SOURCE LINE 20
        else:
            # SOURCE LINE 21
            __M_writer(u'    <div id="login-bg"></div>\r\n')
            pass
        # SOURCE LINE 23
        __M_writer(u'\r\n<div class="row welcome">\r\n')
        # SOURCE LINE 25
        if c.success:
            # SOURCE LINE 26
            __M_writer(u'            <div class="well main-well success-well green">\r\n                <div class="login-top">\r\n                    <h2>Success!</h2>\r\n                <div>\r\n                Check your email to finish setting up your account.\r\n                If you don\'t see an email from us in your inbox, try checking your junk mail folder.\r\n            </div>\r\n        </div>\r\n')
            # SOURCE LINE 34
        else: 
            # SOURCE LINE 35
            __M_writer(u'    <div class="slogan centered">\r\n        <h1>Democracy starts at home</h1>\r\n')
            # SOURCE LINE 37
            if c.splashMsg:
                # SOURCE LINE 38
                __M_writer(u'            ')
                message = c.splashMsg 
                
                __M_locals_builtin_stored = __M_locals_builtin()
                __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['message'] if __M_key in __M_locals_builtin_stored]))
                __M_writer(u'\r\n            <div class="row-fluid centered">\r\n                <div class="span6 offset3 alert alert-')
                # SOURCE LINE 40
                __M_writer(escape(message['type']))
                __M_writer(u'">\r\n                    <button data-dismiss="alert" class="close">x</button>\r\n                    <strong>')
                # SOURCE LINE 42
                __M_writer(escape(message['title']))
                __M_writer(u'</strong> ')
                __M_writer(escape(message['content']))
                __M_writer(u'\r\n                </div>\r\n            </div>\r\n')
                pass
            # SOURCE LINE 46
            __M_writer(u'        <button href="#signupLoginModal" data-toggle="modal" class="btn btn-large btn-primary">Sign up to Vote</button>\r\n        <!-- <p>or <span style="text-decoration: underline;">subscribe to our newsletter</span></p> -->\r\n    </div>\r\n</div><!-- row welcome -->\r\n<div class="container splash-container">\r\n    <div class="row-fluid">\r\n        <div class="span4 zipLookup" ng-controller="zipLookupCtrl" ng-cloak>\r\n            <div class="well well-splash-content">\r\n                <h3>Zip Code Lookup</h3>\r\n                <form class="form-inline" name="zipForm">\r\n                    <div ng-class=" {\'error\': zipForm.zipValue.$error.pattern} " ng-cloak>\r\n                        <input class="input-small" type="number" name="zipValue" id="zipValue" ng-model="zipValue" ng-pattern="zipValueRegex" ng-minlength="5" ng-maxlength="5" placeholder="{{zipValue}}" ng-cloak>\r\n                        <button class="btn btn-primary" ng-click="lookup()">Search</button><br>\r\n                        <span class="error help-block" ng-show="zipForm.zipValue.$error.pattern" ng-cloak>Invalid zip code!</span>\r\n                    </div>\r\n                </form>\r\n                <div class="loading-civ" ng-show="loading" ng-cloak>\r\n                    <i class="icon-spinner icon-spin icon-4x" style="color: #333333;"></i>\r\n                </div>\r\n                <table ng-show="!loading">\r\n                    <tr ng-repeat="geo in geos">\r\n                        <td><a href="{{geo.href}}"><img class="thumbnail flag med-flag border tight" src="{{geo.flag}}"></a></td>\r\n                        <td><a class="lead no-highlight" href="{{geo.href}}" ng-cloak><span ng-show="!(geo.level == \'Country\' || geo.level == \'Postalcode\' || geo.level == \'County\')">{{geo.level}} of</span> {{geo.name}} <span ng-show="geo.level == \'County\'">{{geo.level}}</span></a></td>\r\n                    </tr>\r\n                </table>\r\n            </div>\r\n        </div>\r\n        <div class="span8 well well-splash-content" ng-controller="SearchCtrl">\r\n            <h3>\r\n                Top Initiatives\r\n                <!--\r\n                <span class="pull-right" ng-show="showingInitiatives.create" ng-cloak>\r\n')
            # SOURCE LINE 78
            if 'user' in session:
                # SOURCE LINE 79
                __M_writer(u'                        <a class="btn btn-success" style="margin-top: 7px;" href="/profile/')
                __M_writer(escape(c.authuser['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.authuser['url']))
                __M_writer(u'/newInitiative">\r\n                            <i class="icon-plus"></i> New Initiative\r\n                        </a>\r\n')
                # SOURCE LINE 82
            else:
                # SOURCE LINE 83
                __M_writer(u'                        <a class="btn btn-civ" style="margin-top: 7px;" href="/login"><i class="icon-edit"></i> Start an Initiative</a>\r\n')
                pass
            # SOURCE LINE 85
            __M_writer(u'                </span>\r\n                -->\r\n            </h3>\r\n            <div class="loading-civ" ng-show="loading" ng-cloak>\r\n                <i class="icon-spinner icon-spin icon-4x" style="color: #333333;"></i>\r\n            </div>\r\n            <div ng-show="noQuery" ng-cloak>\r\n                <div class="row-fluid">\r\n                    <div class="alert alert-info centered span6 offset3">\r\n                        Searching for nothing yields nothing.  How zen.\r\n                    </div>\r\n                </div>\r\n            </div>\r\n            <div ng-show="noResult" ng-cloak>\r\n                <div class="row-fluid">\r\n                    <div class="alert centered span6 offset3">\r\n')
            # SOURCE LINE 101
            if c.searchType == 'region':
                # SOURCE LINE 102
                __M_writer(u'                            Sorry, we couldn\'t find any {{objType}} scoped for "{{searchQueryPretty}}"\r\n')
                # SOURCE LINE 103
            else:
                # SOURCE LINE 104
                __M_writer(u'                            Sorry, we couldn\'t find any {{objType}} matching "{{searchQueryPretty}}"\r\n')
                pass
            # SOURCE LINE 106
            __M_writer(u'                        \r\n                    </div>\r\n                </div>\r\n            </div>\r\n            <div id="initiatives" class="tab-pane" ng-class="showingInitiatives.class" ng-show="showingInitiatives.show" ng-cloak>\r\n                <table class="table">\r\n\r\n                    <tr ng-repeat = "item in initiatives | orderBy:orderProp | limitTo:10">\r\n                        <td>\r\n                            ')
            # SOURCE LINE 115
            __M_writer(escape(ng_helpers.initiative_listing()))
            __M_writer(u'\r\n                        </td>\r\n\r\n                    </tr>\r\n\r\n                </table>\r\n                <div class="centered" ng-show="initiative.length>pageSize">\r\n                    <button class="btn" onclick="$(\'html,body\').scrollTop(0);" ng-disabled="currentPage == 0" ng-click="currentPage=currentPage-1">\r\n                        Prev\r\n                    </button>\r\n                    <span style="color: #ffffff;"> <strong>{{currentPage+1}}</strong> of <strong>{{numberOfPages()}}</strong> </span>\r\n                    <button class="btn" onclick="$(\'html,body\').scrollTop(0);" ng-disabled="currentPage >= photos.length/pageSize - 1" ng-click="currentPage=currentPage+1">\r\n                        Next\r\n                    </button>\r\n                    <div class="spacer"></div>\r\n                </div>\r\n                <div class="row-fluid centered">\r\n                    <a href="/browse/initiatives">View more initiatives</a>\r\n                </div>\r\n            </div>\r\n        </div><!-- span8 -->\r\n        \r\n    </div><!-- row-fluid -->\r\n    </div>\r\n    ')
            # SOURCE LINE 139
            __M_writer(escape(templateHelpers.condensedFooter()))
            __M_writer(u'\r\n    ')
            # SOURCE LINE 140
            __M_writer(escape(templateHelpers.signupLoginModal()))
            __M_writer(u'\r\n\r\n')
            pass
        # SOURCE LINE 148
        __M_writer(u'\r\n\r\n')
        # SOURCE LINE 163
        __M_writer(u'\r\n\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bodyTag_extras(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 165
        __M_writer(u'\r\n    ng-app\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headScripts(context):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 143
        __M_writer(u'\r\n    <script src="//cdnjs.cloudflare.com/ajax/libs/angular-strap/0.7.1/angular-strap.min.js"></script>\r\n    <script type="text/javascript" src="')
        # SOURCE LINE 145
        __M_writer(escape(lib_6.fingerprintFile('/js/ng/search.js')))
        __M_writer(u'"></script>\r\n    <script type="text/javascript" src="')
        # SOURCE LINE 146
        __M_writer(escape(lib_6.fingerprintFile('/js/ng/yesno_vote.js')))
        __M_writer(u'"></script>\r\n    <script type="text/javascript" src="')
        # SOURCE LINE 147
        __M_writer(escape(lib_6.fingerprintFile('/js/ng/activity.js')))
        __M_writer(u'"></script>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraScripts(context):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 150
        __M_writer(u'\r\n    <script src="/js/bootstrap/bootstrap-tooltip.js"></script>\r\n    <script type="text/javascript" src="')
        # SOURCE LINE 152
        __M_writer(escape(lib_6.fingerprintFile('/js/ng/zipLookup.js')))
        __M_writer(u'"></script>\r\n    <script type="text/javascript">\r\n        $(\'.modal i[rel="tooltip"]\')\r\n        .tooltip({placement: \'top\'})\r\n        .data(\'tooltip\')\r\n        .tip()\r\n        .css(\'z-index\', 2080);\r\n        $(\'.signup-tooltip\').tooltip();\r\n        $(\'.icon-question-sign\').tooltip();\r\n        $(\'.upVote.nullvote\').tooltip();\r\n    </script>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraStyles(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 6
        __M_writer(u'\r\n   <link href="/styles/splash.css" rel="stylesheet">\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


