# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render
from pylowiki.lib.utils import urlify

import webhelpers.paginate as paginate
import pylowiki.lib.helpers as h
from pylons import config

from pylowiki.lib.images import saveImage, resizeImage
from pylowiki.lib.db.geoInfo import GeoInfo, getGeoInfo
from pylowiki.lib.db.user import get_user, getUserByID, isAdmin, changePassword, checkPassword, getUserPosts, getUserByEmail
from pylowiki.lib.db.activity import getMemberPosts
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.facilitator import getFacilitatorsByUser
from pylowiki.lib.db.workshop import getWorkshopByID, getWorkshopsByOwner
from pylowiki.lib.db.pmember import getPrivateMemberWorkshops
from pylowiki.lib.db.follow import getUserFollowers, getWorkshopFollows, getUserFollows, isFollowing, getFollow, Follow
from pylowiki.lib.db.event import Event, getParentEvents
from pylowiki.lib.db.flag import getFlags
from pylowiki.lib.db.revision import Revision, getRevisionByCode, getParentRevisions


from hashlib import md5

log = logging.getLogger(__name__)

class ProfileController(BaseController):
    
    ##@h.login_required
    def showUserPage(self, id1, id2, id3 = ''):
        # Called when visiting /profile/urlCode/url
        code = id1
        url = id2
        rev = id3
        c.user = get_user(code, url)
        if id3 != '':
            c.revision = getRevisionByCode(id3)
        else:
            c.revision = False

        c.revisions = getParentRevisions(c.user.id)
        c.title = c.user['name']
        c.geoInfo = getGeoInfo(c.user.id)
        c.isFollowing = False
        if 'user' in session and c.authuser:
           c.isFollowing = isFollowing(c.authuser.id, c.user.id) 
        else:
           c.isFollowing = False

        
        if 'user' in session and c.user.id == c.authuser.id:
            c.pworkshops = []
            privList = getPrivateMemberWorkshops(c.user['email'])
            for p in privList:
                w = getWorkshopByID(p.owner)
                c.pworkshops.append(w)
        else:
            c.pmembers = False

        fList = getFacilitatorsByUser(c.user.id)
        c.facilitatorWorkshops = []
        c.pendingFacilitators = []
        for f in fList:
           if 'pending' in f and f['pending'] == '1':
              c.pendingFacilitators.append(f)
           elif f['disabled'] == '0':
              wID = f['workshopID']
              myW = getWorkshopByID(wID)
              if myW['startTime'] == '0000-00-00' or myW['deleted'] == '1' or myW['public_private'] != 'public':
                 # show to the workshop owner, show to the facilitator owner, show to admin
                 if 'user' in session: 
                     if c.authuser.id == f.owner or isAdmin(c.authuser.id):
                         c.facilitatorWorkshops.append(myW)
              else:
                    c.facilitatorWorkshops.append(myW)

        fList = getWorkshopFollows(c.user.id)
        ##log.info('fList is %s userID is %s'%(fList, c.user.id))
        c.followingWorkshops = []
        for f in fList:
           wID = f['thingID']
           c.followingWorkshops.append(getWorkshopByID(wID))

        uList = getUserFollows(c.user.id)
        ##log.info('uList is %s c.user.id is %s'%(uList, c.user.id))
        c.followingUsers = []
        for u in uList:
           uID = u['thingID']
           c.followingUsers.append(getUserByID(uID))

        uList = getUserFollowers(c.user.id)
        ##log.info('uList is %s c.user.id is %s'%(uList, c.user.id))
        c.userFollowers = []
        for u in uList:
           uID = u.owner
           c.userFollowers.append(getUserByID(uID))

        if 'user' in session and (c.user.id == c.authuser.id or isAdmin(c.authuser.id)):
            pList = getMemberPosts(c.user, 0)
        else:
            pList = getMemberPosts(c.user, 1)
        c.totalPoints = 0
        c.suggestions = []
        c.resources = []
        c.discussions = []
        c.comments = []
        c.flags = 0
        resUpVotes = 0
        c.resVotes = 0
        comUpVotes = 0
        c.comVotes = 0
        disUpVotes = 0
        c.disVotes = 0

        c.posts = len(pList)
        for p in pList:
           if p['deleted'] == '0' and p['disabled'] == '0':
               if p.objType == 'suggestion':
                   c.suggestions.append(p)
               elif p.objType == 'resource':
                   c.resources.append(p)
                   resUpVotes += int(p['ups'])
                   c.resVotes = c.resVotes + int(p['ups']) + int(p['downs'])
               elif p.objType == 'discussion':
                   c.discussions.append(p)
                   disUpVotes += int(p['ups'])
                   c.disVotes = c.disVotes + int(p['ups']) + int(p['downs'])
               elif p.objType == 'comment':
                   c.comments.append(p)
                   comUpVotes += int(p['ups'])
                   c.comVotes = c.comVotes + int(p['ups']) + int(p['downs'])

           fList = getFlags(p)
           if fList:
              c.flags += len(fList)
           if 'ups' in p and 'downs' in p:
               t = int(p['ups']) - int(p['downs'])
               c.totalPoints += t 

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

        c.numRes = len(c.resources)
        if c.resVotes > 0:
            c.resUpsPercent = 100*float(resUpVotes)/float(c.resVotes)
        else:
            c.resUpsPercent = 0

        c.numDis = len(c.discussions)
        if c.disVotes > 0:
            c.disUpsPercent = 100*float(disUpVotes)/float(c.disVotes)
        else:
            c.disUpsPercent = 0

        c.numComs = len(c.comments)
        if c.comVotes > 0:
            c.comUpsPercent = 100*float(comUpVotes)/float(c.comVotes)
        else:
            c.comUpsPercent = 0

        return render("/derived/profile.bootstrap")
    
    def showUserSuggestions(self, id1, id2):
        # Called when visiting /profile/urlCode/url/suggestions
        code = id1
        url = id2
        c.user = get_user(code, url)
        c.title = c.user['name']
        c.geoInfo = getGeoInfo(c.user.id)
        c.isFollowing = False
        if 'user' in session and c.authuser:
           c.isFollowing = isFollowing(c.authuser.id, c.user.id) 
        else:
           c.isFollowing = False

        pList = getUserPosts(c.user)
        c.totalPoints = 0
        c.suggestions = []
        c.userFollowers = []
        c.flags = 0

        uList = getUserFollowers(c.user.id)
        ##log.info('uList is %s c.user.id is %s'%(uList, c.user.id))
        c.userFollowers = []
        for u in uList:
           uID = u.owner
           c.userFollowers.append(getUserByID(uID))


        c.posts = len(pList)
        for p in pList:
           if p['deleted'] == '0' and p['disabled'] == '0':
               if p.objType == 'suggestion':
                   c.suggestions.append(p)

           fList = getFlags(p)
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
        code = id1
        url = id2
        c.user = get_user(code, url)
        c.title = c.user['name']
        c.geoInfo = getGeoInfo(c.user.id)
        c.isFollowing = False
        if 'user' in session and c.authuser:
           c.isFollowing = isFollowing(c.authuser.id, c.user.id) 
        else:
           c.isFollowing = False

        uList = getUserFollows(c.user.id)
        ##log.info('uList is %s c.user.id is %s'%(uList, c.user.id))
        c.followingUsers = []
        for u in uList:
           uID = u['thingID']
           c.followingUsers.append(getUserByID(uID))

        uList = getUserFollowers(c.user.id)
        ##log.info('uList is %s c.user.id is %s'%(uList, c.user.id))
        c.userFollowers = []
        for u in uList:
           uID = u.owner
           c.userFollowers.append(getUserByID(uID))

        pList = getUserPosts(c.user)
        c.totalPoints = 0
        c.resources = []
        c.flags = 0
        resUpVotes = 0
        c.resVotes = 0

        c.posts = len(pList)
        for p in pList:
           if p['deleted'] == '0' and p['disabled'] == '0':
               if p.objType == 'resource':
                   c.resources.append(p)
                   resUpVotes += int(p['ups'])
                   c.resVotes = c.resVotes + int(p['ups']) + int(p['downs'])

           fList = getFlags(p)
           if fList:
              c.flags += len(fList)
           if 'ups' in p and 'downs' in p:
               t = int(p['ups']) - int(p['downs'])
               c.totalPoints += t 

        c.numRes = len(c.resources)
        if c.resVotes > 0:
            c.resUpsPercent = 100*float(resUpVotes)/float(c.resVotes)
        else:
            c.resUpsPercent = 0

        c.count = len(c.resources)
        c.paginator = paginate.Page(
            c.resources, page=int(request.params.get('page', 1)),
            items_per_page = 25, item_count = c.count
        )

        return render("/derived/profileResources.bootstrap")
    
    def showUserDiscussions(self, id1, id2):
        # Called when visiting /profile/urlCode/url/discussions
        code = id1
        url = id2
        c.user = get_user(code, url)
        c.title = c.user['name']
        c.geoInfo = getGeoInfo(c.user.id)
        c.isFollowing = False
        if 'user' in session and c.authuser:
           c.isFollowing = isFollowing(c.authuser.id, c.user.id) 
        else:
           c.isFollowing = False

        uList = getUserFollows(c.user.id)
        ##log.info('uList is %s c.user.id is %s'%(uList, c.user.id))
        c.followingUsers = []
        for u in uList:
           uID = u['thingID']
           c.followingUsers.append(getUserByID(uID))

        uList = getUserFollowers(c.user.id)
        ##log.info('uList is %s c.user.id is %s'%(uList, c.user.id))
        c.userFollowers = []
        for u in uList:
           uID = u.owner
           c.userFollowers.append(getUserByID(uID))

        pList = getUserPosts(c.user)
        c.totalPoints = 0
        c.discussions = []
        c.flags = 0
        disUpVotes = 0
        c.disVotes = 0

        c.posts = len(pList)
        for p in pList:
           if p['deleted'] == '0' and p['disabled'] == '0':
               if p.objType == 'discussion':
                   c.discussions.append(p)
                   disUpVotes += int(p['ups'])
                   c.disVotes = c.disVotes + int(p['ups']) + int(p['downs'])

           fList = getFlags(p)
           if fList:
              c.flags += len(fList)
           if 'ups' in p and 'downs' in p:
               t = int(p['ups']) - int(p['downs'])
               c.totalPoints += t 

        c.numDis = len(c.discussions)
        if c.disVotes > 0:
            c.disUpsPercent = 100*float(disUpVotes)/float(c.disVotes)
        else:
            c.disUpsPercent = 0

        c.count = len(c.discussions)
        c.paginator = paginate.Page(
            c.discussions, page=int(request.params.get('page', 1)),
            items_per_page = 25, item_count = c.count
        )


        return render("/derived/profileDiscussions.bootstrap")
    
    def showUserComments(self, id1, id2):
        # Called when visiting /profile/urlCode/url/comments
        code = id1
        url = id2
        c.user = get_user(code, url)
        c.title = c.user['name']
        c.geoInfo = getGeoInfo(c.user.id)
        c.isFollowing = False
        if 'user' in session and c.authuser:
           c.isFollowing = isFollowing(c.authuser.id, c.user.id) 
        else:
           c.isFollowing = False

        uList = getUserFollows(c.user.id)
        ##log.info('uList is %s c.user.id is %s'%(uList, c.user.id))
        c.followingUsers = []
        for u in uList:
           uID = u['thingID']
           c.followingUsers.append(getUserByID(uID))

        uList = getUserFollowers(c.user.id)
        ##log.info('uList is %s c.user.id is %s'%(uList, c.user.id))
        c.userFollowers = []
        for u in uList:
           uID = u.owner
           c.userFollowers.append(getUserByID(uID))

        pList = getUserPosts(c.user)
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

           fList = getFlags(p)
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
        code = id1
        url = id2
        c.user = get_user(code, url)
        c.title = c.user['name']
        c.geoInfo = getGeoInfo(c.user.id)
        c.isFollowing = False
        if 'user' in session and c.authuser:
           c.isFollowing = isFollowing(c.authuser.id, c.user.id) 
        else:
           c.isFollowing = False

        uList = getUserFollows(c.user.id)
        ##log.info('uList is %s c.user.id is %s'%(uList, c.user.id))
        c.followingUsers = []
        for u in uList:
           uID = u['thingID']
           c.followingUsers.append(getUserByID(uID))

        uList = getUserFollowers(c.user.id)
        ##log.info('uList is %s c.user.id is %s'%(uList, c.user.id))
        c.listUserFollowers = []
        for u in uList:
           uID = u.owner
           c.listUserFollowers.append(getUserByID(uID))

        pList = getUserPosts(c.user)
        c.totalPoints = 0
        c.flags = 0

        c.posts = len(pList)
        for p in pList:
           fList = getFlags(p)
           if fList:
              c.flags += len(fList)
           if 'ups' in p and 'downs' in p:
               t = int(p['ups']) - int(p['downs'])
               c.totalPoints += t 

        c.count = len(c.listUserFollowers)
        c.paginator = paginate.Page(
            c.listUserFollowers, page=int(request.params.get('page', 1)),
            items_per_page = 25, item_count = c.count
        )

        return render("/derived/profileFollowers.bootstrap")
    
    def showUserFollows(self, id1, id2):
        # Called when visiting /profile/urlCode/url/following
        code = id1
        url = id2
        c.user = get_user(code, url)
        c.title = c.user['name']
        c.geoInfo = getGeoInfo(c.user.id)
        c.isFollowing = False
        if 'user' in session and c.authuser:
           c.isFollowing = isFollowing(c.authuser.id, c.user.id) 
        else:
           c.isFollowing = False

        uList = getUserFollows(c.user.id)
        ##log.info('uList is %s c.user.id is %s'%(uList, c.user.id))
        c.listFollowingUsers = []
        for u in uList:
           uID = u['thingID']
           c.listFollowingUsers.append(getUserByID(uID))

        uList = getUserFollowers(c.user.id)
        ##log.info('uList is %s c.user.id is %s'%(uList, c.user.id))
        c.userFollowers = []
        for u in uList:
           uID = u.owner
           c.userFollowers.append(getUserByID(uID))

        pList = getUserPosts(c.user)
        c.totalPoints = 0
        c.flags = 0

        c.posts = len(pList)
        for p in pList:
           fList = getFlags(p)
           if fList:
              c.flags += len(fList)
           if 'ups' in p and 'downs' in p:
               t = int(p['ups']) - int(p['downs'])
               c.totalPoints += t 

        c.count = len(c.listFollowingUsers)
        c.paginator = paginate.Page(
            c.listFollowingUsers, page=int(request.params.get('page', 1)),
            items_per_page = 25, item_count = c.count
        )

        return render("/derived/profileFollowing.bootstrap")
    
    @h.login_required
    def index( self ):
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
        code = id1
        url = id2
        c.user = get_user(code, url)
        c.events = getParentEvents(c.user)
        if isAdmin(c.authuser.id) or c.user.id == c.authuser.id:
            c.title = 'Member Dashboard'
            if 'confTab' in session:
                c.tab = session['confTab']
                session.pop('confTab')
                session.save()
            if isAdmin(c.authuser.id):
                c.admin = True
            else:
                c.admin = False
            return render('/derived/6_profile_dashboard.bootstrap')
        else:
            return render('/derived/404.bootstrap')

    @h.login_required
    def editHandler(self,id1, id2):
        code = id1
        url = id2
        c.user = get_user(code, url)
        
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
        if c.user.id != c.authuser.id and isAdmin(c.authuser.id) != 1:
            return render('/derived/404.bootstrap')
            
        session['confTab'] = "tab1"
        session.save()
        
        if 'pictureFile' in request.POST:
            picture = request.POST['pictureFile']
            if picture == "":
                picture = False



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
                checkUser = getUserByEmail(email)
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

        if picture != False:
           identifier = 'avatar'
           ##log.info('doing new picture for %s'%c.authuser['name'])
           imageFile = picture.file
           filename = picture.filename
           hash = saveImage(imageFile, filename, c.user, 'avatar', c.user)
           c.user['pictureHash'] = hash
           resizeImage(identifier, hash, 200, 200, 'profile')
           resizeImage(identifier, hash, 25, 25, 'thumbnail')
           anyChange = True
           changeMsg = changeMsg + "Picture updated. "

        if nameChange:
            c.user['url'] = urlify(c.user['name'])
            if c.user.id == c.authuser.id:
                session["userURL"] = c.user['url']
                session.save()
                c.authuser = c.user
            log.info('Changed name')
        if anyChange and perror == 0:
            commit(c.user)
            Event('Profile updated.', changeMsg, c.user, c.authuser)
            Revision(c.user, c.user['name'], c.user)
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
        code = id1
        url = id2
        c.user = get_user(code, url)
        
        perror = 0
        perrorMsg = ""
        changeMsg = ""
        # make sure they are authorized to do this
        if c.user.id != c.authuser.id and isAdmin(c.authuser.id) != 1:
            return render('/derived/404.bootstrap')
            
        
        if 'password' in request.params:
            password = request.params['password']

        else:
            password = False 
        if 'verify_password' in request.params:
            verify_password = request.params['verify_password']
        else:
            verify_password = False 

        if password and verify_password and password == verify_password:
            changePassword(c.user, password)
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
            old_password = checkPassword(c.authuser, request.params['oldPassword'])
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
            changePassword(c.user, newPassword)
            Event('Profile updated.', 'Password changed', c.user, c.authuser)
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
    def followHandler(self, id1, id2):
        code = id1
        url = id2
        c.user = get_user(code, url)
        ##log.info('followHandler %s %s' % (code, url))
        # this gets a follow which has been unfollowed
        f = getFollow(c.authuser.id, c.user.id)
        if f:
           log.info('f is %s' % f)
           f['disabled'] = '0'
           commit(f)
        # this only gets follows which are not disabled
        elif not isFollowing(c.authuser.id, c.user.id):
           ##log.info('not isFollowing')
           f = Follow(c.authuser.id, c.user.id, 'user')
        else:
           ##log.info('else')
           f = Follow(c.authuser.id, c.user.id, 'user')

        return "ok"

    @h.login_required
    def unfollowHandler(self, id1, id2):
        code = id1
        url = id2
        c.user = get_user(code, url)
        log.info('unfollowHandler %s %s' % (code, url))
        f = getFollow(c.authuser.id, c.user.id)
        if f:
           log.info('f is %s' % f)
           f['disabled'] = '1'
           commit(f)

        return "ok"

    @h.login_required
    def userAdmin(self, id1, id2):
        if not isAdmin(c.authuser.id):
           return render("/derived/404.bootstrap")

        code = id1
        url = id2
        c.user = get_user(code, url)
        c.title = c.user['name'] 
        c.events = getParentEvents(c.user)

        return render("/derived/member_admin.bootstrap")


    @h.login_required
    def enableHandler(self, id1, id2):
        code = id1
        url = id2
        c.user = get_user(code, url)
        if not isAdmin(c.authuser.id):
            return render("/derived/404.bootstrap")

        session['confTab'] = "tab3"
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
              
           e = Event(eAction, enableUserReason, c.user, c.authuser)
           commit(c.user)
           session['alert'] = alert
           session.save()
        else:
           alert = {'type':'error'}
           alert['title'] = 'Error:'
           alert['content'] = 'Enter reason and verify action before submit'
           session['alert'] = alert
           session.save()

        return redirect("/profile/" + code + "/" + url + "/dashboard" )

    @h.login_required
    def privsHandler(self, id1, id2):
        code = id1
        url = id2
        c.user = get_user(code, url)
        if not isAdmin(c.authuser.id):
            return render("/derived/404.bootstrap")
            
        session['confTab'] = "tab3"
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
            e = Event(eAction, accessChangeReason, c.user, c.authuser)
            commit(c.user)
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

        return redirect("/profile/" + code + "/" + url + "/dashboard" )


