import logging

from pylons import config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

import pylowiki.lib.db.user             as  userLib
import pylowiki.lib.db.facilitator      as  facilitatorLib
import pylowiki.lib.db.dbHelpers        as  dbHelpers
import pylowiki.lib.db.workshop         as  workshopLib
import pylowiki.lib.db.initiative       as  initiativeLib
import pylowiki.lib.db.event            as  eventLib
import pylowiki.lib.db.generic          as  genericLib
import pylowiki.lib.db.resource         as  resourceLib
import pylowiki.lib.db.discussion       as  discussionLib
import pylowiki.lib.db.comment          as  commentLib
import pylowiki.lib.db.revision         as  revisionLib
import pylowiki.lib.db.geoInfo          as  geoInfoLib
import pylowiki.lib.db.mainImage        as  mainImageLib


import pylowiki.lib.alerts              as  alertsLib
from pylowiki.lib.base                  import BaseController, render
from pylowiki.lib.facebook              import FacebookShareObject
import pylowiki.lib.helpers             as h
import pylowiki.lib.utils               as  utils
import pylowiki.lib.sort                as  sort

import webbrowser
from tldextract import extract

import simplejson as json

log = logging.getLogger(__name__)

class ResourceController(BaseController):
    
    def __before__(self, action, resourceCode, resourceURL, parentCode = None, parentURL = None):
        c.resource = resourceLib.getResourceByCode(resourceCode)
        if not c.resource:
            log.info("no resource after basic lookup")
            c.resource = resourceLib.getResourceByCode(resourceCode, disabled = '1')
            if not c.resource:
                c.resource = revisionLib.getRevisionByCode(resourceCode)
                if not c.resource:
                    abort(404)

        c.thing = c.resource

        userLib.setUserPrivs()  

        if parentCode != None:
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

                if 'user' in session:
                    utils.isWatching(c.authuser, c.w)

                shareType = 'workshop'
                shareUrl = utils.workshopURL(c.w)
                shareDescription = c.w['description'].replace("'", "\\'")
                shareOk = workshopLib.isPublic(c.w)
            elif parent.objType == 'initiative':
                c.initiative = parent
                userLib.setUserPrivs()
                shareType = 'initiative'
                shareUrl = utils.initiativeURL(c.initiative)
                # note: why doesn't the workshop description use misaka? if this changes over we'll need to
                #   catch this happening and mod the uses of c.w['description'] in places that can't handle html
                shareDescription = utils.getTextFromMisaka(c.initiative['description'])
                shareOk = initiativeLib.isPublic(c.initiative)
            else:
                abort(404)

            c.title = parent['title']
        
        else:
            shareType = 'resource'
            c.title = c.resource['title']
            shareUrl = '/resource/%s/%s' % (c.resource['urlCode'], c.resource['url'])
            shareDescription = c.resource['link']
            shareOk = True

        ################## FB SHARE ###############################
        # these values are needed for facebook sharing of a workshop
        # - details for sharing a specific idea are modified in the view idea function
        c.facebookShare = FacebookShareObject(
            itemType=shareType,
            url=shareUrl,
            parentCode=parentCode,
            title=c.title,
            description=shareDescription,
            shareOk = shareOk
        )
        # add this line to tabs in the workshop in order to link to them on a share:
        # c.facebookShare.url = c.facebookShare.url + '/activity'
        #################################################

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

    def showResource(self, resourceCode, resourceURL, parentCode = None, parentURL = None):
        log.info('resourceCode is %s' % resourceCode)
        log.info("in showResource")

        if c.w:
            #get the scope to display jurisidction flag
            if c.w['public_private'] == 'public':
                c.scope = workshopLib.getPublicScope(c.w)

            # standard thumbnail image for facebook shares
            #if c.mainImage['pictureHash'] == 'supDawg':
            #    c.backgroundImage = '/images/slide/slideshow/supDawg.slideshow'
            #elif 'format' in c.mainImage.keys():
            #    c.backgroundImage = '/images/mainImage/%s/orig/%s.%s' %(c.mainImage['directoryNum'], c.mainImage['pictureHash'], c.mainImage['format'])
            #else:
            #    c.backgroundImage = '/images/mainImage/%s/orig/%s.jpg' %(c.mainImage['directoryNum'], c.mainImage['pictureHash'])
            # Note: I need to check on how c.backgroundImage is used elsewhere. If it's only being used with fb shares,
            #   then I should call this with the thumbnail flag set to true, and I don't need to use the c. global, 
            #   I just need to update the c.facebookShare object.
            c.backgroundImage = utils.workshopImageURL(c.w, c.mainImage)
            c.facebookShare.updateImageUrl(c.backgroundImage)
            thingParent = c.w
        elif c.initiative:
            scopeProps = utils.getPublicScope(c.initiative)
            scopeName = scopeProps['name'].title()
            scopeLevel = scopeProps['level'].title()
            if scopeLevel == 'Earth':
                c.scopeTitle = scopeName
            else:
                c.scopeTitle = scopeLevel + ' of ' + scopeName
            c.scopeFlag = scopeProps['flag']
            c.scopeHref = scopeProps['href']

            #if 'directoryNum_photos' in c.initiative and 'pictureHash_photos' in c.initiative:
            #    c.photo_url = "/images/photos/%s/photo/%s.png"%(c.initiative['directoryNum_photos'], c.initiative['pictureHash_photos'])
            #    c.thumbnail_url = "/images/photos/%s/thumbnail/%s.png"%(c.initiative['directoryNum_photos'], c.initiative['pictureHash_photos'])
            #else:
            #    c.photo_url = "/images/icons/generalInitiative.jpg"
            #    c.thumbnail_url = "/images/icons/generalInitiative.jpg"
            #c.bgPhoto_url = "'" + c.photo_url + "'"

            c.bgPhoto_url, c.photo_url, c.thumbnail_url = utils.initiativeImageURL(c.initiative)
            c.facebookShare.updateImageUrl(c.photo_url)
            thingParent = c.initiative
        else:
            scopeProps = utils.getPublicScope(c.resource)



        ################## FB SHARE ###############################
        log.info('%s' % c.resource['title'])
        # not sure why this isn't working
        c.facebookShare.title = c.resource['title']
        c.facebookShare.thingCode = c.resource['urlCode']
        # update url for this item
        c.facebookShare.updateUrl('/resource/%s/%s' % (c.resource['urlCode'], c.resource['url']))
        # set description to be that of the topic's description
        c.facebookShare.description = utils.getTextFromMisaka(c.resource['text'])
        #################################################

        if 'views' not in c.resource:
            c.resource['views'] = u'0'
            
        views = int(c.resource['views']) + 1
        c.resource['views'] = str(views)
        dbHelpers.commit(c.resource)
        log.info("before c.discussion")
        c.discussion = discussionLib.getDiscussionForThing(c.resource)
        c.listingType = 'resource'
        c.revisions = revisionLib.getRevisionsForThing(c.resource)
        
        if 'comment' in request.params:
            c.rootComment = commentLib.getCommentByCode(request.params['comment'])
            if not c.rootComment:
                abort(404)
                
        if c.w:
            return render('/derived/6_item_in_listing.bootstrap')
        elif c.initiative:
            return render('/derived/6_initiative_resource.bootstrap')
        else:
            return render('/derived/6_item_in_listing.bootstrap')

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
    def addResourceHandler(self, parent = None, parentCode = None, parentURL = None):
        if c.w:
            parent = c.w
        elif c.initiative:
            parent = c.initiative
        
        userLib.setUserPrivs()    

        payload = json.loads(request.body)
        if 'title' not in payload:
            return redirect(session['return_to'])
        title = payload['title'].strip()
        if title == '':
            return redirect(session['return_to'])
        if 'link' not in payload:
            return redirect(session['return_to'])
        if parent:
            if resourceLib.getResourceByLink(payload['link'], parent):
                return redirect(session['return_to']) # Link already submitted
        else:
            # need to check in org or geo that link hasn't already been submitted
            pass
        link = payload['link']
        text = ''
        if 'text' in payload:
            text = payload['text'] # Optional
        if len(title) > 120:
            title = title[:120]
        if c.w:
            log.info('submited with c.w')
            newResource = resourceLib.Resource(link, title, c.authuser, c.privs, workshop = c.w, text = text)
        elif c.initiative:
            log.info('submited with c.initiative')
            newResource = resourceLib.Resource(link, title, c.authuser, c.privs, text = text, parent = parent)
        # resource doens't have a parent - it needs its own scope and tag
        else:
            log.info('submited with no parent')
            if 'scope' in payload:
                scope = payload['scope']
            else:
                log.info('no resource scope')
                return redirect(session['return_to'])
            if 'tags' in payload:
                tags = payload['tags']
            else:
                log.info('no resource tags')
                return redirect(session['return_to'])
            newResource = resourceLib.Resource(link, title, c.authuser, c.privs, text = text, scope = scope, tags = tags)

        if newResource:
            alertsLib.emailAlerts(newResource)
            jsonReturn = '{"state":"Success", "resourceCode":"' + newResource['urlCode'] + '","resourceURL":"' + newResource['url'] + '"}'
            log.info('resource added successfully')
            return jsonReturn
        else:
            log.info('resource not added')
            return '{"state":"Error", "errorMessage":"Resource not added!"}'

