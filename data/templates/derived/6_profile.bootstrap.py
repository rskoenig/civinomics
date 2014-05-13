# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1399837520.0065291
_template_filename = '/home/maria/civinomics/pylowiki/templates/derived/6_profile.bootstrap'
_template_uri = '/derived/6_profile.bootstrap'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['headScripts', 'extraScripts']


# SOURCE LINE 8

from pylowiki.lib.db.user import isAdmin


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

    # SOURCE LINE 7
    ns = runtime.TemplateNamespace(u'ihelpers', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_initiative_home.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'ihelpers')] = ns

    # SOURCE LINE 3
    ns = runtime.TemplateNamespace(u'lib', context._clean_inheritance_tokens(), templateuri=u'/lib/mako_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib')] = ns

    # SOURCE LINE 6
    ns = runtime.TemplateNamespace(u'photos', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_profile_photos.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'photos')] = ns

    # SOURCE LINE 4
    ns = runtime.TemplateNamespace(u'helpers', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_profile.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'helpers')] = ns

    # SOURCE LINE 5
    ns = runtime.TemplateNamespace(u'dashboard', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_profile_dashboard.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'dashboard')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base/base_indented.bootstrap', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        ihelpers = _mako_get_namespace(context, 'ihelpers')
        lib = _mako_get_namespace(context, 'lib')
        session = context.get('session', UNDEFINED)
        helpers = _mako_get_namespace(context, 'helpers')
        dashboard = _mako_get_namespace(context, 'dashboard')
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
        __M_writer(u'\n')
        # SOURCE LINE 10
        __M_writer(u'\n')
        # SOURCE LINE 11

        lib.return_to()
        
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in [] if __M_key in __M_locals_builtin_stored]))
        # SOURCE LINE 13
        __M_writer(u'\n')
        # SOURCE LINE 15
        __M_writer(u'    <!-- inline style kludge to handle fixed nav bar -->\n    ')
        # SOURCE LINE 16
 
        if c.user['memberType'] == 'organization':
            who = "Our"
        else:
            who = "My"
            
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['who'] if __M_key in __M_locals_builtin_stored]))
        # SOURCE LINE 21
        __M_writer(u'\n    <div class="spacer">\n    <div class="row-fluid" ng-controller="ProfileEditController">\n        <div class="span8">\n            <div class="tabbable"> <!-- Only required for left/right tabs -->\n                <ul class="nav nav-tabs" id="profileTabs">\n                    <li class="active"><a href="#tab-activity" data-toggle="tab" class="green green-hover">Activity</a></li>\n')
        # SOURCE LINE 28
        if c.user['memberType'] == 'organization':
            # SOURCE LINE 29
            __M_writer(u'                        <li><a href="#tab-endorsements" data-toggle="tab" class="green green-hover">Endorsements</a></li>\n                        <li><a href="#tab-forum" data-toggle="tab" class="green green-hover">Forum</a></li>\n')
            pass
        # SOURCE LINE 32
        __M_writer(u'                    <li><a href="#tab-workshops" data-toggle="tab" class="green green-hover">')
        __M_writer(escape(who))
        __M_writer(u' Workshops</a></li>\n                    <li><a href="#tab-initiatives" data-toggle="tab" class="green green-hover">')
        # SOURCE LINE 33
        __M_writer(escape(who))
        __M_writer(u' Initiatives</a></li>\n                    <li><a href="/profile/')
        # SOURCE LINE 34
        __M_writer(escape(c.user['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.user['url']))
        __M_writer(u'/photos/show">')
        __M_writer(escape(who))
        __M_writer(u' Pictures</a></li>\n                    <li><a href="/profile/')
        # SOURCE LINE 35
        __M_writer(escape(c.user['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.user['url']))
        __M_writer(u'/archives">')
        __M_writer(escape(who))
        __M_writer(u' Unpublished</a></li>\n')
        # SOURCE LINE 36
        if 'user' in session:
            # SOURCE LINE 37
            if c.user['email'] == c.authuser['email'] or isAdmin(c.authuser.id):
                # SOURCE LINE 38
                if not c.privs['provisional']:
                    # SOURCE LINE 39
                    if c.user['accessLevel'] > '200':
                        # SOURCE LINE 40
                        __M_writer(u'                                \t<li><a href="/profile/')
                        __M_writer(escape(c.user['urlCode']))
                        __M_writer(u'/')
                        __M_writer(escape(c.user['url']))
                        __M_writer(u'/csv">Upload</a></li>\n')
                        pass
                    # SOURCE LINE 42
                    __M_writer(u'                                <li class="pull-right"><a href="/profile/')
                    __M_writer(escape(c.user['urlCode']))
                    __M_writer(u'/')
                    __M_writer(escape(c.user['url']))
                    __M_writer(u'/edit">Edit Profile</a></li>\n')
                    pass
                # SOURCE LINE 44
            else:
                # SOURCE LINE 45
                __M_writer(u'                            ')
                __M_writer(escape(helpers.followButton(c.user)))
                __M_writer(u'\n')
                pass
            pass
        # SOURCE LINE 48
        __M_writer(u'                </ul>\n                <div class="tab-content">\n                    <div class="tab-pane active" id="tab-activity">\n')
        # SOURCE LINE 51
        if c.user['activated'] == "0" and isAdmin(c.authuser.id):
            # SOURCE LINE 52
            __M_writer(u'                            <button class="btn btn-civ activateButton notactivated" data-URL-list="user_')
            __M_writer(escape(c.user['urlCode']))
            __M_writer(u'_')
            __M_writer(escape(c.user['url']))
            __M_writer(u'" rel="tooltip" data-placement="bottom" data-original-title="Activate this user" id="userActivate"> \n                            <span><i class="icon-user btn-height icon-light"></i><strong> Activate </strong></span>\n                            </button>\n')
            pass
        # SOURCE LINE 56
        if c.user['memberType'] == 'organization' and 'user' in session and c.userid != c.authuser.id:
            # SOURCE LINE 57
            __M_writer(u'                            <div class="row-fluid">\n                                <div class="span2">\n                                    ')
            # SOURCE LINE 59
            __M_writer(escape(lib_6.upDownVote(c.user)))
            __M_writer(u'\n                                </div><!-- span2 -->\n                                <div class="span10">\n                                    <h3>Rate this organization</h3>\n                                </div><!-- span10 -->\n                            </div><!-- row-fluid -->\n')
            pass
        # SOURCE LINE 66
        __M_writer(u'                        ')
        __M_writer(escape(helpers.showMemberPosts(c.memberPosts)))
        __M_writer(u'\n                    </div><!-- tab-pane -->\n')
        # SOURCE LINE 68
        if c.user['memberType'] == 'organization':
            # SOURCE LINE 69
            __M_writer(u'                        <div class="tab-pane" id="tab-endorsements">\n                            ')
            # SOURCE LINE 70
            __M_writer(escape(helpers.showPositions()))
            __M_writer(u'\n                        </div><!-- tab-pane -->\n                        <div class="tab-pane" id="tab-forum">\n                            <button type="button" class="btn btn-success" data-toggle="collapse" data-target="#demo"><i class="icon-plus icon-white"></i></button>\n                             Add a discussion topic to the forum.\n                            <div id="demo" class="collapse">\n                                <div class="spacer"></div>\n                                ')
            # SOURCE LINE 77
            __M_writer(escape(helpers.addTopic()))
            __M_writer(u'\n                            </div>\n                            ')
            # SOURCE LINE 79
            __M_writer(escape(helpers.showDiscussions()))
            __M_writer(u'\n                        </div><!-- tab-pane -->\n')
            pass
        # SOURCE LINE 82
        __M_writer(u'                    <div class="tab-pane" id="tab-workshops">\n                        ')
        # SOURCE LINE 83
        __M_writer(escape(helpers.inviteCoFacilitate()))
        __M_writer(u'\n                        <table class="table table-hover table-condensed">\n                        <tbody>\n')
        # SOURCE LINE 86
        for item in c.facilitatorWorkshops:
            # SOURCE LINE 87
            __M_writer(u'                            <tr><td>')
            __M_writer(escape(helpers.showWorkshop(item, role = "Facilitating")))
            __M_writer(u'</td></tr>\n')
            pass
        # SOURCE LINE 89
        for item in c.listeningWorkshops:
            # SOURCE LINE 90
            __M_writer(u'                            <tr><td>')
            __M_writer(escape(helpers.showWorkshop(item, role = "Listening")))
            __M_writer(u'</td></tr>\n')
            pass
        # SOURCE LINE 92
        for item in c.bookmarkedWorkshops:
            # SOURCE LINE 93
            __M_writer(u'                            <tr><td>')
            __M_writer(escape(helpers.showWorkshop(item, role = "Bookmarked")))
            __M_writer(u'</td></tr>\n')
            pass
        # SOURCE LINE 95
        for item in c.privateWorkshops:
            # SOURCE LINE 96
            __M_writer(u'                            <tr><td>')
            __M_writer(escape(helpers.showWorkshop(item, role = "Private")))
            __M_writer(u'</td></tr>\n')
            pass
        # SOURCE LINE 98
        __M_writer(u'                        </tbody>\n                        </table>\n                    </div><!-- tab-pane -->\n                    <div class="tab-pane" id="tab-initiatives">\n                        <table class="table table-hover table-condensed">\n                        <tbody>\n')
        # SOURCE LINE 104
        for item in c.initiatives:
            # SOURCE LINE 105
            __M_writer(u'                            <tr><td>')
            __M_writer(escape(ihelpers.listInitiative(item, 'Author')))
            __M_writer(u'</td></tr>\n')
            pass
        # SOURCE LINE 107
        for item in c.facilitatorInitiatives:
            # SOURCE LINE 108
            __M_writer(u'                            <tr><td>')
            __M_writer(escape(ihelpers.listInitiative(item, 'Author')))
            __M_writer(u'</td></tr>\n')
            pass
        # SOURCE LINE 110
        for item in c.initiativeBookmarks:
            # SOURCE LINE 111
            __M_writer(u'                            <tr><td>')
            __M_writer(escape(ihelpers.listInitiative(item, 'Bookmarked')))
            __M_writer(u'</td></tr>\n')
            pass
        # SOURCE LINE 113
        __M_writer(u'                        </tbody>\n                        </table>\n                    </div><!-- tab-pane -->\n                </div><!-- tab-content -->\n            </div><!-- tabbable -->\n        </div><!-- span8 -->\n        <div class="span4">\n            ')
        # SOURCE LINE 120
        __M_writer(escape(dashboard.profileDashboard()))
        __M_writer(u'\n        </div><!--/.span4-->\n    </div>\n')
        # SOURCE LINE 124
        __M_writer(u'\n')
        # SOURCE LINE 146
        __M_writer(u'\n\n')
        # SOURCE LINE 158
        __M_writer(u'\n\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headScripts(context):
    context.caller_stack._push_frame()
    try:
        session = context.get('session', UNDEFINED)
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 148
        __M_writer(u'\n    <script src="')
        # SOURCE LINE 149
        __M_writer(escape(lib_6.fingerprintFile('/js/ng/profile_edit.js')))
        __M_writer(u'" type="text/javascript"></script>\n')
        # SOURCE LINE 150
        if 'user' in session:
            # SOURCE LINE 151
            if c.user.id == c.authuser.id or isAdmin(c.authuser.id):
                # SOURCE LINE 152
                __M_writer(u'            <script src="')
                __M_writer(escape(lib_6.fingerprintFile('/js/ng/alerts_admin.js')))
                __M_writer(u'" type="text/javascript"></script>\n            <script src="')
                # SOURCE LINE 153
                __M_writer(escape(lib_6.fingerprintFile('/js/profile.js')))
                __M_writer(u'" type="text/javascript"></script>\n')
                pass
            # SOURCE LINE 155
            __M_writer(u'        <script type="text/javascript" src="')
            __M_writer(escape(lib_6.fingerprintFile('/js/upDown.js')))
            __M_writer(u'"></script>\n')
            pass
        # SOURCE LINE 157
        __M_writer(u'    <script src="')
        __M_writer(escape(lib_6.fingerprintFile('/js/bootstrap/bootstrap-tab.js')))
        __M_writer(u'" type="text/javascript"></script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraScripts(context):
    context.caller_stack._push_frame()
    try:
        session = context.get('session', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 125
        __M_writer(u'\n    <script src="')
        # SOURCE LINE 126
        __M_writer(escape(lib_6.fingerprintFile('/js/follow.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script src="')
        # SOURCE LINE 127
        __M_writer(escape(lib_6.fingerprintFile('/js/activate.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script src="')
        # SOURCE LINE 128
        __M_writer(escape(lib_6.fingerprintFile('/js/vendor/jquery.expander.min.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script type="text/javascript">\n        $(document).ready(function() {\n            $(\'.expandable\').expander({\n                slicePoint: 55,\n                widow: 2,\n                expandText: \' ...->\',\n                expandPrefix: \'\',\n                userCollapseText: \' <-\',\n                userCollapsePrefix: \'\',\n                preserveWords: true\n            });\n        });\n    </script>\n')
        # SOURCE LINE 142
        if 'user' in session:
            # SOURCE LINE 143
            __M_writer(u'        <script src="')
            __M_writer(escape(lib_6.fingerprintFile('/js/ng/org_topic.js')))
            __M_writer(u'" type="text/javascript"></script>\n')
            pass
        # SOURCE LINE 145
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


