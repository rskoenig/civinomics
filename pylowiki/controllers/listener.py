# -*- coding: utf-8 -*-
import logging

from pylons import config, request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylowiki.lib.base import BaseController, render

import pylowiki.lib.helpers         as h
import pylowiki.lib.db.listener     as listenerLib
import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.facilitator  as facilitatorLib
import pylowiki.lib.db.message      as messageLib
import pylowiki.lib.db.event        as eventLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.utils           as utils
import pylowiki.lib.db.dbHelpers    as dbHelpers
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.mail            as mailLib
import simplejson as json

log = logging.getLogger(__name__)

class ListenerController(BaseController):
    
    @h.login_required
    def __before__(self, action, userCode = None, workshopCode = None):
        wList = ['listenerResignHandler', 'listenerTitleHandler']
        uList = ['listenerInviteHandler', 'listenerResponseHandler']
        adminList = ['listenerNotificationHandler', 'listenerAddHandler', 'listenerDisableHandler', 'listenerEmailHandler', 'listenerListHandler', 'listenerEditHandler', 'listenerSuggestHandler']
        if action in wList and workshopCode is not None and 'userCode' in request.params:
                userCode = request.params['userCode']
                c.user = userLib.getUserByCode(userCode)                
                c.w = workshopLib.getWorkshopByCode(workshopCode)
        elif action in uList and userCode is not None and 'workshopCode' in request.params:
                c.user = userLib.getUserByCode(userCode)
                workshopCode = request.params['workshopCode']
                c.w = workshopLib.getWorkshopByCode(workshopCode)
        elif (action in adminList) and userCode is not None and workshopCode is not None:
                c.user = userLib.getUserByCode(userCode)
                c.w = workshopLib.getWorkshopByCode(workshopCode)
        else:
            abort(404)
            
        if action == 'listenerResponseHandler':
            if 'messageCode' not in request.params:
                abort(404)
            message = messageLib.getMessage(c.user, request.params['messageCode'])
            if not message:
                abort(404)
            self.message = message
        
        if not c.user or not c.w:
            abort(404)
            
    @h.login_required
    def listenerAddHandler(self):   
        payload = json.loads(request.body)
        if 'lName' not in payload or 'lTitle' not in payload or 'lEmail' not in payload:
            return "Error"
        lName = payload['lName']
        lTitle = payload['lTitle']
        lEmail = payload['lEmail']
        if not lName or not lTitle or not lEmail:
            return "Please enter complete information"
        # make sure not already a listener for this workshop
        listener = listenerLib.getListener(lEmail, c.w)
        if not listener:
            listener = listenerLib.Listener(lName, lTitle, lEmail, c.w, "0")
            user = userLib.getUserByEmail(lEmail)
            if user:
                userImage = generic.userImageSource(user)
                profileLink = "/profile/" + user['urlCode'] + "/" + user['url']
                lState = 'Active'
                eventLib.Event('Active Listener Added', '%s added as listener'%user['name'], listener, user = c.authuser)
            else:
                userImage = "/images/glyphicons_pro/glyphicons/png/glyphicons_003_user.png"
                profileLink = ''
                lState = 'Pending'
                eventLib.Event('Pending Listener Added', '%s added as listener'%lName, listener, user = c.authuser)
            mailLib.sendListenerAddMail(listener['email'], c.authuser, c.w)
            jsonReturn = '{"urlCode":"' + listener['urlCode'] + '","lName":"' + listener['name'].replace("'", "&#39;") + '", "lTitle":"' + listener['title'].replace("'", "&#39;") + '", "lEmail":"' + listener['email'] + '", "profileLink":"' + profileLink + '","userImage":"' + userImage + '", "button":"Disable","state":"' + lState + '"}'
            return jsonReturn
        else:
            return '{"state":"Error", "errorMessage":"Already a Listener!"}'
            
    @h.login_required
    def listenerEditHandler(self):   
        payload = json.loads(request.body)
        if 'lName' not in payload or 'lTitle' not in payload or 'lEmail' not in payload or 'urlCode' not in payload:
            return "Error"
        lName = payload['lName']
        lTitle = payload['lTitle']
        lEmail = payload['lEmail']
        urlCode = payload['urlCode']
        if not lName or not lTitle or not lEmail:
            return "Please enter complete information"
        listener = listenerLib.getListenerByCode(urlCode)
        if not listener:
            return 'No such listener!'
        listener['name'] = lName;
        listener['title'] = lTitle;
        listener['email'] = lEmail;
        dbHelpers.commit(listener)
        eventLib.Event('Listener edited', '%s edited listener info'%c.authuser['name'], listener, user = c.authuser)
        return "Updated Listener."
            
    @h.login_required
    def listenerDisableHandler(self):
        payload = json.loads(request.body)
        if 'lReason' not in payload:
            return "Error no lReason"
        if 'urlCode' not in payload:
            return "Error no urlCode"
        lReason = payload['lReason']
        urlCode = payload['urlCode']
        if not lReason or not urlCode:
            return "Please enter complete information"
        # make sure not already a listener for this workshop
        listener = listenerLib.getListenerByCode(urlCode)

        if not listener:
            return 'No such Listener!'
        if listener['disabled'] == '1':
            listener['disabled'] = '0';
            dbHelpers.commit(listener)
            returnMsg = "Listener Enabled!"
        if listener['disabled'] == '0':
            listener['disabled'] = '1';
            dbHelpers.commit(listener)
            returnMsg = "Listener Disabled!"
            
        if 'userCode' in listener:
            user = userLib.getUserByCode(listener['userCode'])
            lKey = 'listener_counter'
            if lKey in user:
                lValue = int(user[lKey])
                if listener['disabled'] == '0':
                    lValue += 1
                else:
                    lValue -= 1
            else:
                if listener['disabled'] == '0':
                    lValue = 1
                else:
                    lValue = 0
            user[lKey] = str(lValue)
            dbHelpers.commit(user)
            
        eventLib.Event(returnMsg, '%s by %s'%(returnMsg, c.authuser['name']), listener, user = c.authuser)
            
    @h.login_required
    def listenerEmailHandler(self):   
        payload = json.loads(request.body)
        if 'urlCode' not in payload or 'memberMessage' not in payload:
            return "Error no urlCode or memberMessage"
        urlCode = payload['urlCode']
        memberMessage = payload['memberMessage']
        # make sure not already a listener for this workshop
        listener = listenerLib.getListenerByCode(urlCode)
        if listener['invites'] != '':
            inviteList = listener['invites'].split(",")
            numInvites = str(len(inviteList))
        else:
            inviteList = []
            numInvites = '0'
        if c.user['urlCode'] in inviteList:
            return "You have already sent an invitiation to this person for this workshop!"
        mailLib.sendListenerInviteMail(listener['email'], c.authuser, c.w, memberMessage, numInvites)
        inviteList.append(c.user['urlCode'])
        listener['invites'] = ",".join(inviteList)
        dbHelpers.commit(listener)
        eventLib.Event('Listener invitation sent', 'Listener invitation sent by %s: %s'%(c.authuser['name'], memberMessage), listener, user = c.authuser)
        return "Invitation sent. Thanks!"
        
    @h.login_required
    def listenerSuggestHandler(self):   
        payload = json.loads(request.body)
        if 'suggestListener' not in payload:
            return "Error no suggestListener"
        suggestListener = payload['suggestListener']
        facilitators = facilitatorLib.getFacilitatorsByWorkshop(c.w)
        sMessage = suggestListener
        sTitle = "Listener Suggestion"
        workshopLib.setWorkshopPrivs(c.w)
        for facilitator in facilitators:
            fUser = userLib.getUserByID(facilitator.owner)
            message = messageLib.Message(owner = fUser, title = sTitle, text = sMessage, sender = c.authuser, privs = c.privs, workshop = c.w, extraInfo = "listenerSuggestion")
        return "Suggestion sent. Thanks!"
        
    @h.login_required
    def listenerListHandler(self):
        activeEnabled = []
        pendingEnabled = []
        activeDisabled = []
        pendingDisabled = []
        
        log.info('listenerListHandler')
        enabled = listenerLib.getListenersForWorkshop(c.w)
        for l in enabled:
            if 'userCode' in l:
                activeEnabled.append(l)
            else:
                pendingEnabled.append(l)
                
        disabled = listenerLib.getListenersForWorkshop(c.w, '1')
        for l in disabled:
            if 'userCode' in l:
                activeDisabled.append(l)
            else:
                pendingDisabled.append(l)
                    
        jsonReturn = '{ "listeners": ['
        comma = ''
        for l in activeEnabled:
            user = userLib.getUserByCode(l['userCode'])
            userImage = generic.userImageSource(user)
            profileLink = "/profile/" + user['urlCode'] + "/" + user['url']
            jsonReturn += comma + '{"urlCode":"' + l['urlCode'] + '","lName":"' + l['name'].replace("'", "&#39;") + '", "lTitle":"' + l['title'].replace("'", "&#39;") + '", "lEmail":"' + l['email'] + '", "profileLink":"' + profileLink + '","userImage":"' + userImage + '", "button":"Disable","state":"Active"}'
            comma = ','
 
        if not activeEnabled:
            comma = ''
        userImage = "/images/glyphicons_pro/glyphicons/png/glyphicons_003_user.png"
        profileLink = ""
        for l in pendingEnabled:
            jsonReturn += comma + '{"urlCode":"' + l['urlCode'] + '","lName":"' + l['name'].replace("'", "&#39;") + '", "lTitle":"' + l['title'].replace("'", "&#39;") + '", "lEmail":"' + l['email'] + '", "profileLink":"' + profileLink + '","userImage":"' + userImage + '", "button":"Disable","state":"Pending"}'
            comma = ','

        if not activeEnabled and not pendingEnabled:
            comma = ''
        for l in activeDisabled:
            user = userLib.getUserByCode(l['userCode'])
            userImage = generic.userImageSource(user)
            profileLink = "/profile/" + user['urlCode'] + "/" + user['url']
            jsonReturn += comma + '{"urlCode":"' + l['urlCode'] + '","lName":"' + l['name'].replace("'", "&#39;") + '", "lTitle":"' + l['title'].replace("'", "&#39;") + '", "lEmail":"' + l['email'] + '", "profileLink":"' + profileLink + '","userImage":"' + userImage + '", "button":"Enable","state":"Active"}'
            comma = ','

        if not activeEnabled and not pendingEnabled and not activeDisabled:
            comma = ''
        userImage = "/images/glyphicons_pro/glyphicons/png/glyphicons_003_user.png"
        profileLink = ''
        for l in pendingDisabled:
            jsonReturn += comma + '{"urlCode":"' + l['urlCode'] + '","lName":"' + l['name'].replace("'", "&#39;") + '", "lTitle":"' + l['title'].replace("'", "&#39;") + '", "lEmail":"' + l['email'] + '", "profileLink":"' + profileLink + '","userImage":"' + userImage + '", "button":"Enable","state":"Pending"}'
            comma = ','
        jsonReturn += "]}"
        
        return jsonReturn

            
    def listenerInviteHandler(self):
        listener = listenerLib.getListener(c.user['email'], c.w)
        lTitle = ''
        if 'lTitle' in request.params:
            lTitle = request.params['lTitle']
        if not listener:
            listener = listenerLib.Listener(c.user['name'], lTitle, c.user['email'], c.w, "0")
        else:
            listener['disabled'] = '0'
            listener['title'] = lTitle
            dbHelpers.commit(listener)
        
        return redirect("/profile/%s/%s"%(c.user['urlCode'], c.user['url']))

    def listenerResponseHandler(self):
        listeners = listenerLib.getListenersForUser(c.authuser)
        listener = False
        for l in listeners:
            if l['workshopCode'] == c.w['urlCode']:
                listener = l

            if listener and 'acceptInvite' in request.params:
                listener['pending'] = '0'
                eAction = "Accepted"
                
            if listener and 'declineInvite' in request.params:
                listener['pending'] = '0'
                listener['disabled'] = '1'
                eAction = "Declined"

            if listener:
                dbHelpers.commit(listener)
                eventLib.Event('Listener Invitation %s'%eAction, '%s %s an invitation to be a listener %s'%(c.user['name'], eAction.lower(), c.w['title']), self.message, user = c.user, action = eAction.lower())
                alert = {'type':'success'}
                alert['title'] = 'Invitation %s'%eAction
                session['alert'] = alert
                session.save()
                
                self.message['read'] = u'1'
                dbHelpers.commit(self.message)
                
                return redirect("/profile/%s/%s"%(c.user['urlCode'], c.user['url']))
                
        abort(404)

    def listenerResignHandler(self):
        if c.authuser.id != c.user.id and not userLib.isAdmin(c.authuser.id) and not facilitatorLib.isFacilitator(c.authuser, c.w):
            abort(404)
            
        listeners = listenerLib.getListenersForUser(c.user)
        
        listener = False
        for l in listeners:
            if l['workshopCode'] == c.w['urlCode'] and l['disabled'] != '1':
                listener = l

        if 'resignReason' in request.params:
            resignReason = request.params['resignReason']
            if resignReason == '':
                alert = {'type':'error'}
                alert['title'] = 'Reason for resignation required..'
                session['alert'] = alert
                session.save()
                return redirect("/workshop/%s/%s"%(c.w['urlCode'], c.w['url']))
        else:
            alert = {'type':'error'}
            alert['title'] = 'Reason for resignation required..'
            session['alert'] = alert
            session.save()   
            return redirect("/workshop/%s/%s"%(c.w['urlCode'], c.w['url']))
            
        if listener:
            listener['disabled'] = '1'
            dbHelpers.commit(listener)
            eventLib.Event('Listener Resigned', '%s resigned as listener of %s: %s'%(c.user['name'], c.w['title'], resignReason), listener, user = c.user, action = 'resigned', reason = resignReason)
            alert = {'type':'success'}
            alert['title'] = 'Listener resignation accepted.'
            session['alert'] = alert
            session.save()
            return redirect("/workshop/%s/%s"%(c.w['urlCode'], c.w['url']))

        return redirect("/workshop/%s/%s"%(c.w['urlCode'], c.w['url']))

    def listenerTitleHandler(self):
        listener = listenerLib.getListener(c.user, c.w)
        if 'listenerTitle' in request.params:
            title = request.params['listenerTitle']
            listener['title'] = title
            dbHelpers.commit(listener)
            eventLib.Event('Listener Title Updated', '%s updated listener title to %s'%(c.authuser['name'], listener['title']), listener, c.authuser)
            
        return redirect("/workshop/%s/%s/preferences"%(c.w['urlCode'], c.w['url']))
        
    @h.login_required
    def listenerNotificationHandler(self, workshopCode, url, userCode):
        # check to see if this is a request from the iphone app
        iPhoneApp = utils.iPhoneRequestTest(request)

        user = userLib.getUserByCode(userCode)
        listener = listenerLib.getListener(user['email'], c.w)
        # initialize to current value if any, '0' if not set in object
        iAlerts = '0'
        eAction = ''
        if 'itemAlerts' in listener:
            iAlerts = listener['itemAlerts']
        
        if iPhoneApp:
            try:
                alert = request.params['alert']
            except:
                statusCode = 2
                response.headers['Content-type'] = 'application/json'
                #log.info("results workshop: %s"%json.dumps({'statusCode':statusCode, 'result':result}))
                return json.dumps({'statusCode':statusCode, 'result':'error'})
        else:
            payload = json.loads(request.body)
            if 'alert' not in payload:
                return "Error"
            alert = payload['alert']
        if alert == 'items':
            if 'itemAlerts' in listener.keys(): # Not needed after DB reset
                if listener['itemAlerts'] == u'1':
                    listener['itemAlerts'] = u'0'
                    eAction = 'Turned off'
                else:
                    listener['itemAlerts'] = u'1'
                    eAction = 'Turned on'
            else:
                listener['itemAlerts'] = u'1'
                eAction = 'Turned on'
        elif alert == 'digest':
            if 'digest' in listener.keys(): # Not needed after DB reset
                if listener['digest'] == u'1':
                    listener['digest'] = u'0'
                    eAction = 'Turned off'
                else:
                    listener['digest'] = u'1'
                    eAction = 'Turned on'
            else:
                listener['digest'] = u'1'
                eAction = 'Turned on'
        else:
            if iPhoneApp:
                statusCode = 2
                response.headers['Content-type'] = 'application/json'
                #log.info("results workshop: %s"%json.dumps({'statusCode':statusCode, 'result':result}))
                return json.dumps({'statusCode':statusCode, 'result':'error'})
            else:
                return "Error"

        dbHelpers.commit(listener)
        if eAction != '':
            eventLib.Event('Listener item notifications set', eAction, listener, c.authuser)

        if iPhoneApp:
            statusCode = 0
            response.headers['Content-type'] = 'application/json'
            result = eAction
            return json.dumps({'statusCode':statusCode, 'result':result})
        else:
            return eAction

            
