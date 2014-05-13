# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398463876.4154291
_template_filename = '/home/maria/civinomics/pylowiki/templates/derived/login.bootstrap'
_template_uri = '/derived/login.bootstrap'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['headScripts', 'extraStyles']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 2
    ns = runtime.TemplateNamespace(u'template_lib', context._clean_inheritance_tokens(), templateuri=u'/lib/template_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'template_lib')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base/base_splash.bootstrap', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        session = context.get('session', UNDEFINED)
        template_lib = _mako_get_namespace(context, 'template_lib')
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\r\n')
        # SOURCE LINE 2
        __M_writer(u'\r\n\r\n')
        # SOURCE LINE 6
        __M_writer(u'\r\n\r\n')
        # SOURCE LINE 11
        __M_writer(u'\r\n\r\n<div id="login-bg"></div>\r\n\r\n')
        # SOURCE LINE 15

        if 'loginResetPassword' in session._environ['PATH_INFO']:
          session['afterLoginURL'] = 'loginResetPassword'
        
        
        # SOURCE LINE 18
        __M_writer(u'\r\n\r\n<div class="login">\r\n  <div class="container">\r\n    <div class="row">\r\n')
        # SOURCE LINE 23
        if 'forgot' in session._environ['PATH_INFO']:
            # SOURCE LINE 24
            __M_writer(u'        <div ng-init="showTitle = \'pTitle\'">\r\n')
            # SOURCE LINE 25
        elif 'signup' in session._environ['PATH_INFO']:
            # SOURCE LINE 26
            __M_writer(u'        <div ng-init="showTitle = \'sTitle\'">\r\n')
            # SOURCE LINE 27
        elif 'login' or 'Login' in session._environ['PATH_INFO']:
            # SOURCE LINE 28
            __M_writer(u'        <div ng-init="showTitle = \'lTitle\'">\r\n')
            pass
        # SOURCE LINE 30
        __M_writer(u'          <div class="well main-well login" ng-controller="signupController">\r\n              <div class="row-fluid">\r\n                ')
        # SOURCE LINE 32
        __M_writer(escape(template_lib.tabbableSignupLogin('title')))
        __M_writer(u'\r\n              </div>\r\n              <div class="social-sign-in-separator sc-font-light sc-text-light no-bottom"></div>\r\n              <div class="row-fluid centered tcs">\r\n                  <p class="sc-font-light tcs">By joining, or logging in via Facebook or Twitter, you agree to Civinomics\' <a href="/corp/terms" target="_blank" class="green">terms of use</a> and <a href="/corp/privacy" target="_blank" class="green">privacy policy</a></p>\r\n              </div>\r\n          </div><!-- main-well -->\r\n      </div><!-- sapn6 -->\r\n    </div><!-- row -->\r\n  </div><!-- container -->\r\n</div><!-- login -->\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headScripts(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 8
        __M_writer(u'\r\n    <script src="/js/ng/signup_login.js" type="text/javascript"></script>\r\n    <script src="/js/geo.js" type="text/javascript"></script>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraStyles(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 4
        __M_writer(u'\r\n   <link href="/styles/splash.css" rel="stylesheet">\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


