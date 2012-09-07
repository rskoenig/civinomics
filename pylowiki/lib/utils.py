import logging, string

from urllib import quote
from zlib import adler32

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
