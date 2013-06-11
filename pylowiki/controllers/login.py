# -*- coding: utf-8 -*-
import logging, time

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import config

from pylowiki.lib.base import BaseController, render

import pylowiki.lib.helpers as h
import pylowiki.lib.db.user as userLib
import pylowiki.lib.mail as mailLib
from pylowiki.lib.auth import login_required
from pylowiki.lib.db.dbHelpers import commit

import requests
import mechanize

import base64
import hashlib
import hmac
import urllib2 as urllib2
import simplejson as json

log = logging.getLogger(__name__)

class LoginController(BaseController):

    def base64_url_decode(self, inp):
        padding_factor = (4 - len(inp) % 4) % 4
        inp += "="*padding_factor 
        return base64.b64decode(unicode(inp).translate(dict(zip(map(ord, u'-_'), u'+/'))))

    def verifyFbSignature(self, signed):
        encoded_sig, payload = signed.split('.')

        sig = LoginController.base64_url_decode(self, encoded_sig)
        data = json.loads(LoginController.base64_url_decode(self, payload))

        if data.get('algorithm').upper() != 'HMAC-SHA256':
            log.error('Unknown algorithm')
            return None
        else:
            expected_sig = hmac.new(config['facebook.secret'], msg=payload, digestmod=hashlib.sha256).digest()

        if sig != expected_sig:
            log.error('Invalid signature')
            return None
        #else:
            # we have signature verified data
            # return data

        for piece in data:
            log.info("signature key: %s" % piece)
            log.info("signature data: %s" % data[piece])

        return data

    def fbAuthCheckEmail(self, id1):
        # this receives an email from the fb javascript auth checker, figures out what to do
        # is there a user with this email?
        # info == [0 email, 1 access token, 2 expires in, 3 signed request, 4 user id]
        email, access, expires, signed, userid = id1.split("&")
        #info = id1.split("&")
        #for inf in info:
        #    log.info("in login controller: %s" % inf)
        log.info("in login controller email: %s" % email)
        log.info("in login controller access: %s" % access)
        log.info("in login controller expires: %s" % expires)
        log.info("in login controller signed: %s" % signed)
        log.info("in login controller userid: %s" % userid)

        data = LoginController.verifyFbSignature(self, signed)
        if data is None:
            log.error('Invalid signature')
            return None

        # we're good, signed request is valid. data we get is:
        #key: issued_at
        #data: 1370378594
        #key: code
        #data: AQDNf1wHzz..
        #key: user_id
        #data: 559612846
        #key: algorithm
        #data: HMAC-SHA256


        user = userLib.getUserByEmail( email )
        if user:
            #- fb checker finds I'm logged in and auth'd
            #    - civ finds there's already a linked account
            #        * present login button that will log me in
            #            - do I save the access token? the code? the email in session?
            #                - however it is standard to work with fb when logged in
            # try using the access token and our ap token with an ajax roundy for the next button
            # signal - this will be a server-side way to check if the user's still cool with us/fb
            # GET graph.facebook.com/debug_token?
            #       input_token={token-to-inspect}
            #       &access_token={app-token-or-admin-token}
            # return a button to be created on the page that will simply log the user in
            # code example for what next button will execute after pinging fb with above code:
            #  loginURL = LoginController.logUserIn(self, user, fbLogin=True)
            #log.info("adding accessToken to session['fbAccessToken']: %s"%access)
            session['fbAccessToken'] = access
            session['fbEmail'] = email
            session.save()
            newButton = '<li><a href="/fbLogin">Login with Facebook</a></li>'
            return newButton
            # if so, is it linked to an fb account by this email yet?
            # ! seeIfUserFbAuth
            
            # ! here is where I either tap into the normal login flow, or 
            # tap into the signup/registration/activation flow

            # will need to figure out if I have ot do anything to pass along the 'afterLoginURL'
            # - just look at how people can land on the site from invites, and press this fb login
            # button instead of pressing the normal signup or login link.

            #if so, log in
            # ! go look at how the login controller logs you in
            # likely a redirect to the workshop page
        # from geo fx
        #return json.dumps({'statusCode':statusCode, 'cityTitle':cityTitle, 'cityURL':cityURL, 'stateTitle':stateTitle, 'stateURL':stateURL, 'countryTitle':countryTitle, 'countryURL':countryURL})
        else:
            #- civ finds there's not yet an account or it is not yet linked
            #* present login button that prompts:
            #    - do you have an account on civinomics already? enter the email/password you use for this account, and we'll link it to your facebook info so you can login with this button in one click next time.
            #    - if you don't already have an account with us, click continue and we will set it up so that you can use our site with your facebook identity, logging in with one click next time
            return "not found"

    def fbLoginHandler(self):
        # NEW ANGLE!
        # send user to page where id will be anych tested again - if it agrees with who
        # this process started with, we log them in
        # if not, a message pertaining to the sitch is put on splash and user is redirected to 
        # the login page.
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
            # confirmed this user's account already exists - render a
            # page made just for logging in by asking facebook one more time
            # if this user is auth'd
            return render("/derived/fbLoggingIn.bootstrap")
            #LoginController.logUserIn(self, user)
        #else:
            #log.warning("incorrect facebook login credentials")
            #splashMsg['content'] = 'incorrect facebook login credentials'
        
    def fbLoggingIn(self):
        # this page has already confirmed we're authd and logged in, just need to 
        # log this person in now
        accessToken = session['fbAccessToken']
        email = session['fbEmail']
        # get user
        user = userLib.getUserByEmail( email )
        if user:
            LoginController.logUserIn(self, user)
        #else:
            # somehow this flow got mixed up and now there's not an account yet
            # create new account flow from here? what are the possible cases?

    def logUserIn(self, user, **kwargs):
        # todo logic to see if pass change on next login, display reset page
        user['laston'] = time.time()
        loginTime = time.localtime(float(user['laston']))
        loginTime = time.strftime("%Y-%m-%d %H:%M:%S", loginTime)
        commit(user)
        session["user"] = user['name']
        session["userCode"] = user['urlCode']
        session["userURL"] = user['url']
        session.save()
        
        if 'afterLoginURL' in session:
            # look for accelerator cases: workshop home, item listing, item home
            loginURL = session['afterLoginURL']
            session.pop('afterLoginURL')
            session.save()
        else:
            loginURL = "/"
        
        #if 'fbLogin' in kwargs:
        #    if kwargs['fbLogin'] is True:
        #        return loginURL
        return redirect(loginURL)

    def loginHandler(self):
        """ Display and Handle Login """
        c.title = c.heading = "Login"  
        c.splashMsg = False
        splashMsg = {}
        splashMsg['type'] = 'error'
        splashMsg['title'] = 'Error'

        try:
            email = request.params["email"].lower()
            password = request.params["password"]
                
            log.info('user %s attempting to log in' % email)
            if email and password:
                user = userLib.getUserByEmail( email )
         
                if user: # not none or false
                    if user['activated'] == '0':
                        splashMsg['content'] = "This account has not yet been activated. An email with information about activating your account has been sent. Check your junk mail folder if you don't see it in your inbox."
                        baseURL = c.conf['activation.url']
                        url = '%s/activate/%s__%s'%(baseURL, user['activationHash'], user['email'])
                        mailLib.sendActivationMail(user['email'], url)
                        
                    elif user['disabled'] == '1':
                        log.warning("disabled account attempting to login - " + email )
                        splashMsg['content'] = 'This account has been disabled by the Civinomics administrators.'
                    elif userLib.checkPassword( user, password ): 
                        # if pass is True
                        LoginController.logUserIn(self, user)

                    else:
                        log.warning("incorrect username or password - " + email )
                        splashMsg['content'] = 'incorrect username or password'
                else:
                    log.warning("incorrect username or password - " + email )
                    splashMsg['content'] = 'incorrect username or password'
            else:
                splashMsg['content'] = 'missing username or password'
            
            session['splashMsg'] = splashMsg
            session.save()
            
            return redirect("/login")

        except KeyError:
            return redirect('/')

    @login_required
    def logout(self):
        """ Action will logout the user. """
        return_url = '/'
        username = session['user']
        log.info( "Successful logout by - " + username )
        session.delete()
        return redirect( return_url )

    def forgot_handler(self):
        c.title = c.heading = "Forgot Password"
        c.splashMsg = False
        splashMsg = {}
        splashMsg['type'] = 'error'
        splashMsg['title'] = 'Error'
        email = request.params["email"].lower()
        user = userLib.getUserByEmail( email ) 
        if user:
            if email != config['app_conf']['admin.email']:
                password = userLib.generatePassword() 
                userLib.changePassword( user, password )
                commit( user ) # commit database change

                toEmail = user['email']
                frEmail = 'Civinomics Helpdesk <helpdesk@civinomics.com>' 
                subject = 'Password Recovery'
                message = '''We have created a new password for you.\n\n 
Your password has been reset to: ''' + password
                message += '''
Please use this password to login at the Civinomics login page:\n
https://civinomics.com/login.\n\n
You can change your password to something you prefer on your profile page.\n\n'''


                mailLib.send( toEmail, frEmail, subject, message )

                log.info( "Successful forgot password for " + email )
                splashMsg['type'] = 'success'
                splashMsg['title'] = 'Success'
                splashMsg['content'] = '''A new password was emailed to you.'''
                session['alert'] = splashMsg
                session.save()
                return redirect('/forgotPassword')
            else:
                log.info( "Failed forgot password for " + email )
                splashMsg['content'] = "Email not found or account has been disabled or deleted."
                session['alert'] = splashMsg
                session.save()
                return redirect('/forgotPassword')
        else:
            log.info( "Failed forgot password for " + email )
            splashMsg['content'] = "Email not found or account has been disabled or deleted."
            session['alert'] = splashMsg
            session.save()
            return redirect('/forgotPassword')

    @login_required
    def changepass(self):
        """ Action will display a change password form. """
        user = session['user']
        c.title = c.heading = "Change password for " + user  
        return render( "/derived/changepass.mako" )

    def loginDisplay(self, workshopCode, workshopURL, thing, thingCode, thingURL):
        if workshopCode != 'None' and workshopURL != 'None':
            afterLoginURL = "/workshop/%s/%s"%(workshopCode, workshopURL)
            if thing != 'None':
                afterLoginURL += "/" + thing
                if thingCode != 'None' and thingURL != 'None':
                    afterLoginURL += "/%s/%s"%(thingCode, thingURL)
            session['afterLoginURL'] = afterLoginURL
            session.save()
            log.info('loginDisplay afterLoginURL is %s'%afterLoginURL)
        
        if 'splashMsg' in session:
            c.splashMsg = session['splashMsg']
            session.pop('splashMsg')
            session.save()
            
        return render("/derived/login.bootstrap")

    def forgotPassword(self):
        return render("/derived/forgotPassword.bootstrap")
