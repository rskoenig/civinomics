# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

import webhelpers.paginate as paginate
import pylowiki.lib.helpers as h
from pylons import config

from pylowiki.lib.images import saveImage, resizeImage
from pylowiki.lib.db.geoInfo import GeoInfo, getGeoInfo
from pylowiki.lib.db.user import get_user, getUserByID, isAdmin, changePassword
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.facilitator import getFacilitatorsByUser
from pylowiki.lib.db.workshop import getWorkshopByID, getWorkshopsByOwner
from pylowiki.lib.db.follow import getUserFollowers, getWorkshopFollows, getUserFollows, isFollowing, getFollow, Follow
from pylowiki.lib.db.event import Event, getParentEvents
from pylowiki.lib.db.account import Account, getUserAccount


from hashlib import md5

log = logging.getLogger(__name__)

class ProfileController(BaseController):
    
    ##@h.login_required
    def showUserPage(self, id1, id2):
        # Called when visiting /profile/urlCode/url
        code = id1
        url = id2
        c.user = get_user(code, url)
        c.title = c.user['name']
        c.geoInfo = getGeoInfo(c.user.id)
        c.isFollowing = False
        if c.authuser:
           c.isFollowing = isFollowing(c.authuser.id, c.user.id) 
        
        c.account = getUserAccount(c.user.id)

        fList = getFacilitatorsByUser(c.user.id)
        c.facilitatorWorkshops = []
        c.pendingFacilitators = []
        for f in fList:
           if 'pending' in f and f['pending'] == '1':
              c.pendingFacilitators.append(f)
           elif f['disabled'] == '0':
              wID = f['workshopID']
              myW = getWorkshopByID(wID)
              if myW['startTime'] == '0000-00-00':
                 # show to the workshop owner, show to the facilitator owner
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


        return render("/derived/profile.bootstrap")
    
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
    def user( self, id ):
        c.user = get_user( id )

        c.list = c.user.events

        types = ['edit', 'create', 'delete', 'revert', 'restore']
        stats = []
        
        for t in types:
            stats.append(meta.Session.query( Event ).filter_by( type = t ).join( User ).filter_by( name = c.user.name ).count())

        c.statzip = zip ( types, stats )
        
        c.count = len( c.list )
        c.paginator = paginate.Page(
            c.list, page=int(request.params.get('page', 1)),
            items_per_page = 25, item_count = c.count
        )
        c.title = c.heading = c.user.name
        return render( "/derived/account.mako" )

    @h.login_required
    def edit(self):
        c.title = 'Edit Your Civinomics Profile'
        return render('/derived/profile_edit.bootstrap')

    @h.login_required
    def editSubmit(self):
        perror = 0
        perrorMsg = ""
        if 'pictureFile' in request.POST:
            picture = request.POST['pictureFile']
            if picture == "":
                picture = False
        else:
            picture = False
        log.info('picture is %s'%picture)
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
            log.info('changed password for  %s'%c.authuser['name'])

        if password and verify_password and password != verify_password:
            perror = 1
            perrorMsg = 'Password and Verify Password must match'
        if password or verify_password and password != verify_password:
            perror = 1
            perrorMsg = 'Password and Verify Password must match'

        if 'first_name' in request.params:
            firstName = request.params['first_name']
        else:
            firstName = False
        if 'last_name' in request.params:
            lastName = request.params['last_name']
        else:
            lastName = False
        if 'email' in request.params:
            email = request.params['email']
        else:
            email = False
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
        if lastName and lastName != '' and lastName != c.authuser['lastName']:
            u['lastName'] = lastName
            nameChange = True
            anyChange = True
        if tagline and tagline != '' and tagline != c.authuser['tagline']:
            if len(tagline)>140:
                u['tagline'] = tagline[:140]
            else:
                u['tagline'] = tagline
                anyChange = True

        log.info('before doing new picture for %s'%c.authuser['name'])
        if picture != False:
           identifier = 'avatar'
           log.info('doing new picture for %s'%c.authuser['name'])
           imageFile = picture.file
           filename = picture.filename
           hash = saveImage(imageFile, filename, u, 'avatar', u)
           u['pictureHash'] = hash
           resizeImage(identifier, hash, 200, 200, 'profile')
           resizeImage(identifier, hash, 25, 25, 'thumbnail')
           log.info('Saving picture change for %s'%c.authuser['name'])
           anyChange = True

        if nameChange:
            u['name'] = '%s %s' %(u['firstName'], u['lastName'])
            log.info('Changed name')
        if anyChange and perror == 0:
            commit(u)
            h.flash('Changes saved.', 'success')
        elif anyChange and perror == 1:
            h.flash(perrorMsg, 'error')
        else:
            h.flash('No changes submitted.', 'success')

        return redirect('/profile/edit')
    
    def hashPicture(self, username, title):
        return md5(username + title).hexdigest()

    @h.login_required
    def followHandler(self, id1, id2):
        code = id1
        url = id2
        c.user = get_user(code, url)
        log.info('followHandler %s %s' % (code, url))
        # this gets a follow which has been unfollowed
        f = getFollow(c.authuser.id, c.user.id)
        if f:
           log.info('f is %s' % f)
           f['disabled'] = False
           commit(f)
        # this only gets follows which are not disabled
        elif not isFollowing(c.authuser.id, c.user.id):
           log.info('not isFollowing')
           f = Follow(c.authuser.id, c.user.id, 'user')
        else:
           log.info('else')
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
           f['disabled'] = True
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
        c.account = getUserAccount(c.user.id)
        c.workshops = getWorkshopsByOwner(c.user.id)
        log.info('userAdmin %s %s' % (code, url))

        return render("/derived/user_admin.bootstrap")


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
              c.user['disabled'] = 0
              eAction = 'User Enabled'
           else:
              c.user['disabled'] = 1
              eAction = 'User Disabled'
 
           e = Event(eAction, enableUserReason, c.user, c.authuser)
           commit(c.user)
           
           h.flash(eAction, 'success')
        else:
           h.flash('Error: Enter reason and verify action before submit', 'error')

        return redirect("/profile/" + code + "/" + url + "/admin" )

    @h.login_required
    def privsHandler(self, id1, id2):
        code = id1
        url = id2
        c.user = get_user(code, url)
        log.info('privHandler %s %s' % (code, url))

        if 'setPrivs' in request.params and 'changeAccessReason' in request.params and request.params['changeAccessReason'] != '':
           eAction = 'Access Level Changed from ' + c.user['accessLevel'] + ' to ' + request.params['setPrivs']
           c.user['accessLevel'] = request.params['setPrivs']
           changeAccessReason = request.params['changeAccessReason']
           e = Event(eAction, changeAccessReason, c.user, c.authuser)
           commit(c.user)
           h.flash('New Access Level Set', 'success')
        else:
           h.flash('Error: Enter reason and pecify a new access level', 'error')

        return redirect("/profile/" + code + "/" + url + "/admin" )

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           