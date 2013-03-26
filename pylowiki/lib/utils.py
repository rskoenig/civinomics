import logging, string

from urllib import quote
from zlib import adler32
from pylons import session, tmpl_context as c
import pylowiki.lib.db.follow       as followLib

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
  
def thingURL(workshop, thing):
    return "/workshop/%s/%s/%s/%s/%s" %(workshop['urlCode'], workshop['url'], thing.objType, thing['urlCode'], thing['url'])
    
def workshopImageURL(workshop, mainImage):
    if mainImage['pictureHash'] == 'supDawg':
        return '/images/slide/slideshow/supDawg.slideshow'
    else:
        return '/images/mainImage/%s/listing/%s.jpg' %(mainImage['directoryNum'], mainImage['pictureHash'])
    