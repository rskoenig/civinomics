#-*- coding: utf-8 -*-
import logging
log = logging.getLogger(__name__)

from sqlalchemy import and_
from pylowiki.model import Thing, Data, meta
from dbHelpers import with_characteristic as wc
import pylowiki.lib.db.dbHelpers    as dbHelpers
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.event        as eventLib

def Flag(thing, flagger, flagType = "overall", workshop = None):
    """
        Any Thing object can be flagged.  The flagType parameter is optional,
        and can be used to specify a type of flag (e.g. off-topic, inflamatory,
        factually incorrect, etc...)
    """
    f = Thing('flag', flagger.id)
    f['deleted'] = '0'
    f['disabled'] = '0'
    f['flagType'] = flagType
    dbHelpers.commit(f)
    
    # Now set up all the references
    thingOwner = userLib.getUserByID(thing.owner)
    generic.linkChildToParent(f, thingOwner)
    generic.linkChildToParent(f, thing)
    if workshop is not None:
        generic.linkChildToParent(f, workshop)
    dbHelpers.commit(f)
    
    return f

def FlagMetaData(thing, user, reason, immune = u'1'):
    # Instead of denormalizing the object getting flagged, we instead
    # create a new object that dictates whether or not the flagged item
    # is immune to flagging.
    flagMetaData = Thing('flagMetaData', user.id)
    flagMetaData['immune'] = immune
    dbHelpers.commit(flagMetaData)
    generic.linkChildToParent(flagMetaData, thing)
    dbHelpers.commit(flagMetaData)
    
    action = 'immunified'
    eventTitle = '%s %s' % (action.title(), thing.objType)
    eventDescriptor = 'User with email %s %s object of type %s with code %s for this reason: %s' %(user['email'], action, thing.objType, thing['urlCode'], reason)
    eventLib.Event(eventTitle, eventDescriptor, thing, user, reason = reason, action = action)

def getFlagMetaData(thing):
    try:
        thingKey = '%sCode' % thing.objType
        thingCode = thing['urlCode']
        return meta.Session.query(Thing)\
            .filter_by(objType = 'flagMetaData')\
            .filter(Thing.data.any(wc(thingKey, thingCode)))\
            .one()
    except:
        return False

def isImmune(thing):
    metaData = getFlagMetaData(thing)
    if not metaData:
        return False
    if metaData['immune'] == u'1':
        return True
    return False

def getFlaggedThingsInWorkshop(workshop):
    try:
        rows = meta.Session.query(Thing)\
            .filter_by(objType = 'flag')\
            .filter(Thing.data.any(wc('workshopCode', workshop['urlCode'])))\
            .all()
        if len(rows) == 0:
            return False
        flaggedThings = []
        flaggedCodes = []
        codeTypes = ['discussionCode', 'ideaCode', 'resourceCode', 'commentCode']
        for row in rows:
            key = [item for item in codeTypes if item in row.keys()][0] # one of the codeTypes
            code = row[key]
            if code not in flaggedCodes:
                flaggedCodes.append(code)
                flaggedThings.append(generic.getThing(code))
        return flaggedThings
    except:
        return False

def getFlaggedThings(objType, workshop = None):
    try:
        thingKey = u'%sCode' % objType
        flaggedThings = []
        if workshop is None:
            rows = meta.Session.query(Thing)\
                .filter_by(objType = 'flag')\
                .filter(Thing.data.any(and_(Data.key == thingKey)))\
                .all()
        else:
            rows =  meta.Session.query(Thing)\
                .filter_by(objType = 'flag')\
                .filter(Thing.data.any(wc('workshopCode', workshop['urlCode'])))\
                .filter(Thing.data.any(and_(Data.key == thingKey)))\
                .all()
        if len(rows) == 0:
            return False
        for row in rows:
            flaggedThings.append(generic.getThing(row[thingKey]))
        return flaggedThings
    except:
        return False

def getFlags(thing, deleted = '0', disabled = '0'):
    try:
        thingKey = '%sCode' % thing.objType
        thingCode = thing['urlCode']
        return meta.Session.query(Thing)\
            .filter_by(objType = 'flag')\
            .filter(Thing.data.any(wc(thingKey, thingCode)))\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .all()
    except:
        return False

def getNumFlags(thing, deleted = '0', disabled = '0'):
    try:
        thingKey = '%sCode' % thing.objType
        thingCode = thing['urlCode']
        return meta.Session.query(Thing)\
            .filter_by(objType = 'flag')\
            .filter(Thing.data.any(wc(thingKey, thingCode)))\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .count()
    except:
        return 0

def immunify(thing):
    # Flips the 'immune' bit
    flagMetaData = getFlagMetaData(thing)
    if not flagMetaData:
        FlagMetaData(thing, immune = '1')
    else:
        flagMetaData['immune'] = unicode(not int(flagMetaData['immune']))
        dbHelpers.commit(flagMetaData)

def checkFlagged(thing):
    return getNumFlags(thing) > 0

def isFlagged(thing, flagger):
    """
        Check if a Thing object has already been flagged by the flagger.
        Returns True if so, False if not.
    """
    try:
        thingKey = '%sCode' % thing.objType
        thingCode = thing['urlCode']
        rows = meta.Session.query(Thing)\
            .filter_by(objType = 'flag')\
            .filter_by(owner = flagger.id)\
            .filter(Thing.data.any(wc(thingKey, thingCode)))\
            .all()
        return len(rows) == 1
    except:
        return None
