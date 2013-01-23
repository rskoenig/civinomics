import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

import pylowiki.lib.db.user             as  userLib
import pylowiki.lib.db.facilitator      as  facilitatorLib
import pylowiki.lib.db.dbHelpers        as  dbHelpers
import pylowiki.lib.db.workshop         as  workshopLib
import pylowiki.lib.db.event            as  eventLib
import pylowiki.lib.db.resource         as  resourceLib
import pylowiki.lib.db.discussion       as  discussionLib
import pylowiki.lib.db.comment          as  commentLib
import pylowiki.lib.db.revision         as  revisionLib
import pylowiki.lib.utils               as  utils
import pylowiki.lib.sort                as  sort

from tldextract import extract
from pylowiki.lib.base import BaseController, render
import pylowiki.lib.helpers as h

log = logging.getLogger(__name__)

class ResourceController(BaseController):
    
    def __before__(self, action, workshopCode = None, workshopURL = None):
        if workshopCode is None:
            abort(404)
        c.w = workshopLib.getWorkshopByCode(workshopCode)
        if not c.w:
            abort(404)
        c.title = c.w['title']
        workshopLib.setWorkshopPrivs(c.w)
        
        if c.w['public_private'] != 'public':
            if not c.privs['guest'] and not c.privs['participant'] and not c.privs['facilitator'] and not c.privs['admin']:
                abort(404)
        
        if 'user' in session:
            utils.isWatching(c.authuser, c.w)

    def listing(self, workshopCode, workshopURL):
        resources = resourceLib.getResourcesByWorkshopCode(workshopCode)
        if not resources:
            c.resources = []
        else:
            c.resources = sort.sortBinaryByTopPop(resources)
        c.listingType = 'resources'
        return render('/derived/6_detailed_listing.bootstrap')

    def showResource(self, workshopCode, workshopURL, resourceCode, resourceURL):
        c.resource = resourceLib.getResourceByCode(resourceCode)
        if not c.resource:
            abort(404)
        c.discussion = discussionLib.getDiscussionForThing(c.resource)
        c.listingType = 'resource'
        return render('/derived/6_item_in_listing.bootstrap')

    def thread(self, workshopCode, workshopURL, resourceCode, resourceURL, commentCode = ''):
        c.resource = resourceLib.getResourceByCode(resourceCode)
        c.discussion = discussionLib.getDiscussionForThing(c.resource)
        c.rootComment = commentLib.getCommentByCode(commentCode)
        c.listingType = 'resource'
        return render('/derived/6_item_in_listing.bootstrap')

    @h.login_required
    def addResource(self, workshopCode, workshopURL):
        if (c.privs['participant'] or c.privs['facilitator'] or c.privs['admin']) and c.w['allowResources'] == '1':
            c.listingType = 'resource'
            return render('/derived/6_add_to_listing.bootstrap')
        else:
            c.listingType = 'resources'
            return render('/derived/6_detailed_listing.bootstrap')

    @h.login_required
    def addResourceHandler(self, workshopCode, workshopURL):
        if 'submit' not in request.params or 'title' not in request.params or 'link' not in request.params:
            return redirect(session['return_to'])
        if request.params['title'].strip() == '':
            return redirect(session['return_to'])
        if resourceLib.getResourceByLink(request.params['link'], c.w):
            return redirect(session['return_to']) # Link already submitted
        text = ''
        if 'text' in request.params:
            text = request.params['text'] # Optional
        
        newResource = resourceLib.Resource(request.params['link'], request.params['title'], c.authuser, c.w, text = text)
        return redirect(session['return_to'])
