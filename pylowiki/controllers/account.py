# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

import webhelpers.paginate as paginate
import pylowiki.lib.helpers as h
from pylons import config

from pylowiki.lib.db.user import get_user, getUserByID, isAdmin
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.workshop import getWorkshopByID, getWorkshopsByOwner
from pylowiki.lib.db.account import Account, getUserAccount


from hashlib import md5

log = logging.getLogger(__name__)

class AccountController(BaseController):

    @h.login_required
    def accountAdminHandler(self, id1, id2):
        code = id1
        url = id2
        if not isAdmin(c.authuser.id):
           h.flash('Error: You are not authorized', 'error')
           return redirect("/" )

        c.user = get_user(code, url)
        c.account = getUserAccount(c.user.id)
        if not c.account and 'numHost' in request.params:
           log.info('accountAdminHandler %s %s' % (code, url))
           numHost = request.params['numHost']
           numParticipants = '10'
           monthlyRate = '0'
           a = Account(c.user, numHost, numParticipants, monthlyRate, 'trial')
           h.flash('Account Admin Created', 'success')
        elif c.account and 'numHost' in request.params:
           numHost = request.params['numHost']
           if c.account['numHost'] != numHost:
              c.account['numHost'] = numHost
              w = getWorkshopsByOwner(c.user.id)
              numWorkshops = len(w)
              numRemaining = int(numHost) - numWorkshops
              c.account['numRemaining'] = numRemaining
              commit(c.account)
              h.flash('Account hosting upgraded to %s'%numHost, 'success')
        else:
              h.flash('No change to account', 'success')

        return redirect("/profile/" + code + "/" + url + "/admin" )

