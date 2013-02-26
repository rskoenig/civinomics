# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

import webhelpers.paginate as paginate
import pylowiki.lib.helpers as h
from pylons import config

import pylowiki.lib.db.facilitator  as facilitatorLib
import pylowiki.lib.db.event        as eventLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.dbHelpers    as dbhelpersLib
import pylowiki.lib.utils           as utilsLib

from hashlib import md5
import simplejson as json

log = logging.getLogger(__name__)

class FacilitatorController(BaseController):

    def __before__(self, action, code, url):
        if action in ['facilitateInviteHandler', 'facilitateResponseHandler']:
            c.user = userLib.getUserByCode(facilitatorCode)
        elif action in ['facilitateResignHandler', 'facilitatorNotificationHandler']:
            c.w = workshopLib.getWorkshopByCode(code)

    @h.login_required
    def facilitateInviteHandler(self, code, url):
        if c.user and 'inviteToFacilitate' in request.params:
           invite = request.params['inviteToFacilitate']
           iList = invite.split("/")
           wCode = iList[0]
           wURL = iList[1]
           w = workshopLib.getWorkshopByCode(wCode)
           facilitatorLib.Facilitator(c.user, w, 1)
           fList = facilitatorLib.getFacilitatorsByUserAndWorkshop(c.user.id, w.id)
           eventLib.Event('CoFacilitator Invitation Issued', '%s issued an invitation to co facilitate %s'%(c.authuser['name'], w['title']), fList[0], c.authuser)
           alert = {'type':'success'}
           alert['title'] = 'Success. CoFacilitation invitation issued.'
           session['alert'] = alert
           session.save()
           return redirect("/profile/%s/%s"%(code, url))
        else:
           alert = {'type':'error'}
           alert['title'] = 'Authorization Error. You are not authorized.'
           session['alert'] = alert
           session.save()
           return redirect("/" )

    @h.login_required
    def facilitateResponseHandler(self, code, url):
        if 'workshopCode' in request.params and 'workshopURL' in request.params:
            wCode = request.params['workshopCode']
            wURL = request.params['workshopURL']
            c.w = workshopLib.getWorkshop(wCode, utilsLib.urlify(wURL))
            fList = facilitatorLib.getFacilitatorsByUser(c.authuser.id)
            doF = False
            for f in fList:
               if int(f['workshopID']) == int(c.w.id):
                  doF = f

            if doF and 'acceptInvite' in request.params:
                  doF['pending'] = '0'
                  eAction = "Accepted"
                  
            if doF and 'declineInvite' in request.params:
                  doF['pending'] = '0'
                  doF['disabled'] = '1'
                  eAction = "Declined"

            if doF:
                  dbhelpersLib.commit(doF)
                  eventLib.Event('CoFacilitator Invitation %s'%eAction, '%s %s an invitation to co facilitate %s'%(c.user['name'], eAction.lower(), c.w['title']), doF, c.user)
                  # success message
                  alert = {'type':'success'}
                  alert['title'] = 'Success. CoFacilitation Invitation %s.'%eAction
                  session['alert'] = alert
                  session.save()
                  return redirect("/profile/%s/%s"%(code, url))

        alert = {'type':'error'}
        alert['title'] = 'Authorization Error. You are not authorized.'
        session['alert'] = alert
        session.save()
        return redirect("/" )

    @h.login_required
    def facilitateResignHandler(self, code, url):
        fList = facilitatorLib.getFacilitatorsByUser(c.authuser.id, 0)
        doF = False
        for f in fList:
           if int(f['workshopID']) == int(c.w.id) and f['disabled'] != '1':
              doF = f

        if 'resignReason' in request.params:
           resignReason = request.params['resignReason']
           resignReason = resignReason.lstrip()
           resignReason = resignReason.rstrip()
           if resignReason == '':
              alert = {'type':'error'}
              alert['title'] = 'Error. Please include a reason.'
              session['alert'] = alert
              session.save()
              return redirect("/workshop/%s/%s/preferences"%(code, url))

           log.info('resignReason is %s'%resignReason)
        else:
           alert = {'type':'error'}
           alert['title'] = 'Error. Please include a reason.'
           session['alert'] = alert
           session.save()
           return redirect("/workshop/%s/%s"%(code, url))

        if doF and c.authuser.id == doF.owner:
           doF['disabled'] = '1'
           dbhelpersLib.commit(doF)
           eventLib.Event('CoFacilitator Resigned', '%s resigned as cofacilitator of %s: %s'%(c.authuser['name'], w['title'], resignReason), doF, c.authuser)
           alert = {'type':'success'}
           alert['title'] = 'Success. CoFacilitation resignation successful.'
           session['alert'] = alert
           session.save()
           return redirect("/workshop/%s/%s"%(code, url))

        alert = {'type':'error'}
        alert['title'] = 'Authorization Error. You are not authorized.'
        session['alert'] = alert
        session.save()
        return redirect("/workshop/%s/%s"%(code, url))
        
    @h.login_required
    def facilitatorNotificationHandler(self, code, url, userCode):
        user = userLib.getUserByCode(userCode)
        facilitator = facilitatorLib.getFacilitatorInWorkshop(user, c.w)
        # initialize to current value if any, '0' if not set in object
        iAlerts = '0'
        fAlerts = '0'
        eAction = ''
        if 'itemAlerts' in facilitator:
            iAlerts = facilitator['itemAlerts']
        if 'flagAlerts' in facilitator:
            fAlerts = facilitator['flagAlerts']
        
        payload = json.loads(request.body)
        if 'alert' not in payload:
            return "Error"
        alert = payload['alert']
        if alert == 'flags':
            if 'flagAlerts' in facilitator.keys(): # Not needed after DB reset
                if facilitator['flagAlerts'] == u'1':
                    facilitator['flagAlerts'] = u'0'
                    eAction = 'Turned off flag alerts'
                else:
                    facilitator['flagAlerts'] = u'1'
                    eAction = 'Turned on flag alerts'
            else:
                facilitator['flagAlerts'] = u'1'
                eAction = 'Turned on flag alerts'
        elif alert == 'items':
            if 'itemAlerts' in facilitator.keys(): # Not needed after DB reset
                if facilitator['itemAlerts'] == u'1':
                    facilitator['itemAlerts'] = u'0'
                    eAction = 'Turned off item alerts'
                else:
                    facilitator['itemAlerts'] = u'1'
                    eAction = 'Turned on item alerts'
            else:
                facilitator['itemAlerts'] = u'1'
                eAction = 'Turned on item alerts'
        else:
            return "Error"   
        dbhelpersLib.commit(facilitator)
        if eAction != '':
            eventLib.Event('Facilitator notifications set', eAction, facilitator, c.authuser)
        return eAction

