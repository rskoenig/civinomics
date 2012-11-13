from pylowiki.model import Thing, meta
from pylowiki.lib.utils import urlify, toBase62
from pylowiki.lib.db.flag import checkFlagged
from dbHelpers import commit
from dbHelpers import with_characteristic as wc
from discussion import Discussion
from revision import Revision
from page import Page
from time import time
from rating import Rating
import pylowiki.lib.db.generic as generic
import logging
log = logging.getLogger(__name__)

def getSuggestionByID(id):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'suggestion').filter_by(id = id).one()
    except:
        return False

def getAllSuggestions(deleted = '0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'suggestion').filter_by(objType = 'suggestion').all()
    except:
        return False

# Note this function is deprecated, use getSuggestion() instead.
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

def getActiveSuggestionsForWorkshop(code, url="deprecated"):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'suggestion').filter(Thing.data.any(wc('workshopCode', code))).filter(Thing.data.any(wc('adopted', '0'))).filter(Thing.data.any(wc('disabled', '0'))).filter(Thing.data.any(wc('deleted', '0'))).all()
    except:
        return False

def getAdoptedSuggestionsForWorkshop(code, url):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'suggestion').filter(Thing.data.any(wc('workshopCode', code))).filter(Thing.data.any(wc('workshopURL', url))).filter(Thing.data.any(wc('adopted', '1'))).filter(Thing.data.any(wc('disabled', '0'))).filter(Thing.data.any(wc('deleted', '0'))).all()
    except:
        return False

def getDisabledSuggestionsForWorkshop(code, url):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'suggestion').filter(Thing.data.any(wc('workshopCode', code))).filter(Thing.data.any(wc('workshopURL', url))).filter(Thing.data.any(wc('disabled', '1'))).all()
    except:
        return False

def getDeletedSuggestionsForWorkshop(code, url):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'suggestion').filter(Thing.data.any(wc('workshopCode', code))).filter(Thing.data.any(wc('workshopURL', url))).filter(Thing.data.any(wc('deleted', '1'))).all()
    except:
        return False

def getInactiveSuggestionsForWorkshop(code, url):
    InactiveSugs = []
    DisabledSugs = getDisabledSuggestionsForWorkshop(code, url)
    DeletedSugs = getDeletedSuggestionsForWorkshop(code, url)
    if DisabledSugs:
        InactiveSugs = DisabledSugs
    if DeletedSugs:
        InactiveSugs += DeletedSugs
    if DisabledSugs or DeletedSugs:
        return InactiveSugs
    else:
        return False

def getFlaggedSuggestionsForWorkshop(code, url):
    try:
        sList = meta.Session.query(Thing).filter_by(objType = 'suggestion').filter(Thing.data.any(wc('workshopCode', code))).filter(Thing.data.any(wc('workshopURL', url))).all()
        fList = []
        for s in sList:
           if checkFlagged(s) and s.id not in sList:
              fList.append(s.id)

        return fList
    except:
        return False

# Takes in a hash and a title - hash for primary lookup, url for collision resolution
def getSuggestion(hash, url):
    try:
        q = meta.Session.query(Thing).filter_by(objType = 'suggestion').filter(Thing.data.any(wc('urlCode', hash))).all()
        if len(q) == 1:
            return q[0]
        else:
            q = meta.Session.query(Thing).filter_by(objType = 'suggestion').filter(Thing.data.any(wc('urlCode', hash))).filter(Thing.data.any(wc('url', url))).all()
            if len(q) == 1:
                return q[0]
            else:
                log.error('Unresolvable collision when getting suggestion for hash = %s, url = %s'%(hash, url))
                return False
    except:
        return False
    
# owner is a Thing object
# title is a string
class Suggestion(object):
    def __init__(self, owner, title, data, allowComments, workshop):
        s = Thing('suggestion', owner.id)
        s['title'] = title
        s['url'] = urlify(title[:30])
        s['data'] = data
        #s['workshopCode'] = workshop['urlCode']
        #s['workshopURL'] = workshop['url']
        s = generic.linkChildToParent(s, workshop)
        s['allowComments'] = allowComments
        s['numComments'] = 0
        s['disabled'] = '0'
        s['deleted'] = '0'
        s['adopted'] = '0'
        ##log.info('data = %s' % data)
        commit(s)
        s['urlCode'] = toBase62(s)
        self.s = s
        
        r = Revision(owner, data, s)
        s['mainRevision_id'] = r.r.id
        
        # Should this be set to the owner, or be ownerless?
        d = Discussion(title='suggestion', attachedThing = s, workshop = workshop, discType = 'suggestion')
        s['discussion_id'] = d.d.id
        p = Page(title, owner, s, data)
        if 'numSuggestions' not in owner.keys():
            owner['numSuggestions'] = 1
        else:
            owner['numSuggestions'] = int(owner['numSuggestions']) + 1
        
        if 'suggestionList' not in owner.keys():
            owner['suggestionList'] = s.id
        else:
            owner['suggestionList'] = owner['suggestionList'] + ',' + str(s.id)
        commit(owner)
        
        rateAmount = 50
        thisRating = Rating(rateAmount, s, owner, 'overall')
        commit(s)
