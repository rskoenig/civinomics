#-*- coding: utf-8 -*-
import logging
log = logging.getLogger(__name__)

from pylowiki.model import Thing, Data, meta
from dbHelpers import commit, with_characteristic as wc

import pickle

def Flag(thing, flagger, flagType = "overall"):
    """
        Any Thing object can be flagged.  The flagType parameter is optional,
        and can be used to specify a type of flag (e.g. off-topic, inflamatory,
        factually incorrect, etc...)
    """
    # flag creation
    f = Thing('flag', flagger.id)
    f['flaggedThing_id'] = thing.id
    f['flaggedThing_owner'] = thing.owner
    f['flaggedThing_objType'] = thing.objType
    f['category'] = flagType
    f['deleted'] = '0'
    commit(f)
    
    # thing commits
    if 'numFlagsTotal' in thing.keys():
        thing['numFlagsTotal'] = str(int(thing['numFlagsTotal']) + 1)
        if ('numFlags_%s'%flagType) in thing.keys():
            thing['numFlags_%s'%flagType] = str(int(thing['numFlags_%s'%flagType]) + 1)
        else:
            thing['numFlags_%s'%flagType] = u'1'
        if ('flag_ids_%s'%flagType) in thing.keys():
            thing['flag_ids_%s'%flagType] = thing['flag_ids_%s'%flagType] + ',' + str(f.id)
        else:
            thing['flag_ids_%s'%flagType] = str(f.id)
    else:
        thing['numFlags'] = u'1'
        thing['numFlags_%s'%flagType] = u'1'
        thing['flag_ids_%s'%flagType] = str(f.id)
    commit(thing)
    
    # User commits
    if 'numFlagsTotal' in flagger.keys():
        flagger['numFlagsTotal'] = str( int(flagger['numFlagsTotal']) + 1 )
        flagger['allFlag_ids'] = flagger['allFlag_ids'] + ',' + str(f.id)
        flagger['allFlaggedThing_ids'] = flagger['allFlaggedThing_ids'] + ',' + str(thing.id)
        if ('numFlags_%s'%flagType) in flagger.keys():
            flagger['numFlags_%s'%flagType] = str( int(flagger['numFlags_%s'%flagType]) + 1 )
        else:
            flagger['numFlags_%s'%flagType] = u'1'
        if ('flag_ids_%s'%flagType) in flagger.keys():
            flagger['flag_ids_%s'%flagType] = flagger['flag_ids_%s'%flagType] + ',' + str(f.id)
        else:
            flagger['flag_ids_%s'%flagType] = str(f.id)
    else:
        flagger['numFlagsTotal'] = u'1'
        flagger['numFlags_%s'%flagType] = u'1'
        flagger['flag_ids_%s'%flagType] = str(f.id)
        flagger['allFlag_ids'] = str(f.id)
        flagger['allFlaggedThing_ids'] = str(thing.id)
    commit(flagger)
    
    return f
    
def getFlags(thing):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'flag').filter(Thing.data.any(wc('flaggedThing_id', thing.id))).filter(Thing.data.any(wc('deleted', '0'))).all()
    except:
        return False

def clearFlags(thing):
        fList =  meta.Session.query(Thing).filter_by(objType = 'flag').filter(Thing.data.any(wc('flaggedThing_id', thing.id))).filter(Thing.data.any(wc('deleted', '0'))).all()
        for f in fList:
            f['deleted'] = 1
            commit(f)

        if 'numFlags' in thing.keys() and int(thing['numFlags']) != 0:
            thing['numFlags'] = 0
            commit(thing)

def checkFlagged(thing):
    if len(getFlags(thing)) > 0:
       return True
    else:
       return False

def isFlagged(thing, flagger):
    """
        Check if a Thing object has already been flagged by the flagger.
        Returns True if so, False if not.
    """
    if 'allFlaggedThing_ids' not in flagger.keys():
        return False
    thing_id = int(thing.id)
    l = map(int, flagger['allFlaggedThing_ids'].split(','))
    if thing_id in l:
        return True
    return False
