# -*- coding: utf-8 -*-
import logging, formencode

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons import config

from pylowiki.lib.base import BaseController, render
import pylowiki.lib.helpers as h
#from pylowiki.lib.activate import activateCreate

#from pylowiki.model import User, commit, Event, get_user, get_user_by_email, Points
from pylowiki.lib.db.user import User, getUserByEmail
from pylowiki.lib.db.geoInfo import getPostalInfo
from pylowiki.lib.db.dbHelpers import commit

log = logging.getLogger(__name__)

class plaintextForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    username = formencode.validators.PlainText(not_empty=True)

class RegisterController(BaseController):

    def __before__(self):
        if config['app_conf']['public.reg'] != "true": # set in enviroment config
            h.check_if_login_required()

    def index( self ):
        """ Display Registration Form """
        c.title = c.heading = "Registration"
        #return render( "/derived/register.mako" )
        return render("/derived/signup.html")

    def register_handler( self ):
        """ Handler for registration, validates """
        c.title = c.heading = "Registration"
        c.splashMsg = False
        splashMsg = {}
        splashMsg['type'] = 'error'
        splashMsg['title'] = 'Error'
        try:
            
            #username = request.params['username'].lower()
            password = request.params['password']
            password2 = request.params['password2']
            email = request.params['email']
            postalCode = request.params['postalCode']
            country = request.params['country']
            memberType = request.params['memberType']
            firstName = request.params['firstName']
            lastName = request.params['lastName']
            checkTOS = request.params['chkTOS']

            schema = plaintextForm()
            try:
                nameTst = schema.to_python(dict(username = firstName))
            except formencode.Invalid, error:
                splashMsg['content'] = "Error: " + unicode(error)
                c.splashMsg = splashMsg 
                return render('/derived/splash.bootstrap')
            try:
                nameTst = schema.to_python(dict(username = lastName))
            except formencode.Invalid, error:
                splashMsg['content'] = "Error: " + unicode(error)
                c.splashMsg = splashMsg 
                return render('/derived/splash.bootstrap')
            username = "%s %s" %(firstName, lastName)
            maxChars = 50;
            errorFound = False;
            # These warnings should all be collected onto the stack, then at the end we should render the page
            if firstName and lastName and password and password2 and email and checkTOS:
                if len(firstName) > maxChars:
                    firstName = firstName[:50]
                if len(lastName) > maxChars:
                    lastName = lastName[:50]
                if len(email) > maxChars:
                    log.info("Error: Long email")
                    errorFound = True
                    splashMsg['content'] = "Email can be " + unicode(maxChars) + " characters at most"
                    c.splashMsg = splashMsg 
                if len(password) > maxChars:
                    log.info("Error: Long password")
                    errorFound = True
                    splashMsg['content'] = "Password can be " + unicode(maxChars) + " characters at most"
                    c.splashMsg = splashMsg 
                if postalCode:
                    pInfo = getPostalInfo(postalCode, 'United States')
                    if pInfo == None:
                        log.info("Error: Bad Postal Code password")
                        errorFound = True
                        splashMsg['content'] = "Invalid postal code"
                        c.splashMsg = splashMsg 
                else: 
                    log.info("Error: Bad Postal Code")
                    errorFound = True
                    splashMsg['content'] = "Invalid postal code"
                    c.splashMsg = splashMsg 
                if errorFound:
                    return render('/derived/splash.bootstrap')
                username = "%s %s" %(firstName, lastName)
                if getUserByEmail( email ) == False:
                    if password == password2:
                        u = User(email, firstName, lastName, password, country, memberType, postalCode)
                        message = "The user '" + username + "' was created successfully!"
                                
                        log.info( message )
                        splashMsg['type'] = 'success'
                        splashMsg['title'] = 'Success'
                        splashMsg['content'] = 'Check your email to finish setting up your account'
                        c.splashMsg = splashMsg
                        
                        return render('/derived/splash.bootstrap')
                    else:
                        splashMsg['content'] = "The password and confirmation do not match"
                        c.splashMsg = splashMsg 
                else:
                    splashMsg['content'] = "The email '" + email + "' is already in use"
                    c.splashMsg = splashMsg 
            else:
                splashMsg['content'] = "Please fill all fields"
                c.splashMsg = splashMsg 
      
        except KeyError:
            if "user" in session:
                return render('/derived/splash.bootstrap')
            splashMsg['content'] = "Please fill all fields"
            c.splashMsg = splashMsg 
        return render('/derived/splash.bootstrap')
