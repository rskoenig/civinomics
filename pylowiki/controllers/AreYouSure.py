# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

# fox added the following imports
from pylowiki.model import commit_trash, get_page, get_revision, commit_edit
import pylowiki.lib.helpers as h

log = logging.getLogger(__name__)

class AreyousureController(BaseController):

    @h.login_required
    def delete( self, id ):
        """Delete a page"""
        c.action = "delete"
        c.url = id
        c.title = c.heading = "Are you sure you want to delete " + id + "?"
        return render( "/derived/AreYouSure.mako")
        
    @h.login_required
    def restore( self, id ):
        """Restore a page"""
        c.action = "restore"
        c.url = id
        c.title = c.heading = "Are you sure you want to restore " + id + "?"
        return render( "/derived/AreYouSure.mako")
        
    @h.login_required
    def revert( self, id ): # id = rev id
        """Revert a page"""    
        c.action = "revert"
        c.revid = id
        c.title = c.heading = "Are you sure you want to revert to revision " + id + "?"
        return render( "/derived/AreYouSure.mako")
        
    @h.login_required
    def handler( self, id ):
              
        try:

            request.params['submit']
            action = request.params['action']
            comment = ""           

            if request.params.get('remark') is None:
                pass # Do nothing
            else:
                remark = request.params.get('remark')
           
            if action == "delete" or action == "restore":
                """Logic for delete and restore"""
                if commit_trash( id, session['user'], action, remark ):
                    h.flash( "The page '" + id + "' was " + action + "d.", "success" )
                else:
                    h.flash( "The page '" + id + "' was NOT " + action + "d.", "error" )
                return redirect( "/" + action )
            
            if action == "revert":
                """Logic for revert"""
                
                r = get_revision( id )
                pageurl = r.event.page.url
   
                if commit_edit( pageurl, session['user'], r.data, action, remark  ):
                    h.flash( pageurl + " was reverted to revision " + id, "success" )
                else:
                    h.flash( pageurl + " was NOT reverted ...", "error" )
                    
                redirect( "/" + pageurl)

        except KeyError: 
            h.flash( "Do not access a handler directly", "error" )
      
