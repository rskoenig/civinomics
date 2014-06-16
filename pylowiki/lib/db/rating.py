from pylowiki.model import Thing, meta
from pylowiki.lib.utils import urlify, toBase62
import pylowiki.lib.db.generic as generic
from dbHelpers import commit
from dbHelpers import with_characteristic as wc, with_key as wk
from pylons import session, tmpl_context as c

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
     
def getRatingsForUser():
    userRatings = {}
    itemTypes = {"commentCode" : "1", "ideaCode" : "1", "resourceCode" : "1", "photoCode" : "1", "initiativeCode" : "1"}
    if c.authuser:
        ratings = meta.Session.query(Thing)\
            .filter_by(objType = 'rating')\
            .filter_by(owner = c.authuser.id).all()

        for rating in ratings:
            for k in rating.keys():
                if k in itemTypes:
                    thingCode = rating[k];
                    userRatings[thingCode] = rating['amount']
                    
        return userRatings
        #log.info("c.ratings is %s"%c.ratings)
    else:
        return False

        
def getRatingForWorkshopObjects(user, workshopCode, objType):
    objCode = objType + 'Code'
    #log.info("objCode is %s workshopCode is %s"%(objCode, workshopCode))
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
            
        if user['activated'] == '0':
            ratingObj['provisional'] = '1'
            
        generic.linkChildToParent(ratingObj, thing)
        ratingObj['ratingType'] = ratingType
      
    commit(ratingObj)
    commit(thing)
    if c.personalRatings:
        if 'ratings' in session:
            log.info("user rating")
            myRatings = session["ratings"]
        else:
            log.info("not user rating")
            myRatings = {}
        thingCode = thing['urlCode']
        myRatings[thingCode] = str(ratingObj['amount'])
        session["ratings"] = myRatings
        session.save()
    return ratingObj