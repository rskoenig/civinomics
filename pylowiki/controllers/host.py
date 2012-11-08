import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import redirect
from pylowiki.lib.base import BaseController, render
from pylowiki.lib.db.account import getAccountByName, isAccountAdmin
from pylowiki.lib.db.workshop import getWorkshopsByAccount
from pylowiki.lib.utils import urlify

log = logging.getLogger(__name__)

class HostController(BaseController):

    def showHost(self, id1):
        accountName = id1
        account = getAccountByName(urlify(accountName))
        if account and account['type'] != 'trial':
            c.account = account
            if 'user' in session and isAccountAdmin(c.authuser, c.account):
                publicPrivate = 'all'
            else:
                publicPrivate = 'public'
            c.workshops = getWorkshopsByAccount(c.account.id, publicPrivate)
            return render("/derived/host.bootstrap")
        else:
            return render('/derived/404.bootstrap')