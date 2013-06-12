#-*- coding: utf-8 -*-
import logging

from sqlalchemy import and_
from pylowiki.model import Thing, Data, meta
import pylowiki.lib.db.generic as generic
from dbHelpers import commit, with_characteristic as wc

log = logging.getLogger(__name__)

# Getters
# Who is following the workshop
def getWorkshopFollowers( workshop, disabled = '0', count = False):
    try:
        query = meta.Session.query(Thing)\
            .filter_by(objType = 'follow')\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .filter(Thing.data.any(wc('workshopCode', workshop['urlCode'])))
        if count:
            return query.count()
        return query.all()
    except:
        return False

# Who is following the user
def getUserFollowers( user, disabled = '0'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'follow')\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .filter(Thing.data.any(wc('userCode', user['urlCode']))).all()
    except:
        return False

# Which workshops is the user following
def getWorkshopFollows( user, disabled = '0'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'follow')\
            .filter_by(owner = user.id)\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .filter(Thing.data.any(and_(Data.key == u'workshopCode'))).all()
    except:
        return False

# Which users is the user following
def getUserFollows( user, disabled = '0'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'follow')\
            .filter_by(owner = user.id)\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .filter(Thing.data.any(and_(Data.key == u'userCode'))).all()
    except:
        return False

# get the Follow object for this user and thing
def getFollow( user, thing ):
    try:
        thingCode = '%sCode' % thing.objType
        return meta.Session.query(Thing)\
            .filter_by(objType = 'follow')\
            .filter_by(owner = user.id)\
            .filter(Thing.data.any(wc(thingCode, thing['urlCode']))).one()
    except:
        return False

# is the user following the thing
def isFollowing(user, thing):
    try:
        thingCode = '%sCode' % thing.objType
        f = meta.Session.query(Thing)\
            .filter_by(objType = 'follow')\
            .filter_by(owner = user.id)\
            .filter(Thing.data.any(wc('disabled', False)))\
            .filter(Thing.data.any(wc(thingCode, thing['urlCode']))).all()
        if f:
           return True
        else:
           return False
    except:
        return False

# Object creation/modification here
def FollowOrUnfollow(user, thing, disabled = '0'):
    # We link the follow object to the user and the thing being followed.  The follow object is set up as a child of both, and points to both.
    # The link to the user is done by the 'owner' property (dot notation), and the link to the thing is done by the 'thingCode' attribute
    # (dict notation).
    try:
        f = getFollow(user, thing)
        if f:
            # Ugly hack to reverse the bit when it's stored as a string
            f['disabled'] = str(int(not int(f['disabled'])))
            commit(f)
            return True
        f = Thing('follow', user.id)
        generic.linkChildToParent(f, thing)
        f['itemAlerts'] = '0'
        f['digest'] = '0'
        f['disabled'] = disabled
        commit(f)
        return True
    except:
        return False
        