# -*- coding: utf-8 -*-
import logging, time

from pylons import request, response, session, tmpl_context as c, url
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
import pylowiki.lib.db.rating   as ratingLib
import pylowiki.lib.db.share    as shareLib
import pylowiki.lib.utils       as utils
import pylowiki.lib.db.follow       	as followLib
import pylowiki.lib.db.workshop     	as workshopLib
import pylowiki.lib.db.facilitator      as facilitatorLib
import pylowiki.lib.db.listener         as listenerLib
import pylowiki.lib.db.pmember      	as pMemberLib
import pylowiki.lib.db.facilitator      as facilitatorLib

# twython imports
from twython import Twython

import requests
import mechanize

import base64
import hashlib
import hmac
import urllib2 as urllib2
import simplejson as json

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
        log.info("twythonLogin")
        #: https://github.com/ryanmcgrath/twython
        # create a Twython instance with Consumer Key and Consumer Secret
        twitter = Twython(config['twitter.consumerKey'], config['twitter.consumerSecret'])
        # callback url is set in the app on twitter, otherwise it can be set in this call
        auth = twitter.get_authentication_tokens(force_login=True)

        # From the auth variable, save the oauth_token and oauth_token_secret for later use 
        # (these are not the final auth tokens).
        session['oauth_token'] = auth['oauth_token']
        session['oauth_token_secret'] = auth['oauth_token_secret']
        session.save()

        #Send the user to the authentication url
        return redirect(auth['auth_url'])

    def twythonLogin2(self):
        log.info("twythonLogin2")
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
        log.info("grabbed verify_credentials")
        user = userLib.getUserByTwitterId( myCreds['id'] )
        if user:
            log.info('found twitter id')
            # we have an active account.
            user['oauth_twitter_token'] = final_step['oauth_token']
            user['oauth_twitter_token_secret'] = final_step['oauth_token_secret']
            user['externalAuthType'] = 'twitter'
            profilePicLink = myCreds['profile_image_url_https']
            profilePicLink = profilePicLink.replace('_normal', '_bigger', -1)
            user['twitterProfilePic'] = profilePicLink
            commit(user)
            if user['activated'] == '0':
                log.info('twitter user not activated')
                splashMsg['content'] = "This account has not yet been activated. An email with information about activating your account has been sent. Check your junk mail folder if you don't see it in your inbox."
                baseURL = c.conf['activation.url']
                url = '%s/activate/%s__%s'%(baseURL, user['activationHash'], user['email'])
                mailLib.sendActivationMail(user['email'], url)
            elif user['disabled'] == '1':
                log.warning("disabled account attempting to login via twitter - " + user['email'])
                splashMsg['content'] = 'This account has been disabled by the Civinomics administrators.'
            else:
                log.info("logging twt user in")
                # log this person in
                loginURL = LoginController.logUserIn(self, user)
                return redirect(loginURL)
        else:
            log.info('did not find twitter id')
            
            # save necessary info in session for registering this user
            session['twitterId'] = myCreds['id']
            session['twitter_oauth_token'] = final_step['oauth_token']
            session['twitter_oauth_secret'] = final_step['oauth_token_secret']
            session['twitterName'] = myCreds['name']
            # myCreds['profile_image_url_https'] links to a 48x48 image. we can
            # get 73x73 by replacing _normal with _bigger, or ask for the original.
            # for now let's just link to the bigger version
            profilePicLink = myCreds['profile_image_url_https']
            profilePicLink = profilePicLink.replace('_normal', '_bigger', -1)
            session['twitterProfilePic'] = profilePicLink

            c.title = c.heading = "Registration using your Twitter Account"
            c.success = False
            splashMsg = {}
            splashMsg['type'] = 'success'
            splashMsg['title'] = 'Email, zipcode and terms of use.'
            splashMsg['content'] = 'Before we can sign you in, please provide your email, zipcode and agree to our use terms of use.'
            
            session['splashMsg'] = splashMsg
            session.save()
            log.info("rendering twitterSignUp")
            return render("/derived/twitterSignUp.bootstrap")

        log.info("redirect to login")
        session['splashMsg'] = splashMsg
        session.save()
        return redirect("/login")

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
        if utils.badEmail(email):
            user = False
        else:
            # get user by email, if no match look for match by facebook user id
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
                # IF they know their password, and only if their account was originally
                # a normal account. If they've authenticated with twitter, for now they 
                # have made their choice. No need to auth with facebook as well.
                if 'twitterAuthId' in user.keys():
                    log.info('twitter auth id in user keys')
                    #log.info("user who auths with twitter now wants to auth with facebook. not allowed at this point.")
                    #splashMsg['content'] = ", we cannot allow you to login using facebook authentication since you do so with your twitter account already."
                    #session['splashMsg'] = splashMsg
                    #session.save()
                    #return redirect('/login')
                    if user['activated'] == '0':
                        # NOTE this case may not ever occur
                        log.info('twitter user not activated')
                        splashMsg['content'] = "This account has not yet been activated. An email with information about activating your account has been sent. Check your junk mail folder if you don't see it in your inbox. Otherwise, try the Sign In with Facebook button."
                        baseURL = c.conf['activation.url']
                        url = '%s/activate/%s__%s'%(baseURL, user['activationHash'], user['email'])
                        mailLib.sendActivationMail(user['email'], url)
                        
                    elif user['disabled'] == '1':
                        log.info('disabled account attempting to login')
                        log.warning("disabled account attempting to login - " + email )
                        splashMsg['content'] = 'This account has been disabled by the Civinomics administrators.'
                    else: 
                        # link up this account with their facebook stuff
                        log.info('link facebook data to twitter activated account')
                        if 'avatarSource' not in user.keys():
                            user['avatarSource'] = 'facebook'
                        user['facebookAccessToken'] = session['fbAccessToken']
                        user['externalAuthType'] = 'facebook'
                        # a user's account email can be different from the email on their facebook account.
                        # we should keep track of this, it'll be handy
                        user['facebookAuthId'] = session['facebookAuthId']
                        user['fbEmail'] = email
                        commit(user)
                        loginURL = LoginController.logUserIn(self, user)
                        return redirect(loginURL)
                elif 'unactivatedTwitterAuthId' in user.keys():
                    # ok, unactivatedTwitterAuthId IS in user.keys():
                    # is this an account created just with twitter signup? Is this a normal account?
                    if 'originTwitter' in user.keys():
                        # this is an account that was attempted to be created by twitter id, but
                        # not activated. treat this as a new signup, overwrite the account data 
                        # with the facebook data
                        return redirect("signup/fbSignUp/")
                    else:
                        # this is a normal account and this (or another) person has tried to register
                        # using twitter, but has not completed the process. allow them to link this account 
                        # to facebook login if they know their password
                        log.info('link to normal account')
                        c.email = email
                        return render("/derived/fbLinkAccount.bootstrap")
                else:
                    # we have a normal account on this site, and someone with an fb account by this
                    # email wants to log in. I can't guarantee facebook makes a new user verify their
                    # email before being able to authenticate on other sites (created too many test accounts, I'm blocked now).
                    # so, ask for their current account's password
                    log.info('link to normal account')
                    c.email = email
                    return render("/derived/fbLinkAccount.bootstrap")
                
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
            loginURL = LoginController.logUserIn(self, user)
            return redirect(loginURL)
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
                if not utils.badEmail(email):
                    user['fbEmail'] = email
                    # a bug may have set some user emails to be made from their fb auth id
                    # so this is in place to fix that
                    if user['email'] == "%s@%s.com"%(facebookAuthId, facebookAuthId):
                        log.info('fixing facebook id generated email')
                        user['email'] = email
                commit(user)
                #return redirect("/fbLoggingIn")
                loginURL = LoginController.logUserIn(self, user)
                return redirect(loginURL)
            else:
                return redirect("signup/fbSigningUp")
        
    def fbLinkAccountHandler(self):
        #: handles a login when first connecting a user's account with facebook external
        #: authentication
        c.title = c.heading = "Linking account with Facebook Login"  
        c.splashMsg = False
        splashMsg = {}
        splashMsg['type'] = 'error'
        splashMsg['title'] = 'Error'

        try:
            email = session['fbEmail']
            password = request.params["password"]
                
            log.info('user %s attempting to log in with facebook auth for first time' % email)
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
                        # if pass is True, link up this account with their facebook stuff
                        # don't set their pic to be from facebook, allow them to do that
                        # if 'avatarSource' not in user.keys():
                        #    user['avatarSource'] = 'facebook'
                        user['facebookAccessToken'] = session['fbAccessToken']
                        user['externalAuthType'] = 'facebook'
                        # a user's account email can be different from the email on their facebook account.
                        # we should keep track of this, it'll be handy
                        user['facebookAuthId'] = session['facebookAuthId']
                        user['fbEmail'] = email
                        commit(user)
                        loginURL = LoginController.logUserIn(self, user)
                        return redirect(loginURL)
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

    def twtLinkAccountHandler(self):
        #: handles a login when first connecting a user's account with twitter external
        #: authentication
        log.info('twtLinkAccountHandler')
        c.title = c.heading = "Linking account with Twitter Login"  
        c.splashMsg = False
        splashMsg = {}
        splashMsg['type'] = 'error'
        splashMsg['title'] = 'Error'
        try:
            email = session['twtEmail']
            password = request.params["password"]
                
            log.info('user attempting to log in with twitter auth for first time')
            if email and password:
                user = userLib.getUserByEmail( email )
         
                if user: # not none or false
                    log.info('found user')
                    if user['activated'] == '0':
                        log.info('not activated')
                        splashMsg['content'] = "This account has not yet been activated. An email with information about activating your account has been sent. Check your junk mail folder if you don't see it in your inbox."
                        baseURL = c.conf['activation.url']
                        url = '%s/activate/%s__%s'%(baseURL, user['activationHash'], user['email'])
                        mailLib.sendActivationMail(user['email'], url)
                        
                    elif user['disabled'] == '1':
                        log.info('disabled')
                        log.warning("disabled account attempting to login - " + email )
                        splashMsg['content'] = 'This account has been disabled by the Civinomics administrators.'
                    elif userLib.checkPassword( user, password ): 
                        log.info('password valid')
                        # if pass is True, link up this account with their twitter stuff
                        # add twitter userid to user
                        user['twitterAuthId'] = session['twitterId']
                        # this will allow us to use the twitter api in their name
                        user['twitter_oauth_token'] = session['twitter_oauth_token']
                        user['twitter_oauth_secret'] = session['twitter_oauth_secret']
                        user['externalAuthType'] = 'twitter'
                        
                        if 'twitterProfilePic' in session:
                            # don't set their pic to be from twitter, allow them to do that
                            #user['avatarSource'] = 'twitter'
                            user['twitterProfilePic'] = session['twitterProfilePic']
                        
                        commit(user)
                        log.info( "Successful twitter link")
                        loginURL = LoginController.logUserIn(self, user)
                        return redirect(loginURL)
                    else:
                        log.warning("incorrect username or password")
                        splashMsg['content'] = 'incorrect username or password'
                else:
                    log.info('did not find user')
                    log.warning("incorrect username or password" )
                    splashMsg['content'] = 'incorrect username or password'
            else:
                splashMsg['content'] = 'missing username or password'
            
            session['splashMsg'] = splashMsg
            session.save()
            
            return redirect("/login")

        except KeyError:
            return redirect('/')


    def fbLoggingIn(self):
        # this page has already confirmed we're authd and logged in, just need to 
        # log this person in now
        facebookAuthId = session['facebookAuthId']
        email = session['fbEmail']
        log.info("login:fbLoggingIn")
        # get user
        if utils.badEmail(email):
            user = False
        else:
            # get user by email, if no match look for match by facebook user id
            user = userLib.getUserByEmail( email )

        if not user:
            user = userLib.getUserByFacebookAuthId( facebookAuthId )
        if user:
            log.info("login:fbLoggingIn found user, logging in")
            if user['activated'] == '0':
                splashMsg['content'] = "This account has not yet been activated. An email with information about activating your account has been sent. Check your junk mail folder if you don't see it in your inbox."
                baseURL = c.conf['activation.url']
                url = '%s/activate/%s__%s'%(baseURL, user['activationHash'], user['email'])
                mailLib.sendActivationMail(user['email'], url)
            elif user['disabled'] == '1':
                log.warning("disabled account attempting to login - " + email )
                splashMsg['content'] = 'This account has been disabled by the Civinomics administrators.'
            else:
                loginURL = LoginController.logUserIn(self, user)
                return redirect(loginURL)
        else:
            log.info("login:fbLoggingIn DID NOT FIND USER")
        session['splashMsg'] = splashMsg
        session.save()
            
        return redirect("/login")

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
        
        # get and cache their ratings
        ratings = ratingLib.getRatingsForUser()
        session["ratings"] = ratings
        session.save()
        
        # get their workshops and initiatives of interest
        bookmarkedWorkshops = []
        privateWorkshops = []
        listenerWorkshops = []
        facilitatorWorkshops = []
        interestedWorkshops = []
        facilitatorInitiatives = []
        bookmarkedInitiatives = []
        interestedInitiatives = []
        
        bookmarked = followLib.getWorkshopFollows(c.authuser)
        bookmarkedWorkshops = [ followObj['workshopCode'] for followObj in bookmarked ]
        session["bookmarkedWorkshops"] = bookmarkedWorkshops
        session.save()

        privateList = pMemberLib.getPrivateMemberWorkshops(c.authuser, deleted = '0')
        if privateList:
            pmemberWorkshops = [workshopLib.getWorkshopByCode(pMemberObj['workshopCode']) for pMemberObj in privateList]
            privateList = [w for w in pmemberWorkshops if w['public_private'] != 'public']
            privateWorkshops = [w['urlCode'] for w in privateList]
        session["privateWorkshops"] = privateWorkshops
        session.save()
		
        listenerList = listenerLib.getListenersForUser(c.authuser, disabled = '0')
        listenerWorkshops = [lw['workshoplCode'] for lw in listenerList]
        session["listenerWorkshops"] = listenerWorkshops
        session.save()
        
        facilitatorList = facilitatorLib.getFacilitatorsByUser(c.authuser)
        for f in facilitatorList:
            if f['disabled'] == '0':
                if 'workshopCode' in f:
                    facilitatorWorkshops.append(f['workshopCode'])
                elif 'initiativeCode' in f:
                    facilitatorInitiatives(f['initiativeCode'])
                    
        session["facilitatorWorkshops"] = facilitatorWorkshops
        session.save()
        
        interestedWorkshops = list(set(listenerWorkshops + bookmarkedWorkshops + privateWorkshops + facilitatorWorkshops))
        session["interestedWorkshops"] = interestedWorkshops
        session.save()

	       
        log.info("login:logUserIn")
        if 'iPhoneApp' in kwargs:
            if kwargs['iPhoneApp'] != True:
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
        else:
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
            if 'loginResetPassword' in loginURL:
                loginURL = '/profile/' + user['urlCode'] + '/' + user['url'] + '/edit#tab4'
            session.pop('afterLoginURL')
            session.save()
        else:
            loginURL = "/"
        
        #if 'fbLogin' in kwargs:
        #    if kwargs['fbLogin'] is True:
        #        return loginURL
        return loginURL

    def loginHandler(self):
        """ Display and Handle Login. 
        JSON responses:
            statusCode == 0:    Same as unix exit code (OK)
            statusCode == 1:    No query was submitted
            statusCode == 2:    Query submitted, no results found
            result:             user's email and password are valid, session data returned?
        """
        c.title = c.heading = "Login"  
        c.splashMsg = False
        splashMsg = {}
        splashMsg['type'] = 'error'
        splashMsg['title'] = 'Error'

        iPhoneApp = utils.iPhoneRequestTest(request)

        try:
            email = request.params["email"].lower()
            password = request.params["password"]
                
            log.info('user %s attempting to log in' % email)
            if email and password:
                user = userLib.getUserByEmail( email )
                if user: # not none or false
                    if user['activated'] == '6':
                        splashMsg['content'] = "This account has not yet been activated. An email with information about activating your account has been sent. Check your junk mail folder if you don't see it in your inbox."
                        baseURL = c.conf['activation.url']
                        url = '%s/activate/%s__%s'%(baseURL, user['activationHash'], user['email'])
                        mailLib.sendActivationMail(user['email'], url)
                        
                    elif user['disabled'] == '1':
                        log.warning("disabled account attempting to login - " + email )
                        splashMsg['content'] = 'This account has been disabled by the Civinomics administrators.'
                    elif userLib.checkPassword( user, password ):
                        # if pass is True
                        loginURL = LoginController.logUserIn(self, user, iPhoneApp=iPhoneApp)
                        if iPhoneApp:
                            response.headers['Content-type'] = 'application/json'
                            # iphone app is having problems with the case where a user logs in after 
                            # browsing the site first, so for now we'll just return a login url of /
                            #return json.dumps({'statusCode':0, 'user':dict(user), 'returnPage':loginURL})
                            return json.dumps({'statusCode':0, 'user':dict(user), 'returnPage':'/'})
                        else:
                            return redirect(loginURL)
                    else:
                        log.warning("incorrect username or password - " + email )
                        splashMsg['content'] = 'incorrect username or password'
                        if iPhoneApp:
                            response.headers['Content-type'] = 'application/json'
                            return json.dumps({'statusCode':2, 'message':'incorrect username or password'})
                else:
                    log.warning("incorrect username or password - " + email )
                    splashMsg['content'] = 'incorrect username or password'
                    if iPhoneApp:
                        response.headers['Content-type'] = 'application/json'
                        return json.dumps({'statusCode':2, 'message':'incorrect username or password'})
            else:
                splashMsg['content'] = 'missing username or password'
                if iPhoneApp:
                    response.headers['Content-type'] = 'application/json'
                    return json.dumps({'statusCode':1, 'message':'missing username or password'})
            
            session['splashMsg'] = splashMsg
            session.save()
            
            return redirect("/login")

        except KeyError:
            if iPhoneApp:
                response.headers['Content-type'] = 'application/json'
                return json.dumps({'statusCode':1, 'message':'keyerror'})
            return redirect('/')

    @login_required
    def logout(self):
        """ Action will logout the user. """
        iPhoneApp = utils.iPhoneRequestTest(request)

        return_url = '/'
        username = session['user']
        log.info( "Successful logout by - " + username )
        session.delete()
        if iPhoneApp:
            statusCode = 0
            response.headers['Content-type'] = 'application/json'
            return json.dumps({'statusCode':statusCode})
        else:
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
                return redirect('/loginResetPassword')
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

        if workshopCode != 'None':
            afterLoginURL = "/workshop/%s/%s"%(workshopCode, workshopURL)
            if thing != 'None' and thing != 'newWorkshop':
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

    def loginRedirects(self, page):
        c.facebookAppId = config['facebook.appid']
        c.channelUrl = config['facebook.channelUrl']

        afterLoginURL = ''
        if page == 'newWorkshop':
            afterLoginURL += "/workshop/display/create/form"
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
        return render("/derived/login.bootstrap")
