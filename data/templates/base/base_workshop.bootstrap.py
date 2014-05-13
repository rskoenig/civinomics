# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398544345.2302561
_template_filename = u'/home/maria/civinomics/pylowiki/templates/base/base_workshop.bootstrap'
_template_uri = u'/base/base_workshop.bootstrap'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['headScripts2', 'headScripts', 'extraScripts']


# SOURCE LINE 1

import pylowiki.lib.db.workshop         as workshopLib
import cgi


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 7
    ns = runtime.TemplateNamespace(u'lib_6', context._clean_inheritance_tokens(), templateuri=u'/lib/6_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib_6')] = ns

    # SOURCE LINE 8
    ns = runtime.TemplateNamespace(u'helpers', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_workshop_home.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'helpers')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base/base_indented.bootstrap', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        session = context.get('session', UNDEFINED)
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        helpers = _mako_get_namespace(context, 'helpers')
        next = context.get('next', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 4
        __M_writer(u'\n\n')
        # SOURCE LINE 6
        __M_writer(u'\n')
        # SOURCE LINE 7
        __M_writer(u'\n')
        # SOURCE LINE 8
        __M_writer(u'\n\n<div class="darkened-workshop"></div>\n<div class="spacer"></div>\n<div class="row-fluid one-up">\n      <div class="row-fluid">\n        <div class="span10">\n          \n          <h1 class="workshop-title"> \n            <a href="')
        # SOURCE LINE 17
        __M_writer(escape(lib_6.workshopLink(c.w, embed=True, raw=True)))
        __M_writer(u'" id="workshopTitle" class="workshop-title" ng-init=" workshopTitle=\'')
        __M_writer(escape(c.w['title'].replace("'", "\\'")))
        __M_writer(u'\' " style="color: #fff;" ng-cloak>\n              {{workshopTitle}}\n            </a>\n          </h1>\n          <h4 style="color: #fff">')
        # SOURCE LINE 21
        __M_writer(escape(helpers.displayWorkshopFlag(c.w, 'small', 'workshopFor')))
        __M_writer(u' ')
        __M_writer(escape(lib_6.showTags(c.w)))
        __M_writer(u'</h4>\n        </div>\n        <div class="span2">\n')
        # SOURCE LINE 24
        if 'user' in session:
            # SOURCE LINE 25
            __M_writer(u'            <div class="span12">\n              ')
            # SOURCE LINE 26
            __M_writer(escape(helpers.watchButton(c.w)))
            __M_writer(u'\n            </div>\n')
            pass
        # SOURCE LINE 29
        __M_writer(u'          <div class="span12" style="margin-top:10px; margin-left: 0px">\n            <span class = "share-icons contrast pull-right">\n              ')
        # SOURCE LINE 31
        __M_writer(escape(lib_6.facebookDialogShare2(shareOnWall=True, sendMessage=True)))
        __M_writer(u'\n              ')
        # SOURCE LINE 32
        __M_writer(escape(lib_6.emailShare(c.requestUrl, c.w['urlCode'])))
        __M_writer(u'\n')
        # SOURCE LINE 33
        if c.w['public_private'] == 'public':
            # SOURCE LINE 34
            __M_writer(u'                  <a href="/workshop/')
            __M_writer(escape(c.w['urlCode']))
            __M_writer(u'/')
            __M_writer(escape(c.w['url']))
            __M_writer(u'/rss" target="_blank"><i class="icon-rss icon-2x"></i></a>\n')
            pass
        # SOURCE LINE 36
        __M_writer(u'            </span>\n          </div>\n        </div>  \n      </div> <!-- /.row-fluid -->\n      <div class="row-fluid">\n            ')
        # SOURCE LINE 41

        if c.listingType != '':
          listingType = c.listingType
        else:
          listingType = None
        
        linkHref = lib_6.workshopLink(c.w, embed = True, raw = True)
        infoHref = linkHref + '/information'
        forumHref = linkHref + '/discussion'
        activityHref= linkHref + '/activity'
        publicStatsHref= linkHref + '/publicStats'
        adminHref= linkHref + '/preferences'
        
            
        summaryActive = infoActive = activityActive = forumActive = publicStatsActive = adminActive = ''
        
        if c.listingType == 'resources' or listingType == 'resource':
          infoActive = 'active'
        elif c.listingType == 'discussion':
          forumActive = 'active'
        elif c.listingType == 'ideas' or listingType == 'idea':
          summaryActive = 'active'
        elif c.listingType == 'activity':
          activityActive = 'active'
        elif c.listingType == 'publicStats':
          publicStatsActive = 'active'
        elif c.adminPanel == True:
          adminActive = 'active'
                    
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['publicStatsActive','forumActive','listingType','adminHref','adminActive','activityActive','activityHref','forumHref','linkHref','infoActive','infoHref','publicStatsHref','summaryActive'] if __M_key in __M_locals_builtin_stored]))
        # SOURCE LINE 69
        __M_writer(u'\n\n            <ul class="nav nav-tabs workshop-tabs">\n              <li class="')
        # SOURCE LINE 72
        __M_writer(escape(summaryActive))
        __M_writer(u'">\n                <a href="')
        # SOURCE LINE 73
        __M_writer(linkHref )
        __M_writer(u'">Summary</a>\n              </li>\n              <li class="')
        # SOURCE LINE 75
        __M_writer(escape(infoActive))
        __M_writer(u'"><a href="')
        __M_writer(infoHref )
        __M_writer(u'">Info</a></li>\n              <li class="')
        # SOURCE LINE 76
        __M_writer(escape(forumActive))
        __M_writer(u'"><a href="')
        __M_writer(forumHref )
        __M_writer(u'">Forum</a></li>\n              <li class="')
        # SOURCE LINE 77
        __M_writer(escape(activityActive))
        __M_writer(u'"><a href="')
        __M_writer(activityHref )
        __M_writer(u'">Activity</a></li>\n              <li class="')
        # SOURCE LINE 78
        __M_writer(escape(publicStatsActive))
        __M_writer(u'"><a href="')
        __M_writer(publicStatsHref )
        __M_writer(u'">Stats</a></li>\n')
        # SOURCE LINE 79
        if c.privs['admin'] or c.privs['facilitator']: 
            # SOURCE LINE 80
            __M_writer(u'                <li class="pull-right ')
            __M_writer(escape(adminActive))
            __M_writer(u'" style="margin-right: 10px;"><a href="')
            __M_writer(adminHref )
            __M_writer(u'">Admin</a></li>\n')
            pass
        # SOURCE LINE 82
        __M_writer(u'            </ul>\n            \n         </div>\n      <div class="span12 well workshop-panel" style="margin-left: 0px;">\n      ')
        # SOURCE LINE 86
        __M_writer(escape(next.body()))
        __M_writer(u'\n   </div><!-- /.span12.well -->\n</div><!--/.row-->\n')
        # SOURCE LINE 89
        if c.thing:
            # SOURCE LINE 90
            __M_writer(u'  ')
            __M_writer(escape(lib_6.emailShareModal(c.objectUrl, c.thing['urlCode'])))
            __M_writer(u'\n')
            pass
        # SOURCE LINE 92
        __M_writer(escape(lib_6.emailShareModal(c.requestUrl, c.w['urlCode'])))
        __M_writer(u'\n')
        # SOURCE LINE 93
        __M_writer(escape(helpers.whoListeningModals()))
        __M_writer(u'\n\n')
        # SOURCE LINE 112
        __M_writer(u'\n\n')
        # SOURCE LINE 136
        __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headScripts2(context):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 138
        __M_writer(u'\n')
        # SOURCE LINE 140
        __M_writer(u'    <script src="')
        __M_writer(escape(lib_6.fingerprintFile('/js/ng/goals.js')))
        __M_writer(u'"></script>\n    <script src="')
        # SOURCE LINE 141
        __M_writer(escape(lib_6.fingerprintFile('/js/ng/share.js')))
        __M_writer(u'"></script>\n    <script src="')
        # SOURCE LINE 142
        __M_writer(escape(lib_6.fingerprintFile('/js/ng/resource.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script src="')
        # SOURCE LINE 143
        __M_writer(escape(lib_6.fingerprintFile('/js/ng/edit_item.js')))
        __M_writer(u'" type="text/javascript"></script>\n    \n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headScripts(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 114
        __M_writer(u'\n')
        # SOURCE LINE 115
        if c.facebookShare:
            # SOURCE LINE 116
            if c.facebookShare.facebookAppId:
                # SOURCE LINE 117
                if c.facebookShare.facebookAppId:
                    # SOURCE LINE 118
                    __M_writer(u'                <meta property="fb:app_id" content="')
                    __M_writer(escape(c.facebookShare.facebookAppId))
                    __M_writer(u'" />\n')
                    pass
                # SOURCE LINE 120
                if c.facebookShare.title:
                    # SOURCE LINE 121
                    __M_writer(u'                <meta property="og:title" content="')
                    __M_writer(escape(c.facebookShare.title))
                    __M_writer(u'" />\n')
                    pass
                # SOURCE LINE 123
                __M_writer(u'            <meta property="og:site_name" content="Civinomics"/>\n            <meta property="og:locale" content="en_US" /> \n')
                # SOURCE LINE 125
                if c.facebookShare.url:
                    # SOURCE LINE 126
                    __M_writer(u'                <meta property="og:url" content="')
                    __M_writer(escape(c.facebookShare.url))
                    __M_writer(u'" />\n')
                    pass
                # SOURCE LINE 128
                if c.facebookShare.description:
                    # SOURCE LINE 129
                    __M_writer(u'                <meta property="og:description" content="')
                    __M_writer(escape(c.facebookShare.description))
                    __M_writer(u'" />\n')
                    pass
                # SOURCE LINE 131
                if c.facebookShare.image:
                    # SOURCE LINE 132
                    __M_writer(u'                <meta property="og:image" content="')
                    __M_writer(escape(c.facebookShare.image))
                    __M_writer(u'"/>\n')
                    pass
                pass
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraScripts(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 95
        __M_writer(u'\n   <script type="text/javascript" src="/js/vendor/jquery.backstretch.min.js"></script>\n   ')
        # SOURCE LINE 97

        if c.mainImage['pictureHash'] == 'supDawg':
           backgroundImage = '"/images/slide/slideshow/supDawg.slideshow"'
        elif 'format' in c.mainImage.keys():
           backgroundImage = '"/images/mainImage/%s/orig/%s.%s"' %(c.mainImage['directoryNum'], c.mainImage['pictureHash'], c.mainImage['format'])
        else:
           backgroundImage = '"/images/mainImage/%s/orig/%s.jpg"' %(c.mainImage['directoryNum'], c.mainImage['pictureHash'])
           
        
        # SOURCE LINE 104
        __M_writer(u'\n   <script>$.backstretch(')
        # SOURCE LINE 105
        __M_writer(backgroundImage )
        __M_writer(u', {centeredX: true})</script>\n   <script src="')
        # SOURCE LINE 106
        __M_writer(escape(lib_6.fingerprintFile('/js/follow.js')))
        __M_writer(u'" type="text/javascript"></script>\n   <script type="text/javascript">\n      $(".followButton").tooltip();\n      $(".preferencesLink").tooltip();\n      $(".publishButton").tooltip();\n   </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


