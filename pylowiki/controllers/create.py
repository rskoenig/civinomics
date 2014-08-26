#
# -*- coding: utf-8 -*-
import logging
import urllib2
import datetime
import pickle

from pylons                     import config
from pylons                     import request, response, session, tmpl_context as c, url, config
from pylons.controllers.util    import abort, redirect
from pylowiki.lib.base          import BaseController, render
from pylowiki.lib.db.page       import get_all_pages
from pylowiki.lib.db.tag        import getTagCategories
from pylowiki.lib.db.user       import searchUsers, getUserByID
from pylowiki.lib.db.workshop   import getActiveWorkshops
from pylowiki.model             import Thing



import webhelpers.feedgenerator         as feedgenerator
import pylowiki.lib.db.user         	as userLib
import pylowiki.lib.db.message      	as messageLib
import pylowiki.lib.db.photo        	as photoLib
import pylowiki.lib.db.pmember      	as pMemberLib
import pylowiki.lib.sort            	as sort
import pylowiki.lib.db.mainImage    	as mainImageLib
import pylowiki.lib.db.follow       	as followLib
import pylowiki.lib.db.workshop     	as workshopLib
import pylowiki.lib.db.facilitator      as facilitatorLib
import pylowiki.lib.db.listener         as listenerLib
import pylowiki.lib.db.initiative   	as initiativeLib
import pylowiki.lib.db.activity   	    as activityLib
import pylowiki.lib.db.discussion 		as discussionLib
import pylowiki.lib.db.comment 			as commentLib
import pylowiki.lib.utils				as utils
import pylowiki.lib.fuzzyTime			as fuzzyTime	
import pylowiki.lib.db.dbHelpers        as dbHelpers
import pylowiki.lib.db.geoInfo          as geoInfoLib
import pylowiki.lib.helpers             as h
import misaka                           as m
import pylowiki.lib.db.motd             as motdLib
import pylowiki.lib.db.account          as accountLib
import pylowiki.lib.images              as imageLib
import pylowiki.lib.db.resource         as resourceLib
import pylowiki.lib.db.discussion       as discussionLib
import pylowiki.lib.db.idea             as ideaLib
import pylowiki.lib.alerts              as alertsLib
import pylowiki.lib.db.geoInfo          as geoInfoLib
import simplejson                       as json


log = logging.getLogger(__name__)

class CreateController(BaseController):
    def __before__(self, action, id1 = None, id2 = None, id3 = None):
        log.info("Create controller action at before is %s"%action)
        c.user = None
        if action == 'createThing' and id2 is not None and id3 is not None:
            c.user = userLib.getUserByCode(id2)
            userLib.setUserPrivs()
            if not c.user:
                abort(404)

    
    def showCreateForm(self):
        c.tagList = getTagCategories()
        return render('/derived/6_create.bootstrap')

    def showCreateFormGeo(self, thingType, geoString):
        c.tagList = getTagCategories()
        c.geoScope = geoString
        c.geoString = geoInfoLib.getFullScope(geoString)
        log.info("I'm requesting to create a(n) %s", thingType)
        c.thingType = thingType
        return render('/derived/6_create.bootstrap')
    
    def showCreateFormGeoTag(self, thingType, geoString, tag):
        c.tagList = getTagCategories()
        c.tag = tag
        c.geoScope = geoString
        c.geoString = geoInfoLib.getFullScope(geoString)
        log.info("I'm requesting to create a(n) %s", thingType)
        c.thingType = thingType
        return render('/derived/6_create.bootstrap')
    
    def createThing(self, id1):
        if id1 == "Initiative":
            self.createInitiative()
        
        elif id1 == "Workshop":
            self.createWorkshop()
            
        elif id1 == "Resource":
            #Do something with the necessary arguments here
            self.addResourceHandler()

        elif id1 == "Discussion":
            #Do something with the necessary arguments here
            self.addDiscussionHandler()

        elif id1 == "Idea":
            #Do something with the necessary arguments here
            self.addIdeaHandler()            

