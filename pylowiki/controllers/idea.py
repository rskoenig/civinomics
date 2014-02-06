import logging

from pylons import config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.idea         as ideaLib
import pylowiki.lib.db.discussion   as discussionLib
import pylowiki.lib.db.geoInfo      as geoInfoLib
import pylowiki.lib.utils           as utils
import pylowiki.lib.sort            as sortLib
import pylowiki.lib.db.revision     as revisionLib
import pylowiki.lib.db.mainImage    as mainImageLib
import pylowiki.lib.alerts          as alertsLib
import pylowiki.lib.db.comment      as commentLib
import pylowiki.lib.db.dbHelpers    as dbHelpers
import pylowiki.lib.db.rating       as ratingLib
import pylowiki.lib.helpers as h

import simplejson as json
import misaka as m

from pylowiki.lib.facebook          import FacebookShareObject
from pylowiki.lib.base              import BaseController, render

log = logging.getLogger(__name__)

class IdeaController(BaseController):

    def __before__(self, action, workshopCode = None):
        if workshopCode is None:
            abort(404)
        c.w = workshopLib.getWorkshopByCode(workshopCode)
        if not c.w:
            abort(404)
            
        c.mainImage = mainImageLib.getMainImage(c.w)
        
        # Demo workshop status
        c.demo = workshopLib.isDemo(c.w)
        
        workshopLib.setWorkshopPrivs(c.w)
        if c.w['public_private'] != 'public':
            if not c.privs['guest'] and not c.privs['participant'] and not c.privs['facilitator'] and not c.privs['admin']:
                abort(404)
        if c.w['public_private'] == 'public':
            c.scope = geoInfoLib.getPublicScope(c.w)
        if 'user' in session:
            utils.isWatching(c.authuser, c.w)

        ################## FB SHARE ###############################
        # these values are needed for facebook sharing of a workshop
        # - details for sharing a specific idea are modified in the view idea function
        c.backgroundImage = utils.workshopImageURL(c.w, c.mainImage)
        shareOk = workshopLib.isPublic(c.w)
        c.facebookShare = FacebookShareObject(
            itemType='workshop',
            url=utils.workshopURL(c.w),
            parentCode=workshopCode, 
            image=c.backgroundImage,
            title=c.w['title'],
            description=c.w['description'].replace("'", "\\'"),
            shareOk = shareOk
        )
        # add this line to tabs in the workshop in order to link to them on a share:
        # c.facebookShare.url = c.facebookShare.url + '/activity'
        #################################################

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
        if c.w['public_private'] == 'public':
            c.scope = workshopLib.getPublicScope(c.w)
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
        # check to see if this is a request from the iphone app
        iPhoneApp = utils.iPhoneRequestTest(request)

        if 'submit' not in request.params or 'title' not in request.params:
            log.info("submit or title not in req params")
            return redirect(session['return_to'])
        title = request.params['title'].strip()
        text = request.params['text']
        if title == '':
            log.info("title is blank")
            return redirect(session['return_to'])
        if len(title) > 120:
            title = title[:120]
        newIdea = ideaLib.Idea(c.authuser, title, text, c.w, c.privs)
        log.info("made new idea")
        alertsLib.emailAlerts(newIdea)
        if iPhoneApp:
            log.info("in iphone app")
            entry = {}
            entry['workshopCode'] = newIdea['workshopCode']
            entry['workshop_url'] = newIdea['workshop_url']
            entry['thingCode'] = newIdea['urlCode']
            entry['url'] = newIdea['url']
            result = []
            result.append(entry)
            statusCode = 0
            response.headers['Content-type'] = 'application/json'
            #log.info("results workshop: %s"%json.dumps({'statusCode':statusCode, 'result':result}))
            return json.dumps({'statusCode':statusCode, 'result':result})
        else:
            return redirect(utils.thingURL(c.w, newIdea))
    
    def showIdea(self, workshopCode, workshopURL, ideaCode, ideaURL):
        # check to see if this is a request from the iphone app
        iPhoneApp = utils.iPhoneRequestTest(request)
        
        c.thingCode = ideaCode
        
        c.thing = ideaLib.getIdea(ideaCode)
        if not c.thing:
            c.thing = revisionLib.getRevisionByCode(ideaCode)
            if not c.thing:
                abort(404)
        
        ################## FB SHARE ###############################
        c.facebookShare.title = c.thing['title']
        c.facebookShare.thingCode = c.thingCode
        # update url for this item
        c.facebookShare.updateUrl(utils.thingURL(c.w, c.thing))
        # set description to be that of the topic's description
        c.facebookShare.description = utils.getTextFromMisaka(c.thing['text'])
        #################################################

        if 'views' not in c.thing:
            c.thing['views'] = u'0'
        
        views = int(c.thing['views']) + 1
        c.thing['views'] = str(views)
        dbHelpers.commit(c.thing)

        if not iPhoneApp:
            c.discussion = discussionLib.getDiscussionForThing(c.thing)
        
        c.listingType = 'idea'
        
        if not iPhoneApp:
            c.revisions = revisionLib.getRevisionsForThing(c.thing)
        
        if not iPhoneApp:
            if 'comment' in request.params:
                c.rootComment = commentLib.getCommentByCode(request.params['comment'])
                if not c.rootComment:
                    abort(404)

        if iPhoneApp:
            log.info("iphone idea")
            entry = {}
            # if this person has voted on the idea, we need to pack their vote data in
            if 'user' in session:
                log.info("iphone idea: user in session")
                rated = ratingLib.getRatingForThing(c.authuser, c.thing)
                if rated:
                    if rated['amount'] == '1':
                        entry['rated'] = "1"
                    elif rated['amount'] == '-1':
                        entry['rated'] = "-1"
                    elif rated['amount'] == '0' :
                        entry['rated'] = "0"
                    else:
                        entry['rated'] = "0"
                else:
                    entry['rated'] = "0"
            #    utils.isWatching(c.authuser, c.w)
            #if c.authuser:
                #
            # rated = ratingLib.getRatingForThing(c.authuser, thing) 
            
            entry['thingCode'] = c.thingCode
            entry['backgroundImage'] = c.backgroundImage
            #entry['title'] = c.thing['title']
            #entry['text'] = c.thing['text']
            ideaTextHtml = m.html(c.thing['text'], render_flags=m.HTML_SKIP_HTML)
            entry['ideaText'] = ideaTextHtml
            entry['thing'] = dict(c.thing)
            entry['discussion'] = dict(c.discussion)
            #entry['revisions'] = c.revisions
            entry['rootComment'] = c.rootComment
            result = []
            result.append(entry)
            statusCode = 0
            response.headers['Content-type'] = 'application/json'
            #log.info("results workshop: %s"%json.dumps({'statusCode':statusCode, 'result':result}))
            return json.dumps({'statusCode':statusCode, 'result':result})
        else:    
            return render('/derived/6_item_in_listing.bootstrap')