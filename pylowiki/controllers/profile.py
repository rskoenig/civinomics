# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, config, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render
from pylowiki.lib.utils import urlify

import pylowiki.lib.helpers as h
from pylons import config

import pylowiki.lib.db.activity         as activityLib
import pylowiki.lib.db.geoInfo          as geoInfoLib
import pylowiki.lib.db.user             as userLib
import pylowiki.lib.db.dbHelpers        as dbHelpers
import pylowiki.lib.db.facilitator      as facilitatorLib
import pylowiki.lib.db.listener         as listenerLib
import pylowiki.lib.db.workshop         as workshopLib
import pylowiki.lib.db.pmember          as pMemberLib
import pylowiki.lib.db.follow           as followLib
import pylowiki.lib.db.event            as eventLib
import pylowiki.lib.db.flag             as flagLib
import pylowiki.lib.db.revision         as revisionLib
import pylowiki.lib.db.message          as messageLib
import pylowiki.lib.utils               as utils
import pylowiki.lib.images              as imageLib
import pylowiki.lib.db.photo               as photoLib

import time, datetime
import simplejson as json


log = logging.getLogger(__name__)

class ProfileController(BaseController):
    
    def __before__(self, action, id1 = None, id2 = None):
        if action not in ['hashPicture']:
            if id1 is not None and id2 is not None:
                c.user = userLib.getUserByCode(id1)
                if not c.user:
                    abort(404)
            else:
                abort(404)

            c.geoInfo = []
            gList = geoInfoLib.getGeoInfo(c.user.id)
            for g in gList:
                if g['disabled'] == '0':
                    c.geoInfo.append(g)
                
            c.isAdmin = False
            if 'user' in session:
                if userLib.isAdmin(c.authuser.id):
                    c.isAdmin = True
                if c.user.id == c.authuser.id or c.isAdmin:
                    c.messages = messageLib.getMessages(c.user)
                    c.unreadMessageCount = messageLib.getMessages(c.user, read = u'0', count = True)
                    
        c.scope = {'level':'earth', 'name':'all'}

    def showUserPage(self, id1, id2, id3 = ''):
        # Called when visiting /profile/urlCode/url
        rev = id3
        if id3 != '':
            c.revision = revisionLib.getRevisionByCode(id3)
        else:
            c.revision = False

        c.revisions = revisionLib.getParentRevisions(c.user.id)
        c.title = c.user['name']
               
        c.isFollowing = False
        c.isUser = False
        c.browse = False
        if 'user' in session:
            if c.authuser.id != c.user.id:
                c.isFollowing = followLib.isFollowing(c.authuser, c.user)
            else:
                c.isUser = True
            if userLib.isAdmin(c.authuser.id):
                c.isAdmin = True
        else:
            c.browse = True
            

        facilitatorList = facilitatorLib.getFacilitatorsByUser(c.user)
        c.facilitatorWorkshops = []
        c.pendingFacilitators = []
        for f in facilitatorList:
           if 'pending' in f and f['pending'] == '1':
              c.pendingFacilitators.append(f)
           elif f['disabled'] == '0':
              myW = workshopLib.getWorkshopByCode(f['workshopCode'])
              if not workshopLib.isPublished(myW) or myW['public_private'] != 'public':
                 # show to the workshop owner, show to the facilitator owner, show to admin
                 if 'user' in session: 
                     if c.authuser.id == f.owner or userLib.isAdmin(c.authuser.id):
                         c.facilitatorWorkshops.append(myW)
              else:
                    c.facilitatorWorkshops.append(myW)

        watching = followLib.getWorkshopFollows(c.user)
        watchList = [ workshopLib.getWorkshopByCode(followObj['workshopCode']) for followObj in watching ]
        c.watching = []
        for workshop in watchList:
            if workshop['public_private'] == 'public' or (c.isUser or c.isAdmin):
                c.watching.append(workshop)
                
        c.bookmarkedWorkshops = []
        for workshop in c.watching:
            if workshop['public_private'] == 'public':
                c.bookmarkedWorkshops.append(workshop)
            if workshop['public_private'] == 'private' and 'user' in session and c.authuser:
                if c.isUser or c.isAdmin:
                    c.bookmarkedWorkshops.append(workshop)
 
        interestedList = [workshop['urlCode'] for workshop in c.interestedWorkshops]
        
        listenerList = listenerLib.getListenersForUser(c.user, disabled = '0')
        c.pendingListeners = []
        c.listeningWorkshops = []
        for l in listenerList:
            lw = workshopLib.getWorkshopByCode(l['workshopCode'])
            c.listeningWorkshops.append(lw)
        
        c.privateWorkshops = []
        if 'user' in session and c.authuser:
            if c.user.id == c.authuser.id or userLib.isAdmin(c.authuser.id):
                privateList = pMemberLib.getPrivateMemberWorkshops(c.user, deleted = '0')
                if privateList:
                    c.privateWorkshops = [workshopLib.getWorkshopByCode(pMemberObj['workshopCode']) for pMemberObj in privateList]

        following = followLib.getUserFollows(c.user) # list of follow objects
        c.following = [userLib.getUserByCode(followObj['userCode']) for followObj in following] # list of user objects

        followers = followLib.getUserFollowers(c.user)
        c.followers = [ userLib.getUserByID(followObj.owner) for followObj in followers ]

        # this still needs to be optimized so we don't get the activity twice
        c.resources = []
        c.discussions = []
        c.comments = []
        c.ideas = []
        
        c.photos = photoLib.getUserPhotos(c.user)
        
        c.rawActivity = activityLib.getMemberActivity(c.user)
        
        for itemCode in c.rawActivity['itemList']:
            # ony active objects
            if c.rawActivity['items'][itemCode]['deleted'] == '0' and c.rawActivity['items'][itemCode]['disabled'] == '0':
                # only public objects unless author or admin
                workshopCode = c.rawActivity['items'][itemCode]['workshopCode']
                if c.rawActivity['workshops'][workshopCode]['deleted'] == '0' and c.rawActivity['workshops'][workshopCode]['published'] == '1' and c.rawActivity['workshops'][workshopCode]['public_private'] == 'public' or (c.isUser or c.isAdmin):
                    if c.rawActivity['items'][itemCode]['objType'] == 'resource':
                        c.resources.append(c.rawActivity['items'][itemCode])
                    elif c.rawActivity['items'][itemCode]['objType'] == 'discussion':
                        c.discussions.append(c.rawActivity['items'][itemCode])
                    elif c.rawActivity['items'][itemCode]['objType'] == 'idea':
                        c.ideas.append(c.rawActivity['items'][itemCode])
                    elif c.rawActivity['items'][itemCode]['objType'] == 'comment':
                        c.comments.append(c.rawActivity['items'][itemCode])

        return render("/derived/6_profile.bootstrap")

    def showUserMessages(self, id1, id2, id3 = ''):
        return render("/derived/6_messages.bootstrap")
    
    def showUserResources(self, id1, id2):
        # Called when visiting /profile/urlCode/url
        self._basicSetup(id1, id2, 'resources')
        return render("/derived/6_profile_list.bootstrap")
    
    def showUserDiscussions(self, id1, id2):
        # Called when visiting /profile/urlCode/url/discussions
        self._basicSetup(id1, id2, 'discussions')
        return render("/derived/6_profile_list.bootstrap")
    
    def showUserIdeas(self, id1, id2):
        # Called when visiting /profile/urlCode/url/ideas
        self._basicSetup(id1, id2, 'ideas')
        return render("/derived/6_profile_list.bootstrap")
    
    def showUserFollowers(self, id1, id2):
        # Called when visiting /profile/urlCode/url/followers
        self._basicSetup(id1, id2, 'followers')
        return render("/derived/6_profile_list.bootstrap")
    
    def showUserFollows(self, id1, id2):
        # Called when visiting /profile/urlCode/url/following
        self._basicSetup(id1, id2, 'following')
        return render("/derived/6_profile_list.bootstrap")
        
    def showUserWatching(self, id1, id2):
        # Called when visiting /profile/urlCode/url/watching
        self._basicSetup(id1, id2, 'watching')
        return render("/derived/6_profile_list.bootstrap")
    
    def _basicSetup(self, code, url, page):
        # code and url are now unused here, now that __before__ is defined
        c.title = c.user['name']
        c.geoInfo = geoInfoLib.getGeoInfo(c.user.id)
        c.isFollowing = False
        c.isUser = False
        c.isAdmin = False
        if 'user' in session and c.authuser:
           c.isFollowing = followLib.isFollowing(c.authuser, c.user)
        else:
           c.isFollowing = False
        
        items = self._userItems(c.user)
        c.listingType = page
        c.things = items[page]
        c.thingsTitle = page.title()
        
        c.discussions = items['discussions']
        c.resources = items['resources']
        c.ideas = items['ideas']
        c.followers = items['followers']
        c.following = items['following']
        c.watching = items['watching']
    
    def _userItems(self, user):
        isUser = False
        isAdmin = False
        if 'user' in session and c.authuser:
            if user.id == c.authuser.id:
               isUser = True
            if userLib.isAdmin(c.authuser.id):
               isAdmin = True

        # returns a dictionary of user-created (e.g. resources, discussions, ideas)
        # or user-interested (e.g. followers, following, watching) objects
        items = {}
        
        following = followLib.getUserFollows(c.user) # list of follow objects
        items['following'] = [userLib.getUserByCode(followObj['userCode']) for followObj in following] # list of user objects

        followers = followLib.getUserFollowers(c.user)
        items['followers'] = [ userLib.getUserByID(followObj.owner) for followObj in followers ]
        
        watching = followLib.getWorkshopFollows(user)
        watchList = [ workshopLib.getWorkshopByCode(followObj['workshopCode']) for followObj in watching ]
        items['watching'] = []
        for workshop in watchList:
            if workshop['public_private'] == 'public' or (isUser or isAdmin):
                items['watching'].append(workshop)
        
        # Already checks for disabled/deleted by default
        # The following section feels like a good candidate for map/reduce
        createdThings = userLib.getUserPosts(user)
        items['resources'] = []
        items['discussions'] = []
        items['ideas'] = []
        items['searchWorkshops'] = []
        items['searchUsers'] = []
        for thing in createdThings:
            if 'workshopCode' in thing:
                w = workshopLib.getWorkshopByCode(thing['workshopCode'])
                if workshopLib.isPublished(w) or isAdmin:
                    if w['public_private'] == 'public' and thing['disabled'] != '1' and thing['deleted'] != '1' or (isUser or isAdmin):
                        if thing.objType == 'resource':
                            items['resources'].append(thing)
                        elif thing.objType == 'discussion':
                            items['discussions'].append(thing)
                        elif thing.objType == 'idea':
                            items['ideas'].append(thing)

        return items

    @h.login_required
    def edit(self, id1, id2):
        c.events = eventLib.getParentEvents(c.user)
        if userLib.isAdmin(c.authuser.id) or c.user.id == c.authuser.id:
            c.title = 'Edit Profile'
            if 'confTab' in session:
                c.tab = session['confTab']
                session.pop('confTab')
                session.save()
            if userLib.isAdmin(c.authuser.id):
                c.admin = True
            else:
                c.admin = False
            c.pendingFacilitators = []
            fList = facilitatorLib.getFacilitatorsByUser(c.user)
            for f in fList:
                if 'pending' in f and f['pending'] == '1':
                    c.pendingFacilitators.append(f)

            listenerList = listenerLib.getListenersForUser(c.user, disabled = '0')
            c.pendingListeners = []
            for l in listenerList:
                if 'pending' in l and l['pending'] == '1':
                    c.pendingListeners.append(l)
                    
            return render('/derived/6_profile.bootstrap')
        else:
            abort(404)

    @h.login_required
    def infoEditHandler(self,id1, id2):
        perror = 0
        perrorMsg = ""
        changeMsg = ""
        nameChange = False
        postalChange = False
        anyChange = False
        name = False
        email = False
        postalCode = False
        picture = False
        greetingMsg = False
        websiteLink = False
        websiteDesc = False
        
        now = datetime.datetime.now()
        SQLtoday = now.strftime("%Y-%m-%d")

        # make sure they are authorized to do this
        if c.user.id != c.authuser.id and userLib.isAdmin(c.authuser.id) != 1:
            abort(404)
            
        session['confTab'] = "tab1"
        session.save()
        
        payload = json.loads(request.body)
        if 'member_name' in payload:
            name = payload['member_name']
            if name == '':
               name = False
        if not name:
            perror = 1
            perrorMsg = perrorMsg + ' Member name required.'

        if 'email' in payload:
            email = payload['email']
            if email == '':
                email = False
            elif email != c.user['email']:
                checkUser = userLib.getUserByEmail(email)
                if checkUser:
                    perror = 1
                    perrorMsg = perrorMsg + ' Email address ' + email + ' is already in use by other member!'
                    email = c.user['email']
        if not email:
            perror = 1
            perrorMsg = perrorMsg + ' Email required.'
        
        if 'postalCode' in payload:
            postalCode = payload['postalCode']
            if postalCode == '':
                postalCode = False
            elif postalCode != c.user['postalCode']:
                # first, make sure it is valid
                checkPostal = geoInfoLib.getPostalInfo(postalCode)
                if checkPostal == None:
                    log.info("Error: Bad Postal Code in profile edit")
                    perror = 1
                    perrorMsg = perrorMsg + ' No such postal code: ' + postalCode
                    postalCode = c.user['postalCode']
        if not postalCode:
            perror = 1
            perrorMsg = perrorMsg + ' Postal code required.'

        if 'greetingMsg' in payload:
            greetingMsg = payload['greetingMsg']


        if 'websiteLink' in payload:
            websiteLink = payload['websiteLink']

        if 'websiteDesc' in payload:
            websiteDesc = payload['websiteDesc']

        if name and name != '' and name != c.user['name']:
            c.user['name'] = name
            nameChange = True
            anyChange = True
            changeMsg = changeMsg + "Member name updated. "
        if email and email != '' and email != c.user['email']:
            c.user['email'] = email
            anyChange = True
            changeMsg = changeMsg + "Member email updated. "
        if postalCode and postalCode != '' and postalCode != c.user['postalCode']:
            c.user['postalCode'] = postalCode
            anyChange = True
            changeMsg = changeMsg + "Postal code updated. "
            # get the previous geo scope info
            gList = geoInfoLib.getGeoInfo(c.user.id)
            # deactivate and disable any existing geocodes
            for g in gList:
                if g['disabled'] == u'0':
                    g['disabled'] = u'1'
                    g['deactivated'] = SQLtoday
                    dbHelpers.commit(g)
                    
            # make a new one
            g = geoInfoLib.GeoInfo(postalCode, 'United States', c.user.id)
            c.geoInfo = []
            c.geoInfo.append(g)
            postalChange = True
            
        if greetingMsg and greetingMsg != '' and greetingMsg != c.user['greetingMsg']:
            c.user['greetingMsg'] = greetingMsg
            anyChange = True
            changeMsg = changeMsg + "Greeting message updated. "
        if websiteLink and websiteLink != '' and websiteLink != c.user['websiteLink']:
            anyChange = True
            changeMsg = changeMsg + "Website link updated. "
            if not websiteLink.startswith('http://'):
                websiteLink = u'http://' + websiteLink
            c.user['websiteLink'] = websiteLink
        if websiteDesc and websiteDesc != ''and websiteDesc != c.user['websiteDesc']:
            anyChange = True
            changeMsg = changeMsg + "Website description updated. "
            c.user['websiteDesc'] = websiteDesc

        if nameChange:
            c.user['url'] = urlify(c.user['name'])
            if c.user.id == c.authuser.id:
                session["userURL"] = c.user['url']
                session.save()
                c.authuser = c.user
            log.info('Changed name')
            
        returnURL = "/profile/" + c.user['urlCode'] + "/" + c.user['url']
        if anyChange and perror == 0:
            dbHelpers.commit(c.user)
            eventLib.Event('Profile updated.', changeMsg, c.user, c.authuser)
            revisionLib.Revision(c.authuser, c.user)
            if postalChange:
                statusCode = 2
            else:
                statusCode = 0
            return json.dumps({'statusCode':statusCode, 'result':changeMsg, 'returnURL':returnURL})

        elif perror == 1:
            return json.dumps({'statusCode':'1', 'result':perrorMsg, 'returnURL':returnURL})
        else:
            return json.dumps({'statusCode':'1', 'result':'No changes submitted.'})

    @h.login_required
    def pictureUploadHandler(self, id1, id2):
        """
            Ideally:  
            1) User selects image, gets presented with aspect-ratio constrained selection.
            2) User adjusts centering and dimensions, hits 'start'
            3) Process image - detailed below
        
            Grab the uploaded file.  Hash and save the original first.  Then process.
            Processing means:
            1) Check to ensure it is an image (should be done in the hash + save step)
            2) Check for square dimensions.  If not square, crop.  Do not save the image here, just pass on the image object.
            3) If necessary, resize the dimensions of the image to 200px x 200px.  Save the final image here.
            
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
        
        requestKeys = request.params.keys()
        if 'files[]' in requestKeys:
            file = request.params['files[]']
            filename = file.filename
            file = file.file
            image = imageLib.openImage(file)
            if not image:
                abort(404) # Maybe make this a json response instead
            imageHash = imageLib.generateHash(filename, c.authuser)
            image = imageLib.saveImage(image, imageHash, 'avatar', 'orig', thing = c.authuser)
            
            width = min(image.size)
            x = 0
            y = 0
            if 'width' in requestKeys:
                width = int(request.params['width'])
            if 'x' in requestKeys:
                x = int(request.params['x'])
            if 'y' in requestKeys:
                y = int(request.params['y'])
            dims = {'x': x, 
                    'y': y, 
                    'width':width,
                    'height':width}
            clientWidth = -1
            clientHeight = -1
            if 'clientWidth' in requestKeys:
                clientWidth = request.params['clientWidth']
            if 'clientHeight' in requestKeys:
                clientHeight = request.params['clientHeight']
            image = imageLib.cropImage(image, imageHash, dims, clientWidth = clientWidth, clientHeight = clientHeight)
            image = imageLib.resizeImage(image, imageHash, 200, 200)
            image = imageLib.saveImage(image, imageHash, 'avatar', 'avatar')
            image = imageLib.resizeImage(image, imageHash, 100, 100)
            image = imageLib.saveImage(image, imageHash, 'avatar', 'thumbnail')
            
            jsonResponse =  {'files': [
                                {
                                    'name':filename,
                                    'thumbnail_url':'/images/avatar/%s/avatar/%s.png' %(c.authuser['directoryNum_avatar'], imageHash)
                                }
                            ]}
            return json.dumps(jsonResponse)
        else:
            abort(404)
        
    @h.login_required
    def setImageSource(self, id1, id2):
        try:
            payload = json.loads(request.body)
            source = payload['source']
        except:
            log.error("User %s tried to set a profile image source for user %s with an unknown source.  Body was %s." %(c.authuser.id, c.user.id, request.body))
            return json.dumps({"statusCode": 1})
        c.user['avatarSource'] = source
        dbHelpers.commit(c.user)
        return json.dumps({"statusCode": 0})
        
    @h.login_required
    def preferencesCommentsHandler(self, id1, id2):
        # initialize to current value if any, '0' if not set in object
        cAlerts = '0'
        eAction = ''
        if 'itemAlerts' in c.user:
            cAlerts = c.user['commentAlerts']
        
        payload = json.loads(request.body)
        if 'alert' not in payload:
            return "Error"
        alert = payload['alert']
        if alert == 'comments':
            if 'commentAlerts' in c.user.keys():
                if c.user['commentAlerts'] == u'1':
                    c.user['commentAlerts'] = u'0'
                    eAction = 'Turned off'
                else:
                    c.user['commentAlerts'] = u'1'
                    eAction = 'Turned on'
            else:
                c.user['commentAlerts'] = u'1'
                eAction = 'Turned on'
        else:
            return "Error"   
        dbHelpers.commit(c.user)
        if eAction != '':
            eventLib.Event('Member comment notifications set', eAction, c.user, c.authuser)
        return eAction      
  
    @h.login_required
    def passwordUpdateHandler(self, id1, id2):
        perror = 0
        perrorMsg = ""
        changeMsg = ""
        # make sure they are authorized to do this
        if c.user.id != c.authuser.id and userLib.isAdmin(c.authuser.id) != 1:
            abort(404)      
                    
        session['confTab'] = "tab4"
        session.save()
            
        
        if 'password' in request.params:
            password = request.params['password']

        else:
            password = False 
        if 'verify_password' in request.params:
            verify_password = request.params['verify_password']
        else:
            verify_password = False 

        if password and verify_password and password == verify_password:
            userLib.changePassword(c.user, password)
            changeMsg = changeMsg + "Password updated. "
        if password and verify_password and password != verify_password:
            perror = 1
            perrorMsg = 'Password and Verify Password must match'
        if password or verify_password and password != verify_password:
            perror = 1
            perrorMsg = 'Password and Verify Password must match'

        " FOR CHANGING USE PASSWORD"
        pass_error = 4
        if 'oldPassword' in request.params:
            old_password = userLib.checkPassword(c.authuser, request.params['oldPassword'])
            pass_error = 0
            
            if not old_password:
                pass_error = 2
            if request.params['oldPassword'] == '':
                pass_error = 4
                
        if 'newPassword' in request.params:
            newPassword = request.params['newPassword']
        else:
            pass_error = 1
        if 'reNewPassword' in request.params:
            reNewPassword = request.params['reNewPassword']
        else:
            pass_error = 1
            
        if newPassword == '' or reNewPassword == '' or request.params['oldPassword'] == '':
            pass_error = 1
        elif newPassword != reNewPassword:
            pass_error = 3
                        
        if 'oldPassword' not in request.params and 'newPassword' not in request.params and 'reNewPassword' not in request.params:
            pass_error = 4
        else:
            if request.params['oldPassword'] == '' and request.params['newPassword'] == '' and request.params['reNewPassword'] == '':
                pass_error = 4
            
        if pass_error == 0:
            userLib.changePassword(c.user, newPassword)
            eventLib.Event('Profile updated.', 'Password changed', c.user, c.authuser)
            log.info('changed password for  %s'%c.authuser['name'])
            alert = {'type':'success'}
            alert['title'] = 'Password Change Successful'
            alert['content'] = ''
            session['alert'] = alert
            session.save()
        elif pass_error == 1:
            alert = {'type':'error'}
            alert['title'] = 'Password Change: All Fields Required'
            alert['content'] = ''
            session['alert'] = alert
            session.save()
        elif pass_error == 2:
            alert = {'type':'error'}
            alert['title'] = 'Password Change: Old Password Incorrect'
            alert['content'] = ''
            session['alert'] = alert
            session.save()
        elif pass_error == 3:
            alert = {'type':'error'}
            alert['title'] = 'Password Change: New Passwords Do Not Match'
            alert['content'] = ''
            session['alert'] = alert
            session.save()
            
        returnURL = "/profile/" + c.user['urlCode'] + "/" + c.user['url']
                
        return redirect(returnURL)

    @h.login_required
    def enableHandler(self, id1, id2):
        if not userLib.isAdmin(c.authuser.id):
            abort(404)

        session['confTab'] = "tab5"
        session.save()
        
        if 'verifyEnableUser' in request.params and 'enableUserReason' in request.params and len(request.params['enableUserReason']) > 0:
           log.info('disabled is %s' % c.user['disabled'])
           enableUserReason = request.params['enableUserReason']

           if c.user['disabled'] == '1':
              c.user['disabled'] = '0'
              eAction = 'User Enabled'
              alert = {'type':'success'}
              alert['title'] = 'Enabled:'
              alert['content'] = 'Member Enabled'
           else:
              c.user['disabled'] = '1'
              eAction = 'User Disabled'
              alert = {'type':'warning'}
              alert['title'] = 'Disabled:'
              alert['content'] = 'Member Disabled'
              
           e = eventLib.Event(eAction, enableUserReason, c.user, c.authuser)
           dbHelpers.commit(c.user)
           session['alert'] = alert
           session.save()
        else:
           alert = {'type':'error'}
           alert['title'] = 'Error:'
           alert['content'] = 'Enter reason and verify action before submit'
           session['alert'] = alert
           session.save()

        return redirect("/profile/" + id1 + "/" + id2 + "/edit" )

    @h.login_required
    def privsHandler(self, id1, id2):
        if not userLib.isAdmin(c.authuser.id):
            abort(404)
            
        session['confTab'] = "tab5"
        session.save()
        if 'accessChangeReason' in request.params and request.params['accessChangeReason'] != '' and 'accessChangeVerify' in request.params:
            if c.user['accessLevel'] == '0':
                newAccessTitle = "Admin"
                newAccess = "200"
                oldAccessTitle = "User"
            else:
                newAccessTitle = "User"
                newAccess = "0"
                oldAccessTitle = "Admin"
                
            eAction = 'Access Level Changed from ' + oldAccessTitle + ' to ' + newAccessTitle
            c.user['accessLevel'] = '200'
            accessChangeReason = request.params['accessChangeReason']
            e = eventLib.Event(eAction, accessChangeReason, c.user, c.authuser)
            dbHelpers.commit(c.user)
            alert = {'type':'success'}
            alert['title'] = 'Success:'
            alert['content'] = 'New Access Level Set'
            session['alert'] = alert
            session.save()
        else:
            alert = {'type':'error'}
            alert['title'] = 'Error:'
            alert['content'] = 'Enter reason and specify a new access level'
            session['alert'] = alert
            session.save()

        return redirect("/profile/" + id1 + "/" + id2 + "/edit" )


