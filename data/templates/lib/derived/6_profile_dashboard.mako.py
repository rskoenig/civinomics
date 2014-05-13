# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398540607.7357211
_template_filename = u'/home/maria/civinomics/pylowiki/templates/lib/derived/6_profile_dashboard.mako'
_template_uri = u'/lib/derived/6_profile_dashboard.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['profileDashboard']


# SOURCE LINE 1

import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.facilitator  as facilitatorLib
import pylowiki.lib.db.listener     as listenerLib
import pylowiki.lib.db.follow       as followLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.pmember      as pmemberLib
import pylowiki.lib.utils           as utils


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 11
    ns = runtime.TemplateNamespace(u'lib_6', context._clean_inheritance_tokens(), templateuri=u'/lib/6_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib_6')] = ns

def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 9
        __M_writer(u'\n\n')
        # SOURCE LINE 11
        __M_writer(u'\n\n')
        # SOURCE LINE 185
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_profileDashboard(context):
    context.caller_stack._push_frame()
    try:
        session = context.get('session', UNDEFINED)
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 13
        __M_writer(u'\n    <div class="centered">\n        ')
        # SOURCE LINE 15
        __M_writer(escape(lib_6.userImage(c.user, className="avatar avatar-large")))
        __M_writer(u'\n    </div>\n    <div class="section-wrapper">\n        <div class="browse">\n')
        # SOURCE LINE 19
        if ('user' in session and c.user.id == c.authuser.id) or c.isAdmin:
            # SOURCE LINE 20
            __M_writer(u'                <div ng-init="dashboardFullName=\'')
            __M_writer(escape(c.user['name']))
            __M_writer(u"'; greetingMsg='")
            __M_writer(escape(c.user['greetingMsg']))
            __M_writer(u"'; fullName='")
            __M_writer(escape(c.user['name']))
            __M_writer(u"'; websiteDesc='")
            __M_writer(escape(c.user['websiteDesc']))
            __M_writer(u"'; postalCode='")
            __M_writer(escape(c.user['postalCode']))
            __M_writer(u'\'; updateGeoLinks();";>\n                    <h3 class="section-header">{{fullName}}</h3>\n                    <p><a href="{{cityURL}}">{{cityTitle}}</a>, <a href="{{stateURL}}">{{stateTitle}}</a>, <a href="{{countryURL}}">{{countryTitle}}</a>\n                </div>\n')
            # SOURCE LINE 24
        else:
            # SOURCE LINE 25
            __M_writer(u'                <h3 class="section-header">')
            __M_writer(escape(c.user['name']))
            __M_writer(u'</h3>\n                <p>')
            # SOURCE LINE 26
            __M_writer(escape(lib_6.userGeoLink(c.user)))
            __M_writer(u'</p>\n')
            pass
        # SOURCE LINE 28
        __M_writer(u'            \n            <p>Joined ')
        # SOURCE LINE 29
        __M_writer(escape(c.user.date.strftime('%b %d, %Y')))
        __M_writer(u'</p>\n            \n')
        # SOURCE LINE 31
        if c.user['greetingMsg'] != '':
            # SOURCE LINE 32
            if ('user' in session and c.user.id == c.authuser.id) or c.isAdmin:
                # SOURCE LINE 33
                __M_writer(u'                    <div ng-init="dashboardGreetingMsg=\'')
                __M_writer(escape(c.user['greetingMsg']))
                __M_writer(u'\'">\n                    <small class="muted expandable">{{greetingMsg}}</small>\n')
                # SOURCE LINE 35
            else:
                # SOURCE LINE 36
                __M_writer(u'                    <small class="muted expandable">')
                __M_writer(escape(c.user['greetingMsg']))
                __M_writer(u'</small>\n')
                pass
            pass
        # SOURCE LINE 39
        if c.user['websiteLink'] != '':
            # SOURCE LINE 40
            if ('user' in session and c.user.id == c.authuser.id) or c.isAdmin:
                # SOURCE LINE 41
                __M_writer(u'                    <div ng-init="dashboardWebsiteLink=\'')
                __M_writer(escape(c.user['websiteLink']))
                __M_writer(u'\'">\n                    <p class = "expandable no-bottom"><a href="{{dashboardWebsiteLink}}" target="_blank">{{dashboardWebsiteLink}}</a></p>\n')
                # SOURCE LINE 43
            else:
                # SOURCE LINE 44
                __M_writer(u'                    <p class = "expandable no-bottom"><a href="')
                __M_writer(escape(c.user['websiteLink']))
                __M_writer(u'" target="_blank">')
                __M_writer(escape(c.user['websiteLink']))
                __M_writer(u'</a></p>\n')
                pass
            # SOURCE LINE 46
            if c.user['websiteDesc'] != '':
                # SOURCE LINE 47
                if ('user' in session and c.user.id == c.authuser.id) or c.isAdmin:
                    # SOURCE LINE 48
                    __M_writer(u'                        <div ng-init="dashboardWebsiteDesc=\'')
                    __M_writer(escape(c.user['websiteDesc']))
                    __M_writer(u'\'">\n                            <small class="muted expandable">{{websiteDesc}}</small>\n                        </div>\n')
                    # SOURCE LINE 51
                else:
                    # SOURCE LINE 52
                    __M_writer(u'                        <small class="muted expandable">')
                    __M_writer(escape(c.user['websiteDesc']))
                    __M_writer(u'</small>\n')
                    pass
                pass
            pass
        # SOURCE LINE 56
        __M_writer(u'\n            <hr>\n            <div class="row-fluid">\n                <div class="span4">\n                    ')
        # SOURCE LINE 60
 
        thingListingURL = "/profile/%s/%s/resources" %(c.user['urlCode'], c.user['url'])
        if 'resource_counter' in c.user:
            numThings = c.user['resource_counter']
        else:
            numThings = '0'
                            
        
        # SOURCE LINE 66
        __M_writer(u'\n                    <h3 class="profile-count centered">\n                    <a class="black" href="')
        # SOURCE LINE 68
        __M_writer(escape(thingListingURL))
        __M_writer(u'">')
        __M_writer(escape(numThings))
        __M_writer(u'</a>\n                    </h3>\n                    <div class="centered"><p><a class="green green-hover" href="')
        # SOURCE LINE 70
        __M_writer(escape(thingListingURL))
        __M_writer(u'">resources</a></p></div>\n                </div><!-- span4 -->\n                <div class="span4">\n                    ')
        # SOURCE LINE 73
 
        thingListingURL = "/profile/%s/%s/ideas" %(c.user['urlCode'], c.user['url'])
        if 'idea_counter' in c.user:
            numThings = c.user['idea_counter']
        else:
            numThings = '0'
                            
        
        # SOURCE LINE 79
        __M_writer(u'\n                    <h3 class="profile-count centered">\n                    <a class="black" href="')
        # SOURCE LINE 81
        __M_writer(escape(thingListingURL))
        __M_writer(u'">')
        __M_writer(escape(numThings))
        __M_writer(u'</a>\n                    </h3>\n                    <div class="centered"><p><a class="green green-hover" href="')
        # SOURCE LINE 83
        __M_writer(escape(thingListingURL))
        __M_writer(u'">ideas</a></p></div>\n                </div>\n                <div class="span4">\n                    ')
        # SOURCE LINE 86
 
        thingListingURL = "/profile/%s/%s/discussions" %(c.user['urlCode'], c.user['url'])
        if 'discussion_counter' in c.user:
            numThings = c.user['discussion_counter']
        else:
            numThings = '0'
                            
        
        # SOURCE LINE 92
        __M_writer(u'\n                    <h3 class="profile-count centered">\n                    <a class="black" href="')
        # SOURCE LINE 94
        __M_writer(escape(thingListingURL))
        __M_writer(u'">')
        __M_writer(escape(numThings))
        __M_writer(u'</a>\n                    </h3>\n                    <div class="centered"><p><a class="green green-hover" href="')
        # SOURCE LINE 96
        __M_writer(escape(thingListingURL))
        __M_writer(u'">conversations</a></p></div>\n                </div>\n            </div> <!--/.row-fluid-->\n            <hr>\n            <div class="row-fluid">\n                <div class="span4">\n                    ')
        # SOURCE LINE 102
 
        thingListingURL = "/profile/%s/%s/followers" %(c.user['urlCode'], c.user['url'])
        if 'follower_counter' in c.user:
            numThings = c.user['follower_counter']
        else:
            numThings = '0'
                            
        
        # SOURCE LINE 108
        __M_writer(u'\n                    <h3 class="profile-count centered">\n                    <a class="black" href="')
        # SOURCE LINE 110
        __M_writer(escape(thingListingURL))
        __M_writer(u'">')
        __M_writer(escape(numThings))
        __M_writer(u'</a>\n                    </h3>\n                    <div class="centered"><p><a class="green green-hover" href="')
        # SOURCE LINE 112
        __M_writer(escape(thingListingURL))
        __M_writer(u'">followers</a></p></div>\n                </div>\n                <div class="span4">\n                    ')
        # SOURCE LINE 115
 
        thingListingURL = "/profile/%s/%s/following" %(c.user['urlCode'], c.user['url'])
        if 'follow_counter' in c.user:
            numThings = c.user['follow_counter']
        else:
            numThings = '0'
                            
        
        # SOURCE LINE 121
        __M_writer(u'\n                    <h3 class="profile-count centered">\n                    <a class="black" href="')
        # SOURCE LINE 123
        __M_writer(escape(thingListingURL))
        __M_writer(u'">')
        __M_writer(escape(numThings))
        __M_writer(u'</a>\n                    </h3>\n                    <div class="centered"><p><a class="green green-hover" href="')
        # SOURCE LINE 125
        __M_writer(escape(thingListingURL))
        __M_writer(u'">following</a></p></div>\n                </div>\n                <div class="span4">\n                    ')
        # SOURCE LINE 128
 
        thingListingURL = "/profile/%s/%s/watching" %(c.user['urlCode'], c.user['url'])
        if 'bookmark_counter' in c.user:
            numThings = c.user['bookmark_counter']
        else:
            numThings = '0'
                            
        
        # SOURCE LINE 134
        __M_writer(u'\n                    <h3 class="profile-count centered">\n                    <a class="black" href="')
        # SOURCE LINE 136
        __M_writer(escape(thingListingURL))
        __M_writer(u'">')
        __M_writer(escape(numThings))
        __M_writer(u'</a>\n                    </h3>\n                    <div class="centered"><p><a class="green green-hover" href="')
        # SOURCE LINE 138
        __M_writer(escape(thingListingURL))
        __M_writer(u'">bookmarks</a></p></div>\n                </div>\n            </div> <!--/.row-fluid-->\n                        <hr>\n            <div class="row-fluid">\n                <div class="span4">\n                    ')
        # SOURCE LINE 144
 
        thingListingURL = "/profile/%s/%s/pictures" %(c.user['urlCode'], c.user['url'])
        if 'photo_counter' in c.user:
            numThings = c.user['photo_counter']
        else:
            numThings = '0'
                            
        
        # SOURCE LINE 150
        __M_writer(u'\n                    <h3 class="profile-count centered">\n                    <a class="black" href="')
        # SOURCE LINE 152
        __M_writer(escape(thingListingURL))
        __M_writer(u'">')
        __M_writer(escape(numThings))
        __M_writer(u'</a>\n                    </h3>\n                    <div class="centered"><p><a class="green green-hover" href="')
        # SOURCE LINE 154
        __M_writer(escape(thingListingURL))
        __M_writer(u'">pictures</a></p></div>\n                </div>\n                <div class="span4">\n                    ')
        # SOURCE LINE 157
 
        thingListingURL = "/profile/%s/%s/facilitating" %(c.user['urlCode'], c.user['url'])
        if 'facilitator_counter' in c.user:
            numThings = c.user['facilitator_counter']
        else:
            numThings = '0'
                            
        
        # SOURCE LINE 163
        __M_writer(u'\n                    <h3 class="profile-count centered">\n                    <a class="black" href="')
        # SOURCE LINE 165
        __M_writer(escape(thingListingURL))
        __M_writer(u'">')
        __M_writer(escape(numThings))
        __M_writer(u'</a>\n                    </h3>\n                    <div class="centered"><p><a class="green green-hover" href="')
        # SOURCE LINE 167
        __M_writer(escape(thingListingURL))
        __M_writer(u'">facilitating</a></p></div>\n                </div>\n                <div class="span4">\n                    ')
        # SOURCE LINE 170
 
        thingListingURL = "/profile/%s/%s/listening" %(c.user['urlCode'], c.user['url'])
        if 'listener_counter' in c.user:
            numThings = c.user['listener_counter']
        else:
            numThings = '0'
                            
        
        # SOURCE LINE 176
        __M_writer(u'\n                    <h3 class="profile-count centered">\n                    <a class="black" href="')
        # SOURCE LINE 178
        __M_writer(escape(thingListingURL))
        __M_writer(u'">')
        __M_writer(escape(numThings))
        __M_writer(u'</a>\n                    </h3>\n                    <div class="centered"><p><a class="green green-hover" href="')
        # SOURCE LINE 180
        __M_writer(escape(thingListingURL))
        __M_writer(u'">listening</a></p></div>\n                </div>\n            </div> <!--/.row-fluid-->\n        </div><!--/.browse-->\n    </div><!--/.section-wrapper-->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


