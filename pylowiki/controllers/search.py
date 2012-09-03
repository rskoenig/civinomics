# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import config

from pylowiki.lib.base import BaseController, render

#fox added the following imports
from pylowiki.model import get_search_results, get_page
import webhelpers.paginate as paginate
import pylowiki.lib.helpers as h

log = logging.getLogger(__name__)

class SearchController(BaseController):

    def __before__(self):
        c.title = c.heading = "Search"
        if c.conf['public.search'] != "true": # set in enviroment config
            h.check_if_login_required()
    
    def index(self):
        return render( "/derived/search.mako" )
    
    def handler(self):
        try:
            request.params['submit']

            result = get_search_results( request.params.get('needle') )

            if result[0] == 0: # check if result is false
                c.content = result[1]
                return render( "/derived/body.mako" )
				
            c.list = []
            for r in result[1]:
                c.list.append( get_page( r[1] ) )

            c.count = len( c.list )
            if c.count == 1:
                return redirect( "/" + c.list[0].url )

            c.paginator = paginate.Page(
                c.list, page=int(request.params.get('page', 1)),
                items_per_page = 20, item_count = c.count
            )
   
            return render( "/derived/ActionList.mako" )

        except KeyError:
            h.flash( "Do not access a handler directly", "error" )
            redirect( "/search" )
