from pylowiki.model import Thing, meta
from pylowiki.lib.utils import urlify, toBase62
from dbHelpers import commit
from dbHelpers import with_characteristic as wc
from discussion import Discussion
from page import Page

import logging
log = logging.getLogger(__name__)

def getSuggestionByID(id):
    try:
        return meta.Session.query(Thing).filter_by(id = id).one()
    except:
        return False

def getAllSuggestions(deleted = False):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'suggestion').filter_by(objType = 'suggestion').all()
    except:
        return False

# Note this function is deprecated, use getSuggestionByHash() instead.
def getSuggestionByURL(url):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'suggestion').filter(Thing.data.any(wc('url', url))).all()
    except:
        return False

def getSuggestionsForWorkshop(code, url):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'suggestion').filter(Thing.data.any(wc('workshopCode', code))).filter(Thing.data.any(wc('workshopURL', url))).all()
    except:
        return False

# Takes in a hash and a title - hash for primary lookup, url for collision resolution
def getSuggestion(hash, url):
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
    def __init__(self, owner, title, data, workshop):
        s = Thing('suggestion', owner.id)
        s['title'] = title
        s['url'] = urlify(title)
        s['urlCode'] = toBase62('%s_%s'%(title, owner['name']))
        s['data'] = data
        s['workshopCode'] = workshop['urlCode']
        s['workshopURL'] = workshop['url']
        s['numComments'] = 0
        log.info('data = %s' % data)
        commit(s)
        self.s = s
        
        # Should this be set to the owner, or be ownerless?
        d = Discussion('suggestion')
        s['discussion_id'] = d.d.id
        p = Page(title, owner, s, data)
        commit(s)