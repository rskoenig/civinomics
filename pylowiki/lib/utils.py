import logging, string

from urllib import quote
from zlib import adler32
from pylons import session, tmpl_context as c
import pylowiki.lib.db.follow       as followLib
import pylowiki.lib.db.generic      as generic
from pylons import tmpl_context as c, config, session
import urllib2

log = logging.getLogger(__name__)

# For base62 conversion
BASE_LIST = string.digits + string.letters
BASE_DICT = dict((c, i) for i, c in enumerate(BASE_LIST))

def iPhoneRequestTest(req):
    """ check for json=1 in the request parameters, if so this is a request from our iphone app """
    try:
        useJson = req.params['json']
        if useJson == '1':
            return True
        else:
            return False
    except:
        return False

def profileDisplayWorkshops(req):
    """ check for type=ws in the request parameters, if so this is a request to display workshops """
    try:
        displayType = req.params['type']
        if displayType == 'ws':
            return True
        else:
            return False
    except:
        return False

def urlify(url):
    import re
    pattern = re.compile('[^-\w]+')
    url = url.strip()
    url = url.lower()
    url = url.replace(' ', '-')
    url = pattern.sub('', url)
    url = url.encode('utf8')
    url = quote(url)
    return url

def geoDeurlify( something ):
    deurl = something.replace('-', ' ')
    return deurl.title() 

"""
    Takes in a string 's', returns a base-62 representation of a hash of that string.
    Used for generating short-form codes within URLs.  If a collision occurs, a secondary
    match will need to be used.  For example, matching a workshop's code and title if the
    workshop's code results in a collision.
"""
def toBase62(thing):
    s = str(thing.id + 1124816) # Offset by 1-1-2-4-8-16; first 5 numbers in Fibbonacci sequence
    #num = adler32(s)
    num = int(s)
    if num < 0: num = -num
    return base_encode(num)

# base_decode taken from http://stackoverflow.com/a/2549514
def base_decode(string, reverse_base=BASE_DICT):
    length = len(reverse_base)
    ret = 0
    for i, c in enumerate(string[::-1]):
        ret += (length ** i) * reverse_base[c]
    return ret

# base_encode taken from http://stackoverflow.com/a/2549514
def base_encode(integer, base=BASE_LIST):
    length = len(base)
    ret = ''
    while integer != 0:
        ret = base[integer % length] + ret
        integer /= length
    return ret

def isWatching(user, workshop):
   # Even though the functions use the verb 'following', the mechanism is the same...we just display 
   # object follows as 'watching'.
   c.isFollowing = followLib.isFollowing(user, workshop)
  
def thingURL(thingParent, thing):
    if thingParent.objType.replace("Unpublished", "") == 'workshop':
        parentBase = "workshop"
    elif thingParent.objType.replace("Unpublished", "") == 'user':
        parentBase = "profile"
    elif thingParent.objType.replace("Unpublished", "") == 'initiative':
        parentBase = "initiative"
    baseURL = '/%s/%s/%s' % (parentBase, thingParent['urlCode'], thingParent['url'])
    if thing.objType.replace("Unpublished", "") == 'photo':
        return baseURL + "/photo/show" + thing['urlCode']
    if thing.objType.replace("Unpublished", "") == 'initiative':
        return baseURL + "/show"
    if thing.objType.replace("Unpublished", "") == 'comment':
        if 'ideaCode' in thing.keys():
            thing = generic.getThing(thing['ideaCode'])
        elif 'resourceCode' in thing.keys():
            thing = generic.getThing(thing['resourceCode'])
        elif 'photoCode' in thing.keys():
            thing = generic.getThing(thing['photoCode'])
            return baseURL + "/photo/show/" + thing['urlCode'] 
        elif 'initiativeCode' in thing.keys():
            thing = generic.getThing(thing['initiativeCode'])
            return baseURL + "/show/" 
        elif 'discussionCode' in thing.keys():
            thing = generic.getThing(thing['discussionCode'])
        else:
            return baseURL
    return baseURL + "/%s/%s/%s" %(thing.objType, thing['urlCode'], thing['url'])
    
def profilePhotoURL(thing):
    owner = generic.getThing(thing['userCode'])

    return "/profile/%s/%s/photo/show/%s" %(owner['urlCode'], owner['url'], thing['urlCode'])
    
