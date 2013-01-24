# -*- coding: utf-8 -*-
"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render

from pylons import tmpl_context as c

from pylons import config, session, request
from pylons.controllers.util import abort, redirect

#from pylowiki.model import meta, get_user, getPoints
from pylowiki.model import meta
from pylowiki.lib.db.user import get_user
from pylowiki.lib.db.geoInfo import getGeoInfo

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']

        # Allow the templates to see the config dictionary
        c.conf = config['app_conf']
        c.url = ""
        c.action = ""

        if "user" in session:
            c.authuser = get_user( session['userCode'], session['userURL'] )
            if not c.authuser:
               session.delete()
            else:
               c.authuser_geo = getGeoInfo(c.authuser.id)[0]
            
        try:
            spamremark = request.params['sremark']
        except KeyError:
            spamremark = ''

        try:
            
            if spamremark != '': # spamremark must be empty
                abort( 403, comment="Sorry, you appear to be a spam bot" )
            else:
                return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()

