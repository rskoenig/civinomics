import logging

from pylons import config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

import pylowiki.lib.db.user             as  userLib
import pylowiki.lib.db.facilitator      as  facilitatorLib
import pylowiki.lib.db.dbHelpers        as  dbHelpers
import pylowiki.lib.db.workshop         as  workshopLib
import pylowiki.lib.db.event            as  eventLib
import pylowiki.lib.db.generic          as  genericLib
import pylowiki.lib.db.resource         as  resourceLib
import pylowiki.lib.db.discussion       as  discussionLib
import pylowiki.lib.db.comment          as  commentLib
import pylowiki.lib.db.revision         as  revisionLib
import pylowiki.lib.db.geoInfo          as  geoInfoLib
import pylowiki.lib.alerts              as  alertsLib
import pylowiki.lib.utils               as  utils
import pylowiki.lib.sort                as  sort
import pylowiki.lib.db.mainImage        as  mainImageLib
import webbrowser
from tldextract import extract
from pylowiki.lib.base import BaseController, render
import pylowiki.lib.helpers as h
import simplejson as json

log = logging.getLogger(__name__)

class ResourceController(BaseController):
    
    def __before__(self, action, parentCode = None, parentURL = None):
        if parentCode is None:
            abort(404)
        parent = genericLib.getThing(parentCode)
        if not parent:
            abort(404)
        if parent.objType == 'workshop':
            c.w = parent
            c.mainImage = mainImageLib.getMainImage(c.w)
            workshopLib.setWorkshopPrivs(c.w)
            if c.w['public_private'] == 'public':
                c.scope = geoInfoLib.getPublicScope(c.w)
            if c.w['public_private'] != 'public':
                if not c.privs['guest'] and not c.privs['participant'] and not c.privs['facilitator'] and not c.privs['admin']:
                    abort(404)
        
            # Demo workshop status
            c.demo = workshopLib.isDemo(c.w)
                    
            #################################################
            # these values are needed for facebook sharing
            c.facebookAppId = config['facebook.appid']
            c.channelUrl = config['facebook.channelUrl']
            c.baseUrl = utils.getBaseUrl()
            # c.requestUrl is for lib_6.emailShare
            c.objectUrl = c.requestUrl = request.url
            c.thingCode = parentCode
            # standard thumbnail image for facebook shares
            if c.mainImage['pictureHash'] == 'supDawg':
                c.backgroundImage = '/images/slide/slideshow/supDawg.slideshow'
            elif 'format' in c.mainImage.keys():
                c.backgroundImage = '/images/mainImage/%s/orig/%s.%s' %(c.mainImage['directoryNum'], c.mainImage['pictureHash'], c.mainImage['format'])
            else:
                c.backgroundImage = '/images/mainImage/%s/orig/%s.jpg' %(c.mainImage['directoryNum'], c.mainImage['pictureHash'])
            # name for facebook share posts
            c.name = c.title = c.w['title']
            c.description = c.w['description']
            #################################################

            if 'user' in session:
                utils.isWatching(c.authuser, c.w)
        elif parent.objType == 'initiative':
            c.initiative = parent
            userLib.setUserPrivs()
        else:
            abort(404)

        c.title = parent['title']
        

    def listing(self, parentCode, parentURL):
        #get the scope to display jurisidction flag
        if c.w['public_private'] == 'public':
            c.scope = workshopLib.getPublicScope(c.w)
        resources = resourceLib.getResourcesByWorkshopCode(parentCode)
        if not resources:
            c.resources = []
        else:
            c.resources = sort.sortBinaryByTopPop(resources)
        disabled = resourceLib.getResourcesByWorkshopCode(parentCode, disabled = '1')
        if disabled:
            c.resources = c.resources + disabled
        c.listingType = 'resources'
        return render('/derived/6_detailed_listing.bootstrap')

    def showResource(self, parentCode, parentURL, resourceCode, resourceURL):
        
        c.thingCode = resourceCode
        log.info("in showResource")
        if c.w:
            #get the scope to display jurisidction flag
            if c.w['public_private'] == 'public':
                c.scope = workshopLib.getPublicScope(c.w)

            # standard thumbnail image for facebook shares
            if c.mainImage['pictureHash'] == 'supDawg':
                c.backgroundImage = '/images/slide/slideshow/supDawg.slideshow'
            elif 'format' in c.mainImage.keys():
                c.backgroundImage = '/images/mainImage/%s/orig/%s.%s' %(c.mainImage['directoryNum'], c.mainImage['pictureHash'], c.mainImage['format'])
            else:
                c.backgroundImage = '/images/mainImage/%s/orig/%s.jpg' %(c.mainImage['directoryNum'], c.mainImage['pictureHash'])


        if c.initiative:
            scopeProps = utils.getPublicScope(c.initiative)
            scopeName = scopeProps['name'].title()
            scopeLevel = scopeProps['level'].title()
            if scopeLevel == 'Earth':
                c.scopeTitle = scopeName
            else:
                c.scopeTitle = scopeLevel + ' of ' + scopeName
            c.scopeFlag = scopeProps['flag']
            c.scopeHref = scopeProps['href']

            if 'directoryNum_photos' in c.initiative and 'pictureHash_photos' in c.initiative:
                c.photo_url = "/images/photos/%s/photo/%s.png"%(c.initiative['directoryNum_photos'], c.initiative['pictureHash_photos'])
                c.thumbnail_url = "/images/photos/%s/thumbnail/%s.png"%(c.initiative['directoryNum_photos'], c.initiative['pictureHash_photos'])
            else:
                c.photo_url = "/images/icons/generalInitiative.jpg"
                c.thumbnail_url = "/images/icons/generalInitiative.jpg"
            c.bgPhoto_url = "'" + c.photo_url + "'"


        c.thing = resourceLib.getResourceByCode(resourceCode)
        if not c.thing:
            c.thing = resourceLib.getResourceByCode(resourceCode, disabled = '1')
            if not c.thing:
                c.thing = revisionLib.getRevisionByCode(resourceCode)
                if not c.thing:
                    abort(404)
        c.resource = c.thing
        # name/title for facebook sharing
        c.name = c.thing['title']
        if 'views' not in c.thing:
            c.thing['views'] = u'0'
            
        views = int(c.thing['views']) + 1
        c.thing['views'] = str(views)
        dbHelpers.commit(c.thing)
        log.info("before c.discussion")
        c.discussion = discussionLib.getDiscussionForThing(c.thing)
        c.listingType = 'resource'
        c.revisions = revisionLib.getRevisionsForThing(c.thing)
        
        if 'comment' in request.params:
            c.rootComment = commentLib.getCommentByCode(request.params['comment'])
            if not c.rootComment:
                abort(404)
                
        if c.w:
            return render('/derived/6_item_in_listing.bootstrap')
        elif c.initiative:
            return render('/derived/6_initiative_resource.bootstrap')

    def thread(self, parentCode, parentURL, resourceCode, resourceURL, commentCode = ''):
        c.resource = resourceLib.getResourceByCode(resourceCode)
        c.discussion = discussionLib.getDiscussionForThing(c.resource)
        c.rootComment = commentLib.getCommentByCode(commentCode)
        c.listingType = 'resource'
        return render('/derived/6_item_in_listing.bootstrap')

    def addResource(self, parentCode, parentURL):
        #get the scope to display jurisidction flag
        if c.w['public_private'] == 'public':
            c.scope = workshopLib.getPublicScope(c.w)
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
    def addResourceHandler(self, parentCode, parentURL):
        if c.w:
            parent = c.w
        else:
            parent = c.initiative
            userLib.setUserPrivs()
            c.w = None
        payload = json.loads(request.body)
        if 'title' not in payload:
            return redirect(session['return_to'])
        title = payload['title'].strip()
        if title == '':
            return redirect(session['return_to'])
        if 'link' not in payload:
            return redirect(session['return_to'])
        if resourceLib.getResourceByLink(payload['link'], parent):
            return redirect(session['return_to']) # Link already submitted
        link = payload['link']
        text = ''
        if 'text' in payload:
            text = payload['text'] # Optional
        if len(title) > 120:
            title = title[:120]
        if c.w:
            newResource = resourceLib.Resource(link, title, c.authuser, c.w, c.privs, text = text)
        else:
            newResource = resourceLib.Resource(link, title, c.authuser, c.w, c.privs, text = text, parent = parent)
        if newResource:
            alertsLib.emailAlerts(newResource)
            jsonReturn = '{"state":"Success", "resourceCode":"' + newResource['urlCode'] + '","resourceURL":"' + newResource['url'] + '"}'
            return jsonReturn
        else:
            return '{"state":"Error", "errorMessage":"Resource not added!"}'

