from pylowiki.model import Thing, meta
from pylowiki.lib.utils import urlify, toBase62
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

"""
    amount        ->    The rating, in numerical format
    ratedThing    ->    The Thing that is being rated
    owner         ->    The Thing (user) that is doing the rating
    ratingType    ->    The type of rating being given (e.g. helpfulness/mischevious/overall), in string format
    
    We will create a comma-separated list of ratings in the rated object.  The list is called 'ratingList_type', where 'type' is the ratingType defined above.
    The average rating is called 'ratingAvg_type', with the same convention for 'type' as before.  The list 'ratingIDs_type' contains the 
    Thing IDs of the rating objects.
     
"""
class Rating(object):
    def __init__(self, amount, ratedThing, owner, ratingType):
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
            ratings = [int(item) for item in ratedThing[keyList].split(',')]
            ratedThing[keyAvg] = sum(ratings, 0.0)/len(ratings)
            
        commit(r)
        
        # Linkback to the thing being rated
        if keyIDs not in ratedThing.keys():
            ratedThing[keyIDs] = r.id
        else:
            ratedThing[keyIDs] = ratedThing[keyIDs] + ',' + str(r.id)
        
        # Linkback to the owner doing the rating
        key = 'ratedThings_%s' % ratedThing.objType
        tup = (ratedThing.id, r.id)
        if key not in owner.keys():
            # tuple of ratedThing id and the rating id
            l = []
            l.append(tup)
            owner[key] = pickle.dumps(l)
        else:
            log.info('key = %s' % key)
            l = pickle.loads(str(owner[key]))
            l.append(tup)
            owner[key] = pickle.dumps(l)
            
        commit(ratedThing)
        commit(owner)
        