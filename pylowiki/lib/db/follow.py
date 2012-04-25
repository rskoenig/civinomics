#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, meta
from dbHelpers import commit, with_characteristic as wc

log = logging.getLogger(__name__)

# Getters
# Who is following the workshop
def getWorkshopFollowers( workshopID, disabled = False):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'follow').filter(Thing.data.any(wc('disabled', disabled))).filter(Thing.data.any(wc('thingID', workshopID))).filter(Thing.data.any(wc('thingType', 'workshop'))).all()
    except:
        return False

# Who is following the user
def getUserFollowers( userID, disabled = False):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'follow').filter(Thing.data.any(wc('disabled', disabled))).filter(Thing.data.any(wc('thingID', userID))).filter(Thing.data.any(wc('thingType', 'user'))).all()
    except:
        return False

# Which workshops is the user following
def getWorkshopFollows( userID, disabled = False):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'follow').filter_by(owner = userID).filter(Thing.data.any(wc('disabled', disabled))).filter(Thing.data.any(wc('thingType', 'workshop'))).all()
    except:
        return False

# Which users is the user following
def getUserFollows( userID, disabled = False):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'follow').filter_by(owner = userID).filter(Thing.data.any(wc('disabled', disabled))).filter(Thing.data.any(wc('thingType', 'user'))).all()
    except:
        return False

# get the Follow object for this user and thing
def getFollow( userID, thingID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'follow').filter_by(owner = userID).filter(Thing.data.any(wc('thingID', thingID))).one()
    except:
        return False

# is the user following the thing
def isFollowing(userID, thingID):
    try:
        f = meta.Session.query(Thing).filter_by(objType = 'follow').filter_by(owner = userID).filter(Thing.data.any(wc('thingID', thingID))).all()
        if f:
           return True
        else:
           return False
    except:
        return False

# Setters
def unfollow( userID, thingID ):
    f =  meta.Session.query(Thing).filter_by(objType = 'follow').filter_by(owner = userID).filter(Thing.data.any(wc('thingID', thingID))).one()
    f['disabled'] = True
    commit(f)

# Object
class Follow(object):
    def __init__(self, userID, thingID, thingType, disabled = False):
        f = Thing('follow', userID)
        f['thingID'] = thingID
        f['thingType'] = thingType
        f['disabled'] = disabled
        commit(f)

