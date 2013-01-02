# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

import webhelpers.paginate as paginate
import pylowiki.lib.helpers as h
from pylons import config

from pylowiki.lib.db.facilitator import Facilitator, getFacilitatorsByUser, getFacilitatorsByUserAndWorkshop
from pylowiki.lib.db.event import Event
from pylowiki.lib.db.user import get_user, getUserByID, isAdmin
from pylowiki.lib.db.workshop import getWorkshop, getWorkshopByID, getWorkshopsByOwner
from pylowiki.lib.db.account import Account, getUserAccount
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.utils import urlify

from hashlib import md5

log = logging.getLogger(__name__)

class FacilitatorController(BaseController):

    @h.login_required
    def coFacilitateInvite(self, id1, id2):
        code = id1
        url = id2
        c.user = get_user(code, url)
        if c.user and 'inviteToFacilitate' in request.params:
           invite = request.params['inviteToFacilitate']
           iList = invite.split("/")
           wCode = iList[0]
           wURL = iList[1]
           w = getWorkshop(wCode, urlify(wURL))
           Facilitator(c.user, w, 1)
           # Becasue the __init__ function doesn't return the object... sigh
           fList = getFacilitatorsByUserAndWorkshop(c.user.id, w.id)
           Event('CoFacilitator Invitation Issued', '%s issued an invitation to co facilitate %s'%(c.authuser['name'], w['title']), fList[0], c.authuser)
           h.flash('CoFacilitation Invitation Issued', 'success')
           return redirect("/profile/%s/%s"%(code, url))
        else:
           h.flash('Error: You are not authorized', 'error')
           return redirect("/" )

    @h.login_required
    def coFacilitateHandler(self, id1, id2):
        code = id1
        url = id2
        c.user = get_user(code, urlify(url))
        if 'workshopCode' in request.params and 'workshopURL' in request.params:
            wCode = request.params['workshopCode']
            wURL = request.params['workshopURL']
            ##log.info('coFacilitateHandler %s %s' % (wCode, wURL))
            w = getWorkshop(wCode, urlify(wURL))
            fList = getFacilitatorsByUser(c.authuser.id)
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
                  commit(doF)
                  Event('CoFacilitator Invitation %s'%eAction, '%s %s an invitation to co facilitate %s'%(c.user['name'], eAction.lower(), w['title']), doF, c.user)
                  h.flash('CoFacilitation Invitation %s'%eAction, 'success')
                  return redirect("/profile/%s/%s"%(code, url))

        h.flash('Error: You are not authorized', 'error')
        return redirect("/" )

    @h.login_required
    def resignFacilitatorHandler(self, id1, id2):
        code = id1
        url = id2
        log.info('in resignFacilitatorHandler')
        w = getWorkshop(code, urlify(url))
        fList = getFacilitatorsByUser(c.authuser.id, 0)
        doF = False
        for f in fList:
           if int(f['workshopID']) == int(w.id) and f['disabled'] != '1':
              doF = f

        if 'resignReason' in request.params:
           resignReason = request.params['resignReason']
           resignReason = resignReason.lstrip()
           resignReason = resignReason.rstrip()
           if resignReason == '':
              h.flash('Error: include note', 'error')
              return redirect("/workshop/%s/%s"%(code, url))

           log.info('resignReason is %s'%resignReason)
        else:
           h.flash('Error: include note', 'error')
           return redirect("/workshop/%s/%s"%(code, url))


        if doF and c.authuser.id == doF.owner:
           doF['disabled'] = '1'
           commit(doF)
           Event('CoFacilitator Resigned', '%s resigned as cofacilitator of %s: %s'%(c.authuser['name'], w['title'], resignReason), doF, c.authuser)
           h.flash('CoFacilitation Resignation Accepted', 'success')
           return redirect("/workshop/%s/%s"%(code, url))

        h.flash('Error: You are not authorized', 'error')
        return redirect("/workshop/%s/%s"%(code, url))
