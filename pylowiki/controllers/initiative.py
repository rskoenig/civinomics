# -*- coding: utf-8 -*-
import logging
import datetime
import pickle

from pylons import config, request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylowiki.lib.base import BaseController, render

import pylowiki.lib.db.initiative   as initiativeLib
import pylowiki.lib.db.geoInfo      as geoInfoLib
import pylowiki.lib.db.event        as eventLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.resource     as resourceLib
import pylowiki.lib.db.discussion   as discussionLib
import pylowiki.lib.db.dbHelpers    as dbHelpers
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.db.revision     as revisionLib
import pylowiki.lib.db.follow       as followLib
import pylowiki.lib.db.facilitator  as facilitatorLib
import pylowiki.lib.json            as jsonLib

from pylowiki.lib.facebook          import FacebookShareObject
import pylowiki.lib.helpers         as h
import pylowiki.lib.images          as imageLib
import pylowiki.lib.utils           as utils

import simplejson as json

log = logging.getLogger(__name__)

class InitiativeController(BaseController):
    
    def __before__(self, action, id1 = None, id2 = None, id3 = None):
        log.info("inititive before action is %s"%action)
        c.user = None
        c.initiative = None
        existingList = ['initiativeEditHandler', 'initiativeShowHandler', 'initiativeEdit', 'photoUploadHandler', 'resourceEdit', 'updateEdit', 'updateEditHandler', 'updateShow', 'getInitiativeAuthors', 'getJson']
        adminList = ['initiativeEditHandler', 'initiativeEdit', 'photoUploadHandler', 'updateEdit', 'updateEditHandler']
        c.saveMessageClass = 'alert-success'
        c.error = False
        if action == 'initiativeNewHandler' and id1 is not None and id2 is not None:
            c.user = userLib.getUserByCode(id1)
            if not c.user:
                abort(404)
        elif action in existingList and id1 is not None and id2 is not None:
            c.initiative = initiativeLib.getInitiative(id1)
            if not c.initiative:
                c.initiative = revisionLib.getRevisionByCode(id1)
                if not c.initiative:
                    abort(404)
                            
            if c.initiative:
                #log.info("got initiative")
                c.user = userLib.getUserByCode(c.initiative['userCode'])

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
                    c.photo_url = "/images/photos/%s/orig/%s.png"%(c.initiative['directoryNum_photos'], c.initiative['pictureHash_photos'])
                    c.bgPhoto_url = "/images/photos/%s/photo/%s.png"%(c.initiative['directoryNum_photos'], c.initiative['pictureHash_photos'])
                    c.thumbnail_url = "/images/photos/%s/thumbnail/%s.png"%(c.initiative['directoryNum_photos'], c.initiative['pictureHash_photos'])
                    if 'directoryNum_cover' and 'pictureHash_cover' in c.initiative:
                        c.cover_url = "/images/cover/%s/orig/%s.png"%(c.initiative['directoryNum_cover'], c.initiative['pictureHash_cover'])
                    else:
                        c.cover_url = False
                else:
                    c.photo_url = "/images/icons/generalInitiative_lg.jpg"
                    c.bgPhoto_url = "/images/icons/generalInitiative_lg.jpg"
                    c.thumbnail_url = "/images/icons/generalInitiative.jpg"
                    c.cover_url = False
                c.bgPhoto_url = "'" + c.bgPhoto_url + "'"

            else:
                #log.info("abort 1")
                abort(404)  
        else:
            #log.info("abort 2")
            abort(404)

        # only the author or an admin can edit 
        c.iPrivs = False

        facilitator = False
        f = facilitatorLib.getFacilitatorsByUserAndInitiative(c.authuser, c.initiative)
        if f != False and f != 'NoneType' and len(f) != 0:
            if f[0]['pending'] == '0' and f[0]['disabled'] == '0':
                facilitator = True

        if 'user' in session and (c.user['email'] == c.authuser['email'] or userLib.isAdmin(c.authuser.id)) or facilitator:
            c.iPrivs = True

        if action in adminList:
            if 'user' not in session:
                abort(404)
            if c.iPrivs == False:
                abort(404)
                
            # c.complete = self.initiativeCheck()
            # removing requirements for publishing an initiative
            c.complete = True
            
        c.resources = []
        c.updates = []
        if c.initiative:
            #log.info("got initiative 2 action is %s"%action)
            # for compatibility with comments
            c.thing = c.initiative
            c.discussion = discussionLib.getDiscussionForThing(c.initiative)
            c.updates = discussionLib.getUpdatesForInitiative(c.initiative['urlCode'])
            c.resources = resourceLib.getResourcesByInitiativeCode(c.initiative['urlCode'])
            disabledResources = resourceLib.getResourcesByInitiativeCode(c.initiative['urlCode'], '1')
            if disabledResources:
                for dr in disabledResources:
                    c.resources.append(dr)
                    
        if action == 'updateShow' and id3 != None:
            c.update = discussionLib.getDiscussion(id3)
            if not c.update:
                c.update = revisionLib.getRevisionByCode(id3)
                if not c.update:
                    abort(404)
            # for compatability with comments
            c.thing = c.update
            
        if c.user:
            userGeo = geoInfoLib.getGeoInfo(c.user.id)[0]
            c.authorGeo = {}
            c.authorGeo['cityURL'] = '/workshops/geo/earth/%s/%s/%s/%s' %(userGeo['countryURL'], userGeo['stateURL'], userGeo['countyURL'], userGeo['cityURL'])
            c.authorGeo['cityTitle'] = userGeo['cityTitle']
            c.authorGeo['stateURL'] = '/workshops/geo/earth/%s/%s' %(userGeo['countryURL'], userGeo['stateURL'])
            c.authorGeo['stateTitle'] = userGeo['stateTitle']

        ################## FB SHARE ###############################
        # these values are needed for facebook sharing of a workshop
        # - details for sharing a specific idea are modified in the view idea function
        if c.initiative:
            shareOk = initiativeLib.isPublic(c.initiative)
            bgPhoto_url, photo_url, thumbnail_url = utils.initiativeImageURL(c.initiative)
            c.description_nohtml = utils.getTextFromMisaka(c.initiative['description'])
            c.facebookShare = FacebookShareObject(
                itemType='initiative',
                url=utils.initiativeURL(c.initiative),
                parentCode=c.initiative['urlCode'],
                title=c.initiative['title'],
                description=c.description_nohtml,
                image=photo_url,
                shareOk = shareOk
            )
        # add this line to tabs in the workshop in order to link to them on a share:
        # c.facebookShare.url = c.facebookShare.url + '/activity'
        #################################################

        userLib.setUserPrivs()


    def initiativeNewHandler(self):
        if 'initiativeTitle' in request.params:
            title = request.params['initiativeTitle']
        else:
            title = 'New Initiative'
            
        if 'initiativeDescription' in request.params:
            description = request.params['initiativeDescription']
        else:
            description = ''

        # the scope if initiative is created from a geoSearch page
        if 'initiativeRegionScope' in request.params:
            scope = request.params['initiativeRegionScope']
            
        else:
            scope = '0|0|united-states|0|0|0|0|0|0|0'
            
        goal = self.getInitiativeGoal(scope)

        c.thumbnail_url = "/images/icons/generalInitiative.jpg"
        c.bgPhoto_url = "'" + c.thumbnail_url + "'"
        
        # shortcut scoping for 'My County, My City, My Zip Code'
        #if 'initiativeScope' in request.params:
        #  level = request.params['initiativeScope']
        #    userScope = geoInfoLib.getGeoScope(c.user['postalCode'], c.user['country'])
        #    scopeList = userScope.split('|')
        #    index = 0
        #    for scope in scopeList:
        #        if scope == '':
        #            scopeList[index] = '0'
        #        index += 1
        #        
        #    if level == 'city':
        #        scopeList[9] = '0'
        #    elif level == 'county':
        #        scopeList[9] = '0'
        #        scopeList[8] = '0'
        #        
        #    scope = '|'.join(scopeList)
        #    log.info('userScope is %s'%userScope)
        
            
        #create the initiative
        c.initiative = initiativeLib.Initiative(c.user, title, description, scope, goal = goal)
        log.info('%s goal is %s' % (c.initiative['title'], c.initiative['goal']))
        
        session['facilitatorInitiatives'].append(c.initiative['urlCode'])
        facilitatorInitiatives = pickle.loads(str(c.authuser["facilitatorInitiatives"]))
        if c.initiative['urlCode'] not in facilitatorInitiatives:
            facilitatorInitiatives.append(c.initiative['urlCode'])
            c.authuser["facilitatorInitiatives"] = str(pickle.dumps(facilitatorInitiatives))
            dbHelpers.commit(c.authuser)
        
        c.level = scope

        # now that the initiative edits have been commited, update the scopeProps for the template to use:
        scopeProps = utils.getPublicScope(c.initiative)
        scopeName = scopeProps['name'].title()
        scopeLevel = scopeProps['level'].title()
        if scopeLevel == 'Earth':
            c.scopeTitle = scopeName
        else:
            c.scopeTitle = scopeLevel + ' of ' + scopeName
        c.scopeFlag = scopeProps['flag']
        c.scopeHref = scopeProps['href']

        # initialize the scope dropdown selector in the edit template
        c.states = geoInfoLib.getStateList('United-States')
        # ||country||state||county||city|zip
        if c.initiative['scope'] != '':
            geoTags = c.initiative['scope'].split('|')
            c.country = utils.geoDeurlify(geoTags[2])
            c.state = utils.geoDeurlify(geoTags[4])
            c.county = utils.geoDeurlify(geoTags[6])
            c.city = utils.geoDeurlify(geoTags[8])
            c.postal = utils.geoDeurlify(geoTags[9])
        else:
            c.country = "0"
            c.state = "0"
            c.county = "0"
            c.city = "0"
            c.postal = "0"

        c.editInitiative = True
       
        return render('/derived/6_initiative_edit.bootstrap')
    
    def initiativeCheck(self):
        atrList = ['title', 'scope', 'tags', 'description', 'funding_summary', 'cost', 'background', 'proposal', 'directoryNum_photos', 'pictureHash_photos']
        completeList = []
        for atr in atrList:
            complete = 0
            if atr in c.initiative:
                if c.initiative[atr] != '':
                    complete = 1
            else:
                complete = 0
            completeList.append(complete)

        if not 0 in completeList:
            allComplete = 1
        else:
            allComplete = 0
                
        return allComplete
        
    def initiativeEdit(self):
        # initialize the scope dropdown selector in the edit template
        c.states = geoInfoLib.getStateList('United-States')
        # ||country||state||county||city|zip
        if c.initiative['scope'] != '':
            geoTags = c.initiative['scope'].split('|')
            c.country = utils.geoDeurlify(geoTags[2])
            c.state = utils.geoDeurlify(geoTags[4])
            c.county = utils.geoDeurlify(geoTags[6])
            c.city = utils.geoDeurlify(geoTags[8])
            c.postal = utils.geoDeurlify(geoTags[9])
        else:
            c.country = "0"
            c.state = "0"
            c.county = "0"
            c.city = "0"
            c.postal = "0"

        if 'public' in request.params:
            log.info("got %s"%request.params['public'])
        if 'public' in request.params and request.params['public'] == 'publish':
            if c.complete and c.initiative['public'] == '0':
                c.initiative['public'] = '1'
                startTime = datetime.datetime.now(None)
                c.initiative['publishDate'] = startTime
                c.initiative['unpublishDate'] = u'0000-00-00'
                dbHelpers.commit(c.initiative)
                c.saveMessage = "Your initiative is now live. Share it with your friends!"
                return redirect('/initiative/%s/%s' % (c.initiative['urlCode'], c.initiative['url']))

        elif 'public' in request.params and request.params['public'] == 'unpublish':
            if c.initiative['public'] == '1':
                c.initiative['public'] = '0'
                endTime = datetime.datetime.now(None)
                c.initiative['unpublishDate'] = endTime
                dbHelpers.commit(c.initiative)
                c.saveMessage = "Your initiative has been unpublished. It is no longer publicy viewable."

        c.editInitiative = True

        return render('/derived/6_initiative_edit.bootstrap')
        
    def initiativeEditHandler(self):
        iKeys = ['inititive_tags', 'initiative_scope', 'initiative_url', 'initiative_title', 'initiative_public']
        if 'title' in request.params:
            c.initiative['title'] = request.params['title']
            c.initiative['url'] = utils.urlify(c.initiative['title'])
        if 'description' in request.params:
            c.initiative['description'] = request.params['description']
        if 'funding_summary' in request.params:
            c.initiative['funding_summary'] = request.params['funding_summary']
        if 'cost' in request.params:
            cost = request.params['cost']
            cost = cost.replace(',','')
            cost = cost.replace(' ','')
            try:
                cost = int(cost)
                c.initiative['cost'] = cost
            except ValueError:
                c.error = True
                errorMessage = "Invalid cost number"
                c.initiative['cost'] = 0
            
        if 'tag' in request.params:
            c.initiative['tags'] = request.params['tag']
        if 'background' in request.params:
            c.initiative['background'] = request.params['background']
        if 'proposal' in request.params:
            c.initiative['proposal'] = request.params['proposal']


        # update the scope based on info in the scope dropdown selector, if they're in the submitted form
        if 'geoTagCountry' in request.params:
            if 'geoTagCountry' in request.params and request.params['geoTagCountry'] != '0':
                geoTagCountry = request.params['geoTagCountry']
            else:
                geoTagCountry = "0"
                
            if 'geoTagState' in request.params and request.params['geoTagState'] != '0':
                geoTagState = request.params['geoTagState']
            else:
                geoTagState = "0"
                
            if 'geoTagCounty' in request.params and request.params['geoTagCounty'] != '0':
                geoTagCounty = request.params['geoTagCounty']
            else:
                geoTagCounty = "0"
                
            if 'geoTagCity' in request.params and request.params['geoTagCity'] != '0':
                geoTagCity = request.params['geoTagCity']
            else:
                geoTagCity = "0"
                
            if 'geoTagPostal' in request.params and request.params['geoTagPostal'] != '0':
                geoTagPostal = request.params['geoTagPostal']
            else:
                geoTagPostal = "0"

            # assemble the scope string 
            # ||country||state||county||city|zip
            geoTagString = "0|0|" + utils.urlify(geoTagCountry) + "|0|" + utils.urlify(geoTagState) + "|0|" + utils.urlify(geoTagCounty) + "|0|" + utils.urlify(geoTagCity) + "|" + utils.urlify(geoTagPostal)
            if c.initiative['scope'] != geoTagString:
                c.initiative['scope'] = geoTagString
                # need to come back and add 'updateInitiativeChildren' when it is written
                #workshopLib.updateWorkshopChildren(c.w, 'workshop_public_scope')
                
                # update the goal vote number based on new scope
                c.initiative['goal'] = self.getInitiativeGoal(geoTagString)
                log.info('%s' % c.initiative['goal'])
                
                wchanges = 1
                
        for key in iKeys:
            initiativeLib.updateInitiativeChildren(c.initiative, key)
                
        dbHelpers.commit(c.initiative)
        revisionLib.Revision(c.authuser, c.initiative)

        # now that the initiative edits have been commited, update the scopeProps for the template to use:
        scopeProps = utils.getPublicScope(c.initiative)
        scopeName = scopeProps['name'].title()
        scopeLevel = scopeProps['level'].title()
        if scopeLevel == 'Earth':
            c.scopeTitle = scopeName
        else:
            c.scopeTitle = scopeLevel + ' of ' + scopeName
        c.scopeFlag = scopeProps['flag']
        c.scopeHref = scopeProps['href']

        # initialize the scope dropdown selector in the edit template
        c.states = geoInfoLib.getStateList('United-States')
        # ||country||state||county||city|zip
        if c.initiative['scope'] != '':
            geoTags = c.initiative['scope'].split('|')
            c.country = utils.geoDeurlify(geoTags[2])
            c.state = utils.geoDeurlify(geoTags[4])
            c.county = utils.geoDeurlify(geoTags[6])
            c.city = utils.geoDeurlify(geoTags[8])
            c.postal = utils.geoDeurlify(geoTags[9])
        else:
            c.country = "0"
            c.state = "0"
            c.county = "0"
            c.city = "0"
            c.postal = "0"

        if c.error:
            c.saveMessageClass = 'alert-error'
            c.saveMessage = errorMessage
        else:
            c.saveMessage = "Changes saved."

        c.editInitiative = True
        #c.complete = self.initiativeCheck()
        # removing requirements for publishing an intiative to make it easier/ encourage more ideation
        c.complete = True
        
        return render('/derived/6_initiative_edit.bootstrap')
        
    @h.login_required
    def photoUploadHandler(self, id1, id2):
        """
            Ideally:  
            1) User selects image, gets presented with aspect-ratio constrained selection.
            2) User adjusts centering and dimensions, hits 'start'
            3) Process image - detailed below
        
            Grab the uploaded file.  Hash and save the original first.  Then process.
            Processing means:
            1) Check to ensure it is an image (should be done in the hash + save step)
            2) Check for square dimensions.  If not square, crop.  Do not save the image here, just pass on the image object.
            3) If necessary, resize the dimensions of the image to 1200px x 1200px.  Save the final image here.
            
            The client expects a json-encoded string with the following format:
            
            {"files": [
              {
                "name": "picture1.jpg",
                "size": 902604,
                "url": "http:\/\/example.org\/files\/picture1.jpg",
                "thumbnail_url": "http:\/\/example.org\/files\/thumbnail\/picture1.jpg",
                "delete_url": "http:\/\/example.org\/files\/picture1.jpg",
                "delete_type": "DELETE"
              },
              {
                "name": "picture2.jpg",
                "size": 841946,
                "url": "http:\/\/example.org\/files\/picture2.jpg",
                "thumbnail_url": "http:\/\/example.org\/files\/thumbnail\/picture2.jpg",
                "delete_url": "http:\/\/example.org\/files\/picture2.jpg",
                "delete_type": "DELETE"
              }
            ]}
        """
        if c.iPrivs == False:
            abort(404)
            
        cover = False
        
        if 'files[]' in request.params:
            file = request.params['files[]']
            filename = file.filename
            file = file.file
            image = imageLib.openImage(file)
            
        elif 'cover[]' in request.params:
            cover = True
            file = request.params['cover[]']
            filename = file.filename
            file = file.file
            image = imageLib.openImage(file)
        else:
            abort(404)
                
        if not image:
            abort(404) # Maybe make this a json response instead
        imageHash = imageLib.generateHash(filename, c.authuser)
        
        if cover:
            log.info("I'm a cover!!")
            image = imageLib.saveImage(image, imageHash, 'cover', 'orig', thing = c.initiative)
        else:
            log.info("I'm not a cover")
            image = imageLib.saveImage(image, imageHash, 'photos', 'orig', thing = c.initiative)
        
        width = min(image.size)
        x = 0
        y = 0
        if 'width' in request.params:
            width = request.params['width']
            if not width or width == 'undefined':
                width = 100
            else:
                width = int(float(width))
        if 'x' in request.params:
            x = request.params['x']
            if not x or x == 'undefined':
                x = 0
            else:
                x = int(float(x))
        if 'y' in request.params:
            y = request.params['y']
            if not y or y == 'undefined':
                y = 0
            else:
                y = int(float(y))
        dims = {'x': x, 
                'y': y, 
                'width':width,
                'height':width}
        clientWidth = -1
        clientHeight = -1
        if 'clientWidth' in request.params:
            clientWidth = request.params['clientWidth']
            if not clientWidth or clientWidth == 'null':
                clientWidth = -1
        if 'clientHeight' in request.params:
            clientHeight = request.params['clientHeight']
            if not clientHeight or clientHeight == 'null':
                clientHeight = -1
        
        if cover:
            picType = 'cover'
        else:
            picType = 'photos'
             
        image = imageLib.cropImage(image, imageHash, dims, clientWidth = clientWidth, clientHeight = clientHeight)
        image = imageLib.resizeImage(image, imageHash, 480, 480)
        image = imageLib.saveImage(image, imageHash, picType, 'photo')
        image = imageLib.resizeImage(image, imageHash, 160, 160)
        image = imageLib.saveImage(image, imageHash, picType, 'thumbnail')
        
        
        
        jsonResponse =  {'files': [
                            {
                                'name':filename,
                                'thumbnail_url':'/images/photos/%s/thumbnail/%s.png' %(c.initiative['directoryNum_photos'], imageHash),
                                'image_hash':imageHash
                            }
                        ]}
        return json.dumps(jsonResponse)
        
            
 
    def initiativeShowHandler(self):

        c.revisions = revisionLib.getRevisionsForThing(c.initiative)
        c.isFollowing = False
        if 'user' in session:
            c.isFollowing = followLib.isFollowing(c.authuser, c.initiative)
            log.info("c.isFollowing is %s"%c.isFollowing)
        
        if c.initiative.objType == 'initiative' and 'views' not in c.initiative:
            c.initiative['views'] = u'0'
        
        if c.initiative.objType != 'revision' and 'views' in c.initiative:
            views = int(c.initiative['views']) + 1
            c.initiative['views'] = str(views)
            dbHelpers.commit(c.initiative)

        c.numComments = 0
        if 'numComments' in c.initiative:
            c.numComments = c.initiative['numComments']

        c.authors = [c.user]
        coAuthors = facilitatorLib.getFacilitatorsByInitiative(c.initiative)
        for author in coAuthors:
            if author['pending'] == '0' and author['disabled'] == '0':
                c.authors.append(author)
        
        c.initiativeHome = True

        return render('/derived/6_initiative_home.bootstrap')


    def getInitiativeAuthors(self):
        authors = []
        coAuthors = facilitatorLib.getFacilitatorsByInitiative(c.initiative)
        for author in coAuthors:
            authors.append(author)

        result = []
        for a in authors:
            entry = {}
            u = userLib.getUserByID(a.owner)
            entry['name'] = u['name']
            entry['photo'] = utils._userImageSource(u)
            entry['urlCode'] = u['urlCode']
            entry['url'] = u['url']
            entry['pending'] = a['pending']
            userGeo = geoInfoLib.getGeoInfo(u.id)[0]
            entry['cityURL'] = '/workshops/geo/earth/%s/%s/%s/%s' %(userGeo['countryURL'], userGeo['stateURL'], userGeo['countyURL'], userGeo['cityURL'])
            entry['cityTitle'] = userGeo['cityTitle']
            entry['stateURL'] = '/workshops/geo/earth/%s/%s' %(userGeo['countryURL'], userGeo['stateURL'])
            entry['stateTitle'] = userGeo['stateTitle']

            result.append(entry)
        if len(result) == 0:
            return json.dumps({'statusCode':1})
        return json.dumps({'statusCode': 0, 'result': result})


    @h.login_required
    def resourceEdit(self, id1, id2, id3):
        c.editResource = True
        if 'user' not in session:
            log.info("someone not logged in tried to add a resource to an initiative...")
            abort(404)
            
        if id3 == 'new':
            c.resource = None
            
        else:
            c.resource = resourceLib.getResource(id3)
            if not c.resource:
                log.info("no resource with this code: %s"%id3)
                abort(404)
            
        return render('/derived/6_initiative_resource.bootstrap')
        
    def updateShow(self):
        c.revisions = revisionLib.getRevisionsForThing(c.update)
        
        return render('/derived/6_initiative_update.bootstrap')
        
    @h.login_required       
    def updateEdit(self):
        c.editUpdate = True
        return render('/derived/6_initiative_update.bootstrap')
        
    @h.login_required
    def updateEditHandler(self):
        payload = json.loads(request.body)
        if 'title' in payload:
            title = payload['title']
        else:
            title = "Sample Title"
        
        if not c.update:
            d = discussionLib.Discussion(owner = c.authuser, discType = 'update', attachedThing = c.initiative, title = title)
            log.info("got d.d, objtype of d is %s"%d.d.objType)
            
        d.d['title'] = title
            
        if 'text' in payload:
            d.d['text'] = payload['text']
        else:
            d.d['text'] = "Sample text"
            
        dbHelpers.commit(d.d)
        revisionLib.Revision(c.authuser, d.d)
        
        jsonReturn = '{"state":"Success", "updateCode":"' + d.d['urlCode'] + '","updateURL":"' + d.d['url'] + '"}'
        return jsonReturn
       
        
    def getInitiativeGoal(self, scope):
        geoScope = scope.split('|') 
        if geoScope[2] == '0':
            #earth
            population = 7172450000
            
        elif geoScope[4] == '0':
            # country
            geoInfo = geoInfoLib.getCountryInfo(geoScope[2]) 
            if geoInfo:
                population = geoInfo['Country_population']
            
        elif geoScope[6] == '0':
            #state
            geoInfo = geoInfoLib.getStateInfo(geoScope[4], geoScope[2]) 
            if geoInfo:
                population = geoInfo['Population']
            
        elif geoScope[8] == '0':
            #county
            county = geoInfoLib.geoDeurlify(geoScope[6])
            geoInfo = geoInfoLib.getCountyInfo(county, geoScope[4], geoScope[2])
            if geoInfo:
                population = geoInfo['Population']

        elif geoScope[9] == '0':
            #city
            city = geoInfoLib.geoDeurlify(geoScope[8])
            geoInfo = geoInfoLib.getCityInfo(city, geoScope[4], geoScope[2]) 
            if geoInfo:
                population = geoInfo['Population']

        else:
            #zip
            geoInfo = geoInfoLib.getPostalInfo(geoScope[9]) 
            if geoInfo:
                population = geoInfo['Population']
        
        percentVoters = 0.35
        percentSigsNeeded = 0.10
        goalPercent = percentVoters * percentSigsNeeded
        
        if population:
            population = int(population)
            goal = int(population * goalPercent)
        else:
            population = 0
            log.info('no population data found')
            goal = 1000
            
        return goal

    def getJson(self):
        entry = jsonLib.getJsonProperties(c.initiative)
        return json.dumps({'statusCode':1, 'thing': entry})
        
            
