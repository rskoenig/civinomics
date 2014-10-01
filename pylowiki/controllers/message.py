import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, redirect

from pylowiki.lib.base import BaseController, render

import pylowiki.lib.db.comment      as commentLib
import pylowiki.lib.db.dbHelpers    as dbHelpers
import pylowiki.lib.db.event        as eventLib
import pylowiki.lib.db.facilitator  as facilitatorLib
import pylowiki.lib.fuzzyTime       as fuzzyTime
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.db.initiative   as initiativeLib
import pylowiki.lib.db.listener     as listenerLib
import pylowiki.lib.db.mainImage    as mainImageLib
import pylowiki.lib.db.message      as messageLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.workshop     as workshopLib

import pylowiki.lib.utils           as utils

import simplejson as json

log = logging.getLogger(__name__)

class MessageController(BaseController):

    def __before__(self, action, id1 = None, id2 = None):
        if id1 is not None and id2 is not None:
            c.user = userLib.getUserByCode(id1)
            if not c.user:
                abort(404)
            if 'user' in session:
                if userLib.isAdmin(c.authuser.id):
                    c.isAdmin = True
            else:
                #log.info('user not in session')
                session['afterLoginURL'] = session._environ['PATH_INFO']
                #log.info('message ctrl %s' % session['afterLoginURL'])
                session.save()
                return redirect('/login')
        

    def markRead(self, urlCode):
        self.error = False
        self.message = messageLib.getMessage(c.authuser, urlCode)
        #log.info('got urlcode %s'%urlCode)
        if not self.message:
            self.error = True

        if self.error:
            return "Error"
        self.message['read'] = u'1'
        dbHelpers.commit(self.message)
        #log.info('got here')
        return "OK"

    def showUserMessages(self, id1, id2, id3 = ''):
        c.userCode = id1
        c.userUrl = id2
        return render("/derived/6_messages.bootstrap")


    def getUserMessages(self, id1, id2, type = 'auto', limit = 7, offset = 0):

        if type == 'unread':
            read = 0

        if id1 is not None and id2 is not None:
            c.user = userLib.getUserByCode(id1)
            if not c.user:
                abort(404)
            if 'user' in session:
                if userLib.isAdmin(c.authuser.id):
                    c.isAdmin = True
                if c.user.id == c.authuser.id or c.isAdmin:
                    log.info("in controller, asking for %s messages"%limit)
                    if type == 'all':
                        c.messages = messageLib.getMessages(user=c.user, limit=limit, offset=offset)
                    elif type == 'auto':
                        #log.info('getting messages in controller')
                        c.messages = messageLib.getMessages(user=c.user, limit=limit, offset=offset)
                    elif type == 'unread':
                        log.info('looking for unread messages')
                        c.messages = messageLib.getMessages(user=c.user, limit=limit, offset=offset, read=read)
                    
            else:
                #log.info('user not in session')
                session['afterLoginURL'] = session._environ['PATH_INFO']
                #log.info('message ctrl %s' % session['afterLoginURL'])
                session.save()
                return redirect('/login')

        if not c.messages:
            #log.info("getUserMessages return NOT messages")
            return json.dumps({'statusCode':2})

        result = []

        c.unreadMessageCount = 0
        for message in c.messages:
            # if this field isn't in the message then nothing happens for this entry
            if 'extraInfo' not in message.keys():
                continue
            # now that we've asserted this fact, we can check one more thing that takes a bit more time
            if 'commentCode' in message and not commentLib.getCommentByCode(message['commentCode']):
                continue
            #log.info('loading message type: %s'%(message['extraInfo']))
            
            entry = {}
            entry['action'] = ''
            # this next field is a hack that will allow us to use ng-switch in order
            # to choose what template function to call in ng_lib.mako from 6_profile_messages.mako
            entry['combinedInfo'] = ''
            entry['commentData'] = ''
            entry['eventAction'] = ''
            entry['eventReason'] = ''
            entry['extraInfo'] = message['extraInfo']
            entry['formLink'] = ''
            entry['formStr'] = ''
            entry['itemCode'] = ''
            entry['itemImage'] = ''
            entry['itemLink'] = ''
            entry['itemTitle'] = ''
            entry['itemUrl'] = ''
            entry['messageCode'] = ''
            entry['messageDate'] = message.date.strftime('%Y-%m-%dT%H:%M:%S')
            entry['fuzzyTime'] = fuzzyTime.timeSince(message.date)
            entry['messageText'] = ''
            entry['messageTitle'] = ''
            entry['read'] = message['read']
            # instead of asking the db for a count of unread messages, we can count them as 
            if entry['read'] == u'0':
                c.unreadMessageCount = c.unreadMessageCount + 1
            
            entry['responseAction'] = ''
            entry['rowClass'] = ''
            entry['userLink'] = '#'
            entry['userImage'] = utils.civinomicsAvatar()
            entry['userName'] = 'Civinomics'
            # Try to assemble a message entry.
            # There is a key error in some cases, this is an easy fix.
            if message['read'] == u'0':
                entry['rowClass']= 'warning unread-message'
            # note: should we have an object for Civinomics just as we do for users with a code?
            if message['sender'] != u'0':
                sender = userLib.getUserByCode(message['sender'])
                entry['userName'] = utils.userName(sender)
                entry['userLink'] = utils.userLink(sender)
                entry['userImage'] = utils._userImageSource(sender)

            # fields used in all if not most of the message types are loaded here
            if 'title' in message:    
                entry['messageTitle'] = message['title']            
            if 'text' in message:
                entry['messageText'] = message['text']
            if 'urlCode' in message:
                entry['messageCode'] = message['urlCode']
            if 'read' in message:
                entry['read'] = message['read']
            # there is one edge case we've found so far that makes authorResponse throw an error
            # this code is set up to gather the basic info we expect every message to have, so
            # at the least a message will be somewhat useful even if this part throws an error.
            # entry['combinedInfo'] will not have any data, so the ng-switch in the template will
            # display a default message for these cases
            try:
                if message['extraInfo'] in ['listenerInvite', 'facilitationInvite']:
                    entry['combinedInfo'] = 'listenerFacilitationInvite'
                    workshop = workshopLib.getWorkshopByCode(message['workshopCode'])
                    if message['extraInfo'] == 'listenerInvite':
                        entry['formLink'] = "/profile/%s/%s/listener/response/handler/" %(c.user['urlCode'], c.user['url'])
                        entry['action'] = 'be a listener for'
                        # note: commenting out this next line because it appears to not be used or needed anymore
                        # role = listenerLib.getListenerByCode(message['listenerCode'])
                    else:
                        entry['formLink'] = "/profile/%s/%s/facilitate/response/handler/" %(c.user['urlCode'], c.user['url'])
                        entry['action'] = 'facilitate'
                        # note: commenting out this next line because it appears to not be used or needed anymore
                        # role = facilitatorLib.getFacilitatorByCode(message['facilitatorCode'])
                    entry['itemCode'] = workshop['urlCode']
                    entry['itemUrl'] = workshop['url']
                    entry['itemTitle'] = workshop['title'] 
                    entry['itemLink'] = utils.workshopURL(workshop)
                    mainImage = mainImageLib.getMainImage(workshop)
                    entry['itemImage'] = utils.workshopImageURL(workshop, mainImage, thumbnail=True)
                    if message['read'] == u'1':
                        # Since this is tied to the individual message, we will only have one action
                        # The query here should be rewritten to make use of map/reduce for a single query
                        # note: marking this with "note:" so the above statement is noticed more easily
                        event = eventLib.getEventsWithAction(message, 'accepted')
                        if not event:
                            entry['responseAction'] = 'declining'
                        else:
                            entry['responseAction'] = 'accepting'
                    
                elif message['extraInfo'] in ['listenerSuggestion']:
                    entry['combinedInfo'] = 'listenerSuggestion'
                    workshop = workshopLib.getWorkshopByCode(message['workshopCode'])
                    entry['itemTitle'] = workshop['title']
                    entry['itemLink'] = utils.workshopURL(workshop)
                    entry['messageTitle'] = message['title']
                    entry['messageText'] = message['text']
                    
                elif message['extraInfo'] in ['authorInvite']:
                    entry['combinedInfo'] = 'authorInvite'
                    initiative = initiativeLib.getInitiative(message['initiativeCode'])
                    entry['formLink'] = "/profile/%s/%s/facilitate/response/handler/"%(c.user['urlCode'], c.user['url'])
                    entry['action'] = 'coauthor'
                    # note: commenting out this next line because it appears to not be used or needed anymore
                    # role = facilitatorLib.getFacilitatorByCode(message['facilitatorCode'])
                    entry['itemCode'] = initiative['urlCode']
                    bgPhoto_url, photo_url, thumbnail_url  = utils.initiativeImageURL(initiative)
                    entry['itemImage'] = thumbnail_url
                    entry['itemLink'] = utils.initiativeURL(initiative)
                    entry['itemTitle'] = initiative['title']
                    entry['itemUrl'] = initiative['url']

                    entry['messageText'] = message['text']
                    entry['messageTitle'] = message['title']

                    if message['read'] == u'1':                    
                        # Since this is tied to the individual message, we will only have one action
                        # The query here should be rewritten to make use of map/reduce for a single query
                        event = eventLib.getEventsWithAction(message, 'accepted')
                        if not event:
                            entry['responseAction'] = 'declining'
                        else:
                            entry['responseAction'] = 'accepting'
                    #else:                                    
                        # note: ?what to do?
                                                                
                elif message['extraInfo'] in ['authorResponse']:
                    entry['combinedInfo'] = 'authorResponse'
                    if 'workshopCode' in message:
                        container = workshopLib.getWorkshopByCode(message['workshopCode'])
                    elif 'initiativeCode' in message:
                        container = initiativeLib.getInitiative(message['initiativeCode'])
                    entry['itemTitle'] = container['title']
                    
                elif message['extraInfo'] in ['commentResponse']:
                    entry['combinedInfo'] = 'commentResponse'
                    comment = commentLib.getCommentByCode(message['commentCode'])
                    entry['itemLink'] = utils.commentLinker(comment)
                    entry['commentData'] = comment['data']
                    
                elif message['extraInfo'] in ['commentOnPhoto', 'commentOnInitiative']:
                    entry['combinedInfo'] = 'commentOnPhotoOnInitiative'
                    comment = commentLib.getCommentByCode(message['commentCode'])
                    entry['itemLink'] = utils.commentLinker(comment)
                    entry['commentData'] = comment['data']
                    
                elif message['extraInfo'] in ['commentOnOrgGeneral']:
                    entry['combinedInfo'] = 'commentOnOrgGeneral'
                    comment = commentLib.getCommentByCode(message['commentCode'])
                    entry['itemLink'] = utils.commentLinker(comment)
                    entry['commentData'] = comment['data']
                    
                elif message['extraInfo'] in ['commentOnOrgPosition']:
                    entry['combinedInfo'] = 'commentOnOrgPosition'
                    comment = commentLib.getCommentByCode(message['commentCode'])
                    entry['itemLink'] = utils.commentLinker(comment)
                    entry['commentData'] = comment['data']
                    
                elif message['extraInfo'] in ['commentOnResource']:
                    if 'workshopCode' in message:
                        container = workshopLib.getWorkshopByCode(message['workshopCode'])
                    elif 'initiativeCode' in message:
                        container = initiativeLib.getInitiative(message['initiativeCode'])
                    entry['itemTitle'] = container['title']
                    entry['combinedInfo'] = 'commentOnResource'
                    comment = commentLib.getCommentByCode(message['commentCode'])
                    entry['itemLink'] = utils.commentLinker(comment)
                    entry['commentData'] = comment['data']
                    
                elif message['extraInfo'] in ['commentOnUpdate']:
                    if 'workshopCode' in message:
                        container = workshopLib.getWorkshopByCode(message['workshopCode'])
                    elif 'initiativeCode' in message:
                        container = initiativeLib.getInitiative(message['initiativeCode'])
                    entry['itemTitle'] = container['title']
                    entry['combinedInfo'] = 'commentOnUpdate'
                    comment = commentLib.getCommentByCode(message['commentCode'])
                    entry['itemLink'] = utils.commentLinker(comment)
                    entry['commentData'] = comment['data']
                    
                elif message['extraInfo'] in ['disabledPhoto', 'enabledPhoto', 'deletedPhoto']:
                    entry['combinedInfo'] = 'disabledEnabledDeletedPhoto'
                    photoCode = message['photoCode']
                    thing = generic.getThing(photoCode)
                    title = thing['title']
                    if message['extraInfo'] in ['disabledPhoto']:
                        event = eventLib.getEventsWithAction(message, 'disabled')
                    elif message['extraInfo'] in ['enabledPhoto']:
                        event = eventLib.getEventsWithAction(message, 'enabled')
                    elif message['extraInfo'] in ['deletedPhoto']:
                        event = eventLib.getEventsWithAction(message, 'deleted')
                        
                    entry['eventAction'] = event[0]['action']
                    entry['eventReason'] = event[0]['reason']
                    
                    # note: assuming this message is about the logged in user's own photo
                    entry['itemLink'] = utils.photoLink(photoCode, c.user)
                    entry['itemTitle'] = title
                    
                elif message['extraInfo'] in ['disabledInitiative', 'enabledInitiative', 'deletedInitiative']:
                    entry['combinedInfo'] = 'disabledEnabledDeletedInitiative'
                    initiativeCode = message['initiativeCode']
                    thing = generic.getThing(initiativeCode)
                    entry['itemTitle'] = thing['title']
                    if message['extraInfo'] in ['disabledInitiative']:
                        event = eventLib.getEventsWithAction(message, 'disabled')
                    elif message['extraInfo'] in ['enabledInitiative']:
                        event = eventLib.getEventsWithAction(message, 'enabled')
                    elif message['extraInfo'] in ['deletedInitiative']:
                        event = eventLib.getEventsWithAction(message, 'deleted')
                        
                    entry['eventAction'] = event[0]['action']
                    entry['eventReason'] = event[0]['reason']
                    
                    entry['itemLink'] = utils.initiativeLink(thing)
                    
                elif message['extraInfo'] in ['disabledInitiativeResource', 'enabledInitiativeResource', 'deletedInitiativeResource']:
                    entry['combinedInfo'] = 'disabledEnabledDeletedInitiativeResource'
                    resourceCode = message['resourceCode']
                    thing = generic.getThing(resourceCode)
                    entry['itemTitle'] = thing['title']
                    if message['extraInfo'] in ['disabledInitiativeResource']:
                        event = eventLib.getEventsWithAction(message, 'disabled')
                    elif message['extraInfo'] in ['enabledInitiativeResource']:
                        event = eventLib.getEventsWithAction(message, 'enabled')
                    elif message['extraInfo'] in ['deletedInitiativeResource']:
                        event = eventLib.getEventsWithAction(message, 'deleted')
                        
                    entry['eventAction'] = event[0]['action']
                    entry['eventReason'] = event[0]['reason']
                    
                    entry['itemLink'] = utils.initiativeURL(thing)
                    #Your initiative resource:
                    #href="/initiative/thing['initiativeCode']/thing['initiative_url']/resource/thing['urlCode']/thing['url']" class="green green-hover">title

                elif message['extraInfo'] in ['disabledInitiativeUpdate', 'enabledInitiativeUpdate', 'deletedInitiativeUpdate']:
                    entry['combinedInfo'] = 'disabledEnabledDeletedInitiativeUpdate'
                    if 'updateCode' in message:
                        updateCode = message['updateCode']
                    else:
                        updateCode = message['discussionCode']
                    thing = generic.getThing(updateCode)
                    entry['itemTitle'] = thing['title']

                    if message['extraInfo'] in ['disabledInitiativeUpdate']:
                        event = eventLib.getEventsWithAction(message, 'disabled')
                    elif message['extraInfo'] in ['enabledInitiativeUpdate']:
                        event = eventLib.getEventsWithAction(message, 'enabled')
                    elif message['extraInfo'] in ['deletedInitiativeUpdate']:
                        event = eventLib.getEventsWithAction(message, 'deleted')
                        
                    entry['eventAction'] = event[0]['action']
                    entry['eventReason'] = event[0]['reason']
                    
                    entry['itemLink'] = utils.initiativeURL(thing)
                    #Your initiative update:
                    #href="/initiative/thing['initiativeCode']/thing['initiative_url']/updateShow/thing['urlCode']" class="green green-hover">title

                elif message['extraInfo'] in ['disabled', 'enabled', 'deleted', 'adopted']:
                    entry['combinedInfo'] = 'disabledEnabledDeletedAdopted'
                    event = eventLib.getEventsWithAction(message, message['extraInfo'])
                    if not event:
                        continue
                        
                    # Mako was bugging out on me when I tried to do this with sets
                    codeTypes = ['commentCode', 'discussionCode', 'ideaCode', 'resourceCode', 'initiativeCode']
                    thing = None
                    for codeType in codeTypes:
                        if codeType in message.keys():
                            thing = generic.getThing(message[codeType])
                            break
                    if thing is None:
                        continue
                    if 'workshopCode' in thing:
                        parent = generic.getThing(thing['workshopCode'])
                    elif 'initiativeCode' in thing:
                        parent = generic.getThing(thing['initiativeCode'])
                    elif 'resourceCode' in thing:
                        parent = generic.getThing(thing['resourceCode'])
                    
                    entry['eventAction'] = event[0]['action']
                    entry['eventReason'] = event[0]['reason']
                    
                    entry['itemLink'] = utils.thingURL(parent, thing)
                    if thing.objType == 'comment':
                        entry['itemTitle'] = thing['data']
                    else:
                        entry['itemTitle'] = thing['title']

            except:
                log.info('error in message type: %s'%(message['extraInfo']))
                pass

            #log.info('combinedInfo: %s, extraInfo: %s' %(entry['combinedInfo'], message['extraInfo']))
            result.append(entry)

        # if there is a limit query, len(c.messages) no longer works. so, we look for it here instead
        if len(result) == 0:
            return json.dumps({'statusCode':1})
        return json.dumps({'statusCode': 0, 'result': result})
        