# -*- coding: utf-8 -*-
import logging

from pylons import config, request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylowiki.lib.base import BaseController, render

import pylowiki.lib.helpers         as h
import pylowiki.lib.db.listener     as listenerLib
import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.facilitator  as facilitatorLib
import pylowiki.lib.db.event        as eventLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.utils           as utils
import pylowiki.lib.db.dbHelpers    as dbHelpers




log = logging.getLogger(__name__)

class ListenerController(BaseController):

    @h.login_required
    def listenerInviteHandler(self, id1, id2):
        code = id1
        url = id2
        c.user = userLib.get_user(code, url)
        if c.user and 'inviteToListen' in request.params:
            invite = request.params['inviteToListen']
            iList = invite.split("/")
            wCode = iList[0]
            wURL = iList[1]
            w = workshopLib.getWorkshopByCode(wCode)
            listener = listenerLib.Listener(c.user, w, 1)
            eventLib.Event('Listener Invitation Issued', '%s issued an invitation to be a listener of %s'%(c.authuser['name'], w['title']), listener, c.authuser)
            alert = {'type':'success'}
            alert['title'] = 'Listener invitation issued.'
            session['alert'] = alert
            session.save()
            return redirect("/profile/%s/%s"%(code, url))
        else:
            return redirect("/" )

    @h.login_required
    def listenerResponseHandler(self, id1, id2):
        code = id1
        url = id2
        c.user = userLib.get_user(code, utils.urlify(url))
        if 'workshopCode' in request.params and 'workshopURL' in request.params:
            wCode = request.params['workshopCode']
            wURL = request.params['workshopURL']
            w = workshopLib.getWorkshopByCode(wCode)
            listeners = listenerLib.getListenersForUser(c.authuser)
            listener = False
            for l in listeners:
                if l['workshopCode'] == w['urlCode']:
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
                eventLib.Event('Listener Invitation %s'%eAction, '%s %s an invitation to be a listener %s'%(c.user['name'], eAction.lower(), w['title']), listener, c.user)
                alert = {'type':'success'}
                alert['title'] = 'Invitation %s'%eAction
                session['alert'] = alert
                session.save()
                return redirect("/profile/%s/%s"%(code, url))

        return redirect("/" )

    @h.login_required
    def listenerResignHandler(self, id1, id2):
        code = id1
        url = id2
        w = workshopLib.getWorkshopByCode(code)
        if 'userCode' in request.params:
            userCode = request.params['userCode']
            user = userLib.getUserByCode(userCode)
        else:
            abort(404)
            
        if c.authuser.id != user.id and not userLib.isAdmin(c.authuser.id) and not facilitatorLib.isFacilitator(c.authuser.id, w.id):
            abort(404)
            
        listeners = listenerLib.getListenersForUser(user)
        
        listener = False
        for l in listeners:
            if l['workshopCode'] == w['urlCode'] and l['disabled'] != '1':
                listener = l

        if 'resignReason' in request.params:
            resignReason = request.params['resignReason']
            if resignReason == '':
                alert = {'type':'error'}
                alert['title'] = 'Reason for resignation required..'
                session['alert'] = alert
                session.save()
                return redirect("/workshop/%s/%s"%(code, url))
        else:
            alert = {'type':'error'}
            alert['title'] = 'Reason for resignation required..'
            session['alert'] = alert
            session.save()   
            return redirect("/workshop/%s/%s"%(code, url))
            


        if listener:
            listener['disabled'] = '1'
            dbHelpers.commit(listener)
            eventLib.Event('Listener Resigned', '%s resigned as listener of %s: %s'%(user['name'], w['title'], resignReason), listener, c.authuser)
            alert = {'type':'success'}
            alert['title'] = 'Listener resignation accepted.'
            session['alert'] = alert
            session.save()
            return redirect("/workshop/%s/%s"%(code, url))

        return redirect("/workshop/%s/%s"%(code, url))
