import logging, string
import requests

from urllib import quote
from zlib import adler32
from pylons import session, tmpl_context as c
from hashlib import md5
from pylons import tmpl_context         as c, config, session
import pylowiki.lib.db.follow           as followLib
import pylowiki.lib.db.generic          as generic
import pylowiki.lib.fuzzyTime           as fuzzyTime    

import urllib2
import datetime

import misaka as m
import copy as copy
from HTMLParser import HTMLParser

log = logging.getLogger(__name__)

# For base62 conversion
BASE_LIST = string.digits + string.letters
BASE_DICT = dict((c, i) for i, c in enumerate(BASE_LIST))

###################################
# MLStripper is part of the process of 
# stripping html from misaka's markdown output
###################################
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

##################################################
# simple email checker
##################################################
def badEmail(email):
    log.info("fx checking for bad Email: %s"%email)
    if email.find('@') < 0:
        # if there's not an @ in the string this is a bad email
        return True
    else:
        return False
# validate proper date format
def validate_date(dateString):
    try:
        datetime.datetime.strptime(dateString, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    
    
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

##################################################
# simple string capper
##################################################
def cap(s, l):
    return s if len(s)<=l else s[0:l-3]+'...'

##################################################
# location of our avatar image
##################################################
def civinomicsAvatar():
    return "/images/handdove_medium.png"

##################################################
# create a link to a comment
##################################################
def commentLinker(comment):
    itemLink = ''
    if 'discType' in comment and comment['discType'] == 'organization_general':
        itemLink = '/profile/' + comment['profileCode'] + '/' + comment['profile_url']  + '/discussion/show/' + comment['discussionCode']
    elif 'discType' in comment and comment['discType'] == 'organization_position':
        itemLink = '/profile/' + comment['profileCode'] + '/' + comment['profile_url']  + '/position/show/' + comment['discussionCode']
    elif 'initiativeCode' in comment:
        if 'resourceCode' in comment:
            # this is a comment on a resource in an initiative
            itemLink = '/initiative/' + comment['initiativeCode'] + '/' +  comment['initiative_url'] + '/resource/' + comment['resourceCode'] + '/' + comment['parent_url']
        elif comment['parent_url'] == comment['initiative_url']:
            # this is an initiative
            itemLink = '/initiative/' + comment['initiativeCode'] + '/' +  comment['initiative_url'] + '/show'
        elif comment['parent_url'] != comment['initiative_url']:
            # this is a comment on an initiative update
            itemLink = '/initiative/' + comment['initiativeCode'] + '/' +  comment['initiative_url'] + '/updateShow/' + comment['discussionCode']
    elif 'workshopCode' in comment:
        if 'ideaCode' in comment:
            # /workshop/4OOt/civinomicon-transportation/idea/4PUI/explore-ferry-servic
            itemLink = '/workshop/' + comment['workshopCode'] + '/' +  comment['workshop_url'] + '/idea/' + comment['ideaCode'] + '/' + comment['parent_url']
        elif 'resourceCode' in comment:
            # this is a comment on a resource in a workshop
            itemLink = '/workshop/' + comment['workshopCode'] + '/' +  comment['workshop_url'] + '/resource/' + comment['resourceCode'] + '/' + comment['parent_url']
        else:
            # this is a discussion in a workshop
            # /workshop/4OOt/civinomicon-transportation/discussion/4SKj/no-fin
            itemLink = '/workshop/' + comment['workshopCode'] + '/' +  comment['workshop_url'] + '/discussion/' + comment['discussionCode'] + '/' + comment['parent_url']
    elif 'photoCode' in comment:
        # this is a comment on a photo
        itemLink = '/profile/' + comment['profileCode'] + '/' + comment['profile_url']  + '/photo/show/' + comment['photoCode']
    elif 'profileCode' in comment:
        # I don't like this because it is not explicit what kind of comment this is, this is an implicit fallthrough case, ugh
        itemLink = '/profile/' + comment['profileCode'] + '/' + comment['profile_url']  + '/discussion/show/' + comment['discussionCode']

    return itemLink

##################################################
# returns the base url without an ending '/'
##################################################
def getBaseUrl():
    baseUrl = config['site_base_url']
    # for creating a link, we need to make sure baseUrl doesn't have an '/' on the end
    if baseUrl[-1:] == "/":
        baseUrl = baseUrl[:-1]
    return baseUrl

def geoDeurlify( something ):
    deurl = something.replace('-', ' ')
    return deurl.title() 

def getGeoExceptions():
    geoExceptions = {
        'San Francisco' : 'County',
    }

    return geoExceptions

def getPublicScope(item):
    # takes an item with scope attribute and returns scope level, name, flag and href
    flag = '/images/flags/'
    href = '/workshops/geo/earth'
    scope = None
    scopeString = ''
    if 'scope' in item and item['scope'] != '':
        scope = item['scope'].split('|')
    elif 'workshop_public_scope' in item and item['workshop_public_scope'] != '':
        scope = item['workshop_public_scope'].split('|')
    elif '|' in item:
        scope = item.split('|')
    if scope:
        if scope[2] != '0':
            scopeLevel = 'country'
            scopeName  = scope[2].replace('-', ' ').title()
            scopeString = scopeName
            flag += 'country/' + scope[2]
            href += '/' + scope[2]
            if scope[4] != '0':
                scopeLevel = 'state'
                scopeName  = scope[4].replace('-', ' ').title()
                scopeString += ', State of %s' % scopeName
                flag += '/states/' + scope[4]
                href += '/' + scope[4]
                if scope[6] != '0':
                    scopeLevel = 'county'
                    scopeName  = scope[6].replace('-', ' ').title()
                    scopeString += ', County of %s' % scopeName
                    flag += '/counties/' + scope[6]
                    href += '/' + scope[6]
                    if scope[8] != '0':
                        scopeLevel = 'city'
                        scopeName  = scope[8].replace('-', ' ').title()
                        scopeString += ', City of %s' % scopeName
                        flag += '/cities/' + scope[8]
                        #log.info('The city flag url is %s' % flag)
                        href += '/' + scope[8]
                        if scope[9] != '0':
                            scopeLevel = 'postalCode'
                            scopeName  = scope[9].replace('-', ' ').title()
                            scopeString += ', Zip Code %s' % scopeName
                            flag += 'generalFlag.gif'
                            href += '/' + scope[9]
            flag += '.gif'
        else:
            scopeLevel = 'earth'
            scopeName  = 'Earth'
            scopeString  = 'Earth'
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
    scopeLevel = scopeLevel.title()
    return {'level':scopeLevel, 'name':scopeName, 'scopeString':scopeString, 'flag':flag, 'href':href}

def getTextFromMisaka(content):
    # create html-free description for sharing on facebook
    contentCopy = copy.copy(content)
    contentHtml = m.html(contentCopy, render_flags=m.HTML_SKIP_HTML)
    s = MLStripper()
    s.feed(contentHtml)
    contentWithLineBreaks = s.get_data()
    contentNoLineBreaks = contentWithLineBreaks.replace('\n', ' ').replace('\r', '')
    return contentNoLineBreaks

def initiativeURL(thing):
    #log.info("objType is %s"%thing.objType)
    if thing.objType == 'resource':
        # an initiative resource
        return "/initiative/%s/%s/resource/%s/%s" %(thing['initiativeCode'], thing['initiative_url'], thing['urlCode'], thing['url'])
    elif thing.objType == 'discussion' and thing['discType'] == 'update':
        returnURL =  "/initiative/%s/%s/updateShow/%s" %(thing['initiativeCode'], thing['initiative_url'], thing['urlCode'])
        #log.info("return URL is %s"%returnURL)
        return "/initiative/%s/%s/updateShow/%s" %(thing['initiativeCode'], thing['initiative_url'], thing['urlCode'])
    else:
        return "/initiative/%s/%s/show" %(thing['urlCode'], thing['url'])
        
def initiativeImageURL(i):
    if 'directoryNum_photos' in i and 'pictureHash_photos' in i:
        photo_url = "/images/photos/%s/photo/%s.png"%(i['directoryNum_photos'], i['pictureHash_photos'])
        thumbnail_url = "/images/photos/%s/thumbnail/%s.png"%(i['directoryNum_photos'], i['pictureHash_photos'])
    else:
        photo_url = "/images/icons/generalInitiative.jpg"
        thumbnail_url = "/images/icons/generalInitiative.jpg"
    bgPhoto_url = "'" + photo_url + "'"
    return (bgPhoto_url, photo_url, thumbnail_url)

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

def isWatching(user, workshop):
   # Even though the functions use the verb 'following', the mechanism is the same...we just display 
   # object follows as 'watching'.
   c.isFollowing = followLib.isFollowing(user, workshop)

def photoLink(photoCode, parent):
    photoStr = '/profile/%s/%s/photo/show/%s' %(parent["urlCode"], parent["url"], photoCode)    
    return photoStr

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

def profilePhotoURL(thing):
    owner = generic.getThing(thing['userCode'])

    return "/profile/%s/%s/photo/show/%s" %(owner['urlCode'], owner['url'], thing['urlCode'])
    

def profileDiscussionURL(thing):
    owner = generic.getThing(thing['userCode'])
    if thing['discType'] == 'organization_general':
        dType = 'discussion'
    else:
        dType = 'position'

    return "/profile/%s/%s/%s/show/%s" %(owner['urlCode'], owner['url'], dType, thing['urlCode'])
    
##################################################
# generates a url for a thing
# kwarg returnTitle gets the title out of the thing as well.
##################################################
def thingURL(thingParent, thing, **kwargs):
    thingUrl = True
    
    if thingParent.objType.replace("Unpublished", "") == 'workshop':
        parentBase = "workshop"
    elif thingParent.objType.replace("Unpublished", "") == 'user':
        parentBase = "profile"
    elif thingParent.objType.replace("Unpublished", "") == 'initiative':
        parentBase = "initiative"
    baseURL = '/%s/%s/%s' % (parentBase, thingParent['urlCode'], thingParent['url'])
    if thing.objType.replace("Unpublished", "") == 'photo':
        returnString = baseURL + "/photo/show" + thing['urlCode']
        thingUrl = False
    if thing.objType.replace("Unpublished", "") == 'initiative':
        returnString = baseURL + "/show"
        thingUrl = False
    if thing.objType.replace("Unpublished", "") == 'comment':
        if 'ideaCode' in thing.keys():
            thing = generic.getThing(thing['ideaCode'])
        elif 'resourceCode' in thing.keys():
            thing = generic.getThing(thing['resourceCode'])
        elif 'photoCode' in thing.keys():
            thing = generic.getThing(thing['photoCode'])
            returnString = baseURL + "/photo/show/" + thing['urlCode'] 
            thingUrl = False
        elif 'initiativeCode' in thing.keys():
            thing = generic.getThing(thing['initiativeCode'])
            returnString = baseURL + "/show/" 
            thingUrl = False
        elif 'discussionCode' in thing.keys():
            thing = generic.getThing(thing['discussionCode'])
        else:
            returnString = baseURL
            thingUrl = False
    if thingUrl:
        if thing.objType == 'discussion' and thing['discType'] == 'organization_general':
            returnString = "/profile/%s/%s/discussion/show/%s"%(thing['userCode'], thing['user_url'], thing['urlCode'])
        elif thing.objType == 'discussion' and thing['discType'] == 'organization_position':
            returnString = "/profile/%s/%s/position/show/%s"%(thing['userCode'], thing['user_url'], thing['urlCode'])
        else:
            returnString = baseURL + "/%s/%s/%s" %(thing.objType, thing['urlCode'], thing['url'])
            
    if 'returnTitle' in kwargs:
        if kwargs['returnTitle'] == True:
            try:
                views = thing['views']
            except:
                views = 0
                pass
            try:
                title = thing['title']
            except:
                title = ''
                pass
            return views, title, returnString
        else:
            return returnString
    else:
        return returnString

##################################################
#    Takes in a string 's', returns a base-62 representation of a hash of that string.
#    Used for generating short-form codes within URLs.  If a collision occurs, a secondary
#    match will need to be used.  For example, matching a workshop's code and title if the
#    workshop's code results in a collision.
##################################################
def toBase62(thing):
    s = str(thing.id + 1124816) # Offset by 1-1-2-4-8-16; first 5 numbers in Fibbonacci sequence
    #num = adler32(s)
    num = int(s)
    if num < 0: num = -num
    return base_encode(num)

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

def _userImageSource(user, **kwargs):
    # Assumes 'user' is a Thing.
    # Defaults to a gravatar source
    # kwargs:   forceSource:   Instead of returning a source based on the user-set preference in the profile editor,
    #                          we return a source based on the value given here (civ/gravatar)
    source = 'http://www.gravatar.com/avatar/%s?r=pg&d=identicon' % md5(user['email']).hexdigest()
    large = False
    gravatar = True

    if 'className' in kwargs:
        if 'avatar-large' in kwargs['className']:
            large = True
    if 'forceSource' in kwargs:
        if kwargs['forceSource'] == 'civ':
            gravatar = False
            if 'directoryNum_avatar' in user.keys() and 'pictureHash_avatar' in user.keys():
                source = '/images/avatar/%s/avatar/%s.png' %(user['directoryNum_avatar'], user['pictureHash_avatar'])
            else:
                source = '/images/hamilton.png'
        elif kwargs['forceSource'] == 'facebook':
            log.info("Forced!")
            if large:
                source = user['facebookProfileBig']
            else:
                source = user['facebookProfileSmall']
            if len(source) == 0:
                if 'facebookAuthId' in user:
                    graphUrl = 'https://graph.facebook.com/' + user['facebookAuthId'] + '/picture?height=200&type=normal&width=200'
                    response = requests.request("GET", graphUrl)
                    source = response.url
        elif kwargs['forceSource'] == 'twitter':
            source = user['twitterProfilePic']

    else:
        if 'avatarSource' in user.keys():
            if user['avatarSource'] == 'civ':
                if 'directoryNum_avatar' in user.keys() and 'pictureHash_avatar' in user.keys():
                    source = '/images/avatar/%s/avatar/%s.png' %(user['directoryNum_avatar'], user['pictureHash_avatar'])
                    gravatar = False
            elif user['avatarSource'] == 'facebook':
                log.info("Source!")
                gravatar = False
                if large:
                    source = user['facebookProfileBig']
                else:
                    source = user['facebookProfileSmall']
                if len(source) == 0:
                    if 'facebookAuthId' in user:
                        graphUrl = 'https://graph.facebook.com/' + user['facebookAuthId'] + '/picture?height=200&type=normal&width=200'
                        response = requests.request("GET", graphUrl)
                        source = response.url
            elif user['avatarSource'] == 'twitter':
                gravatar = False
                source = user['twitterProfilePic']

        elif 'extSource' in user.keys():
            # this is needed untl we're sure all facebook connected users have properly 
            # functioning profile pics - the logic here is now handled 
            # with the above user['avatarSource'] == 'facebook': ..
            if 'facebookSource' in user.keys():
                if user['facebookSource'] == u'1':
                    log.info("Keys!")
                    gravatar = False
                    # NOTE - when to provide large or small link?
                    if large:
                        source = user['facebookProfileBig']
                    else:
                        source = user['facebookProfileSmall']
                    if len(source) == 0:
                        if 'facebookAuthId' in user:
                            graphUrl = 'https://graph.facebook.com/' + user['facebookAuthId'] + '/picture?height=200&type=normal&width=200'
                            response = requests.request("GET", graphUrl)
                            source = response.url
    if large and gravatar:
        source += '&s=200'
    return source

# return a link to this user's profile page
def userLink(user):
    return "/profile/%s/%s/" %(user['urlCode'], user['url'])

# return this user's name
def userName(user):
    return user['name']

def workshopURL(w, **kwargs):
    return "/workshop/%s/%s" %(w['urlCode'], w['url'])

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

workshopInfo = \
"""
The following is a suggested list of sections to include. This background wiki uses Markdown for styling. See the Formatting Guide above for help.


Overview
-----
_A summary of the key ideas associated with your workshop topic._


Stats and Trends
-----
_What are the key indicators by which this workshop topic is measured? What do history and trends suggest about this topic?_


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

initiativeFields = \
"""
Background
-----

_incl. reference to Current Legislation_


Proposal
-----


Fiscal Effects
-----


"""