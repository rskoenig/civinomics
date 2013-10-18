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
import pylowiki.lib.helpers as h

import simplejson as json
import misaka as m

from pylowiki.lib.base import BaseController, render

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
        if 'submit' not in request.params or 'title' not in request.params:
            return redirect(session['return_to'])
        title = request.params['title'].strip()
        text = request.params['text']
        if title == '':
            return redirect(session['return_to'])
        if len(title) > 120:
            title = title[:120]
        newIdea = ideaLib.Idea(c.authuser, title, text, c.w, c.privs)
        alertsLib.emailAlerts(newIdea)
        return redirect(utils.thingURL(c.w, newIdea))
    
    def showIdea(self, workshopCode, workshopURL, ideaCode, ideaURL):
        # check to see if this is a request from the iphone app
        iPhoneApp = utils.iPhoneRequestTest(request)
        # these values are needed for facebook sharing
        c.facebookAppId = config['facebook.appid']
        c.channelUrl = config['facebook.channelUrl']
        c.baseUrl = config['site_base_url']
        # for creating a link, we need to make sure baseUrl doesn't have an '/' on the end
        if c.baseUrl[-1:] == "/":
            c.baseUrl = c.baseUrl[:-1]
        c.requestUrl = request.url
        c.thingCode = ideaCode
        # standard thumbnail image for facebook shares
        if c.mainImage['pictureHash'] == 'supDawg':
            c.backgroundImage = '/images/slide/slideshow/supDawg.slideshow'
        elif 'format' in c.mainImage.keys():
            c.backgroundImage = '/images/mainImage/%s/orig/%s.%s' %(c.mainImage['directoryNum'], c.mainImage['pictureHash'], c.mainImage['format'])
        else:
            c.backgroundImage = '/images/mainImage/%s/orig/%s.jpg' %(c.mainImage['directoryNum'], c.mainImage['pictureHash'])

        c.thing = ideaLib.getIdea(ideaCode)
        if not c.thing:
            c.thing = revisionLib.getRevisionByCode(ideaCode)
            if not c.thing:
                abort(404)
        # name/title for facebook sharing
        c.name = c.thing['title']
        if 'views' not in c.thing:
            c.thing['views'] = u'0'
            
        views = int(c.thing['views']) + 1
        c.thing['views'] = str(views)
        dbHelpers.commit(c.thing)

        c.discussion = discussionLib.getDiscussionForThing(c.thing)
        c.listingType = 'idea'
        c.revisions = revisionLib.getRevisionsForThing(c.thing)
        
        if 'comment' in request.params:
            c.rootComment = commentLib.getCommentByCode(request.params['comment'])
            if not c.rootComment:
                abort(404)
        if iPhoneApp:
            # if this person is the owner of this idea, we need to pack their vote data in
            #if c.authuser:
                #if idea['userCode'] == c.authuser
            # rated = ratingLib.getRatingForThing(c.authuser, thing) 
            entry = {}
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