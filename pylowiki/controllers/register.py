# -*- coding: utf-8 -*-
import logging, formencode, time

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons import config

from pylowiki.lib.base import BaseController, render
import pylowiki.lib.helpers as h

from pylowiki.lib.db.user import User, getUserByEmail, getActiveUsers
from pylowiki.lib.db.pmember import getPrivateMemberByCode
from pylowiki.lib.db.workshop import getWorkshopByCode, setWorkshopPrivs
from pylowiki.lib.db.geoInfo import getPostalInfo
from pylowiki.lib.db.dbHelpers import commit
import pylowiki.lib.db.mainImage    as mainImageLib

log = logging.getLogger(__name__)

class plaintextForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    username = formencode.validators.PlainText(not_empty=True)

class RegisterController(BaseController):

    def __before__(self):
        if config['app_conf']['public.reg'] != "true": # set in enviroment config
            h.check_if_login_required()

    def signupDisplay(self):
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

    def fbSigningUp( self ):
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
            if getUserByEmail( email ) == False:
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
                splashMsg['content'] = "The email '" + email + "' is already in use"
                session['splashMsg'] = splashMsg
                session.save() 
        else:
            splashMsg['content'] = "Please fill all fields"
            session['splashMsg'] = splashMsg
            session.save() 
   
        return redirect('/signup')

    def signupHandler( self ):
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
            if getUserByEmail( email ) == False:
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
                splashMsg['content'] = "The email '" + email + "' is already in use"
                session['splashMsg'] = splashMsg
                session.save() 
        else:
            splashMsg['content'] = "Please fill all fields"
            session['splashMsg'] = splashMsg
            session.save() 
   
        return redirect('/signup')
