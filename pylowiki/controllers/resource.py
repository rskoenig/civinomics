import logging

from pylons import config, request, response, session, tmpl_context as c
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
import pylowiki.lib.db.geoInfo          as  geoInfoLib
import pylowiki.lib.alerts              as  alertsLib
import pylowiki.lib.utils               as  utils
import pylowiki.lib.sort                as  sort
import pylowiki.lib.db.mainImage        as mainImageLib

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
            
        c.mainImage = mainImageLib.getMainImage(c.w)
        
        # Demo workshop status
        c.demo = workshopLib.isDemo(c.w)

        
        c.title = c.w['title']
        workshopLib.setWorkshopPrivs(c.w)
        if c.w['public_private'] == 'public':
            c.scope = geoInfoLib.getPublicScope(c.w)
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
        disabled = resourceLib.getResourcesByWorkshopCode(workshopCode, disabled = '1')
        if disabled:
            c.resources = c.resources + disabled
        c.listingType = 'resources'
        return render('/derived/6_detailed_listing.bootstrap')

    def showResource(self, workshopCode, workshopURL, resourceCode, resourceURL):
        # these values are needed for facebook sharing
        c.facebookAppId = config['facebook.appid']
        c.channelUrl = config['facebook.channelUrl']
        c.requestUrl = request.url

        c.thing = resourceLib.getResourceByCode(resourceCode)
        if not c.thing:
            c.thing = resourceLib.getResourceByCode(resourceCode, disabled = '1')
            if not c.thing:
                c.thing = revisionLib.getRevisionByCode(resourceCode)
                if not c.thing:
                    abort(404)
        c.discussion = discussionLib.getDiscussionForThing(c.thing)
        c.listingType = 'resource'
        c.revisions = revisionLib.getRevisionsForThing(c.thing)
        
        if 'comment' in request.params:
            c.rootComment = commentLib.getCommentByCode(request.params['comment'])
            if not c.rootComment:
                abort(404)
                
        return render('/derived/6_item_in_listing.bootstrap')

    def thread(self, workshopCode, workshopURL, resourceCode, resourceURL, commentCode = ''):
        c.resource = resourceLib.getResourceByCode(resourceCode)
        c.discussion = discussionLib.getDiscussionForThing(c.resource)
        c.rootComment = commentLib.getCommentByCode(commentCode)
        c.listingType = 'resource'
        return render('/derived/6_item_in_listing.bootstrap')

    def addResource(self, workshopCode, workshopURL):
        if (c.privs['participant'] and c.w['allowResources'] == '1') or c.privs['facilitator'] or c.privs['admin']:
            c.listingType = 'resource'
            return render('/derived/6_add_to_listing.bootstrap')
        elif c.privs['guest']:
            c.listingType = 'resource'
            return render('/derived/6_guest_signup.bootstrap')
        else:
            c.listingType = 'resources'
            return render('/derived/6_detailed_listing.bootstrap')

    @h.login_required
    def addResourceHandler(self, workshopCode, workshopURL):
        resourceType = ''
        resourceInfo = ''
        if 'title' not in request.params or 'resourceType' not in request.params:
            return redirect(session['return_to'])
        title = request.params['title'].strip()
        if title == '':
            return redirect(session['return_to'])
        resourceType = request.params['resourceType']
        if resourceType == 'url':
            if resourceLib.getResourceByLink(request.params['link'], c.w):
                return redirect(session['return_to']) # Link already submitted
            resourceInfo = request.params['link']
        elif resourceType == 'embed':
            resourceInfo = request.params['embed']
            if not resourceInfo.startswith("<iframe") or not resourceInfo.endswith("</iframe>"):
                return redirect(session['return_to'])
        else:
            return redirect(session['return_to'])
        text = ''
        if 'text' in request.params:
            text = request.params['text'] # Optional
        if len(title) > 120:
            title = title[:120]
        newResource = resourceLib.Resource(resourceInfo, resourceType, title, c.authuser, c.w, c.privs, text = text)
        alertsLib.emailAlerts(newResource)
        return redirect(utils.thingURL(c.w, newResource))
