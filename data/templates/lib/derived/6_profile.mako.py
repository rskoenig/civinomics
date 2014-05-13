# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398540607.617569
_template_filename = u'/home/maria/civinomics/pylowiki/templates/lib/derived/6_profile.mako'
_template_uri = u'/lib/derived/6_profile.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['showPositions', 'showWorkshop', 'listCreatedThings', 'listInterestedThings', 'showInitiative', 'showDiscussions', 'thingCount', 'showMemberActivity', 'inviteCoFacilitate', 'addTopic', 'showMemberPosts', 'showPosition', 'showDiscussion', 'showActivity', 'profileModerationPanel', 'followButton']


# SOURCE LINE 1

import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.initiative   as initiativeLib
import pylowiki.lib.db.facilitator  as facilitatorLib
import pylowiki.lib.db.listener     as listenerLib
import pylowiki.lib.db.discussion   as discussionLib
import pylowiki.lib.db.follow       as followLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.pmember      as pmemberLib
import pylowiki.lib.db.generic      as genericLib
import pylowiki.lib.utils           as utils
import pylowiki.lib.fuzzyTime       as fuzzyTime
import misaka as misaka

import logging, os
log = logging.getLogger(__name__)


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 19
    ns = runtime.TemplateNamespace(u'lib_6', context._clean_inheritance_tokens(), templateuri=u'/lib/6_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib_6')] = ns

