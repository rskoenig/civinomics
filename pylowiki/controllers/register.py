# -*- coding: utf-8 -*-
import logging, formencode, time

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons import config

from pylowiki.lib.base      import BaseController, render
import pylowiki.lib.helpers     as h
import pylowiki.lib.utils       as utils

from pylowiki.lib.db.user         import User, getUserByEmail, getUserByFacebookAuthId, getActiveUsers, getUserByTwitterId
from pylowiki.lib.db.pmember      import getPrivateMemberByCode
from pylowiki.lib.db.workshop     import getWorkshopByCode, setWorkshopPrivs
from pylowiki.lib.db.geoInfo      import getPostalInfo
from pylowiki.lib.db.dbHelpers    import commit
import pylowiki.lib.db.mainImage  as mainImageLib
from pylowiki.lib.db.revision     import Revision
import pylowiki.lib.mail          as mailLib
import pylowiki.lib.db.photo      as photoLib
import pylowiki.lib.sort          as sort
import pylowiki.lib.db.user       as userLib
import re
import simplejson as json

log = logging.getLogger(__name__)

class plaintextForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    username = formencode.validators.PlainText(not_empty=True)

class RegisterController(BaseController):

    def __before__(self):
        if config['app_conf']['public.reg'] != "true": # set in enviroment config
            h.check_if_login_required()

    def splashDisplay(self):
        c.title = config['custom.titlebar']

        c.backgroundPhoto = {'title': 'City Council Meeting'}
        c.backgroundPhotoURL = '/images/splash/shasta_blur.jpg'
        c.backgroundAuthor = 'unknown'

        #c.photos = photoLib.getAllPhotos()
        #if c.photos and len(c.photos) != 0:
        #    c.photos = sort.sortBinaryByTopPop(c.photos)
        #    p = c.photos[0]
        #    c.backgroundPhoto = p
        #    c.backgroundPhotoURL = "/images/photos/" + p['directoryNum_photos'] + "/orig/" + p['pictureHash_photos'] + ".png"
        #    c.backgroundAuthor = userLib.getUserByID(p.owner)
        #else: 
        #    c.backgroundPhoto = {'title': 'Santa Cruz Beach Boardwalk'}
        #    c.backgroundPhotoURL = '/images/splash/shasta_blur.jpg'
        #    c.backgroundAuthor = 'Ester Kim'

        self.noQuery = False
        c.searchType = "browse"
        self.searchType = "browse"
        c.searchQuery = "All Initiatives" 
        c.scope = {'level':'earth', 'name':'all'}

        if 'splashMsg' in session:
            c.splashMsg = session['splashMsg']
            session.pop('splashMsg')
            session.save()
        if 'registerSuccess' in session:
            c.success = session['registerSuccess']
            session.pop('registerSuccess')
            session.save()
        if 'guestCode' in session and 'workshopCode' in session:
                c.w = getWorkshopByCode(session['workshopCode'])
                if c.w:
                    setWorkshopPrivs(c.w)
                    c.mainImage = mainImageLib.getMainImage(c.w)
                    c.title = c.w['title']
                    c.listingType = False
                    return render('/derived/6_guest_signup.bootstrap')
                else:
                    session.pop('guestCode')
                    session.pop('workshopCode')
                    session.save()
            
        return render("/derived/splash.bootstrap")

    def signupNoExtAuthDisplay(self):

        # todo - clear splash message if this came from /fbSignUp

        if 'splashMsg' in session:
            c.splashMsg = session['splashMsg']
            session.pop('splashMsg')
            session.save()
        if 'registerSuccess' in session:
            c.success = session['registerSuccess']
            session.pop('registerSuccess')
            session.save()
        if 'guestCode' in session and 'workshopCode' in session:
                c.w = getWorkshopByCode(session['workshopCode'])
                if c.w:
                    setWorkshopPrivs(c.w)
                    c.mainImage = mainImageLib.getMainImage(c.w)
                    c.title = c.w['title']
                    c.listingType = False
                    return render('/derived/6_guest_signup.bootstrap')
                else:
                    session.pop('guestCode')
                    session.pop('workshopCode')
                    session.save()
            
        return render("/derived/signupNoExtAuth.bootstrap")

    def fbNewAccount( self ):
        c.splashMsg = False
        splashMsg = {}
        splashMsg['type'] = 'error'
        splashMsg['title'] = 'Error'
        # the visitor has decided to log in with their fb id
        # grab the access token, confirm it's still cool with fb, locate user and log in
        #if 'fbAccessToken' in session and 'fbEmail' in session:
        accessToken = session['fbAccessToken']
        email = session['fbEmail']
        # get user
        user = userLib.getUserByEmail( email )
        if user:
            # unexpected, but if this is the case then we log them in
            return render("/derived/fbLoggingIn.bootstrap")
        else:
            # confirmed this user's account does not already exist - render a
            # page made just for signing this person up by asking facebook one more time
            # if this user is auth'd and there is no account
            return render("/derived/fbSigningUp.bootstrap")

    def fbSignUpDisplay( self ):
        """ This is an intermediary page for the signup process when a facebook user first
        creates an account. """

        c.title = c.heading = "Registration using your Facbook Account"
        c.success = False
        splashMsg = {}
        splashMsg['type'] = 'success'
        splashMsg['title'] = 'Postal code and terms of use.'
        splashMsg['content'] = 'Before we can sign you in, please provide your zipcode and agree to our use terms.'
        session['splashMsg'] = splashMsg
        session.save()

        return render("/derived/fbSignUp.bootstrap")

    def twitterSignUpDisplay( self ):
        """ This is an intermediary page for the signup process when a twitter user first
        creates an account. """

        c.title = c.heading = "Registration using your Twitter Account"
        c.success = False
        splashMsg = {}
        splashMsg['type'] = 'success'
        splashMsg['title'] = 'Email, zipcode and terms of use.'
        splashMsg['content'] = 'Before we can sign you in, please provide your email, zipcode and agree to our use terms of use.'
        session['splashMsg'] = splashMsg
        session.save()

        return render("/derived/twitterSignUp.bootstrap")

    def twitterSigningUp( self ):
        log.info("register:twitterSigningUp signing up with twt")
        """ handles creating an account for a twitter user who does not have one on the site """
        # I need the facebook identity stuff - load these things into the session when this process
        # happens

        """ Handler for registration, validates """
        returnPage = "/signup"
        name = False
        postalCode = False
        log.info('postalCode1 expect false: %s'%postalCode)
        checkTOS = False
        c.title = c.heading = "Registration"
        splashMsg = {}
        splashMsg['type'] = 'error'
        splashMsg['title'] = 'Error'
        #if  'password' not in request.params:
        #    log.info('password missing')
        #else:
        #    password = request.params['password']
        #if  'password2' not in request.params:
        #    log.info('password2 missing')
        #else:
        #    password2 = request.params['password2']
        if 'guestCode' in session and 'workshopCode' in session and 'workshopCode' in request.params:
            workshopCode = request.params['workshopCode']
            pmember = getPrivateMemberByCode(session['guestCode'])
            if pmember and pmember['workshopCode'] == workshopCode:
                email = pmember['email']
                log.info('got pmember email %s '%email)
                returnPage = "/derived/6_guest_signup.bootstrap"
                c.w = getWorkshopByCode(workshopCode)
                if 'addItem' in request.params:
                    c.listingType = request.params['addItem']
        else:
            if  'email' not in request.params:
                log.info('email missing')
            else:
                email = request.params['email']
                if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    log.info('invalid email %s'%email)

        if  'postalCode' not in request.params:
            log.info('postalCode missing')
        else:
            postalCode = request.params['postalCode']
            log.info('postalCode2 expect number: %s'%postalCode)
        if  'country' not in request.params:
            log.info('country missing')
        else:
            country = request.params['country']
        if  'memberType' not in request.params:
            log.info('memberType missing')
        else:
            memberType = request.params['memberType']
        if  'twitterName' not in session:
            log.info('twitter name missing')
        else:
            name = session['twitterName']
        if  'chkTOS' not in request.params:
            log.info('chkTOS missing')
        else:
            checkTOS = request.params['chkTOS']

        schema = plaintextForm()
        try:
            namecheck = name.replace(' ', '')
            nameTst = schema.to_python(dict(username = namecheck))
        except formencode.Invalid, error:
            splashMsg['content'] = "Full name: Enter only letters, numbers, or _ (underscore)"
            session['splashMsg'] = splashMsg
            session.save()
            return redirect(returnPage)
        username = name
        maxChars = 200;
        errorFound = False;
        # These warnings should all be collected onto the stack, then at the end we should render the page
        if name and email and checkTOS:
            if len(name) > maxChars:
                name = name[:200]
            if len(email) > maxChars:
                log.info("Error: Long email")
                errorFound = True
                splashMsg['content'] = "Email can be " + unicode(maxChars) + " characters at most"
                session['splashMsg'] = splashMsg
                session.save()
            if postalCode:
                pInfo = getPostalInfo(postalCode)
                log.info('postalCode3 expect number after pInfo: %s'%postalCode)
                if pInfo == None:
                    log.info("Error: Bad Postal Code")
                    errorFound = True
                    splashMsg['content'] = "Invalid postal code"
                    session['splashMsg'] = splashMsg
                    session.save() 
            else: 
                log.info("Error: Bad Postal Code")
                errorFound = True
                splashMsg['content'] = "Invalid postal code"
                session['splashMsg'] = splashMsg
                session.save()
            if errorFound:
                return redirect(returnPage)
            username = name

            if 'twitterId' in session:
                twitterId = session['twitterId']
            else:
                splashMsg['content'] = "Some required info is missing from the twitter data."
                session['splashMsg'] = splashMsg
                session.save() 
                return redirect('/signup')
            
            user = getUserByTwitterId( twitterId )
            if not user:
                log.info("didnt find a twitter id")
                # this could be an active user that has just now tried auth'ing
                # with twitter. if we get a match on email, we add the twitter id and other info
                # to this account
                user = getUserByEmail( email )

            if user == False:
                log.info("register:twitterSigningUp didn't find user, making new account")
                # NOTE - generate password here.
                #password = RegisterController.generatePassword()
                from string import letters, digits
                from random import choice
                pool, size = letters + digits, 11
                hash =  ''.join([choice(pool) for i in range(size)])
                password = hash.lower()
                # if they are a guest signing up, we will activate and log them in, externalAuthSignup=True 
                # skips sending an activation email
                log.info('postalCode4 expect number: %s'%postalCode)
                if c.w:
                    u = User(email, name, password, country, memberType, postalCode, externalAuthSignup=True)
                else:
                    u = User(email, name, password, country, memberType, postalCode)
                message = "The user '" + username + "' was created successfully!"
                c.success = True
                session['registerSuccess'] = True
                session.save()
                
                log.info( message )
                
                user = u.u
                log.info('postalCode6 expect number: %s'%user['postalCode'])
                if 'laston' in user:
                    t = time.localtime(float(user['laston']))
                    user['previous'] = time.strftime("%Y-%m-%d %H:%M:%S", t)
                # this will allow us to use the twitter api in their name
                user['twitter_oauth_token'] = session['twitter_oauth_token']
                user['twitter_oauth_secret'] = session['twitter_oauth_secret']
                user['externalAuthType'] = 'twitter'
                if 'twitterProfilePic' in session:
                    user['avatarSource'] = 'twitter'
                    user['twitterProfilePic'] = session['twitterProfilePic']                
                # mark this user as one who created the account originally by twitter signup
                user['originTwitter'] = u'1'

                if c.w:
                    log.info("c.w yes")
                    # if they are a guest signing up, activate and log them in
                    user['laston'] = time.time()
                    # add twitter userid to user
                    user['twitterAuthId'] = twitterId
                    user['activated'] = u'1'
                    loginTime = time.localtime(float(user['laston']))
                    loginTime = time.strftime("%Y-%m-%d %H:%M:%S", loginTime)
                    commit(user)
                    log.info('postalCode7 expect number: %s'%user['postalCode'])
                    splashMsg['type'] = 'success'
                    splashMsg['title'] = 'Success'
                    splashMsg['content'] = "You now have an identity to use on our site."
                    session['splashMsg'] = splashMsg
                    session["user"] = user['name']
                    session["userCode"] = user['urlCode']
                    session["userURL"] = user['url']
                    session.save()
                    log.info('session of user: %s' % session['user'])
                    log.info('%s logged in %s' % (user['name'], loginTime))
                    c.authuser = user
                    mailLib.sendWelcomeMail(user)

                    log.info( "guest activation via twitter - " + email )
                    returnPage = "/workshop/" + c.w['urlCode'] + "/" + c.w['url']
                    if c.listingType:
                        returnPage += "/add/" + c.listingType
                    return redirect(returnPage)
                else:
                    log.info("c.w no")
                    # not a guest, just a new twitter signup.
                    # add twitter userid to user
                    user['unactivatedTwitterAuthId'] = twitterId
                    user['activated'] = u'0'
                    commit(user)
                    log.info('postalCode8 expect number: %s'%user['postalCode'])
                    splashMsg['type'] = 'success'
                    splashMsg['title'] = 'Success'
                    splashMsg['content'] = "Check your email to finish setting up your account. If you don't see an email from us in your inbox, try checking your junk mail folder."
                    session['splashMsg'] = splashMsg
                    session.save()
                    log.info( "twitter signup with email - " + email )
                    return redirect(returnPage)
            else:
                log.info('user == true')
                # we have a match by email. because this is a manually provided email in this signup,
                # there are multiple cases to consider. One of the cases is that someone who doesn't own
                # this email tried to sign up and never was able to activate the account. 
                # person that already has an account on site, but hasn't
                # used the twitter auth to login yet
                # we need to activate parameters for this person's account
                # IF they know their password, and only if their account was originally
                # a normal account. If they've authenticated with facebook, for now they 
                # have made their choice. No need to auth with twitter as well.
                if 'originFacebook' in user.keys():
                    log.info('originFacebook')
                    # this email belongs to a user who has signed up already by facebook authentication
                    # we can allow linking of the twitter account if they verify ownership of this email.
                    # this is not a normal situation, this user is already activated, hence we need to 
                    # create an extra authentication route in order to handle this case.
                    if 'activatedFacebookNotTwitter' in user.keys():
                        log.info('activatedFacebookNotTwitter')
                        # user still needs to verify ownership of this email
                        # this is an unactivated account, initated via normal signup or twitter signup
                        splashMsg['content'] = "This account has not yet been activated. An email with information about activating your account has been sent. Check your junk mail folder if you don't see it in your inbox."
                        session['splashMsg'] = splashMsg
                        session.save()
                        baseURL = c.conf['activation.url']
                        url = '%s/activate/%s__%s'%(baseURL, user['activationFacebookNotTwitterHash'], user['email'])
                        mailLib.sendActivationMail(user['email'], url)
                        splashMsg['title'] = 'Success'
                        splashMsg['content'] = "Check your email to finish setting up your account. If you don't see an email from us in your inbox, try checking your junk mail folder."
                        session['splashMsg'] = splashMsg
                        session.save()
                        #log.info( "twitter signup with email - " + email )
                        return redirect(returnPage)
                    else:
                        log.info('else activatedFacebookNotTwitter')
                        user['unactivatedTwitterAuthId'] = twitterId
                        user['activatedFacebookNotTwitter'] = u'0'
                        commit(user)
                        log.info('postalCode9 expect number: %s'%user['postalCode'])
                        self.generateTwitterActivationHash(user)
                        splashMsg['type'] = 'success'
                        splashMsg['title'] = 'Success'
                        splashMsg['content'] = "Check your email to finish setting up your account. If you don't see an email from us in your inbox, try checking your junk mail folder."
                        session['splashMsg'] = splashMsg
                        session.save()
                        #log.info( "twitter signup with email - " + email )
                        return redirect(returnPage)
                log.info('after fb no twt')
                if user['activated'] == '1':
                    log.info('user activated')
                    c.email = email
                    session['twtEmail'] = email
                    session.save()
                    return render("/derived/twtLinkAccount.bootstrap")
                else:
                    log.info("unactivated user trying to sign up with twitter")
                    # this is an unactivated account, initated via normal signup or twitter signup
                    splashMsg['content'] = "This account has not yet been activated. An email with information about activating your account has been sent. Check your junk mail folder if you don't see it in your inbox."
                    session['splashMsg'] = splashMsg
                    session.save()
                    baseURL = c.conf['activation.url']
                    url = '%s/activate/%s__%s'%(baseURL, user['activationHash'], user['email'])
                    mailLib.sendActivationMail(user['email'], url)
        else:
            log.info("register:twitterSigningUp found user, required info is missing")
            splashMsg['content'] = "Some required info is missing from the twitter data."
            session['splashMsg'] = splashMsg
            session.save() 
   
        return redirect('/signup')

    def generateTwitterActivationHash(self, u):
        """Return a system generated hash for account activation"""
        log.info("generateTwitterActivationHash")
        from string import letters, digits
        from random import choice
        pool, size = letters + digits, 20
        hash =  ''.join([choice(pool) for i in range(size)])
        
        toEmail = u['email']
        frEmail = c.conf['activation.email']
        baseURL = c.conf['activation.url']
        url = '%s/activate/%s__%s'%(baseURL, hash, toEmail) 
        # this next line is needed for functional testing to be able to use the generated hash
        if 'paste.testing_variables' in request.environ:
                request.environ['paste.testing_variables']['hash_and_email'] = '%s__%s'%(hash, toEmail)
        
        u['activationFacebookNotTwitterHash'] = hash
        commit(u)
        Revision(u, u)
        
        # send the activation email
        mailLib.sendActivationMail(u['email'], url)
        
        log.info("Successful account creation (deactivated) for %s" %toEmail)

    def fbSigningUp( self ):
        log.info("register:fbSigningUp signing up with fb")
        """ handles creating an account for a facebook user who does not have one on the site """
        # I need the facebook identity stuff - load these things into the session when this process
        # happens

        """ Handler for registration, validates """
        returnPage = "/signup"
        name = False
        postalCode = False
        checkTOS = False
        c.title = c.heading = "Registration"
        splashMsg = {}
        splashMsg['type'] = 'error'
        splashMsg['title'] = 'Error'
        #if  'password' not in request.params:
        #    log.info('password missing')
        #else:
        #    password = request.params['password']
        #if  'password2' not in request.params:
        #    log.info('password2 missing')
        #else:
        #    password2 = request.params['password2']
        if 'guestCode' in session and 'workshopCode' in session and 'workshopCode' in request.params:
            workshopCode = request.params['workshopCode']
            pmember = getPrivateMemberByCode(session['guestCode'])
            if pmember and pmember['workshopCode'] == workshopCode:
                email = pmember['email']
                log.info('got pmember email %s '%email)
                returnPage = "/derived/6_guest_signup.bootstrap"
                c.w = getWorkshopByCode(workshopCode)
                if 'addItem' in request.params:
                    c.listingType = request.params['addItem']
        else:
            if 'fbEmail' not in session:
                log.info('facebook email missing')
            else:
                email = session['fbEmail']
                if utils.badEmail(email):
                    # simple is best, this next line is what was here
                    # if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    # invalid email, could be the 'undefined' case
                    # we'll make a unique email for this user
                    if 'facebookAuthId' in session:
                        email = "%s@%s.com"%(session['facebookAuthId'],session['facebookAuthId'])
                        log.info("created email %s"%email)
                    else:
                        splashMsg['content'] = "Some required info is missing from the facebook data."
                        session['splashMsg'] = splashMsg
                        session.save() 
                        return redirect('/signup')

        if  'postalCode' not in request.params:
            log.info('postalCode missing')
        else:
            postalCode = request.params['postalCode']
        if  'country' not in request.params:
            log.info('country missing')
        else:
            country = request.params['country']
        if  'memberType' not in request.params:
            log.info('memberType missing')
        else:
            memberType = request.params['memberType']
        if  'fbName' not in session:
            log.info('facebook name missing')
        else:
            name = session['fbName']
        if  'chkTOS' not in request.params:
            log.info('chkTOS missing')
        else:
            checkTOS = request.params['chkTOS']

        schema = plaintextForm()
        try:
            namecheck = name.replace(' ', '')
            nameTst = schema.to_python(dict(username = namecheck))
        except formencode.Invalid, error:
            splashMsg['content'] = "Full name: Enter only letters, numbers, or _ (underscore)"
            session['splashMsg'] = splashMsg
            session.save()
            return redirect(returnPage)
        username = name
        maxChars = 50;
        errorFound = False;
        # These warnings should all be collected onto the stack, then at the end we should render the page
        if name and email and checkTOS:
            if len(name) > maxChars:
                name = name[:50]
            if len(email) > maxChars:
                log.info("Error: Long email")
                errorFound = True
                splashMsg['content'] = "Email can be " + unicode(maxChars) + " characters at most"
                session['splashMsg'] = splashMsg
                session.save()
            if postalCode:
                pInfo = getPostalInfo(postalCode)
                if pInfo == None:
                    log.info("Error: Bad Postal Code")
                    errorFound = True
                    splashMsg['content'] = "Invalid postal code"
                    session['splashMsg'] = splashMsg
                    session.save() 
            else: 
                log.info("Error: Bad Postal Code")
                errorFound = True
                splashMsg['content'] = "Invalid postal code"
                session['splashMsg'] = splashMsg
                session.save()
            if errorFound:
                return redirect(returnPage)
            username = name
            if 'facebookAuthId' in session:
                facebookAuthId = session['facebookAuthId']
            else:
                splashMsg['content'] = "Some required info is missing from the facebook data."
                session['splashMsg'] = splashMsg
                session.save() 
                return redirect('/signup')
            
            user = getUserByFacebookAuthId( facebookAuthId )
            if not user:
                log.info("did not find by fb id")
                user = getUserByEmail( email )



            if user == False:
                log.info("register:fbSigningUp didn't find user, making new account")
                # NOTE - generate password here.
                #password = RegisterController.generatePassword()
                from string import letters, digits
                from random import choice
                pool, size = letters + digits, 11
                hash =  ''.join([choice(pool) for i in range(size)])
                password = hash.lower()
                u = User(email, name, password, country, memberType, postalCode, externalAuthSignup=True)
                message = "The user '" + username + "' was created successfully!"
                c.success = True
                session['registerSuccess'] = True
                session.save()
                
                log.info( message )
                splashMsg['type'] = 'success'
                splashMsg['title'] = 'Success'
                splashMsg['content'] = "You now have an identity to use on our site."
                session['splashMsg'] = splashMsg
                session.save()

                user = u.u
                if 'laston' in user:
                    t = time.localtime(float(user['laston']))
                    user['previous'] = time.strftime("%Y-%m-%d %H:%M:%S", t)
                
                # add facebook userid to user
                user['facebookAuthId'] = facebookAuthId
                # this will allow us to use the facebook api in their name
                user['facebookAccessToken'] = session['fbAccessToken']
                user['externalAuthType'] = 'facebook'
                # a user's account email can be different from the email on their facebook account.
                # we should keep track of this, it'll be handy
                user['fbEmail'] = email
                if 'fbSmallPic' in session:
                    user['avatarSource'] = 'facebook'
                    user['facebookProfileSmall'] = session['fbSmallPic']
                    user['facebookProfileBig'] = session['fbBigPic']
                
                user['laston'] = time.time()
                user['activated'] = u'1'
                # mark this user as one who created the account originally by twitter signup
                user['originFacebook'] = u'1'
                loginTime = time.localtime(float(user['laston']))
                loginTime = time.strftime("%Y-%m-%d %H:%M:%S", loginTime)
                commit(user)
                session["user"] = user['name']
                session["userCode"] = user['urlCode']
                session["userURL"] = user['url']
                session.save()
                log.info('session of user: %s' % session['user'])
                log.info('%s logged in %s' % (user['name'], loginTime))
                c.authuser = user
                mailLib.sendWelcomeMail(user)
                if c.w:
                    # if they are a guest signing up, activate and log them in
                    log.info( "Successful guest activation via facebook - " + email )
                    returnPage = "/workshop/" + c.w['urlCode'] + "/" + c.w['url']
                    if c.listingType:
                        returnPage += "/add/" + c.listingType
                    return redirect(returnPage)
                else:
                    # not a guest, just a new faceboook signup. activate and login
                    log.info( "Successful facebook signup with email - " + email )
                    returnPage = "/"
                    return redirect(returnPage)
            else:
                log.info("found user")
                # NOTE this used to only be a case where a user on site has now tried logging in with
                # the facebook button. Now, however, we can arrive here if an account was created with 
                # twitter, but not activated
                if 'unactivatedTwitterAuthId' in user.keys():
                    log.info("unactivatedTwitterAuthId")
                    if 'originTwitter' in user.keys():
                        log.info("originTwitter")
                        user['name'] = name
                        user['email'] = email
                        user['postalCode'] = postalCode
                        # add facebook userid to user
                        user['facebookAuthId'] = facebookAuthId
                        # this will allow us to use the facebook api in their name
                        user['facebookAccessToken'] = session['fbAccessToken']
                        user['externalAuthType'] = 'facebook'
                        # a user's account email can be different from the email on their facebook account.
                        # we should keep track of this, it'll be handy
                        user['fbEmail'] = email
                        if 'fbSmallPic' in session:
                            user['avatarSource'] = 'facebook'
                            user['facebookProfileSmall'] = session['fbSmallPic']
                            user['facebookProfileBig'] = session['fbBigPic']
                        
                        user['laston'] = time.time()
                        user['activated'] = u'1'
                        loginTime = time.localtime(float(user['laston']))
                        loginTime = time.strftime("%Y-%m-%d %H:%M:%S", loginTime)
                        commit(user)
                        session["user"] = user['name']
                        session["userCode"] = user['urlCode']
                        session["userURL"] = user['url']
                        session.save()
                        log.info('session of user: %s' % session['user'])
                        log.info('%s logged in %s' % (user['name'], loginTime))
                        c.authuser = user
                        if c.w:
                            log.info("c.w")
                            log.info( "Successful guest activation with credentials - " + email )
                            returnPage = "/workshop/" + c.w['urlCode'] + "/" + c.w['url']
                            if c.listingType:
                                returnPage += "/add/" + c.listingType
                            return redirect(returnPage)
                        else:
                            log.info("no c.w")
                            log.info( "Successful facebook signup with email - " + email )
                            returnPage = "/"
                            return redirect(returnPage)
                log.info("register:fbSigningUp found user, should have been logged in")
                splashMsg['content'] = "You should have been logged in already"
                session['splashMsg'] = splashMsg
                session.save() 
        else:
            log.info("register:fbSigningUp found user, required info is missing")
            splashMsg['content'] = "Some required info is missing from the facebook data."
            session['splashMsg'] = splashMsg
            session.save() 
   
        return redirect('/signup')

    def signupHandler( self ):
        """ Handler for registration, validates 
        JSON responses:
            statusCode == 0:    Same as unix exit code (OK)
            statusCode == 1:    No query was submitted
            statusCode == 2:    Query submitted, no results found
            result:             user's email and password are valid, session data returned?
        """
        log.info("in signup handler")

        try:
            useJson = request.params['json']
            if useJson == '1':
                returnJson = True
            else:
                returnJson = False
        except KeyError:
            returnJson = False

        returnPage = "/signup"
        if 'afterLoginURL' in session:
        # look for accelerator cases: workshop home, item listing, item home
            returnPage = session['afterLoginURL']
            if 'loginResetPassword' in returnPage:
                returnPage = '/profile/' + user['urlCode'] + '/' + user['url'] + '/edit#tab4'
                session.pop('afterLoginURL')
                session.save()
        name = False
        password = False
        postalCode = False
        checkTOS = False
        c.title = c.heading = "Registration"
        splashMsg = {}
        splashMsg['type'] = 'error'
        splashMsg['title'] = 'Error'
        if  'password' not in request.params:
            log.info('password missing')
        else:
            password = request.params['password']
        if 'guestCode' in session and 'workshopCode' in session and 'workshopCode' in request.params:
            workshopCode = request.params['workshopCode']
            pmember = getPrivateMemberByCode(session['guestCode'])
            if pmember and pmember['workshopCode'] == workshopCode:
                email = pmember['email']
                log.info('got pmember email %s '%email)
                returnPage = "/derived/6_guest_signup.bootstrap"
                c.w = getWorkshopByCode(workshopCode)
                if 'addItem' in request.params:
                    c.listingType = request.params['addItem']
        else:
            if  'email' not in request.params:
                log.info('email missing')
            else:
                email = request.params['email']
        if  'postalCode' not in request.params:
            log.info('postalCode missing')
        else:
            postalCode = request.params['postalCode']
        if  'country' not in request.params:
            log.info('country missing')
        else:
            country = request.params['country']
        if  'memberType' not in request.params:
            log.info('memberType missing')
        else:
            memberType = request.params['memberType']
        if  'name' not in request.params:
            log.info('name missing')
        else:
            name = request.params['name']
        if  'chkTOS' not in request.params:
            log.info('chkTOS missing')
        else:
            checkTOS = request.params['chkTOS']

        schema = plaintextForm()
        try:
            namecheck = name.replace(' ', '')
            nameTst = schema.to_python(dict(username = namecheck))
        except formencode.Invalid, error:
            splashMsg['content'] = "Full name: Enter only letters, numbers, or _ (underscore)"
            session['splashMsg'] = splashMsg
            session.save()
            if returnJson:
                response.headers['Content-type'] = 'application/json'
                return json.dumps({'statusCode':2, 'message':'Full name: Enter only letters, numbers, or _ (underscore)'})
            else:
                return redirect(returnPage)
        username = name
        maxChars = 50;
        errorFound = False;
        # These warnings should all be collected onto the stack, then at the end we should render the page
        if name and password and email and checkTOS:
            if len(name) > maxChars:
                name = name[:50]
            if len(email) > maxChars:
                log.info("Error: Long email")
                errorFound = True
                splashMsg['content'] = "Email can be " + unicode(maxChars) + " characters at most"
                session['splashMsg'] = splashMsg
                session.save()
            if len(password) > maxChars:
                log.info("Error: Long password")
                errorFound = True
                splashMsg['content'] = "Password can be " + unicode(maxChars) + " characters at most"
                session['splashMsg'] = splashMsg
                session.save() 
            if postalCode:
                pInfo = getPostalInfo(postalCode)
                if pInfo == None:
                    log.info("Error: Bad Postal Code")
                    errorFound = True
                    splashMsg['content'] = "Invalid postal code"
                    session['splashMsg'] = splashMsg
                    session.save() 
            else: 
                log.info("Error: Bad Postal Code")
                errorFound = True
                splashMsg['content'] = "Invalid postal code"
                session['splashMsg'] = splashMsg
                session.save()
            if errorFound:
                if returnJson:
                    response.headers['Content-type'] = 'application/json'
                    return json.dumps({'statusCode':2, 'message':splashMsg['content']})
                else:
                    return redirect(returnPage)
            username = name
            user = getUserByEmail( email )
            if user == False:
                if password:
                    u = User(email, name, password, country, memberType, postalCode)
                    message = "The user '" + username + "' was created successfully!"
                    c.success = True
                    session['registerSuccess'] = True
                    session.save()
                    
                    #log.info( message )
                    #splashMsg['type'] = 'success'
                    #splashMsg['title'] = 'Success'
                    #splashMsg['content'] = "Check your email to finish setting up your account. If you don't see an email from us in your inbox, try checking your junk mail folder."
                    #session['splashMsg'] = splashMsg
                    #session.save()
                    
                    user = u.u
                    if 'laston' in user:
                        t = time.localtime(float(user['laston']))
                        user['previous'] = time.strftime("%Y-%m-%d %H:%M:%S", t)
                            
                    user['laston'] = time.time()
                    #user['activated'] = u'1'
                    loginTime = time.localtime(float(user['laston']))
                    loginTime = time.strftime("%Y-%m-%d %H:%M:%S", loginTime)
                    commit(user)
                    session["user"] = user['name']
                    session["userCode"] = user['urlCode']
                    session["userURL"] = user['url']
                    session.save()
                    log.info('session of user: %s' % session['user'])
                    log.info('%s logged in %s' % (user['name'], loginTime))
                    c.authuser = user
                    
                    # set up their session for the feeds
                    session['listenerWorkshops'] = [] 
                    session['bookmarkedWorkshops'] = [] 
                    session['privateWorkshops'] = []
                    session['facilitatorWorkshops'] = []
                    session['facilitatorInitiatives'] = []
                    session['bookmarkedInitiatives'] = []
                    session['followingUsers'] = []
                    session.save()
                        
                    # if they are a guest signing up, activate them   
                    if c.w:
                        user['activated'] = u'1'
                        commit(user)
                        log.info( "Successful guest activation with credentials - " + email )
                        
                        returnPage = "/workshop/" + c.w['urlCode'] + "/" + c.w['url']
                        if c.listingType:
                            returnPage += "/add/" + c.listingType
                        if returnJson:
                            response.headers['Content-type'] = 'application/json'
                            return json.dumps({'statusCode':0, 'user':dict(user)})
                        else:
                            return redirect(returnPage)
                            
                    returnPage = "/"
                    
                    if 'afterLoginURL' in session:
                    # look for accelerator cases: workshop home, item listing, item home
                        returnPage = session['afterLoginURL']
                        if 'loginResetPassword' in returnPage:
                            returnPage = '/profile/' + user['urlCode'] + '/' + user['url'] + '/edit#tab4'
                            session.pop('afterLoginURL')
                            session.save()
                    
                    if returnJson:
                        response.headers['Content-type'] = 'application/json'
                        return json.dumps({'statusCode':0, 'user':dict(u.u)})
                    else:
                        return redirect(returnPage)
                else:
                    splashMsg['content'] = "You need a password"
                    session['splashMsg'] = splashMsg
                    session.save() 
            else:
                # If they've registered using external authentication, they cannot add a password
                # by registering in this way - unless it is an unactivated account
                if user['activated'] == '0':
                    splashMsg['content'] = "This account has not yet been activated. An email with information about activating your account has been sent. Check your junk mail folder if you don't see it in your inbox."
                    session['splashMsg'] = splashMsg
                    session.save()
                    baseURL = c.conf['activation.url']
                    url = '%s/activate/%s__%s'%(baseURL, user['activationHash'], user['email'])
                    mailLib.sendActivationMail(user['email'], url)
                    if returnJson:
                        response.headers['Content-type'] = 'application/json'
                        return json.dumps({'statusCode':2, 'message':"This account has not yet been activated. An email with information about activating your account has been sent. Check your junk mail folder if you don't see it in your inbox."})
                else:
                    splashMsg['content'] = "The email '" + email + "' is already in use. If you own this account, try Log in or Forgot password."
                    session['splashMsg'] = splashMsg
                    session.save()
                    if returnJson:
                        response.headers['Content-type'] = 'application/json'
                        return json.dumps({'statusCode':2, 'message':'This email is already in use.'})
        else:
            splashMsg['content'] = "Please fill all fields"
            session['splashMsg'] = splashMsg
            session.save()
            if returnJson:
                response.headers['Content-type'] = 'application/json'
                return json.dumps({'statusCode':2, 'message':'Please fill all fields'})
        if returnJson:
            response.headers['Content-type'] = 'application/json'
            return json.dumps({'statusCode':2, 'message':splashMsg['content']})
        else:
            return redirect('/signup')

    def generateHash(self, *length):
        """Return a system generated hash for randomization of user params"""
        from string import letters, digits
        from random import choice
        pool, size = letters + digits, length or 10
        hash =  ''.join([choice(pool) for i in range(size)])
        return hash.lower()