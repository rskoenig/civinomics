import logging

from urllib import quote

log = logging.getLogger(__name__)

def urlify(url):
    url = url.strip()
    url = url.lower()
    url = url.replace(' ', '-')
    url = url.encode('utf8')
    url = quote(url)
    return url