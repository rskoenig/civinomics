# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

#Fox imported these modules
from pylowiki.model import Revision, Page, Event, commit, get_user
import pylowiki.lib.helpers as h

log = logging.getLogger(__name__)

class CreateController(BaseController):
    
    def __before__(self):
        c.rST = "" # because create shares a mako template with edit, we need to set this varible
        c.controller = "create" # think of a better way to do this...  base.mako has logic for parcing the url in pylons object
        c.title = c.heading = c.controller + " a page"

    @h.login_required
    def index( self ):
        """ Display create page form """
        return render( "/derived/CreateOrEdit.mako" ) 

    @h.login_required
    def assist( self, id ):
        """ Display assisted create page form """
        c.url = id
        return render( "/derived/CreateOrEdit.mako" ) 

    @h.login_required
    def handler(self):
        """ Handles page creation """
        try:            

            request.params['submit']
            p = Page( request.params['page_url'].lower().replace (" ", "-"), 'issue' )
            u = get_user( session["user"] )
            r = Revision( request.params["textarea"] )

            e = Event( "create", request.params.get('remark', None) )
            p.events.append( e )
            u.events.append( e )
            r.event = e
            p.revisions.append( r )

            if p.url == "" or r.data == "":
                h.flash( "Page was not created. Please fill all fields.", "warning" )
            elif commit( e ):
                h.flash( "The page was created!", "success" )
                return redirect( "/" + str(p.url) )
            else:
                h.flash( "Page was not created.  URL or title might be in use. Press back", "warning" )
        except KeyError: 
            h.flash( "Do not access a handler directly", "error" )
	return redirect( "/" )

