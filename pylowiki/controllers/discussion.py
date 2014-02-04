import logging, pickle

from pylons import config, request, response, session, tmpl_context as c
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
import pylowiki.lib.db.mainImage    as mainImageLib
import pylowiki.lib.db.dbHelpers    as dbHelpers
import pylowiki.lib.alerts          as  alertsLib

from pylowiki.lib.facebook import FacebookShareObject
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
            
        c.mainImage = mainImageLib.getMainImage(c.w)
        
        #################################################
        # these values are needed for facebook sharing
        c.backgroundImage = utils.workshopImageURL(c.w, c.mainImage)
        shareOk = workshopLib.isPublic(c.w)
        c.facebookShare = FacebookShareObject(
            itemType='workshop',
            url=utils.workshopURL(c.w) + '/discussion',
            thingCode=workshopCode, 
            image=c.backgroundImage,
            title=c.w['title'],
            description=c.w['description'].replace("'", "\\'"),
            shareOk = shareOk
        )
        # add this line to tabs in the workshop in order to link to them on a share:
        # c.facebookShare.url = c.facebookShare.url + '/activity'
        #################################################

        # Demo workshop status
        c.demo = workshopLib.isDemo(c.w)
        
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
        #get the scope to display jurisidction flag
        if c.w['public_private'] == 'public':
            c.scope = workshopLib.getPublicScope(c.w)
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
        #get the scope to display jurisidction flag
        if c.w['public_private'] == 'public':
            c.scope = workshopLib.getPublicScope(c.w)
        
        # sharing - extra details
        c.thingCode = discussionCode        
        c.thing = c.discussion = discussionLib.getDiscussion(discussionCode)
        if not c.thing:
            c.thing = revisionLib.getRevisionByCode(discussionCode)
            if not c.thing:
                abort(404)
        
        ################## FB SHARE ###############################
        c.facebookShare.title = c.thing['title']
        # update url for this item
        newUrl = utils.workshopURL(c.w) + utils.thingURL(c.w, c.thing)
        c.facebookShare.updateUrl(newUrl)
        # set description to be that of the topic's description
        c.facebookShare.description = utils.getTextFromMisaka(c.thing['text'])
        #################################################

        if 'views' not in c.thing:
            c.thing['views'] = u'0'
            
        views = int(c.thing['views']) + 1
        c.thing['views'] = str(views)
        dbHelpers.commit(c.thing)

        c.flags = flagLib.getFlags(c.thing)
        c.events = eventLib.getParentEvents(c.thing)
        c.title = c.w['title']
        c.revisions = revisionLib.getRevisionsForThing(c.thing)
        c.listingType = 'discussion'
        
        if 'comment' in request.params:
            c.rootComment = commentLib.getCommentByCode(request.params['comment'])
            if not c.rootComment:
                abort(404)
        return render('/derived/6_item_in_listing.bootstrap')

    def thread(self, workshopCode, workshopURL, discussionCode, discussionURL, commentCode):
        # note: how to structure a url in order to link to this thread for facebook sharing?
        c.rootComment = commentLib.getCommentByCode(commentCode)
        c.discussion = discussionLib.getDiscussionByID(c.rootComment['discussion_id'])
        c.title = c.w['title']
        c.content = h.literal(h.reST2HTML(c.discussion['text']))
        c.listingType = 'discussion'
        return render('/derived/6_item_in_listing.bootstrap')

    def addDiscussion(self, workshopCode, workshopURL):
        if c.privs['participant'] or c.privs['admin'] or c.privs['facilitator']:
            c.title = c.w['title']
            #get the scope to display jurisidction flag
            if c.w['public_private'] == 'public':
                c.scope = workshopLib.getPublicScope(c.w)
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
            alertsLib.emailAlerts(d.d)
            commit(c.w)
        
        return redirect(utils.thingURL(c.w, d.d))
