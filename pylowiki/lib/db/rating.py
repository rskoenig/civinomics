from pylowiki.model import Thing, meta
from pylowiki.lib.utils import urlify, toBase62
import pylowiki.lib.db.generic as generic
from dbHelpers import commit
from dbHelpers import with_characteristic as wc, with_key as wk

import logging
log = logging.getLogger(__name__)

def getRatingByID(id):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'rating').filter_by(id = id).one()
    except:
        return False

def getRatingForThing(user, thing):
    try:
        thingCode = '%sCode' % thing.objType
        return meta.Session.query(Thing)\
            .filter_by(objType = 'rating')\
            .filter_by(owner = user.id)\
            .filter(Thing.data.any(wc(thingCode, thing['urlCode']))).one()
    except:
        return False
        
def getRatingForWorkshopObjects(user, workshopCode, objType):
    objCode = objType + 'Code'
    log.info("objCode is %s workshopCode is %s"%(objCode, workshopCode))
    return meta.Session.query(Thing)\
            .filter_by(objType = 'rating')\
            .filter_by(owner = user.id)\
            .filter(Thing.data.any(wk(objCode)))\
            .filter(Thing.data.any(wc('workshopCode', workshopCode))).all()


def makeOrChangeRating(thing, user, amount, ratingType):
    if 'ups' not in thing.keys():
        thing['ups'] = 0
    if 'downs' not in thing.keys():
        thing['downs'] = 0
    
    ratingObj = getRatingForThing(user, thing)
    if ratingObj:
        # Just change the previous vote
        prevRating = int(ratingObj['amount'])
        if ratingType == 'binary':
            if amount == 1 and amount == prevRating:
                # user is 'undoing' their upvote
                thing['ups'] = int(thing['ups']) - 1
                ratingObj['amount'] = 0
            elif amount == -1 and amount == prevRating:
                # user is 'undoing' their downvote
                thing['downs'] = int(thing['downs']) - 1
                ratingObj['amount'] = 0
            elif amount == 1 and prevRating == 0:
                # user goes from neutral to upvote
                thing['ups'] = int(thing['ups']) + 1
                ratingObj['amount'] = amount
            elif amount == 1 and prevRating == -1:
                # user changes downvote to an upvote
                thing['ups'] = int(thing['ups']) + 1
                thing['downs'] = int(thing['downs']) - 1
                ratingObj['amount'] = amount
            elif amount == -1 and prevRating == 0:
                # user goes from neutral to downvote
                thing['downs'] = int(thing['downs']) + 1
                ratingObj['amount'] = amount
            elif amount == -1 and prevRating == 1:
                # user changes upvote to downvote
                thing['ups'] = int(thing['ups']) - 1
                thing['downs'] = int(thing['downs']) + 1
                ratingObj['amount'] = amount
    else:
        if amount == 0:
            # Don't make a new neutral object
            return False
        # make a new vote
        ratingObj = Thing('rating', user.id)
        ratingObj['amount'] = amount
        if amount == 1:
            thing['ups'] = int(thing['ups']) + 1
        else:
            thing['downs'] = int(thing['downs']) + 1
        generic.linkChildToParent(ratingObj, thing)
        ratingObj['ratingType'] = ratingType
        
    commit(ratingObj)
    commit(thing)
    return ratingObj