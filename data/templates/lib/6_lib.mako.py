# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398540606.9507971
_template_filename = u'/home/maria/civinomics/pylowiki/templates/lib/6_lib.mako'
_template_uri = u'/lib/6_lib.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['readOnlyMessage', 'fields_alert', 'emailShareModal', 'enableThingLink', 'facebookDialogShare2', 'unpublishThingLink', '_userImageSource', 'createNew', 'showPositions', 'immunifyThingLink', 'public_tag_filter', 'yesNoVote', 'listBookmarks', 'unpublishThing', 'public_tags', 'flagThing', 'ideaLink', 'discussionLink', 'publishThingLink', 'bookmarkOptions', 'flagThingLink', 'userImage', 'initiativeLink', 'workshopImage', 'public_tag_list_filter', 'validateSession', 'outOfScope', 'formattingGuide', 'photoLink', 'facebookDialogShare', 'commentLinkAppender', 'commentLink', 'showTags', 'geoButton', 'publishThing', 'editThingLink', 'public_tag_links', 'upDownVote', 'disableThingLink', 'emailShare', 'thingLinkRouter', 'adminThing', 'resourceLink', 'userLink', 'orgPosition', 'geoBreadcrumbs', 'revisionHistory', 'geoDropdown', '_geoWorkshopLink', 'userGeoLink', 'userGreetingMsg', 'deleteThingLink', 'showFullScope', 'adoptThingLink', 'editThing', 'showItemInActivity', 'isReadOnly', 'ellipsisIZE', 'showScope', 'fingerprintFile', 'initiativeImage', 'workshopLink', 'myPlaces']


# SOURCE LINE 1

from pylowiki.lib.db.geoInfo import getGeoInfo

import locale
try:
   locale.setlocale(locale.LC_ALL, 'en_US.utf8')
except: #windows
   locale.setlocale(locale.LC_ALL, 'eng_US')

import pylowiki.lib.db.discussion    as discussionLib
import pylowiki.lib.db.idea          as ideaLib
import pylowiki.lib.db.resource      as resourceLib
import pylowiki.lib.db.user          as userLib
import pylowiki.lib.db.rating        as ratingLib
import pylowiki.lib.db.mainImage     as mainImageLib
import pylowiki.lib.db.tag           as tagLib
import pylowiki.lib.db.workshop      as workshopLib
import pylowiki.lib.db.photo         as photoLib
import pylowiki.lib.db.follow        as followLib
import pylowiki.lib.db.initiative    as initiativeLib
import pylowiki.lib.utils            as utilsLib
from pylons import session

import misaka as m
from hashlib import md5
import logging, os
log = logging.getLogger(__name__)


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 29
    ns = runtime.TemplateNamespace(u'homeHelpers', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_workshop_home.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'homeHelpers')] = ns

    # SOURCE LINE 30
    ns = runtime.TemplateNamespace(u'ihelpers', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_initiative_home.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'ihelpers')] = ns

