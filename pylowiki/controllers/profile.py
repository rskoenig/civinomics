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
from pylowiki.lib.db.user import get_user, getUserByID, isAdmin, changePassword, checkPassword, getUserPosts
from pylowiki.lib.db.activity import getMemberPosts
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.facilitator import getFacilitatorsByUser
from pylowiki.lib.db.workshop import getWorkshopByID, getWorkshopsByOwner, getAssociateWorkshops
from pylowiki.lib.db.pmember import getPrivateMemberWorkshops
from pylowiki.lib.db.follow import getUserFollowers, getWorkshopFollows, getUserFollows, isFollowing, getFollow, Follow
from pylowiki.lib.db.event import Event, getParentEvents
from pylowiki.lib.db.account import Account, getUserAccount, getUserAccounts
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

        c.accounts = getUserAccounts(c.user)
        
        if 'user' in session and c.user.id == c.authuser.id:
            c.associates = getAssociateWorkshops(c.user)
            c.pworkshops = []
            pList = getPrivateMemberWorkshops(c.user['email'])
            for p in pList:
                w = getWorkshopByID(p.owner)
                c.pworkshops.append(w)
        else:
            c.associates = False
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
              if myW['startTime'] == '0000-00-00' or myW['deleted'] == '1':
                 # show to the workshop owner, show to the facilitator owner
                 if 'user' in session: 
                     if c.authuser.id == f.owner or c.authuser.id == myW.owner:
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

        c.account = getUserAccount(c.user.id)

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

        c.account = getUserAccount(c.user.id)

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

        c.account = getUserAccount(c.user.id)

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

        c.account = getUserAccount(c.user.id)

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

        c.account = getUserAccount(c.user.id)

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

        c.account = getUserAccount(c.user.id)

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
    def edit(self):
        c.title = 'Edit Your Civinomics Profile'
        return render('/derived/profile_edit.bootstrap')

    @h.login_required
    def editSubmit(self):
        perror = 0
        perrorMsg = ""
        changeMsg = ""

        # see if an admin is doing this
        if 'memberCode' in request.params and 'memberURL' in request.params and isAdmin(c.authuser.id):
            code = request.params['memberCode']
            url = request.params['memberURL']
            u = get_user(code, urlify(url))
            returnURL = "/profile/" + code + "/" + url + "/admin"
        else:
            u = c.authuser
            returnURL = "/profile/edit"

        # make sure they are authorized to do this
        if u.id != c.authuser.id and isAdmin(c.authuser.id) != 1:
            return redirect('/')

        if 'pictureFile' in request.POST:
            picture = request.POST['pictureFile']
            if picture == "":
                picture = False
        else:
            picture = False
        #log.info('picture is %s'%picture)
        u = c.authuser

        if 'password' in request.params:
            password = request.params['password']

        else:
            password = False 
        if 'verify_password' in request.params:
            verify_password = request.params['verify_password']

        else:
            verify_password = False 

        if password and verify_password and password == verify_password:
            changePassword(u, password)
            changeMsg = changeMsg + "Password updated. "
            ##log.info('changed password for  %s'%u['name'])


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
            log.info('OLD is %s'%request.params['oldPassword'])
            log.info('Pass is %s'%old_password)
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
            changePassword(u, newPassword)
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

        firstName = False
        if 'first_name' in request.params:
            firstName = request.params['first_name']
            if firstName == '':
               firstName = False
        if not firstName:
            perror = 1
            perrorMsg = perrorMsg + ' First name required.'


        lastName = False
        if 'last_name' in request.params:
            lastName = request.params['last_name']
            if lastName == '':
                lastName = False
        if not lastName:
            perror = 1
            perrorMsg = perrorMsg + ' Last name required.'

        email = False
        if 'email' in request.params:
            email = request.params['email']
            if email == '':
                email = False
        if not email:
            perror = 1
            perrorMsg = perrorMsg + ' Email required.'

        if 'tagline' in request.params:
            tagline = request.params['tagline']
        else:
            tagline = False

        nameChange = False
        anyChange = False
        if firstName and firstName != '' and firstName != c.authuser['firstName']:
            u['firstName'] = firstName
            nameChange = True
            anyChange = True
            changeMsg = changeMsg + "First name updated. "
        if lastName and lastName != '' and lastName != c.authuser['lastName']:
            u['lastName'] = lastName
            nameChange = True
            anyChange = True
            changeMsg = changeMsg + "Last name updated. "
        if tagline and tagline != '' and tagline != c.authuser['tagline']:
            if len(tagline)>140:
                u['tagline'] = tagline[:140]
            else:
                u['tagline'] = tagline
                anyChange = True

            changeMsg = changeMsg + "Tagline updated. "

        ##log.info('before doing new picture for %s'%c.authuser['name'])
        if picture != False:
           identifier = 'avatar'
           ##log.info('doing new picture for %s'%c.authuser['name'])
           imageFile = picture.file
           filename = picture.filename
           hash = saveImage(imageFile, filename, u, 'avatar', u)
           u['pictureHash'] = hash
           resizeImage(identifier, hash, 200, 200, 'profile')
           resizeImage(identifier, hash, 25, 25, 'thumbnail')
           ##log.info('Saving picture change for %s'%c.authuser['name'])
           anyChange = True
           changeMsg = changeMsg + "Picture updated. "

        if nameChange:
            u['name'] = '%s %s' %(u['firstName'], u['lastName'])
            u['url'] = urlify(u['name'])
            if u.id == c.authuser.id:
                session["userURL"] = u['url']
                session.save()
                c.authuser = u
            log.info('Changed name')
        if anyChange and perror == 0:
            commit(u)
            Event('Profile updated.', changeMsg, u, c.authuser)
            Revision(u, u['name'], u)
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
           h.flash('You are not authorized.', 'error')
           return redirect("/")

        code = id1
        url = id2
        c.user = get_user(code, url)
        c.title = c.user['name'] 
        c.events = getParentEvents(c.user)
        c.accounts = getUserAccounts(c.user)
        if c.accounts:
            for account in c.accounts:
                if 'type' not in account:
                    account['type'] = 'basic'
                    account['numParticipants'] = '100'
                    account['urlCode'] = toBase62(account)

                if 'orgName' not in account:
                    account['orgName'] = c.user['name']
                    account['orgEmail'] = c.user['email']

            commit(account)
        log.info('c.accounts is %s' %c.accounts)

        return render("/derived/member_admin.bootstrap")


    @h.login_required
    def enableHandler(self, id1, id2):
        code = id1
        url = id2
        c.user = get_user(code, url)
        log.info('enableHandler %s %s' % (code, url))

        if 'verifyEnableUser' in request.params and 'enableUserReason' in request.params and len(request.params['enableUserReason']) > 0:
           log.info('disabled is %s' % c.user['disabled'])
           enableUserReason = request.params['enableUserReason']

           if c.user['disabled'] == '1':
              c.user['disabled'] = '0'
              eAction = 'User Enabled'
              alert = {'type':'success'}
              alert['title'] = 'Enabled:'
              alert['content'] = 'Account Enabled'
           else:
              c.user['disabled'] = '1'
              eAction = 'User Disabled'
              alert = {'type':'warning'}
              alert['title'] = 'Disabled:'
              alert['content'] = 'Account Disabled'
              
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

        return redirect("/profile/" + code + "/" + url + "/admin" )

    @h.login_required
    def privsHandler(self, id1, id2):
        code = id1
        url = id2
        c.user = get_user(code, url)
        log.info('privHandler %s %s' % (code, url))
        "Check which of three radio type buttons was bubbled in"
        if ('changeAccessReason' in request.params) and (request.params['changeAccessReason'] != '') and ('setPrivsUser' in request.params or 'setPrivsFacil' in request.params or 'setPrivsAdmin' in request.params):
           eAction = 'Access Level Changed from ' + c.user['accessLevel'] + ' to '
           if 'setPrivsUser' in request.params:
               c.user['accessLevel'] = '0'
               eAction += '0'
           elif 'setPrivsFacil' in request.params:
               c.user['accessLevel'] = '100'
               eAction += '0'
           else:
               c.user['accessLevel'] = '200'
               eAction += '0'
           changeAccessReason = request.params['changeAccessReason']
           e = Event(eAction, changeAccessReason, c.user, c.authuser)
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

        return redirect("/profile/" + code + "/" + url + "/admin" )


