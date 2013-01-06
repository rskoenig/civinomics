# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render
from pylowiki.lib.utils import urlify

import webhelpers.paginate as paginate
import pylowiki.lib.helpers as h
from pylons import config

import pylowiki.lib.images              as imageLib
import pylowiki.lib.db.activity         as activityLib
import pylowiki.lib.db.imageIdentifier  as imageIdentifierLib
import pylowiki.lib.db.geoInfo          as geoInfoLib
import pylowiki.lib.db.user             as userLib
import pylowiki.lib.db.dbHelpers        as dbHelpers
import pylowiki.lib.db.facilitator      as facilitatorLib
import pylowiki.lib.db.workshop         as workshopLib
import pylowiki.lib.db.pmember          as pMemberLib
import pylowiki.lib.db.follow           as followLib
import pylowiki.lib.db.event            as eventLib
import pylowiki.lib.db.flag             as flagLib
import pylowiki.lib.db.revision         as revisionLib
import simplejson as json
import csv
import os

from hashlib import md5

log = logging.getLogger(__name__)

class ProfileController(BaseController):
    
    def __before__(self, action, id1 = None, id2 = None):
        if action != 'hashPicture':
            if id1 is not None and id2 is not None:
                c.user = userLib.get_user(id1, id2)
            else:
                abort(404)
    
    def showUserPage(self, id1, id2, id3 = ''):
        # Called when visiting /profile/urlCode/url
        rev = id3
        if id3 != '':
            c.revision = revisionLib.getRevisionByCode(id3)
        else:
            c.revision = False

        c.revisions = revisionLib.getParentRevisions(c.user.id)
        c.title = c.user['name']
        c.geoInfo = geoInfoLib.getGeoInfo(c.user.id)
        c.isFollowing = False
        if 'user' in session and c.authuser.id != c.user.id:
           c.isFollowing = followLib.isFollowing(c.authuser, c.user) 

        fList = facilitatorLib.getFacilitatorsByUser(c.user.id)
        c.facilitatorWorkshops = []
        c.pendingFacilitators = []
        for f in fList:
           if 'pending' in f and f['pending'] == '1':
              c.pendingFacilitators.append(f)
           elif f['disabled'] == '0':
              wID = f['workshopID']
              myW = workshopLib.getWorkshopByID(wID)
              if myW['startTime'] == '0000-00-00' or myW['deleted'] == '1' or myW['public_private'] != 'public':
                 # show to the workshop owner, show to the facilitator owner, show to admin
                 if 'user' in session: 
                     if c.authuser.id == f.owner or userLib.isAdmin(c.authuser.id):
                         c.facilitatorWorkshops.append(myW)
              else:
                    c.facilitatorWorkshops.append(myW)

        c.watching = followLib.getWorkshopFollows(c.user)

        uList = followLib.getUserFollows(c.user)
        c.following = []
        for u in uList:
           uID = u['thingID']
           c.following.append(userLib.getUserByID(uID))

        uList = followLib.getUserFollowers(c.user)
        c.followers = []
        for u in uList:
           uID = u.owner
           c.followers.append(userLib.getUserByID(uID))
          
        c.activity = activityLib.getMemberPosts(c.user)
        c.suggestions = []
        c.resources = []
        c.discussions = []
        c.comments = []
        c.ideas = []
        
        posts = activityLib.getMemberPosts(c.user)
        for p in posts:
            if p['deleted'] == '0' and p['disabled'] == '0':
                if p.objType == 'suggestion':
                    c.suggestions.append(p)
                elif p.objType == 'resource':
                    c.resources.append(p)
                elif p.objType == 'discussion':
                    c.discussions.append(p)
                elif p.objType == 'idea':
                    c.ideas.append(p)
                elif p.objType == 'comment':
                    c.comments.append(p)
        
        return render("/derived/6_profile.bootstrap")
    
    def stats(self, id1, id2):
        if 'user' in session and (user.id == c.authuser.id or userLib.isAdmin(c.authuser.id)):
            posts = activityLib.getMemberPosts(user, 0)
        else:
            posts = activityLib.getMemberPosts(user, 1)
        
        types = ['discussion', 'comment', 'resource']
        counts = {}
        for item in types:
            counts[item] = len([post for post in posts if post.objType == item])
        retObj = {}
        retObj['titles'] = types
        retObj['values'] = [counts[key] for key in types] # Key off of types to preserve order
        return json.dumps(retObj)
    
    def statsCSV(self, id1, id2):
        if 'user' in session and (user.id == c.authuser.id or userLib.isAdmin(c.authuser.id)):
            posts = activityLib.getMemberPosts(user, 0)
        else:
            posts = activityLib.getMemberPosts(user, 1)
        
        headers = ['objType', 'time']
        data = []
        counts = {}
        for post in posts:
            data.append([post.objType, post.date])
            if post.objType not in counts:
                counts[post.objType] = 1
            else:
                counts[post.objType] += 1
                
        for key in counts.keys():
            log.info(key)
            log.info(counts[key])
            
        response.content_type = 'text/csv'
        writer = csv.writer(response)
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)
        return response
    
    def showUserSuggestions(self, id1, id2):
        # Called when visiting /profile/urlCode/url/suggestions
        c.title = c.user['name']
        c.geoInfo = geoInfoLib.getGeoInfo(c.user.id)
        c.isFollowing = False
        if 'user' in session and c.authuser:
           c.isFollowing = followLib.isFollowing(c.authuser, c.user) 
        else:
           c.isFollowing = False

        pList = userLib.getUserPosts(c.user)
        c.totalPoints = 0
        c.suggestions = []
        c.userFollowers = []
        c.flags = 0

        uList = followLib.getUserFollowers(c.user)
        c.userFollowers = []
        for u in uList:
           uID = u.owner
           c.userFollowers.append(userLib.getUserByID(uID))


        c.posts = len(pList)
        for p in pList:
           if p['deleted'] == '0' and p['disabled'] == '0':
               if p.objType == 'suggestion':
                   c.suggestions.append(p)

           fList = flagLib.getFlags(p)
           if fList:
              c.flags += len(fList)

        if c.suggestions and len(c.suggestions) > 0:
            totalRateAvg = 0
            for s in c.suggestions:
                totalRateAvg += float(s['ratingAvg_overall'])

            totalRateAvg = totalRateAvg/len(c.suggestions)
            c.sugRateAvg = int(totalRateAvg)
            c.sugUpperRateAvg = totalRateAvg+(5-totalRateAvg%5)
            c.sugLowerRateAvg = totalRateAvg-(totalRateAvg%5)
            c.sugRateAvgfuzz = c.sugLowerRateAvg+2.5
        else:
            totalRateAvg = 0
            c.sugRateAvg = totalRateAvg
            c.sugUpperRateAvg = 0
            c.sugLowerRateAvg = 0
            c.sugRateAvgfuzz = 0

        c.count = len(c.suggestions)
        c.paginator = paginate.Page(
            c.suggestions, page=int(request.params.get('page', 1)),
            items_per_page = 25, item_count = c.count
        )

        return render("/derived/profileSuggestions.bootstrap")

    def showUserResources(self, id1, id2):
        # Called when visiting /profile/urlCode/url
        self._basicSetup(id1, id2, 'resources')
        return render("/derived/6_profile_list.bootstrap")
    
    def showUserDiscussions(self, id1, id2):
        # Called when visiting /profile/urlCode/url/discussions
        self._basicSetup(id1, id2, 'discussions')
        return render("/derived/6_profile_list.bootstrap")
    
    def showUserComments(self, id1, id2):
        # Called when visiting /profile/urlCode/url/comments
        c.title = c.user['name']
        c.geoInfo = geoInfoLib.getGeoInfo(c.user.id)
        c.isFollowing = False
        if 'user' in session and c.authuser:
           c.isFollowing = followLib.isFollowing(c.authuser, c.user) 
        else:
           c.isFollowing = False

        uList = followLib.getUserFollows(c.user)
        c.followingUsers = []
        for u in uList:
           uID = u['thingID']
           c.followingUsers.append(userLib.getUserByID(uID))

        uList = followLib.getUserFollowers(c.user)
        c.userFollowers = []
        for u in uList:
           uID = u.owner
           c.userFollowers.append(userLib.getUserByID(uID))

        pList = userLib.getUserPosts(c.user)
        c.totalPoints = 0
        c.comments = []
        c.flags = 0
        comUpVotes = 0
        c.comVotes = 0

        c.posts = len(pList)
        for p in pList:
           if p['deleted'] == '0' and p['disabled'] == '0':
               if p.objType == 'comment':
                   c.comments.append(p)
                   comUpVotes += int(p['ups'])
                   c.comVotes = c.comVotes + int(p['ups']) + int(p['downs'])

           fList = flagLib.getFlags(p)
           if fList:
              c.flags += len(fList)
           if 'ups' in p and 'downs' in p:
               t = int(p['ups']) - int(p['downs'])
               c.totalPoints += t 

        c.numComs = len(c.comments)
        if c.comVotes > 0:
            c.comUpsPercent = 100*float(comUpVotes)/float(c.comVotes)
        else:
            c.comUpsPercent = 0

        c.count = len(c.comments)
        c.paginator = paginate.Page(
            c.comments, page=int(request.params.get('page', 1)),
            items_per_page = 25, item_count = c.count
        )

        return render("/derived/profileComments.bootstrap")
    
    def showUserFollowers(self, id1, id2):
        # Called when visiting /profile/urlCode/url/followers
        self._basicSetup(id1, id2, 'followers')
        return render("/derived/6_profile_list.bootstrap")
    
    def showUserFollows(self, id1, id2):
        # Called when visiting /profile/urlCode/url/following
        self._basicSetup(id1, id2, 'following')
        return render("/derived/6_profile_list.bootstrap")
    
    def _basicSetup(self, code, url, page):
        # code and url are now unused here, now that __before__ is defined
        c.title = c.user['name']
        c.geoInfo = geoInfoLib.getGeoInfo(c.user.id)
        c.isFollowing = False
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
        # returns a dictionary of user-created (e.g. resources, discussions, ideas)
        # or user-interested (e.g. followers, following, watching) objects
        items = {}
        
        following = followLib.getUserFollows(user)
        items['following'] = []
        for item in following:
            items['following'].append(userLib.getUserByID(item['thingID']))
        
        followers = followLib.getUserFollowers(user)
        items['followers'] = []
        for item in followers:
            items['followers'].append(userLib.getUserByID(item.owner))
            
        watching = followLib.getWorkshopFollows(user)
        items['watching'] = []
        for item in watching:
            items['watching'].append(workshopLib.getWorkshopByID(item['thingID']))
        
        # Already checks for disabled/deleted by default
        # The following section feels like a good candidate for map/reduce
        createdThings = userLib.getUserPosts(user)
        items['resources'] = []
        items['discussions'] = []
        items['ideas'] = [] # TODO
        for thing in createdThings:
            if thing.objType == 'resource':
                items['resources'].append(thing)
            elif thing.objType == 'discussion':
                items['discussions'].append(thing)
        
        return items
    
    @h.login_required
    def index( self ):
        abort(404)
        c.list = get_all_users()

        c.count = len( c.list )
        c.paginator = paginate.Page(
            c.list, page=int(request.params.get('page', 1)),
            items_per_page = 25, item_count = c.count
        )
        c.title = c.heading = "User Accounts"
        return render( "/derived/AccountList.mako" )

    @h.login_required
    def dashboard(self, id1, id2):
        c.events = eventLib.getParentEvents(c.user)
        if userLib.isAdmin(c.authuser.id) or c.user.id == c.authuser.id:
            c.title = 'Member Dashboard'
            if 'confTab' in session:
                c.tab = session['confTab']
                session.pop('confTab')
                session.save()
            if userLib.isAdmin(c.authuser.id):
                c.admin = True
            else:
                c.admin = False
            c.pendingFacilitators = []
            fList = facilitatorLib.getFacilitatorsByUser(c.user.id)
            for f in fList:
                if 'pending' in f and f['pending'] == '1':
                    c.pendingFacilitators.append(f)

            return render('/derived/6_profile_dashboard.bootstrap')
        else:
            abort(404)

    @h.login_required
    def editHandler(self,id1, id2):
        perror = 0
        perrorMsg = ""
        changeMsg = ""
        nameChange = False
        anyChange = False
        name = False
        email = False
        picture = False
        greetingMsg = False
        websiteLink = False
        websiteDesc = False

        # make sure they are authorized to do this
        if c.user.id != c.authuser.id and userLib.isAdmin(c.authuser.id) != 1:
            abort(404)
            
        session['confTab'] = "tab1"
        session.save()

        if 'member_name' in request.params:
            name = request.params['member_name']
            if name == '':
               name = False
        if not name:
            perror = 1
            perrorMsg = perrorMsg + ' Member name required.'

        if 'email' in request.params:
            email = request.params['email']
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

        if 'greetingMsg' in request.params:
            greetingMsg = request.params['greetingMsg']


        if 'websiteLink' in request.params:
            websiteLink = request.params['websiteLink']

        if 'websiteDesc' in request.params:
            websiteDesc = request.params['websiteDesc']

        if name and name != '' and name != c.user['name']:
            c.user['name'] = name
            nameChange = True
            anyChange = True
            changeMsg = changeMsg + "Member name updated. "
        if email and email != '' and email != c.user['email']:
            c.user['email'] = email
            anyChange = True
            changeMsg = changeMsg + "Member email updated. "
        if greetingMsg and greetingMsg != '' and greetingMsg != c.user['greetingMsg']:
            c.user['greetingMsg'] = greetingMsg
            anyChange = True
            changeMsg = changeMsg + "Greeting message updated. "
        if websiteLink and websiteLink != '' and websiteLink != c.user['websiteLink']:
            anyChange = True
            changeMsg = changeMsg + "Website link updated. "
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
        if anyChange and perror == 0:
            dbHelpers.commit(c.user)
            eventLib.Event('Profile updated.', changeMsg, c.user, c.authuser)
            revisionLib.Revision(c.user, c.user['name'], c.user)
            alert = {'type':'success'}
            alert['title'] = changeMsg
            alert['content'] = ''
            session['alert'] = alert
            session.save()

        elif perror == 1:
            alert = {'type':'error'}
            alert['title'] = perrorMsg 
            alert['content'] = ''
            session['alert'] = alert
            session.save()

        else:
            if 'alert' not in session:
                alert = {'type':'error'}
                alert['title'] = 'No changes submitted.'
                alert['content'] = ''
                session['alert'] = alert
                session.save()
                
        returnURL = "/profile/" + c.user['urlCode'] + "/" + c.user['url'] + "/dashboard"
                
        return redirect(returnURL)
        
    @h.login_required
    def passwordHandler(self, id1, id2):
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
            
        returnURL = "/profile/" + c.user['urlCode'] + "/" + c.user['url'] + "/dashboard"
                
        return redirect(returnURL)
    
    def hashPicture(self, username, title):
        return md5(username + title).hexdigest()
        
    @h.login_required
    def pictureHandler(self, id1, id2):
        session['confTab'] = "tab2"
        session.save()
        
        if 'pictureFile' in request.params:
            file = request.params['pictureFile']
            imageFile = file.file
            filename = file.filename
            identifier = 'avatar'
            hash = imageLib.saveImage(imageFile, filename, c.user, 'avatar', c.user)
            c.user['pictureHash'] = hash
            imageLib.resizeImage(identifier, hash, 200, 200, 'profile')
            imageLib.resizeImage(identifier, hash, 25, 25, 'thumbnail')
            
            alert = {'type':'success'}
            alert['title'] = 'Upload complete. Profile picture updated.'
            alert['content'] = ''
            session['alert'] = alert
            session.save()

            i = imageIdentifierLib.getImageIdentifier(identifier)
            directoryNumber = str(int(i['numImages']) / imageLib.numImagesInDirectory)
            savename = hash + '.orig'
            newPath = os.path.join(config['app_conf']['imageDirectory'], identifier, directoryNumber, 'orig', savename)
            st = os.stat(newPath)
            l = []
            d = {}
            d['name'] = savename
            d['size'] = st.st_size
            if 'site_base_url' in config:
                siteURL = config['site_base_url']
            else:
                siteURL = 'http://www.civinomics.com'
            
            d['url'] = '%s/images/%s/%s/orig/%s.orig' % (siteURL, identifier, directoryNumber, hash)
            d['thumbnail_url'] = '%s/images/%s/%s/thumbnail/%s.thumbnail' % (siteURL, identifier, directoryNumber, hash)
            d['delete_url'] = ''
            d['delete_type'] = "DELETE"
            d['-'] = hash
            d['type'] = 'image/png'
            l.append(d)

            return json.dumps(l)

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

        return redirect("/profile/" + id1 + "/" + id2 + "/dashboard" )

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

        return redirect("/profile/" + id1 + "/" + id2 + "/dashboard" )


