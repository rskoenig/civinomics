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
from pylowiki.lib.db.user import get_user, getUserByID, isAdmin
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.facilitator import getFacilitatorsByUser
from pylowiki.lib.db.workshop import getWorkshopByID, getWorkshopsByOwner
from pylowiki.lib.db.follow import getUserFollowers, getWorkshopFollows, getUserFollows, isFollowing, getFollow, Follow
from pylowiki.lib.db.event import Event, getParentEvents
from pylowiki.lib.db.account import Account, getUserAccount


from hashlib import md5

log = logging.getLogger(__name__)

class ProfileController(BaseController):
    
    @h.login_required
    def showUserPage(self, id1, id2):
        # Called when visiting /profile/urlCode/url
        code = id1
        url = id2
        c.user = get_user(code, url)
        c.title = c.user['name']
        c.geoInfo = getGeoInfo(c.user.id)
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


        return render("/derived/profile.html")
    
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
        c.title = 'Edit your profile'
        c.states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
        c.months = ['Month', 'Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        c.culturalBackground = ['Black', 'Indian', 'Latino', 'Middle Eastern', 'Native American', 'North East Asian', 'Pacific Islander', 'South East Asian', 'White', 'Mixed Race', 'Other']
        c.genders = ['Female', 'Male', 'Other']
        # Religious affiliation
        c.religions = ['Christianity', 'Atheist/Agnostic/Non-religious', 'Judaism', 'Buddhism', 'Hinduism', 'Unitarian Universalist', 'Wiccan/Pagan/Druid', 'Spiritualist', 'Native American Religion', 'Baha\'i', 'New Age', 'Sikhism', 'Scientology', 'Humanism', 'Deity (Deist)', 'Taoism', 'Eckankar']
        c.days = ['Day'] + [str(r) for r in range(1, 32)]
        c.years = ['Year'] + [str(r) for r in range(1900, 2011)]
        return render('/derived/account_create.html')

    @h.login_required
    def editSubmit(self):
        try:
            firstName = request.params['first_name']
            lastName = request.params['last_name']
            email = request.params['email']
            tagline = request.params['tagline']
            #zipCode = request.params['zip_code']
            picture = request.POST['pictureFile']
            
            nameChange = False
            anyChange = False
            u = c.authuser
            if firstName != '':
                u['firstName'] = firstName
                nameChange = True
                anyChange = True
            if lastName != '':
                u['lastName'] = lastName
                nameChange = True
                anyChange = True
            if tagline != '':
                if len(tagline)>140:
                    u['tagline'] = tagline[:140]
                else:
                    u['tagline'] = tagline
                anyChange = True
            #if zipCode != '':
            #    u['zipCode'] = zipCode
                
            #    anyChange = True
            try:
                identifier = 'avatar'
                # CCN below fails if no picture file
                imageFile = picture.file
                filename = picture.filename
                
                hash = saveImage(imageFile, filename, u, 'avatar', u)
                u['pictureHash'] = hash
                
                resizeImage(identifier, hash, 200, 200, 'profile')
                resizeImage(identifier, hash, 25, 25, 'thumbnail')

                anyChange = True
            except:
                raise
                log.info('no picture change for %s'%c.authuser['name'])
            if nameChange:
                u['name'] = '%s %s' %(u['firstName'], u['lastName'])
                log.info('Changed name')
            if anyChange:
                commit(u)
            return redirect('/account/edit')
        except:
            h.flash('Error', 'error')
            raise
            return redirect('/account/edit')
    
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

        return render("/derived/user_admin.html")


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

