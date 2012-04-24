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
from pylowiki.lib.db.user import get_user
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.facilitator import getUserFacilitators
from pylowiki.lib.db.workshop import getWorkshopByID
from pylowiki.lib.db.follow import getUserFollowers, getWorkshopFollows, getUserFollows, isFollowing, unfollow


from hashlib import md5

log = logging.getLogger(__name__)

class AccountController(BaseController):
    
    @h.login_required
    def showUserPage(self, id1, id2):
        # Called when visiting /account/user-name
        code = id1
        url = id2
        c.user = get_user(code, url)
        c.title = c.user['name']
        c.geoInfo = getGeoInfo(c.user.id)

        fList = getUserFacilitators(c.user.id)
        c.facilitatorWorkshops = []
        for f in fList:
           wID = f['workshopID']
           c.facilitatorWorkshops.append(getWorkshopByID(wID))

        followers = getUserFollowers(c.user.id)

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
