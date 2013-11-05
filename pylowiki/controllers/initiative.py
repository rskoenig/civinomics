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

import simplejson as json

log = logging.getLogger(__name__)

class InitiativeController(BaseController):
    
    def __before__(self, action, id1 = None, id2 = None, id3 = None):
        c.user = None
        c.initiative = None
        existingList = ['initiativeEditHandler', 'initiativeShowHandler', 'initiativeEdit', 'photoUploadHandler', 'resourceEdit']
        adminList = ['initiativeEditHandler', 'initiativeEdit', 'photoUploadHandler']
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

                else:
                  abort(404)  
        else:
            abort(404)

        
        # only the author or an admin can edit  
        if action in adminList:
            if 'user' not in session:
                abort(404)
            if c.user['email'] != c.authuser['email'] and not userLib.isAdmin(c.authuser.id):
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
            
        userLib.setUserPrivs()


    def initiativeNewHandler(self):
        title = ""
        description = ""
        scope = ""
        
        if 'initiativeTitle' in request.params:
            title = request.params['initiativeTitle']
        else:
            title = 'New Initiative'
            
        if 'initiativeDescription' in request.params:
            description = request.params['initiativeDescription']
        else:
            description = ''
        
        if 'initiativeScope' in request.params:
            level = request.params['initiativeScope']
            userScope = geoInfoLib.getGeoScope(c.user['postalCode'], c.user['country'])
            scopeList = userScope.split('|')
            index = 0
            for scope in scopeList:
                if scope == '':
                    scopeList[index] = '0'
                index += 1
                
            if level == 'city':
                scopeList[9] = '0'
            elif level == 'county':
                scopeList[9] = '0'
                scopeList[8] = '0'
                
            scope = '|'.join(scopeList)
            log.info('userScope is %s'%userScope)
             
        elif 'initiativeRegionScope' in request.params:
            scope = request.params['initiativeRegionScope']
            level = scope
        else:
            log.init("no initiative scope")
            
        if scope != '':
            c.initiative = initiativeLib.Initiative(c.user, title, description, scope)
            c.level = level
        else:
            log.info("missing initiaitve info: title is %s description is %s and scope is %s"%(title, description, scope))
            abort(404)
            
        c.saveMessage = "Changes saved."
            
        return render('/derived/6_initiative_edit.bootstrap')
    
    def initiativeCheck(self):
        atrList = ['title', 'description', 'cost', 'scope', 'tag', 'background', 'directoryNum_photos', 'pictureHash_photos']
        for atr in atrList:
            complete = 1
            if atr not in c.initiative:
                complete = 0
            elif c.initiative[atr] == '':
                complete = 0
                
        return complete
        
    def initiativeEdit(self):
        
        return render('/derived/6_initiative_edit.bootstrap')
        
    def initiativeEditHandler(self):
        if 'title' in request.params:
            c.initiative['title'] = request.params['title']
            c.initiative['url'] = utils.urlify(c.initiative['title'])
        if 'description' in request.params:
            c.initiative['description'] = request.params['description']
        if 'cost' in request.params:
            c.initiative['cost'] = request.params['cost']
        if 'level' in request.params:
            level = request.params['level']
            userScope = geoInfoLib.getGeoScope(c.user['postalCode'], c.user['country'])
            scopeList = userScope.split('|')
            index = 0
            for scope in scopeList:
                if scope == '':
                    scopeList[index] = '0'
                index += 1

            if level == 'city':
                scopeList[9] = '0'
            elif level == 'county':
                scopeList[9] = '0'
                scopeList[8] = '0'
            c.initiative['scope'] = '|'.join(scopeList)
        if 'tag' in request.params:
            c.initiative['tags'] = request.params['tag']
        if 'data' in request.params:
            c.initiative['background'] = request.params['data']
        
        if 'public' in request.params:
            log.info("got %s"%request.params['public'])
        if 'public' in request.params and request.params['public'] == 'yes':
            if c.complete and c.initiative['public'] == '0':
                c.initiative['public'] = '1'
                
        dbHelpers.commit(c.initiative)
        revisionLib.Revision(c.authuser, c.initiative)

        c.saveMessage = "Changes saved."
        
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
                tWidth = request.params['width']
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
        
        c.revisions = revisionLib.getRevisionsForThing(c.initiative)
        c.isFollowing = False
        if 'user' in session:
            c.isFollowing = followLib.isFollowing(c.authuser, c.initiative)
            log.info("c.isFollowing is %s"%c.isFollowing)
        
        if c.initiative.objType == 'initiative' and 'views' not in c.initiative:
            c.initiative['views'] = u'0'
            
        views = int(c.initiative['views']) + 1
        c.initiative['views'] = str(views)
        dbHelpers.commit(c.initiative)
            
        return render('/derived/6_initiative_home.bootstrap')
        

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
            
