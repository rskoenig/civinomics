# -*- coding: utf-8 -*-
import logging, formencode, time

from formencode.schema import Schema
from formencode.validators import Invalid, FancyValidator

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons import config

from pylowiki.lib.base import BaseController, render
import pylowiki.lib.helpers as h

from pylowiki.lib.db.user import User, getUserByEmail, getUserByFacebookAuthId, getActiveUsers, getUserByTwitterId
from pylowiki.lib.db.pmember import getPrivateMemberByCode
from pylowiki.lib.db.workshop import getWorkshopByCode, setWorkshopPrivs
from pylowiki.lib.db.geoInfo import getPostalInfo
from pylowiki.lib.db.dbHelpers import commit
import pylowiki.lib.db.mainImage    as mainImageLib
import pylowiki.lib.mail            as mailLib
import re

log = logging.getLogger(__name__)

class plaintextForm(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    username = formencode.validators.PlainText(not_empty=True)
    log.info("made it here")
    #username = SecurePassword()
    log.info("and here")

class RegisterController(BaseController):

    def __before__(self):
        if config['app_conf']['public.reg'] != "true": # set in enviroment config
            h.check_if_login_required()

    def apostropheInNameOk(self, name):
        """This is a replacement checker function for the plaintextForm above. This 
        one allows apostrophes ( ' )"""
        not_ok_letters = 0
        nameRegex = re.compile("^([A-Za-z0-9-'_\s])+$", re.IGNORECASE)        
        notOk_letters = nameRegex.sub('', name)
        # If there are any characters in notOk_letters, that means there are chars outside
        # of what are defined as ok by the nameRegex variable, and we are not ok with that.
        if len(notOk_letters) == 0:
            return True
        else:
            return False

    def signupDisplay(self):
        c.facebookAppId = config['facebook.appid']
        c.channelUrl = config['facebook.channelUrl']

        c.numAccounts = 1000
        c.numUsers = len(getActiveUsers())
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
            
        return render("/derived/signup.bootstrap")

    def signupNoExtAuthDisplay(self):

        # todo - clear splash message if this came from /fbSignUp

        c.numAccounts = 1000
        c.numUsers = len(getActiveUsers())
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
        c.facebookAppId = config['facebook.appid']
        c.channelUrl = config['facebook.channelUrl']

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

    def generatePassword(*length):
        """Return a system generated hash for randomization of user params"""
        from string import letters, digits
        from random import choice
        pool, size = letters + digits, length or 10
        hash =  ''.join([choice(pool) for i in range(size)])
        return hash.lower()

    def fbSignUpDisplay( self ):
        """ This is an intermediary page for the signup process when a facebook user first
        creates an account. """
        c.numAccounts = 1000
        c.numUsers = len(getActiveUsers())

        if c.numUsers >= c.numAccounts:
            splashMsg = {}
            splashMsg['type'] = 'error'
            splashMsg['title'] = 'Error:'
            splashMsg['content'] = 'Sorry, our website has reached capacity!  We will be increasing the capacity in the coming weeks.'
            session['splashMsg'] = splashMsg
            session.save()
            return redirect('/')

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
        c.numAccounts = 1000
        c.numUsers = len(getActiveUsers())

        if c.numUsers >= c.numAccounts:
            splashMsg = {}
            splashMsg['type'] = 'error'
            splashMsg['title'] = 'Error:'
            splashMsg['content'] = 'Sorry, our website has reached capacity!  We will be increasing the capacity in the coming weeks.'
            session['splashMsg'] = splashMsg
            session.save()
            return redirect('/')

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
        c.numAccounts = 1000
        c.numUsers = len(getActiveUsers())

        if c.numUsers >= c.numAccounts:
            splashMsg = {}
            splashMsg['type'] = 'error'
            splashMsg['title'] = 'Error:'
            splashMsg['content'] = 'Sorry, our website has reached capacity!  We will be increasing the capacity in the coming weeks.'
            session['splashMsg'] = splashMsg
            session.save()
            return redirect('/')

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

        isNameClean = RegisterController.apostropheInNameOk(self, name)
        if not isNameClean:
            splashMsg['content'] = "Full name: Enter only letters, numbers, ' or _ (underscore)"
            session['splashMsg'] = splashMsg
            session.save()
            return redirect(returnPage)
        #  if there are any 's, replace the ' with &#39 for storage in the db
        name = utils.safeApostrophe(name)

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
                if c.w:
                    u = User(email, name, password, country, memberType, postalCode, externalAuthSignup=True)
                else:
                    u = User(email, name, password, country, memberType, postalCode)
                message = "The user '" + username + "' was created successfully!"
                c.success = True
                session['registerSuccess'] = True
                session.save()
                
                log.info( message )
                
                # if they are a guest signing up, activate and log them in
                if c.w:
                    user = u.u
                    if 'laston' in user:
                        t = time.localtime(float(user['laston']))
                        user['previous'] = time.strftime("%Y-%m-%d %H:%M:%S", t)

                    # add twitter userid to user
                    user['twitterAuthId'] = twitterId
                    # this will allow us to use the twitter api in their name
                    user['twitter_oauth_token'] = session['twitter_oauth_token']
                    user['twitter_oauth_secret'] = session['twitter_oauth_secret']
                    user['externalAuthType'] = 'twitter'
                    
                    if 'twitterProfilePic' in session:
                        user['avatarSource'] = 'twitter'
                        user['twitterProfilePic'] = session['twitterProfilePic']
                    
                    user['laston'] = time.time()
                    user['activated'] = u'1'
                    loginTime = time.localtime(float(user['laston']))
                    loginTime = time.strftime("%Y-%m-%d %H:%M:%S", loginTime)
                    commit(user)
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
                    
                    log.info( "Successful guest activation with credentials - " + email )
                    returnPage = "/workshop/" + c.w['urlCode'] + "/" + c.w['url']
                    if c.listingType:
                        returnPage += "/add/" + c.listingType
                    return redirect(returnPage)
                else:
                    # not a guest, simply a new twitter signup,
                    # we are sending this person an activation email - this is
                    # because twitter does not give us the email of this user so
                    # we have to ask for it, and confirm
                    user = u.u
                    if 'laston' in user:
                        t = time.localtime(float(user['laston']))
                        user['previous'] = time.strftime("%Y-%m-%d %H:%M:%S", t)

                    # add twitter userid to user
                    user['unactivatedTwitterAuthId'] = twitterId
                    # this will allow us to use the twitter api in their name
                    user['twitter_oauth_token'] = session['twitter_oauth_token']
                    user['twitter_oauth_secret'] = session['twitter_oauth_secret']
                    user['externalAuthType'] = 'twitter'
                    
                    if 'twitterProfilePic' in session:
                        user['avatarSource'] = 'twitter'
                        user['twitterProfilePic'] = session['twitterProfilePic']
                    #user['laston'] = time.time()
                    user['activated'] = u'0'
                    #loginTime = time.localtime(float(user['laston']))
                    #loginTime = time.strftime("%Y-%m-%d %H:%M:%S", loginTime)
                    commit(user)
                    #session["user"] = user['name']
                    #session["userCode"] = user['urlCode']
                    #session["userURL"] = user['url']
                    #session.save()
                    splashMsg['type'] = 'success'
                    splashMsg['title'] = 'Success'
                    splashMsg['content'] = "Check your email to finish setting up your account. If you don't see an email from us in your inbox, try checking your junk mail folder."
                    session['splashMsg'] = splashMsg
                    session.save()
                    #log.info('session of user: %s' % session['user'])
                    #log.info('%s logged in %s' % (user['name'], loginTime))
                    #c.authuser = user
                    #mailLib.sendWelcomeMail(user)
                    #log.info( "Successful twitter signup with email - " + email )
                    return redirect(returnPage)
            else:
                # we have a match by email. because this is a manually provided email in this signup,
                # there are multiple cases to consider. One of the cases is that someone who doesn't own
                # this email tried to sign up and never was able to activate the account. 
                # person that already has an account on site, but hasn't
                # used the twitter auth to login yet
                # we need to activate parameters for this person's account
                # IF they know their password, and only if their account was originally
                # a normal account. If they've authenticated with facebook, for now they 
                # have made their choice. No need to auth with twitter as well.
                if 'facebookAuthId' in user.keys():
                    log.info("user who auths with facebook now wants to auth with twitter. not allowed at this point.")
                    splashMsg['content'] = ", we cannot allow you to login using twitter authentication since you do so with your facebook account already."
                    session['splashMsg'] = splashMsg
                    session.save()
                    return redirect('/login')
                if user['activated'] == '1':
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

    def fbSigningUp( self ):
        log.info("register:fbSigningUp signing up with fb")
        """ handles creating an account for a facebook user who does not have one on the site """
        # I need the facebook identity stuff - load these things into the session when this process
        # happens
        c.numAccounts = 1000
        c.numUsers = len(getActiveUsers())

        if c.numUsers >= c.numAccounts:
            splashMsg = {}
            splashMsg['type'] = 'error'
            splashMsg['title'] = 'Error:'
            splashMsg['content'] = 'Sorry, our website has reached capacity!  We will be increasing the capacity in the coming weeks.'
            session['splashMsg'] = splashMsg
            session.save()
            return redirect('/')

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
                if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    # invalid email, could be the 'undefined' case
                    # we'll make a unique email for this user
                    email = "%s@%s.com"%(session['facebookAuthId'],session['facebookAuthId'])
                    log.info("created email %s"%email)

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

        isNameClean = RegisterController.apostropheInNameOk(self, name)
        if not isNameClean:
            splashMsg['content'] = "Full name: Enter only letters, numbers, ' or _ (underscore)"
            session['splashMsg'] = splashMsg
            session.save()
            return redirect(returnPage)
        #  if there are any 's, replace the ' with &#39 for storage in the db
        name = utils.safeApostrophe(name)

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

                # if they are a guest signing up, activate and log them in
                if c.w:
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
                    
                    log.info( "Successful guest activation with credentials - " + email )
                    returnPage = "/workshop/" + c.w['urlCode'] + "/" + c.w['url']
                    if c.listingType:
                        returnPage += "/add/" + c.listingType
                    return redirect(returnPage)
                else:
                    # not a guest, just a new faceboook signup. activate and login
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
                    #user['facebookProfileBig'] = session['fbBigPic']
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
                    mailLib.sendWelcomeMail(user)
                    
                    log.info( "Successful facebook signup with email - " + email )
                    returnPage = "/"
                    return redirect(returnPage)
            else:
                # NOTE this is a case where a user on site has now tried logging in with
                # the facebook button. This should be caught in controllers/login.fbAuthCheckEmail
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
        log.info("in signup handler")
        c.numAccounts = 1000
        c.numUsers = len(getActiveUsers())

        if c.numUsers >= c.numAccounts:
            splashMsg = {}
            splashMsg['type'] = 'error'
            splashMsg['title'] = 'Error:'
            splashMsg['content'] = 'Site at capacity!  We will be increasing the capacity in the coming weeks.'
            session['splashMsg'] = splashMsg
            session.save()
            return redirect('/signup')

        """ Handler for registration, validates """
        returnPage = "/signup"
        name = False
        password = False
        password2 = False
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
        if  'password2' not in request.params:
            log.info('password2 missing')
        else:
            password2 = request.params['password2']
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
        
        isNameClean = RegisterController.apostropheInNameOk(self, name)
        if not isNameClean:
            splashMsg['content'] = "Full name: Enter only letters, numbers, ' or _ (underscore)"
            session['splashMsg'] = splashMsg
            session.save()
            return redirect(returnPage)
        #  if there are any 's, replace the ' with &#39 for storage in the db
        name = utils.safeApostrophe(name)

        username = name
        maxChars = 50;
        errorFound = False;
        # These warnings should all be collected onto the stack, then at the end we should render the page
        if name and password and password2 and email and checkTOS:
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
                return redirect(returnPage)
            username = name
            user = getUserByEmail( email )
            if user == False:
                if password == password2:
                    u = User(email, name, password, country, memberType, postalCode)
                    message = "The user '" + username + "' was created successfully!"
                    c.success = True
                    session['registerSuccess'] = True
                    session.save()
                    
                    log.info( message )
                    splashMsg['type'] = 'success'
                    splashMsg['title'] = 'Success'
                    splashMsg['content'] = "Check your email to finish setting up your account. If you don't see an email from us in your inbox, try checking your junk mail folder."
                    session['splashMsg'] = splashMsg
                    session.save()
                    # if they are a guest signing up, activate and log them in
                    if c.w:
                        user = u.u
                        if 'laston' in user:
                            t = time.localtime(float(user['laston']))
                            user['previous'] = time.strftime("%Y-%m-%d %H:%M:%S", t)
                            
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
                        
                        log.info( "Successful guest activation with credentials - " + email )
                        returnPage = "/workshop/" + c.w['urlCode'] + "/" + c.w['url']
                        if c.listingType:
                            returnPage += "/add/" + c.listingType
                        return redirect(returnPage)
                        
                    return redirect(returnPage)
                else:
                    splashMsg['content'] = "The password and confirmation do not match"
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
                else:
                    splashMsg['content'] = "The email '" + email + "' is already in use"
                    session['splashMsg'] = splashMsg
                    session.save()
        else:
            splashMsg['content'] = "Please fill all fields"
            session['splashMsg'] = splashMsg
            session.save() 
   
        return redirect('/signup')