def initiativeURL(thing):
    if thing.objType == 'resource':
        # an initiative resource
        return "/initiative/%s/%s/resource/%s/%s" %(thing['initiativeCode'], thing['initiative_url'], thing['urlCode'], thing['url'])
    else:
        return "/initiative/%s/%s/show" %(thing['urlCode'], thing['url'])
    
def workshopImageURL(workshop, mainImage, thumbnail = False):
    if thumbnail:
        if mainImage['pictureHash'] == 'supDawg':
            return '/images/slide/thumbnail/supDawg.thumbnail'
        elif 'format' in mainImage.keys():
            return '/images/mainImage/%s/thumbnail/%s.%s' %(mainImage['directoryNum'], mainImage['pictureHash'], mainImage['format'])
        else:
            return '/images/mainImage/%s/thumbnail/%s.jpg' %(mainImage['directoryNum'], mainImage['pictureHash'])
    else:
        if mainImage['pictureHash'] == 'supDawg':
            return '/images/slide/slideshow/supDawg.slideshow'
        elif 'format' in mainImage.keys():
            return '/images/mainImage/%s/listing/%s.%s' %(mainImage['directoryNum'], mainImage['pictureHash'], mainImage['format'])
        else:
            return '/images/mainImage/%s/listing/%s.jpg' %(mainImage['directoryNum'], mainImage['pictureHash'])
            
def getPublicScope(item):
    # takes scope string and returns scope level, name, flag and href
    flag = '/images/flags/'
    href = '/workshops/geo/earth'
    if 'scope' in item and item['scope'] != '':
        scope = item['scope'].split('|')
        if scope[9] != '0':
            scopeLevel = 'postalCode'
            scopeName  = scope[9].replace('-', ' ')
            flag += 'generalFlag.gif'
            href += '/' + scope[2] + '/' + scope[4] + '/' + scope[6] + '/' + scope[8] + '/' + scope[9]
        elif scope[8] != '0':
            scopeLevel = 'city'
            scopeName  = scope[8].replace('-', ' ')
            flag += 'country/' + scope[2] + '/states/' + scope[4] + '/counties/' + scope[6] + '/cities/' + scope[8] + '.gif'
            href += '/' + scope[2] + '/' + scope[4] + '/' + scope[6] + '/' + scope[8]
        elif scope[6] != '0':
            scopeLevel = 'county'
            scopeName  = scope[6].replace('-', ' ')
            flag += 'country/' + scope[2] + '/states/' + scope[4] + '/counties/' + scope[6] + '.gif'
            href += '/' + scope[2] + '/' + scope[4] + '/' + scope[6]
        elif scope[4] != '0':
            scopeLevel = 'state'
            scopeName  = scope[4].replace('-', ' ')
            flag += 'country/' + scope[2] + '/states/' + scope[4] + '.gif'
            href += '/' + scope[2] + '/' + scope[4]
        elif scope[2] != '0':
            scopeLevel = 'country'
            scopeName  = scope[2].replace('-', ' ')
            flag += 'country/' + scope[2] + '.gif'
            href += '/' + scope[2]
        else:
            scopeLevel = 'earth'
            scopeName  = 'earth'
            flag += 'earth.gif'
            href += '/0'

        # make sure the flag exists
        baseUrl = config['site_base_url']
        if baseUrl[-1] == "/":
            baseUrl = baseUrl[:-1]
        flag = baseUrl + flag
        try:
            f = urllib2.urlopen(urllib2.Request(flag))
            flag = flag
        except:
            flag = '/images/flags/generalFlag.gif'
    else:
        scopeLevel = 'earth'
        scopeName  = 'earth'
        flag += 'earth.gif'
    return {'level':scopeLevel, 'name':scopeName, 'flag':flag, 'href':href}


workshopInfo = \
"""
The following is a suggested list of sections to include. This background wiki uses Markdown for styling. See the Formatting Guide above for help.


Overview
-----
_A summary of the key ideas associated with your workshop topic._


Stats and Trends
-----
_What are the key indicators by which this workshop topic is measured? What do history and trends suggest about this topic?


Existing Taxes and/or Revenues
-----
_Are there any public taxes associated with your workshop topic? Are there other current funding sources?_


Current Spending
-----
_What money is currently spent on your workshop topic? What might it look like in the future?_


Current Legislation
-----
_What publicly funded programs related to your workshop topic currently exist?_


Case Studies
-----
_How have other groups or regions tackled this workshop topic already?_


"""