from pylowiki.model import Thing, Data, meta
from dbHelpers import with_characteristic as wc, with_characteristic_like as wcl, greaterThan_characteristic as gtc
from pylowiki.lib.db.discussion import getDiscussionByID
from dbHelpers import commit
from pylowiki.lib.utils import urlify

def getMemberPosts(user, disabled = '0', deleted = '0'):
    activityTypes = ['suggestion', 'resource', 'comment', 'discussion', 'idea']
    try:
        return meta.Session.query(Thing).filter(Thing.objType.in_(activityTypes))\
            .filter_by(owner = user.id)\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .order_by('-date').all()
    except:
        return False

def getAllMemberPosts(user):
    activityTypes = ['suggestion', 'resource', 'comment', 'discussion', 'idea']
    try:
        return meta.Session.query(Thing).filter(Thing.objType.in_(activityTypes))\
            .filter_by(owner = user.id)\
            .order_by('-date').all()
    except:
        return False

def isActiveWorkshop(thing):
    w = False
    if thing.objType == 'suggestion' or thing.objType == 'discussion' or thing.objType == 'resource':
        w = meta.Session.query(Thing).filter_by(objType = 'workshop').filter(Thing.data.any(wc('urlCode', thing['workshopCode']))).one()
    elif thing.objType == 'comment':
        d = getDiscussionByID(thing['discussion_id'])
        if d:
            w = meta.Session.query(Thing).filter_by(objType = 'workshop').filter(Thing.data.any(wc('urlCode', d['workshopCode']))).one()
        else:
            w = False

    if w and w['deleted'] == '0' and w['startTime'] != '0000-00-00' and w['public_private'] == 'public':
        return True
    else:
        return False
        
def getDiscussionCommentsSince(discussionID, memberDatetime):
    try:
       return meta.Session.query(Thing).filter(Thing.date > memberDatetime).filter_by(objType = 'comment').filter(Thing.data.any(wc('discussion_id', discussionID))).all()
    except:
       return False  

def getActivityForWorkshop(workshopCode, disabled = '0', deleted = '0'):
    objTypes = ['resource', 'discussion', 'idea', 'comment']
    finalActivityList = []
    try:
        initialActivityList = meta.Session.query(Thing)\
            .filter(Thing.objType.in_(objTypes))\
            .filter(Thing.data.any(wc('workshopCode', workshopCode)))\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .order_by('-date')\
            .all()
        # Messy
        for activity in initialActivityList:
            if activity.objType == 'discussion' and activity['discType'] != 'general':
                continue
            else:
                finalActivityList.append(activity)
        return finalActivityList
    except:
        return False