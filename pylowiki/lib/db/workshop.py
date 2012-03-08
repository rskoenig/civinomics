from pylowiki.model import Thing, meta
from pylowiki.lib.utils import urlify, toBase62
from dbHelpers import commit, with_characteristic
from page import Page
from event import Event

import time

# Only support for one facilitator.  Otherwise we need to make a list and add/remove from it
def changeFacilitator(workshop, facilitator):
    workshop['facilitator'] = facilitator
    commit(workshop)
    return True

def getWorkshopByID(id):
    try:
        return meta.Session.query(Thing).filter_by(id = id).one()
    except:
        return False

# Note that this may return multiple objects if they share the same name
def getWorkshopByTitle(title):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'workshop').filter(Thing.data.any(with_characteristic('title', title))).all()
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
    def __init__(self, title, owner):
        w = Thing('workshop', owner.id)
        w['title'] = title
        w['url'] = urlify(title)
        w['urlCode'] = toBase62('%s_%s_%d'%(title, owner['name'], int(time.time())))
        
        # def __init__(self, title, owner, type):
        p = Page(title, owner.id, 'workshop')
        
        #def __init__(self, title, data, user = None):
        e = Event('Create workshop', 'User %s created a workshop'%(owner.id))
        
        commit(w)
        commit(p)
        commit(e)
