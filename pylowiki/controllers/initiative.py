# -*- coding: utf-8 -*-
import logging

from pylons import config, request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylowiki.lib.base import BaseController, render

import pylowiki.lib.helpers         as h
import pylowiki.lib.db.initiative   as initiativeLib
import pylowiki.lib.db.geoInfo      as geoInfoLib
import pylowiki.lib.db.event        as eventLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.resource     as resourceLib
import pylowiki.lib.db.discussion   as discussionLib
import pylowiki.lib.utils           as utils
import pylowiki.lib.db.dbHelpers    as dbHelpers
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.db.revision     as revisionLib
import pylowiki.lib.images          as imageLib
import pylowiki.lib.db.follow       as followLib
import pylowiki.lib.db.facilitator  as facilitatorLib

import simplejson as json

log = logging.getLogger(__name__)

class InitiativeController(BaseController):
    
    def __before__(self, action, id1 = None, id2 = None, id3 = None):
        c.user = None
        c.initiative = None
        existingList = ['initiativeEditHandler', 'initiativeShowHandler', 'initiativeEdit', 'photoUploadHandler', 'resourceEdit', 'getInitiativeAuthors']
        adminList = ['initiativeEditHandler', 'initiativeEdit', 'photoUploadHandler']
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
                    else:
                        c.photo_url = "/images/icons/generalInitiative_lg.jpg"
                        c.bgPhoto_url = "/images/icons/generalInitiative_lg.jpg"
                        c.thumbnail_url = "/images/icons/generalInitiative.jpg"
                    c.bgPhoto_url = "'" + c.bgPhoto_url + "'"

                else:
                  abort(404)  
        else:
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
                
            c.complete = self.initiativeCheck()
            
        c.resources = []
        if c.initiative:
            # for compatibility with comments
            c.thing = c.initiative
            c.discussion = discussionLib.getDiscussionForThing(c.initiative)
            c.resources = resourceLib.getResourcesByInitiativeCode(c.initiative['urlCode'])
            disabledResources = resourceLib.getResourcesByInitiativeCode(c.initiative['urlCode'], '1')
            if disabledResources:
                for dr in disabledResources:
                    c.resources.append(dr)
            
        if c.user:
            userGeo = geoInfoLib.getGeoInfo(c.user.id)[0]
            c.authorGeo = {}
            c.authorGeo['cityURL'] = '/workshops/geo/earth/%s/%s/%s/%s' %(userGeo['countryURL'], userGeo['stateURL'], userGeo['countyURL'], userGeo['cityURL'])
            c.authorGeo['cityTitle'] = userGeo['cityTitle']
            c.authorGeo['stateURL'] = '/workshops/geo/earth/%s/%s' %(userGeo['countryURL'], userGeo['stateURL'])
            c.authorGeo['stateTitle'] = userGeo['stateTitle']


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
        c.initiative = initiativeLib.Initiative(c.user, title, description, scope)
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
                c.saveMessage = "Your initiative is now live! It is publicly viewable."
        elif 'public' in request.params and request.params['public'] == 'unpublish':
            if c.initiative['public'] == '1':
                c.initiative['public'] = '0'
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
        c.complete = self.initiativeCheck()
        
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
        if c.authuser.id != c.user.id:
            abort(404)

        if 'files[]' in request.params:
            file = request.params['files[]']
            filename = file.filename
            file = file.file
            image = imageLib.openImage(file)
            if not image:
                abort(404) # Maybe make this a json response instead
            imageHash = imageLib.generateHash(filename, c.authuser)
            
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
            image = imageLib.cropImage(image, imageHash, dims, clientWidth = clientWidth, clientHeight = clientHeight)
            image = imageLib.resizeImage(image, imageHash, 480, 480)
            image = imageLib.saveImage(image, imageHash, 'photos', 'photo')
            image = imageLib.resizeImage(image, imageHash, 160, 160)
            image = imageLib.saveImage(image, imageHash, 'photos', 'thumbnail')
            
            jsonResponse =  {'files': [
                                {
                                    'name':filename,
                                    'thumbnail_url':'/images/photos/%s/thumbnail/%s.png' %(c.initiative['directoryNum_photos'], imageHash),
                                    'image_hash':imageHash
                                }
                            ]}
            return json.dumps(jsonResponse)
        else:
            abort(404)
            
 
    def initiativeShowHandler(self):
        c.facebookAppId = config['facebook.appid']
        c.channelUrl = config['facebook.channelUrl']
        c.baseUrl = utils.getBaseUrl()

        c.revisions = revisionLib.getRevisionsForThing(c.initiative)
        c.isFollowing = False
        if 'user' in session:
            c.isFollowing = followLib.isFollowing(c.authuser, c.initiative)
            log.info("c.isFollowing is %s"%c.isFollowing)
        
        if c.initiative.objType == 'initiative' and 'views' not in c.initiative:
            c.initiative['views'] = u'0'
        
        if c.initiative.objType != 'revision':    
            views = int(c.initiative['views']) + 1
            c.initiative['views'] = str(views)
            dbHelpers.commit(c.initiative)

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
        
    @h.login_required
    def resourceEditHandler(self, id1, id2, id3):
        
        if 'user' not in session:
            abort(404)
        if 'resourceTitle' in request.params():
            title = request.params('resourceTitle')
        else:
            title = "Sample title"
            
        if 'resourceLink' in request.params():
            link = request.params('resourceLink')
        else:
            title = "http://example.com"
            
        if 'resourceText' in request.params():
            title = request.params('resourceText')
        else:
            title = "Sample text"
            
