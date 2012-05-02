# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

#Fox imported these modules
from pylowiki.model import get_page, commit_edit, get_revision, get_prev_revision
import pylowiki.lib.helpers as h
import webhelpers.paginate as paginate

import difflib

log = logging.getLogger(__name__)

class RevisionController(BaseController):

    @h.login_required
    def revisions( self, id ): # id = url
        """ Display all of the page's revisions """
        p = get_page( id )
        c.url = p.url

        c.count = len(p.events)
        c.paginator = paginate.Page(
            p.events, page=int(request.params.get('page', 1)),
            items_per_page = 20, item_count = c.count
        )

        c.title = c.heading = p.url + " revisions / events"
        return render("/derived/revisions.mako")
    
    @h.login_required
    def number(self, id ): # id = rev id
        """ Display revision number rendered in HTML """

        c.r = get_revision( id ) # get revision object by id
        c.r2 = get_prev_revision( c.r.id, c.r.page_id ) # previous revision object

        if c.r2 == False:
            c.r2 = c.r # if c.r2 has no results set it to c.r
       
        d = difflib.HtmlDiff()
        c.diff = h.literal(d.make_table( c.r2.data.splitlines(), c.r.data.splitlines(), fromdesc="Revision " + str(c.r2.id), todesc="Revision " + str(c.r.id), context=True, numlines=1 ))

        c.content = h.literal( h.reST2HTML( c.r.data ) )
        c.title = "Currently viewing revision " + str( c.r.id )
        return render("/derived/ViewRevision.mako")

    @h.login_required
    def handler( self, id ): # id = rev id
        """ Revert to given revision """
        try:
            r = get_revision( id )
            url = r.events[0].page.url

            request.params['submit']        
            if commit_edit( url, session['user'], r.data, "Revert", "Reverted to Revision " + str(id) + ". " + request.params.get('comment') ):
                h.flash( "Successfully Reverted Page!", "success" )
            else:
                h.flash( "The page was NOT reverted! ", "warning" )
        except KeyError: 
            h.flash( "Do not access a handler directly", "error" )
            return redirect( "/" )
        return redirect( "/" + str(url) ) 
