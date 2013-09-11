import os, logging, re

import urllib

from pylons import session, config, request, tmpl_context as c
from pylons.controllers.util import abort, redirect

log = logging.getLogger(__name__)


"""
    General functions for manually implementing oauth with twitter.
    These don't work correctly yet, but they're close.
"""

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

def twtLoginRedirectManual(self):
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

def twtLoginOauth2(self):
    #: oauth2 library from easy_install oauth2
    #: 1) Obtain a request token
    #: user wants to sign in, POST to twitter../oauth/request_token with oauth_callback
    #: twitter generates request token, responds 200 OK with:
    # oath_token, oauth_token_secret, oauth_callback_confirmed
    # this reponse is routed to twtRequestHandler here

    consumer_key = config['twitter.consumerKey']
    consumer_secret = config['twitter.consumerSecret']

    request_token_url = 'https://api.twitter.com/oauth/request_token'
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    authorize_url = 'https://api.twitter.com/oauth/authorize'

    consumer = oauth.Consumer(consumer_key, consumer_secret)
    client = oauth.Client(consumer)

    # Step 1: Post for a request token. This is a temporary token that is used for 
    # having the user authorize an access token and to sign the request to obtain 
    # said access token.

    params = {
        'oauth_nonce': oauth.generate_nonce(),
        'oauth_callback' : config['twitter.requestTokenUrl'],
        'oauth_signature_method' : "HMAC-SHA1",
        'oauth_timestamp': int(time.time()),
        'oauth_version': "1.0"
    }

    # either twitter will respond right here, or the response will be routed to 
    # the next function, twtRequestHandler
    resp, content = client.request(request_token_url, "POST", parameters=params)
    log.info("resp %s" % resp)
    log.info("content %s" % content)
    # this request should generate a response to the callback url, which will route
    # to function twtRequestHandler

def twtRequestHandler(self):
    #: asking twitter for a request token, the response is directed here
    #: 2) redirecting the user
    # Your application should examine the HTTP status of the response. 
    # Any value other than 200 indicates a failure. The body of the response will 
    # contain the oauth_token, oauth_token_secret, and oauth_callback_confirmed parameters. 
    # Your application should verify that oauth_callback_confirmed is true and store the 
    # other two values for the next steps.

    # how do I grab the request token? it is in the body of the response
    request_token = dict(urlparse.parse_qsl(content))

    log.info("Request Token:")
    log.info("    - oauth_token        = %s" % request_token['oauth_token'])
    log.info("    - oauth_token_secret = %s" % request_token['oauth_token_secret'])

    # Step 2: Redirect to the provider. Since this is a CLI script we do not 
    # redirect. In a web application you would redirect the user to the URL
    # below.

    log.info("Redirect to link:")
    log.info("%s?oauth_token=%s" % (authorize_url, request_token['oauth_token']))

    # After the user has granted access to you, the consumer, the provider will
    # redirect you to whatever URL you have told them to redirect to. You can 
    # usually define this in the oauth_callback argument as well.
    #accepted = 'n'
    #while accepted.lower() == 'n':
    #    accepted = raw_input('Have you authorized me? (y/n) ')
    #oauth_verifier = raw_input('What is the PIN? ')

    # Step 3: Once the consumer has redirected the user back to the oauth_callback
    # URL you can request the access token the user has approved. You use the 
    # request token to sign this request. After this is done you throw away the
    # request token and use the access token returned. You should store this 
    # access token somewhere safe, like a database, for future use.
    token = oauth.Token(request_token['oauth_token'],
        request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)

    resp, content = client.request(access_token_url, "POST")
    access_token = dict(urlparse.parse_qsl(content))

    log.info("Access Token:")
    log.info("    - oauth_token        = %s" % access_token['oauth_token'])
    log.info("    - oauth_token_secret = %s" % access_token['oauth_token_secret'])
    
    log.info("You may now access protected resources using the access tokens above.")
    
def twtLoginHandler(self):
    # handles the data sent back from a login/auth with twitter
    # https://api.twitter.com/oauth/authenticate?oauth_token=NESTV7Yhvk5JBwdpBjF3c8KbKdBVJXjRKB3vbKwvxY
    log.info("twitter said hi back!")
