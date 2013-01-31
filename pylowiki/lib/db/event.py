#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic as wc

log = logging.getLogger(__name__)

def getEvent(id):
    try:
        return meta.Session.query(Thing).filter_by(id = id).one()
    except:
        return False

def getParentEvents(parent):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'event').filter(Thing.data.any(wc('parent_id', parent.id))).order_by('-date').all()
    except:
        return False

def getEventsWithAction(parent, action):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'event')\
            .filter(Thing.data.any(wc('parent_id', parent.id)))\
            .filter(Thing.data.any(sa.and_(Data.key == u'action', Data.value == action)))\
            .order_by('-date')\
            .all()
    except:
        return False

def get_all_events():
    try:
        return meta.Session.query(Thing).filter_by(objType = 'event').all()
    except:
        return False

def getCommentEvent(comID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'event').filter(Thing.data.any(wc('parent_id', comID))).all()
    except:
        return False

# May not be needed.  Title is a short descriptor, data is a longer descriptor.
# In the relational model, event was used as a sort of metatable to keep track
# of things that happened (User makes a change, page is created, etc...)
class Event(object):
    def __init__(self, title, data, parent, user = None, **kwargs):
        if user == None:
            user = 0
        else:
            user = user.id
        e = Thing('event', user)
        e['title'] = title
        e['data'] = data
        e['parent_id'] = parent.id
        if 'reason' in kwargs:
            e['reason'] = kwargs['reason']
        if 'action' in kwargs:
            e['action'] = kwargs['action']
        commit(e)
        self.e = e
