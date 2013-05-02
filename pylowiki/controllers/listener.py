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
import simplejson as json

log = logging.getLogger(__name__)

class ListenerController(BaseController):
    
    @h.login_required
    def __before__(self, action, userCode = None, workshopCode = None):
        wList = ['listenerResignHandler', 'listenerTitleHandler']
        uList = ['listenerInviteHandler', 'listenerResponseHandler']
        if action in wList and workshopCode is not None and 'userCode' in request.params:
                userCode = request.params['userCode']
                c.user = userLib.getUserByCode(userCode)                
                c.w = workshopLib.getWorkshopByCode(workshopCode)
        elif action in uList and userCode is not None and 'workshopCode' in request.params:
                c.user = userLib.getUserByCode(userCode)
                workshopCode = request.params['workshopCode']
                c.w = workshopLib.getWorkshopByCode(workshopCode)
        elif action == 'listenerNotificationHandler' and userCode is not None and workshopCode is not None:
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
            

    def listenerInviteHandler(self):
        listener = listenerLib.Listener(c.user, c.w, 1)
        alert = {'type':'success'}
        alert['title'] = 'Listener invitation issued.'
        session['alert'] = alert
        session.save()
        
        workshopLib.setWorkshopPrivs(c.w)
        title = 'Listener invitation'
        text = '(This is an automated message)'
        extraInfo = 'listenerInvite'
        m = messageLib.Message(owner = c.user, title = title, text = text, privs = c.privs, workshop = c.w, extraInfo = extraInfo, sender = c.authuser)
        m = generic.linkChildToParent(m, listener)
        dbHelpers.commit(m)
        eventLib.Event('Listener Invitation Issued', '%s issued an invitation to be a listener of %s'%(c.authuser['name'], c.w['title']), m, user = c.authuser, action='extraInfo')
        
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
        user = userLib.getUserByCode(userCode)
        listener = listenerLib.getListener(user, c.w)
        # initialize to current value if any, '0' if not set in object
        iAlerts = '0'
        eAction = ''
        if 'itemAlerts' in listener:
            iAlerts = listener['itemAlerts']
        
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
            return "Error"   
        dbHelpers.commit(listener)
        if eAction != '':
            eventLib.Event('Listener item notifications set', eAction, listener, c.authuser)
        return eAction

            
