# -*- coding: utf-8 -*-
import logging, time

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.controllers.login import logUserIn
from pylons import config

from urllib import urlencode

from pylowiki.lib.base import BaseController, render

import pylowiki.lib.helpers as h
import pylowiki.lib.db.user as userLib
import pylowiki.lib.mail as mailLib
from pylowiki.lib.auth import login_required
from pylowiki.lib.db.dbHelpers import commit

import simplejson as json

log = logging.getLogger(__name__)

def getFcbkPermissions():
    return 'email'

def facebookGraphAPIGetUsr(token):
    """
        Given an AccessToken gives the fcbk user
    """
    args = dict(access_token=token)
    
    try :
        profile = load(urlopen("https://graph.facebook.com/me?"+
                    urlencode(args)))
        return profile
    except:
        print "Could not Get USer info"
        return None

class FloginController(BaseController):

    def checkEmail(self, id1):
        # this receives an email from the fb javascript auth checker, figures out what to do

        # is there a user with this email?
        user = userLib.getUserByEmail( id1 )
        if user: # not none or false
            logUserIn(self, user)
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
        if not user:
            return 'user %s not found'%id1
        return str( json.dumps({'user name':user['name'], 'user email':user['email']}) )



    def loginHandler(self, id1):
        log.info("loginHandler accessed")
        log.info("id1: "+id1)
        for key in request.environ:
            log.info("req: "+str(request.environ[key]))
        #log.info("token: "+token)
        #log.info("code: "+code)

        raise Exception('need to dig into the request response')
        """http://todd.civinomics.org/flogin/loginHandler/a#
        access_token=CAAB52LI5y94BAPOGLsrXnfJuH9XcINbilYE3LNosiA1ZBxdE7os4ShQaRmKlS5IeEh0BjYWV5orQ4eslduyjCXN0vebbpNwYVp1NtKMW2YQFFjXkerfzspV4L7ZBDaDuUT0Nc725x6ikyBbPWu
        &
        expires_in=5177474
        &
        code=AQBNIgLZoY-_6-YTzD_yA1nfZFlgYJCqLf4XPBG1etcIEyA3-MPgljdxxryHz_1r0P4yjdYY57dYYqURAA-NPgfbs4SvbEwoUpjiViv7jDrA2RsFlp8p3tRS2EyUJF2kScgUlrC74NUW-XYs-X3OrnKs0o61CayjSfIDRJFCZFn4NTdXtMrvtl6837p7nXnL3B3QtpIEnjkBtT7z2YUeZe-pBYTJsTYcPSxCKgf7SianFH0Nr9nygaPcSILMEVYguAA0oq_doaAVaHEBXJE7vpWDHqgcPfrSMaYcqAz5FTsIeO6ds9P82VaMBbwTWE_qnok
        """

        if 'error' in request.params:
            wError = request.params['error']
            if wError == 'error':
                # there has been an error
                if 'error_reason' in request.params:
                    wErrorReason = request.params['error_reason']
                if 'error_description' in request.params:
                    wErrorDescription = request.params['error_description']
                splashMsg['content'] = wErrorReason+'. '+wErrorDescription
                session['splashMsg'] = splashMsg
                session.save()
                return redirect("/login")
        if 'code' in request.params:
            wCode = request.params['code']
            log.info("code: "+wCode)
        if 'token' in request.params:
            wToken = request.params['token']
            log.info("token: "+wToken)
        if 'afterLoginURL' in session:
            # look for accelerator cases: workshop home, item listing, item home
            loginURL = session['afterLoginURL']
            session.pop('afterLoginURL')
            session.save()
        else:
            loginURL = "/"
        
        return redirect(loginURL)

    def login(self):
        args=dict(client_id=config['facebook.appid'], 
                  #display='page',
                  response_type='code token',
                  redirect_uri=config['facebook.loginHandler'],
                  #fbconnect=1,
                  scope=getFcbkPermissions())
        log.info("fb redirect: "+config['facebook.loginHandler'])
        #return redirect("https://www.facebook.com/dialog/permissions.request?"+urlencode(args))
        return redirect("https://www.facebook.com/dialog/oauth?"+urlencode(args))
        """ This also has the following optional parameters:
         - state 
          An arbitrary unique string created by your app to guard against Cross-site Request Forgery
         - response_type 
          Determines whether the response data included when the redirect back to the app occurs 
          is in URL parameters or fragments. See the Confirming Identity section to choose which 
          type your app should use. This can be one of:
           - code 
            Response data is included as URL parameters and contains code parameter 
            (an encrypted string unique to each login request). This is the default behaviour 
            if this parameter is not specified.
           - token 
            Response data is included as a URL fragment and contains an access token
           - code%20token
            Response data is included as a URL fragment and contains both an access token and the 
            code parameter.
         - scope 
          A comma separated list of Permissions to request from the person using your app
        """
    
    def error(self):
        return redirect(ROOT)
    
    def getAccessToken(self, code):
        """
        Given a facebook code , returns an auth token
        """
        args=dict(client_id=FACEBOOK_APP_ID,
                  client_secret=FACEBOOK_SECRET,
                  redirect_uri=request.path_url,
                  code=code)
        response = urlopen('https://graph.facebook.com/oauth/access_token?'+urlencode(args))
        response_txt = response.read()
        return parse_qs(response_txt)

    def processingError(self, error):
        """ 
            Function to handle processing errors 
            TODO: Currently returns error
            But in future we need to redirect the user
            to a webpage that is more informative
        """
        return error

    def index(self):
        if (request.params.get('error', None) != None) :
            return self.error()
        if (request.params.get('code', None) == None) :
            return self.login()
        else :
            code = request.params.get('code')
            accesshash = self.getAccessToken(
                        request.params.get('code', None))
            isAccessTokenPresent = 'access_token' in accesshash
            if (isAccessTokenPresent == False) :
                return self.processingError('Error accessing Faceboook validation')
            else :
                usr = facebookGraphAPIGetUsr(str(accesshash['access_token'][0]))
                if (usr is None) :
                    return self.processingError('Error accessing Facebook '\
                                                 'validation')
                else :
                    buf = "<body><h1> Wie Gehst " +usr['name']+"? </h1>"
                    buf = buf + "id :"+ usr['id']+\
                          "<br> name :"+usr['name']+\
                          "<br> email:"+usr['email']+\
                          "<br>3~"
                    return buf



