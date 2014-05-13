# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398540607.8187411
_template_filename = u'/home/maria/civinomics/pylowiki/templates/base/base.bootstrap'
_template_uri = u'/base/base.bootstrap'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['bodyTag_extras', 'headScripts', 'extraStyles', 'headScripts2', 'google_analytics', 'atlassian_issueCollector', 'extraScripts', 'extraScripts2']


# SOURCE LINE 3
import pylowiki.lib.db.user as userLib 

def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 1
    ns = runtime.TemplateNamespace(u'lib_6', context._clean_inheritance_tokens(), templateuri=u'/lib/6_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib_6')] = ns

    # SOURCE LINE 2
    ns = runtime.TemplateNamespace(u'template_lib', context._clean_inheritance_tokens(), templateuri=u'/lib/template_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'template_lib')] = ns

def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        session = context.get('session', UNDEFINED)
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        self = context.get('self', UNDEFINED)
        next = context.get('next', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n')
        # SOURCE LINE 3
        __M_writer(u'\n')
        # SOURCE LINE 4
        lib_6.validateSession() 
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in [] if __M_key in __M_locals_builtin_stored]))
        __M_writer(u'\n<!DOCTYPE HTML>\n<html lang="en-US" ng-app=\'civ\'>\n   <head>\n      <meta charset="UTF-8">\n      <meta name="description" content="Civinomics is an online citizen collaboration platform. You can use Civinomics to join the movement towards improving social decision-making through the collective creativity of communities.">\n      <title>')
        # SOURCE LINE 10
        __M_writer(escape(c.title))
        __M_writer(u'</title>\n      <!-- Third-party assets -->\n      <link rel="stylesheet" href="/styles/vendor/bootstrap.css">\n      <link rel="stylesheet" href="/styles/vendor/bootstrap-responsive.min.css">\n      <link rel="stylesheet" href="/styles/vendor/font-awesome/css/font-awesome.min.css">\n      <link rel="stylesheet" href="')
        # SOURCE LINE 15
        __M_writer(escape(lib_6.fingerprintFile('/styles/civ.css')))
        __M_writer(u'">\n      <link rel="shortcut icon" href="')
        # SOURCE LINE 16
        __M_writer(escape(lib_6.fingerprintFile('/images/logo_tab.ico')))
        __M_writer(u'">\n      <link href=\'//fonts.googleapis.com/css?family=Roboto:500,400,300,100,400italic,300italic,700\' rel=\'stylesheet\' type=\'text/css\'>\n      <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>\n      <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.2.1/angular.min.js"></script>\n      <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.2.1/angular-sanitize.js"></script>\n      <script type="text/javascript" src="')
        # SOURCE LINE 21
        __M_writer(escape(lib_6.fingerprintFile('/js/vendor/binaryMuse_ngInfiniteScroll.min.js')))
        __M_writer(u'"></script>\n      <script src="/js/geoSearch.js"></script>\n      <script src="/js/ng/signup_login.js" type="text/javascript"></script>\n      <script>\n        var dummyApp = angular.module(\'civ\', [\'ngSanitize\', \'infinite-scroll\']);\n      </script>\n      <script src="/js/extauth.js" type="text/javascript"></script>\n      ')
        # SOURCE LINE 28
        __M_writer(escape(self.extraStyles()))
        __M_writer(u'\n      ')
        # SOURCE LINE 29
        __M_writer(escape(self.headScripts()))
        __M_writer(u'\n      ')
        # SOURCE LINE 30
        __M_writer(escape(self.headScripts2()))
        __M_writer(u'\n      ')
        # SOURCE LINE 31
        __M_writer(escape(self.google_analytics()))
        __M_writer(u'\n      <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->\n      <!--[if lt IE 9]>\n         <script src="//html5shim.googlecode.com/svn/trunk/html5.js"></script>\n      <![endif]-->      \n   </head>\n   <body ')
        # SOURCE LINE 37
        __M_writer(escape(self.bodyTag_extras()))
        __M_writer(u'>\n    ')
        # SOURCE LINE 38
        __M_writer(escape(next.body()))
        __M_writer(u'\n\n   <!-- scripts go at the bottom so they don\'t keep the user waiting -->\n   <script type="text/javascript" src="/js/vendor/bootstrap.min.js"></script>\n   <script type="text/javascript" src="')
        # SOURCE LINE 42
        __M_writer(escape(lib_6.fingerprintFile('/js/searchBox.js')))
        __M_writer(u'"></script>\n   <script type="text/javascript" src="/js/vendor/jquery.autosize.js"></script>\n   <script type="text/javascript">\n    // fix for bootstrap dropdown menus not working on iPad\n    $(\'body\').on(\'touchstart.dropdown\', \'.dropdown-menu\', function (e) { e.stopPropagation(); });\n   </script>\n   <script>\n      $(document).ready(function(){\n        $(\'textarea\').autosize();   \n      });\n   </script>\n   <!-- makes non-local links open in a new tab/window -->\n   <script type="text/javascript">\n      $(document.links).filter(function() {\n          return this.hostname != window.location.hostname;\n      }).attr(\'target\', \'_blank\');\n   </script>\n\n   <!-- Javascript to enable link to tab -->\n   <script type="text/javascript">\n      $(function () { \n        var a = $(\'[href=\' + location.hash + \']\'); \n        a && a.tab(\'show\'); \n      });\n    </script>\n\n\n   ')
        # SOURCE LINE 69
        __M_writer(escape(self.extraScripts()))
        __M_writer(u'\n   ')
        # SOURCE LINE 70
        __M_writer(escape(self.extraScripts2()))
        __M_writer(u'\n   ')
        # SOURCE LINE 71
        __M_writer(escape(self.atlassian_issueCollector()))
        __M_writer(u'\n')
        # SOURCE LINE 72
        if 'user' not in session:
            # SOURCE LINE 73
            __M_writer(u'       ')

            facebookAppId = c.facebookAppId
            channelUrl = c.channelUrl
                   
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['facebookAppId','channelUrl'] if __M_key in __M_locals_builtin_stored]))
            # SOURCE LINE 76
            __M_writer(u'\n       <div id="fb-root"></div>\n       <script>\n         //console.log(\'in fb init\')\n         // activate facebook javascript sdk\n         window.fbAsyncInit = function() {\n            FB.init({\n              appId      : "')
            # SOURCE LINE 83
            __M_writer(escape(facebookAppId))
            __M_writer(u'",\n              channelUrl : "')
            # SOURCE LINE 84
            __M_writer(escape(channelUrl))
            __M_writer(u'", // Channel File\n              status     : true, // check login status\n              cookie     : false, // enable cookies to allow the server to access the session\n              xfbml      : true  // parse XFBML\n            });\n            // this is needed to prevent a hangup with one of the login flows\n            FB.Event.subscribe(\'auth.login\', function(response1) {\n              authSignal();\n            });\n            // check facebook login status\n            FB.Event.subscribe(\'auth.authResponseChange\', function(response) {\n              if (response.status === \'connected\') {\n                // this person is logged into facebook and our app has auth\n                fbConnected(response.authResponse);\n              } else if (response.status === \'not_authorized\') {\n                // this person is logged into facebook but our app does not have auth\n                FB.login(function(response) {\n                  if (response.authResponse) {\n                    //console.log(\'Welcome!  Fetching your information.... \');\n                    //console.log("response status: " + response.status)\n                    //console.log("response email: " + response.email)\n                    fbConnected(response.authResponse);\n                  } else {\n                    console.log(\'User cancelled login or did not fully authorize.\');\n                  }\n                }, {scope: \'email\'});\n              } else {\n                // user not logged into facebook\n                FB.login(function(response) {\n                  if (response.authResponse) {\n                    //console.log(\'Welcome!  Fetching your information.... \');\n                    //console.log("response status: " + response.status)\n                    //console.log("response email: " + response.email)\n                    fbConnected(response.authResponse);\n                  } else {\n                    console.log(\'User cancelled login or did not fully authorize.\');\n                  }\n                }, {scope: \'email\'});\n              }\n            });\n         };\n\n         // Load the SDK asynchronously\n         (function(d){\n          var js, id = \'facebook-jssdk\', ref = d.getElementsByTagName(\'script\')[0];\n          if (d.getElementById(id)) {return;}\n          js = d.createElement(\'script\'); js.id = id; js.async = true;\n          js.src = "//connect.facebook.net/en_US/all.js";\n          ref.parentNode.insertBefore(js, ref);\n         }(document));\n\n         function authSignal() {\n           var authSignal = \'<div id="authSignal"></div>\'\n           $(\'#fbLoginButton1\').append(authSignal);\n           $(\'#fbLoginButton2\').append(authSignal);\n         }\n\n         /*\n         function printObject(o) {\n           var out = \'\';\n           for (var p in o) {\n             out += p + \': \' + o[p] + \'\\n\';\n           }\n           console.log(out);\n         }\n         */\n\n         function fbConnected(authResponse) {\n           FB.api(\'/me\', function(response) {\n             // grab the url to a 200x200 photo of this user\n             var bigPicFql = FB.Data.query(\'SELECT url FROM profile_pic WHERE id = {0} AND width=200 AND height=200\', response.id);\n             var bigPic = \'\';\n             bigPicFql.wait(function (rows) {\n               // the big pic link\n               bigPic = rows[0].url;\n             });\n             // grab the url to a 50x50 photo of this user\n             var smallPicFql = FB.Data.query(\'SELECT url FROM profile_pic WHERE id = {0}\', response.id);\n             var smallPic = \'\';\n             var holder = 0;\n             smallPicFql.wait(function (rows) {\n               //the small pic link\n               smallPic = rows[0].url;\n               holder = 1;\n             });\n             var result = \'\'\n             setTimeout(function(){\n               // check account status on our site for this user\n               //console.log(\'ya\');\n               //printObject(authResponse);\n               result = fbCheckAccount(response, authResponse, smallPic, bigPic);\n               if (result == "not found") {\n                 // no account on site yet.\n                 // this is a unique situation where the person has authorized us to use their\n                 // fb identity, but hasn\'t created an account yet. This assumes that\'s what they\n                 // want to do and redirects once this situation is recognized.\n                 if ($(\'#fbSignUp\').length) {\n                   console.log(\'facebook signup\')\n                 } else {\n                   window.location = \'/signup/fbSignUp/\';\n                 }\n               } else {\n                 // found a matching account on our site\n                 if ($(\'#authSignal\').length) {\n                   // this triggers when a person has arrived but was not yet logged into facebook,\n                   // or had not yet given auth to our app\n                   var newButton = \'Logging In\'\n                   $(\'#fbLoginButton1\').html(newButton);\n                   $(\'#fbLoginButton2\').html(newButton);\n                   window.location = \'/fbLoggingIn/\';\n                 } else if ($(\'#fbLoggingIn\').length) {\n                   // this element is only found on a page meant to be used as a redirect when\n                   // the \'login with facebook\' link has been clicked.\n                   window.location = \'/fbLoggingIn/\';\n                 } else {\n                   // this code is used when a person arrives and it is seen that they have \n                   // auth\'d our app and are logged into facebook \n                   // replace current button with returned result\n                   var newButton = \'<a href="/fbLogin"><img src="/images/f-login.png"></a>\'\n                   $(\'#fbLoginButton1\').html(newButton);\n                   $(\'#fbLoginButton2\').html(newButton);\n                 }\n               }\n             },1000);\n           });\n         }\n       </script>\n')
            pass
        # SOURCE LINE 212
        __M_writer(u'   </body>\n</html>\n\n')
        # SOURCE LINE 218
        __M_writer(u'\n\n')
        # SOURCE LINE 223
        __M_writer(u'\n\n')
        # SOURCE LINE 228
        __M_writer(u'\n\n')
        # SOURCE LINE 233
        __M_writer(u'\n\n')
        # SOURCE LINE 238
        __M_writer(u'\n\n')
        # SOURCE LINE 243
        __M_writer(u'\n\n')
        # SOURCE LINE 259
        __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bodyTag_extras(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 215
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headScripts(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 225
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraStyles(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 220
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headScripts2(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 230
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_google_analytics(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 245
        __M_writer(u'\n')
        # SOURCE LINE 246
        if c.conf['google.analytics']:
            # SOURCE LINE 247
            __M_writer(u'      <script type="text/javascript">\n         var _gaq = _gaq || [];\n         _gaq.push([\'_setAccount\', "')
            # SOURCE LINE 249
            __M_writer(escape(c.conf['google.analytics']))
            __M_writer(u'"]);\n         _gaq.push([\'_trackPageview\']);\n         \n         (function() {\n         var ga = document.createElement(\'script\'); ga.type = \'text/javascript\'; ga.async = true;\n         ga.src = (\'https:\' == document.location.protocol ? \'https://ssl\' : \'http://www\') + \'.google-analytics.com/ga.js\';\n         var s = document.getElementsByTagName(\'script\')[0]; s.parentNode.insertBefore(ga, s);\n         })();\n      </script>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_atlassian_issueCollector(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 261
        __M_writer(u'\n   <script type="text/javascript" src="https://civinomics.atlassian.net/s/d41d8cd98f00b204e9800998ecf8427e/en_US523t43-1988229788/6206/29/1.4.1/_/download/batch/com.atlassian.jira.collector.plugin.jira-issue-collector-plugin:issuecollector/com.atlassian.jira.collector.plugin.jira-issue-collector-plugin:issuecollector.js?collectorId=cd6cc7a9"></script>\n\n\n   <script type="text/javascript">window.ATL_JQ_PAGE_PROPS =  {\n    "triggerFunction": function(showCollectorDialog) {\n      $("#footerFeedbackButton").on( \'click\', function(e) {\n          e.preventDefault();\n          showCollectorDialog();\n        });\n        $("#helpCenter_bugReporter").on( \'click\', function(e) {\n          e.preventDefault();\n          showCollectorDialog();\n        });\n      }};</script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraScripts(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 235
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraScripts2(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 240
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


