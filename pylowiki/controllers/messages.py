import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, redirect

from pylowiki.lib.base import BaseController, render

import pylowiki.lib.db.message      as messageLib
import pylowiki.lib.db.dbHelpers    as dbHelpers
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.listener     as listenerLib
import pylowiki.lib.db.facilitator  as facilitatorLib
import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.initiative   as initiativeLib
import pylowiki.lib.db.comment      as commentLib
import pylowiki.lib.db.event        as eventLib
import pylowiki.lib.db.generic      as generic

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
                if c.user.id == c.authuser.id or c.isAdmin:
                    c.messages = messageLib.getMessages(c.user)
                    c.unreadMessageCount = messageLib.getMessages(c.user, read = u'0', count = True)
                    
            else:
                log.info('user not in session')
                session['afterLoginURL'] = session._environ['PATH_INFO']
                log.info('message ctrl %s' % session['afterLoginURL'])
                session.save()
                return redirect('/login')
        

    def markRead(self, urlCode):
        self.error = False
        self.message = messageLib.getMessage(c.authuser, urlCode)
        if not self.message:
            self.error = True

        if self.error:
            return "Error"
        self.message['read'] = u'1'
        dbHelpers.commit(self.message)
        return "OK"

    def showUserMessages(self, id1, id2, id3 = ''):
        return render("/derived/6_messages_old.bootstrap")

    def getUserMessages(self, id1, id2, id3 = ''):
        if not c.messages:
            log.info("getUserMessages return NOT messages")
            return json.dumps({'statusCode':2})
        if len(c.messages) == 0:
            log.info("getUserMessages return len messages == 0")
            return json.dumps({'statusCode':2})

        result = []

        for message in c.messages:
            # if this field isn't in the message then nothing happens for this entry
            if 'extraInfo' in message.keys():
                continue
            # now that we've asserted this fact, we can check one more thing that takes a bit more time
            if 'commentCode' in message and not commentLib.getCommentByCode(message['commentCode']):
                continue
            
            entry = {}
            entry['rowClass'] = ''
            entry['read'] = message['read']
            entry['userName'] = 'Civinomics'
            entry['userLink'] = '#'
            entry['userImage'] = utils.civinomicsAvatar()
            entry['messageTitle'] = ''
            entry['messageText'] = ''
            entry['messageCode'] = ''
            entry['messageDate'] = message.date
            entry['responseAction'] = ''
            entry['formStr'] = ''
            entry['action'] = ''
            entry['itemCode'] = ''
            entry['itemImage'] = ''
            entry['itemLink'] = ''
            entry['itemTitle'] = ''
            entry['itemUrl'] = ''
            entry['commentData'] = ''
            entry['extraInfo'] = message['extraInfo']
            entry['eventAction'] = ''
            entry['eventReason'] = ''

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
            if 'messageText' in message:
                entry['messageText'] = message['messageText']
            if 'messageCode' in message:
                entry['messageCode'] = message['urlCode']
            if 'read' in message:
                entry['read'] = message['read']


            if message['extraInfo'] in ['listenerInvite', 'facilitationInvite']:
                workshop = workshopLib.getWorkshopByCode(message['workshopCode'])
                if message['extraInfo'] == 'listenerInvite':
                    entry['formStr'] = """<form method="post" name="inviteListener" id="inviteListener" action="/profile/%s/%s/listener/response/handler/">""" %(c.user['urlCode'], c.user['url'])
                    entry['action'] = 'be a listener for'
                    # note: commenting out this next line because it appears to not be used or needed anymore
                    # role = listenerLib.getListenerByCode(message['listenerCode'])
                else:
                    entry['formStr'] = """<form method="post" name="inviteFacilitate" id="inviteFacilitate" action="/profile/%s/%s/facilitate/response/handler/">""" %(c.user['urlCode'], c.user['url'])
                    entry['action'] = 'facilitate'
                    # note: commenting out this next line because it appears to not be used or needed anymore
                    # role = facilitatorLib.getFacilitatorByCode(message['facilitatorCode'])
                entry['itemCode'] = workshop['urlCode']
                entry['itemUrl'] = workshop['url']
                entry['itemTitle'] = workshop['Title'] 
                entry['itemLink'] = utils.workshopLink(workshop)
                entry['itemImage'] = utils.workshopImage(workshop)
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
                
                workshop = workshopLib.getWorkshopByCode(message['workshopCode'])
                entry['itemTitle'] = workshop['title']
                entry['itemLink'] = utils.workshopLink(workshop)
                entry['messageTitle'] = message['title']
                entry['messageText'] = message['text']
                entry['messageDate'] = message.date
                
            elif message['extraInfo'] in ['authorInvite']:

                initiative = initiativeLib.getInitiative(message['initiativeCode'])
                entry['formStr'] = """<form method="post" name="inviteFacilitate" id="inviteFacilitate" action="/profile/%s/%s/facilitate/response/handler/">""" %(c.user['urlCode'], c.user['url'])
                entry['action'] = 'coauthor'
                # note: commenting out this next line because it appears to not be used or needed anymore
                # role = facilitatorLib.getFacilitatorByCode(message['facilitatorCode'])
                entry['itemCode'] = initiative['urlCode']
                entry['itemImage'] = utils.initiativeImageURL(initiative)
                entry['itemLink'] = utils.initiativeURL(initiative)
                entry['itemTitle'] = initiative['title']
                entry['itemUrl'] = initiative['url']

                entry['messageDate'] = message.date
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
                initiative = initiativeLib.getInitiative(message['initiativeCode'])
                entry['itemTitle'] = initiative['title']

            elif message['extraInfo'] in ['commentResponse']:
                comment = commentLib.getCommentByCode(message['commentCode'])
                workshop = workshopLib.getWorkshopByCode(comment['workshopCode'])
                        
                entry['itemLink'] = utils.commentLink(comment, workshop)
                entry['commentData'] = comment['data']
                
            elif message['extraInfo'] in ['commentOnPhoto', 'commentOnInitiative']:
                
                comment = commentLib.getCommentByCode(message['commentCode'])
                entry['itemLink'] = utils.commentLink(comment, c.user)
                entry['commentData'] = comment['data']
                
            elif message['extraInfo'] in ['commentOnResource']:
                
                comment = commentLib.getCommentByCode(message['commentCode'])
                resource = generic.getThing(comment['resourceCode'])
                
                # note: gonna need to decide how best to give these links their titles
                entry['itemLink'] = utils.commentLink(comment, resource)
                entry['commentData'] = comment['data']
                
            elif message['extraInfo'] in ['commentOnUpdate']:
                
                comment = commentLib.getCommentByCode(message['commentCode'])
                update = generic.getThing(comment['discussionCode'])
                
                entry['itemLink'] = utils.commentLink(comment, update)
                entry['commentData'] = comment['data']
                
            elif message['extraInfo'] in ['disabledPhoto', 'enabledPhoto', 'deletedPhoto']:
                
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
                
                entry['itemLink'] = utils.photoLink(c.user, photoCode)
                
            elif message['extraInfo'] in ['disabledInitiative', 'enabledInitiative', 'deletedInitiative']:
                
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
                
                entry['itemLink'] = utils.initiativeResourceLink(thing)
                #Your initiative resource:
                #href="/initiative/thing['initiativeCode']/thing['initiative_url']/resource/thing['urlCode']/thing['url']" class="green green-hover">title

            elif message['extraInfo'] in ['disabledInitiativeUpdate', 'enabledInitiativeUpdate', 'deletedInitiativeUpdate']:
                
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
                
                entry['itemLink'] = utils.initiativeUpdateLink(thing)
                #Your initiative update:
                #href="/initiative/thing['initiativeCode']/thing['initiative_url']/updateShow/thing['urlCode']" class="green green-hover">title

            elif message['extraInfo'] in ['disabled', 'enabled', 'deleted', 'adopted']:
                
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
                
                #You posted:
                if thing.objType == 'comment':
                    entry['itemLink'] = utils.thingLinkRouter(thing, parent, commentCode=thing['urlCode'])
                    entry['itemTitle'] = thing['data']
                else:
                    entry['itemLink'] = utils.thingLinkRouter(thing, parent)
                    entry['itemTitle'] = thing['title']

                                
        return render("/derived/6_messages.bootstrap")