# -*- coding: utf-8 -*-
import logging, formencode

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons import config

from pylowiki.lib.base import BaseController, render
import pylowiki.lib.helpers as h

from pylowiki.lib.db.user import User, getUserByEmail, getActiveUsers
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

    
    #def index( self ):
    #    """ Display Registration Form """
    #    return render("/derived/signup.bootstrap")
    

    def signupDisplay(self):
        c.numAccounts = 1000
        c.numUsers = len(getActiveUsers())
        return render("/derived/signup.bootstrap")

    def register_handler( self ):
        c.numAccounts = 1000
        c.numUsers = len(getActiveUsers())

        if c.numUsers >= c.numAccounts:
            c.splashMsg = {}
            c.splashMsg['type'] = 'error'
            c.splashMsg['title'] = 'Error:'
            c.splashMsg['content'] = 'Site at capacity!  We will be increasing the capacity in the coming weeks.'
            return render('/derived/signup.bootstrap')

        """ Handler for registration, validates """
        name = False
        password = False
        password2 = False
        postalCode = False
        checkTOS = False
        c.title = c.heading = "Registration"
        c.splashMsg = False
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
            splashMsg['content'] = "Error: " + unicode(error)
            c.splashMsg = splashMsg 
            return render('/derived/signup.bootstrap')
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
                c.splashMsg = splashMsg 
            if len(password) > maxChars:
                log.info("Error: Long password")
                errorFound = True
                splashMsg['content'] = "Password can be " + unicode(maxChars) + " characters at most"
                c.splashMsg = splashMsg 
            if postalCode:
                pInfo = getPostalInfo(postalCode)
                if pInfo == None:
                    log.info("Error: Bad Postal Code")
                    errorFound = True
                    splashMsg['content'] = "Invalid postal code"
                    c.splashMsg = splashMsg 
            else: 
                log.info("Error: Bad Postal Code")
                errorFound = True
                splashMsg['content'] = "Invalid postal code"
                c.splashMsg = splashMsg 
            if errorFound:
                return render('/derived/signup.bootstrap')
            username = name
            if getUserByEmail( email ) == False:
                if password == password2:
                    u = User(email, name, password, country, memberType, postalCode)
                    message = "The user '" + username + "' was created successfully!"
                                
                    log.info( message )
                    splashMsg['type'] = 'success'
                    splashMsg['title'] = 'Success'
                    splashMsg['content'] = 'Check your email to finish setting up your account'
                    c.splashMsg = splashMsg
                      
                    return render('/derived/signup.bootstrap')
                else:
                    splashMsg['content'] = "The password and confirmation do not match"
                    c.splashMsg = splashMsg 
            else:
                splashMsg['content'] = "The email '" + email + "' is already in use"
                c.splashMsg = splashMsg 
        else:
            splashMsg['content'] = "Please fill all fields"
            c.splashMsg = splashMsg 
   
        return render('/derived/signup.bootstrap')
