import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylowiki.lib.db.user import isAdmin
import pylowiki.lib.helpers as h

from pylowiki.lib.base import BaseController, render

log = logging.getLogger(__name__)

class SystemadminController(BaseController):

    @h.login_required
    def index(self):
        log.info('%s accessing sysadmin page'%(c.authuser['name']))
        if isAdmin(int(c.authuser.id)):
            log.info('%s rendering sysadmin page'%(c.authuser['name']))
            c.title = 'System Administration'
            return render('/derived/system_admin.html')
        else:
            h.flash("You are not authorized to view that page", "warning")
            return redirect(session['return_to'])
    
    @h.login_required
    def handler(self):
        log.info('%s accessing sysadmin handler page'%(c.authuser['name']))
        if int(c.authuser['accessLevel']) >= 100:
            log.info('%s rendering sysadmin page'%(c.authuser['name']))
            c.title = 'System Administration'
            h.flash("Changes saved.", "success")
            return render('/derived/system_admin.html')
        else:
            h.flash("You are not authorized to view that page", "warning")
            return redirect('/')
    
