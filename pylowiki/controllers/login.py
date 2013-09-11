# -*- coding: utf-8 -*-
import logging, time

from pylons import config, request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import config

from pylowiki.lib.base import BaseController, render

import pylowiki.lib.facebook    as facebookLib
import pylowiki.lib.images      as imageLib
import pylowiki.lib.helpers     as h
import pylowiki.lib.db.user     as userLib
import pylowiki.lib.mail        as mailLib
from pylowiki.lib.auth          import login_required
from pylowiki.lib.db.dbHelpers  import commit
import pylowiki.lib.db.share    as shareLib

# twython imports
from twython import Twython
import urlparse

import base64
import hashlib
import hmac
import urllib as urllib
import urllib2 as urllib2
import simplejson as json

from ordereddict import OrderedDict
import ConfigParser
import random
import binascii

log = logging.getLogger(__name__)

class LoginController(BaseController):

    @h.login_required
    def shareFacebookHandler(self, id1):
        # create the share object
        # we can't directly see what message the user posted with this share, but we
        # might be able to look it up with a facebook graph api call using the postId,
        # so for now it's best to store the postId as the message. 
        # see https://developers.facebook.com/docs/reference/api/post/
        # NOTE - should we add a field to the share object to account for facebook shares?
        itemCode, itemURL, postId = id1.split("&")
        if itemCode and itemURL and postId:
            if 'user' in session:
                share = shareLib.Share(c.authuser, "itemCode", "itemURL", '', '', "postId")
                return 'share stored'
        else:
            return None

    
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

        #for piece in data:
        #    log.info("signature key: %s" % piece)
        #    log.info("signature data: %s" % data[piece])

        return data

    def twythonLogin(self):
        #: https://github.com/ryanmcgrath/twython
        # create a Twython instance with Consumer Key and Consumer Secret
        twitter = Twython(config['twitter.consumerKey'], config['twitter.consumerSecret'])
        # callback url is set in the app on twitter, otherwise it can be set in this call
        auth = twitter.get_authentication_tokens()

        # From the auth variable, save the oauth_token and oauth_token_secret for later use 
        # (these are not the final auth tokens).
        session['oauth_token'] = auth['oauth_token']
        session['oauth_token_secret'] = auth['oauth_token_secret']
        session.save()

        #Send the user to the authentication url
        return redirect(auth['auth_url'])

    def twythonLogin2(self):
        # The callback from twitter will include a verifier as a parameter in the URL.
        # The final step is exchanging the request token for an access token. The access 
        # token is the “key” for opening the Twitter API
        #oauth_verifier = request.GET['oauth_verifier']

        oauth_verifier = request.params['oauth_verifier']
        oauth_token = request.params['oauth_token']

        # We should verify that the token matches the request token received in step 1.
        if not oauth_token == session['oauth_token']:
            log.error('Invalid oauth_token')
            return redirect('/')
        #log.info("oauth_verifier: %s"%oauth_verifier)

        # Now that we have the oauth_verifier stored to a variable, we'll want to create
        # a new instance of Twython and grab the final user tokens
        twitter = Twython(config['twitter.consumerKey'], config['twitter.consumerSecret'], session['oauth_token'], session['oauth_token_secret'])

        final_step = twitter.get_authorized_tokens(oauth_verifier)

        #log.info("session['oauth_token_final']: %s" % session['oauth_token_final'])        
        #log.info("session['oauth_token_secret_final']: %s" % session['oauth_token_secret_final'])

        # with the final user data, we re-initialize the twitter api access object
        twitter = Twython(config['twitter.consumerKey'], config['twitter.consumerSecret'], final_step['oauth_token'], final_step['oauth_token_secret'])

        # grab the user's creds
        myCreds = twitter.verify_credentials()
        
        user = userLib.getUserByTwitterId( myCreds['id'] )
        if user:
            log.info('found twitter id')
            # we have an active account.
            user['oauth_twitter_token'] = final_step['oauth_token']
            user['oauth_twitter_token_secret'] = final_step['oauth_token_secret']
            user['externalAuthType'] = 'twitter'
            commit(user)
            # log this person in
            LoginController.logUserIn(self, user)
        else:
            log.info('did not find twitter id')
            c.numAccounts = 1000
            c.numUsers = len(userLib.getActiveUsers())

            if c.numUsers >= c.numAccounts:
                splashMsg = {}
                splashMsg['type'] = 'error'
                splashMsg['title'] = 'Error:'
                splashMsg['content'] = 'Sorry, our website has reached capacity!  We will be increasing the capacity in the coming weeks.'
                session['splashMsg'] = splashMsg
                session.save()
                return redirect('/')
            # save necessary info in session for registering this user
            session['twitterId'] = myCreds['id']
            session['twitter_oauth_token'] = final_step['oauth_token']
            session['twitter_oauth_secret'] = final_step['oauth_token_secret']
            session['twitterName'] = myCreds['name']
            session['twitterProfilePic'] = myCreds['profile_image_url_https']

            c.title = c.heading = "Registration using your Twitter Account"
            c.success = False
            splashMsg = {}
            splashMsg['type'] = 'success'
            splashMsg['title'] = 'Email, zipcode and terms of use.'
            splashMsg['content'] = 'Before we can sign you in, please provide your email, zipcode and agree to our use terms of use.'
            
            session['splashMsg'] = splashMsg
            session.save()

            return render("/derived/twitterSignUp.bootstrap")

    def fbAuthCheckEmail(self, id1):
        # this receives an email from the fb javascript auth checker, figures out what to do
        # is there a user with this email?
        # info == [0 email, 1 access token, 2 expires in, 3 signed request, 4 user id]
        name, email, access, expires, signed, facebookAuthId, smallPic, bigPic = id1.split("&")
        

        # url has been encoded and the % replaced with , in order for extauth.js to be able to 
        # ajax it over here
        smallPic = smallPic.replace(",","%")
        smallPic = urllib2.unquote(smallPic)
        bigPic = bigPic.replace(",","%")
        bigPic = urllib2.unquote(bigPic)

        log.info("login:fbAuthCheckEmail before verifyFbSignature")
        data = LoginController.verifyFbSignature(self, signed)
        if data is None:
            log.error('Invalid signature')
            return None
        log.info("login:fbAuthCheckEmail made it past verifyFbSignature")

        user = userLib.getUserByFacebookAuthId( facebookAuthId )
        if not user:
            user = userLib.getUserByEmail( email )
            if user:
                log.info("found user by email " + email)
        else:
            if user:
                log.info("found user by facebook id")

        #if user:
        #    for thisKey in user.keys():
        #        log.info("user %s == %s"%(thisKey, user[thisKey]))

        session['facebookAuthId'] = facebookAuthId
        session['fbEmail'] = email
        session['fbAccessToken'] = access
        session['fbName'] = name
        session['fbBigPic'] = bigPic
        session['fbSmallPic'] = smallPic
        session.save()
        if user:           
            # civ finds there's already a linked account
            log.info("returning 'found user'")
            newButton = 'found user'
            return newButton
        else:
            #- civ finds there's not yet an account or it is not yet linked
            log.info("returning 'not found'")
            return "not found"

    def fbLoginHandler(self):
        # NOTE - find when this function is used compared to the one right before this
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
        facebookAuthId = session['facebookAuthId']
        accessToken = session['fbAccessToken']
        email = session['fbEmail']
        # get user by email, if no match look for match by facebook user it
        user = userLib.getUserByEmail( email )
        log.info('asked for email')
        if user:
            log.info('found email')
            alreadyFb = userLib.getUserByFacebookAuthId( unicode(facebookAuthId) )
            if not alreadyFb:
                log.info('did not find by fb id')
                # we have a person that already has an account on site, but hasn't
                # used the facebook auth to login yet
                # we need to activate parameters for this person's account
                user['facebookAuthId'] = facebookAuthId
            else:
                log.info('found by fb id')
            # we have an active account. because of an earlier design flaw we need to 
            # set avatarSource if it hasn't been added to this user object yet
            if 'avatarSource' not in user.keys():
                user['avatarSource'] = 'facebook'
            user['facebookAccessToken'] = accessToken
            user['externalAuthType'] = 'facebook'
            # a user's account email can be different from the email on their facebook account.
            # we should keep track of this, it'll be handy
            user['fbEmail'] = email
            commit(user)
            return redirect("/fbLoggingIn")
        else:
            log.info('did not find by email')
            user = userLib.getUserByFacebookAuthId( unicode(facebookAuthId) )
            if user:
                log.info('found by user id %s'%user['email'])
                # we have an active account. because of an earlier design flaw we need to 
                # set avatarSource if it hasn't been added to this user object yet
                if 'avatarSource' not in user.keys():
                    user['avatarSource'] = 'facebook'
                user['facebookAccessToken'] = accessToken
                user['externalAuthType'] = 'facebook'
                # a user's account email can be different from the email on their facebook account.
                # we should keep track of this, it'll be handy
                user['fbEmail'] = email
                commit(user)
                return redirect("/fbLoggingIn")
            else:
                return redirect("/fbSigningUp")
        
    def fbLoggingIn(self):
        # this page has already confirmed we're authd and logged in, just need to 
        # log this person in now
        facebookAuthId = session['facebookAuthId']
        email = session['fbEmail']
        log.info("login:fbLoggingIn")
        # get user
        user = userLib.getUserByEmail( email )
        if not user:
            user = userLib.getUserByFacebookAuthId( facebookAuthId )
        if user:
            log.info("login:fbLoggingIn found user, logging in")
            LoginController.logUserIn(self, user)
        else:
            log.info("login:fbLoggingIn DID NOT FIND USER - DEAD END") 

    def logUserIn(self, user, **kwargs):
        # NOTE - need to store the access token? kee in session or keep on user?
        # keeping it on the user will allow interaction with user's facebook after they've logged off
        # and by other people
        session["user"] = user['name']
        session["userCode"] = user['urlCode']
        session["userURL"] = user['url']
        session.save()
        log.info("login:logUserIn session save")

        c.authuser = user

        log.info("login:logUserIn")
        if 'externalAuthType' in user.keys():
            log.info("login:logUserIn externalAuthType in user keys")
            if user['externalAuthType'] == 'facebook':
                log.info("login:logUserIn externalAuthType facebook")
                user['facebookAccessToken'] = session['fbAccessToken']
                if 'fbSmallPic' in session:
                    user['facebookProfileSmall'] = session['fbSmallPic']
                    user['facebookProfileBig'] = session['fbBigPic']
            else:
                user['externalAuthType'] = ''
        user['laston'] = time.time()
        loginTime = time.localtime(float(user['laston']))
        loginTime = time.strftime("%Y-%m-%d %H:%M:%S", loginTime)
        commit(user)
        log.info("login:logUserIn commit user")
        
        
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
        c.facebookAppId = config['facebook.appid']
        c.channelUrl = config['facebook.channelUrl']

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

    def loginNoExtAuthDisplay(self, workshopCode, workshopURL, thing, thingCode, thingURL):

        # todo - clear splash message if this came from /fbSignUp

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
            
        return render("/derived/loginNoExtAuth.bootstrap")

    def forgotPassword(self):
        return render("/derived/forgotPassword.bootstrap")
