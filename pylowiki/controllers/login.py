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

import requests
import mechanize

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

    def create_auth_header(self, parameters):
        """For all collected parameters, order them and create auth header"""
        ordered_parameters = {}
        ordered_parameters = OrderedDict(sorted(parameters.items()))
        auth_header = (
            '%s="%s"' % (k, v) for k, v in ordered_parameters.iteritems())
        val = "OAuth " + ', '.join(auth_header)
        return val

    def calculate_signature(self, signing_key, signature_base_string):
        """Calculate the signature using SHA1"""
        hashed = hmac.new(signing_key, signature_base_string, hashlib.sha1)

        sig = binascii.b2a_base64(hashed.digest())[:-1]

        return LoginController.escape(self, sig)


    def create_signing_key(self, oauth_consumer_secret, oauth_token_secret=None):
        """Create key to sign request with"""
        signing_key = LoginController.escape(self, oauth_consumer_secret) + '&'

        if oauth_token_secret is not None:
            signing_key += LoginController.escape(self, oauth_token_secret)

        return signing_key


    def stringify_parameters(self, parameters):
        """Orders parameters, and generates string representation of parameters"""
        output = ''
        ordered_parameters = {}
        ordered_parameters = OrderedDict(sorted(parameters.items()))

        counter = 1
        for k, v in ordered_parameters.iteritems():
            output += LoginController.escape(self, str(k)) + '=' + LoginController.escape(self, str(v))
            if counter < len(ordered_parameters):
                output += '&'
                counter += 1

        return output

    def escape(self, s):
        """Percent Encode the passed in string"""
        return urllib.quote(s, safe='~')

    def collect_parameters(self, oauth_parameters, status, url_parameters):
        """Combines oauth, url and status parameters"""
        #Add the oauth_parameters to a temp hash
        temp = oauth_parameters.copy()

        #Add the status, if passed in.  Used for posting a new tweet
        if status is not None:
            temp['status'] = status

        if url_parameters is not None:
            #Add the url_parameters to the temp hash
            for k, v in url_parameters.iteritems():
                temp[k] = v

        return temp

    def generate_signature(self, method, url, oauth_parameters, oauth_consumer_key, oauth_consumer_secret, oauth_token_secret=None, status=None, url_parameters=None):
        """Create the signature base string"""

        #Combine parameters into one hash
        temp = LoginController.collect_parameters(self, oauth_parameters, status, url_parameters)

        #Create string of combined url and oauth parameters
        parameter_string = LoginController.stringify_parameters(self, temp)

        #Create your Signature Base String
        signature_base_string = ( method.upper() + '&' + LoginController.escape(self, str(url)) + '&' + LoginController.escape(self, parameter_string) )

        #Get the signing key
        signing_key = LoginController.create_signing_key(self, oauth_consumer_secret, oauth_token_secret)

        return LoginController.calculate_signature(self, signing_key, signature_base_string)

    def get_nonce(self):
        """Unique token generated for each request"""
        n = base64.b64encode(''.join([str(random.randint(0, 9)) for i in range(24)]))
        return n

    def get_oauth_parameters(self, consumer_key, access_token):
        """Returns OAuth parameters needed for making request"""
        oauth_parameters = {
            'oauth_callback' : config['twitter.callbackurl'],
            'oauth_timestamp': str(int(time.time())),
            'oauth_signature_method': "HMAC-SHA1",
            'oauth_version': "1.0",
            'oauth_token': access_token,
            'oauth_nonce': LoginController.get_nonce(self),
            'oauth_consumer_key': consumer_key
        }

        return oauth_parameters

    def twtLoginRedirect(self):
        # assemble an oauth post for twitter
        url = config['twitter.requestTokenUrl']
        method = "POST"
        # this is for doing a get at twitter to create a post, not needed here
        #url_parameters = {
        #    'exclude_replies': 'true'
        #}

        #configuration hash for the keys
        keys = {
            "twitter_consumer_secret": config['twitter.consumerSecret'],
            "twitter_consumer_key": config['twitter.consumerKey'],
            "access_token": config['twitter.accessToken'],
            "access_token_secret": config['twitter.accessTokenSecret']
        }

        oauth_parameters = LoginController.get_oauth_parameters(
            self,
            keys['twitter_consumer_key'],
            keys['access_token']
        )

        oauth_parameters['oauth_signature'] = LoginController.generate_signature(
            self,
            method,
            url,
            oauth_parameters,
            keys['twitter_consumer_key'],
            keys['twitter_consumer_secret'],
            keys['access_token_secret']
        )

        headers = {'Authorization': LoginController.create_auth_header(self, oauth_parameters)}

        # this is how the code from 
        # http://mkelsey.com/2013/05/01/authorizing-and-signing-a-twitter-api-call-using-python/
        # is supposed to end, but in this case we're doing a post redirect
        # url += '?' + urllib.urlencode(url_parameters)
        r = requests.post(url, headers=headers)
        print json.dumps(json.loads(r.text), sort_keys=False, indent=4)

        log.info(r)
        #return redirect(requests.post(url, headers=headers))


    def twtLoginHandler(self):
        # handles the data sent back from a login/auth with twitter
        # https://api.twitter.com/oauth/authenticate?oauth_token=NESTV7Yhvk5JBwdpBjF3c8KbKdBVJXjRKB3vbKwvxY
        log.info("twitter said hi back!")

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