def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 17
        __M_writer(u'\n\n')
        # SOURCE LINE 19
        __M_writer(u'\n\n')
        # SOURCE LINE 34
        __M_writer(u'\n\n')
        # SOURCE LINE 67
        __M_writer(u'\n\n')
        # SOURCE LINE 215
        __M_writer(u'\n\n')
        # SOURCE LINE 268
        __M_writer(u'\n\n')
        # SOURCE LINE 312
        __M_writer(u'\n\n')
        # SOURCE LINE 330
        __M_writer(u'\n\n')
        # SOURCE LINE 530
        __M_writer(u'\n\n')
        # SOURCE LINE 621
        __M_writer(u'\n\n')
        # SOURCE LINE 635
        __M_writer(u'\n\n')
        # SOURCE LINE 683
        __M_writer(u'\n\n')
        # SOURCE LINE 695
        __M_writer(u'\n\n')
        # SOURCE LINE 722
        __M_writer(u'\n\n')
        # SOURCE LINE 733
        __M_writer(u'\n\n')
        # SOURCE LINE 771
        __M_writer(u'\n\n')
        # SOURCE LINE 791
        __M_writer(u'\n\n')
        # SOURCE LINE 832
        __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showPositions(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 724
        __M_writer(u'\n    ')
        # SOURCE LINE 725
        discussions = discussionLib.getPositionsForOrganization(c.user) 
        
        __M_writer(u'\n')
        # SOURCE LINE 726
        for d in discussions:
            # SOURCE LINE 727
            __M_writer(u'        ')
            url = "/profile/" + c.user['urlCode'] + "/" + c.user['url'] + "/position/show/" + d['urlCode'] 
            
            __M_writer(u'\n        <div class="row-fluid">\n            <h3><a href="')
            # SOURCE LINE 729
            __M_writer(escape(url))
            __M_writer(u'" class="listed-item-title">')
            __M_writer(escape(d['title']))
            __M_writer(u'</a></h3>\n            posted ')
            # SOURCE LINE 730
            __M_writer(escape(fuzzyTime.timeSince(d.date)))
            __M_writer(u' ago ')
            __M_writer(escape(str(d['numComments'])))
            __M_writer(u' comments <i class="icon-eye-open"></i> ')
            __M_writer(escape(str(d['views'])))
            __M_writer(u' views</br>\n        </div><!-- row-fluid -->\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showWorkshop(context,workshop,**kwargs):
    context.caller_stack._push_frame()
    try:
        session = context.get('session', UNDEFINED)
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 69
        __M_writer(u'\n    <div class="media profile-workshop">\n        <a class="pull-left" ')
        # SOURCE LINE 71
        __M_writer(escape(lib_6.workshopLink(workshop)))
        __M_writer(u'>\n          <div class="thumbnail tight media-object" style="height: 60px; width: 90px; margin-bottom: 5px; background-image:url(')
        # SOURCE LINE 72
        __M_writer(lib_6.workshopImage(workshop, raw=True) )
        __M_writer(u'); background-size: cover; background-position: center center;"></div>\n        </a>\n        ')
        # SOURCE LINE 74

        if 'imageOnly' in kwargs:
            if kwargs['imageOnly'] == True:
                return
        if 'role' in kwargs:
            role = kwargs['role']
        else:
            role = ''
                
        
        # SOURCE LINE 82
        __M_writer(u'\n        <div class="media-body">\n            <a ')
        # SOURCE LINE 84
        __M_writer(escape(lib_6.workshopLink(workshop)))
        __M_writer(u' class="listed-item-title media-heading lead bookmark-title">')
        __M_writer(escape(workshop['title']))
        __M_writer(u'</a>\n            <span class="label label-inverse pull-right">')
        # SOURCE LINE 85
        __M_writer(escape(role))
        __M_writer(u'</span>\n')
        # SOURCE LINE 86
        if 'user' in session:
            # SOURCE LINE 87
            if c.user.id == c.authuser.id or userLib.isAdmin(c.authuser.id):
                # SOURCE LINE 88
                if role == 'Facilitating':
                    # SOURCE LINE 89
                    __M_writer(u'                        <div style="margin-top: 10px;">\n                            ')
                    # SOURCE LINE 90

                    f = facilitatorLib.getFacilitatorsByUserAndWorkshop(c.user, workshop)[0]
                    itemsChecked = ''
                    flagsChecked = ''
                    digestChecked = ''
                    if 'itemAlerts' in f and f['itemAlerts'] == '1':
                        itemsChecked = 'checked'
                    if 'flagAlerts' in f and f['flagAlerts'] == '1':
                        flagsChecked = 'checked'
                    if 'digest' in f and f['digest'] == '1':
                        digestChecked = 'checked'
                                                
                    
                    # SOURCE LINE 101
                    __M_writer(u'\n                            <div class="row-fluid" ng-controller="facilitatorController">\n                                <div class="span3">Email when:</div>\n                                <div class="span3">\n                                    <form ng-init="code=\'')
                    # SOURCE LINE 105
                    __M_writer(escape(workshop['urlCode']))
                    __M_writer(u"'; url='")
                    __M_writer(escape(workshop['url']))
                    __M_writer(u"'; user='")
                    __M_writer(escape(c.user['urlCode']))
                    __M_writer(u'\'" class="no-bottom form-inline">\n                                        New Items: <input type="checkbox" name="flagAlerts" value="flags" ng-click="emailOnAdded()" ')
                    # SOURCE LINE 106
                    __M_writer(escape(itemsChecked))
                    __M_writer(u'>\n                                        <span ng-show="emailOnAddedShow">{{emailOnAddedResponse}}</span>\n                                    </form>\n                                </div><!-- span3 -->\n                                <div class="span3">\n                                    <form ng-init="code=\'')
                    # SOURCE LINE 111
                    __M_writer(escape(workshop['urlCode']))
                    __M_writer(u"'; url='")
                    __M_writer(escape(workshop['url']))
                    __M_writer(u"'; user='")
                    __M_writer(escape(c.user['urlCode']))
                    __M_writer(u'\'" class="no-bottom form-inline">\n                                        New Flags: <input type="checkbox" name="itemAlerts" value="items" ng-click="emailOnFlagged()" ')
                    # SOURCE LINE 112
                    __M_writer(escape(flagsChecked))
                    __M_writer(u'>\n                                        <span ng-show="emailOnFlaggedShow">{{emailOnFlaggedResponse}}</span>\n                                    </form>\n                                </div><!-- span3 -->\n                                <div class="span3">\n                                    <form ng-init="code=\'')
                    # SOURCE LINE 117
                    __M_writer(escape(workshop['urlCode']))
                    __M_writer(u"'; url='")
                    __M_writer(escape(workshop['url']))
                    __M_writer(u"'; user='")
                    __M_writer(escape(c.user['urlCode']))
                    __M_writer(u'\'" class="no-bottom form-inline">\n                                        Weekly Digest: <input type="checkbox" name="digest" value="items" ng-click="emailDigest()" ')
                    # SOURCE LINE 118
                    __M_writer(escape(digestChecked))
                    __M_writer(u'>\n                                        <span ng-show="emailDigestShow">{{emailDigestResponse}}</span>\n                                    </form>\n                                </div><!-- span3 -->\n                            </div><!-- row-fluid -->\n                        </div><!-- margin-top -->\n')
                    pass
                # SOURCE LINE 125
                if role == 'Listening':
                    # SOURCE LINE 126
                    __M_writer(u'                        <div style="margin-top: 10px;">\n                            ')
                    # SOURCE LINE 127

                    l = listenerLib.getListener(c.user['email'], workshop)
                    itemsChecked = ''
                    digestChecked = ''
                    if 'itemAlerts' in l and l['itemAlerts'] == '1':
                        itemsChecked = 'checked'
                    if 'digest' in l and l['digest'] == '1':
                        digestChecked = 'checked'
                                                
                    
                    # SOURCE LINE 135
                    __M_writer(u'\n                            <div class="row-fluid" ng-controller="listenerController">\n                                <div class="span3">Email when:</div>\n                                <div class="span3">\n                                    <form ng-init="code=\'')
                    # SOURCE LINE 139
                    __M_writer(escape(workshop['urlCode']))
                    __M_writer(u"'; url='")
                    __M_writer(escape(workshop['url']))
                    __M_writer(u"'; user='")
                    __M_writer(escape(c.user['urlCode']))
                    __M_writer(u'\'" class="no-bottom form-inline">\n                                        New Items: <input type="checkbox" name="itemAlerts" value="items" ng-click="emailOnAdded()" ')
                    # SOURCE LINE 140
                    __M_writer(escape(itemsChecked))
                    __M_writer(u'>\n                                        <span ng-show="emailOnAddedShow">{{emailOnAddedResponse}}</span>\n                                    </form>\n                                </div><!-- span3 -->\n                                <div class="span3">\n                                    <form ng-init="code=\'')
                    # SOURCE LINE 145
                    __M_writer(escape(workshop['urlCode']))
                    __M_writer(u"'; url='")
                    __M_writer(escape(workshop['url']))
                    __M_writer(u"'; user='")
                    __M_writer(escape(c.user['urlCode']))
                    __M_writer(u'\'" class="no-bottom form-inline">\n                                        Weekly Digest: <input type="checkbox" name="digest" value="items" ng-click="emailDigest()" ')
                    # SOURCE LINE 146
                    __M_writer(escape(digestChecked))
                    __M_writer(u'>\n                                        <span ng-show="emailDigestShow">{{emailDigestResponse}}</span>\n                                    </form>\n                                </div><!-- span3 -->\n                            </div><!-- row-fluid -->\n                        </div><!-- margin-top -->\n')
                    pass
                # SOURCE LINE 153
                if role == 'Bookmarked': 
                    # SOURCE LINE 154
                    __M_writer(u'                        ')
                    f = followLib.getFollow(c.user, workshop) 
                    
                    __M_writer(u'\n')
                    # SOURCE LINE 155
                    if f:
                        # SOURCE LINE 156
                        __M_writer(u'                            <div style="margin-top: 10px;">\n                                ')
                        # SOURCE LINE 157

                        itemsChecked = ''
                        digestChecked = ''
                        if 'itemAlerts' in f and f['itemAlerts'] == '1':
                            itemsChecked = 'checked'
                        if 'digest' in f and f['digest'] == '1':
                            digestChecked = 'checked'
                                                        
                        
                        # SOURCE LINE 164
                        __M_writer(u'\n                                <div class="row-fluid" ng-controller="followerController">\n                                    <div class="span3">Email when:</div>\n                                    <div class="span3">\n                                        <form ng-init="code=\'')
                        # SOURCE LINE 168
                        __M_writer(escape(workshop['urlCode']))
                        __M_writer(u"'; url='")
                        __M_writer(escape(workshop['url']))
                        __M_writer(u"'; user='")
                        __M_writer(escape(c.user['urlCode']))
                        __M_writer(u'\'" class="no-bottom form-inline">\n                                            New Items: <input type="checkbox" name="itemAlerts" value="items" ng-click="emailOnAdded()" ')
                        # SOURCE LINE 169
                        __M_writer(escape(itemsChecked))
                        __M_writer(u'>\n                                            <span ng-show="emailOnAddedShow">{{emailOnAddedResponse}}</span>\n                                        </form>\n                                    </div><!-- span3 -->\n                                    <div class="span3">\n                                        <form ng-init="code=\'')
                        # SOURCE LINE 174
                        __M_writer(escape(workshop['urlCode']))
                        __M_writer(u"'; url='")
                        __M_writer(escape(workshop['url']))
                        __M_writer(u"'; user='")
                        __M_writer(escape(c.user['urlCode']))
                        __M_writer(u'\'" class="no-bottom form-inline">\n                                            Weekly Digest: <input type="checkbox" name="digest" value="items" ng-click="emailDigest()" ')
                        # SOURCE LINE 175
                        __M_writer(escape(digestChecked))
                        __M_writer(u'>\n                                            <span ng-show="emailDigestShow">{{emailDigestResponse}}</span>\n                                        </form>\n                                    </div><!-- span3 -->\n                                </div><!-- row-fluid -->\n                            </div><!-- margin-top -->\n')
                        pass
                    pass
                # SOURCE LINE 183
                if role == 'Private':
                    # SOURCE LINE 184
                    __M_writer(u'                        <div style="margin-top: 10px;">\n                            ')
                    # SOURCE LINE 185
 
                    p = pmemberLib.getPrivateMember(workshop['urlCode'], c.user['email'])
                    itemsChecked = ''
                    digestChecked = ''
                    if 'itemAlerts' in p and p['itemAlerts'] == '1':
                            itemsChecked = 'checked'
                    if 'digest' in p and p['digest'] == '1':
                            digestChecked = 'checked'
                                                
                    
                    # SOURCE LINE 193
                    __M_writer(u'\n                            <div class="row-fluid" ng-controller="pmemberController">\n                                <div class="span3">Email when:</div>\n                                <div class="span3">\n                                    <form ng-init="code=\'')
                    # SOURCE LINE 197
                    __M_writer(escape(workshop['urlCode']))
                    __M_writer(u"'; url='")
                    __M_writer(escape(workshop['url']))
                    __M_writer(u"'; user='")
                    __M_writer(escape(c.user['urlCode']))
                    __M_writer(u'\'" class="no-bottom form-inline">\n                                        New Items: <input type="checkbox" name="itemAlerts" value="items" ng-click="emailOnAdded()" ')
                    # SOURCE LINE 198
                    __M_writer(escape(itemsChecked))
                    __M_writer(u'>\n                                        <span ng-show="emailOnAddedShow">{{emailOnAddedResponse}}</span>\n                                    </form>\n                                </div><!-- span3 -->\n                                <div class="span3">\n                                    <form ng-init="code=\'')
                    # SOURCE LINE 203
                    __M_writer(escape(workshop['urlCode']))
                    __M_writer(u"'; url='")
                    __M_writer(escape(workshop['url']))
                    __M_writer(u"'; user='")
                    __M_writer(escape(c.user['urlCode']))
                    __M_writer(u'\'" class="no-bottom form-inline">\n                                        Weekly Digest: <input type="checkbox" name="digest" value="items" ng-click="emailDigest()" ')
                    # SOURCE LINE 204
                    __M_writer(escape(digestChecked))
                    __M_writer(u'>\n                                        <span ng-show="emailDigestShow">{{emailDigestResponse}}</span>\n                                    </form>\n                                </div><!-- span3 -->\n                            </div><!-- row-fluid -->\n                        </div><!-- margin-top -->\n')
                    pass
                pass
            pass
        # SOURCE LINE 213
        __M_writer(u'        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_listCreatedThings(context,user,things,title):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        def showWorkshop(workshop,**kwargs):
            return render_showWorkshop(context,workshop,**kwargs)
        def showInitiative(item,**kwargs):
            return render_showInitiative(context,item,**kwargs)
        __M_writer = context.writer()
        # SOURCE LINE 217
        __M_writer(u'\n    <div class="section-wrapper">\n        <div class="browse">\n            <h3 class="centered section-header"> ')
        # SOURCE LINE 220
        __M_writer(escape(title))
        __M_writer(u' </h3>\n            <table class="table table-condensed table-hover user-thing-listing">\n                <tbody>\n                    ')
        # SOURCE LINE 223
        counter = 0 
        
        __M_writer(u'\n')
        # SOURCE LINE 224
        for thing in things:
            # SOURCE LINE 225
            if counter == 0:
                # SOURCE LINE 226
                __M_writer(u'                            <tr> <td class="no-border">\n')
                # SOURCE LINE 227
            else:
                # SOURCE LINE 228
                __M_writer(u'                            <tr> <td>\n')
                pass
            # SOURCE LINE 230
            if 'workshopCode' in thing:
                # SOURCE LINE 231
                __M_writer(u'                            ')

                workshop = workshopLib.getWorkshopByCode(thing['workshopCode'])
                thingLink = lib_6.thingLinkRouter(thing, workshop, raw=True, embed=True)
                workshopLink = lib_6.workshopLink(workshop, embed=True)
                descriptionText = 'No description'
                if 'comment' in thing.keys():
                    if thing['comment'] != '':
                        descriptionText = thing['comment']
                elif 'text' in thing.keys():
                    if thing['text'] != '':
                        descriptionText = thing['text']
                                            
                
                # SOURCE LINE 242
                __M_writer(u'\n                            ')
                # SOURCE LINE 243
                __M_writer(escape(showWorkshop(workshop, imageOnly = True)))
                __M_writer(u'\n                            <a ')
                # SOURCE LINE 244
                __M_writer(thingLink )
                __M_writer(u'> ')
                __M_writer(escape(lib_6.ellipsisIZE(thing['title'], 60)))
                __M_writer(u' </a> in workshop <a ')
                __M_writer(workshopLink )
                __M_writer(u'> ')
                __M_writer(escape(workshop['title']))
                __M_writer(u' </a> on <span class="green">')
                __M_writer(escape(thing.date.strftime('%b %d, %Y')))
                __M_writer(u'</span>\n')
                # SOURCE LINE 245
                if thing.objType == 'idea':
                    # SOURCE LINE 246
                    if thing['adopted'] == '1':
                        # SOURCE LINE 247
                        __M_writer(u'                                    <br/><i class="icon-star"></i> This idea adopted!\n')
                        pass
                    pass
                # SOURCE LINE 250
                __M_writer(u'                            <br />\n                            Description: ')
                # SOURCE LINE 251
                __M_writer(escape(lib_6.ellipsisIZE(descriptionText, 135)))
                __M_writer(u'\n')
                # SOURCE LINE 252
            elif 'initiativeCode' in thing and thing.objType == 'resource':
                # SOURCE LINE 253
                __M_writer(u'                            ')

                initiative = initiativeLib.getInitiative(thing['initiativeCode'])
                initiativeLink = "/initiative/" + initiative['urlCode'] + "/" + initiative['url']
                thingLink = initiativeLink + "/resource/" + thing['urlCode'] + "/" + thing['url']
                                            
                
                # SOURCE LINE 257
                __M_writer(u'\n                            ')
                # SOURCE LINE 258
                __M_writer(escape(showInitiative(initiative, imageOnly = True)))
                __M_writer(u'\n                            <a href="')
                # SOURCE LINE 259
                __M_writer(escape(thingLink))
                __M_writer(u'"> ')
                __M_writer(escape(lib_6.ellipsisIZE(thing['title'], 60)))
                __M_writer(u' </a> in initiative <a href="')
                __M_writer(escape(initiativeLink))
                __M_writer(u'"> ')
                __M_writer(escape(initiative['title']))
                __M_writer(u' </a> on <span class="green">')
                __M_writer(escape(thing.date.strftime('%b %d, %Y')))
                __M_writer(u'</span>\n')
                pass
            # SOURCE LINE 261
            __M_writer(u'                        </td> </tr>\n                        ')
            # SOURCE LINE 262
            counter += 1 
            
            __M_writer(u'\n')
            pass
        # SOURCE LINE 264
        __M_writer(u'                </tbody>\n            </table>\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_listInterestedThings(context,user,things,title):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        def showWorkshop(workshop,**kwargs):
            return render_showWorkshop(context,workshop,**kwargs)
        len = context.get('len', UNDEFINED)
        def showInitiative(item,**kwargs):
            return render_showInitiative(context,item,**kwargs)
        __M_writer = context.writer()
        # SOURCE LINE 270
        __M_writer(u'\n    <div class="section-wrapper">\n        <div class="browse">\n            <h3 class="centered section-header"> ')
        # SOURCE LINE 273
        __M_writer(escape(title))
        __M_writer(u' </h3>\n')
        # SOURCE LINE 274
        if len(things) == 0:
            # SOURCE LINE 275
            __M_writer(u"                There doesn't seem to be anything here!\n")
            # SOURCE LINE 276
        else:
            # SOURCE LINE 277
            if c.listingType == 'watching' or c.listingType == 'listening' or c.listingType == 'facilitating':
                # SOURCE LINE 278
                __M_writer(u'                    <table class="table table-condensed table-hover user-thing-listing">\n                        <tbody>\n                            ')
                # SOURCE LINE 280
                counter = 0 
                
                __M_writer(u'\n')
                # SOURCE LINE 281
                for thing in things:
                    # SOURCE LINE 282
                    if counter == 0:
                        # SOURCE LINE 283
                        __M_writer(u'                                    <tr> <td class="no-border">\n')
                        # SOURCE LINE 284
                    else:
                        # SOURCE LINE 285
                        __M_writer(u'                                    <tr> <td>\n')
                        pass
                    # SOURCE LINE 287
                    if thing.objType == 'workshop':
                        # SOURCE LINE 288
                        __M_writer(u'                                    ')
                        __M_writer(escape(showWorkshop(thing, imageOnly = True)))
                        __M_writer(u'\n                                    <span class="label label-inverse">Workshop</span> <a ')
                        # SOURCE LINE 289
                        __M_writer(lib_6.workshopLink(thing, embed=True) )
                        __M_writer(u'> ')
                        __M_writer(escape(lib_6.ellipsisIZE(thing['title'], 60)))
                        __M_writer(u' </a>\n                                    <br />\n                                    Description: ')
                        # SOURCE LINE 291
                        __M_writer(escape(lib_6.ellipsisIZE(thing['description'], 135)))
                        __M_writer(u'\n')
                        # SOURCE LINE 292
                    elif thing.objType == 'initiative':
                        # SOURCE LINE 293
                        __M_writer(u'                                    ')
                        __M_writer(escape(showInitiative(thing)))
                        __M_writer(u'\n')
                        pass
                    # SOURCE LINE 295
                    __M_writer(u'\n')
                    pass
                # SOURCE LINE 297
                __M_writer(u'                        </tbody>\n                    </table>\n')
                # SOURCE LINE 299
            else:
                # SOURCE LINE 300
                __M_writer(u'                    ')
                objType = things[0].objType 
                
                __M_writer(u'\n                    <ul class="thumbnails">\n')
                # SOURCE LINE 302
                for thing in things:
                    # SOURCE LINE 303
                    __M_writer(u'                            <li class="follow">\n                                ')
                    # SOURCE LINE 304
                    __M_writer(escape(lib_6.userImage(thing, className="avatar hoverTip", rel="tooltip", placement="bottom")))
                    __M_writer(u'\n                            </li>\n')
                    pass
                # SOURCE LINE 307
                __M_writer(u'                    </ul>\n')
                pass
            pass
        # SOURCE LINE 310
        __M_writer(u'        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showInitiative(context,item,**kwargs):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 36
        __M_writer(u'\n    <div class="media profile-workshop">\n        <a class="pull-left" href="/initiative/')
        # SOURCE LINE 38
        __M_writer(escape(item['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(item['url']))
        __M_writer(u'/show">\n')
        # SOURCE LINE 39
        if 'directoryNum_photos' in item and 'pictureHash_photos' in item:
            # SOURCE LINE 40
            __M_writer(u'            ')
            thumbnail_url = "/images/photos/%s/thumbnail/%s.png"%(item['directoryNum_photos'], item['pictureHash_photos']) 
            
            __M_writer(u'\n')
            # SOURCE LINE 41
        else:
            # SOURCE LINE 42
            __M_writer(u'            ')
            thumbnail_url = "/images/slide/thumbnail/supDawg.thumbnail" 
            
            __M_writer(u'\n')
            pass
        # SOURCE LINE 44
        __M_writer(u'        <div class="thumbnail tight media-object" style="height: 60px; width: 90px; margin-bottom: 5px; background-image:url(')
        __M_writer(escape(thumbnail_url))
        __M_writer(u'); background-size: cover; background-position: center center;"></div>\n        </a>\n        ')
        # SOURCE LINE 46

        if 'imageOnly' in kwargs:
            if kwargs['imageOnly'] == True:
                return
                
        
        # SOURCE LINE 50
        __M_writer(u'\n        <div class="media-body">\n            <span class="label label-inverse">Initiative</span> <a href="/initiative/')
        # SOURCE LINE 52
        __M_writer(escape(item['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(item['url']))
        __M_writer(u'/show" class="listed-item-title media-heading lead bookmark-title">')
        __M_writer(escape(item['title']))
        __M_writer(u'</a>\n')
        # SOURCE LINE 53
        if 'user' in session:
            # SOURCE LINE 54
            if c.user.id == c.authuser.id or userLib.isAdmin(c.authuser.id):
                # SOURCE LINE 55
                __M_writer(u'                    <a href="/initiative/')
                __M_writer(escape(item['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(item['url']))
                __M_writer(u'/edit">Edit</a> &nbsp;\n')
                # SOURCE LINE 56
                if item['public'] == '0':
                    # SOURCE LINE 57
                    __M_writer(u'                        Not yet public\n')
                    # SOURCE LINE 58
                else:
                    # SOURCE LINE 59
                    __M_writer(u'                        Public\n')
                    pass
                pass
            pass
        # SOURCE LINE 63
        __M_writer(u'            <br />\n            Description: ')
        # SOURCE LINE 64
        __M_writer(escape(lib_6.ellipsisIZE(item['description'], 135)))
        __M_writer(u'\n        </div><!-- media-body -->\n    </div><!-- media -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showDiscussions(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 685
        __M_writer(u'\n    ')
        # SOURCE LINE 686
        discussions = discussionLib.getDiscussionsForOrganization(c.user) 
        
        __M_writer(u'\n')
        # SOURCE LINE 687
        for d in discussions:
            # SOURCE LINE 688
            __M_writer(u'        ')
            url = "/profile/" + c.user['urlCode'] + "/" + c.user['url'] + "/discussion/show/" + d['urlCode'] 
            
            __M_writer(u'\n        <div class="row-fluid">\n            <h3><a href="')
            # SOURCE LINE 690
            __M_writer(escape(url))
            __M_writer(u'" class="listed-item-title">')
            __M_writer(escape(d['title']))
            __M_writer(u'</a></h3>\n            ')
            # SOURCE LINE 691
            __M_writer(escape(lib_6.userLink(d.owner)))
            __M_writer(u' from ')
            __M_writer(escape(lib_6.userGeoLink(d.owner)))
            __M_writer(escape(lib_6.userImage(d.owner, className="avatar med-avatar")))
            __M_writer(u'</br>\n            posted ')
            # SOURCE LINE 692
            __M_writer(escape(fuzzyTime.timeSince(d.date)))
            __M_writer(u' ago ')
            __M_writer(escape(str(d['numComments'])))
            __M_writer(u' comments <i class="icon-eye-open"></i> ')
            __M_writer(escape(str(d['views'])))
            __M_writer(u' views</br>\n        </div><!-- row-fluid -->\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_thingCount(context,user,things,title):
    context.caller_stack._push_frame()
    try:
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 21
        __M_writer(u'\n    ')
        # SOURCE LINE 22
 
        thisTitle = title
        if title == 'conversations':
            thisTitle = 'discussions'
        elif title == 'bookmarks':
            thisTitle = 'watching'
        thingListingURL = "/profile/%s/%s/%s" %(user['urlCode'], user['url'], thisTitle)
            
        
        # SOURCE LINE 29
        __M_writer(u'\n    <h3 class="profile-count centered">\n        <a class="black" href="')
        # SOURCE LINE 31
        __M_writer(escape(thingListingURL))
        __M_writer(u'">')
        __M_writer(escape(len(things)))
        __M_writer(u'</a>\n    </h3>\n    <div class="centered"><p><a class="green green-hover" href="')
        # SOURCE LINE 33
        __M_writer(escape(thingListingURL))
        __M_writer(u'">')
        __M_writer(escape(title))
        __M_writer(u'</a></p></div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showMemberActivity(context,activity):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 532
        __M_writer(u'\n    ')
        # SOURCE LINE 533

        actionMapping = {   'resource': 'added the resource',
                            'discussion': 'started the conversation',
                            'idea': 'posed the idea',
                            'photo': 'added the picture',
                            'comment': 'commented on a'}
        objTypeMapping = {  'resource':'resource',
                            'discussion':'conversation',
                            'idea':'idea',
                            'photo':'photo',
                            'comment':'comment'}
            
        
        # SOURCE LINE 544
        __M_writer(u'\n    <table class="table table-hover table-condensed">\n        <tbody>\n        \n')
        # SOURCE LINE 548
        for itemCode in activity['itemList']:
            # SOURCE LINE 549
            __M_writer(u'            ')
 
            objType = activity['items'][itemCode]['objType']
            activityStr = actionMapping[objType]
            
            if 'workshopCode' in activity['items'][itemCode]:
                workshopCode = activity['items'][itemCode]['workshopCode']
                workshopLink = "/workshop/" + activity['workshops'][workshopCode]['urlCode'] + "/" + activity['workshops'][workshopCode]['url']
            else:
                workshopCode = "photo"
                workshopLink = "/foo/photo"
            parent = False
            if activity['items'][itemCode]['objType'] == 'comment':
                parentCode = activity['items'][itemCode]['parentCode']
                parentObjType = activity['parents'][parentCode]['objType']
                if parentObjType == 'photo':
                    ownerID = activity['parents'][parentCode]['owner']
                    owner = userLib.getUserByID(ownerID)
                    parentLink = "/profile/" + owner['urlCode'] + "/" + owner['url'] + "/photo/show/" + parentCode
                else:
                    parentLink = workshopLink + "/" + parentObjType + "/" + activity['parents'][parentCode]['urlCode'] + "/" + activity['parents'][parentCode]['url']
                title = lib_6.ellipsisIZE(activity['items'][itemCode]['data'], 40)
                itemLink = parentLink + '?comment=' + itemCode
            else:
                parentCode = False
                title = lib_6.ellipsisIZE(activity['items'][itemCode]['title'], 40)
                itemLink = workshopLink + "/" + activity['items'][itemCode]['objType'] + "/" + activity['items'][itemCode]['urlCode'] + "/" + activity['items'][itemCode]['url']
            
            
                        
            
            # SOURCE LINE 577
            __M_writer(u'\n\n')
            # SOURCE LINE 579
            if objType == 'photo':
                # SOURCE LINE 580
                __M_writer(u'                ')
 
                ownerID = activity['items'][itemCode]['owner']
                owner = userLib.getUserByID(ownerID)
                title = activity['items'][itemCode]['title']
                urlCode = activity['items'][itemCode]['urlCode']
                link = "/profile/" + owner['urlCode'] + "/" + owner['url'] + "/photo/show/" + urlCode
                activityStr = "added the picture <a href=\"" + link + "\">" + title + "</a>"
                                
                                
                
                # SOURCE LINE 588
                __M_writer(u'\n')
                # SOURCE LINE 589
                if activity['items'][itemCode]['deleted'] == '0':
                    # SOURCE LINE 590
                    __M_writer(u'                    <tr><td>')
                    __M_writer(activityStr )
                    __M_writer(u'</td></tr>\n')
                    pass
                # SOURCE LINE 592
            elif objType == 'comment' and workshopCode == 'photo':
                # SOURCE LINE 593
                __M_writer(u'                ')
 
                if parentCode and activity['parents'][parentCode]['deleted'] != '1':
                    activityStr = "commented on a <a href=\"" + parentLink + "\">picture</a>, saying"
                    activityStr += " <a href=\"" + itemLink + "\" class=\"expandable\">" + title + "</a>"
                                
                
                # SOURCE LINE 597
                __M_writer(u'\n                <tr><td>')
                # SOURCE LINE 598
                __M_writer(activityStr )
                __M_writer(u' </td></tr>\n')
                # SOURCE LINE 599
            else:
                # SOURCE LINE 600
                if activity['workshops'][workshopCode]['public_private'] == 'public' or (c.browser == False or c.isAdmin == True or c.isUser == True):
                    # SOURCE LINE 601
                    if activity['items'][itemCode]['deleted'] == '0':
                        # SOURCE LINE 602
                        __M_writer(u'                        ')
 
                        if parentCode and activity['parents'][parentCode]['deleted'] == '1':
                            continue
                        
                        if objType == 'comment':
                            if parentObjType == 'idea':
                                activityStr += 'n'
                            activityStr += ' <a href="' + parentLink + '">' + objTypeMapping[parentObjType] + '</a>, saying'
                            activityStr += ' <a href="' + itemLink + '" class="expandable">' + title + '</a>'
                        else:
                            activityStr += ' <a href="' + itemLink + '" class="expandable">' + title + '</a>'
                                                
                        
                        # SOURCE LINE 613
                        __M_writer(u'\n                        <tr><td>')
                        # SOURCE LINE 614
                        __M_writer(activityStr )
                        __M_writer(u'</td></tr>\n')
                        pass
                    pass
                pass
            pass
        # SOURCE LINE 619
        __M_writer(u'        </tbody>\n    </table>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_inviteCoFacilitate(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 637
        __M_writer(u'\n')
        # SOURCE LINE 638
        if 'user' in session and c.authuser:
            # SOURCE LINE 639
            __M_writer(u'        ')

            fList = facilitatorLib.getFacilitatorsByUser(c.authuser)
            wListF = []
            wListL = []
            for f in fList:
                if not 'initiativeCode' in f:
                    w = workshopLib.getWorkshopByCode(f['workshopCode'])
                    if w['deleted'] == '0':
                        wlisten = listenerLib.getListener(c.user['email'], w)
                        if not facilitatorLib.isFacilitator(c.user, w) and not facilitatorLib.isPendingFacilitator(c.user, w):
                            wListF.append(w)
                        if (not wlisten or wlisten['disabled'] == '1') and w['type'] != 'personal':
                            wListL.append(w)
                    
            
            # SOURCE LINE 652
            __M_writer(u'\n')
            # SOURCE LINE 653
            if c.authuser.id != c.user.id and wListF:
                # SOURCE LINE 654
                __M_writer(u'            <div class="row">\n                <div class="centered">\n                <form method="post" name="inviteFacilitate" id="inviteFacilitate" action="/profile/')
                # SOURCE LINE 656
                __M_writer(escape(c.user['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.user['url']))
                __M_writer(u'/facilitate/invite/handler/" class="form-inline">\n                    <br />\n                    <button type="submit" class="btn btn-mini btn-warning" title="Click to invite this member to cofacilitate the selected workshop">Invite</button> to co-facilitate <select name="inviteToFacilitate">\n')
                # SOURCE LINE 659
                for myW in wListF:
                    # SOURCE LINE 660
                    __M_writer(u'                        <option value="')
                    __M_writer(escape(myW['urlCode']))
                    __M_writer(u'/')
                    __M_writer(escape(myW['url']))
                    __M_writer(u'">')
                    __M_writer(escape(myW['title']))
                    __M_writer(u'</option>\n')
                    pass
                # SOURCE LINE 662
                __M_writer(u'                    </select>\n                </form>\n                </div>\n            </div><!-- row -->\n')
                pass
            # SOURCE LINE 667
            if wListL:
                # SOURCE LINE 668
                __M_writer(u'            <div class="row">\n                <div class="centered">\n                <form method="post" name="inviteListen" id="inviteListen" action="/profile/')
                # SOURCE LINE 670
                __M_writer(escape(c.user['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.user['url']))
                __M_writer(u'/listener/invite/handler" class="form-inline">\n                    <br />\n                    <button type="submit" class="btn btn-mini btn-warning" title="Click to invite this member to be a listener of the selected workshop">Invite</button> to be a listener <select name="workshopCode">\n')
                # SOURCE LINE 673
                for myW in wListL:
                    # SOURCE LINE 674
                    __M_writer(u'                        <option value="')
                    __M_writer(escape(myW['urlCode']))
                    __M_writer(u'">')
                    __M_writer(escape(myW['title']))
                    __M_writer(u'</option>\n')
                    pass
                # SOURCE LINE 676
                __M_writer(u'                    </select>\n                    <input type="text" name="lTitle" placeholder="Title or Description" required>\n                </form>\n                </div>\n            </div><!-- row -->\n')
                pass
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_addTopic(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 773
        __M_writer(u'\n    <form ng-controller="topicController" ng-init="userCode = \'')
        # SOURCE LINE 774
        __M_writer(escape(c.user['urlCode']))
        __M_writer(u"'; userURL = '")
        __M_writer(escape(c.user['url']))
        __M_writer(u'\'; topicCode = \'new\'; addTopicTitleResponse=\'\'; addUpdateTextResponse=\'\'; addTopicResponse=\'\';"  id="addTopicForm" name="addTopicForm" ng-submit="submitTopicForm(addTopicForm)">\n        <fieldset>\n            <label>Topic Title</label><span class="help-block"> (Try to keep your title informative, but concise.) </span>\n            <input type="text" class="input-block-level" name="title" ng-model="title" maxlength = "120" required>\n            <span ng-show="addTopicTitleShow"><div class="alert alert-danger" ng-cloak>{{addTopicTitleResponse}}</div></span>\n        </fieldset>\n        <fieldset>\n            <label><strong>Topic Description</strong>\n            <a href="#" class="btn btn-mini btn-info" onclick="window.open(\'/help/markdown.html\',\'popUpWindow\',\'height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes\');"><i class="icon-list"></i> <i class="icon-photo"></i> View Formatting Guide</a></label>\n            <textarea name="text" rows="3" class="input-block-level" ng-model="text" required></textarea>\n            <span ng-show="addTopicTextShow"><div class="alert alert-danger" ng-cloak>{{addTopicTextResponse}}</div></span>\n            <span class="help-block"> (Describe the topic you wish to discuss in the forum.) </span>\n        </fieldset>\n        <fieldset>\n            <button class="btn btn-large btn-civ pull-right" type="submit" name="submit">Submit</button>\n        </fieldset>\n   </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showMemberPosts(context,activity):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 332
        __M_writer(u'\n    ')
        # SOURCE LINE 333

        actionMapping = {   'resource': 'added the resource',
                            'discussion': 'started the conversation',
                            'idea': 'posed the idea',
                            'photo': 'added the picture',
                            'initiative': 'launched the initiative',
                            'comment': 'commented on a'}
        
        objTypeMapping = {  'resource':'resource',
                            'discussion':'conversation',
                            'idea':'idea',
                            'photo':'photo',
                            'initiative':'initiative',
                            'comment':'comment'}
            
        
        # SOURCE LINE 347
        __M_writer(u'\n    <table class="table table-hover table-condensed">\n        <tbody>\n        \n')
        # SOURCE LINE 351
        for item in activity:
            # SOURCE LINE 352
            __M_writer(u'            ')
 
            objType = item.objType.replace("Unpublished", "")
            activityStr = actionMapping[objType]
            
            if 'workshopCode' in item:
                workshopLink = "/workshop/" + item['workshopCode'] + "/" + item['workshop_url']
            else:
                workshopCode = "photo"
                workshopLink = "/foo/photo"
            parent = False
            
            if objType == 'comment':
                if 'workshopCode' in item:
                    if 'ideaCode' in item:
                        parentCode = item['ideaCode']
                        parentURL = item['parent_url']
                        parentObjType = 'idea'
                    elif 'resourceCode' in item:
                        parentCode = item['resourceCode']
                        parentURL = item['parent_url']
                        parentObjType = 'resource'
                    elif 'discussionCode' in item:
                        parentCode = item['discussionCode']
                        parentURL = item['parent_url']
                        parentObjType = 'discussion'
                    parentLink = workshopLink + "/" + parentObjType + "/" + parentCode + "/" + parentURL
                elif 'photoCode' in item:
                    parentCode = item['photoCode']
                    parentURL = item['parent_url']
                    parentObjType = 'photo'
                    parentLink = "/profile/" + item['profileCode'] + "/" + item['profile_url'] + "/photo/show/" + parentCode
                elif 'initiativeCode' in item and 'resourceCode' in item:
                    parentCode = item['resourceCode']
                    parentURL = item['parent_url']
                    parentObjType = 'resource'
                    parentLink = "/initiative/" + item['initiativeCode'] + "/" + item['initiative_url'] + "/resource/"+ parentCode + "/" + parentURL
                elif 'initiativeCode' in item:
                    parentCode = item['initiativeCode']
                    parentURL = item['parent_url']
                    parentObjType = 'initiative'
                    parentLink = "/initiative/" + parentCode + "/" + parentURL + "/show/"
                elif 'profileCode' in item:
                    # not a photo, must be an organization discussion
                    parentLink = "/profile/" + item['profileCode'] + "/" + item['profile_url'] + "/discussion/show/" + item['discussionCode']
                    parentCode = item['discussionCode']
                    parentObjType = 'discussion'
                    parentURL = item['parent_url']
                else:
                    log.info("no parentObjType item is %s"%item.keys())
                    parentLink = workshopLink + "/" + parentObjType + "/" + parentCode + "/" + parentURL
                title = lib_6.ellipsisIZE(item['data'], 40)
                itemLink = parentLink + '?comment=' + item['urlCode']
            elif objType == 'resource' and 'initiativeCode' in item:
                    parentCode = item['initiativeCode']
                    parentURL = item['initiative_url']
                    parentObjType = 'initiative'
                    title = lib_6.ellipsisIZE(item['title'], 40)
            else:
                parentCode = False
                title = lib_6.ellipsisIZE(item['title'], 40)
                itemLink = workshopLink + "/" + objType + "/" + item['urlCode'] + "/" + item['url']
                        
            
            # SOURCE LINE 413
            __M_writer(u'\n\n')
            # SOURCE LINE 415
            if objType == 'photo':
                # SOURCE LINE 416
                __M_writer(u'                ')
 
                link = "/profile/" + item['userCode'] + "/" + item['user_url'] + "/photo/show/" + item['urlCode']
                activityStr = "added the picture <a href=\"" + link + "\">" + title + "</a>"
                                
                                
                
                # SOURCE LINE 420
                __M_writer(u'\n')
                # SOURCE LINE 421
                if item['deleted'] == '0':
                    # SOURCE LINE 422
                    __M_writer(u'                    <tr><td>')
                    __M_writer(activityStr )
                    __M_writer(u'</td></tr>\n')
                    pass
                # SOURCE LINE 424
            elif objType == 'initiative':
                # SOURCE LINE 425
                __M_writer(u'                ')
 
                link = "/initiative/" + item['urlCode'] + "/" + item['url'] + "/show"
                activityStr = "launched the initiative <a href=\"" + link + "\">" + title + "</a>"
                                
                                
                
                # SOURCE LINE 429
                __M_writer(u'\n')
                # SOURCE LINE 430
                if item['deleted'] == '0' and item['public'] == '1':
                    # SOURCE LINE 431
                    __M_writer(u'                    <tr><td>')
                    __M_writer(activityStr )
                    __M_writer(u'</td></tr>\n')
                    pass
                # SOURCE LINE 433
            elif objType == 'resource' and 'initiativeCode' in item:
                # SOURCE LINE 434
                __M_writer(u'                ')
 
                link = "/initiative/" + parentCode + "/" + parentURL + "/resource/" + item['urlCode'] + "/" + item['url']
                activityStr = "added the resource <a href=\"" + link + "\">" + title + "</a>"
                                
                                
                
                # SOURCE LINE 438
                __M_writer(u'\n')
                # SOURCE LINE 439
                if item['deleted'] == '0' and item['initiative_public'] == '1':
                    # SOURCE LINE 440
                    __M_writer(u'                    <tr><td>')
                    __M_writer(activityStr )
                    __M_writer(u'</td></tr>\n')
                    pass
                # SOURCE LINE 442
            elif objType == 'comment' and 'initiativeCode' in item and 'resourceCode' in item:
                # SOURCE LINE 443
                __M_writer(u'                ')
 
                activityStr = "commented on a <a href=\"" + parentLink + "\">resource</a>, saying"
                activityStr += " <a href=\"" + itemLink + "\" class=\"expandable\">" + title + "</a>"
                                
                
                # SOURCE LINE 446
                __M_writer(u'\n')
                # SOURCE LINE 447
                if item['deleted'] == '0' and item['initiative_public'] == '1':
                    # SOURCE LINE 448
                    __M_writer(u'                    <tr><td>')
                    __M_writer(activityStr )
                    __M_writer(u' </td></tr>\n')
                    pass
                # SOURCE LINE 450
            elif objType == 'comment' and 'discType' in item and item['discType'] == 'organization_position':
                # SOURCE LINE 451
                __M_writer(u'                ')
 
                if 'initiativeCode' in item:
                    pItem = 'initiative'
                else:
                    pItem = 'idea'
                link = "/profile/" + item['userCode'] + "/" + item['user_url'] + "/position/show/" + item['discussionCode']
                activityStr = "commented on an organization <a href=\"" + link + "\">position</a>, saying"
                activityStr += " <a href=\"" + link + "\" class=\"expandable\">" + title + "</a>"
                                
                
                # SOURCE LINE 459
                __M_writer(u'\n')
                # SOURCE LINE 460
                if item['deleted'] == '0':
                    # SOURCE LINE 461
                    __M_writer(u'                    <tr><td>')
                    __M_writer(activityStr )
                    __M_writer(u' </td></tr>\n')
                    pass
                # SOURCE LINE 463
            elif objType == 'comment' and 'initiativeCode' in item:
                # SOURCE LINE 464
                __M_writer(u'                ')
 
                activityStr = "commented on an <a href=\"" + parentLink + "\">initiative</a>, saying"
                activityStr += " <a href=\"" + itemLink + "\" class=\"expandable\">" + title + "</a>"
                                
                
                # SOURCE LINE 467
                __M_writer(u'\n')
                # SOURCE LINE 468
                if item['deleted'] == '0' and ('initiative_public' in item and item['initiative_public'] == '1'):
                    # SOURCE LINE 469
                    __M_writer(u'                    <tr><td>')
                    __M_writer(activityStr )
                    __M_writer(u' </td></tr>\n')
                    pass
                # SOURCE LINE 471
            elif objType == 'comment' and 'photoCode' in item:
                # SOURCE LINE 472
                __M_writer(u'                ')
 
                activityStr = "commented on a <a href=\"" + parentLink + "\">picture</a>, saying"
                activityStr += " <a href=\"" + itemLink + "\" class=\"expandable\">" + title + "</a>"
                                
                
                # SOURCE LINE 475
                __M_writer(u'\n')
                # SOURCE LINE 476
                if item['deleted'] == '0':
                    # SOURCE LINE 477
                    __M_writer(u'                    <tr><td>')
                    __M_writer(activityStr )
                    __M_writer(u' </td></tr>\n')
                    pass
                # SOURCE LINE 479
            elif objType == 'discussion' and item['discType'] == 'organization_general':
                # SOURCE LINE 480
                __M_writer(u'                ')
 
                link = "/profile/" + item['userCode'] + "/" + item['user_url'] + "/discussion/show/" + item['urlCode']
                activityStr = "started the organization forum topic "
                activityStr += " <a href=\"" + link + "\" class=\"expandable\">" + title + "</a>"
                                
                
                # SOURCE LINE 484
                __M_writer(u'\n')
                # SOURCE LINE 485
                if item['deleted'] == '0':
                    # SOURCE LINE 486
                    __M_writer(u'                    <tr><td>')
                    __M_writer(activityStr )
                    __M_writer(u' </td></tr>\n')
                    pass
                # SOURCE LINE 488
            elif objType == 'discussion' and item['discType'] == 'organization_position':
                # SOURCE LINE 489
                __M_writer(u'                ')
 
                if 'initiativeCode' in item:
                    pItem = 'initiative'
                    pTitle = item['initiative_title']
                else:
                    pItem = 'idea'
                    pTitle = item['idea_title']
                link = "/profile/" + item['userCode'] + "/" + item['user_url'] + "/position/show/" + item['urlCode']
                activityStr = "took a position to %s the %s "%(item['position'], pItem)
                activityStr += " <a href=\"" + link + "\" class=\"expandable\">" + pTitle + "</a>"
                                
                
                # SOURCE LINE 499
                __M_writer(u'\n')
                # SOURCE LINE 500
                if item['deleted'] == '0':
                    # SOURCE LINE 501
                    __M_writer(u'                    <tr><td>')
                    __M_writer(activityStr )
                    __M_writer(u' </td></tr>\n')
                    pass
                # SOURCE LINE 503
            elif objType == 'comment' and 'profileCode' in item:
                # SOURCE LINE 504
                __M_writer(u'                ')
 
                activityStr = "commented on an organization forum <a href=\"" + parentLink + "\">discussion</a>, saying"
                activityStr += " <a href=\"" + itemLink + "\" class=\"expandable\">" + title + "</a>"
                                
                
                # SOURCE LINE 507
                __M_writer(u'\n')
                # SOURCE LINE 508
                if item['deleted'] == '0':
                    # SOURCE LINE 509
                    __M_writer(u'                    <tr><td>')
                    __M_writer(activityStr )
                    __M_writer(u' </td></tr>\n')
                    pass
                # SOURCE LINE 511
            elif 'workshopCode' in item:
                # SOURCE LINE 512
                if item['workshop_searchable'] == '1' or (c.browser == False or c.isAdmin == True or c.isUser == True):
                    # SOURCE LINE 513
                    if item['deleted'] == '0':
                        # SOURCE LINE 514
                        __M_writer(u'                        ')
 
                        if objType == 'comment':
                            if parentObjType == 'idea':
                                activityStr += 'n'
                            activityStr += ' <a href="' + parentLink + '">' + objTypeMapping[parentObjType] + '</a>, saying'
                            activityStr += ' <a href="' + itemLink + '" class="expandable">' + title + '</a>'
                        else:
                            activityStr += ' <a href="' + itemLink + '" class="expandable">' + title + '</a>'
                                                
                        
                        # SOURCE LINE 522
                        __M_writer(u'\n                        <tr><td>')
                        # SOURCE LINE 523
                        __M_writer(activityStr )
                        __M_writer(u'</td></tr>\n')
                        pass
                    pass
                pass
            pass
        # SOURCE LINE 528
        __M_writer(u'        </tbody>\n    </table>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showPosition(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 735
        __M_writer(u'\n    ')
        # SOURCE LINE 736

        url = "/profile/" + c.user['urlCode'] + "/" + c.user['url'] + "/position/show/" + c.discussion['urlCode']
        role = ''
        if 'addedAs' in c.discussion.keys():
            roles = ['admin', 'facilitator', 'listener']
            if c.discussion['addedAs'] in roles:
                role = ' (%s)' % c.discussion['addedAs']
        
        if 'initiativeCode' in c.discussion:
            parentType = 'initiative'
            parentURL = "/initiative/%s/%s/show"%(c.discussion['initiativeCode'], c.discussion['initiative_url'])
            parentTitle = c.discussion['initiative_title']
        else:
            parentType = 'idea'
            parentURL = "/workshop/%s/%s/idea/%s/%s"%(c.discussion['workshopCode'], c.discussion['workshop_url'], c.discussion['ideaCode'], c.discussion['idea_url'])
            parentTitle = c.discussion['idea_title']
            
        
        # SOURCE LINE 752
        __M_writer(u'\n    <div class="row-fluid">\n        <div class="span2">\n            ')
        # SOURCE LINE 755
        __M_writer(escape(lib_6.upDownVote(c.discussion)))
        __M_writer(u'\n        </div><!-- span2 -->\n        <div class="span10">\n            <h3><a href="')
        # SOURCE LINE 758
        __M_writer(escape(url))
        __M_writer(u'" class="listed-item-title">')
        __M_writer(escape(c.discussion['title']))
        __M_writer(u'</a></h3>\n            View ')
        # SOURCE LINE 759
        __M_writer(escape(parentType))
        __M_writer(u': <a href="')
        __M_writer(escape(parentURL))
        __M_writer(u'">')
        __M_writer(escape(parentTitle))
        __M_writer(u'</a>\n            <div class="spacer"></div>\n')
        # SOURCE LINE 761
        if 'text' in c.discussion.keys():
            # SOURCE LINE 762
            __M_writer(u'                ')
            __M_writer(misaka.html(c.discussion['text']) )
            __M_writer(u'\n')
            pass
        # SOURCE LINE 764
        __M_writer(u'            ')
        __M_writer(escape(lib_6.userLink(c.discussion.owner)))
        __M_writer(escape(role))
        __M_writer(u' from ')
        __M_writer(escape(lib_6.userGeoLink(c.discussion.owner)))
        __M_writer(escape(lib_6.userImage(c.discussion.owner, className="avatar med-avatar")))
        __M_writer(u'\n')
        # SOURCE LINE 765
        if c.discussion.objType == 'discussion':
            # SOURCE LINE 766
            __M_writer(u'                <br />Originally posted  ')
            __M_writer(escape(c.discussion.date))
            __M_writer(u'\n                <i class="icon-eye-open"></i> ')
            # SOURCE LINE 767
            __M_writer(escape(str(c.discussion['views'])))
            __M_writer(u' views\n')
            pass
        # SOURCE LINE 769
        __M_writer(u'        </div><!-- span10 -->\n    </div><!-- row-fluid -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showDiscussion(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 697
        __M_writer(u'\n    ')
        # SOURCE LINE 698

        url = "/profile/" + c.user['urlCode'] + "/" + c.user['url'] + "/discussion/show/" + c.discussion['urlCode']
        role = ''
        if 'addedAs' in c.discussion.keys():
            roles = ['admin', 'facilitator', 'listener']
            if c.discussion['addedAs'] in roles:
                role = ' (%s)' % c.discussion['addedAs']
            
        
        # SOURCE LINE 705
        __M_writer(u'\n    <div class="row-fluid">\n        <div class="span2">\n            ')
        # SOURCE LINE 708
        __M_writer(escape(lib_6.upDownVote(c.discussion)))
        __M_writer(u'\n        </div><!-- span2 -->\n        <div class="span10">\n            <h3><a href="')
        # SOURCE LINE 711
        __M_writer(escape(url))
        __M_writer(u'" class="listed-item-title">')
        __M_writer(escape(c.discussion['title']))
        __M_writer(u'</a></h3>\n')
        # SOURCE LINE 712
        if 'text' in c.discussion.keys():
            # SOURCE LINE 713
            __M_writer(u'                ')
            __M_writer(misaka.html(c.discussion['text']) )
            __M_writer(u'\n')
            pass
        # SOURCE LINE 715
        __M_writer(u'            ')
        __M_writer(escape(lib_6.userLink(c.discussion.owner)))
        __M_writer(escape(role))
        __M_writer(u' from ')
        __M_writer(escape(lib_6.userGeoLink(c.discussion.owner)))
        __M_writer(escape(lib_6.userImage(c.discussion.owner, className="avatar med-avatar")))
        __M_writer(u'\n')
        # SOURCE LINE 716
        if c.discussion.objType == 'discussion':
            # SOURCE LINE 717
            __M_writer(u'                <br />Originally posted  ')
            __M_writer(escape(c.discussion.date))
            __M_writer(u'\n                <i class="icon-eye-open"></i> ')
            # SOURCE LINE 718
            __M_writer(escape(str(c.discussion['views'])))
            __M_writer(u' views\n')
            pass
        # SOURCE LINE 720
        __M_writer(u'        </div><!-- span10 -->\n    </div><!-- row-fluid -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showActivity(context,activity):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 623
        __M_writer(u'\n    <table class="table table-hover table-condensed">\n        <tbody>\n        \n')
        # SOURCE LINE 627
        for item in activity:
            # SOURCE LINE 628
            __M_writer(u'            ')
            workshop = workshopLib.getWorkshopByCode(item['workshopCode']) 
            
            __M_writer(u'\n')
            # SOURCE LINE 629
            if workshop['public_private'] == 'public' or (c.browser == False or c.isAdmin == True or c.isUser == True): 
                # SOURCE LINE 630
                __M_writer(u'                <tr><td>')
                __M_writer(escape(lib_6.showItemInActivity(item, workshop, expandable = True)))
                __M_writer(u'</td></tr>\n')
                pass
            pass
        # SOURCE LINE 633
        __M_writer(u'        </tbody>\n    </table>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_profileModerationPanel(context,thing):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 793
        __M_writer(u'\n    ')
        # SOURCE LINE 794

        if 'user' not in session or thing.objType == 'revision':
            return
        flagID = 'flag-%s' % thing['urlCode']
        editID = 'edit-%s' % thing['urlCode']
        adminID = 'admin-%s' % thing['urlCode']
        publishID = 'publish-%s' % thing['urlCode']
        unpublishID = 'unpublish-%s' % thing['urlCode']
            
        
        # SOURCE LINE 802
        __M_writer(u'\n    <div class="btn-group">\n')
        # SOURCE LINE 804
        if thing['disabled'] == '0':
            # SOURCE LINE 805
            __M_writer(u'            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#')
            __M_writer(escape(flagID))
            __M_writer(u'">flag</a>\n')
            pass
        # SOURCE LINE 807
        if c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id):
            # SOURCE LINE 808
            __M_writer(u'            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#')
            __M_writer(escape(editID))
            __M_writer(u'">edit</a>>\n')
            pass
        # SOURCE LINE 810
        if userLib.isAdmin(c.authuser.id):
            # SOURCE LINE 811
            __M_writer(u'            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#')
            __M_writer(escape(adminID))
            __M_writer(u'">admin</a>\n')
            pass
        # SOURCE LINE 813
        __M_writer(u'\n    </div>\n    \n')
        # SOURCE LINE 816
        if thing['disabled'] == '0':
            # SOURCE LINE 817
            __M_writer(u'        ')
            __M_writer(escape(lib_6.flagThing(thing)))
            __M_writer(u'\n')
            # SOURCE LINE 818
            if (c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id)):
                # SOURCE LINE 819
                __M_writer(u'            ')
                __M_writer(escape(lib_6.editThing(thing)))
                __M_writer(u'\n')
                # SOURCE LINE 820
                if userLib.isAdmin(c.authuser.id):
                    # SOURCE LINE 821
                    __M_writer(u'                ')
                    __M_writer(escape(lib_6.adminThing(thing)))
                    __M_writer(u'\n')
                    pass
                pass
            # SOURCE LINE 824
        else:
            # SOURCE LINE 825
            if userLib.isAdmin(c.authuser.id):
                # SOURCE LINE 826
                __M_writer(u'            ')
                __M_writer(escape(lib_6.editThing(thing)))
                __M_writer(u'\n')
                pass
            # SOURCE LINE 828
            if userLib.isAdmin(c.authuser.id):
                # SOURCE LINE 829
                __M_writer(u'            ')
                __M_writer(escape(lib_6.adminThing(thing)))
                __M_writer(u'\n')
                pass
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_followButton(context,user):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 314
        __M_writer(u'\n')
        # SOURCE LINE 315
        if c.conf['read_only.value'] == 'true':
            # SOURCE LINE 316
            __M_writer(u'          ')
            pass 
            
            __M_writer(u'\n')
            # SOURCE LINE 317
        else:
            # SOURCE LINE 318
            __M_writer(u'        <span class="button_container">\n')
            # SOURCE LINE 319
            if c.isFollowing:
                # SOURCE LINE 320
                __M_writer(u'            <button data-URL-list="profile_')
                __M_writer(escape(c.user['urlCode']))
                __M_writer(u'_')
                __M_writer(escape(c.user['url']))
                __M_writer(u'" class="btn-civ btn pull-right followButton following">\n            <span><i class="icon-user icon-white"></i><strong> Following </strong></span>\n            </button>\n')
                # SOURCE LINE 323
            else:
                # SOURCE LINE 324
                __M_writer(u'            <button data-URL-list="profile_')
                __M_writer(escape(c.user['urlCode']))
                __M_writer(u'_')
                __M_writer(escape(c.user['url']))
                __M_writer(u'" class="btn pull-right followButton unfollow">\n            <span><i class="icon-user med-green"></i><strong> Follow </strong></span>\n            </button>\n')
                pass
            # SOURCE LINE 328
            __M_writer(u'        </span>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


