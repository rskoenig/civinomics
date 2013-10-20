import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons import config

import pylowiki.lib.helpers as h
from pylowiki.lib.db.user import get_user

from pylowiki.lib.base import BaseController, render

log = logging.getLogger(__name__)

class IndexController(BaseController):

    def index(self):
        if session.get('user'):
            return redirect('/home')
        else:
            c.site_base_url = config['app_conf']['site_base_url']
            c.site_secure_url = config['app_conf']['site_secure_url']
            return redirect('/signup')

