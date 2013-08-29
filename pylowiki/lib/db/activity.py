from pylowiki.model import Thing, Data, meta
from sqlalchemy import and_
from dbHelpers import with_characteristic as wc, with_characteristic_like as wcl, greaterThan_characteristic as gtc
import pylowiki.lib.db.discussion   as discussionLib
import pylowiki.lib.db.generic      as generic
from pylowiki.lib.utils import urlify
import logging
log = logging.getLogger(__name__)

def getMemberPosts(user, disabled = '0', deleted = '0'):
    activityTypes = ['resource', 'comment', 'discussion', 'idea']
    codes = ['resourceCode', 'ideaCode', 'discussionCode']
    keys = ['deleted', 'disabled']
    values = [deleted, disabled]
    finalActivityList = []
    try:
        initialActivityList = meta.Session.query(Thing).filter(Thing.objType.in_(activityTypes))\
            .filter_by(owner = user.id)\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .order_by('-date').all()
        # Messy
        for activity in initialActivityList:
            if activity.objType == 'discussion' and activity['discType'] != 'general':
                continue
            elif activity.objType == 'comment':
                parentCode = [i for i in codes if i in activity.keys()]
                thing = generic.getThing(activity[parentCode[0]], keys, values)
                if thing:
                    finalActivityList.append(activity)
            else:                
                finalActivityList.append(activity)
        return finalActivityList
    except:
        return False
        
def getMemberActivity(user):
    activityTypes = ['resource', 'comment', 'discussion', 'idea']
    codes = ['resourceCode', 'ideaCode', 'discussionCode']
    workshopKeys = ['deleted', 'disabled', 'public_private', 'urlCode', 'url',  'title', 'published']
    itemKeys = ['deleted', 'disabled', 'urlCode', 'workshopCode']
    
    # we want to only lookup each item once from the database, so we save it in these dicts.
    activityDict = {}
    itemList = []
    itemDict = {}
    workshopDict = {}
    parentDict = {}
    
    initialActivityList = meta.Session.query(Thing).filter(Thing.objType.in_(activityTypes))\
        .filter_by(owner = user.id)\
        .order_by('-date').all()
    # Messy
    for activity in initialActivityList:
        if activity.objType == 'discussion' and activity['discType'] != 'general':
            continue
        if activity.objType == 'comment' and 'photoCode' in activity:
            continue
            
        # load the itemDict for this item
        itemCode = activity['urlCode']
        itemList.append(itemCode)
        itemDict[itemCode] = {}
        itemDict[itemCode]['objType'] = activity.objType
        for key in itemKeys:
            if key in activity:
                itemDict[itemCode][key] = activity[key]
                
        if activity.objType == 'comment':
            key = 'data'
            # comprehensions return a list
            parentCodeList = [i for i in codes if i in activity.keys()]
            parentCodeField = parentCodeList[0]
            parentCode = activity[parentCodeField]
            itemDict[itemCode]['parentCode'] = parentCode
            # see if this item is already in the parentDict, if not, fetch it and add it
            if parentCode not in parentDict.keys():
                parent = generic.getThing(activity[parentCodeField])
                parentDict[parentCode] = {}
                parentDict[parentCode]['objType'] = parent.objType
                for pkey in itemKeys:
                    if pkey in parent:
                        parentDict[parentCode][pkey] = parent[pkey]
                if parent.objType == 'comment':
                    pkey = 'data'
                else:
                    parentDict[parentCode]['url'] = parent['url']
                    pkey = 'title'
                if pkey in parent:    
                    parentDict[parentCode][pkey] = parent[pkey]
                
        else:
            itemDict[itemCode]['url'] = activity['url']
            key = 'title'
                
        itemDict[itemCode][key] = activity[key]
            
        # see if we need to lookup the workshop and add it to the workshopDict
        if 'workshopCode' in activity and activity['workshopCode'] not in workshopDict:
            workshopCode = activity['workshopCode']
            workshop = generic.getThing(workshopCode)
            workshopDict[workshopCode] = {}
            for key in workshopKeys:
                workshopDict[workshopCode][key] = workshop[key]
    activityDict['itemList'] = itemList
    activityDict['items'] = itemDict
    activityDict['workshops'] = workshopDict
    activityDict['parents'] = parentDict
    return activityDict

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
        d = discussionLib.getDiscussionByID(thing['discussion_id'])
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
    """
        Activity inside a single workshop
        Should be rewritten to return a count if that's all we want, and to do the discussion filtering on the db level
    """
    objTypes = ['resource', 'discussion', 'idea', 'comment']
    codes = ['resourceCode', 'ideaCode', 'discussionCode']
    keys = ['deleted', 'disabled']
    values = [deleted, disabled]
    finalActivityList = []
    try:
        initialActivityList = meta.Session.query(Thing)\
            .filter(Thing.objType.in_(objTypes))\
            .filter(Thing.data.any(wc('workshopCode', workshopCode)))\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .order_by('-date')\
            .all()
        # Messy
        for activity in initialActivityList:
            if activity.objType == 'discussion' and activity['discType'] != 'general':
                continue
            elif activity.objType == 'comment':
                parentCode = [i for i in codes if i in activity.keys()]
                thing = generic.getThing(activity[parentCode[0]], keys, values)
                if thing:
                    finalActivityList.append(activity)
            else:                
                finalActivityList.append(activity)
        return finalActivityList
    except:
        return False
        
def getActivityCountForWorkshop(workshopCode, disabled = '0', deleted = '0'):
    """
        Activity inside a single workshop
        Should be rewritten to return a count if that's all we want, and to do the discussion filtering on the db level
    """
    objTypes = ['resource', 'discussion', 'idea']
    finalActivityList = []
    initialActivityList = meta.Session.query(Thing)\
            .filter(Thing.objType.in_(objTypes))\
            .filter(Thing.data.any(wc('workshopCode', workshopCode)))\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .order_by('-date')\
            .all()
    # Messy
    count = 0
    for activity in initialActivityList:
        if activity.objType == 'discussion':
            if activity['discType'] == 'general':
                count += 1
            count += int(activity['numComments'])
        else:
            count += 1
    return count

        
def getActivityForWorkshops(workshopCodes, disabled = '0', deleted = '0'):
    """
        Activity inside multiple workshops, given a list of workshop codes
        Should be rewritten to return a count if that's all we want, and to do the discussion filtering on the db level
    """
    objTypes = ['resource', 'discussion', 'idea']
    finalActivityList = []
    try:
        initialActivityList = meta.Session.query(Thing)\
            .filter(Thing.objType.in_(objTypes))\
            .filter(Thing.data.any(and_(Data.key == u'workshopCode', Data.value.in_(workshopCodes))))\
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

def getRecentActivity(number, publicPrivate = 'public'):
        limit = number * 15
        returnList = []
        keys = ['deleted', 'disabled', 'published', 'public_private']
        values = [u'0', u'0', u'1', u'public']
        postList = meta.Session.query(Thing)\
            .filter(Thing.objType.in_(['idea', 'resource', 'discussion']))\
            .filter(Thing.data.any(and_(Data.key == u'workshopCode')))\
            .filter(Thing.data.any(wc('disabled', u'0')))\
            .filter(Thing.data.any(wc('deleted', u'0')))\
            .order_by('-date')\
            .limit(limit)
        for item in postList:
            w = generic.getThing(item['workshopCode'], keys = keys, values = values)
            if item.objType == 'discussion' and item['discType'] != 'general':
                continue
            
            if w:
                returnList.append(item)
                if len(returnList) == number:
                    return returnList

        return returnList