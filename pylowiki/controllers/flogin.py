import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, redirect
from urllib import urlencode
from urllib2 import urlopen
from urlparse import parse_qs
from json import load

import pylowiki.lib.helpers as h
from pylowiki.model import get_user, getPoints, getUserSuggestions, getArticlesRead, getVotes
from pylowiki.model import getSolutions, getUserContributions, getUserConnections, getUserWork

from pylowiki.lib.base import BaseController, render


log = logging.getLogger(__name__)

FACEBOOK_APP_ID = '134890166613257'
FACEBOOK_SECRET = 'ab78d6311b43361f1e4e7620d70d93bb' #Dont share this
ROOT = 'http://greenocracy.org'

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

    def login(self):
        args=dict(client_id=FACEBOOK_APP_ID, 
                  #display='page',
                  #response_type='code',
                  redirect_uri=request.path_url,
                  #fbconnect=1,
                  scope=getFcbkPermissions())
        #return redirect("https://www.facebook.com/dialog/permissions.request?"+urlencode(args))
        return redirect("https://www.facebook.com/dialog/oauth?"+urlencode(args))
    
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



