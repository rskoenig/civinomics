# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

#from pylowiki.model import get_all_pages, getIssues, getSolutions, getParticipantsByID
from pylowiki.lib.db.page import get_all_pages
from pylowiki.lib.db.workshop import getActiveWorkshops
import webhelpers.paginate as paginate
import pylowiki.lib.helpers as h
from pylons import config

log = logging.getLogger(__name__)

class ActionlistController(BaseController):

    def __before__(self):
        if c.conf['public.sitemap'] != "true": 
            h.check_if_login_required()

    
    def index( self, id ): # id is the action
        """Create a list of pages with the given action/option """
        """Valid actions: edit, revision, delete, restore, sitemap """
        c.action = id
        
        if c.action == "sitemap":
            c.title = c.heading = c.action
            c.action = ""
            c.list = get_all_pages()
        elif c.action == 'sitemapIssues':
            c.title = c.heading = 'Workshops'
            c.list = getActiveWorkshops()
        elif c.action == 'sitemapIssuesByTag':
            c.title = c.heading = 'Workshops'
            c.list = getWorkshops()
            """
        elif c.action == 'sitemapSolutions':
            c.title = c.heading = 'Solutions'
            c.list = getSolutions()
            """
        else:
            c.title = c.heading = "Which " + c.action + "?"

        if c.action == "restore":
            c.list = get_all_pages(1)

        """
        if c.action == "issues":
            c.title = c.heading = c.action
            c.action = ""
        else:
            c.list = get_all_pages()
        """
        c.count = len( c.list )
        c.paginator = paginate.Page(
            c.list, page=int(request.params.get('page', 1)),
            items_per_page = 10, item_count = c.count
        )

        return render('/derived/top_issues.html')
        return render( "/derived/ActionList.mako" )
