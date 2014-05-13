# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398544345.08371
_template_filename = u'/home/maria/civinomics/pylowiki/templates/lib/derived/6_workshop_home.mako'
_template_uri = u'/lib/derived/6_workshop_home.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['workshopNavButton', 'showActivity', 'configButton', 'showGoals', 'workshopNav', 'whoListening', 'slideshow', 'previewButton', 'whoListeningModals', 'viewButton', 'displayWorkshopFlag', 'imagePreviewer', 'showInfo', 'showScope', 'showFacilitators', 'watchButton', '_slide', '_slideListing']


# SOURCE LINE 1

import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.slideshow as slideshowLib
from pylowiki.lib.db.user import getUserByID
import pylowiki.lib.db.activity as activityLib
import pylowiki.lib.db.facilitator   as facilitatorLib
import pylowiki.lib.utils   as utils
import misaka as m

import logging
log = logging.getLogger(__name__)


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 14
    ns = runtime.TemplateNamespace(u'lib_6', context._clean_inheritance_tokens(), templateuri=u'/lib/6_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib_6')] = ns

def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 12
        __M_writer(u'\n\n')
        # SOURCE LINE 14
        __M_writer(u'\n\n')
        # SOURCE LINE 64
        __M_writer(u'\n\n')
        # SOURCE LINE 103
        __M_writer(u'\n\n')
        # SOURCE LINE 109
        __M_writer(u'\n\n')
        # SOURCE LINE 142
        __M_writer(u'\n\n')
        # SOURCE LINE 156
        __M_writer(u'\n\n')
        # SOURCE LINE 161
        __M_writer(u'\n\n')
        # SOURCE LINE 165
        __M_writer(u'\n\n')
        # SOURCE LINE 169
        __M_writer(u'\n\n')
        # SOURCE LINE 196
        __M_writer(u'\n\n')
        # SOURCE LINE 252
        __M_writer(u'\n\n')
        # SOURCE LINE 289
        __M_writer(u'\n\n\n')
        # SOURCE LINE 322
        __M_writer(u'\n\n')
        # SOURCE LINE 370
        __M_writer(u'\n\n')
        # SOURCE LINE 406
        __M_writer(u'\n\n')
        # SOURCE LINE 418
        __M_writer(u'\n\n')
        # SOURCE LINE 436
        __M_writer(u'\n\n')
        # SOURCE LINE 461
        __M_writer(u'\n\n')
        # SOURCE LINE 489
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_workshopNavButton(context,workshop,count,objType,active=False):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 171
        __M_writer(u'\n    ')
        # SOURCE LINE 172

        imageMap = {'discussion':'/images/glyphicons_pro/glyphicons/png/glyphicons_244_conversation.png',
                    'idea':'/images/glyphicons_pro/glyphicons/png/glyphicons_064_lightbulb.png',
                    'resource':'/images/glyphicons_pro/glyphicons/png/glyphicons_050_link.png',
                    'home':'/images/glyphicons_pro/glyphicons/png/glyphicons_020_home.png',
                    'information':'/images/glyphicons_pro/glyphicons/png/glyphicons_318_more_items.png',
                    'activity':'/images/glyphicons_pro/glyphicons/png/glyphicons_057_history.png'}
        titleMap = {'discussion':' Forum',
                    'idea':' Vote',
                    'resource':' Links',
                    'home':' Home',
                    'information':' Information',
                    'activity':'Activity'}
        linkHref = lib_6.workshopLink(workshop, embed = True, raw = True)
        if objType != 'home':
            linkHref += '/' + objType
        linkClass = 'btn workshopNav'
        if active:
            linkClass += ' selected-nav'
        linkID = objType + 'Button'
            
        
        # SOURCE LINE 192
        __M_writer(u'\n    <a class="')
        # SOURCE LINE 193
        __M_writer(escape(linkClass))
        __M_writer(u'" id="')
        __M_writer(escape(linkID))
        __M_writer(u'" href = "')
        __M_writer(linkHref )
        __M_writer(u'"> <img class="workshop-nav-icon" src="')
        __M_writer(imageMap[objType] )
        __M_writer(u'"> ')
        __M_writer(escape(titleMap[objType]))
        __M_writer(u'\n    (')
        # SOURCE LINE 194
        __M_writer(escape(count))
        __M_writer(u')\n    </a>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showActivity(context,activity):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 111
        __M_writer(u'\n    ')
        # SOURCE LINE 112

        numItems = 5
        shownItems = 0
            
        
        # SOURCE LINE 115
        __M_writer(u'\n    \n')
        # SOURCE LINE 117
        for item in activity:
            # SOURCE LINE 118
            __M_writer(u'      <div class="media"  id="workshopActivity">\n        ')
            # SOURCE LINE 119

            if c.demo:
                author = getUserByID(item.owner)
                if not c.privs['admin']:
                    if 'user' in session:
                        if ((author['accessLevel'] != '300' and not facilitatorLib.isFacilitator(author, c.w)) and author.id != c.authuser.id):
                            continue
                    else:
                        if author['accessLevel'] != '300' and not facilitatorLib.isFacilitator(author, c.w):
                            continue
            if shownItems >= numItems:
                break
                    
            
            # SOURCE LINE 131
            __M_writer(u'\n        <div class="pull-left">\n          ')
            # SOURCE LINE 133
            __M_writer(escape(lib_6.userImage(getUserByID(item.owner), className="avatar small-avatar inline")))
            __M_writer(u'\n        </div>\n        <div class="media-body">\n          ')
            # SOURCE LINE 136
            __M_writer(escape(lib_6.userLink(item.owner, className = "green green-hover", maxChars = 25)))
            __M_writer(u'\n          ')
            # SOURCE LINE 137
            __M_writer(escape(lib_6.showItemInActivity(item, c.w, expandable = True)))
            __M_writer(u'\n        </div>\n      </div>\n')
            pass
        # SOURCE LINE 141
        __M_writer(u'    \n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_configButton(context,w):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 158
        __M_writer(u'\n   ')
        # SOURCE LINE 159
        workshopLink = "%s/preferences" % lib_6.workshopLink(w, embed = True, raw = True) 
        
        __M_writer(u'\n   <a class="btn btn-civ pull-right preferencesLink left-space" href="')
        # SOURCE LINE 160
        __M_writer(workshopLink )
        __M_writer(u'" rel="tooltip" data-placement="bottom" data-original-title="workshop moderation and configuration"><span><i class="icon-wrench icon-white pull-left"></i></span></a>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showGoals(context,goals):
    context.caller_stack._push_frame()
    try:
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 420
        __M_writer(u'\n')
        # SOURCE LINE 421
        if len(goals) == 0:
            # SOURCE LINE 422
            __M_writer(u'        <p>This workshop has no goals!</p>\n')
            # SOURCE LINE 423
        else:
            # SOURCE LINE 424
            __M_writer(u'        <div id="workshopGoals">\n        <ol class="workshop-goals">\n')
            # SOURCE LINE 426
            for goal in goals:
                # SOURCE LINE 427
                if goal['status'] == '100':
                    # SOURCE LINE 428
                    __M_writer(u'                <li class="done-true"><span>')
                    __M_writer(escape(goal['title']))
                    __M_writer(u'</span></li>\n')
                    # SOURCE LINE 429
                else:
                    # SOURCE LINE 430
                    __M_writer(u'                <li><span>')
                    __M_writer(escape(goal['title']))
                    __M_writer(u'</span></li>\n')
                    pass
                pass
            # SOURCE LINE 433
            __M_writer(u'        </ul>\n        </div><!-- workshopGoals -->\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_workshopNav(context,w,listingType):
    context.caller_stack._push_frame()
    try:
        session = context.get('session', UNDEFINED)
        c = context.get('c', UNDEFINED)
        def workshopNavButton(workshop,count,objType,active=False):
            return render_workshopNavButton(context,workshop,count,objType,active)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 198
        __M_writer(u'\n   ')
        # SOURCE LINE 199
 
        activity = activityLib.getActivityForWorkshop(w['urlCode'])
        discussionCount = 0
        ideaCount = 0
        resourceCount = 0
        activityCount = len(activity)
        for item in activity:
           if c.demo:
              author = getUserByID(item.owner)
              if not c.privs['admin']:
                 if 'user' in session:
                    if ((author['accessLevel'] != '300' and not facilitatorLib.isFacilitator(author, c.w)) and author.id != c.authuser.id):
                       continue
                 else:
                    if author['accessLevel'] != '300' and not facilitatorLib.isFacilitator(author, c.w):
                       continue
           
           if item.objType == 'discussion':
              discussionCount += 1
           elif item.objType == 'idea':
              ideaCount += 1
           elif item.objType == 'resource':
              resourceCount += 1
           
        
        # SOURCE LINE 222
        __M_writer(u'\n   <div class="btn-group four-up">\n   ')
        # SOURCE LINE 224
 
        if listingType == 'resources' or listingType == 'resource':
           workshopNavButton(w, ideaCount, 'home')
           workshopNavButton(w, resourceCount, 'information', active = True)
           workshopNavButton(w, discussionCount, 'discussion')
           workshopNavButton(w, activityCount, 'activity')
        elif listingType == 'discussion':
           workshopNavButton(w, ideaCount, 'home')
           workshopNavButton(w, resourceCount, 'information')
           workshopNavButton(w, discussionCount, 'discussion', active = True)
           workshopNavButton(w, activityCount, 'activity')
        elif listingType == 'ideas' or listingType == 'idea':
           workshopNavButton(w, ideaCount, 'home', active = True)
           workshopNavButton(w, resourceCount, 'information')
           workshopNavButton(w, discussionCount, 'discussion')
           workshopNavButton(w, activityCount, 'activity')
        elif listingType == 'activity':
           workshopNavButton(w, ideaCount, 'home')
           workshopNavButton(w, resourceCount, 'information')
           workshopNavButton(w, discussionCount, 'discussion')
           workshopNavButton(w, activityCount, 'activity', active = True)
        else:
           workshopNavButton(w, ideaCount, 'home')
           workshopNavButton(w, resourceCount, 'information')
           workshopNavButton(w, discussionCount, 'discussion')
           workshopNavButton(w, activityCount, 'activity')
           
        
        # SOURCE LINE 250
        __M_writer(u'\n   </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_whoListening(context):
    context.caller_stack._push_frame()
    try:
        session = context.get('session', UNDEFINED)
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 16
        __M_writer(u'\n    <h4 class="section-header smaller section-header-inner">Listeners</h4>\n')
        # SOURCE LINE 18
        if c.activeListeners:
            # SOURCE LINE 19
            __M_writer(u'        <ul class="media-list" id="workshopNotables">\n')
            # SOURCE LINE 20
            for person in c.activeListeners:
                # SOURCE LINE 21
                __M_writer(u'            <li class="media notables-item">\n                ')
                # SOURCE LINE 22
                __M_writer(escape(lib_6.userImage(person, className="avatar med-avatar media-object", linkClass="pull-left")))
                __M_writer(u'\n                <div class="media-body">\n                    ')
                # SOURCE LINE 24
                __M_writer(escape(lib_6.userLink(person, className="listener-name")))
                __M_writer(u'<br />\n                    <small>')
                # SOURCE LINE 25
                __M_writer(escape(lib_6.userGreetingMsg(person)))
                __M_writer(u'</small>\n                </div>\n            </li>\n            \n')
                pass
            # SOURCE LINE 30
            __M_writer(u'        </ul>\n')
            pass
        # SOURCE LINE 32
        if c.pendingListeners:
            # SOURCE LINE 33
            __M_writer(u'        <hr>\n        <div><p><em class="grey">Not yet participating. Invite them to join in.</em></p></div>\n        <ul class="media-list" id="workshopNotables">\n')
            # SOURCE LINE 36
            for person in c.pendingListeners:
                # SOURCE LINE 37
                __M_writer(u'            <li class="media notables-item">\n')
                # SOURCE LINE 38
                if 'user' in session and c.authuser:
                    # SOURCE LINE 39
                    __M_writer(u'                    <div class="pull-left rightbuttonspacing"><a href="#invite')
                    __M_writer(escape(person['urlCode']))
                    __M_writer(u'" class="btn btn-primary btn-mini" data-toggle="modal"><i class="icon-envelope icon-white"></i> Invite</a></div>\n')
                    # SOURCE LINE 40
                else:
                    # SOURCE LINE 41
                    __M_writer(u'                    <div class="pull-left rightbuttonspacing"><a href="#signupLoginModal" data-toggle="modal" class="btn btn-primary btn-mini"><i class="icon-envelope icon-white"></i> Invite</a></div>\n')
                    pass
                # SOURCE LINE 43
                __M_writer(u'                <div class="media-body">\n                    <span class="listener-name">')
                # SOURCE LINE 44
                __M_writer(escape(person['name']))
                __M_writer(u'</span><br />\n                    <small>')
                # SOURCE LINE 45
                __M_writer(escape(person['title']))
                __M_writer(u'</small> \n                </div>\n            </li>\n')
                pass
            # SOURCE LINE 49
            __M_writer(u'        </ul>\n        <hr>\n')
            pass
        # SOURCE LINE 52
        __M_writer(u'      \n')
        # SOURCE LINE 53
        if 'user' in session and c.authuser and not c.privs['provisional']:
            # SOURCE LINE 54
            __M_writer(u'        <em class="grey">Which public officials should participate?</em><br />\n        <form ng-controller="listenerController" ng-init="code=\'')
            # SOURCE LINE 55
            __M_writer(escape(c.w['urlCode']))
            __M_writer(u"'; url='")
            __M_writer(escape(c.w['url']))
            __M_writer(u"'; user='")
            __M_writer(escape(c.authuser['urlCode']))
            __M_writer(u'\'; suggestListenerText=\'\';" id="suggestListenerForm" ng-submit="suggestListener()" class="form-inline suggestListener no-bottom" name="suggestListenerForm">\n          <input class="listenerInput" type="text" ng-model="suggestListenerText" name="suggestListenerText" placeholder="Suggest a Listener"  required>\n          <button type="submit" class="btn btn-success btn-small">Submit</button>\n          <div class="alert top-space" style="margin-bottom: 0;" ng-show="suggestListenerShow">\n            <button data-dismiss="alert" class="close">x</button>\n            {{suggestListenerResponse}}\n          </div>\n        </form>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_slideshow(context,w,*args):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        def _slideListing(showSlide,slideNum,*args):
            return render__slideListing(context,showSlide,slideNum,*args)
        __M_writer = context.writer()
        # SOURCE LINE 292
        __M_writer(u'\n    ')
        # SOURCE LINE 293
 
        slides = slideshowLib.getSlidesInOrder(slideshowLib.getSlideshow(w)) 
        slideNum = 0
        spanX = ""
        if 'hero' in args:
          spanX = "span8"
            
        
        # SOURCE LINE 299
        __M_writer(u'\n    <div class="')
        # SOURCE LINE 300
        __M_writer(escape(spanX))
        __M_writer(u'">\n        <ul class="gallery thumbnails no-bottom" data-clearing>\n        ')
        # SOURCE LINE 302

        for slide in slides:
          if slide['deleted'] != '1':
            if 'hero' in args:
              _slideListing(slide, slideNum, 'hero')
            else:
              _slideListing(slide, slideNum)
            slideNum += 1
                
        
        # SOURCE LINE 310
        __M_writer(u'\n        </ul>\n    </div>\n')
        # SOURCE LINE 313
        if 'hero' in args:
            # SOURCE LINE 314
            __M_writer(u'        ')
            infoHref = lib_6.workshopLink(c.w, embed = True, raw = True) + '/information' 
            
            __M_writer(u'\n        <div class="span4">\n          <p class="description" style="color: #FFF; padding-top: 15px;">\n            ')
            # SOURCE LINE 317
            __M_writer(escape(lib_6.ellipsisIZE(c.w['description'], 285)))
            __M_writer(u'\n            <a href="')
            # SOURCE LINE 318
            __M_writer(escape(infoHref))
            __M_writer(u'">read more</a>\n          </p>\n        </div>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_previewButton(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 163
        __M_writer(u'\n  <a class="btn btn-civ pull-right" href="')
        # SOURCE LINE 164
        __M_writer(escape(lib_6.workshopLink(c.w, embed=True, raw=True)))
        __M_writer(u'"><span><i class="icon-eye-open icon-white pull-left"></i> Preview </span></a>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_whoListeningModals(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        str = context.get('str', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 66
        __M_writer(u'\n')
        # SOURCE LINE 67
        if c.pendingListeners:
            # SOURCE LINE 68
            for person in c.pendingListeners:
                # SOURCE LINE 69
                if 'user' in session and c.authuser:
                    # SOURCE LINE 70
                    __M_writer(u'        ')

                    memberMessage = "Please join me and participate in this Civinomics workshop. There are good ideas and informed discussions that I think you should be a part of."
                    
                    if person['invites'] != '':
                        inviteList = person['invites'].split(',')
                        numInvites = str(len(inviteList))
                    else:
                        numInvites = '0'
                        
                            
                    
                    # SOURCE LINE 79
                    __M_writer(u'\n        <div id="invite')
                    # SOURCE LINE 80
                    __M_writer(escape(person['urlCode']))
                    __M_writer(u'" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="invite')
                    __M_writer(escape(person['urlCode']))
                    __M_writer(u'Label" aria-hidden="true">\n            <div class="modal-header">\n                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">\xd7</button>\n                <h3 id="invite')
                    # SOURCE LINE 83
                    __M_writer(escape(person['urlCode']))
                    __M_writer(u'Label">Invite ')
                    __M_writer(escape(person['name']))
                    __M_writer(u' to Listen</h3>\n            </div><!-- modal-header -->\n            <div class="modal-body"> \n              <div class="row-fluid">\n                <form ng-controller="listenerController" ng-init="code=\'')
                    # SOURCE LINE 87
                    __M_writer(escape(c.w['urlCode']))
                    __M_writer(u"'; url='")
                    __M_writer(escape(c.w['url']))
                    __M_writer(u"'; user='")
                    __M_writer(escape(c.authuser['urlCode']))
                    __M_writer(u"'; listener='")
                    __M_writer(escape(person['urlCode']))
                    __M_writer(u"'; memberMessage='")
                    __M_writer(escape(memberMessage))
                    __M_writer(u'\'" id="inviteListener" ng-submit="emailListener()" class="form-inline" name="inviteListener">\n                <div class="alert" ng-show="emailListenerShow">{{emailListenerResponse}}</div>\n                Add a personalized message to the listener invitation:<br />\n                <textarea rows="6" class="field span12" ng-model="memberMessage" name="memberMessage">{{memberMessage}}</textarea>\n                <br />\n                <div class="spacer"></div>\n                <button class="btn btn-danger" data-dismiss="modal" aria-hidden="true">Close</button>\n                <button type="submit" class="btn btn-success">Send Invitation</button>\n                <br />\n                </form>\n              </div><!-- row-fluid -->\n            </div><!-- modal-footer -->\n        </div><!-- modal -->\n')
                    pass
                pass
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_viewButton(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 167
        __M_writer(u'\n  <a class="btn btn-civ pull-right" href="')
        # SOURCE LINE 168
        __M_writer(escape(lib_6.workshopLink(c.w, embed=True, raw=True)))
        __M_writer(u'"><span><i class="icon-eye-open icon-white pull-left"></i> View </span></a>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_displayWorkshopFlag(context,w,*args):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 463
        __M_writer(u'\n    ')
        # SOURCE LINE 464

        workshopFlag = '/images/flags/generalFlag.gif'
        href = '#'
        if w['public_private'] == 'public':
            scope = utils.getPublicScope(w)
            href = scope['href']
            workshopFlag = scope['flag']
            level = scope['level']
            name = scope['name']
        else:
            workshopFlag = '/images/flags/generalGroup.gif'
        flagSize = 'med-flag'
        if 'small' in args:
          flagSize = 'small-flag'
        
            
        
        # SOURCE LINE 479
        __M_writer(u'\n    <a href="')
        # SOURCE LINE 480
        __M_writer(escape(href))
        __M_writer(u'"><img class="thumbnail flag ')
        __M_writer(escape(flagSize))
        __M_writer(u'" src="')
        __M_writer(escape(workshopFlag))
        __M_writer(u'"></a>\n')
        # SOURCE LINE 481
        if 'workshopFor' in args and w['public_private'] == 'public':
            # SOURCE LINE 482
            __M_writer(u'        Workshop for\n')
            # SOURCE LINE 483
            if name == 'Earth':
                # SOURCE LINE 484
                __M_writer(u'          <a href="')
                __M_writer(escape(href))
                __M_writer(u'">')
                __M_writer(escape(name))
                __M_writer(u'</a>\n')
                # SOURCE LINE 485
            else:
                # SOURCE LINE 486
                __M_writer(u'          the <a href="')
                __M_writer(escape(href))
                __M_writer(u'">')
                __M_writer(escape(level))
                __M_writer(u' of ')
                __M_writer(escape(name))
                __M_writer(u'</a>\n')
                pass
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_imagePreviewer(context,w):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 254
        __M_writer(u'\n  <!-- using the data-clearing twice on a page leads to slide skipping this function allows a preview but will not launch slideshow -->\n  ')
        # SOURCE LINE 256
 
        images = slideshowLib.getSlidesInOrder(slideshowLib.getSlideshow(w))
        count = 0
          
        
        # SOURCE LINE 259
        __M_writer(u'\n  <ul class="gallery thumbnails no-bottom">\n')
        # SOURCE LINE 261
        for image in images:
            # SOURCE LINE 262
            __M_writer(u'      ')
 
            imageFormat = 'jpg'
            if 'format' in image.keys():
              imageFormat = image['format']
            
            spanX = 'noShow'
            if count <= 5:
              spanX = 'span4'
                  
            
            # SOURCE LINE 270
            __M_writer(u'\n')
            # SOURCE LINE 271
            if image['deleted'] != '1':
                # SOURCE LINE 272
                __M_writer(u'        <li class="')
                __M_writer(escape(spanX))
                __M_writer(u' slideListing">\n')
                # SOURCE LINE 273
                if image['pictureHash'] == 'supDawg':
                    # SOURCE LINE 274
                    __M_writer(u'             <a href="#moreimages" data-toggle="tab" ng-click="switchImages()">\n                <img src="/images/slide/slideshow/')
                    # SOURCE LINE 275
                    __M_writer(escape(image['pictureHash']))
                    __M_writer(u'.slideshow"/>\n             </a>\n')
                    # SOURCE LINE 277
                else:
                    # SOURCE LINE 278
                    __M_writer(u'            <a href="#moreimages" data-toggle="tab" ng-click="switchImages()">\n              <!-- div with background-image needed to appropirately size and scale image in workshop_home template -->\n              <div class="slide-preview" style="background-image:url(\'/images/slide/')
                    # SOURCE LINE 280
                    __M_writer(escape(image['directoryNum']))
                    __M_writer(u'/slideshow/')
                    __M_writer(escape(image['pictureHash']))
                    __M_writer(u'.')
                    __M_writer(escape(imageFormat))
                    __M_writer(u'\');"/>\n              </div>\n            </a>\n')
                    pass
                # SOURCE LINE 284
                __M_writer(u'        </li>\n')
                pass
            # SOURCE LINE 286
            __M_writer(u'      ')
            count += 1 
            
            __M_writer(u'\n')
            pass
        # SOURCE LINE 288
        __M_writer(u'  </ul>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showInfo(context,workshop):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 408
        __M_writer(u'\n    <div>\n    <p class="description" >\n      ')
        # SOURCE LINE 411
        __M_writer(escape(c.w['description']))
        __M_writer(u'\n    </p>\n')
        # SOURCE LINE 413
        if c.information and 'data' in c.information: 
            # SOURCE LINE 414
            __M_writer(u'        <hr class="list-header">\n        ')
            # SOURCE LINE 415
            __M_writer(m.html(c.information['data'], render_flags=m.HTML_SKIP_HTML) )
            __M_writer(u'\n')
            pass
        # SOURCE LINE 417
        __M_writer(u'    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showScope(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 438
        __M_writer(u'\n    ')
        # SOURCE LINE 439

        if c.w['public_private'] == 'public':
            scopeName = c.scope['level']
            scopeString = 'Scope: '
            if scopeName == 'earth':
                scopeString += 'the entire planet Earth.'
            else:
                # More mapping for the postal code, this time to display Postal Code instead of just Postal.
                # The real fix for this is through use of message catalogs, which we will need to implement
                # when we support multiple languages in the interface, so for right now this kludge is
                # "good enough"
                if scopeName == 'postalCode':
                    scopeNeme = 'Postal Code '
        
                scopeString += "the " + scopeName.title() + " of "
                scopeString += c.scope['name']\
                        .replace('-', ' ')\
                        .title()
        else:
            scopeString = "Scope: This is a private workshop."
            
        
        # SOURCE LINE 459
        __M_writer(u'\n    ')
        # SOURCE LINE 460
        __M_writer(scopeString )
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showFacilitators(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 105
        __M_writer(u'\n')
        # SOURCE LINE 106
        for facilitator in c.facilitators:
            # SOURCE LINE 107
            __M_writer(u'        Facilitator: ')
            __M_writer(escape(lib_6.userLink(facilitator)))
            __M_writer(u'<br />\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_watchButton(context,w,**kwargs):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 144
        __M_writer(u'\n')
        # SOURCE LINE 145
        if 'user' in session:
            # SOURCE LINE 146
            if c.isFollowing or 'following' in kwargs:
                # SOURCE LINE 147
                __M_writer(u'            <button class="btn btn-civ pull-right followButton following" data-URL-list="workshop_')
                __M_writer(escape(w['urlCode']))
                __M_writer(u'_')
                __M_writer(escape(w['url']))
                __M_writer(u'" rel="tooltip" data-placement="bottom" data-original-title="this workshop" id="workshopBookmark"> \n            <span><i class="icon-bookmark btn-height icon-light"></i><strong> Bookmarked </strong></span>\n            </button>\n')
                # SOURCE LINE 150
            else:
                # SOURCE LINE 151
                __M_writer(u'            <button class="btn pull-right followButton" data-URL-list="workshop_')
                __M_writer(escape(w['urlCode']))
                __M_writer(u'_')
                __M_writer(escape(w['url']))
                __M_writer(u'" rel="tooltip" data-placement="bottom" data-original-title="this workshop" id="workshopBookmark"> \n             <span><i class="icon-bookmark med-green"></i><strong> Bookmark </strong></span>\n            </button>\n')
                pass
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render__slide(context,slide,slideNum,numSlides):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 372
        __M_writer(u'\n  <!-- original code -->\n   ')
        # SOURCE LINE 374
 
        if slideNum == 0:
           spanX = "span12"
        else:
           if slideNum <= 3:
              if numSlides == 2:
                 spanX = "span4 offset4 thumbnail-gallery"
              elif numSlides == 3:
                 spanX = "span4 offset1 thumbnail-gallery"
              elif numSlides >= 4:
                 spanX = "span4 thumbnail-gallery"
           else:
              spanX = "noShow"
           
        
        # SOURCE LINE 387
        __M_writer(u'\n      <li class="')
        # SOURCE LINE 388
        __M_writer(escape(spanX))
        __M_writer(u'">\n')
        # SOURCE LINE 389
        if slide['pictureHash'] == 'supDawg':
            # SOURCE LINE 390
            __M_writer(u'         <a href="/images/slide/slideshow/')
            __M_writer(escape(slide['pictureHash']))
            __M_writer(u'.slideshow">\n            <img src="/images/slide/slideshow/')
            # SOURCE LINE 391
            __M_writer(escape(slide['pictureHash']))
            __M_writer(u'.slideshow" data-caption="')
            __M_writer(escape(slide['title']))
            __M_writer(u'"/>\n         </a>\n')
            # SOURCE LINE 393
        elif 'format' in slide.keys():
            # SOURCE LINE 394
            __M_writer(u'         <a href="/images/slide/')
            __M_writer(escape(slide['directoryNum']))
            __M_writer(u'/slideshow/')
            __M_writer(escape(slide['pictureHash']))
            __M_writer(u'.')
            __M_writer(escape(slide['format']))
            __M_writer(u'">\n            <img src="/images/slide/')
            # SOURCE LINE 395
            __M_writer(escape(slide['directoryNum']))
            __M_writer(u'/slideshow/')
            __M_writer(escape(slide['pictureHash']))
            __M_writer(u'.')
            __M_writer(escape(slide['format']))
            __M_writer(u'" data-caption="')
            __M_writer(escape(slide['title']))
            __M_writer(u'"/>\n         </a>\n')
            # SOURCE LINE 397
        else:
            # SOURCE LINE 398
            __M_writer(u'         <a href="/images/slide/')
            __M_writer(escape(slide['directoryNum']))
            __M_writer(u'/slideshow/')
            __M_writer(escape(slide['pictureHash']))
            __M_writer(u'.jpg">\n            <img src="/images/slide/')
            # SOURCE LINE 399
            __M_writer(escape(slide['directoryNum']))
            __M_writer(u'/slideshow/')
            __M_writer(escape(slide['pictureHash']))
            __M_writer(u'.jpg" data-caption="')
            __M_writer(escape(slide['title']))
            __M_writer(u'"/>\n         </a>\n')
            pass
        # SOURCE LINE 402
        if slideNum == 0:
            # SOURCE LINE 403
            __M_writer(u'         <small class="centered">')
            __M_writer(escape(slide['title']))
            __M_writer(u'</small>\n')
            pass
        # SOURCE LINE 405
        __M_writer(u'   </li>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render__slideListing(context,showSlide,slideNum,*args):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 324
        __M_writer(u'\n    ')
        # SOURCE LINE 325

        if slideNum == 0:
            spanX = "span12"
        else:
            spanX = "noShow"
        slideFormat = 'jpg'
        if 'format' in showSlide.keys():
            slideFormat = showSlide['format']
            
        
        # SOURCE LINE 333
        __M_writer(u'\n')
        # SOURCE LINE 334
        if slideNum == 0 and 'hero' in args:
            # SOURCE LINE 335
            __M_writer(u'      <li class="')
            __M_writer(escape(spanX))
            __M_writer(u' no-bottom">\n')
            # SOURCE LINE 336
            if showSlide['pictureHash'] == 'supDawg':
                # SOURCE LINE 337
                __M_writer(u'          <a href="/images/slide/slideshow/')
                __M_writer(escape(showSlide['pictureHash']))
                __M_writer(u'.slideshow">\n          <div class="slide-hero" style="background-image:url(\'/images/slide/slideshow/')
                # SOURCE LINE 338
                __M_writer(escape(showSlide['pictureHash']))
                __M_writer(u'.slideshow\');" data-caption="')
                __M_writer(escape(showSlide['title']))
                __M_writer(u'"/></div>\n          </a>\n')
                # SOURCE LINE 340
            else:
                # SOURCE LINE 341
                __M_writer(u'          <a href="/images/slide/')
                __M_writer(escape(showSlide['directoryNum']))
                __M_writer(u'/slideshow/')
                __M_writer(escape(showSlide['pictureHash']))
                __M_writer(u'.')
                __M_writer(escape(slideFormat))
                __M_writer(u'">\n          <!-- img class is needed by data-clearing to assemble the slideshow carousel-->\n          <img class="noShow"src="/images/slide/')
                # SOURCE LINE 343
                __M_writer(escape(showSlide['directoryNum']))
                __M_writer(u'/slideshow/')
                __M_writer(escape(showSlide['pictureHash']))
                __M_writer(u'.')
                __M_writer(escape(slideFormat))
                __M_writer(u'" data-caption="')
                __M_writer(escape(showSlide['title']))
                __M_writer(u'"/>\n          <!-- div with background-image needed to appropirately size and scale image in workshop_home template -->\n          <div class="slide-hero" style=" background-image:url(\'/images/slide/')
                # SOURCE LINE 345
                __M_writer(escape(showSlide['directoryNum']))
                __M_writer(u'/slideshow/')
                __M_writer(escape(showSlide['pictureHash']))
                __M_writer(u'.')
                __M_writer(escape(slideFormat))
                __M_writer(u'\');" data-caption="')
                __M_writer(escape(showSlide['title']))
                __M_writer(u'"/>\n              <div class="well slide-hero-caption">\n                  <i class="icon-play"></i> Slideshow\n              </div>\n          </div>\n          </a>\n')
                pass
            # SOURCE LINE 352
            __M_writer(u'      </li>\n')
            # SOURCE LINE 353
        else:
            # SOURCE LINE 354
            __M_writer(u'      <li class="span4 slideListing">\n')
            # SOURCE LINE 355
            if showSlide['pictureHash'] == 'supDawg':
                # SOURCE LINE 356
                __M_writer(u'           <a href="/images/slide/slideshow/')
                __M_writer(escape(showSlide['pictureHash']))
                __M_writer(u'.slideshow">\n              <img src="/images/slide/slideshow/')
                # SOURCE LINE 357
                __M_writer(escape(showSlide['pictureHash']))
                __M_writer(u'.slideshow" data-caption="')
                __M_writer(escape(showSlide['title']))
                __M_writer(u'"/>\n           </a>\n')
                # SOURCE LINE 359
            else:
                # SOURCE LINE 360
                __M_writer(u'            <a href="/images/slide/')
                __M_writer(escape(showSlide['directoryNum']))
                __M_writer(u'/slideshow/')
                __M_writer(escape(showSlide['pictureHash']))
                __M_writer(u'.')
                __M_writer(escape(slideFormat))
                __M_writer(u'">\n              <!-- img class is needed by data-clearing to assemble the slideshow carousel-->\n              <img class="noShow" src="/images/slide/')
                # SOURCE LINE 362
                __M_writer(escape(showSlide['directoryNum']))
                __M_writer(u'/slideshow/')
                __M_writer(escape(showSlide['pictureHash']))
                __M_writer(u'.')
                __M_writer(escape(slideFormat))
                __M_writer(u'" data-caption="')
                __M_writer(escape(showSlide['title']))
                __M_writer(u'"/>\n              <!-- div with background-image needed to appropirately size and scale image in workshop_home template -->\n              <div class="slide-preview" style="background-image:url(\'/images/slide/')
                # SOURCE LINE 364
                __M_writer(escape(showSlide['directoryNum']))
                __M_writer(u'/slideshow/')
                __M_writer(escape(showSlide['pictureHash']))
                __M_writer(u'.')
                __M_writer(escape(slideFormat))
                __M_writer(u'\');" data-caption="')
                __M_writer(escape(showSlide['title']))
                __M_writer(u'"/>\n              </div>\n            </a>\n')
                pass
            # SOURCE LINE 368
            __M_writer(u'      </li>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


