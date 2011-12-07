# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

from pylowiki.model import get_user, get_all_users, meta, Event, User, commit
import webhelpers.paginate as paginate
import pylowiki.lib.helpers as h
from pylons import config
from pylowiki.lib.images import saveImage, resizeImage
from hashlib import md5

log = logging.getLogger(__name__)

class AccountController(BaseController):
    
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

        firstName = request.params['first_name']
        lastName = request.params['last_name']
        email = request.params['email']
        zipCode = request.params['zip_code']
        address = request.params['address']
        state = request.params['state']
        city = request.params['city']
        try:
            request.params['hideBirth']
            hideBirth = 1
        except:
            hideBirth = 0
        birthMonth = request.params['month']
        birthDay = request.params['birthDay']
        birthYear = request.params['birthYear']
        try:
            request.params['hideCultBack']
            hideCultBack = 1
        except:
            hideCultBack = 0
        culturalBackground1 = request.params['culturalBackground1']
        #culturalBackground2 = request.params['culturalBackground2']
        try:
            request.params['hideGender']
            hideGender = 1
        except:
            hideGender = 0
        gender = request.params['gender']
        try:
            request.params['hideReligion']
            hideReligion = 1
        except:
            hideReligion = 0
        religion = request.params['religion']
        tagline = request.params['tagline']
        bio = request.params['bio']
        picture = request.POST['pictureFile']
       
        # Validation goes here...
        
        if len(tagline) > 140:
            tagline = tagline[0:140]


        # Save to database
        u = get_user(c.authuser.name)
        nameChange = 0
        if firstName:
            u.firstName = firstName
            nameChange = 1
        if lastName:
            u.lastName = lastName
            nameChange = 1
        if nameChange:
            u.name = '%s %s'%(u.firstName, u.lastName)

        try:
            hash = self.hashPicture(c.authuser.name, picture.filename)
            u.pictureHash = hash
            saveImage(picture.filename, hash, picture.file, 'avatar')
            resizeImage(picture.filename, hash, 200, 200, 'profile', 'avatar')
            resizeImage(picture.filename, hash, 25, 25, 'thumbnail', 'avatar')
        except:
            # do nothing 
            log.info('no picture change for %s'%c.authuser.name)
        if email:
            u.email = email
        if zipCode:
            u.zipCode = zipCode
        if state:
            u.state = state
        if city:
            u.city = city
        if birthMonth != 'Month':
            u.birthMonth = birthMonth
        if birthDay != 'Day':
            u.birthDay = birthDay
        if birthYear != 'Year':
            u.birthYear = birthYear
        if culturalBackground1:
            u.culturalBackground1 = culturalBackground1
        if gender:
            u.gender = gender
        if religion:
            u.religion = religion
        if tagline != 'in 140 characters or fewer ...':
            u.tagline = tagline
        if bio:
            u.bio = bio
        if address:
            u.address = address
        u.hideBirth = hideBirth
        u.hideGender = hideGender
        u.hideCultBack = hideCultBack
        u.hideReligion = hideReligion

        try:
            commit(u)
        except:
            message = '%s: user info not updated!' % u.name
            log.info(message)
            h.flash(message, 'warning')
            return redirect('/account/edit')
        return redirect('/home/mainPage/%s' % u.name)

    def hashPicture(self, username, title):
        return md5(username + title).hexdigest()
