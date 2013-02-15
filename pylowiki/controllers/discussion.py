import logging, pickle

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, redirect
import webhelpers.paginate as paginate
from pylowiki.lib.base import BaseController, render

from pylowiki.lib.db.dbHelpers import commit
import pylowiki.lib.utils as utils
import pylowiki.lib.db.event        as eventLib
import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.discussion   as discussionLib
import pylowiki.lib.db.comment      as commentLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.facilitator  as facilitatorLib
import pylowiki.lib.db.flag         as flagLib
import pylowiki.lib.db.rating       as ratingLib
import pylowiki.lib.db.revision     as revisionLib
import pylowiki.lib.db.geoInfo      as geoInfoLib
import pylowiki.lib.db.demo         as demoLib

from pylowiki.lib.sort import sortBinaryByTopPop, sortContByAvgTop

import pylowiki.lib.helpers as h
import simplejson as json

log = logging.getLogger(__name__)

class DiscussionController(BaseController):

    def __before__(self, action, workshopCode = None):
        publicOrPrivate = ['index', 'topic', 'thread']
        
        if workshopCode is None:
            abort(404)
        c.w = workshopLib.getWorkshopByCode(workshopCode)
        if not c.w:
            abort(404)
        
        # Demo workshop status
        demo = demoLib.getDemo()
        if not demo:
            c.demo = False
        else:
            if demo['workshopCode'] == c.w['urlCode']:
                c.demo = True
            else:
                c.demo = False
        
        workshopLib.setWorkshopPrivs(c.w)
        if c.w['public_private'] == 'public':
            c.scope = geoInfoLib.getPublicScope(c.w)
        if action in publicOrPrivate:
            if c.w['public_private'] != 'public':
                if not c.privs['guest'] and not c.privs['participant'] and not c.privs['facilitator'] and not c.privs['admin']:
                    abort(404)
        if 'user' in session:
            utils.isWatching(c.authuser, c.w)

    def index(self, workshopCode, workshopURL):
        c.title = c.w['title']
        c.discussions = discussionLib.getDiscussionsForWorkshop(workshopCode)
        if not c.discussions:
            c.discussions = []
        else:
            c.discussions = sortBinaryByTopPop(c.discussions)
        disabled = discussionLib.getDiscussionsForWorkshop(workshopCode, disabled = '1')
        if disabled:
            c.discussions = c.discussions + disabled
        c.listingType = 'discussion'
        return render('/derived/6_detailed_listing.bootstrap')

    def topic(self, workshopCode, workshopURL, discussionCode, discussionURL):
        c.thing = c.discussion = discussionLib.getDiscussion(discussionCode)
        if not c.thing:
            c.thing = revisionLib.getRevisionByCode(discussionCode)
            if not c.thing:
                abort(404)
        c.flags = flagLib.getFlags(c.thing)
        c.events = eventLib.getParentEvents(c.thing)
        c.title = c.w['title']
        c.revisions = revisionLib.getRevisionsForThing(c.thing)
        c.listingType = 'discussion'
        
        return render('/derived/6_item_in_listing.bootstrap')

    def thread(self, workshopCode, workshopURL, discussionCode, discussionURL, commentCode):
        c.rootComment = commentLib.getCommentByCode(commentCode)
        c.discussion = discussionLib.getDiscussionByID(c.rootComment['discussion_id'])
        c.title = c.w['title']
        c.content = h.literal(h.reST2HTML(c.discussion['text']))
        c.listingType = 'discussion'
        return render('/derived/6_item_in_listing.bootstrap')

    def addDiscussion(self, workshopCode, workshopURL):
        if c.privs['participant'] or c.privs['admin'] or c.privs['facilitator']:
            c.title = c.w['title']
            c.listingType = 'discussion'
            return render('/derived/6_add_to_listing.bootstrap')
        elif c.privs['guest']:
            c.listingType = 'discussion'
            return render('/derived/6_guest_signup.bootstrap')
        else:
            return redirect('/workshop/%s/%s' % (c.w['urlCode'], c.w['url']))

    @h.login_required
    def addDiscussionHandler(self, workshopCode, workshopURL):
        if not c.privs['participant'] and not c.privs['admin'] and not c.privs['facilitator']:
            return redirect('/workshop/%s/%s' % (c.w['urlCode'], c.w['url']))
       
        if 'title' in request.params:
            title = request.params['title']
        else: 
            title = False
        if 'text' in request.params:
            text = request.params['text']
        else:
            text = ''

        if not title or title=='':
            alert = {'type':'error'}
            alert['title'] = 'Title Field Required'
            alert['content'] = ''
            session['alert'] = alert
            session.save()
            return redirect(session['return_to'])

        else:
            if len(title) > 120:
                title = title[:120]
            d = discussionLib.Discussion(owner = c.authuser, discType = 'general', attachedThing = c.w,\
                title = title, text = text, workshop = c.w, privs = c.privs, role = None)
            r = revisionLib.Revision(c.authuser, d.d)
            commit(c.w)
        
        return redirect('/workshop/%s/%s/discussion/%s/%s' % (workshopCode, workshopURL, d.d['urlCode'], d.d['url']))
