import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from pylowiki.lib.db.user import isAdmin
from pylowiki.lib.db.facilitator import isFacilitator
from pylowiki.lib.db.workshop import getWorkshopByCode, isScoped
from pylowiki.lib.utils import urlify
import pylowiki.lib.helpers as h

from pylowiki.lib.base import BaseController, render

log = logging.getLogger(__name__)

class IdeaController(BaseController):

    def listing(self, id1, id2):
        code = id1
        url = id2
        
        c.w = getWorkshopByCode(code)
        c.title = c.w['title']
        
        c.ideas = []
        
        c.listingType = 'ideas'
        if 'user' in session:
            c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
            c.isScoped = isScoped(c.authuser, c.w)
            c.isAdmin = isAdmin(c.authuser.id)
        
        return render('/derived/6_detailed_listing.bootstrap')
    
    @h.login_required
    def addIdea(self, id1, id2):
        code = id1
        url = id2
        
        c.w = getWorkshopByCode(code)
        c.title = c.w['title']
        c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
        c.isScoped = isScoped(c.authuser, c.w)
        c.isAdmin = isAdmin(c.authuser.id)
        if c.isScoped or c.isAdmin or c.isFacilitator:
            c.listingType = 'idea'
            c.title = c.w['title']
            return render('/derived/6_add_to_listing.bootstrap')
        else:
            c.listingType = 'ideas'
            return render('/derived/6_detailed_listing.bootstrap')