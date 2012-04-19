import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

import pylowiki.lib.helpers as h
from pylowiki.model import get_user_by_email, commit, Event

from pylowiki.lib.base import BaseController, render

log = logging.getLogger(__name__)

class AdminController(BaseController):

    @h.login_required
    def index( self ):
        if int(c.authuser['accessLevel']) < 300:
            return redirect('/')
        return render('/derived/admin.mako')

    @h.login_required
    def addMod(self):
        if int(c.authuser['accessLevel']) < 300:
            return redirect('/')

        email = request.params['email']
        log.info('email = %s' %email)
        u = get_user_by_email(email)
        e = Event('MOD-ify', '%s made mod by %s'%(u.name, c.authuser['name']))
        u.accessLevel = 200
        u.events.append(e)
        commit(e)
        return redirect('/')