def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 28
        __M_writer(u'\n')
        # SOURCE LINE 29
        __M_writer(u'\n')
        # SOURCE LINE 30
        __M_writer(u'\n\n')
        # SOURCE LINE 244
        __M_writer(u'\n\n')
        # SOURCE LINE 475
        __M_writer(u'\n\n')
        # SOURCE LINE 484
        __M_writer(u'\n\n')
        # SOURCE LINE 514
        __M_writer(u'\n\n')
        # SOURCE LINE 522
        __M_writer(u'\n\n')
        # SOURCE LINE 585
        __M_writer(u'\n\n')
        # SOURCE LINE 602
        __M_writer(u'\n\n')
        # SOURCE LINE 621
        __M_writer(u'\n\n')
        # SOURCE LINE 712
        __M_writer(u'\n\n')
        # SOURCE LINE 721
        __M_writer(u'\n\n')
        # SOURCE LINE 770
        __M_writer(u'\n\n')
        # SOURCE LINE 774
        __M_writer(u'\n\n')
        # SOURCE LINE 806
        __M_writer(u'\n\n')
        # SOURCE LINE 822
        __M_writer(u'\n\n')
        # SOURCE LINE 834
        __M_writer(u'\n\n')
        # SOURCE LINE 868
        __M_writer(u'\n\n')
        # SOURCE LINE 882
        __M_writer(u'\n\n')
        # SOURCE LINE 920
        __M_writer(u'\n\n')
        # SOURCE LINE 937
        __M_writer(u'\n\n')
        # SOURCE LINE 959
        __M_writer(u'\n\n')
        # SOURCE LINE 977
        __M_writer(u'\n\n')
        # SOURCE LINE 1006
        __M_writer(u'\n\n')
        # SOURCE LINE 1027
        __M_writer(u'\n\n')
        # SOURCE LINE 1076
        __M_writer(u'\n\n')
        # SOURCE LINE 1115
        __M_writer(u'\n\n')
        # SOURCE LINE 1177
        __M_writer(u'\n\n')
        # SOURCE LINE 1225
        __M_writer(u'\n\n')
        # SOURCE LINE 1252
        __M_writer(u'\n\n')
        # SOURCE LINE 1282
        __M_writer(u'\n\n')
        # SOURCE LINE 1296
        __M_writer(u'\n\n\n\n\n')
        # SOURCE LINE 1321
        __M_writer(u'\n\n')
        # SOURCE LINE 1338
        __M_writer(u'\n\n')
        # SOURCE LINE 1357
        __M_writer(u'\n\n')
        # SOURCE LINE 1372
        __M_writer(u'\n\n')
        # SOURCE LINE 1387
        __M_writer(u'\n\n')
        # SOURCE LINE 1402
        __M_writer(u'\n\n')
        # SOURCE LINE 1417
        __M_writer(u'\n\n')
        # SOURCE LINE 1432
        __M_writer(u'\n\n')
        # SOURCE LINE 1447
        __M_writer(u'\n\n')
        # SOURCE LINE 1462
        __M_writer(u'\n\n')
        # SOURCE LINE 1477
        __M_writer(u'\n\n')
        # SOURCE LINE 1492
        __M_writer(u'\n\n')
        # SOURCE LINE 1505
        __M_writer(u'\n\n')
        # SOURCE LINE 1518
        __M_writer(u'\n\n')
        # SOURCE LINE 1531
        __M_writer(u'\n\n')
        # SOURCE LINE 1636
        __M_writer(u'\n\n')
        # SOURCE LINE 1717
        __M_writer(u'\n\n')
        # SOURCE LINE 1726
        __M_writer(u'\n\n')
        # SOURCE LINE 1748
        __M_writer(u'\n\n')
        # SOURCE LINE 1787
        __M_writer(u'\n\n')
        # SOURCE LINE 1846
        __M_writer(u'\n\n')
        # SOURCE LINE 1855
        __M_writer(u'\n\n')
        # SOURCE LINE 1870
        __M_writer(u'\n\n')
        # SOURCE LINE 1880
        __M_writer(u'\n\n')
        # SOURCE LINE 1888
        __M_writer(u'\n\n')
        # SOURCE LINE 1895
        __M_writer(u'\n\n')
        # SOURCE LINE 1928
        __M_writer(u'\n\n')
        # SOURCE LINE 1961
        __M_writer(u'\n\n')
        # SOURCE LINE 1965
        __M_writer(u'\n\n')
        # SOURCE LINE 1985
        __M_writer(u'\n\n')
        # SOURCE LINE 2018
        __M_writer(u'\n\n')
        # SOURCE LINE 2059
        __M_writer(u'\n\n')
        # SOURCE LINE 2072
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_readOnlyMessage(context,thing):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 772
        __M_writer(u'\n   <p> Read-only: cannot add a ')
        # SOURCE LINE 773
        __M_writer(escape(thing))
        __M_writer(u'. </p>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_fields_alert(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 1728
        __M_writer(u'\n')
        # SOURCE LINE 1729
        if 'alert' in session:
            # SOURCE LINE 1730
            __M_writer(u'        ')
 
            alert = session['alert']
            if 'type' not in alert.keys() or 'title' not in alert.keys() or 'content' not in alert.keys():
                # Something went wrong...clear and ignore the alert
                session.pop('alert')
                session.save()
                return
                    
            
            # SOURCE LINE 1737
            __M_writer(u' \n        <div class="alert alert-')
            # SOURCE LINE 1738
            __M_writer(escape(alert['type']))
            __M_writer(u'">\n            <button data-dismiss="alert" class="close">x</button>\n            <strong>')
            # SOURCE LINE 1740
            __M_writer(escape(alert['title']))
            __M_writer(u'</strong>\n            ')
            # SOURCE LINE 1741
            __M_writer(escape(alert['content']))
            __M_writer(u'\n        </div>\n        ')
            # SOURCE LINE 1743
 
            session.pop('alert')
            session.save()
                    
            
            # SOURCE LINE 1746
            __M_writer(u'\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_emailShareModal(context,itemURL,itemCode):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 486
        __M_writer(u'\n')
        # SOURCE LINE 487
        if ('user' in session and c.authuser) and (workshopLib.isPublished(c.w) and workshopLib.isPublic(c.w) and not c.privs['provisional']):
            # SOURCE LINE 488
            __M_writer(u'        ')
 
            memberMessage = "I thought this might interest you!"
                    
            
            # SOURCE LINE 490
            __M_writer(u'\n        <div id="emailShare')
            # SOURCE LINE 491
            __M_writer(escape(itemCode))
            __M_writer(u'" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">\n            <div class="modal-header">\n                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">\xd7</button>\n                <h3 id="myModalLabel">Share This With a Friend</h3>\n            </div><!-- modal-header -->\n            <div class="modal-body">\n              <div class="row-fluid">\n                <form ng-controller="shareController" ng-init="code=\'')
            # SOURCE LINE 498
            __M_writer(escape(c.w['urlCode']))
            __M_writer(u"'; url='")
            __M_writer(escape(c.w['url']))
            __M_writer(u"'; user='")
            __M_writer(escape(c.authuser['urlCode']))
            __M_writer(u"'; itemURL='")
            __M_writer(escape(itemURL))
            __M_writer(u"'; itemCode='")
            __M_writer(escape(itemCode))
            __M_writer(u"'; memberMessage='")
            __M_writer(escape(memberMessage))
            __M_writer(u'\'; recipientEmail=\'\'; recipientName=\'\'; shareEmailResponse=\'\';" id="shareEmailForm" ng-submit="shareEmail()" class="form-inline" name="shareEmailForm">\n                    <div class="alert" ng-show="shareEmailShow">{{shareEmailResponse}}</div>\n                    Your friend\'s email:<br>\n                    <input type="text" name="recipientEmail" ng-model="recipientEmail" required><br>\n                    <br>\n                    Add a message for your friend:<br />\n                    <textarea rows="6" class="field span12" ng-model="memberMessage" name="memberMessage">{{memberMessage}}</textarea>\n                    <div class="spacer"></div>\n                    <button class="btn btn-danger" data-dismiss="modal" aria-hidden="true">Close</button>\n                    <button type="submit" class="btn btn-success">Send Email</button>\n                    <br />\n                </form>\n              </div><!-- row -->\n            </div><!-- modal-body -->\n        </div><!-- modal -->\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_enableThingLink(context,thing,**kwargs):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 1374
        __M_writer(u'\n    ')
        # SOURCE LINE 1375

        enableStr = '"/enable/%s/%s"' %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return enableStr
                    return 'href = ' + enableStr
                return 'href = ' + enableStr
        enableStr = 'href = ' + enableStr
            
        
        # SOURCE LINE 1385
        __M_writer(u'\n    ')
        # SOURCE LINE 1386
        __M_writer(enableStr )
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_facebookDialogShare2(context,**kwargs):
    context.caller_stack._push_frame()
    try:
        int = context.get('int', UNDEFINED)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 32
        __M_writer(u'\n    ')
        # SOURCE LINE 33

        shareOk = False
        shareOn = False
        if c.facebookShare:
            if c.facebookShare.facebookAppId:
                shareOn = True
                # link: direct url to item being shared
                # picture: url of the parent workshop's background image
                facebookAppId = int(c.facebookShare.facebookAppId)
                #log.info("app id %s and %s"%(c.facebookShare.facebookAppId, facebookAppId))
                channelUrl = c.facebookShare.channelUrl
                thingCode = c.facebookShare.thingCode
        
                link = c.facebookShare.url
                image = c.facebookShare.image
                #log.info("link %s and image %s"%(link, image))
                userCode = ''
        
                parentCode = c.facebookShare.parentCode
        
                # in order to prevent the javascript for these buttons from being included multiple
                # times, these kwargs are now used to activate either or both of the buttons
                if 'shareOnWall' in kwargs:
                    if kwargs['shareOnWall'] is True:
                        shareOnWall = True
                    else:
                        shareOnWall = False
                else:
                    shareOnWall = False
        
                if 'sendMessage' in kwargs:
                    if kwargs['sendMessage'] is True:
                        sendMessage = True
                    else:
                        sendMessage = False
                else:
                    sendMessage = False
                
        
                title = c.facebookShare.title
                description = c.facebookShare.description
        
                # this is an elaborate way to get the item or workshop's description loaded as the caption
                caption = c.facebookShare.caption
                if c.thing:
                    if 'text' in c.thing.keys():
                        caption = c.thing['text']
                    else:
                        caption = ''
                
                shareOk = c.facebookShare.shareOk
        
            
        
        # SOURCE LINE 85
        __M_writer(u'\n\n')
        # SOURCE LINE 87
        if shareOk and shareOn:
            # SOURCE LINE 88
            __M_writer(u'        <div id="fb-root"></div>\n        <script src="/js/extauth.js" type="text/javascript"></script>\n        <script>\n            // activate facebook javascript sdk\n            var fbAuthId = \'\';\n            \n            window.fbAsyncInit = function() {\n                FB.init({\n                    appId      : "')
            # SOURCE LINE 96
            __M_writer(escape(facebookAppId))
            __M_writer(u'", // App ID\n                    channelUrl : "')
            # SOURCE LINE 97
            __M_writer(escape(channelUrl))
            __M_writer(u'", // Channel File\n                    status     : true, // check login status\n                    cookie     : false, // enable cookies to allow the server to access the session\n                    xfbml      : true  // parse XFBML\n                });\n                FB.Event.subscribe(\'auth.authResponseChange\', function(response) {\n                // Here we specify what we do with the response anytime this event occurs.\n                console.log(\'above response tree\');\n                if (response.status === \'connected\') {\n                    console.log(\'calling fb connected\');\n                    fbAuthId = response.authResponse.userID;\n                } else if (response.status === \'not_authorized\') {\n                    console.log(\'not authd\');                \n                    //FB.login();\n                } else {\n                    console.log(\'else\');\n                    //FB.login();\n                }\n                });\n            };\n            \n            // Load the SDK asynchronously\n            (function(d){\n                var js, id = \'facebook-jssdk\', ref = d.getElementsByTagName(\'script\')[0];\n                if (d.getElementById(id)) {return;}\n                js = d.createElement(\'script\'); js.id = id; js.async = true;\n                js.src = "//connect.facebook.net/en_US/all.js";\n                ref.parentNode.insertBefore(js, ref);\n            }(document));\n\n            function shareOnWall() {\n                // grab checked value of checkbox IF it\'s on the page. add to description.\n                //var shareChecked = $("#shareVote").is(\':checked\');\n                \n                var shareChecked = false;\n                var shareText = \'\';\n                var inputElements = document.getElementsByTagName(\'input\');\n                for(var i=0; inputElements[i]; ++i){\n                    //console.log("input class: "+inputElements[i].className)\n                    if(inputElements[i].className=="shareVote" && inputElements[i].checked) {\n                        //console.log("it\'s checked ")\n                        shareChecked = true;\n                        break;\n                    }\n                }\n                \n                if (shareChecked) {\n                    //console.log("share checked")\n                    // get the value of the voted button\n                    var linkElements = document.getElementsByTagName(\'a\');\n                    for(var j=0; linkElements[j]; ++j){\n                        //console.log(linkElements[j].className)\n                        if(linkElements[j].className=="voted yesVote" || linkElements[j].className=="yesVote voted"){\n                            //console.log("HURRAH!")\n                            shareText = \'I am in favor of this.\';\n                            break;\n                        } else if(linkElements[j].className=="noVote voted" || linkElements[j].className=="voted noVote") {\n                            //console.log("NAH AH!")\n                            shareText = \'I am not in favor of this.\';\n                            break;\n                        } else {\n                            shareText = \'I have not voted on this yet.\';\n                        }\n                    }\n                }\n                \n                FB.ui(\n                    {\n                      method: \'feed\',\n                      name: "')
            # SOURCE LINE 166
            __M_writer(escape(title))
            __M_writer(u'",\n                      link: "')
            # SOURCE LINE 167
            __M_writer(escape(link))
            __M_writer(u'",\n                      picture: "')
            # SOURCE LINE 168
            __M_writer(escape(image))
            __M_writer(u'",\n                      caption: shareText,\n                      description: "')
            # SOURCE LINE 170
            __M_writer(escape(description))
            __M_writer(u'"\n                    },\n                    function(response) \n                    {\n                        \n                        if (response && response.post_id) {\n                          // if there\'s a post_id, create share object\n                          var thingCode = "')
            # SOURCE LINE 177
            __M_writer(escape(thingCode))
            __M_writer(u'";\n                          var link = "')
            # SOURCE LINE 178
            __M_writer(escape(link))
            __M_writer(u'"\n                          var userCode = fbAuthId;\n                          var parentCode = "')
            # SOURCE LINE 180
            __M_writer(escape(parentCode))
            __M_writer(u'"\n                          \n                          //console.log(\'tc: \'+thingCode);\n                          //console.log(\'wc: \'+parentCode);\n\n                          result = postShared(response, thingCode, link, response.post_id, userCode, parentCode, \'facebook-wall\');\n                        }\n                    }\n                );\n            };\n\n            function messageFriends() {\n                // there is no callback for messages sent\n                // we can simply record that the message dialog was brought up\n                // grab checked value of checkbox IF it\'s on the page. add to description.\n                \n                var thingCode = "')
            # SOURCE LINE 196
            __M_writer(escape(thingCode))
            __M_writer(u'";\n                var link = "')
            # SOURCE LINE 197
            __M_writer(escape(link))
            __M_writer(u'";\n                var userCode = fbAuthId;\n                var parentCode = "')
            # SOURCE LINE 199
            __M_writer(escape(parentCode))
            __M_writer(u'";\n                \n                //console.log(\'tc mf: \'+thingCode);\n                //console.log(\'wc mf: \'+parentCode);\n                          \n                result = postShared("no response", thingCode, link, \'0\', userCode, parentCode, \'facebook-message\');\n                console.log("3");\n                FB.ui(\n                    {\n                      method: \'send\',\n                      name: "')
            # SOURCE LINE 209
            __M_writer(escape(title))
            __M_writer(u'",\n                      link: "')
            # SOURCE LINE 210
            __M_writer(escape(link))
            __M_writer(u'",\n                      picture: "')
            # SOURCE LINE 211
            __M_writer(escape(image))
            __M_writer(u'"\n                    }\n                );\n\n            };\n        \n        </script>\n        <div class="btn-group facebook">\n')
            # SOURCE LINE 219
            if 'btn' in kwargs:
                # SOURCE LINE 220
                __M_writer(u'            <a class="btn dropdown-toggle btn-primary" data-toggle="dropdown" href="#">\n              <i class="icon-facebook icon-light right-space"></i> | Share\n            </a>\n')
                # SOURCE LINE 223
            else:
                # SOURCE LINE 224
                __M_writer(u'            <a class="btn dropdown-toggle clear" data-toggle="dropdown" href="#">\n              <i class="icon-facebook-sign icon-2x"></i>\n            </a>\n')
                pass
            # SOURCE LINE 228
            __M_writer(u'          <ul class="dropdown-menu share-icons" style="margin-left: -50px;">\n            <li>\n')
            # SOURCE LINE 230
            if shareOnWall:
                # SOURCE LINE 231
                __M_writer(u'                <a href="#" target=\'_top\' onClick="shareOnWall()"><i class="icon-facebook-sign icon"></i> Post to Timeline</a>\n')
                pass
            # SOURCE LINE 233
            __M_writer(u'            </li>\n            <li>\n')
            # SOURCE LINE 235
            if sendMessage:
                # SOURCE LINE 236
                __M_writer(u'                  <a href="#" target=\'_top\' onClick="messageFriends()"><i class="icon-user"></i> Share with Friends</a>\n')
                pass
            # SOURCE LINE 238
            __M_writer(u'            </li>\n          </ul>\n        </div>\n        \n        \n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_unpublishThingLink(context,thing,**kwargs):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 1449
        __M_writer(u'\n    ')
        # SOURCE LINE 1450

        unpublishStr = '"/unpublish/%s/%s"' %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return unpublishStr
                    return 'href = ' + unpublishStr
                return 'href = ' + unpublishStr
        unpublishStr = 'href = ' + unpublishStr
            
        
        # SOURCE LINE 1460
        __M_writer(u'\n    ')
        # SOURCE LINE 1461
        __M_writer(unpublishStr )
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render__userImageSource(context,user,**kwargs):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 1117
        __M_writer(u'\n    ')
        # SOURCE LINE 1118

        # Assumes 'user' is a Thing.
        # Defaults to a gravatar source
        # kwargs:   forceSource:   Instead of returning a source based on the user-set preference in the profile editor,
        #                          we return a source based on the value given here (civ/gravatar)
        source = 'http://www.gravatar.com/avatar/%s?r=pg&d=identicon' % md5(user['email']).hexdigest()
        large = False
        gravatar = True
        
        if 'className' in kwargs:
            if 'avatar-large' in kwargs['className']:
                large = True
        if 'forceSource' in kwargs:
            if kwargs['forceSource'] == 'civ':
                gravatar = False
                if 'directoryNum_avatar' in user.keys() and 'pictureHash_avatar' in user.keys():
                    source = '/images/avatar/%s/avatar/%s.png' %(user['directoryNum_avatar'], user['pictureHash_avatar'])
                else:
                    source = '/images/hamilton.png'
            elif kwargs['forceSource'] == 'facebook':
                if large:
                    source = user['facebookProfileBig']
                else:
                    source = user['facebookProfileSmall']
            elif kwargs['forceSource'] == 'twitter':
                source = user['twitterProfilePic']
        
        else:
            if 'avatarSource' in user.keys():
                if user['avatarSource'] == 'civ':
                    if 'directoryNum_avatar' in user.keys() and 'pictureHash_avatar' in user.keys():
                        source = '/images/avatar/%s/avatar/%s.png' %(user['directoryNum_avatar'], user['pictureHash_avatar'])
                        gravatar = False
                elif user['avatarSource'] == 'facebook':
                    gravatar = False
                    if large:
                        source = user['facebookProfileBig']
                    else:
                        source = user['facebookProfileSmall']
                elif user['avatarSource'] == 'twitter':
                    gravatar = False
                    source = user['twitterProfilePic']
        
            elif 'extSource' in user.keys():
                # this is needed untl we're sure all facebook connected users have properly 
                # functioning profile pics - the logic here is now handled 
                # with the above user['avatarSource'] == 'facebook': ..
                if 'facebookSource' in user.keys():
                    if user['facebookSource'] == u'1':
                        gravatar = False
                        # NOTE - when to provide large or small link?
                        if large:
                            source = user['facebookProfileBig']
                        else:
                            source = user['facebookProfileSmall']
        if large and gravatar:
            source += '&s=200'
        return source
        
        
        # SOURCE LINE 1176
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_createNew(context,thing,*args):
    context.caller_stack._push_frame()
    try:
        def isReadOnly():
            return render_isReadOnly(context)
        def readOnlyMessage(thing):
            return render_readOnlyMessage(context,thing)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 723
        __M_writer(u'\n   ')
        # SOURCE LINE 724

        if isReadOnly():
            readOnlyMessage(thing)
            return
        if c.w['allowResources'] == '0' and thing == 'resources' and not (c.privs['admin'] or c.privs['facilitator']):
            return
        if c.w['allowIdeas'] == '0' and thing == 'ideas' and not (c.privs['admin'] or c.privs['facilitator']):
            return
        
        printStr = ''
        btnX = "large"
        if 'small' in args or 'tiny' in args:
            btnX = "small"
        
        if c.privs['provisional']:
            printStr = '<a href="#activateAccountModal" data-toggle="modal"'
              
        elif c.privs['participant'] or c.privs['facilitator'] or c.privs['admin'] or c.privs['guest']:     
            printStr = '<a id="addButton" href="/workshop/%s/%s/add/' %(c.w['urlCode'], c.w['url'])
        
        else:
            printStr = '<a href="#signupLoginModal" data-toggle="modal"'
            
        if thing == 'discussion':
            printStr += 'discussion" title="Click to add a general conversation topic to this workshop"'
        elif thing == 'resources':
            printStr += 'resource" title="Click to add a resource to this workshop"'
        elif thing == 'ideas':
            printStr += 'idea" title="Click to add an idea to this workshop"'
                
        printStr += ' class="pull-right btn btn-' + btnX + ' btn-civ right-space" type="button"><i class="icon-white icon-plus"></i>'
        
        if not 'tiny' in args:
          if thing == 'discussion':
              printStr += ' Topic'
          elif thing == 'ideas':
              printStr += ' Idea'
          elif thing == 'resources':
              printStr += ' Resource'
        
        printStr += '</a>'
        
            
        
        # SOURCE LINE 766
        __M_writer(u'\n\n    ')
        # SOURCE LINE 768
        __M_writer(printStr )
        __M_writer(u' \n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showPositions(context,thing):
    context.caller_stack._push_frame()
    try:
        def userImage(user,**kwargs):
            return render_userImage(context,user,**kwargs)
        __M_writer = context.writer()
        # SOURCE LINE 587
        __M_writer(u'\n    ')
        # SOURCE LINE 588
 
        pStr = ""
        positions = discussionLib.getPositionsForItem(thing)
            
        
        # SOURCE LINE 591
        __M_writer(u'\n')
        # SOURCE LINE 592
        for p in positions:
            # SOURCE LINE 593
            __M_writer(u'        ')
            org = userLib.getUserByID(p.owner) 
            
            __M_writer(u'\n        ')
            # SOURCE LINE 594
            __M_writer(escape(userImage(org, className="avatar small-avatar")))
            __M_writer(u'\n')
            # SOURCE LINE 595
            if p['position'] == 'support':
                # SOURCE LINE 596
                __M_writer(u'            ')
                pStr += '<a href="/profile/' + p['userCode'] + '/' + p['user_url'] + '">' + p['user_name'] + '</a> supports this initiative.</br>' 
                
                __M_writer(u'\n')
                # SOURCE LINE 597
            else:
                # SOURCE LINE 598
                __M_writer(u'            ')
                pStr += '<a href="/profile/' + p['userCode'] + '/' + p['user_url'] + '">' + p['user_name'] + '</a> opposes this initiative.</br>' 
                
                __M_writer(u'\n')
                pass
            pass
        # SOURCE LINE 601
        __M_writer(u'    ')
        __M_writer(pStr )
        __M_writer(u'                                \n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_immunifyThingLink(context,thing,**kwargs):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 1389
        __M_writer(u'\n    ')
        # SOURCE LINE 1390

        immunifyStr = '"/immunify/%s/%s"' %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return immunifyStr
                    return 'href = ' + immunifyStr
                return 'href = ' + immunifyStr
        immunifyStr = 'href = ' + immunifyStr
            
        
        # SOURCE LINE 1400
        __M_writer(u'\n    ')
        # SOURCE LINE 1401
        __M_writer(immunifyStr )
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_public_tag_filter(context):
    context.caller_stack._push_frame()
    try:
        sorted = context.get('sorted', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1872
        __M_writer(u'\n  ')
        # SOURCE LINE 1873
        categories = workshopLib.getWorkshopTagCategories() 
        
        __M_writer(u'\n  <select class="med-width" ng-model="query">\n      <option value=\'\'>All Tags</option>\n')
        # SOURCE LINE 1876
        for category in sorted(categories):
            # SOURCE LINE 1877
            __M_writer(u'      <option value="')
            __M_writer(escape(category))
            __M_writer(u'">')
            __M_writer(escape(category))
            __M_writer(u'</option>\n')
            pass
        # SOURCE LINE 1879
        __M_writer(u'  </select>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_yesNoVote(context,thing,*args):
    context.caller_stack._push_frame()
    try:
        def orgPosition(thing):
            return render_orgPosition(context,thing)
        int = context.get('int', UNDEFINED)
        c = context.get('c', UNDEFINED)
        float = context.get('float', UNDEFINED)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 623
        __M_writer(u'\n   <div class="yesNoWrapper">\n')
        # SOURCE LINE 625
        if thing['disabled'] == '1' or thing.objType == 'revision':
            # SOURCE LINE 626
            __M_writer(u'         </div> <!-- /.yesNoWrapper -->\n         ')
            # SOURCE LINE 627
            return 
            
            __M_writer(u'\n')
            pass
        # SOURCE LINE 629
        __M_writer(u'      ')
 
        rating = int(thing['ups']) - int(thing['downs']) 
        totalYes = int(thing['ups'])
        totalNo = int(thing['downs'])
        totalVotes = int(thing['ups']) + int(thing['downs'])
        percentYes = percentNo = 0
        if totalVotes > 0:
          percentYes = int(float(totalYes)/float(totalVotes) * 100)
          percentNo = int(float(totalNo)/float(totalVotes) * 100)
        if 'ratings' in session:
            myRatings = session["ratings"]
        else:
            myRatings = {}
              
        
        # SOURCE LINE 642
        __M_writer(u'\n')
        # SOURCE LINE 643
        if 'user' in session and (c.privs['participant'] or c.privs['provisional']) and not self.isReadOnly() and c.authuser['memberType'] == 'organization':
            # SOURCE LINE 644
            __M_writer(u'        ')
            __M_writer(escape(orgPosition(thing)))
            __M_writer(u'\n')
            # SOURCE LINE 645
        elif 'user' in session and (c.privs['participant'] or c.privs['facilitator'] or c.privs['admin'] or c.privs['provisional'])  and not self.isReadOnly():
            # SOURCE LINE 646
            __M_writer(u'         ')
 
            thingCode = thing['urlCode']
            #log.info("thingCode is %s"%thingCode)
            if thingCode in myRatings:
                myRating = myRatings[thingCode]
                log.info("thingCode %s myRating %s"%(thingCode, myRating))
            else:
                myRating = "0"
                
            if myRating == '1':
                commentClass = 'voted yesVote'
                displayTally = ''
                displayPrompt = 'hidden'
            else:
                commentClass = 'yesVote'
                displayTally = ''
                displayPrompt = 'hidden'
                if myRating == '0' :
                    displayTally = 'hidden'
                    displayPrompt = ''
            
            #else:
            #   commentClass = 'yesVote'
            #   displayTally = 'hidden'
            #   displayPrompt = ''
                     
            
            # SOURCE LINE 671
            __M_writer(u'\n         <a href="/rate/')
            # SOURCE LINE 672
            __M_writer(escape(thing.objType))
            __M_writer(u'/')
            __M_writer(escape(thing['urlCode']))
            __M_writer(u'/')
            __M_writer(escape(thing['url']))
            __M_writer(u'/1" class="')
            __M_writer(escape(commentClass))
            __M_writer(u'">\n              <div class="vote-icon yes-icon detail"></div>\n              <div class="ynScoreWrapper ')
            # SOURCE LINE 674
            __M_writer(escape(displayTally))
            __M_writer(u'"><span class="yesScore">')
            __M_writer(escape(percentYes))
            __M_writer(u'</span>%</div>\n         </a>\n         <br>\n         <br>\n         ')
            # SOURCE LINE 678

            if myRating == '-1':
                commentClass = 'voted noVote'
            else:
                commentClass = 'noVote'
                     
            
            # SOURCE LINE 683
            __M_writer(u'\n         <a href="/rate/')
            # SOURCE LINE 684
            __M_writer(escape(thing.objType))
            __M_writer(u'/')
            __M_writer(escape(thing['urlCode']))
            __M_writer(u'/')
            __M_writer(escape(thing['url']))
            __M_writer(u'/-1" class="')
            __M_writer(escape(commentClass))
            __M_writer(u'">\n              <div class="vote-icon no-icon detail"></div>\n              <div class="ynScoreWrapper ')
            # SOURCE LINE 686
            __M_writer(escape(displayTally))
            __M_writer(u'"><span class="noScore">')
            __M_writer(escape(percentNo))
            __M_writer(u'</span>%</div> \n         </a>\n         <br>\n         <div class="totalVotesWrapper">\n')
            # SOURCE LINE 690
            if 'detail' in args:
                # SOURCE LINE 691
                __M_writer(u'            <span class="orange ')
                __M_writer(escape(displayPrompt))
                __M_writer(u'"><strong>Vote to display rating</strong></span><br>\n')
                pass
            # SOURCE LINE 693
            __M_writer(u'          Total Votes: <span class="totalVotes">')
            __M_writer(escape(locale.format("%d", totalVotes, grouping=True)))
            __M_writer(u'</span>\n        </div>\n')
            # SOURCE LINE 695
        else:
            # SOURCE LINE 696
            __M_writer(u'         <a href="#signupLoginModal" role="button" data-toggle="modal" rel="tooltip" data-placement="top" data-trigger="hover" title="Login to vote" id="nulvote" class="nullvote">\n         <div class="vote-icon yes-icon"></div>\n         </a>\n         <br>\n         <br>\n         <a href="#signupLoginModal" role="button" data-toggle="modal" rel="tooltip" data-placement="top" data-trigger="hover" title="Login to vote" id="nulvote" class="nullvote">\n         <div class="vote-icon no-icon"></div>\n         </a>\n         <br>\n         <div class="totalVotesWrapper">\n')
            # SOURCE LINE 706
            if 'detail' in args:
                # SOURCE LINE 707
                __M_writer(u'            <span class="orange"><strong>Vote to display rating</strong></span><br>\n')
                pass
            # SOURCE LINE 709
            __M_writer(u'          Total Votes: <span class="totalVotes">')
            __M_writer(escape(locale.format("%d", totalVotes, grouping=True)))
            __M_writer(u'</span></div>\n')
            pass
        # SOURCE LINE 711
        __M_writer(u'   </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_listBookmarks(context,bookmarked,ltitle):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        homeHelpers = _mako_get_namespace(context, 'homeHelpers')
        def workshopImage(w,**kwargs):
            return render_workshopImage(context,w,**kwargs)
        def showScope(item):
            return render_showScope(context,item)
        def bookmarkOptions(user,workshop):
            return render_bookmarkOptions(context,user,workshop)
        def workshopLink(w,**kwargs):
            return render_workshopLink(context,w,**kwargs)
        __M_writer = context.writer()
        # SOURCE LINE 1930
        __M_writer(u'\n  <table class="table table-hover table-condensed no-bottom">\n')
        # SOURCE LINE 1932
        for item in bookmarked:
            # SOURCE LINE 1933
            __M_writer(u'      <tr>\n        <td>\n            <div class="media profile-workshop" style="overflow:visible;">\n                <a class="pull-left" ')
            # SOURCE LINE 1936
            __M_writer(escape(workshopLink(item)))
            __M_writer(u'>\n                  <div class="thumbnail tight media-object" style="height: 60px; width: 90px; margin-bottom: 5px; background-image:url(')
            # SOURCE LINE 1937
            __M_writer(workshopImage(item, raw=True) )
            __M_writer(u'); background-size: cover; background-position: center center;"></div>\n                </a>\n                <div class="media-body" style="overflow:visible;">\n                  <a ')
            # SOURCE LINE 1940
            __M_writer(escape(workshopLink(item)))
            __M_writer(u' class="listed-item-title media-heading lead bookmark-title">')
            __M_writer(escape(item['title']))
            __M_writer(u'</a>\n')
            # SOURCE LINE 1941
            if ltitle == 'Facilitating' or ltitle == 'Author' or userLib.isAdmin(c.authuser.id):
                # SOURCE LINE 1942
                __M_writer(u'                      <a class="btn pull-right" href="/workshop/')
                __M_writer(escape(item['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(item['url']))
                __M_writer(u'/preferences"><strong>Edit Workshop</strong></a> &nbsp;\n')
                # SOURCE LINE 1943
            else:
                # SOURCE LINE 1944
                if ltitle == 'Bookmarked':
                    # SOURCE LINE 1945
                    __M_writer(u'                        ')
                    __M_writer(escape(homeHelpers.watchButton(item, following = True)))
                    __M_writer(u'\n')
                    pass
                # SOURCE LINE 1947
                __M_writer(u'                      ')
                __M_writer(escape(bookmarkOptions(c.authuser, item)))
                __M_writer(u'\n')
                pass
            # SOURCE LINE 1949
            __M_writer(u'                    <br>\n')
            # SOURCE LINE 1950
            if item['public_private'] == 'public':
                # SOURCE LINE 1951
                __M_writer(u'                      <span class="grey">Workshop for</span> ')
                __M_writer(showScope(item) )
                __M_writer(u'\n')
                # SOURCE LINE 1952
            else:
                # SOURCE LINE 1953
                __M_writer(u'                      <span class="grey">Private Workshop</span>\n')
                pass
            # SOURCE LINE 1955
            __M_writer(u'                </div>\n            </div>\n        </td>\n      </tr>\n')
            pass
        # SOURCE LINE 1960
        __M_writer(u'  </table>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_unpublishThing(context,thing,**kwargs):
    context.caller_stack._push_frame()
    try:
        def unpublishThingLink(thing,**kwargs):
            return render_unpublishThingLink(context,thing,**kwargs)
        __M_writer = context.writer()
        # SOURCE LINE 1507
        __M_writer(u'\n    ')
        # SOURCE LINE 1508
        unpublishID = 'unpublish-%s' % thing['urlCode'] 
        
        __M_writer(u'\n    <div class="row-fluid collapse" id="')
        # SOURCE LINE 1509
        __M_writer(escape(unpublishID))
        __M_writer(u'">\n        <div class="span11 offset1 alert">\n            <strong>Are you sure you want to unpublish this ')
        # SOURCE LINE 1511
        __M_writer(escape(thing.objType))
        __M_writer(u'?</strong>\n            <br />\n            <a ')
        # SOURCE LINE 1513
        __M_writer(escape(unpublishThingLink(thing)))
        __M_writer(u' class="btn btn-danger">Yes</a>\n            <a class="btn accordion-toggle" data-toggle="collapse" data-target="#')
        # SOURCE LINE 1514
        __M_writer(escape(unpublishID))
        __M_writer(u'">No</a>\n            <span id = "unpublish_')
        # SOURCE LINE 1515
        __M_writer(escape(thing['urlCode']))
        __M_writer(u'"></span>\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_public_tags(context):
    context.caller_stack._push_frame()
    try:
        sorted = context.get('sorted', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1857
        __M_writer(u'\n  ')
        # SOURCE LINE 1858
        categories = workshopLib.getWorkshopTagCategories() 
        
        __M_writer(u'\n  <div class="btn-group pull-right left-space">\n    <button class="btn dropdown-toggle" data-toggle="dropdown">\n      Search by Tag\n      <span class="caret"></span>\n    </button>\n    <ul class="dropdown-menu">\n')
        # SOURCE LINE 1865
        for category in sorted(categories):
            # SOURCE LINE 1866
            __M_writer(u'            <li><a href="/searchTags/')
            __M_writer(escape(category.replace(" ", "_")))
            __M_writer(u'/" title="Click to view workshops with this tag">')
            __M_writer(escape(category.replace(" ", "_")))
            __M_writer(u'</a></li>\n')
            pass
        # SOURCE LINE 1868
        __M_writer(u'    </ul> <!-- /.unstyled -->\n  </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_flagThing(context,thing,**kwargs):
    context.caller_stack._push_frame()
    try:
        def flagThingLink(thing,**kwargs):
            return render_flagThingLink(context,thing,**kwargs)
        __M_writer = context.writer()
        # SOURCE LINE 1494
        __M_writer(u'\n    ')
        # SOURCE LINE 1495
        flagID = 'flag-%s' % thing['urlCode'] 
        
        __M_writer(u'\n    <div class="row-fluid collapse" id="')
        # SOURCE LINE 1496
        __M_writer(escape(flagID))
        __M_writer(u'">\n        <div class="span11 offset1 alert">\n            <strong>Are you sure you want to flag this ')
        # SOURCE LINE 1498
        __M_writer(escape(thing.objType))
        __M_writer(u'?</strong>\n            <br />\n            <a ')
        # SOURCE LINE 1500
        __M_writer(escape(flagThingLink(thing)))
        __M_writer(u' class="btn btn-danger flagCommentButton">Yes</a>\n            <a class="btn accordion-toggle" data-toggle="collapse" data-target="#')
        # SOURCE LINE 1501
        __M_writer(escape(flagID))
        __M_writer(u'">No</a>\n            <span id = "flagged_')
        # SOURCE LINE 1502
        __M_writer(escape(thing['urlCode']))
        __M_writer(u'"></span>\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_ideaLink(context,i,w,**kwargs):
    context.caller_stack._push_frame()
    try:
        def commentLinkAppender(**kwargs):
            return render_commentLinkAppender(context,**kwargs)
        __M_writer = context.writer()
        # SOURCE LINE 961
        __M_writer(u'\n   ')
        # SOURCE LINE 962

        if 'noHref' in kwargs:
            ideaStr = '/workshop/%s/%s/idea/%s/%s' %(w["urlCode"], w["url"], i["urlCode"], i["url"])
        else:
            ideaStr = 'href="/workshop/%s/%s/idea/%s/%s' %(w["urlCode"], w["url"], i["urlCode"], i["url"])
        ideaStr += commentLinkAppender(**kwargs)
        if 'noHref' in kwargs:
            ideaStr += ''
        else:
            ideaStr += '"'
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                return ideaStr
           
        
        # SOURCE LINE 975
        __M_writer(u'\n   ')
        # SOURCE LINE 976
        __M_writer(ideaStr )
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_discussionLink(context,d,p,**kwargs):
    context.caller_stack._push_frame()
    try:
        def commentLinkAppender(**kwargs):
            return render_commentLinkAppender(context,**kwargs)
        __M_writer = context.writer()
        # SOURCE LINE 979
        __M_writer(u'\n    ')
        # SOURCE LINE 980

        if 'workshopCode' in d:
            if 'noHref' in kwargs:
                discussionStr = '/workshop/%s/%s/discussion/%s/%s' %(p["urlCode"], p["url"], d["urlCode"], d["url"])
            else:
                discussionStr = 'href="/workshop/%s/%s/discussion/%s/%s' %(p["urlCode"], p["url"], d["urlCode"], d["url"])
            discussionStr += commentLinkAppender(**kwargs)
            if 'noHref' in kwargs:
                discussionStr += ''
            else:
                discussionStr += '"'
        elif 'initiativeCode' in d:
            if 'noHref' in kwargs:
                discussionStr = '/initiative/%s/%s/updateShow/%s'%(d['initiativeCode'], d['initiative_url'], d['urlCode'])
            else:
                discussionStr = 'href="/initiative/%s/%s/updateShow/%s"'%(d['initiativeCode'], d['initiative_url'], d['urlCode'])
        elif d['discType'] == 'organization_general':
            if 'noHref' in kwargs:
                discussionStr = '/profile/%s/%s/discussion/show/%s'%(d['userCode'], d['user_url'], d['urlCode'])
            else:
                discussionStr = 'href="/profile/%s/%s/discussion/show/%s"'%(d['userCode'], d['user_url'], d['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                return discussionStr
            
        
        # SOURCE LINE 1004
        __M_writer(u'\n    ')
        # SOURCE LINE 1005
        __M_writer(discussionStr )
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_publishThingLink(context,thing,**kwargs):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 1464
        __M_writer(u'\n    ')
        # SOURCE LINE 1465

        publishStr = '"/publish/%s/%s"' %(thing.objType.replace("Unpublish", ""), thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return publishStr
                    return 'href = ' + publishStr
                return 'href = ' + publishStr
        publishStr = 'href = ' + publishStr
            
        
        # SOURCE LINE 1475
        __M_writer(u'\n    ')
        # SOURCE LINE 1476
        __M_writer(publishStr )
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bookmarkOptions(context,user,workshop):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 1897
        __M_writer(u'\n  ')
        # SOURCE LINE 1898
        f = followLib.getFollow(user, workshop) 
        
        __M_writer(u'\n')
        # SOURCE LINE 1899
        if f:
            # SOURCE LINE 1900
            __M_writer(u'      ')

            itemsChecked = ''
            digestChecked = ''
            if 'itemAlerts' in f and f['itemAlerts'] == '1':
                itemsChecked = 'checked'
            if 'digest' in f and f['digest'] == '1':
                digestChecked = 'checked'
                  
            
            # SOURCE LINE 1907
            __M_writer(u'\n      <div class="btn-group pull-right" ng-controller="followerController" ng-init="code=\'')
            # SOURCE LINE 1908
            __M_writer(escape(workshop['urlCode']))
            __M_writer(u"'; url='")
            __M_writer(escape(workshop['url']))
            __M_writer(u"'; user='")
            __M_writer(escape(user['urlCode']))
            __M_writer(u'\'">\n        <a class="btn dropdown-toggle" data-toggle="dropdown" href="#">\n          <i class="icon-envelope"></i>\n          <span class="caret"></span>\n        </a>\n        <ul class="dropdown-menu bookmark-options">\n          <li>Email on:</li>\n          <li>\n            <label class="checkbox">\n              <input type="checkbox" name="itemAlerts" value="items" ng-click="emailOnAdded()" ')
            # SOURCE LINE 1917
            __M_writer(escape(itemsChecked))
            __M_writer(u'> New Items\n            </label>\n          </li>\n          <li>\n            <label class="checkbox">\n              <input type="checkbox" name="digest" value="items" ng-click="emailDigest()" ')
            # SOURCE LINE 1922
            __M_writer(escape(digestChecked))
            __M_writer(u'> Daily Digest\n            </label>\n          </li>\n        </ul>\n      </div>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_flagThingLink(context,thing,**kwargs):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 1434
        __M_writer(u'\n    ')
        # SOURCE LINE 1435

        flagStr = '"/flag/%s/%s"' %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return flagStr
                    return 'href = ' + flagStr
                return 'href = ' + flagStr
        flagStr = 'href = ' + flagStr
            
        
        # SOURCE LINE 1445
        __M_writer(u'\n    ')
        # SOURCE LINE 1446
        __M_writer(flagStr )
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_userImage(context,user,**kwargs):
    context.caller_stack._push_frame()
    try:
        type = context.get('type', UNDEFINED)
        def userLink(user,**kwargs):
            return render_userLink(context,user,**kwargs)
        def _userImageSource(user,**kwargs):
            return render__userImageSource(context,user,**kwargs)
        __M_writer = context.writer()
        # SOURCE LINE 1078
        __M_writer(u'\n   ')
        # SOURCE LINE 1079

        if type(user) == type(1L):
           user = userLib.getUserByID(user)
        imgStr = ''
        if user.objType == 'facilitator':
           user = userLib.getUserByID(user.owner)
        if user.objType == 'listener':
           user = userLib.getUserByEmail(user['email'])
        imgStr += '<a href="'
        imgStr += userLink(user, raw=True)
        imgStr += '"'
        if 'linkClass' in kwargs:
           imgStr += ' class="%s"' %(kwargs['linkClass'])
        if 'rel' in kwargs:
           imgStr += ' rel="%s"' %(kwargs['rel'])
        imgStr += '>'
        if 'revision' in kwargs:
           revision = kwargs['revision']
           title = revision['data']
        else:
           title = user['name']
              
        imageSource = _userImageSource(user, **kwargs)
        imgStr += '<img src="%s" alt="%s" title="%s"' %(imageSource, title, title)
        if 'className' in kwargs:
           imgStr += ' class="%s"' % kwargs['className']
        if 'placement' in kwargs:
           imgStr += ' data-placement="%s"' % kwargs['placement']
        
        imgStr += '></a>'
           
        
        # SOURCE LINE 1109
        __M_writer(u'\n')
        # SOURCE LINE 1110
        if 'noLink' in kwargs:
            # SOURCE LINE 1111
            __M_writer(u'      <img src="')
            __M_writer(escape(_userImageSource(user, **kwargs)))
            __M_writer(u'" class="')
            __M_writer(escape(kwargs['className']))
            __M_writer(u'" alt="')
            __M_writer(escape(title))
            __M_writer(u'" title="')
            __M_writer(escape(title))
            __M_writer(u'">\n')
            # SOURCE LINE 1112
        else:
            # SOURCE LINE 1113
            __M_writer(u'    ')
            __M_writer(imgStr )
            __M_writer(u'\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_initiativeLink(context,initiative,**kwargs):
    context.caller_stack._push_frame()
    try:
        def commentLinkAppender(**kwargs):
            return render_commentLinkAppender(context,**kwargs)
        __M_writer = context.writer()
        # SOURCE LINE 939
        __M_writer(u'\n   ')
        # SOURCE LINE 940

        if 'noHref' in kwargs:
            initiativeStr = '/initiative/%s/%s/show' %(initiative["urlCode"], initiative["url"])
            if 'fullURL' in kwargs:
              baseURL = utilsLib.getBaseUrl()
              initiativeStr = '%s/initiative/%s/%s/show' %(baseURL, initiative["urlCode"], initiative["url"])
        
        else:
            initiativeStr = 'href="/initiative/%s/%s/show' %(initiative["urlCode"], initiative["url"])
        initiativeStr += commentLinkAppender(**kwargs)
        if 'noHref' in kwargs:
            initiativeStr += ''
        else:
            initiativeStr += '"'
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                return initiativeStr
           
        
        # SOURCE LINE 957
        __M_writer(u'\n   ')
        # SOURCE LINE 958
        __M_writer(initiativeStr )
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_workshopImage(context,w,**kwargs):
    context.caller_stack._push_frame()
    try:
        def workshopLink(w,**kwargs):
            return render_workshopLink(context,w,**kwargs)
        __M_writer = context.writer()
        # SOURCE LINE 836
        __M_writer(u'\n    ')
        # SOURCE LINE 837

        mainImage = mainImageLib.getMainImage(w)
        if 'raw' in kwargs:
           if kwargs['raw'] == True:
              if mainImage['pictureHash'] == 'supDawg':
                 return "/images/slide/thumbnail/supDawg.thumbnail"
              elif 'format' in mainImage.keys():
                  return "/images/mainImage/%s/thumbnail/%s.%s" %(mainImage['directoryNum'], mainImage['pictureHash'], mainImage['format'])
              else:
                 return "/images/mainImage/%s/thumbnail/%s.jpg" %(mainImage['directoryNum'], mainImage['pictureHash'])
                 
        imgStr = '<a href="'
        imgStr += workshopLink(w, embed=True, raw=True)
        if 'linkClass' in kwargs:
           imgStr += '" class="%s"' %(kwargs['linkClass'])
        imgStr += '">'
        if mainImage['pictureHash'] == 'supDawg':
           picturePath = "/images/slide/thumbnail/supDawg.thumbnail"
        elif 'format' in mainImage.keys():
           picturePath = "/images/mainImage/%s/thumbnail/%s.%s" %(mainImage['directoryNum'], mainImage['pictureHash'], mainImage['format'])
        else:
           picturePath = "/images/mainImage/%s/thumbnail/%s.jpg" %(mainImage['directoryNum'], mainImage['pictureHash'])
        title = w['title']
        imgStr += '<img src="%s" alt="%s" title="%s"' %(picturePath, title, title)
           
        if 'className' in kwargs:
           imgStr += ' class="%s"' % kwargs['className']
        
        imgStr += '></a>'
           
        
        # SOURCE LINE 866
        __M_writer(u'\n   ')
        # SOURCE LINE 867
        __M_writer(imgStr )
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_public_tag_list_filter(context):
    context.caller_stack._push_frame()
    try:
        sorted = context.get('sorted', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1882
        __M_writer(u'\n  ')
        # SOURCE LINE 1883
        categories = workshopLib.getWorkshopTagCategories() 
        
        __M_writer(u'\n      <li ng-class="{active: query == \'\'}"><a href="" ng-click="query = \'\' ">All Categories</a></li>\n')
        # SOURCE LINE 1885
        for category in sorted(categories):
            # SOURCE LINE 1886
            __M_writer(u'      <li ng-class="{active: query == \'')
            __M_writer(escape(category))
            __M_writer(u'\'}"><a href="#" ng-click="query = \'')
            __M_writer(escape(category))
            __M_writer(u'\' ">')
            __M_writer(escape(category))
            __M_writer(u'</a></li>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_validateSession(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 516
        __M_writer(u'\n   ')
        # SOURCE LINE 517

        if 'user' in session:
           if not c.authuser:
              session.delete()
           
        
        # SOURCE LINE 521
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_outOfScope(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1301
        __M_writer(u'\n    ')
        # SOURCE LINE 1302

        scopeName = c.scope['level']
        
        # More mapping for the postal code, this time to display Postal Code instead of just Postal.
        # The real fix for this is through use of message catalogs, which we will need to implement
        # when we support multiple languages in the interface, so for right now this kludge is
        # "good enough" 
        if scopeName == 'postalCode':
            scopeName = 'Postal Code'
        
        scopeName += " of "
        scopeName += c.scope['name']\
                        .replace('-', ' ')\
                        .title()
            
        
        # SOURCE LINE 1316
        __M_writer(u'\n    <div class="alert alert-info span6 offset3">\n        <button type="button" class="close" data-dismiss="alert">x</button>\n        This page is scoped for the ')
        # SOURCE LINE 1319
        __M_writer(escape(scopeName))
        __M_writer(u'\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_formattingGuide(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 1963
        __M_writer(u'\n  <a href="#" class="btn btn-mini btn-info" onclick="window.open(\'/help/markdown.html\',\'popUpWindow\',\'height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes\');"><i class="icon-picture"></i> <i class="icon-list"></i> View Formatting Guide</a></label>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_photoLink(context,photo,dparent,**kwargs):
    context.caller_stack._push_frame()
    try:
        def commentLinkAppender(**kwargs):
            return render_commentLinkAppender(context,**kwargs)
        __M_writer = context.writer()
        # SOURCE LINE 922
        __M_writer(u'\n   ')
        # SOURCE LINE 923

        photoStr = 'href="/profile/%s/%s/photo/show/%s' %(dparent["urlCode"], dparent["url"], photo["urlCode"])
        
        photoStr += commentLinkAppender(**kwargs)
        if 'noHref' in kwargs:
            photoStr += ''
        else:
            photoStr += '"'
        
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                return photoStr
           
        
        # SOURCE LINE 935
        __M_writer(u'\n   ')
        # SOURCE LINE 936
        __M_writer(photoStr )
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_facebookDialogShare(context,link,picture,**kwargs):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 246
        __M_writer(u'\n    ')
        # SOURCE LINE 247

        # link: direct url to item being shared
        # picture: url of the parent workshop's background image
        facebookAppId = c.facebookAppId
        channelUrl = c.channelUrl
        thingCode = c.thingCode
        if not thingCode:
          thingCode = 'noCode'
        
        userCode = ''
        if c.w:
            if 'urlCode' in c.w.keys():
                workshopCode = c.w['urlCode']
            else:
                workshopCode = 'noCode'
        else:
            workshopCode = 'noCode'
        # in order to prevent the javascript for these buttons from being included multiple
        # times, these kwargs are now used to activate either or both of the buttons
        if 'shareOnWall' in kwargs:
            if kwargs['shareOnWall'] is True:
                shareOnWall = True
            else:
                shareOnWall = False
        else:
            shareOnWall = False
        
        if 'sendMessage' in kwargs:
            if kwargs['sendMessage'] is True:
                sendMessage = True
            else:
                sendMessage = False
        else:
            sendMessage = False
        
        
        # name: the workshop's name or the item's title. This ends up as the name of the object being shared on facebook.
        if 'title' in kwargs:
          name = kwargs['title']
        else:
          name = c.name
        
        if 'description' in kwargs:
          description = kwargs['description']
        else:
          description = "Civinomics is an Open Intelligence platform. Collaborate to create solutions."
        
        # this is an elaborate way to get the item or workshop's description loaded as the caption
        if c.thing:
            if 'text' in c.thing.keys():
                caption = c.thing['text']
            else:
                if c.w:
                    if 'description' in c.w.keys():
                        caption = c.w['description'].replace("'", "\\'")
                    else:
                        caption = ''
                else:
                    caption = ''
        else:
            if 'description' in c.w.keys():
                caption = c.w['description'].replace("'", "\\'")
            else:
                caption = ''
        
        shareOk = False
        if 'photoShare' in kwargs:
            if kwargs['photoShare'] == True:
                shareOk = True
        if c.w:
            if workshopLib.isPublished(c.w) and workshopLib.isPublic(c.w):
                shareOk = True
        if c.initiative:
            if c.initiative['public'] == '1':
                shareOk = True
            
        
        # SOURCE LINE 322
        __M_writer(u'\n')
        # SOURCE LINE 323
        if shareOk:
            # SOURCE LINE 324
            __M_writer(u'        <div id="fb-root"></div>\n        <script src="/js/extauth.js" type="text/javascript"></script>\n        <script>\n            // activate facebook javascript sdk\n            var fbAuthId = \'\';\n            window.fbAsyncInit = function() {\n                FB.init({\n                    appId      : "')
            # SOURCE LINE 331
            __M_writer(escape(facebookAppId))
            __M_writer(u'", // App ID\n                    channelUrl : "')
            # SOURCE LINE 332
            __M_writer(escape(channelUrl))
            __M_writer(u'", // Channel File\n                    status     : true, // check login status\n                    cookie     : false, // enable cookies to allow the server to access the session\n                    xfbml      : true  // parse XFBML\n                });\n                FB.Event.subscribe(\'auth.authResponseChange\', function(response) {\n                // Here we specify what we do with the response anytime this event occurs.\n                console.log(\'above response tree\');\n                if (response.status === \'connected\') {\n                    console.log(\'calling fb connected\');\n                    fbAuthId = response.authResponse.userID;\n                } else if (response.status === \'not_authorized\') {\n                    console.log(\'not authd\');                \n                    //FB.login();\n                } else {\n                    console.log(\'else\');\n                    //FB.login();\n                }\n                });\n            };\n        \n            // Load the SDK asynchronously\n            (function(d){\n                var js, id = \'facebook-jssdk\', ref = d.getElementsByTagName(\'script\')[0];\n                if (d.getElementById(id)) {return;}\n                js = d.createElement(\'script\'); js.id = id; js.async = true;\n                js.src = "//connect.facebook.net/en_US/all.js";\n                ref.parentNode.insertBefore(js, ref);\n            }(document));\n\n            function shareOnWall() {\n                // grab checked value of checkbox IF it\'s on the page. add to description.\n                //var shareChecked = $("#shareVote").is(\':checked\');\n                var shareChecked = false;\n                var shareText = \'\';\n                var inputElements = document.getElementsByTagName(\'input\');\n                for(var i=0; inputElements[i]; ++i){\n                    //console.log("input class: "+inputElements[i].className)\n                    if(inputElements[i].className=="shareVote" && inputElements[i].checked) {\n                        //console.log("it\'s checked ")\n                        shareChecked = true;\n                        break;\n                    }\n                }\n                \n                if (shareChecked) {\n                    //console.log("share checked")\n                    // get the value of the voted button\n                    var linkElements = document.getElementsByTagName(\'a\');\n                    for(var j=0; linkElements[j]; ++j){\n                        //console.log(linkElements[j].className)\n                        if(linkElements[j].className=="voted yesVote" || linkElements[j].className=="yesVote voted"){\n                            //console.log("HURRAH!")\n                            shareText = \'I am in favor of this.\';\n                            break;\n                        } else if(linkElements[j].className=="noVote voted" || linkElements[j].className=="voted noVote") {\n                            //console.log("NAH AH!")\n                            shareText = \'I am not in favor of this.\';\n                            break;\n                        } else {\n                            shareText = \'I have not voted on this yet.\';\n                        }\n                    }\n                }\n\n                FB.ui(\n                    {\n                      method: \'feed\',\n                      name: "')
            # SOURCE LINE 400
            __M_writer(escape(name))
            __M_writer(u'",\n                      link: "')
            # SOURCE LINE 401
            __M_writer(escape(link))
            __M_writer(u'",\n                      picture: "')
            # SOURCE LINE 402
            __M_writer(escape(picture))
            __M_writer(u'",\n                      caption: shareText,\n                      description: "')
            # SOURCE LINE 404
            __M_writer(escape(description))
            __M_writer(u'"\n                    },\n                    function(response) \n                    {\n                        if (response && response.post_id) {\n                          // if there\'s a post_id, create share object\n                          var thingCode = "')
            # SOURCE LINE 410
            __M_writer(escape(thingCode))
            __M_writer(u'";\n                          var link = "')
            # SOURCE LINE 411
            __M_writer(escape(link))
            __M_writer(u'"\n                          var userCode = fbAuthId;\n                          var workshopCode = "')
            # SOURCE LINE 413
            __M_writer(escape(workshopCode))
            __M_writer(u'"\n                          \n                          //console.log(\'tc: \'+thingCode);\n                          //console.log(\'wc: \'+workshopCode);\n\n                          result = postShared(response, thingCode, link, response.post_id, userCode, workshopCode, \'facebook-wall\');\n                        }\n                    }\n                );\n            };\n\n            function messageFriends() {\n                // there is no callback for messages sent\n                // we can simply record that the message dialog was brought up\n                // grab checked value of checkbox IF it\'s on the page. add to description.\n                var thingCode = "')
            # SOURCE LINE 428
            __M_writer(escape(thingCode))
            __M_writer(u'";\n                var link = "')
            # SOURCE LINE 429
            __M_writer(escape(link))
            __M_writer(u'"\n                var userCode = fbAuthId;\n                var workshopCode = "')
            # SOURCE LINE 431
            __M_writer(escape(workshopCode))
            __M_writer(u'"\n                \n                //console.log(\'tc mf: \'+thingCode);\n                //console.log(\'wc mf: \'+workshopCode);\n                          \n                result = postShared("no response", thingCode, link, \'0\', userCode, workshopCode, \'facebook-message\');\n                FB.ui(\n                    {\n                      method: \'send\',\n                      name: "')
            # SOURCE LINE 440
            __M_writer(escape(name))
            __M_writer(u'",\n                      link: "')
            # SOURCE LINE 441
            __M_writer(escape(link))
            __M_writer(u'",\n                      picture: "')
            # SOURCE LINE 442
            __M_writer(escape(picture))
            __M_writer(u'"\n                      //description: \'Civinomics is an Open Intelligence platform. Collaborate to create the solutions you need.\'\n                    }\n                );\n            };\n        \n        </script>\n        <div class="btn-group facebook">\n')
            # SOURCE LINE 450
            if 'btn' in kwargs:
                # SOURCE LINE 451
                __M_writer(u'            <a class="btn dropdown-toggle btn-primary" data-toggle="dropdown" href="#">\n              <i class="icon-facebook icon-light right-space"></i> | Share\n            </a>\n')
                # SOURCE LINE 454
            else:
                # SOURCE LINE 455
                __M_writer(u'            <a class="btn dropdown-toggle clear" data-toggle="dropdown" href="#">\n              <i class="icon-facebook-sign icon-2x"></i>\n            </a>\n')
                pass
            # SOURCE LINE 459
            __M_writer(u'          <ul class="dropdown-menu share-icons" style="margin-left: -50px;">\n            <li>\n')
            # SOURCE LINE 461
            if shareOnWall:
                # SOURCE LINE 462
                __M_writer(u'                <a href="#" target=\'_top\' onClick="shareOnWall()"><i class="icon-facebook-sign icon"></i> Post to Timeline</a>\n')
                pass
            # SOURCE LINE 464
            __M_writer(u'            </li>\n            <li>\n')
            # SOURCE LINE 466
            if sendMessage:
                # SOURCE LINE 467
                __M_writer(u'                  <a href="#" target=\'_top\' onClick="messageFriends()"><i class="icon-user"></i> Share with Friends</a>\n')
                pass
            # SOURCE LINE 469
            __M_writer(u'            </li>\n          </ul>\n        </div>\n        \n        \n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_commentLinkAppender(context,**kwargs):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 870
        __M_writer(u'\n')
        # SOURCE LINE 872
        __M_writer(u'    ')

        appendedLink = ''
        if 'id' not in kwargs and 'commentCode' not in kwargs:
            return appendedLink
        if 'id' in kwargs:
            appendedLink = '#%s' % kwargs['id']
        elif 'commentCode' in kwargs:
            appendedLink = '?comment=%s' % kwargs['commentCode']
        return appendedLink
            
        
        # SOURCE LINE 881
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_commentLink(context,comment,dparent,**kwargs):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 1008
        __M_writer(u'\n   ')
        # SOURCE LINE 1009
 
        if dparent.objType.replace("Unpublished", "") == 'workshop':
            parentBase = 'workshop'
            commentSuffix = "/comment/%s"%comment['urlCode']
        elif dparent.objType.replace("Unpublished", "") == 'user':
            parentBase = 'profile'
        elif dparent.objType.replace("Unpublished", "") == 'initiative':
            parentBase = 'initiative'
            
        if 'noHref' in kwargs:
            linkStr = '/%s/%s/%s/comment/%s' %(parentBase, dparent["urlCode"], dparent["url"], comment["urlCode"])
        else:
            linkStr = 'href="/%s/%s/%s/comment/%s"' %(parentBase, dparent["urlCode"], dparent["url"], comment["urlCode"])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                return linkStr
           
        
        # SOURCE LINE 1025
        __M_writer(u'\n   ')
        # SOURCE LINE 1026
        __M_writer(linkStr )
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showTags(context,item):
    context.caller_stack._push_frame()
    try:
        KeyError = context.get('KeyError', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1967
        __M_writer(u'\n    ')
        # SOURCE LINE 1968
 
        colors = workshopLib.getWorkshopTagColouring()
        try:
          tagList = item['tags'].split('|')
        except KeyError:
          tagList = item['workshop_category_tags'].split('|')
        tagList = tagList[:3]
            
        
        # SOURCE LINE 1975
        __M_writer(u'\n')
        # SOURCE LINE 1976
        for tag in tagList:
            # SOURCE LINE 1977
            if tag and tag != '':
                # SOURCE LINE 1978
                __M_writer(u'              ')
 
                tagClass = colors[tag] 
                tagValue = tag.replace(" ", "_")
                              
                
                # SOURCE LINE 1981
                __M_writer(u'\n              <a class="label workshop-tag ')
                # SOURCE LINE 1982
                __M_writer(escape(tagClass))
                __M_writer(u'" href="/searchTags/')
                __M_writer(escape(tagValue))
                __M_writer(u'/" >')
                __M_writer(escape(tag))
                __M_writer(u'</a>\n')
                pass
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_geoButton(context,scopeMapping):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1254
        __M_writer(u'\n  <div class="btn-group pull-right left-space">\n        <button class="btn dropdown-toggle" data-toggle="dropdown">\n          Search by Region\n          <span class="caret"></span>\n        </button>\n        <ul class="dropdown-menu">\n')
        # SOURCE LINE 1261
        for scopeLevel in scopeMapping:
            # SOURCE LINE 1262
            __M_writer(u'              ')

            activeClass = ''
                
            if c.scope['level'] == scopeLevel[0]:
                if scopeLevel[0] != 'earth':
                    scopeKey = '%sURL' % scopeLevel[0] 
                    userScope = c.authuser_geo[scopeKey]
                else:
                    userScope = 'earth'
                if c.scope['name'] == userScope:
                    activeClass = 'active'
                else:
                    outOfScope = True
                          
            
            # SOURCE LINE 1275
            __M_writer(u'\n              <li class="')
            # SOURCE LINE 1276
            __M_writer(escape(activeClass))
            __M_writer(u'">\n                  <a ')
            # SOURCE LINE 1277
            __M_writer(self._geoWorkshopLink(c.authuser_geo, depth = scopeLevel[0]) )
            __M_writer(u'>')
            __M_writer(escape(scopeLevel[1]))
            __M_writer(u'</a>\n              </li>\n')
            pass
        # SOURCE LINE 1280
        __M_writer(u'        </ul>\n      </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_publishThing(context,thing,**kwargs):
    context.caller_stack._push_frame()
    try:
        def publishThingLink(thing,**kwargs):
            return render_publishThingLink(context,thing,**kwargs)
        __M_writer = context.writer()
        # SOURCE LINE 1520
        __M_writer(u'\n    ')
        # SOURCE LINE 1521
        publishID = 'publish-%s' % thing['urlCode'] 
        
        __M_writer(u'\n    <div class="row-fluid collapse" id="')
        # SOURCE LINE 1522
        __M_writer(escape(publishID))
        __M_writer(u'">\n        <div class="span11 offset1 alert">\n            <strong>Are you sure you want to publish this ')
        # SOURCE LINE 1524
        __M_writer(escape(thing.objType.replace("Unpublished", "")))
        __M_writer(u'?</strong>\n            <br />\n            <a ')
        # SOURCE LINE 1526
        __M_writer(escape(publishThingLink(thing)))
        __M_writer(u' class="btn btn-danger">Yes</a>\n            <a class="btn accordion-toggle" data-toggle="collapse" data-target="#')
        # SOURCE LINE 1527
        __M_writer(escape(publishID))
        __M_writer(u'">No</a>\n            <span id = "publish_')
        # SOURCE LINE 1528
        __M_writer(escape(thing['urlCode']))
        __M_writer(u'"></span>\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_editThingLink(context,thing,**kwargs):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 1479
        __M_writer(u'\n    ')
        # SOURCE LINE 1480

        editStr = "/edit/%s/%s" %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return editStr
                    return 'href = ' + editStr
                return 'href = ' + editStr
        editStr = 'href = ' + editStr
            
        
        # SOURCE LINE 1490
        __M_writer(u'\n    ')
        # SOURCE LINE 1491
        __M_writer(editStr )
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_public_tag_links(context):
    context.caller_stack._push_frame()
    try:
        sorted = context.get('sorted', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1890
        __M_writer(u'\n  ')
        # SOURCE LINE 1891
        categories = workshopLib.getWorkshopTagCategories() 
        
        __M_writer(u'\n')
        # SOURCE LINE 1892
        for category in sorted(categories):
            # SOURCE LINE 1893
            __M_writer(u'      <a href="/searchTags/')
            __M_writer(escape(category))
            __M_writer(u'">')
            __M_writer(escape(category))
            __M_writer(u'</a><br>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_upDownVote(context,thing):
    context.caller_stack._push_frame()
    try:
        int = context.get('int', UNDEFINED)
        c = context.get('c', UNDEFINED)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 524
        __M_writer(u'\n   <div class="voteWrapper">\n')
        # SOURCE LINE 526
        if thing['disabled'] == '1' or thing.objType == 'revision':
            # SOURCE LINE 527
            __M_writer(u'         </div> <!-- /.voteWrapper -->\n         ')
            # SOURCE LINE 528
            return 
            
            __M_writer(u'\n')
            pass
        # SOURCE LINE 530
        __M_writer(u'      ')
        rating = int(thing['ups']) - int(thing['downs']) 
        
        __M_writer(u'\n')
        # SOURCE LINE 531
        if 'user' in session and (c.privs['participant'] or c.privs['facilitator'] or c.privs['admin'] or c.privs['provisional'])  and not self.isReadOnly():
            # SOURCE LINE 532
            __M_writer(u'         ')
 
            rated = ratingLib.getRatingForThing(c.authuser, thing) 
            if rated:
               if rated['amount'] == '1':
                  commentClass = 'voted upVote'
                  voteClass = 'icon-chevron-sign-up icon-2x voted'
               else:
                  commentClass = 'upVote'
                  voteClass = 'icon-chevron-sign-up icon-2x'
            else:
               commentClass = 'upVote'
               voteClass = 'icon-chevron-sign-up icon-2x'
                     
            
            # SOURCE LINE 544
            __M_writer(u'\n')
            # SOURCE LINE 545
            if thing.objType != 'comment':
                # SOURCE LINE 546
                __M_writer(u'            <a href="/rate/')
                __M_writer(escape(thing.objType))
                __M_writer(u'/')
                __M_writer(escape(thing['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(thing['url']))
                __M_writer(u'/1" class="')
                __M_writer(escape(commentClass))
                __M_writer(u'">\n')
                # SOURCE LINE 547
            else:
                # SOURCE LINE 548
                __M_writer(u'            <a href="/rate/')
                __M_writer(escape(thing.objType))
                __M_writer(u'/')
                __M_writer(escape(thing['urlCode']))
                __M_writer(u'/1" class="')
                __M_writer(escape(commentClass))
                __M_writer(u'">\n')
                pass
            # SOURCE LINE 550
            __M_writer(u'         <i class="')
            __M_writer(escape(voteClass))
            __M_writer(u'"></i>\n         </a>\n         <br />\n         <div class="centered chevron-score"> ')
            # SOURCE LINE 553
            __M_writer(escape(rating))
            __M_writer(u'</div>\n         ')
            # SOURCE LINE 554

            if rated:
               if rated['amount'] == '-1':
                  commentClass = 'voted downVote'
                  voteClass = 'icon-chevron-sign-down icon-2x voted'
               else:
                  commentClass = 'downVote'
                  voteClass = 'icon-chevron-sign-down icon-2x'
            else:
               commentClass = 'downVote'
               voteClass = 'icon-chevron-sign-down icon-2x'
                     
            
            # SOURCE LINE 565
            __M_writer(u'\n')
            # SOURCE LINE 566
            if thing.objType != 'comment':
                # SOURCE LINE 567
                __M_writer(u'            <a href="/rate/')
                __M_writer(escape(thing.objType))
                __M_writer(u'/')
                __M_writer(escape(thing['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(thing['url']))
                __M_writer(u'/-1" class="')
                __M_writer(escape(commentClass))
                __M_writer(u'">\n')
                # SOURCE LINE 568
            else:
                # SOURCE LINE 569
                __M_writer(u'            <a href="/rate/')
                __M_writer(escape(thing.objType))
                __M_writer(u'/')
                __M_writer(escape(thing['urlCode']))
                __M_writer(u'/-1" class="')
                __M_writer(escape(commentClass))
                __M_writer(u'">\n')
                pass
            # SOURCE LINE 571
            __M_writer(u'         <i class="')
            __M_writer(escape(voteClass))
            __M_writer(u'"></i>\n         </a>\n')
            # SOURCE LINE 573
        else:
            # SOURCE LINE 574
            __M_writer(u'         <a href="#signupLoginModal" data-toggle=\'modal\' rel="tooltip" data-placement="right" data-trigger="hover" title="Login to make your vote count" id="nullvote" class="nullvote">\n         <i class="icon-chevron-sign-up icon-2x"></i>\n         </a>\n         <br />\n         <div class="centered chevron-score"> ')
            # SOURCE LINE 578
            __M_writer(escape(rating))
            __M_writer(u'</div>\n         <a href="#signupLoginModal" data-toggle=\'modal\' rel="tooltip" data-placement="right" data-trigger="hover" title="Login to make your vote count" id="nullvote" class="nullvote">\n         <i class="icon-chevron-sign-down icon-2x"></i>\n         </a>\n         <br />\n')
            pass
        # SOURCE LINE 584
        __M_writer(u'   </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_disableThingLink(context,thing,**kwargs):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 1359
        __M_writer(u'\n    ')
        # SOURCE LINE 1360

        disableStr = '"/disable/%s/%s"' %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return disableStr
                    return 'href = ' + disableStr
                return 'href = ' + disableStr
        disableStr = 'href = ' + disableStr
            
        
        # SOURCE LINE 1370
        __M_writer(u'\n    ')
        # SOURCE LINE 1371
        __M_writer(disableStr )
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_emailShare(context,itemURL,itemCode):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 477
        __M_writer(u'\n')
        # SOURCE LINE 478
        if ('user' in session and c.authuser) and (workshopLib.isPublished(c.w) and workshopLib.isPublic(c.w) and not c.privs['provisional']):
            # SOURCE LINE 479
            __M_writer(u'        ')
 
            memberMessage = "You might be interested in this online Civinomics workshop."
                    
            
            # SOURCE LINE 481
            __M_writer(u'\n        <a href="#emailShare')
            # SOURCE LINE 482
            __M_writer(escape(itemCode))
            __M_writer(u'" role="button" data-toggle="modal" class="listed-item-title"><i class="icon-envelope icon-2x"></i></a>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_thingLinkRouter(context,thing,dparent,**kwargs):
    context.caller_stack._push_frame()
    try:
        def initiativeLink(initiative,**kwargs):
            return render_initiativeLink(context,initiative,**kwargs)
        def resourceLink(r,p,**kwargs):
            return render_resourceLink(context,r,p,**kwargs)
        def photoLink(photo,dparent,**kwargs):
            return render_photoLink(context,photo,dparent,**kwargs)
        def commentLink(comment,dparent,**kwargs):
            return render_commentLink(context,comment,dparent,**kwargs)
        def ideaLink(i,w,**kwargs):
            return render_ideaLink(context,i,w,**kwargs)
        def discussionLink(d,p,**kwargs):
            return render_discussionLink(context,d,p,**kwargs)
        __M_writer = context.writer()
        # SOURCE LINE 1029
        __M_writer(u'\n    ')
        # SOURCE LINE 1030

        if thing.objType == 'revision':
            objType = thing['objType'].replace("Unpublished", "")
        else:
            objType = thing.objType.replace("Unpublished", "")
            
        #log.info("working on objType %s with id of %s"%(thing.objType, thing.id))
        if objType == 'discussion':
            return discussionLink(thing, dparent, **kwargs)
        elif objType == 'resource':
            #log.info("before resouce link, parent is type %s"%dparent.objType)
            return resourceLink(thing, dparent, **kwargs)
        elif objType == 'idea':
            return ideaLink(thing, dparent, **kwargs)
        elif objType == 'initiative':
            return initiativeLink(thing, **kwargs)
        elif objType == 'comment':
            if thing.objType == 'revision':
                return commentLink(thing, dparent, **kwargs)
            # set up for member activity feeds in profile.py getMemberPosts  
            if 'ideaCode' in thing.keys():
                idea = ideaLib.getIdea(thing['ideaCode'])
                if not idea:
                    return False
                return ideaLink(idea, dparent, **kwargs)
            elif 'resourceCode' in thing.keys():
                resource = resourceLib.getResourceByCode(thing['resourceCode'])
                if not resource:
                    return False
                return resourceLink(resource, dparent, **kwargs)
            elif 'photoCode' in thing.keys():
                photo = photoLib.getPhoto(thing['photoCode'])
                if not photo:
                    return False
                return photoLink(photo, dparent, **kwargs)
            elif 'initiativeCode' in thing.keys():
                initiative = initiativeLib.getInitiative(thing['initiativeCode'])
                if not initiative:
                    return False
                return initiativeLink(initiative, **kwargs)
            else:
                discussion = discussionLib.getDiscussion(thing['discussionCode'])
                if not discussion:
                    return False
                return discussionLink(discussion, dparent, **kwargs)
            
        
        # SOURCE LINE 1075
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_adminThing(context,thing,**kwargs):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        def enableThingLink(thing,**kwargs):
            return render_enableThingLink(context,thing,**kwargs)
        def immunifyThingLink(thing,**kwargs):
            return render_immunifyThingLink(context,thing,**kwargs)
        def adoptThingLink(thing,**kwargs):
            return render_adoptThingLink(context,thing,**kwargs)
        def deleteThingLink(thing,**kwargs):
            return render_deleteThingLink(context,thing,**kwargs)
        def disableThingLink(thing,**kwargs):
            return render_disableThingLink(context,thing,**kwargs)
        __M_writer = context.writer()
        # SOURCE LINE 1638
        __M_writer(u'\n    ')
        # SOURCE LINE 1639
 
        if thing.objType == 'revision':
            return
        adminID = 'admin-%s' % thing['urlCode']
            
        
        # SOURCE LINE 1643
        __M_writer(u'\n    <div class="row-fluid collapse" id="')
        # SOURCE LINE 1644
        __M_writer(escape(adminID))
        __M_writer(u'">\n        <div class="span11 offset1 alert">\n            <div class="tabbable"> <!-- Only required for left/right tabs -->\n                <ul class="nav nav-tabs">\n                    <li class="active"><a href="#disable-')
        # SOURCE LINE 1648
        __M_writer(escape(adminID))
        __M_writer(u'" data-toggle="tab">Disable</a></li>\n                    <li><a href="#enable-')
        # SOURCE LINE 1649
        __M_writer(escape(adminID))
        __M_writer(u'" data-toggle="tab">Enable</a></li>\n                    <li><a href="#immunify-')
        # SOURCE LINE 1650
        __M_writer(escape(adminID))
        __M_writer(u'" data-toggle="tab">Immunify</a></li>\n')
        # SOURCE LINE 1651
        if thing.objType == 'idea':
            # SOURCE LINE 1652
            __M_writer(u'                    <li><a href="#adopt-')
            __M_writer(escape(adminID))
            __M_writer(u'" data-toggle="tab">Adopt</a></li>\n')
            pass
        # SOURCE LINE 1654
        if c.privs['admin']:
            # SOURCE LINE 1655
            __M_writer(u'                    <li><a href="#delete-')
            __M_writer(escape(adminID))
            __M_writer(u'" data-toggle="tab">Delete</a></li>\n')
            pass
        # SOURCE LINE 1657
        __M_writer(u'                </ul>\n                <div class="tab-content">\n                    <div class="tab-pane active" id="disable-')
        # SOURCE LINE 1659
        __M_writer(escape(adminID))
        __M_writer(u'">\n                        <form class="form-inline" action = ')
        # SOURCE LINE 1660
        __M_writer(disableThingLink(thing, embed=True, raw=True) )
        __M_writer(u'>\n                            <fieldset>\n                                <label>Reason:</label>\n                                <input type="text" name="reason" class="span8">\n                                <button type="submit" name="submit" class="btn disableButton" ')
        # SOURCE LINE 1664
        __M_writer(disableThingLink(thing, embed=True) )
        __M_writer(u'>Submit</button>\n                            </fieldset>\n                        </form>\n                        <span id="disableResponse-')
        # SOURCE LINE 1667
        __M_writer(escape(thing['urlCode']))
        __M_writer(u'"></span>\n                    </div>\n                    <div class="tab-pane" id="enable-')
        # SOURCE LINE 1669
        __M_writer(escape(adminID))
        __M_writer(u'">\n                        <form class="form-inline" action = ')
        # SOURCE LINE 1670
        __M_writer(enableThingLink(thing, embed=True, raw=True) )
        __M_writer(u'>\n                            <fieldset>\n                                <label>Reason:</label>\n                                <input type="text" name="reason" class="span8">\n                                <button type="submit" name = "submit" class="btn enableButton" ')
        # SOURCE LINE 1674
        __M_writer(enableThingLink(thing, embed=True) )
        __M_writer(u'>Submit</button>\n                            </fieldset>\n                        </form>\n                        <span id="enableResponse-')
        # SOURCE LINE 1677
        __M_writer(escape(thing['urlCode']))
        __M_writer(u'"></span>\n                    </div>\n                    <div class="tab-pane" id="immunify-')
        # SOURCE LINE 1679
        __M_writer(escape(adminID))
        __M_writer(u'">\n                        <form class="form-inline" action = ')
        # SOURCE LINE 1680
        __M_writer(immunifyThingLink(thing, embed=True, raw=True) )
        __M_writer(u'>\n                            <fieldset>\n                                <label>Reason:</label>\n                                <input type="text" name="reason" class="span8">\n                                <button type="submit" name = "submit" class="btn immunifyButton" ')
        # SOURCE LINE 1684
        __M_writer(immunifyThingLink(thing, embed=True) )
        __M_writer(u'>Submit</button>\n                            </fieldset>\n                        </form>\n                        <span id="immunifyResponse-')
        # SOURCE LINE 1687
        __M_writer(escape(thing['urlCode']))
        __M_writer(u'"></span>\n                    </div>\n')
        # SOURCE LINE 1689
        if thing.objType == 'idea':
            # SOURCE LINE 1690
            __M_writer(u'                    <div class="tab-pane" id="adopt-')
            __M_writer(escape(adminID))
            __M_writer(u'">\n                        <form class="form-inline" action = ')
            # SOURCE LINE 1691
            __M_writer(adoptThingLink(thing, embed=True, raw=True) )
            __M_writer(u'>\n                            <fieldset>\n                                <label>Reason:</label>\n                                <input type="text" name="reason" class="span8">\n                                <button class="btn adoptButton" type="submit" name="submit" ')
            # SOURCE LINE 1695
            __M_writer(adoptThingLink(thing, embed=True) )
            __M_writer(u'>Submit</button>\n                            </fieldset>\n                        </form>\n                        <span id="adoptResponse-')
            # SOURCE LINE 1698
            __M_writer(escape(thing['urlCode']))
            __M_writer(u'"></span>\n                    </div>\n')
            pass
        # SOURCE LINE 1701
        if c.privs['admin']:
            # SOURCE LINE 1702
            __M_writer(u'                    <div class="tab-pane" id="delete-')
            __M_writer(escape(adminID))
            __M_writer(u'">\n                        <form class="form-inline" action = ')
            # SOURCE LINE 1703
            __M_writer(deleteThingLink(thing, embed=True, raw=True) )
            __M_writer(u'>\n                            <fieldset>\n                                <label>Reason:</label>\n                                <input type="text" name="reason" class="span8">\n                                <button class="btn deleteButton" type="submit" name="submit" ')
            # SOURCE LINE 1707
            __M_writer(deleteThingLink(thing, embed=True) )
            __M_writer(u'>Submit</button>\n                            </fieldset>\n                        </form>\n                        <span id="deleteResponse-')
            # SOURCE LINE 1710
            __M_writer(escape(thing['urlCode']))
            __M_writer(u'"></span>\n                    </div>\n')
            pass
        # SOURCE LINE 1713
        __M_writer(u'                </div>\n            </div>\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_resourceLink(context,r,p,**kwargs):
    context.caller_stack._push_frame()
    try:
        def commentLinkAppender(**kwargs):
            return render_commentLinkAppender(context,**kwargs)
        __M_writer = context.writer()
        # SOURCE LINE 884
        __M_writer(u'\n   ')
        # SOURCE LINE 885

        if 'initiativeCode' in p:
            parentBase = 'initiative'
            parentCode = p['initiativeCode']
            parentURL = p['initiative_url']
        else:
            parentBase = 'workshop'
            parentCode = p['urlCode']
            parentURL = p['url']
            
        if 'directLink' in kwargs:
            if kwargs['directLink'] == True and r['type'] == 'url':
                    resourceStr = 'href="%s' %(r['info'])
            else:
                if 'noHref' in kwargs:
                    resourceStr = '/%s/%s/%s/resource/%s/%s' %(parentBase, parentCode, parentURL, r["urlCode"], r["url"])
                else:
                    resourceStr = 'href="/%s/%s/%s/resource/%s/%s' %(parentBase, parentCode, parentURL, r["urlCode"], r["url"])
        else:
            if 'noHref' in kwargs:
                resourceStr = '/%s/%s/%s/resource/%s/%s' %(parentBase, parentCode, parentURL, r["urlCode"], r["url"])
            else:
                resourceStr = 'href="/%s/%s/%s/resource/%s/%s' %(parentBase, parentCode, parentURL, r["urlCode"], r["url"])
        
        resourceStr += commentLinkAppender(**kwargs)
        if 'noHref' in kwargs:
            resourceStr += ''
        else:
            resourceStr += '"'
        
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                return resourceStr
           
        
        # SOURCE LINE 918
        __M_writer(u'\n   ')
        # SOURCE LINE 919
        __M_writer(resourceStr )
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_userLink(context,user,**kwargs):
    context.caller_stack._push_frame()
    try:
        def userImage(user,**kwargs):
            return render_userImage(context,user,**kwargs)
        def ellipsisIZE(string,numChars,**kwargs):
            return render_ellipsisIZE(context,string,numChars,**kwargs)
        type = context.get('type', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 776
        __M_writer(u'\n   ')
        # SOURCE LINE 777

        if type(user) == type(1L):
           user = userLib.getUserByID(user)
        elif type(user) == type(u''):
           user = userLib.getUserByCode(user)
        if user.objType == 'facilitator':
           user = userLib.getUserByID(user.owner)
        if user.objType == 'listener':
           user = userLib.getUserByEmail(user['email'])
        if 'raw' in kwargs:
           if kwargs['raw']:
              return '/profile/%s/%s/' %(user['urlCode'], user['url'])
        thisLink = "<a href='/profile/%s/%s/'" %(user['urlCode'], user['url'])
        if 'className' in kwargs:
           thisLink += ' class = "' + kwargs['className'] + '"'
        thisLink += '>'
        if 'title' in kwargs:
           thisTitle = kwargs['title']
        else:
           thisTitle = user['name']
        if 'maxChars' in kwargs:
           thisTitle = ellipsisIZE(thisTitle, kwargs['maxChars'])
        thisLink += thisTitle
        if 'image' in kwargs:
           if kwargs['image'] == True:
              thisLink += userImage(user)
        thisLink += "</a>"
           
        
        # SOURCE LINE 804
        __M_writer(u'\n   ')
        # SOURCE LINE 805
        __M_writer(thisLink )
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_orgPosition(context,thing):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 604
        __M_writer(u'\n')
        # SOURCE LINE 605
        if 'positions' in session and thing['urlCode'] not in session['positions']:
            # SOURCE LINE 606
            __M_writer(u'        <form action="/profile/')
            __M_writer(escape(c.authuser['urlCode']))
            __M_writer(u'/')
            __M_writer(escape(c.authuser['url']))
            __M_writer(u'/add/position/handler/')
            __M_writer(escape(thing['urlCode']))
            __M_writer(u'" method="POST">\n            Does your organization:</br>\n            <label class="radio">\n            <input type="radio" name="position" id="positionSupport" value="support" checked>\n                Support this ')
            # SOURCE LINE 610
            __M_writer(escape(thing.objType))
            __M_writer(u'\n            </label>\n            <label class="radio">\n            <input type="radio" name="position" id="positionOppose" value="oppose">\n                Oppose this ')
            # SOURCE LINE 614
            __M_writer(escape(thing.objType))
            __M_writer(u'\n            </label>\n            Reason:\n            <textarea rows="3" name="text" required></textarea>\n            <button class="btn btn-success">Submit</button>\n        </form>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_geoBreadcrumbs(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1179
        __M_writer(u'\n    ')
        # SOURCE LINE 1180

        outOfScope = False
        if 'user' in session:
            county = c.authuser_geo['countyTitle']
            city = c.authuser_geo['cityTitle']
            if county == city:
                county = 'County of ' + county
                city = 'City of ' + city
            scopeMapping = [    ('earth', 'Earth'),
                            ('country', c.authuser_geo['countryTitle']),
                            ('state', c.authuser_geo['stateTitle']),
                            ('county', county),
                            ('city', city),
                            ('postalCode', c.authuser_geo['postalCode'])
                            ]
            
        
        # SOURCE LINE 1195
        __M_writer(u'\n')
        # SOURCE LINE 1196
        if 'user' in session:
            # SOURCE LINE 1197
            __M_writer(u'      <ul class="nav nav-pills geo-breadcrumbs">\n')
            # SOURCE LINE 1198
            for scopeLevel in scopeMapping:
                # SOURCE LINE 1199
                __M_writer(u'                ')

                activeClass = ''
                    
                if c.scope['level'] == scopeLevel[0]:
                    if scopeLevel[0] != 'earth':
                        scopeKey = '%sURL' % scopeLevel[0] 
                        userScope = c.authuser_geo[scopeKey]
                    else:
                        userScope = 'earth'
                    if c.scope['name'] == userScope:
                        activeClass = 'active'
                    else:
                        outOfScope = True
                                
                
                # SOURCE LINE 1212
                __M_writer(u'\n                <li class="')
                # SOURCE LINE 1213
                __M_writer(escape(activeClass))
                __M_writer(u'">\n                    <a ')
                # SOURCE LINE 1214
                __M_writer(self._geoWorkshopLink(c.authuser_geo, depth = scopeLevel[0]) )
                __M_writer(u'>')
                __M_writer(escape(scopeLevel[1]))
                __M_writer(u'</a>\n')
                # SOURCE LINE 1215
                if scopeLevel[0] != 'postalCode':
                    # SOURCE LINE 1216
                    __M_writer(u'                        <span class="divider">/</span>\n')
                    pass
                # SOURCE LINE 1218
                __M_writer(u'                </li>\n')
                pass
            # SOURCE LINE 1220
            __M_writer(u'        </ul>\n')
            pass
        # SOURCE LINE 1222
        __M_writer(u'    ')
 
        return outOfScope
            
        
        # SOURCE LINE 1224
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_revisionHistory(context,revisions,parent):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        def thingLinkRouter(thing,dparent,**kwargs):
            return render_thingLinkRouter(context,thing,dparent,**kwargs)
        def userLink(user,**kwargs):
            return render_userLink(context,user,**kwargs)
        __M_writer = context.writer()
        # SOURCE LINE 1750
        __M_writer(u'\n')
        # SOURCE LINE 1751
        if revisions:
            # SOURCE LINE 1752
            __M_writer(u'        <div class="accordion" id="revision-wrapper">\n            <div class="accordion-group no-border">\n                <div class="accordion-heading">\n                    <a class="accordion-toggle green green-hover" data-toggle="collapse" data-parent="#revision-wrapper" href="#revisionsTable-')
            # SOURCE LINE 1755
            __M_writer(escape(parent['urlCode']))
            __M_writer(u'">\n                        <small>Click to show revisions</small>\n                    </a>\n                </div>\n                <div id="revisionsTable-')
            # SOURCE LINE 1759
            __M_writer(escape(parent['urlCode']))
            __M_writer(u'" class="accordion-body collapse">\n                    <div class="accordion-inner no-border">\n                        <table class="table table-hover table-condensed">\n                            <tr>\n                                <th>Revision</th>\n                                <th>Author</th>\n                            </tr>\n')
            # SOURCE LINE 1766
            for rev in revisions:
                # SOURCE LINE 1767
                __M_writer(u'                                ')
 
                if c.w:
                    dparent = c.w
                elif c.initiative:
                    dparent = c.initiative
                elif c.user:
                    dparent = c.user
                linkStr = '<a %s>%s</a>' %(thingLinkRouter(rev, dparent, embed=True), rev.date) 
                                                
                
                # SOURCE LINE 1775
                __M_writer(u'\n                                <tr>\n                                    <td>')
                # SOURCE LINE 1777
                __M_writer(linkStr )
                __M_writer(u'</td>\n                                    <td>')
                # SOURCE LINE 1778
                __M_writer(escape(userLink(rev.owner)))
                __M_writer(u'</td>\n                                </tr>\n')
                pass
            # SOURCE LINE 1781
            __M_writer(u'                        </table>\n                    </div><!-- accordian-inner -->\n                </div><!-- accordian-body -->\n            </div><!-- accordian-group -->\n        </div><!-- accordian -->\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_geoDropdown(context,*args):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        def geoButton(scopeMapping):
            return render_geoButton(context,scopeMapping)
        def myPlaces(scopeMapping):
            return render_myPlaces(context,scopeMapping)
        __M_writer = context.writer()
        # SOURCE LINE 1227
        __M_writer(u'\n    ')
        # SOURCE LINE 1228

        outOfScope = False
        if 'user' in session:
            county = c.authuser_geo['countyTitle']
            city = c.authuser_geo['cityTitle']
            if county == city:
                county = 'County of ' + county
                city = 'City of ' + city
            scopeMapping = [    ('earth', 'Earth'),
                            ('country', c.authuser_geo['countryTitle']),
                            ('state', c.authuser_geo['stateTitle']),
                            ('county', county),
                            ('city', city),
                            ('postalCode', c.authuser_geo['postalCode'])
                            ]
            
        
        # SOURCE LINE 1243
        __M_writer(u'\n')
        # SOURCE LINE 1244
        if 'user' in session:
            # SOURCE LINE 1245
            if 'navBar' in args:
                # SOURCE LINE 1246
                __M_writer(u'        ')
                __M_writer(escape(myPlaces(scopeMapping)))
                __M_writer(u'\n')
                # SOURCE LINE 1247
            else:
                # SOURCE LINE 1248
                __M_writer(u'        ')
                __M_writer(escape(geoButton(scopeMapping)))
                __M_writer(u'\n')
                pass
            # SOURCE LINE 1250
            __M_writer(u'\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render__geoWorkshopLink(context,geoInfo,depth=None,**kwargs):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 1340
        __M_writer(u'\n    ')
        # SOURCE LINE 1341

        link = 'href="/workshops/geo/earth/'
        if depth is None or depth == 'earth':
            link += '0"'
        elif depth == 'country':
            link += '%s"' % geoInfo['countryURL']
        elif depth == 'state':
            link += '%s/%s"' % (geoInfo['countryURL'], geoInfo['stateURL'])
        elif depth == 'county':
            link += '%s/%s/%s"' % (geoInfo['countryURL'], geoInfo['stateURL'], geoInfo['countyURL'])
        elif depth == 'city':
            link += '%s/%s/%s/%s"' % (geoInfo['countryURL'], geoInfo['stateURL'], geoInfo['countyURL'], geoInfo['cityURL'])
        elif depth == 'postalCode':
            link += '%s/%s/%s/%s/%s"' % (geoInfo['countryURL'], geoInfo['stateURL'], geoInfo['countyURL'], geoInfo['cityURL'], geoInfo['postalCodeURL'])
        return link
            
        
        # SOURCE LINE 1356
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_userGeoLink(context,user,**kwargs):
    context.caller_stack._push_frame()
    try:
        self = context.get('self', UNDEFINED)
        type = context.get('type', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1323
        __M_writer(u'\n    ')
        # SOURCE LINE 1324

        if type(user) == type(1L):
            user = userLib.getUserByID(user)
        userGeo = getGeoInfo(user.id)[0]
        geoLinkStr = ''
        
        geoLinkStr += '<a %s class="geoLink">%s</a>' %(self._geoWorkshopLink(userGeo, depth = 'city'), userGeo['cityTitle'])
        geoLinkStr += ', '
        geoLinkStr += '<a %s class="geoLink">%s</a>' %(self._geoWorkshopLink(userGeo, depth = 'state'), userGeo['stateTitle'])
        if 'comment' not in kwargs:
            geoLinkStr += ', '
            geoLinkStr += '<a %s class="geoLink">%s</a>' %(self._geoWorkshopLink(userGeo, depth = 'country'), userGeo['countryTitle'])
            
        
        # SOURCE LINE 1336
        __M_writer(u'\n    ')
        # SOURCE LINE 1337
        __M_writer(geoLinkStr )
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_userGreetingMsg(context,user):
    context.caller_stack._push_frame()
    try:
        def ellipsisIZE(string,numChars,**kwargs):
            return render_ellipsisIZE(context,string,numChars,**kwargs)
        type = context.get('type', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 808
        __M_writer(u'\n  ')
        # SOURCE LINE 809

        if type(user) == type(1L):
           user = userLib.getUserByID(user)
        elif type(user) == type(u''):
           user = userLib.getUserByCode(user)
        if user.objType == 'facilitator':
           user = userLib.getUserByID(user.owner)
        if user.objType == 'listener':
           user = userLib.getUserByEmail(user['email'])
          
        
        # SOURCE LINE 818
        __M_writer(u'\n')
        # SOURCE LINE 819
        if len(user['greetingMsg']) > 0:
            # SOURCE LINE 820
            __M_writer(u'    ')
            __M_writer(escape(ellipsisIZE(user['greetingMsg'], 35)))
            __M_writer(u'\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_deleteThingLink(context,thing,**kwargs):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 1419
        __M_writer(u'\n    ')
        # SOURCE LINE 1420

        deleteStr = '"/delete/%s/%s"' %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return deleteStr
                    return 'href = ' + deleteStr
                return 'href = ' + deleteStr
        deleteStr = 'href = ' + deleteStr
            
        
        # SOURCE LINE 1430
        __M_writer(u'\n    ')
        # SOURCE LINE 1431
        __M_writer(deleteStr )
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showFullScope(context,item):
    context.caller_stack._push_frame()
    try:
        KeyError = context.get('KeyError', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 2020
        __M_writer(u'\n    ')
        # SOURCE LINE 2021
  
        try:
          try:
            scopeList = item['scope']
          except KeyError:
            scopeList = item['workshop_public_scope']
        except:
          scopeList = "0|0|0|0|0|0|0|0|0|0"
        
        scopeList = scopeList.split('|')
        country = scopeList[2].replace("-", " ")
        state = scopeList[4].replace("-", " ")
        county = scopeList[6].replace("-", " ")
        city = scopeList[8].replace("-", " ")
        postalCode = scopeList[9]
        if country == '0':
            scopeString = '<span class="badge badge-info">Planet Earth</span>'
        else:
            scopeString = "Planet Earth"
            if state == '0':
                scopeString += ', <span class="badge badge-info">Country of %s</span>'%country.title()
            else:
                scopeString += ', Country of %s'%country.title()
                if county == '0':
                    scopeString += ', <span class="badge badge-info">State of %s</span>'%state.title()
                else:
                    scopeString += ', State of %s'%state.title()
                    if city == '0':
                        scopeString += ', <span class="badge badge-info">County of %s</span>'%county.title()
                    else:
                        scopeString += ', County of %s'%county.title()
                        if postalCode == '0':
                            scopeString += ', <span class="badge badge-info">City of %s</span>'%city.title()
                        else:
                            scopeString += ", City of %s"%city.title()
                            scopeString += ', <span class="badge badge-info">Zip code of %s</span>'%postalCode
            
        
        # SOURCE LINE 2057
        __M_writer(u'\n    ')
        # SOURCE LINE 2058
        __M_writer(scopeString )
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_adoptThingLink(context,thing,**kwargs):
    context.caller_stack._push_frame()
    try:
        immunifyStr = context.get('immunifyStr', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1404
        __M_writer(u'\n    ')
        # SOURCE LINE 1405

        adoptStr = '"/adopt/%s/%s"' %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return adoptStr
                    return 'href = ' + adoptStr
                return 'href = ' + adoptStr
        adoptStr = 'href = ' + adoptStr
            
        
        # SOURCE LINE 1415
        __M_writer(u'\n    ')
        # SOURCE LINE 1416
        __M_writer(immunifyStr )
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_editThing(context,thing,**kwargs):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        def editThingLink(thing,**kwargs):
            return render_editThingLink(context,thing,**kwargs)
        __M_writer = context.writer()
        # SOURCE LINE 1533
        __M_writer(u'\n\n    ')
        # SOURCE LINE 1535
        editID = 'edit-%s' % thing['urlCode'] 
        
        __M_writer(u'\n    ')
        # SOURCE LINE 1536
 
        text = ''
        if 'text' in thing.keys():
            text = thing['text']
            
        ctype = ""
        if thing.objType == 'comment':
            if c.discussion and c.discussion['discType'] == 'organization_position':
                ctype = "regular"
            elif 'initiativeCode' in thing and 'resourceCode' not in thing:
                ctype = "initiative"
            elif 'ideaCode' in thing:
                ctype = "idea"
            else:
                ctype = "reguar"
        
            yesChecked = ""
            noChecked = ""
            neutralChecked = ""
            
            if ctype != "regular":
                if 'commentRole' in thing:
                    if thing['commentRole'] == 'yes':
                        yesChecked = 'checked'
                    elif thing['commentRole'] == 'no':
                        noChecked = 'checked'
                    else:
                        neutralChecked = 'checked'
                else:
                    neutralChecked = 'checked'
        if thing.objType == 'discussion' and 'position' in thing:
            supportChecked = ""
            opposeChecked = ""
            if thing['position'] == 'support':
                supportChecked = 'checked'
            else:
                opposeChecked = 'checked'
            ctype = ""
            if 'initiativeCode' in thing:
                ctype = 'initiative'
            elif 'ideaCode' in thing:
                ctype = 'idea'
            
        
        # SOURCE LINE 1578
        __M_writer(u'\n    <div class="row-fluid collapse" id="')
        # SOURCE LINE 1579
        __M_writer(escape(editID))
        __M_writer(u'">\n        <div class="span11 offset1">\n            <div class="spacer"></div>\n            <form action="')
        # SOURCE LINE 1582
        __M_writer(escape(editThingLink(thing, embed=True, raw=True)))
        __M_writer(u'" ng-controller="editItemController" method="post" class="form" id="edit-')
        __M_writer(escape(thing.objType))
        __M_writer(u'">\n                <fieldset>\n                <label>Edit</label>\n                <span ng-show="editItemShow"><div class="alert alert-danger">{{editItemResponse}}</div></span>\n')
        # SOURCE LINE 1586
        if thing.objType == 'comment':
            # SOURCE LINE 1587
            __M_writer(u'                    <label>Comment text</label>\n')
            # SOURCE LINE 1588
            if ctype == 'initiative' or ctype == 'idea':
                # SOURCE LINE 1589
                __M_writer(u'                        <div class="row-fluid">\n                                <label class="radio inline">\n                                    <input type=radio name="commentRole')
                # SOURCE LINE 1591
                __M_writer(escape(thing['urlCode']))
                __M_writer(u'" value="yes" ')
                __M_writer(escape(yesChecked))
                __M_writer(u'> I support this ')
                __M_writer(escape(ctype))
                __M_writer(u'\n                                </label>\n                                <label class="radio inline">\n                                    <input type=radio name="commentRole')
                # SOURCE LINE 1594
                __M_writer(escape(thing['urlCode']))
                __M_writer(u'" value="neutral" ')
                __M_writer(escape(neutralChecked))
                __M_writer(u'> Neutral\n                                </label>\n                                <label class="radio inline">\n                                    <input type=radio name="commentRole')
                # SOURCE LINE 1597
                __M_writer(escape(thing['urlCode']))
                __M_writer(u'" value="no" ')
                __M_writer(escape(noChecked))
                __M_writer(u'> I am against this ')
                __M_writer(escape(ctype))
                __M_writer(u'\n                                </label>\n                        </div><!-- row-fluid -->\n')
                pass
            # SOURCE LINE 1601
            __M_writer(u'                    <textarea class="comment-reply span12" name="textarea')
            __M_writer(escape(thing['urlCode']))
            __M_writer(u'" required>')
            __M_writer(escape(thing['data']))
            __M_writer(u'</textarea>\n')
            # SOURCE LINE 1602
        elif thing.objType == 'idea':
            # SOURCE LINE 1603
            __M_writer(u'                    <label>Idea title</label>\n                    <input type="text" class="input-block-level" name="title" value = "')
            # SOURCE LINE 1604
            __M_writer(escape(thing['title']))
            __M_writer(u'" maxlength="120" id = "title" required>\n                    <label>Additional information <a href="#" class="btn btn-mini btn-info" onclick="window.open(\'/help/markdown.html\',\'popUpWindow\',\'height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes\');">View Formatting Guide</a></label>\n                    <textarea name="text" rows="3" class="input-block-level">')
            # SOURCE LINE 1606
            __M_writer(escape(thing['text']))
            __M_writer(u'</textarea>\n')
            # SOURCE LINE 1607
        elif thing.objType == 'discussion':
            # SOURCE LINE 1608
            __M_writer(u'                    <label>Topic title</label>\n                    <input type="text" class="input-block-level" name="title" value = "')
            # SOURCE LINE 1609
            __M_writer(escape(thing['title']))
            __M_writer(u'" maxlength="120" id = "title" required>\n')
            # SOURCE LINE 1610
            if 'position' in thing:
                # SOURCE LINE 1611
                __M_writer(u'                        <div class="row-fluid">\n                            <label class="radio inline">\n                                <input type=radio name="position" value="support" ')
                # SOURCE LINE 1613
                __M_writer(escape(supportChecked))
                __M_writer(u'> We support this ')
                __M_writer(escape(ctype))
                __M_writer(u'\n                            </label>\n                            <label class="radio inline">\n                                <input type=radio name="position" value="oppose" ')
                # SOURCE LINE 1616
                __M_writer(escape(opposeChecked))
                __M_writer(u'> We oppose this ')
                __M_writer(escape(ctype))
                __M_writer(u'\n                            </label>\n                        </div><!-- row-fluid -->\n                        <div class="spacer"></div>\n')
                pass
            # SOURCE LINE 1621
            __M_writer(u'                    <label>Additional information <a href="#" class="btn btn-mini btn-info" onclick="window.open(\'/help/markdown.html\',\'popUpWindow\',\'height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes\');">View Formatting Guide</a></label>\n                    <textarea name="text" rows="3" class="input-block-level">')
            # SOURCE LINE 1622
            __M_writer(escape(text))
            __M_writer(u'</textarea>\n')
            # SOURCE LINE 1623
        elif thing.objType == 'resource':
            # SOURCE LINE 1624
            __M_writer(u'                    <label>Resource title</label>\n                    <input type="text" class="input-block-level" name="title" value = "')
            # SOURCE LINE 1625
            __M_writer(escape(thing['title']))
            __M_writer(u'" maxlength="120" id="title" required>\n                    <label>Resource URL</label>\n                    <input type="url" class="input-block-level" name="link" value = "')
            # SOURCE LINE 1627
            __M_writer(escape(thing['link']))
            __M_writer(u'" id = "link" required>\n                    <label>Additional information <a href="#" class="btn btn-mini btn-info" onclick="window.open(\'/help/markdown.html\',\'popUpWindow\',\'height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes\');">View Formatting Guide</a></label>\n                    <textarea name="text" rows="3" class="input-block-level">')
            # SOURCE LINE 1629
            __M_writer(escape(thing['text']))
            __M_writer(u'</textarea>\n')
            pass
        # SOURCE LINE 1631
        __M_writer(u'                </fieldset>\n                <button type="submit" class="btn btn-civ pull-right" name = "submit" value = "reply">Submit</button>\n            </form>\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showItemInActivity(context,item,w,**kwargs):
    context.caller_stack._push_frame()
    try:
        def ellipsisIZE(string,numChars,**kwargs):
            return render_ellipsisIZE(context,string,numChars,**kwargs)
        def thingLinkRouter(thing,dparent,**kwargs):
            return render_thingLinkRouter(context,thing,dparent,**kwargs)
        __M_writer = context.writer()
        # SOURCE LINE 1789
        __M_writer(u'\n    ')
        # SOURCE LINE 1790

        thisUser = userLib.getUserByID(item.owner)
        actionMapping = {   'resource': 'added the resource',
                            'discussion': 'started the conversation',
                            'update': 'added an initiative progress report',
                            'idea': 'posed the idea',
                            'initiative': 'launched the initiative',
                            'comment': 'commented on a'}
        objTypeMapping = {  'resource':'resource',
                            'discussion':'conversation',
                            'idea':'idea',
                            'initiative':'initiative',
                            'comment':'comment'}
        eclass = ""
        if 'expandable' in kwargs:
            if kwargs['expandable']:
                eclass=' class="expandable"'
                if item.objType == 'comment':
                    title = item['data']
                else:
                    title = item['title']
            else:
                if item.objType == 'comment':
                    title = ellipsisIZE(item['data'], 40)
                else:
                    title = ellipsisIZE(item['title'], 40)
        else:
            if item.objType == 'comment':
                title = ellipsisIZE(item['data'], 40)
            else:
                title = ellipsisIZE(item['title'], 40)
        
        if item.objType == 'discussion' and item['discType'] == 'update':
            activityStr = actionMapping['update']
        else:
            activityStr = actionMapping[item.objType]
        # used for string mapping below
        objType = item.objType
        if item.objType == 'comment':
            if 'ideaCode' in item.keys():
                activityStr += 'n'
                objType = 'idea'
            elif 'resourceCode' in item.keys():
                objType = 'resource'
            elif 'initiativeCode' in item.keys():
                objType = 'initiative'
            elif item.keys():
                objType = 'discussion'
            
            activityStr += ' <a ' + thingLinkRouter(item, w, embed = True) + '>' + objTypeMapping[objType]
            activityStr += '</a>, saying '
            activityStr += ' <a ' + thingLinkRouter(item, w, embed = True, commentCode=item['urlCode']) + eclass + '>' + title + '</a>'
        else:
            activityStr += ' <a ' + thingLinkRouter(item, w, embed = True) + eclass + '>' + title + '</a>'
            
        
        # SOURCE LINE 1844
        __M_writer(u'\n    ')
        # SOURCE LINE 1845
        __M_writer(activityStr )
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_isReadOnly(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 714
        __M_writer(u'\n   ')
        # SOURCE LINE 715

        if (c.conf['read_only.value'] == 'true') or (c.conf['read_only.value'] == 'True'):
           return True
        else:
           return False
           
        
        # SOURCE LINE 720
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_ellipsisIZE(context,string,numChars,**kwargs):
    context.caller_stack._push_frame()
    try:
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1719
        __M_writer(u'\n    ')
        # SOURCE LINE 1720

        if numChars > len(string):
            return string
        else:
            return string[:numChars] + "..."
            
        
        # SOURCE LINE 1725
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showScope(context,item):
    context.caller_stack._push_frame()
    try:
        KeyError = context.get('KeyError', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1987
        __M_writer(u'\n    ')
        # SOURCE LINE 1988
  
        try:
          try:
            scopeList = item['scope']
          except KeyError:
            scopeList = item['workshop_public_scope']
        except:
          scopeList = "0|0|0|0|0|0|0|0|0|0"
        
        scopeList = scopeList.split('|')
        country = scopeList[2].replace("-", " ")
        state = scopeList[4].replace("-", " ")
        county = scopeList[6].replace("-", " ")
        city = scopeList[8].replace("-", " ")
        postalCode = scopeList[9]
        scopeString = ""
        if country == '0':
            scopeString = 'Planet Earth'
        elif state == '0':
            scopeString = 'Country of %s' %country.title()
        elif county == '0':
            scopeString = 'State of %s' %state.title()
        elif city == '0':
            scopeString = 'County of %s'%county.title()
        elif postalCode == '0':
            scopeString += 'City of %s'%city.title()
        else:
            scopeString += 'Zip Code %s</span>'%postalCode
            
        
        # SOURCE LINE 2016
        __M_writer(u'\n    <span class="badge badge-info">')
        # SOURCE LINE 2017
        __M_writer(scopeString )
        __M_writer(u'</span>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_fingerprintFile(context,path):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 1848
        __M_writer(u'\n    ')
        # SOURCE LINE 1849

        # Adds a fingerprint so we can cache-bust the browser if the file is modified
        prefix = 'pylowiki/public'
        modTime = os.stat(prefix + path).st_mtime
        return "%s?t=%s" %(path, modTime)
            
        
        # SOURCE LINE 1854
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_initiativeImage(context,i):
    context.caller_stack._push_frame()
    try:
        def initiativeLink(initiative,**kwargs):
            return render_initiativeLink(context,initiative,**kwargs)
        __M_writer = context.writer()
        # SOURCE LINE 2061
        __M_writer(u'\n  ')
        # SOURCE LINE 2062

        if 'directoryNum_photos' in i and 'pictureHash_photos' in i:
          imgURL = "/images/photos/" + i['directoryNum_photos'] + "/thumbnail/" + i['pictureHash_photos'] + ".png" 
        else:
          imgURL = "/images/icons/generalInitiative.jpg"
          
        
        # SOURCE LINE 2067
        __M_writer(u'\n\n  <a ')
        # SOURCE LINE 2069
        __M_writer(escape(initiativeLink(i)))
        __M_writer(u'>\n      <div style="height:80px; width:110px; background-image:url(\'')
        # SOURCE LINE 2070
        __M_writer(escape(imgURL))
        __M_writer(u'\'); background-repeat:no-repeat; background-size:cover; background-position:center;"/></div>\n  </a>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_workshopLink(context,w,**kwargs):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 824
        __M_writer(u'\n   ')
        # SOURCE LINE 825

        if 'embed' in kwargs:
           if kwargs['embed'] == True:
              if 'raw' in kwargs:
                 if kwargs['raw'] == True:
                    return "/workshop/%s/%s" %(w['urlCode'], w['url'])
              return 'href = "/workshop/%s/%s"' %(w['urlCode'], w['url'])
        
        
        # SOURCE LINE 832
        __M_writer(u'\n   href="/workshops/')
        # SOURCE LINE 833
        __M_writer(escape(w['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(w['url']))
        __M_writer(u'"\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_myPlaces(context,scopeMapping):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1284
        __M_writer(u'\n  \n  <li class="dropdown">\n    <a href="#" class="dropdown-toggle" data-toggle="dropdown">My Places<b class="caret"></b></a>\n    <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu">\n')
        # SOURCE LINE 1289
        for scopeLevel in scopeMapping:
            # SOURCE LINE 1290
            __M_writer(u'            <li>\n                <a ')
            # SOURCE LINE 1291
            __M_writer(self._geoWorkshopLink(c.authuser_geo, depth = scopeLevel[0]) )
            __M_writer(u'>')
            __M_writer(escape(scopeLevel[1]))
            __M_writer(u'</a>\n            </li>\n')
            pass
        # SOURCE LINE 1294
        __M_writer(u'      </ul>\n  </li>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


