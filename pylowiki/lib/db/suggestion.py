from pylowiki.model import Thing, meta
from pylowiki.lib.utils import urlify, toBase62
from dbHelpers import commit
from dbHelpers import with_characteristic as wc

import logging
log = logging.getLogger(__name__)

def getSuggestionByID(id):
    try:
        return meta.Session.query(Thing).filter_by(id = id).one()
    except:
        return False

def getAllSuggestions(deleted = False):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'suggestion').all()
    except:
        return False

# Note this function is deprecated, use getSuggestionByHash() instead.
def getSuggestionByURL(url):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'suggestion').filter(Thing.data.any(wc('url', url))).all()
    except:
        return False
    
# Note this function is deprecated, use getSuggestionByHash() instead.
def getSuggestion(title, issue_id):
    try:
        return False
    except:
        return False

# Takes in a hash and a title - hash for primary lookup, url for collision resolution
def getSuggestionByHash(hash, url):
    try:
        q = meta.Session.query(Thing).filter_by(objType = 'suggestion').filter(Thing.data.any(wc('urlCode', hash)))
        if len(q) == 1:
            return q.one()
        else:
            q = meta.Session.query(Thing).filter_by(objType = 'suggestion').filter(Thing.data.any(wc('urlCode', hash))).filter(Thing.data.any(wc('url', url)))
            if len(q) == 1:
                return q.one()
            else:
                log.error('Unresolvable collision when getting suggestion for hash = %s, url = %s'%(hash, url))
                return False
    except:
        return False
    
# owner is a Thing object
# title is a string
class Suggestion(object):
    def __init__(self, title, owner):
        s = Thing('suggestion', owner.id)
        s['title'] = title
        s['url'] = urlify(title)
        s['urlCode'] = toBase62('%s_%s'%(title, owner['name']))
        
