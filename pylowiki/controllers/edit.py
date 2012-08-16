# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

#Fox imported these modules
from pylowiki.model import commit_edit, get_page
import pylowiki.lib.helpers as h

log = logging.getLogger(__name__)

class EditController(BaseController):

    @h.login_required
    def edit( self, id ):
        """ Display page editor for ID/URL """

        p = get_page( id )
        if p == False: # Error page not found
            abort(404, h.literal("This page does not exist yet ... Would you like to <a href='/create/assist/" + id + "'> Create it?</a>") )
    
        c.title = c.heading = "Currently editing " + p.url
        c.url = p.url

        r = p.revisions[0]

        c.rST = r.data
        c.controller = "edit"

        return render( "/derived/CreateOrEdit.mako" )

    @h.login_required   
    def handler(self, id):
        """ Handle page edit submission """
        try:
            request.params['submit']        
            if commit_edit( id, session['user'], request.params['textarea'], "edit", request.params.get('remark') ):
                h.flash( "The page was saved!", "success" )
            else:
                h.flash( "The page was NOT saved!", "warning" )
        except KeyError: 
            h.flash( "Do not access a handler directly", "error" )
        p = get_page(id)
        type = p.type
        return redirect( "/%s/%s" %(type, str(id)) )
