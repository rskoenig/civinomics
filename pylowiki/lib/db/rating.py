from pylowiki.model import Thing, meta
from pylowiki.lib.utils import urlify, toBase62
import pylowiki.lib.db.generic as generic
from dbHelpers import commit
from dbHelpers import with_characteristic as wc, with_key as wk
from pylons import session, tmpl_context as c

import logging
import pickle
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

def getBinaryRatingForThing(user, thing):
    try:
        thingCode = '%sCode' % thing.objType
        return meta.Session.query(Thing)\
            .filter_by(objType = 'rating')\
            .filter_by(owner = user.id)\
            .filter(Thing.data.any(wc('ratingType', 'binary')))\
            .filter(Thing.data.any(wc(thingCode, thing['urlCode']))).one()
    except:
        return False

def getCriteriaRatingForThingUser(user, thing, criteria):
    try:
        thingCode = '%sCode' % thing.objType
        q = meta.Session.query(Thing)\
            .filter_by(objType = 'rating')\
            .filter_by(owner = user.id)\
            .filter(Thing.data.any(wc('criteria', criteria)))\
            .filter(Thing.data.any(wc(thingCode, thing['urlCode']))).one()
        return q
    except:
        return False
        

def getCriteriaRatingForThing(workshopCode, thing, criteria):
    thingCode = '%sCode' % thing.objType
    q = meta.Session.query(Thing)\
        .filter_by(objType = 'rating')\
        .filter(Thing.data.any(wc('criteria', criteria)))\
        .filter(Thing.data.any(wc(thingCode, thing['urlCode']))).all()
    return q
     
def getRatingsForUser():
    userRatings = {}
    itemTypes = {"commentCode" : "1", "ideaCode" : "1", "resourceCode" : "1", "photoCode" : "1", "initiativeCode" : "1", "agendaitemCode" : "1"}
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


def makeOrChangeRating(thing, user, amount, ratingType, criteria = None):
    if criteria:
        ratingObj = getCriteriaRatingForThingUser(user, thing, criteria)
    else:
        if 'ups' not in thing.keys():
            thing['ups'] = 0
        if 'downs' not in thing.keys():
            thing['downs'] = 0
        ratingObj = getBinaryRatingForThing(user, thing)

    if ratingObj:
        # Just change the previous vote        
        if ratingType == 'binary':
            prevRating = int(ratingObj['amount'])
            log.info("I'm binary")
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
        if ratingType == 'criteria':
            log.info("I'm criteria")
            if ratingObj['criteria'] == criteria:
                log.info("Changing amount")
                ratingObj['amount'] = amount
            else:
                log.info("Creating new one")
                ratingObj = Thing('rating', user.id)
                if criteria is None:
                    return False
                ratingObj['criteria'] = criteria
                ratingObj['amount'] = amount
                if user['activated'] == '0':
                    ratingObj['provisional'] = '1'
                generic.linkChildToParent(ratingObj, thing)
                ratingObj['ratingType'] = ratingType
    else:
        if ratingType == 'binary':    
            log.info("I don't exist but I'm binary")
            if amount == 0:
                # Don't make a new neutral object
                return False
            # make a new vote
            ratingObj = Thing('rating', user.id)
            ratingObj['amount'] = amount
            if amount == 1:
                log.info("Going up")
                thing['ups'] = int(thing['ups']) + 1
            else:
                log.info("Going down")
                thing['downs'] = int(thing['downs']) + 1
            if user['activated'] == '0':
                ratingObj['provisional'] = '1'

        elif ratingType == 'criteria':
            log.info("I don't exist but I'm criteria")
            ratingObj = Thing('rating', user.id)
            if criteria is None:
                return False
            ratingObj['criteria'] = criteria
            ratingObj['amount'] = amount
            if user['activated'] == '0':
                ratingObj['provisional'] = '1'
            
        generic.linkChildToParent(ratingObj, thing)
        ratingObj['ratingType'] = ratingType
      
    commit(ratingObj)
    commit(thing)
    if 'ratings' in user:
        myRatings = pickle.loads(str(user["ratings"]))
    else:
        myRatings = {}
    thingCode = thing['urlCode']
    myRatings[thingCode] = str(ratingObj['amount'])
    user["ratings"] = str(pickle.dumps(myRatings))
    commit(user)
    #if c.personalRatings:
    if 'user' in session and (c.authuser['email'] == user['email']):
        session["ratings"] = myRatings
        session.save()

    return ratingObj
    