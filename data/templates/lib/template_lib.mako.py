# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398540607.7875221
_template_filename = u'/home/maria/civinomics/pylowiki/templates/lib/template_lib.mako'
_template_uri = u'/lib/template_lib.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['mainNavbar', 'copyright', 'activateAccountModal', 'forgotPassword', 'search_drawer', 'splashNavbar', 'shortFooter', 'signupLoginModal', 'loginForm', 'tabbableSignupLogin', 'corpNavbar', 'signupForm', 'condensedFooter', 'socialLogins']


# SOURCE LINE 3
 
import pylowiki.lib.db.user     as userLib 
import pylowiki.lib.db.message  as messageLib
import pylowiki.lib.db.workshop as workshopLib
from types import StringTypes


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
    ns = runtime.TemplateNamespace('__anon_0x2950290', context._clean_inheritance_tokens(), templateuri=u'/lib/mako_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, '__anon_0x2950290')] = ns

def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x2950290')._populate(_import_ns, [u'fields_alert'])
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n')
        # SOURCE LINE 8
        __M_writer(u'\n\n!\n')
        # SOURCE LINE 124
        __M_writer(u'\n\n')
        # SOURCE LINE 151
        __M_writer(u'\n\n')
        # SOURCE LINE 170
        __M_writer(u'\n\n')
        # SOURCE LINE 194
        __M_writer(u'\n\n')
        # SOURCE LINE 206
        __M_writer(u'\n\n')
        # SOURCE LINE 262
        __M_writer(u'\n\n')
        # SOURCE LINE 328
        __M_writer(u'\n\n\n')
        # SOURCE LINE 359
        __M_writer(u'\n\n')
        # SOURCE LINE 373
        __M_writer(u'\n\n')
        # SOURCE LINE 435
        __M_writer(u'\n\n')
        # SOURCE LINE 459
        __M_writer(u'\n\n')
        # SOURCE LINE 480
        __M_writer(u'\n\n')
        # SOURCE LINE 520
        __M_writer(u'\n\n\n')
        # SOURCE LINE 541
        __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_mainNavbar(context):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x2950290')._populate(_import_ns, [u'fields_alert'])
        lib_6 = _mako_get_namespace(context, 'lib_6')
        def search_drawer():
            return render_search_drawer(context)
        c = _import_ns.get('c', context.get('c', UNDEFINED))
        session = _import_ns.get('session', context.get('session', UNDEFINED))
        endif = _import_ns.get('endif', context.get('endif', UNDEFINED))
        __M_writer = context.writer()
        # SOURCE LINE 11
        __M_writer(u'\n    ')
        # SOURCE LINE 12
        tagCategories = workshopLib.getWorkshopTagCategories() 
        
        __M_writer(u'\n    <div class="navbar civ-navbar navbar-fixed-top">\n        <div class="navbar-inner">\n            <div class="container">\n                <a class="brand civ-brand" href="/">\n                    <div class="logo" id="civinomicsLogo"></div>\n                </a>\n                <ul class="nav">\n                    <li class="small-hidden">\n                        <form class="form-search" action="/search">\n                            <div class="input-append">\n                                <input type="text" class="span2 search-query" name="searchQuery" placeholder="Search">\n                                <button type="submit" class="btn btn-search-first"><i class="icon-search"></i></button>\n                                <button type="button" class="btn" data-toggle="collapse" data-target="#search">Advanced</button>\n                            </div>\n                        </form>\n                    </li>\n                </ul>\n                <ul class="nav pull-right" id="profileAvatar">\n                    ')
        # SOURCE LINE 31

        wSelected = mSelected = pSelected = aSelected = hSelected = homeSelected = aSelected = bSelected = ''
        if "/workshops" in session._environ['PATH_INFO'] and not 'geo' in session._environ['PATH_INFO']:
            wSelected = "active"
        elif "/messages" in session._environ['PATH_INFO']:
            mSelected = "active"
        elif "/profile" in session._environ['PATH_INFO']:
            pSelected = "active"
        elif "/admin" in session._environ['PATH_INFO']:
            aSelected = "active"
        elif "/help" in session._environ['PATH_INFO']:
            hSelected = "active"
        elif "/home" in session._environ['PATH_INFO']:
            homeSelected = "active"
        elif "/browse/initiatives" in session._environ['PATH_INFO']:
            bSelected = "active"
        elif "/corp/about" in session._environ['PATH_INFO']:
            aSelected = "active"
        endif
                            
        
        # SOURCE LINE 50
        __M_writer(u'\n')
        # SOURCE LINE 51
        if 'user' in session:
            # SOURCE LINE 52
            __M_writer(u'                        <li class="')
            __M_writer(escape(homeSelected))
            __M_writer(u'">\n                            <a href="/">Home</a>\n                        </li>\n                        <!--<li class="')
            # SOURCE LINE 55
            __M_writer(escape(bSelected))
            __M_writer(u'"><a href="/browse/initiatives">Browse</a></li>-->\n')
            # SOURCE LINE 56
            if userLib.isAdmin(c.authuser.id):
                # SOURCE LINE 57
                __M_writer(u'                            <li class="dropdown ')
                __M_writer(escape(aSelected))
                __M_writer(u'">\n                                <a href="#" class="dropdown-toggle" data-toggle="dropdown">Objects<b class="caret"></b></a>\n                                <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu">\n                                    <li><a tabindex="-1" href="/admin/users">All Users</a></li>\n                                    <li><a tabindex="-1" href="/admin/usersNotActivated">Unactivated Users</a></li>\n                                    <li><a tabindex="-1" href="/admin/workshops">Workshops</a></li>\n                                    <li><a tabindex="-1" href="/admin/ideas">Ideas</a></li>\n                                    <li><a tabindex="-1" href="/admin/resources">Resources</a></li>\n                                    <li><a tabindex="-1" href="/admin/discussions">Discussions</a></li>\n                                    <li><a tabindex="-1" href="/admin/comments">Comments</a></li>\n                                    <li><a tabindex="-1" href="/admin/photos">Photos</a></li>\n                                    <li><a tabindex="-1" href="/admin/flaggedPhotos">Flagged Photos</a></li>\n                                    <li><a tabindex="-1" href="/admin/initiatives">Initiatives</a></li>\n                                    <li><a tabindex="-1" href="/admin/flaggedInitiatives">Flagged Initiatives</a></li>\n                                </ul>\n                            </li>\n')
                pass
            # SOURCE LINE 74
            if c.authuser['activated'] == '1':
                # SOURCE LINE 75
                __M_writer(u'                            <li class="dropdown">\n                                <a href="#" class="dropdown-toggle" data-toggle="dropdown">\n                                    Create <span class="caret"></span>\n                                </a>\n                                <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu">\n                                    <li>\n                                        <a href="/profile/')
                # SOURCE LINE 81
                __M_writer(escape(c.authuser['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.authuser['url']))
                __M_writer(u'/newInitiative"><i class="icon-file-text"></i> New Initiative</a>\n                                    </li>\n                                    <li><a href="/workshop/display/create/form"><i class="icon-gear"></i> New Workshop</a></li>\n                                </ul>\n                            </li>\n\n                            <li class="')
                # SOURCE LINE 87
                __M_writer(escape(mSelected))
                __M_writer(u'">\n                                ')
                # SOURCE LINE 88

                messageCount = ''
                numMessages = messageLib.getMessages_count(c.authuser, read = '0', count = True)
                if numMessages:
                    if numMessages > 0:
                        messageCount += '<span class="badge badge-warning left-space"> %s</span>' % numMessages
                                                
                
                # SOURCE LINE 94
                __M_writer(u'\n                                <a href="/messages/')
                # SOURCE LINE 95
                __M_writer(escape(c.authuser['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.authuser['url']))
                __M_writer(u'"><i class="icon-envelope icon-white"></i>')
                __M_writer(messageCount )
                __M_writer(u'</a>\n                            </li>\n')
                pass
            # SOURCE LINE 98
            __M_writer(u'                        <li class="dropdown ')
            __M_writer(escape(pSelected))
            __M_writer(u'">\n                            <a href="#" class="dropdown-toggle" data-toggle="dropdown">\n                                ')
            # SOURCE LINE 100
            __M_writer(escape(lib_6.userImage(c.authuser, className="avatar topbar-avatar", noLink=True)))
            __M_writer(u' Me<b class="caret"></b></a>\n                            <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu">\n                                <li><a tabindex="-1" href="/profile/')
            # SOURCE LINE 102
            __M_writer(escape(c.authuser['urlCode']))
            __M_writer(u'/')
            __M_writer(escape(c.authuser['url']))
            __M_writer(u'">My Profile</a>\n')
            # SOURCE LINE 103
            if c.authuser['activated'] == '1':
                # SOURCE LINE 104
                __M_writer(u'                                    <li><a tabindex="-1" href="/profile/')
                __M_writer(escape(c.authuser['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.authuser['url']))
                __M_writer(u'/edit#tab4">Reset Password</a>\n')
                pass
            # SOURCE LINE 106
            __M_writer(u'                                <li><a href="/help">Help</a></li>\n                                <li><a tabindex="-1" href="/login/logout">Logout</a></li>\n                            </ul>\n                        </li>\n')
            # SOURCE LINE 110
        else:
            # SOURCE LINE 111
            __M_writer(u'                        <li class="')
            __M_writer(escape(bSelected))
            __M_writer(u'"><a href="/browse/initiatives">Browse</a></li>\n                        <li class="')
            # SOURCE LINE 112
            __M_writer(escape(hSelected))
            __M_writer(u'"><a href="/help">Help</a></li>\n                        <li><a href="/login">Login</a></li>\n                        <li><a href="/signup">Signup</a></li>\n')
            pass
        # SOURCE LINE 116
        __M_writer(u'                    <li class="small-show">\n                        <a type="button" data-toggle="collapse" data-target="#search"><i class="icon-search"></i></a>\n                    </li>\n                </ul>\n            </div> <!--/.container-->\n        </div> <!--/.navbar-inner.civ-navbar -->\n    </div> <!-- /.navbar -->\n    ')
        # SOURCE LINE 123
        __M_writer(escape(search_drawer()))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_copyright(context):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x2950290')._populate(_import_ns, [u'fields_alert'])
        __M_writer = context.writer()
        # SOURCE LINE 196
        __M_writer(u'\n    <div id="baseTemplate_footer">\n        <div id="footerContainer" class="container">\n            <div class="row footer well">\n                <div class="span pull-right">\n                  \xa9 2014 Civinomics\n                </div>\n            </div><!-- row footer well -->\n        </div><!-- footerContainer -->\n    </div><!-- baseTemplate_footer -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_activateAccountModal(context):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x2950290')._populate(_import_ns, [u'fields_alert'])
        c = _import_ns.get('c', context.get('c', UNDEFINED))
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 523
        __M_writer(u'\n    <div id="activateAccountModal" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="activateAccountModal" aria-hidden="true">\n      <div class="modal-header">\n        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\n        <h3>Activate Your Account</h3>\n      </div>\n      <div class="modal-body">\n        <p>You can\'t add comments, ideas, discussions or resources until you\'ve activated your account.</p>\n\n        <p>To activate your account, click the link in your activation email from <strong>registration@civinomics.com</strong>. Don\'t see the email? Check your Spam or Junk folder.</p>\n        <div class="top-space green" id="resendMessage"></div>\n      </div>\n      <div class="modal-footer">\n        <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>\n        <button class="btn btn-success resendActivateEmailButton" data-URL-list="user_')
        # SOURCE LINE 537
        __M_writer(escape(c.authuser['urlCode']))
        __M_writer(u'_')
        __M_writer(escape(c.authuser['url']))
        __M_writer(u'">Resend Activation Email</button>\n      </div>\n    </div>\n    <script src="')
        # SOURCE LINE 540
        __M_writer(escape(lib_6.fingerprintFile('/js/activate.js')))
        __M_writer(u'" type="text/javascript"></script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_forgotPassword(context):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x2950290')._populate(_import_ns, [u'fields_alert'])
        __M_writer = context.writer()
        # SOURCE LINE 461
        __M_writer(u'\n    <div class="row-fluid">\n        <div class="span8 offset2">\n            <p class="centered">Enter your email and click \'Reset Password.\' Then check your inbox for your new password.</p>\n        </div>\n    <form id="forgot_password" action="/forgotPasswordHandler" class="form form-horizontal" method="post">\n        <div class="control-group">\n            <label class="control-label" for="email"> Email: </label>\n            <div class="controls">\n                <input type="email" name="email" id="email"><br>\n                <a href="#login" ng-click="switchLoginTitle()" data-toggle="tab" class="green green-hover"> Back to log in</a>\n            </div>\n        </div>\n        <div class="control-group">\n            <div class="controls">\n                <button type="submit" class="btn btn-success"> Reset Password </button>\n            </div>\n        </div>\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_search_drawer(context):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x2950290')._populate(_import_ns, [u'fields_alert'])
        __M_writer = context.writer()
        # SOURCE LINE 264
        __M_writer(u'\n    <div id="search" class="collapse search_drawer">\n        ')
        # SOURCE LINE 266
        tagCategories = workshopLib.getWorkshopTagCategories() 
        
        __M_writer(u'\n        <div class="spacer"></div>\n        <div class="row-fluid searches">\n            <div class="span3 offset1 small-show">\n                <form class="form-search" action="/search">\n                    <input type="text" class="search-query" placeholder="Search by Word" id="search-input" name="searchQuery">\n                </form>\n            </div>\n            <div class="span4">\n                <script type="text/javascript">\n                    function searchTags() {\n                        var sIndex = document.getElementById(\'categoryTag\').selectedIndex;\n                        var sValue = document.getElementById(\'categoryTag\').options[sIndex].value;\n                        if(sValue) {\n                            var queryURL = sValue;\n                            window.location = queryURL;\n                        }\n                    }\n                </script>\n                <form action="/searchTags" class="form-search search-type" method="POST">\n                    <i class="icon-tag icon-light"></i>\n                    <select name="categoryTag" id="categoryTag" onChange="searchTags();">\n                    <option value="0">Search by Category</option>\n')
        # SOURCE LINE 289
        for tag in tagCategories:
            # SOURCE LINE 290
            __M_writer(u'                        ')
            tagValue = tag.replace(" ", "_") 
            
            __M_writer(u'\n                        <option value="/searchTags/')
            # SOURCE LINE 291
            __M_writer(escape(tagValue))
            __M_writer(u'/">')
            __M_writer(escape(tag.title()))
            __M_writer(u'</option>\n')
            pass
        # SOURCE LINE 293
        __M_writer(u'                    </select>\n                </form>\n            </div><!-- span4 -->\n            <div class="span4">\n                <form  action="/searchGeo"  class="form-search search-type" method="POST">\n                    <div class="row-fluid"><span id="searchCountrySelect">\n                        <i class="icon-globe icon-light"></i>\n                        <select name="geoSearchCountry" id="geoSearchCountry" class="geoSearchCountry" onChange="geoSearchCountryChange(); return 1;">\n                        <option value="0" selected>Search by Region</option>\n                        <option value="United States">United States</option>\n                        </span><!-- searchCountrySelect -->\n                        </select>\n                        <span id="searchCountryButton"></span>\n                    </div><!-- row-fluid -->\n                    <div class="row-fluid">\n                        <span id="searchStateSelect"></span>\n                        <span id="searchStateButton"></span>\n                    </div>\n                    <div class="row-fluid">\n                        <span id="searchCountySelect"></span>\n                        <span id="searchCountyButton"></span>\n                    </div>\n                    <div class="row-fluid">\n                        <span id="searchCitySelect"></span>\n                        <span id="searchCityButton"></span>\n                    </div>\n                    <div class="row-fluid">\n                        <span id="searchPostalSelect"></span>\n                        <span id="searchPostalButton">\n                    </div>\n                </form>\n            </div><!-- span4 -->\n        </div><!-- row-fluid -->\n        <div class="spacer"></div>\n    </div><!-- collapse -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_splashNavbar(context):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x2950290')._populate(_import_ns, [u'fields_alert'])
        def search_drawer():
            return render_search_drawer(context)
        __M_writer = context.writer()
        # SOURCE LINE 126
        __M_writer(u'\n    <div class="navbar splash-nav" ng-init="showTitle = \'sTitle\'">\n      <div class="navbar-inner civinomics-splash">\n        <div class="container-fluid">\n            <a class="brand" href="/"><div class="logo logo-lg" id="civinomicsLogo"></div></a>\n            <ul class="nav">\n                <li class="small-hidden">\n                    <form class="form-search" action="/search">\n                        <input type="text" class="span2 search-query splash" placeholder="Search" name="searchQuery">\n                    </form>\n                </li>\n            </ul>\n            <ul class="nav pull-right">\n                <li class="nav-item"><a href="/corp/about" class="nav-item">About</a></li>\n                <li class="nav-item"><a href="/browse/initiatives" class="nav-item">Browse</a></li>\n                <li class="nav-item"><a href="http://civinomics.wordpress.com" target="_blank" class="nav-item">Blog</a></li>\n                <!-- <li class="nav-item"><a href="/corp/about" class="nav-item">Create</a></li> -->\n                <li class="nav-item">\n                    <a href="/login" class="btn nav-login">Log in</a>                            \n                </li>\n            </ul>\n        </div>\n      </div>\n    </div>\n    ')
        # SOURCE LINE 150
        __M_writer(escape(search_drawer()))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_shortFooter(context):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x2950290')._populate(_import_ns, [u'fields_alert'])
        __M_writer = context.writer()
        # SOURCE LINE 172
        __M_writer(u'\n    </div><!-- kludge for case of missing close div tag -->\n    <div id="baseTemplate_footer">\n        <div id="footerContainer" class="container">\n            <div class="row footer well">\n                <div class="span8 no-left">\n                    <ul class="horizontal-list">\n                        <li><a class="green green-hover" href="/corp/about">About</a></li> \n                        <li><a class="green green-hover" href="http://civinomics.wordpress.com" target="_blank">Blog</a></li>\n                        <li><a class="green green-hover" href="/corp/polling">Polling</a></li>\n                        <li><a class="green green-hover" href="/corp/contact">Contact</a></li>\n                        <li><a class="green green-hover" href="/corp/terms">Terms</a></li>\n                        <li><a class="green green-hover" href="/help">Help</a></li>\n                        <li><a class="green green-hover" href="#" id="footerFeedbackButton">Feedback</a></li>\n                    </ul>\n                </div><!-- span8 -->\n                <div class="span pull-right">\n                  \xa9 2014 Civinomics\n                </div><!-- span pull-right -->\n            </div><!-- row footer well -->\n        </div><!-- footerContainer -->\n    </div><!-- baseTemplate_footer -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_signupLoginModal(context):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x2950290')._populate(_import_ns, [u'fields_alert'])
        def tabbableSignupLogin(*args):
            return render_tabbableSignupLogin(context,*args)
        session = _import_ns.get('session', context.get('session', UNDEFINED))
        __M_writer = context.writer()
        # SOURCE LINE 482
        __M_writer(u'\n    <!-- Signup Login Modal -->\n    ')
        # SOURCE LINE 484
 
      ####
      #### After Login URL
      ####
        alURL= session._environ['PATH_INFO']
        if 'QUERY_STRING' in session._environ :
          alURL = alURL + '?' + session._environ['QUERY_STRING'] 
        # handles exception with geo pages where angular appends itself to URL
        if '{{' in alURL:
          try:
              alURL = session._environ['HTTP_REFERER']
          except:
              alURL = '/browse/initiatives'
        if 'zip/lookup' in alURL or '/signup' in alURL:
          alURL = '/home'
        session['afterLoginURL'] = alURL
            
        
        # SOURCE LINE 500
        __M_writer(u'\n\n    <div id="signupLoginModal" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="signupLoginModal" aria-hidden="true" ng-controller="signupController" ng-init="showTitle = \'sTitle\'">\n      <div class="modal-header">\n        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">\xd7</button>\n        <h3 ng-show="showTitle == \'sTitle\'" class="login top centered" ng-cloak>Sign up</h3>\n        <h3 ng-show="showTitle == \'lTitle\'" class="login top centered" ng-cloak>Log in</h3>\n        <h3 ng-show="showTitle == \'pTitle\'" class="login top centered" ng-cloak>Forgot Password</h3>\n      </div>\n      <div class="modal-body">\n        ')
        # SOURCE LINE 510
        __M_writer(escape(tabbableSignupLogin()))
        __M_writer(u'\n      </div>\n      <div class="modal-footer">\n        <div class="row-fluid centered tcs">\n          <div class="span10 offset1">\n            <p class="sc-font-light tcs">By joining, or logging in via Facebook or Twitter, you agree to Civinomics\' <a href="/corp/terms" target="_blank" class="green">terms of use</a> and <a href="/corp/privacy" target="_blank" class="green">privacy policy</a></p>\n          </div>\n        </div>\n      </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_loginForm(context):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x2950290')._populate(_import_ns, [u'fields_alert'])
        __M_writer = context.writer()
        # SOURCE LINE 437
        __M_writer(u'\n    <form id="sign_in" action="/loginHandler" class="form form-horizontal" method="post">\n        <div class="control-group">\n            <label class="control-label" for="email"> Email: </label>\n            <div class="controls">\n                <input type="email" name="email" id="email" required>\n            </div>\n        </div>\n        <div class="control-group">\n            <label class="control-label" for="passphrase"> Password: </label>\n            <div class="controls">\n                <input type="password" name="password" id="password"><br>\n                <a href="#forgot" ng-click="switchPasswordTitle()" data-toggle="tab" class="green green-hover"> Forgot password?</a>\n            </div>\n        </div>\n        <div class="control-group">\n            <div class="controls">\n                <button type="submit" class="btn btn-civ login"> Log in </button>\n            </div>\n        </div>\n    </form>\n    <p class="centered">Don\'t have an account? <a href="#signup" ng-click="switchSignupTitle()" class="green green-hover" data-toggle="tab">Sign up</a></p>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_tabbableSignupLogin(context,*args):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x2950290')._populate(_import_ns, [u'fields_alert'])
        fields_alert = _import_ns.get('fields_alert', context.get('fields_alert', UNDEFINED))
        c = _import_ns.get('c', context.get('c', UNDEFINED))
        def forgotPassword():
            return render_forgotPassword(context)
        def signupForm():
            return render_signupForm(context)
        def loginForm():
            return render_loginForm(context)
        def socialLogins():
            return render_socialLogins(context)
        __M_writer = context.writer()
        # SOURCE LINE 331
        __M_writer(u'\n')
        # SOURCE LINE 332
        if c.conf['read_only.value'] == 'true':
            # SOURCE LINE 333
            __M_writer(u'      <h1> Sorry, Civinomics is in read only mode right now </h1>\n')
            # SOURCE LINE 334
        else:
            # SOURCE LINE 335
            if 'title' in args:
                # SOURCE LINE 336
                __M_writer(u'            <h2 ng-show="showTitle == \'sTitle\'" class="login top centered" ng-cloak>Sign up</h2>\n            <h2 ng-show="showTitle == \'lTitle\'" class="login top centered" ng-cloak>Log in</h2>\n            <h2 ng-show="showTitle == \'pTitle\'" class="login top centered" ng-cloak>Forgot Password</h2>\n')
                pass
            # SOURCE LINE 340
            __M_writer(u'        ')
            __M_writer(escape(fields_alert()))
            __M_writer(u'\n')
            # SOURCE LINE 341
            if c.splashMsg:
                # SOURCE LINE 342
                __M_writer(u'            ')
                message = c.splashMsg 
                
                __M_writer(u'\n            <div class="alert alert-')
                # SOURCE LINE 343
                __M_writer(escape(message['type']))
                __M_writer(u'">\n                <button data-dismiss="alert" class="close">x</button>\n                <strong>')
                # SOURCE LINE 345
                __M_writer(escape(message['title']))
                __M_writer(u'</strong> ')
                __M_writer(escape(message['content']))
                __M_writer(u'\n            </div> \n')
                pass
            # SOURCE LINE 348
            __M_writer(u'      ')
            __M_writer(escape(socialLogins()))
            __M_writer(u'\n      <div ng-show="showTitle == \'sTitle\'" ng-cloak>\n        ')
            # SOURCE LINE 350
            __M_writer(escape(signupForm()))
            __M_writer(u'\n      </div>\n      <div ng-show="showTitle == \'lTitle\'" ng-cloak>\n        ')
            # SOURCE LINE 353
            __M_writer(escape(loginForm()))
            __M_writer(u'\n      </div>\n      <div ng-show="showTitle == \'pTitle\'" ng-cloak>\n        ')
            # SOURCE LINE 356
            __M_writer(escape(forgotPassword()))
            __M_writer(u'\n      </div>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_corpNavbar(context):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x2950290')._populate(_import_ns, [u'fields_alert'])
        __M_writer = context.writer()
        # SOURCE LINE 153
        __M_writer(u'\n    <div class="navbar navbar-fixed-top">\n        <div class="navbar-inner">\n            <div class="container-fluid">\n                <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">\n                    <span class="icon-bar"></span>\n                    <span class="icon-bar"></span>\n                    <span class="icon-bar"></span>\n                </a>\n                <div class="span2 offset" style="padding-top: 2px; padding-bottom: 5px;">\n                    <a href="/"><img src="/images/logo_white.png"></a>\n                </div>\n                <div class="nav-collapse">\n                </div><!--/.nav-collapse -->\n            </div>\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_signupForm(context):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x2950290')._populate(_import_ns, [u'fields_alert'])
        __M_writer = context.writer()
        # SOURCE LINE 375
        __M_writer(u'\n        <form id="sign_in" action="/signup/handler" class="form form-horizontal" name="signupForm" method="POST">\n            <input type="hidden" name="country" value="United States">\n\n            <div ng-class=" {\'control-group\': true, \'error\': signupForm.name.$error.pattern} ">\n                <label class="control-label" for="name"> Full name: </label>\n                <div class="controls">\n                    <input type="text" name="name" id="name" ng-model="fullName" ng-pattern="fullNameRegex" required>\n                    <span class="error help-block" ng-show="signupForm.name.$error.pattern" ng-cloak>Use only letters, numbers, spaces, and _ (underscore)</span>\n                </div>\n            </div>\n            <div class="control-group">\n                <label class="control-label" for="email"> Email: </label>\n                <div class="controls">\n                    <input type="email" name="email" id="email" ng-model="email" required>\n                    <span class="error help-block" ng-show="signupForm.email.$error.email" ng-cloak>Not a valid email!</span>\n                </div>\n            </div>\n            <div class="control-group">\n                <label class="control-label" for="passphrase"> Password: </label>\n                <div class="controls">\n                    <input type="password" name="password" id="passphrase" ng-model= "passphrase1" required>\n                </div>\n            </div>\n            <div class="control-group">\n                <label class="control-label" for="memberType">Membership Type</label>\n                <div class="controls">\n                    <label class="radio">\n                        <input type="radio" name="memberType" id="memberType1" ng-model="memberType1" value="professional" checked>\n                        This membership is for an individual\n                    </label>\n                    <label class="radio">\n                        <input type="radio" name="memberType" id="memberType2" ng-model="memberType2" value="organization">\n                        This membership is for an organization\n                    </label>\n                </div>\n            </div>\n            <div ng-class=" {\'control-group\': true, \'error\': signupForm.postalCode.$error.pattern} " ng-cloak>\n                <label class="control-label" for="postalCode"><i class="icon-question-sign" rel="tooltip" data-placement="top" data-title="To help you find relevant topics in your region. Never displayed or shared." title="To help you find relevant topics in your region. Never displayed or shared."></i> Zip Code: </label>\n                <div class="controls">\n                    <input class="input-small" type="text" name="postalCode" id="postalCode" ng-model="postalCode" ng-pattern="postalCodeRegex" ng-minlength="5" ng-maxlength="5" ng-blur="lookup()" required>\n                    <span class="error help-block" ng-show="signupForm.postalCode.$error.pattern" ng-cloak>Invalid zip code!</span>\n                    <div id="postalGeoString">{{geos[0][\'name\']}}{{geos[0][\'sep\']}} {{geos[1][\'name\']}}{{geos[1][\'sep\']}} {{geos[3][\'name\']}}</div>\n                </div>\n            </div>\n            <div class="control-group">\n                <label class="control-label" for="terms">&nbsp;</label>\n                <div class="controls">\n                    <span id="terms">&nbsp;</span>\n                </div>\n            </div>\n            <div class="control-group">\n                <label class="control-label" for="submit">&nbsp;</label>\n                <div class="controls">\n                    <button type="submit" name="submit" class="btn btn-success signup">Sign up</button>\n                </div>\n            </div>\n        </form>\n        <script src="/js/signup.js" type="text/javascript"></script>\n        <p class="centered"> Already have an account? <a href="#login" ng-click="switchLoginTitle()" class="green green-hover" data-toggle="tab">Log in</a></p>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_condensedFooter(context):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x2950290')._populate(_import_ns, [u'fields_alert'])
        lib_6 = _mako_get_namespace(context, 'lib_6')
        c = _import_ns.get('c', context.get('c', UNDEFINED))
        isinstance = _import_ns.get('isinstance', context.get('isinstance', UNDEFINED))
        __M_writer = context.writer()
        # SOURCE LINE 208
        __M_writer(u'\n    <div class="footer-civ condensed">\n        <div class="container-fluid" >\n            <div class="row-fluid pretty">\n                <div class="span5">\n                    <div class="pull-right">\n                        \xa9 2014 Civinomics, Inc. \n                        <ul class="horizontal-list">\n                            <li><a href="/corp/terms">Terms</a></li>\n                            <li><a href="/corp/privacy">Privacy</a></li>\n                            <li><a href="/corp/news">News</a></li>\n                            <li><a href="/corp/contact">Contact</a></li>\n                        </ul>\n                    </div>\n                </div>\n                <div class="span2 centered">\n                    <img src="/images/logo_white_simple.png">\n                </div>\n                <div class="span5">\n                    <ul class="horizontal-list">\n                        <li><a href="/corp/careers">Careers</a></li>\n                        <li><a href="/corp/team">Team</a></li>\n                        <li><a href="http://www.civinomics.wordpress.com" target="_blank">Blog</a></li>\n                        <li><a href="/corp/caseStudies">Case Studies</a></li>\n                    </ul>\n                </div>\n            </div>\n            <div class="row-fluid simple">\n                <div class="span10">\n                    <ul class="horizontal-list">\n                        <li><a href="/corp/terms">Terms</a></li>\n                        <li><a href="/corp/privacy">Privacy</a></li>\n                        <li><a href="/corp/news">News</a></li>\n                        <li><a href="/corp/contact">Contact</a></li>\n                        <li><a href="/corp/careers">Careers</a></li>\n                        <li><a href="/corp/team">Team</a></li>\n                        <li><a href="http://www.civinomics.wordpress.com" target="_blank">Blog</a></li>\n                        <li><a href="/corp/caseStudies">Case Studies</a></li>\n                        <li>\xa9 2014 Civinomics, Inc. </li>\n                    </ul>\n                </div>\n                <div class="span2 centered">\n                    <img src="/images/logo_white_simple.png">\n                </div>\n            </div>\n            <div class="row-fluid">\n')
        # SOURCE LINE 254
        if not isinstance(c.backgroundAuthor, StringTypes):
            # SOURCE LINE 255
            __M_writer(u'\t\t\t<em class="photo-cred">Cover photo: "')
            __M_writer(escape(c.backgroundPhoto['title']))
            __M_writer(u'", Author: ')
            __M_writer(escape(lib_6.userLink(c.backgroundAuthor)))
            __M_writer(u' ')
            __M_writer(escape(lib_6.userImage(c.backgroundAuthor, className="avatar topbar-avatar", noLink=True)))
            __M_writer(u' </em>\n')
            # SOURCE LINE 256
        else:
            # SOURCE LINE 257
            __M_writer(u'\t\t\t<em class="photo-cred">Cover photo: "')
            __M_writer(escape(c.backgroundPhoto['title']))
            __M_writer(u'", Author: ')
            __M_writer(escape(c.backgroundAuthor))
            __M_writer(u'</em>\n')
            pass
        # SOURCE LINE 259
        __M_writer(u'            </div>\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_socialLogins(context):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x2950290')._populate(_import_ns, [u'fields_alert'])
        __M_writer = context.writer()
        # SOURCE LINE 361
        __M_writer(u'\n    <div class="row-fluid social-login centered">\n        <div id="fbLoginButton2">\n            <a onclick="facebookLogin()"><img src="/images/f-login.png"></a>\n        </div>\n        <div id="twtLoginButton1">\n            <a href="/twitterLoginBegin"><img src="/images/t-login.png"></a>\n        </div>\n    </div>\n    <div class="social-sign-in-separator sc-font-light sc-text-light">\n        <span>or</span>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


