from pylowiki.model import Thing, meta
from pylowiki.lib.utils import urlify, toBase62
from dbHelpers import commit, with_characteristic as wc
from page import Page
from event import Event
from revision import Revision

import time
import logging

log = logging.getLogger(__name__)

# Only support for one facilitator.  Otherwise we need to make a list and add/remove from it
def changeFacilitator(workshop, facilitator):
    workshop['facilitator'] = facilitator
    commit(workshop)
    return True

def getWorkshops( deleted = False):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'workshop').filter(Thing.data.any(wc('deleted', deleted))).all()
    except:
        return False

# TODO: Add in a check for object type
def getWorkshopByID(id):
    try:
        return meta.Session.query(Thing).filter_by(id = id).one()
    except:
        return False

def getWorkshop(code, url):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'workshop').filter(Thing.data.any(wc('urlCode', code))).filter(Thing.data.any(wc('url', url))).one()
    except:
        return False

# Note that this may return multiple objects if they share the same name
def getWorkshopByTitle(title):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'workshop').filter(Thing.data.any(wc('title', title))).all()
    except:
       return False 

# requires a 'participants' field for the queried object
def getParticipantsByID(id):
    try:
        return meta.Session.query(Thing).filter_by(id = id).one()['participants']
    except:
        return False

class Workshop(object):
    # title -> A string
    # owner -> A user object in Thing form
    #
    # Note this will generate the page and event for you.
    def __init__(self, title, owner, day, month, year, background, goals):
        w = Thing('workshop', owner.id)
        w['title'] = title
        w['url'] = urlify(title)
        w['urlCode'] = toBase62('%s_%s_%d'%(title, owner['name'], int(time.time())))
        # time.strptime("%s %s %s"%(day, month, year), "%d %m %Y")
        w['endTime'] = '%s %s %s' %(day, month, year)
        w['deleted'] = False
        w['facilitators'] = owner.id
        w['goals'] = goals
        w['numArticles'] = 1
        commit(w)
        self.w = w
        
        # def __init__(self, title, owner, type):
        p = Page(title, owner, w)
        r = Revision(owner, background, p.p.id)
        
        #def __init__(self, title, data, user = None):
        e = Event('Create workshop', 'User %s created a workshop'%(owner.id))
        
        
