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

            # all fields are initialized here
            entry['formStr'] = ''
            entry['action'] = ''
            entry['responseAction'] = ''
            entry['itemImage'] = ''
            entry['itemLink'] = ''
            entry['itemTitle'] = ''
            entry['itemCode'] = ''
            entry['itemURL'] = ''
            entry['messageText'] = ''
            entry['messageCode'] = message['urlCode']

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

                entry['messageTitle'] = message['title']
                entry['messageText'] = message['text']
                entry['messageDate'] = message.date
                
                if message['read'] == u'1':
                
                    # Since this is tied to the individual message, we will only have one action
                    # The query here should be rewritten to make use of map/reduce for a single query
                    # note: marking this with "note:" so the above statement is noticed more easily
                    event = eventLib.getEventsWithAction(message, 'accepted')
                    if not event:
                        entry['responseAction'] = 'declining'
                    else:
                        entry['responseAction'] = 'accepting'

                    
                    entry['itemImageClass'] = utils.whatDoICallThis("pull-left message-workshop-image")
                    

                else:
                    entry['itemImageClass'] = utils.whatDoICallThis("pull-left")
                    entry['button1Name'] =  "acceptInvite" 
                    entry['button1Type'] = "submit"
                    entry['button1Class'] = "btn btn-mini btn-civ" 
                    entry['button1Title'] = "Accept the invitation to " + action + " the workshop"
                    entry['button1Text'] = "Accept"

                    entry['button2Name'] =  "declineInvite"
                    entry['button2Type'] = "submit"
                    entry['button2Class'] = "btn btn-mini btn-danger" 
                    entry['button2Title'] = "Decline the invitation to " + action + " the workshop"
                    entry['button2Text'] = "Decline"
                
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
                entry['itemImage'] = lib_6.initiativeImage(initiative)
                entry['itemTitle'] = initiative['title']
                entry['itemCode'] = initiative['urlCode']
                entry['itemURL'] = initiative['url']
                entry['messageTitle'] = message['title']
                entry['itemLink'] = lib_6.initiativeLink(initiative)
                entry['messageText'] = message['text']
                entry['messageDate'] = message.date

                # * *
                if message['read'] == u'1':
                    
                    # Since this is tied to the individual message, we will only have one action
                    # The query here should be rewritten to make use of map/reduce for a single query
                    event = eventLib.getEventsWithAction(message, 'accepted')
                    if not event:
                        entry['responseAction'] = 'declining'
                    else:
                        entry['responseAction'] = 'accepting'
                    " invites you to facilitate "
                    # (You have already responded by response Action)
                else:
                    # invites you to action 
                    #acceptInvite" class="btn btn-mini btn-civ"
                    #declineInvite" class="btn btn-mini btn-danger"

            elif message['extraInfo'] in ['authorResponse']:
                # (:                
                initiative = initiativeLib.getInitiative(message['initiativeCode'])
                
                message['title']
                lib_6.userLink(sender)
                message['text'] 
                lib_6.initiativeLink(initiative)
                initiative['title']
                message.date

            elif message['extraInfo'] in ['commentResponse']:
                comment = commentLib.getCommentByCode(message['commentCode'])
                workshop = workshopLib.getWorkshopByCode(comment['workshopCode'])
                
                lib_6.userLink(sender) 
                message['title']
                        
                lib_6.thingLinkRouter(comment, workshop, embed=True, commentCode=comment['urlCode'])
                comment['data']
                message['text']
                    
                
            elif message['extraInfo'] in ['commentOnPhoto', 'commentOnInitiative']:
                
                comment = commentLib.getCommentByCode(message['commentCode'])
                
                lib_6.userLink(sender) 
                message['title']
                lib_6.thingLinkRouter(comment, c.user, embed=True, commentCode=comment['urlCode'])
                comment['data']
                message['text']                                
                
            elif message['extraInfo'] in ['commentOnResource']:
                
                comment = commentLib.getCommentByCode(message['commentCode'])
                resource = generic.getThing(comment['resourceCode'])
                
                lib_6.userLink(sender) 
                message['title']
                lib_6.thingLinkRouter(comment, resource, embed=True, commentCode=comment['urlCode'])
                comment['data']
                message['text']
                message.date
                
            elif message['extraInfo'] in ['commentOnUpdate']:
                
                comment = commentLib.getCommentByCode(message['commentCode'])
                update = generic.getThing(comment['discussionCode'])
                
                
                lib_6.userLink(sender) 
                message['title']
                lib_6.thingLinkRouter(comment, update, embed=True, commentCode=comment['urlCode'])
                comment['data']
                message['text']
                message.date
                    
                
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
                    
                action = event[0]['action']
                reason = event[0]['reason']
                
                message['title']
                # It was action because: reason
                #Your photo:
                #href="/profile/
                #c.user['urlCode']/
                #c.user['url']
                #/photo/show/photoCode" class="green green-hover">title
                        
                if 'text' in message:
                    message['text']                                
                
            elif message['extraInfo'] in ['disabledInitiative', 'enabledInitiative', 'deletedInitiative']:
                
                initiativeCode = message['initiativeCode']
                thing = generic.getThing(initiativeCode)
                title = thing['title']
                if message['extraInfo'] in ['disabledInitiative']:
                    event = eventLib.getEventsWithAction(message, 'disabled')
                elif message['extraInfo'] in ['enabledInitiative']:
                    event = eventLib.getEventsWithAction(message, 'enabled')
                elif message['extraInfo'] in ['deletedInitiative']:
                    event = eventLib.getEventsWithAction(message, 'deleted')
                    
                action = event[0]['action']
                reason = event[0]['reason']
                
                
                message['title']
                #It was action because: 
                reason
                #Your initiative:
                #href="/initiative/thing['urlCode']/thing['url']/show
                #title
                        
                if 'text' in message:
                    message['text']
                
            elif message['extraInfo'] in ['disabledInitiativeResource', 'enabledInitiativeResource', 'deletedInitiativeResource']:
                
                resourceCode = message['resourceCode']
                thing = generic.getThing(resourceCode)
                title = thing['title']
                if message['extraInfo'] in ['disabledInitiativeResource']:
                    event = eventLib.getEventsWithAction(message, 'disabled')
                elif message['extraInfo'] in ['enabledInitiativeResource']:
                    event = eventLib.getEventsWithAction(message, 'enabled')
                elif message['extraInfo'] in ['deletedInitiativeResource']:
                    event = eventLib.getEventsWithAction(message, 'deleted')
                    
                action = event[0]['action']
                reason = event[0]['reason']
                
                message['title']</h4>
                #It was action because: reason
                #Your initiative resource:
                #href="/initiative/thing['initiativeCode']/thing['initiative_url']/resource/thing['urlCode']/thing['url']" class="green green-hover">title
                        
                if 'text' in message:
                    message['text']
                
            elif message['extraInfo'] in ['disabledInitiativeUpdate', 'enabledInitiativeUpdate', 'deletedInitiativeUpdate']:
                
                if 'updateCode' in message:
                    updateCode = message['updateCode']
                else:
                    updateCode = message['discussionCode']
                thing = generic.getThing(updateCode)
                title = thing['title']
                if message['extraInfo'] in ['disabledInitiativeUpdate']:
                    event = eventLib.getEventsWithAction(message, 'disabled')
                elif message['extraInfo'] in ['enabledInitiativeUpdate']:
                    event = eventLib.getEventsWithAction(message, 'enabled')
                elif message['extraInfo'] in ['deletedInitiativeUpdate']:
                    event = eventLib.getEventsWithAction(message, 'deleted')
                    
                action = event[0]['action']
                reason = event[0]['reason']
                
                message['title']
                #It was action because: reason
                #Your initiative update:
                #href="/initiative/thing['initiativeCode']/thing['initiative_url']/updateShow/thing['urlCode']" class="green green-hover">title
                        
                if 'text' in message:
                    message['text']
                    
                
            elif message['extraInfo'] in ['disabled', 'enabled', 'deleted', 'adopted']:
                
                event = eventLib.getEventsWithAction(message, message['extraInfo'])
                if not event:
                    continue
                event = event[0]
                    
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
                
                message['title']
                event['action'] 
                #because: 
                event['reason']
                #You posted:
                if thing.objType == 'comment':
                    lib_6.thingLinkRouter(thing, parent, embed=True, commentCode=thing['urlCode']) | n class="green green-hover">thing['data']
                else:
                    lib_6.thingLinkRouter(thing, parent, embed=True) | n class="green green-hover">thing['title']
                        
                        
                message['text']
                
                                
        return render("/derived/6_messages.bootstrap")