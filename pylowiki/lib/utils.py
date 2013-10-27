import logging, string

from urllib import quote
from zlib import adler32
from pylons import session, tmpl_context as c
import pylowiki.lib.db.follow       as followLib
import pylowiki.lib.db.generic      as generic

log = logging.getLogger(__name__)

# For base62 conversion
BASE_LIST = string.digits + string.letters
BASE_DICT = dict((c, i) for i, c in enumerate(BASE_LIST))

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
            return baseURL + "/photo/show/" + thing['urlCode'] 
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
            

workshopInfo = \
"""
Quick Markdown Syntax Guide
===========================

This guide shows you how to use Markdown instead of HTML when
writing background information.

Markdown simplifies the HTML rendering

Links
-----

Raw links: <http://civ.io>

Links with [text](http://civ.io).

You can add hover words(which show up under the cursor), 
[like this](http://civ.io "Hovering text").

Text
----

There are *two* ways to _italicize_ (or emphasize) text.

Blank lines separate paragraphs.

So this is a new paragraph. But any text on adjacent lines
will all end up 
in the same paragraph.

Quoting
----------
> This is quoted *like email*
Even though this line doesn't have the '>' character, it's still part of the same paragraph, so it's still quoted.

This paragraph is not quoted.

Literal text
----------------

You can use `*backquotes*` to mark certain sections as literal text (Note it is not italicized)

    You can apply this to entire paragraphs by starting with four spaces
    These two lines start off with four spaces.

Lists
--------
Bulleted lists

* Asterisks
* make
* unordered
* lists

Numbered lists

1. numbers
2. make
3. numbered
4. lists
1. the number used does not matter        

Headers
----------

# Biggest #
## Big ##
### Medium-big ###
#### Medium-small ####
##### Smaller #####
###### smallest

None of these require us to wrap both sides with hashes.
"""