#################
# Workshops
#################
    
    def createWorkshop(self):
        log.info("In create workshop: I do nothing yet")
        if 'privacy' in request.params:
            if request.params['privacy'] == 'personal':
                wType = 'personal'
                scope = 'private'
        # added to make workshops free
            elif request.params['privacy'] == 'public':
                wType = 'professional'
                scope = 'public'
                c.stripeToken = "ADMINCOMP"
                c.billingName = c.authuser['name']
                c.billingEmail = "billing@civinomics.com"
                c.coupon = ''
            elif request.params['privacy'] == 'private':
                wType = 'professional'
                scope = 'private'
                c.stripeToken = "ADMINCOMP"
                c.billingName = c.authuser['name']
                c.billingEmail = "billing@civinomics.com"
                c.coupon = ''
            # end addition
        else:
            if self.validatePaymentForm():
                wType = 'professional'
            else:
                c.stripeKey = config['app_conf']['stripePublicKey'].strip()
                return render('/derived/6_workshop_payment.bootstrap')
                
        if 'title' in request.params:
            title = request.params['title']
        else:
            title = 'New Initiative'
            
        if 'description' in request.params:
            description = request.params['description']
            
        w = workshopLib.Workshop(title, c.authuser, scope, wType, description)
        
        if request.params['avatar[]'] is not u'':
            file = request.params['avatar[]']
            filename = file.filename
            fileitem = file.file
            s = self.saveSlide(c.authuser, "Main Image", filename, fileitem)
            mainImageLib.setMainImage(c.authuser, w, s)
            dbHelpers.commit(w)
            
        if request.params['privacy'] == 'public' and 'geoScope' in request.params:
            w['workshop_public_scope'] =  request.params['geoScope']
        else:
            w['workshop_public_scope'] = '0||united-states||0||0||0|0'
        c.workshop_id = w.id # TEST
        c.title = 'Configure Workshop'
        c.motd = motdLib.MOTD('Welcome to the workshop!', w.id, w.id)
        if wType == 'professional':
            account = accountLib.Account(c.billingName, c.billingEmail, c.stripeToken, w, 'PRO', c.coupon)
        alert = {'type':'success'}
        alert['title'] = 'Your new ' + scope + ' workshop is ready to be set up. Have fun!'
        session['alert'] = alert
        session.save()
        redirectUrl2 = "/home"
        redirectUrl = '/workshop/%s/%s/preferences'%(w['urlCode'], w['url'])
        return redirect(redirectUrl)
    
#################
# Initiatives
#################    
    
    def createInitiative(self):
#         log.info("In create initiative")
#         log.info("body")
#         log.info(request.body)
#         log.info("post")
#         log.info(vars(request.POST))
#         log.info("params")
#         log.info(vars(request.params))
#         log.info(c.authuser['urlCode'])
#         log.info(c.authuser['url'])
        
        requestKeys = request.params.keys()
        kwargs = {}
        query = request.POST
        log.info(query)
        
        if 'title' in query:
            title = query['title']
        else:
            title = 'New Initiative'
            
        if 'description' in query:
            description = query['description']
        else:
            description = ''

        if 'tags' in query:
            tags = query['tags']
            kwargs['tag'] = tags

        # the scope if initiative is created from a geoSearch page
        if 'geoScope' in query:
            scope = query['geoScope']
        else:
            scope = '0|0|united-states|0|0|0|0|0|0|0'
            
        goal = self.getInitiativeGoal(scope)

        c.thumbnail_url = "/images/icons/generalInitiative.jpg"
        c.bgPhoto_url = "'" + c.thumbnail_url + "'"
        
        #create the initiative
        c.initiative = initiativeLib.Initiative(c.user, title, description, scope, goal = goal, **kwargs)
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


        if 'avatar[]' in requestKeys and request.params['avatar[]'] is not u'':
            file = request.params['avatar[]']
            filename = file.filename
            fileitem = file.file
            photoAvatarInfo = self.photoUploadHandler(file)
            
        if 'cover[]' in requestKeys and request.params['cover[]'] is not u'':
            fileThing = request.params['cover[]']
            filename = fileThing.filename
            fileitem = fileThing.file
            log.info("Processing cover photo %s", fileThing.filename)
            photoCoverInfo = self.photoUploadHandler(fileThing, tipus = 'cover')
            
        
        c.editInitiative = True
        returnURL = '/initiative/%s/%s'%(c.initiative['urlCode'], c.initiative['url'])
        redirectUrl2 = "/"
        return redirect(returnURL)

#################
# Resources
# I have to edit this so it suits the current form.
#################

    @h.login_required
    def addResourceHandler(self):
        log.info(request.params)

        if c.w:
            parent = c.w
        elif c.initiative:
            parent = c.initiative
            userLib.setUserPrivs()
            c.w = None
        else:
            c.w = None
            parent = None
            userLib.setUserPrivs()
            
        payload = request.params
        if 'title' not in payload:
            return redirect(session['return_to'])
        title = payload['title'].strip()
        if title == '':
            return redirect(session['return_to'])
        if 'link' not in payload:
            return redirect(session['return_to'])
        
