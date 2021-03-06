#-*- coding: utf-8 -*-
import logging
import pickle

from sqlalchemy import and_
from pylons import session, tmpl_context as c
from pylowiki.model import Thing, Data, meta
import pylowiki.lib.db.generic as generic
from dbHelpers import commit, with_characteristic as wc

log = logging.getLogger(__name__)

# Getters
# Who is following the workshop
def getWorkshopFollowers( workshop, disabled = '0'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'follow')\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .filter(Thing.data.any(wc('workshopCode', workshop['urlCode']))).all()
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

def setWorkshopFollowsInSession(fwdisabled = '0'):
    if 'bookmarkedWorkshops' not in c.authuser:
        bookmarked = getWorkshopFollows(c.authuser, disabled = fwdisabled)
        if bookmarked:
            bookmarkedWorkshops = [ followObj['workshopCode'] for followObj in bookmarked ]
        else:
            bookmarkedWorkshops = []
        c.authuser['bookmarkedWorkshops'] = str(pickle.dumps(bookmarkedWorkshops))
        commit(c.authuser)
    else:
        bookmarkedWorkshops = pickle.loads(str(c.authuser['bookmarkedWorkshops']))
        
    session["bookmarkedWorkshops"] = bookmarkedWorkshops
    session.save()

# Which initiatives is the user following
def getInitiativeFollows( user, disabled = '0'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'follow')\
            .filter_by(owner = user.id)\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .filter(Thing.data.any(and_(Data.key == u'initiativeCode'))).all()
    except:
        return False
        
def setInitiativeFollowsInSession(idisabled = '0'):
    if 'bookmarkedInitiatives' not in c.authuser:
        bookmarkedInitiatives = []
        bookmarked = getInitiativeFollows(c.authuser)
        if bookmarked:
            initiativeList = [ generic.getThing(followObj['initiativeCode']) for followObj in bookmarked ]
            for i in initiativeList:
                if i.objType == 'initiative':
                    if i['public'] == '1':
                        if i['deleted'] != '1':
                            bookmarkedInitiatives.append(i['urlCode'])
        else:
            bookmarkedInitiatives = []
        c.authuser['bookmarkedInitiatives'] = str(pickle.dumps(bookmarkedInitiatives))
        commit(c.authuser)
    else:
        bookmarkedInitiatives = pickle.loads(str(c.authuser['bookmarkedInitiatives']))
        
    session["bookmarkedInitiatives"] = bookmarkedInitiatives
    session.save()
    
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
        
def setUserFollowsInSession(udisabled = '0'):
    if 'followingUsers' not in c.authuser:
        following = getUserFollows(c.authuser, disabled = udisabled)
        if following:
            userList = [ generic.getThing(followObj['userCode']) for followObj in following ]
            followingUsers = [ user.id for user in userList ]
        else:
            followingUsers = []
        c.authuser['followingUsers'] = str(pickle.dumps(followingUsers))
        commit(c.authuser)
    else:
        followingUsers = pickle.loads(str(c.authuser['followingUsers']))
    session["followingUsers"] = followingUsers
    session.save()

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
        log.info("broken following query")
        return False

# Object creation/modification here
def FollowOrUnfollow(user, thing, disabled = '0'):
    # We link the follow object to the user and the thing being followed.  The follow object is set up as a child of both, and points to both.
    # The link to the user is done by the 'owner' property (dot notation), and the link to the thing is done by the 'thingCode' attribute
    # (dict notation).
    try:
        f = getFollow(user, thing)
        thingCode = thing['urlCode']
        if thing.objType == 'workshop':
            sKey = 'bookmarkedWorkshops'
        elif thing.objType == 'initiative':
            sKey = 'bookmarkedInitiatives'
        elif thing.objType == 'user':
            sKey = 'followingUsers'
            thingCode = thing.id
        if f:
            # Ugly hack to reverse the bit when it's stored as a string
            f['disabled'] = str(int(not int(f['disabled'])))
            if f['disabled'] == '1':
                if sKey in session and thingCode in session[sKey]:
                    session[sKey].remove(thingCode)
                    user[sKey] = str(pickle.dumps(session[sKey]))
                    commit(user)
            else:
                if sKey in session and thingCode not in session[sKey]:
                    session[sKey].append(thingCode)
                    user[sKey] = str(pickle.dumps(session[sKey]))
                    commit(user)
        else:
            f = Thing('follow', user.id)
            generic.linkChildToParent(f, thing)
            f['itemAlerts'] = '0'
            f['digest'] = '0'
            f['disabled'] = disabled
            if sKey in session and session[sKey] and thingCode not in session[sKey]:
                session[sKey].append(thingCode)
                user[sKey] = str(pickle.dumps(session[sKey]))
                commit(user)
            elif sKey in session and not session[sKey]:
                session[sKey].append(thingCode)
                user[sKey] = str(pickle.dumps(session[sKey]))
                commit(user)

        
        if thing.objType == 'user':
            fKey = 'follower_counter'
            if f['disabled'] == '0':
                if fKey in thing:
                    fValue = int(thing[fKey])
                    fValue += 1
                    thing[fKey] = str(fValue)
                else:
                    thing[fKey] = '1'
            else:
                if fKey in thing:
                    fValue = int(thing[fKey])
                    fValue -= 1
                    thing[fKey] = str(fValue)
                else:
                    thing[fKey] = '0'
            fKey = 'follow_counter'
        elif thing.objType == 'workshop' or thing.objType == 'initiative':
            fKey = 'bookmark_counter'
        
        if f['disabled'] == '0':
            if fKey in user:
                fValue = int(user[fKey])
                fValue += 1
                user[fKey] = str(fValue)
            else:
                user[fKey] = '1'
        else:
            if fKey in user:
                fValue = int(user[fKey])
                fValue -= 1
                user[fKey] = str(fValue)
            else:
                user[fKey] = '0'
        commit(user)
        commit(f)
        
        session.save()
        return True
    except:
        return False
        