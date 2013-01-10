from pylowiki.model import Thing, meta
from pylowiki.lib.utils import urlify, toBase62
import pylowiki.lib.db.generic as generic
from dbHelpers import commit
from dbHelpers import with_characteristic as wc

import logging
log = logging.getLogger(__name__)

import pickle

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

# Looks like this needs to also update the user's pickled list of rating tuples
def changeRating(ratedThing, rateObj_id, amount):
    rateObj = getRatingByID(rateObj_id)
    ratingType = rateObj['ratingType']
    oldRating = rateObj['rating']
    ratingAmounts = ratedThing['ratingList_%s' % ratingType]
    ratingAmounts = map(float, ratingAmounts.split(','))
    try:
        log.info(ratingAmounts)
        log.info(oldRating)
        ratingAmounts.remove(float(oldRating))
        rateObj['rating'] = amount
    except:
        raise
        return False
    ratingAmounts.append(amount)
    ratedThing['ratingList_%s' % ratingType] = ','.join(map(str, ratingAmounts))
    ratedThing['ratingAvg_%s' % ratingType] = sum(ratingAmounts)/len(ratingAmounts)
    commit(ratedThing)
    commit(rateObj)
    return True

class Rating(object):
    def __init__(self, amount, ratedThing, owner, ratingType):
        """
            amount        ->    The rating, in numerical format
            ratedThing    ->    The Thing that is being rated
            owner         ->    The Thing (user) that is doing the rating
            ratingType    ->    The type of rating being given (e.g. helpfulness/mischevious/overall), in string format
            
            We will create a comma-separated list of ratings in the rated object.  The list is called 'ratingList_type', where 'type' is the ratingType defined above.
            The average rating is called 'ratingAvg_type', with the same convention for 'type' as before.  The list 'ratingIDs_type' contains the 
            Thing IDs of the rating objects.
             
        """
        keyList = 'ratingList_%s' % ratingType
        keyAvg = 'ratingAvg_%s' % ratingType
        keyIDs = 'ratingIDs_%s' % ratingType
        
        r = Thing('rating', owner.id)
        r['rating'] = amount
        r['ratingType'] = ratingType
        r['ratedThing_id'] = ratedThing.id
        
        if keyList not in ratedThing.keys():
            ratedThing[keyList] = amount
            ratedThing[keyAvg] = amount
        else:
            ratedThing[keyList] = ratedThing[keyList] + ',' + str(amount)
            ratings = [int(float(item)) for item in ratedThing[keyList].split(',')]
            ratedThing[keyAvg] = sum(ratings, 0.0)/len(ratings)
            
        commit(r)
        
        # Linkback to the thing being rated
        if keyIDs not in ratedThing.keys():
            ratedThing[keyIDs] = r.id
        else:
            ratedThing[keyIDs] = ratedThing[keyIDs] + ',' + str(r.id)
        
        # Linkback to the owner doing the rating
        key = 'ratedThings_%s_%s' % (ratedThing.objType, ratingType)
        if key not in owner.keys():
            # Dictionary of ratedThing id as key and the rating id as value
            rateDict = {ratedThing.id:r.id}
            owner[key] = pickle.dumps(rateDict)
        else:
            rateDict = pickle.loads(str(owner[key]))
            rateDict[ratedThing.id] = r.id
            owner[key] = pickle.dumps(rateDict)
            
        commit(ratedThing)
        commit(owner)
        