#       
#       if resourceLib.getResourceByLink(payload['link'], parent):
#             return redirect(session['return_to']) # Link already submitted
        link = payload['link']
        text = ''
        if 'description' in payload:
            text = payload['description'] # Optional
        if len(title) > 120:
            title = title[:120]
            
        if 'geoScope' in payload:
            log.info("it has a scope in create")
            scope = payload['geoScope']
        else:
            log.info("still has a scope")
            scope = '0|0|united-states|0|0|0|0|0|0|0'

        kwargs = {'geoScope' : scope}

        if 'tags' in payload:
            log.info(payload['tags'])
            tags = payload['tags']
            kwargs['tags'] = tags
			
		
        if c.w:
            newResource = resourceLib.Resource(link, title, c.authuser, c.w, c.privs, text = text)
        else:
            newResource = resourceLib.Resource(link, title, c.authuser, c.w, c.privs, text = text, parent = parent, **kwargs)
        if newResource:
            log.info("5")
            alertsLib.emailAlerts(newResource)
            redirectUrl = "/resource/" + newResource['urlCode'] +"/"+ newResource['url']
            redirectUrl2 = "/home"
            redirect(redirectUrl2)
        else:
            return '{"state":"Error", "errorMessage":"Resource not added!"}'
            
#################
# Discussions
# I have to edit this so it suits the current form.
#################           
            
    @h.login_required
    def addDiscussionHandler(self):

        # check throughout function if add comment was submited via traditional form or json
        # if through json, it's coming from an activity feed and we do NOT want to return redirect
        # return redirect breaks the success function on https
        if request.params:
            payload = request.params  
        elif json.loads(request.body):
            payload = json.loads(request.body)
        
        c.w = None
        
#         if not c.privs['participant'] and not c.privs['admin'] and not c.privs['facilitator']:
#             if request.params:
#                 return redirect(session['return_to'])
#             elif json.loads(request.body):
#                 return json.dumps({'statusCode':1})
       
        if 'title' in payload:
            title = payload['title']
        else: 
            title = False
        if 'description' in payload:
            text = payload['description']
        else:
            text = ''
            
        if 'geoScope' in payload:
            log.info("it has a scope in create")
            scope = payload['geoScope']
        else:
            log.info("still has a scope")
            scope = '0|0|united-states|0|0|0|0|0|0|0'
        kwargs = {'geoScope' : scope}
        
        if 'tags' in payload:
        	tags = payload['tags']
        	kwargs['tags'] = tags
        
        if not title or title=='':
            if request.params:
                return redirect(session['return_to'])
            elif json.loads(request.body):
                return json.dumps({'statusCode':1})
        else:
            if len(title) > 120:
                title = title[:120]
            
            d = discussionLib.Discussion(owner = c.authuser, discType = 'general',\
                title = title, text = text, privs = c.privs, role = None, **kwargs)
            alertsLib.emailAlerts(d.d)
            #commit(c.w)
        
        log.info(vars(d.d))
        if d:
            redirectUrl2 = "/home"
            redirectUrl = "/discussion/" + d.d['urlCode'] +"/"+ d.d['url']
            redirect(redirectUrl2)

#################
# Ideas
# I have to edit this so it suits the current form.
#################             

    @h.login_required
    def addIdeaHandler(self):
        # check to see if this is a request from the iphone app
        iPhoneApp = utils.iPhoneRequestTest(request)

        # check throughout function if add comment was submited via traditional form or json
        # if through json, it's coming from an activity feed and we do NOT want to return redirect
        # return redirect breaks the success function on https
        if request.params:
            payload = request.params  
        elif json.loads(request.body):
            payload = json.loads(request.body)
        
        log.info(payload)
        if 'title' not in payload:
            log.info("submit or title not in req params")
            if request.params:
                return redirect(session['return_to'])
            elif json.loads(request.body):
                return json.dumps({'statusCode':1})
        title = payload['title'].strip()
        if 'description' in payload:
            text = payload['description']
        else:
            text = ''
        if 'geoScope' in payload:
            log.info("it has a scope in create")
            scope = payload['geoScope']
        else:
            log.info("still has a scope")
            scope = '||united-states|0|0|0|0|0|0|0'
        
        kwargs = {'geoScope' : scope}
        
        if 'tags' in payload:
        	tags = payload['tags']
        	kwargs['tags'] = tags
        
        if title == '':
            log.info("title is blank")
            if request.params:
                return redirect(session['return_to'])
            elif json.loads(request.body):
                return json.dumps({'statusCode':1})
        if len(title) > 120:
            title = title[:120]
        newIdea = ideaLib.Idea(c.authuser, title, text, None, c.privs, **kwargs)
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
        if newIdea:
            log.info("5")
            redirectUrl2 = "/home"
            alertsLib.emailAlerts(newIdea)
            redirectUrl = "/idea/" + newIdea['urlCode'] +"/"+ newIdea['url']
            redirect(redirectUrl2)

    
