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

log = logging.getLogger(__name__)

class FacilitatorController(BaseController):

    @h.login_required
    def facilitateInviteHandler(self, id1, id2):
        code = id1
        url = id2
        c.user = userLib.get_user(code, utilsLib.urlify(url))
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
    def facilitateResponseHandler(self, id1, id2):
        code = id1
        url = id2
        c.user = userLib.get_user(code, utilsLib.urlify(url))
        if 'workshopCode' in request.params and 'workshopURL' in request.params:
            wCode = request.params['workshopCode']
            wURL = request.params['workshopURL']
            ##log.info('coFacilitateHandler %s %s' % (wCode, wURL))
            w = workshopLib.getWorkshop(wCode, utilsLib.urlify(wURL))
            fList = facilitatorLib.getFacilitatorsByUser(c.authuser.id)
            doF = False
            for f in fList:
               ##log.info('coFacilitateHandler got %s w.id is %s'%(f, w.id))
               if int(f['workshopID']) == int(w.id):
                  doF = f
                  ##log.info('coFacilitateHandler got doF')

            if doF and 'acceptInvite' in request.params:
                  doF['pending'] = '0'
                  eAction = "Accepted"
                  
            if doF and 'declineInvite' in request.params:
                  doF['pending'] = '0'
                  doF['disabled'] = '1'
                  eAction = "Declined"

            if doF:
                  dbhelpersLib.commit(doF)
                  eventLib.Event('CoFacilitator Invitation %s'%eAction, '%s %s an invitation to co facilitate %s'%(c.user['name'], eAction.lower(), w['title']), doF, c.user)
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
    def facilitateResignHandler(self, id1, id2):
        code = id1
        url = id2
        w = workshopLib.getWorkshop(code, utilsLib.urlify(url))
        fList = facilitatorLib.getFacilitatorsByUser(c.authuser.id, 0)
        doF = False
        for f in fList:
           if int(f['workshopID']) == int(w.id) and f['disabled'] != '1':
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
    def facilitatorNotificationHandler(self, id1, id2):
        code = id1
        url = id2
        w = workshopLib.getWorkshop(code, utilsLib.urlify(url))
        facilitator = facilitatorLib.getFacilitatorsByUserAndWorkshop(c.authuser.id, w.id)[0]
        if 'notifications' in request.params:
            notifications = request.params.getall('notifications')
            if 'alerts' in notifications:
                facilitator['alerts'] = '1'
                eAction = 'Turned on alerts'
        else:
            facilitator['alerts'] = '0'
            eAction = 'Turned off alerts'
            
        dbhelpersLib.commit(facilitator)
        eventLib.Event('Facilitator notifications set', eAction, facilitator, c.authuser)
        alert = {'type':'success'}
        alert['title'] = 'Success. ' + eAction
        session['alert'] = alert
        session.save()
            
        return redirect("/workshop/%s/%s/preferences"%(code, url))

