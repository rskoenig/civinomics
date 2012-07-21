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
                h.flash("Error: " + unicode(error), "warning")
                #return render("/derived/signup.html")
                return render('/derived/splash.html')
            try:
                nameTst = schema.to_python(dict(username = lastName))
            except formencode.Invalid, error:
                h.flash("Error: " + unicode(error), "warning")
                #return render("/derived/signup.html")
                return render('/derived/splash.html')
            username = "%s %s" %(firstName, lastName)
            maxChars = 50;
            errorFound = False;
            # These warnings should all be collected onto the stack, then at the end we should render the page
            if firstName and lastName and password and password2 and email and checkTOS:
                if len(firstName) > maxChars:
                    h.flash("Error: First name: First name can be " + unicode(maxChars) + " characters at most", "warning")
                    log.info("Error: Long first name")
                    errorFound = True
                if len(lastName) > maxChars:
                    h.flash("Error: Last name: Last name can me " + unicode(maxChars) + " characters at most", "warning")
                    log.info("Error: Long last name")
                    errorFound = True
                if len(email) > maxChars:
                    h.flash("Error: Email: Email can be " + unicode(maxChars) + " characters at most", "warning")
                    log.info("Error: Long email")
                    errorFound = True
                if len(password) > maxChars:
                    h.flash("Error: Password: Password can be " + unicode(maxChars) + " characters at most", "warning")
                    log.info("Error: Long password")
                    errorFound = True
                if postalCode:
                    pInfo = getPostalInfo(postalCode, 'United States')
                    if pInfo == None:
                        h.flash("Error: invalid postal code", "warning")
                        log.info("Error: Bad Postal Code password")
                        errorFound = True
                else: 
                    h.flash("Error: invalid postal code", "warning")
                    log.info("Error: Bad Postal Code password")
                    errorFound = True
                if errorFound:
                    #return render("/derived/signup.html")
                    return render('/derived/splash.html')
                username = "%s %s" %(firstName, lastName)
                if getUserByEmail( email ) == False:
                    if password == password2:
                        u = User(email, firstName, lastName, password, country, memberType, postalCode)
                        message = "The user '" + username + "' was created successfully!"
                                
                        log.info( message )
                        
                        session['popup'] = True
                        c.popper = {}
                        c.popper['leftTitle'] = 'SIGN UP'
                        c.popper['subject'] = 'Thank you for registering'
                        c.popper['message'] = 'Check your email to finish setting up your account'
                                
                        return render('/derived/splash.html')
                    else:
                        h.flash( "The password and confirmation do not match", "warning" )
                else:
                    h.flash( "The email '" + email + "' is already in use", "warning" )
            else:
                h.flash( "Please fill all fields", "warning" )
      
        except KeyError:
            if "user" in session:
                #return redirect( "/" )
                return render('/derived/splash.html')
            h.flash( "Please fill all fields.", "error" )
        #return render( "/derived/register.mako" )
        #return render("/derived/signup.html")
        return render('/derived/splash.html')