#################
# Helper functions
#################

# Photo uploader

    @h.login_required
    def photoUploadHandler(self, photo, tipus = False):
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
        
        file = photo
        filename = file.filename
        file = file.file
        image = imageLib.openImage(file)
        if not image:
            abort(404) # Maybe make this a json response instead
        imageHash = imageLib.generateHash(filename, c.authuser)
        if not tipus:
            image = imageLib.saveImage(image, imageHash, 'photos', 'orig', thing = c.initiative)
        elif tipus == 'cover':
            image = imageLib.saveImage(image, imageHash, 'cover', 'orig', thing = c.initiative)
        elif tipus == 'slide':
            image = imageLib.saveImage(image, imageHash, 'cover', 'orig')
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
        if not tipus:
            image = imageLib.cropImage(image, imageHash, dims, clientWidth = clientWidth, clientHeight = clientHeight)
            image = imageLib.resizeImage(image, imageHash, 480, 480)
            image = imageLib.saveImage(image, imageHash, 'photos', 'photo')
            image = imageLib.resizeImage(image, imageHash, 160, 160)
            image = imageLib.saveImage(image, imageHash, 'photos', 'thumbnail')
            location = c.initiative['directoryNum_photos']
        elif tipus == 'slide':
            imageLocation, directoryNum = imageLib.getImageLocation(image)
            location = directoryNum
        elif tipus == 'cover':
            image = imageLib.cropImage(image, imageHash, dims, clientWidth = clientWidth, clientHeight = clientHeight)
            image = imageLib.resizeImage(image, imageHash, 480, 480)
            image = imageLib.saveImage(image, imageHash, 'photos', 'photo')
            image = imageLib.resizeImage(image, imageHash, 160, 160)
            image = imageLib.saveImage(image, imageHash, 'photos', 'thumbnail')
            location = c.initiative['directoryNum_photos']

        
        photoInfo ={
                    'name':filename,
                    'thumbnail_url':'/images/photos/%s/thumbnail/%s.png' %(location, imageHash),
                    'image_hash':imageHash
                   }
        return photoInfo


#Initiative goal (get number of votes required)

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

# Helper functions for workshops

    @h.login_required
    def validatePaymentForm(self):
        
        pError = 0
        pErrorMsg = ''
        
        if 'admin-submit-button' in request.params and c.privs['admin']:
            return True
        
        if 'name' in request.params and request.params['name'] != '':
            c.billingName = request.params['name']
        else:
            pError = 1
            pErrorMsg += 'Credit Card Name required. '
            
        if 'email' in request.params and request.params['email'] != '':
            c.billingEmail = request.params['email']
        else:
            pError = 1
            pErrorMsg += 'Billing email address required. '
            
        if 'stripeToken' in request.params and request.params['stripeToken'] != '':
            c.stripeToken = request.params['stripeToken']
        else:
            pError = 1
            pErrorMsg = 'Invalid credit card information.'

        c.coupon = ''
        if 'coupon' in request.params and request.params['coupon'] != '':
            if request.params['coupon'] == 'CIVCOMP100' or request.params['coupon'] == 'CIVCOMP99':
                c.coupon = request.params['coupon']
            
        if pError: 
            alert = {'type':'danger'}
            alert['title'] = 'Error.' + pErrorMsg
            session['alert'] = alert
            session.save()
            
            return False
            
        return True
        
# Save Slide without slideshow (this is...)
  
    def saveSlide(self, owner, title, filename, image):
        image = imageLib.openImage(image)
        if not image:
            abort(404)
        s = Thing('slide', owner.id)
        dbHelpers.commit(s)
        s['urlCode'] = utils.toBase62(s)
   
        imageHash = imageLib.generateHash(filename, s)
        image = imageLib.saveImage(image, imageHash, 'slide', 'orig', thing = s)
        image = imageLib.resizeImage(image, imageHash, 1200, 1200, preserveAspectRatio = True)
        image = imageLib.saveImage(image, imageHash, 'slide', 'slideshow')
        image = imageLib.resizeImage(image, imageHash, 128, 128, preserveAspectRatio = True)
        image = imageLib.saveImage(image, imageHash, 'slide', 'thumbnail')

        # finally
        s['pictureHash'] = imageHash
        s['title'] = title
        s['filename'] = filename
        s['deleted'] = u'0'
        s['disabled'] = u'0'
        s['format'] = u'png'
        dbHelpers.commit(s)
        return s
