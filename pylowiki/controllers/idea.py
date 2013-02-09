import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.idea         as ideaLib
import pylowiki.lib.db.discussion   as discussionLib
import pylowiki.lib.db.geoInfo      as geoInfoLib
import pylowiki.lib.utils           as utils
import pylowiki.lib.sort            as sortLib
import pylowiki.lib.helpers as h

from pylowiki.lib.base import BaseController, render

log = logging.getLogger(__name__)

class IdeaController(BaseController):

    def __before__(self, action, workshopCode = None):
        if workshopCode is None:
            abort(404)
        c.w = workshopLib.getWorkshopByCode(workshopCode)
        if not c.w:
            abort(404)
        workshopLib.setWorkshopPrivs(c.w)
        if c.w['public_private'] == 'public':
            c.scope = geoInfoLib.getPublicScope(c.w)
        if 'user' in session:
            utils.isWatching(c.authuser, c.w)

    def listing(self, workshopCode, workshopURL):
        c.title = c.w['title']
        ideas = ideaLib.getIdeasInWorkshop(workshopCode)
        if not ideas:
            c.ideas = []
        else:
            c.ideas = sortLib.sortBinaryByTopPop(ideas)
        disabled = ideaLib.getIdeasInWorkshop(workshopCode, disabled = '1')
        if disabled:
            c.ideas = c.ideas + disabled
        c.listingType = 'ideas'
        return render('/derived/6_detailed_listing.bootstrap')

    def addIdea(self, workshopCode, workshopURL):
        c.title = c.w['title']
        if c.privs['participant'] or c.privs['admin'] or c.privs['facilitator']:
            c.listingType = 'idea'
            c.title = c.w['title']
            return render('/derived/6_add_to_listing.bootstrap')
        elif c.privs['guest']:
            c.listingType = 'idea'
            return render('/derived/6_guest_signup.bootstrap')           
        else:
            c.listingType = 'ideas'
            return render('/derived/6_detailed_listing.bootstrap')

    @h.login_required
    def addIdeaHandler(self, workshopCode, workshopURL):
        if 'submit' not in request.params or 'title' not in request.params:
            return redirect(session['return_to'])
        title = request.params['title'].strip()
        if title == '':
            return redirect(session['return_to'])
        if len(title) > 120:
            title = title[:120]
        newIdea = ideaLib.Idea(c.authuser, title, c.w, c.privs)
        return redirect(session['return_to'])
    
    def showIdea(self, workshopCode, workshopURL, ideaCode, ideaURL):
        c.thing = ideaLib.getIdea(ideaCode)
        if not c.thing:
            c.thing = ideaLib.getIdea(ideaCode, disabled = '1')
            if not c.thing:
                abort(404)
        c.discussion = discussionLib.getDiscussionForThing(c.thing)
        c.listingType = 'idea'
        return render('/derived/6_item_in_listing.bootstrap')