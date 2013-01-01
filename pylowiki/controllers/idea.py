import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

import pylowiki.lib.db.workshop as workshopLib
import pylowiki.lib.db.idea as idea
import pylowiki.lib.db.discussion as discussionLib
from pylowiki.lib.utils import urlify
import pylowiki.lib.helpers as h

from pylowiki.lib.base import BaseController, render

log = logging.getLogger(__name__)

class IdeaController(BaseController):

    def __before__(self, action, workshopCode = None):
        if workshopCode is None:
            abort(404)
        c.w = workshopLib.getWorkshopByCode(workshopCode)
        workshopLib.setWorkshopPrivs(c.w)

    def listing(self, workshopCode, workshopURL):
        c.title = c.w['title']
        ideas = idea.getIdeasInWorkshop(workshopCode)
        if not ideas:
            c.ideas = []
        else:
            c.ideas = ideas
        c.listingType = 'ideas'
        return render('/derived/6_detailed_listing.bootstrap')
    
    @h.login_required
    def addIdea(self, workshopCode, workshopURL):
        c.title = c.w['title']
        if c.privs['participant'] or c.privs['admin'] or c.privs['facilitator']:
            c.listingType = 'idea'
            c.title = c.w['title']
            return render('/derived/6_add_to_listing.bootstrap')
        else:
            c.listingType = 'ideas'
            return render('/derived/6_detailed_listing.bootstrap')

    @h.login_required
    def addIdeaHandler(self, workshopCode, workshopURL):
        if 'submit' not in request.params or 'title' not in request.params:
            return redirect(session['return_to'])
        
        newIdea = idea.Idea(c.authuser, request.params['title'], c.w)
        return redirect(session['return_to'])
    
    def showIdea(self, workshopCode, workshopURL, ideaCode, ideaURL):
        c.idea = idea.getIdea(ideaCode)
        c.discussion = discussionLib.getDiscussionForThing(c.idea)
        c.listingType = 'idea'
        return render('/derived/6_item_in_listing.bootstrap')