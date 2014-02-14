import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, redirect

from pylowiki.lib.base import BaseController, render

import pylowiki.lib.db.message      as messageLib
import pylowiki.lib.db.dbHelpers    as dbHelpers
import pylowiki.lib.db.user         as userLib

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
            if message['read'] == u'0':
                entry['rowClass']= 'warning unread-message'
            # note: should we have an object for Civinomics just as we do for users with a code?
            if message['sender'] == u'0':
                sender = 'Civinomics'
                entry['userLink'] = '#'
                entry['userImage'] = utils.civinomicsAvatar()
            else:
                sender = userLib.getUserByCode(message['sender'])
                entry['userLink'] = lib_6.userLink(sender)
                entry['userImage'] = lib_6.userImage(sender, className="avatar")
            

            # fields used in all if not most of the message types are loaded here
            if 'title' in message:    
                entry['messageTitle'] = message['title']
            else:
                entry['messageTitle'] = ''
            if 'messageText' in message:
                entry['messageText'] = message['messageText']
            else:
                entry['messageText'] = ''
            if 'messageCode' in message:
                entry['messageCode'] = message['urlCode']
            else:
                entry['messageCode'] = ''
            entry['messageDate'] = message.date
            
            entry['responseAction'] = ''

            # all fields are initialized here
            entry['formStr'] = ''
            entry['action'] = ''
            entry['responseAction'] = ''
            
            entry['itemCode'] = ''
            entry['itemImage'] = ''
            entry['itemLink'] = ''
            entry['itemTitle'] = ''
            entry['itemURL'] = ''
            
            entry['commentData'] = ''

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
                entry['itemURL'] = workshop['url']
                entry['itemImage'] = lib_6.workshopImage(workshop)
                entry['itemLink'] = lib_6.workshopLink(workshop)
                entry['itemTitle'] = workshop['title']
                
                if message['read'] == u'1':
                    # Since this is tied to the individual message, we will only have one action
                    # The query here should be rewritten to make use of map/reduce for a single query
                    # note: marking this with "note:" so the above statement is noticed more easily
                    event = eventLib.getEventsWithAction(message, 'accepted')
                    if not event:
                        entry['responseAction'] = 'declining'
                    else:
                        entry['responseAction'] = 'accepting'
                    # note: I should be doing this in the template
                    #entry['itemImageClass'] = utils.whatDoICallThis("pull-left message-workshop-image")
                #else:
                    # note: I should be doing this in the template
                    #entry['itemImageClass'] = utils.whatDoICallThis("pull-left")
                    #...
                    #entry['button2Text'] = "Decline"
                
            elif message['extraInfo'] in ['listenerSuggestion']:
                
                entry['itemTitle'] = workshop['title']
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
                entry['itemImage'] = lib_6.initiativeImage(initiative)
                entry['itemLink'] = lib_6.initiativeLink(initiative)
                entry['itemTitle'] = initiative['title']
                entry['itemURL'] = initiative['url']

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
                        
                entry['itemLink'] = lib_6.thingLinkRouter(comment, workshop, embed=True, commentCode=comment['urlCode'])
                entry['commentData'] = comment['data']
                
            elif message['extraInfo'] in ['commentOnPhoto', 'commentOnInitiative']:
                
                comment = commentLib.getCommentByCode(message['commentCode'])
                entry['itemLink'] = lib_6.thingLinkRouter(comment, c.user, embed=True, commentCode=comment['urlCode'])
                entry['commentData'] = comment['data']
                
            elif message['extraInfo'] in ['commentOnResource']:
                
                comment = commentLib.getCommentByCode(message['commentCode'])
                resource = generic.getThing(comment['resourceCode'])
                
                entry['itemLink'] = lib_6.thingLinkRouter(comment, resource, embed=True, commentCode=comment['urlCode'])
                entry['commentData'] = comment['data']
                
            elif message['extraInfo'] in ['commentOnUpdate']:
                
                comment = commentLib.getCommentByCode(message['commentCode'])
                update = generic.getThing(comment['discussionCode'])
                
                entry['itemLink'] = lib_6.thingLinkRouter(comment, update, embed=True, commentCode=comment['urlCode'])
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
                    
                event['action'] = event[0]['action']
                event['reason'] = event[0]['reason']
                
                # note: make photo link?
                # It was action because: reason
                #Your photo:
                #href="/profile/
                #c.user['urlCode']/
                #c.user['url']
                #/photo/show/photoCode" class="green green-hover">title
                
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
                    
                event['action'] = event[0]['action']
                event['reason'] = event[0]['reason']
                
                
                entry['itemLink'] = lib_6.initiativeLink(thing)
                
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
                    
                event['action'] = event[0]['action']
                event['reason'] = event[0]['reason']
                
                entry['itemLink'] = lib_6.initiativeResourceLink(thing)
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
                    
                event['action'] = event[0]['action']
                event['reason'] = event[0]['reason']
                
                entry['itemLink'] = lib_6.initiativeUpdateLink(thing)
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
                
                event['action'] = event[0]['action']
                event['reason'] = event[0]['reason']
                
                #You posted:
                if thing.objType == 'comment':
                    entry['itemLink'] = lib_6.thingLinkRouter(thing, parent, embed=True, commentCode=thing['urlCode']) | n class="green green-hover">thing['data']
                else:
                    entry['itemLink'] = lib_6.thingLinkRouter(thing, parent, embed=True) | n class="green green-hover">thing['title']

                                
        return render("/derived/6_messages.bootstrap")