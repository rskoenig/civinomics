from pylowiki.model import Thing, Data, meta
from sqlalchemy import and_, or_, not_
from dbHelpers import with_characteristic as wc, with_characteristic_like as wcl, greaterThan_characteristic as gtc, with_key_characteristic_like as wkcl, with_key_in_list as wkil, without_characteristic as wo
import pylowiki.lib.db.discussion   as discussionLib
import pylowiki.lib.db.generic      as generic
from pylowiki.lib.utils import urlify
import logging
import datetime
log = logging.getLogger(__name__)

def getMemberPosts(user, limit = None, offset = None, unpublished = '0'):
    if unpublished == '1':
        activityTypes = ['resourceUnpublished', 'commentUnpublished', 'discussionUnpublished', 'ideaUnpublished', 'photoUnpublished', 'initiativeUnpublished', 'meetingUnpublished', 'agendaitemUnpublished', 'ballotUnpublished', 'ballotmeasureUnpublished', 'ballotcandidateUnpublished']
    else:
        activityTypes = activityTypes = ['resource', 'comment', 'discussion', 'idea', 'photo', 'initiative', 'meeting', 'agendaitem', 'ballot', 'ballotmeasure']
    discussionTypes = ['general', 'update', 'organization_general', 'organization_position']
    codes = ['resourceCode', 'ideaCode', 'photoCode', 'discussionCode']
    keys = ['deleted']
    values = ['0']
    finalActivityList = []
    try:
        q = meta.Session.query(Thing).filter(Thing.objType.in_(activityTypes))\
            .filter_by(owner = user.id)\
            .filter(Thing.data.any(wc('deleted', '0')))\
            .order_by('-date').offset(offset)
        if limit:
            initialActivityList = q.limit(limit)
        
        # Messy
        for activity in initialActivityList:
            if activity.objType == 'discussion' and activity['discType'] not in discussionTypes:
                continue
            else:                
                finalActivityList.append(activity)
        return finalActivityList
    except:
        return False
        
def getMemberActivity(user, unpublished = '0'):
    if unpublished == '1':
        activityTypes = ['resourceUnpublished', 'commentUnpublished', 'discussionUnpublished', 'ideaUnpublished', 'photoUnpublished']
    else:
        activityTypes = ['resource', 'comment', 'discussion', 'idea', 'photo']
    codes = ['resourceCode', 'ideaCode', 'photoCode', 'discussionCode']
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
        if activity.objType.replace("Unpublished", "") == 'discussion' and activity['discType'] != 'general':
            continue
            
        # load the itemDict for this item
        itemCode = activity['urlCode']
        itemList.append(itemCode)
        itemDict[itemCode] = {}
        itemDict[itemCode]['objType'] = activity.objType.replace("Unpublished", "")
        itemDict[itemCode]['owner'] = activity.owner
        for key in itemKeys:
            if key in activity:
                itemDict[itemCode][key] = activity[key]
                
        if activity.objType.replace("Unpublished", "") == 'comment':
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
                parentDict[parentCode]['objType'] = parent.objType.replace("Unpublished", "")
                parentDict[parentCode]['owner'] = parent.owner
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

def getActivityForWorkshop(limit, offset, workshopCode, sort = 0, disabled = '0', deleted = '0'):
    objectList = ['idea', 'resource', 'discussion', 'initiative']
    workshop = generic.getThing(workshopCode)
    public_private = workshop['public_private']
    if public_private == 'public':
        svalue = '1'
    else:
        svalue = '2'
        
    q = meta.Session.query(Thing)\
        .filter(Thing.objType.in_(objectList))\
        .filter(Thing.data.any(wc('disabled', u'0')))\
        .filter(Thing.data.any(wc('deleted', u'0')))\
        .filter(Thing.data.any(wc('workshopCode', workshopCode)))\
        .filter(Thing.data.any(or_(and_(Data.key.ilike('%public'), Data.value == u'1'), and_(Data.key == 'workshop_searchable', Data.value == svalue))))\
        .order_by('-date')\
        .offset(offset)

    if limit:
        postList = q.limit(limit)
    else:
        postList = q.all()

    if postList:
        return postList
    else:
        return []

        
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
        activityList = meta.Session.query(Thing)\
            .filter(Thing.objType.in_(objTypes))\
            .filter(Thing.data.any(and_(Data.key == u'workshopCode', Data.value.in_(workshopCodes))))\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .filter(Thing.data.any(wc('workshop_searchable', u'1')))\
            .order_by('-date')\
            .all()
            
        return activityList
    except:
        return False


def getRecentActivity(limit, comments = 0, offset = 0):
        objectList = ['idea', 'resource', 'discussion', 'initiative', 'photo']
        if comments:
            objectList.append('comment')
        q = meta.Session.query(Thing)\
            .filter(Thing.objType.in_(objectList))\
            .filter(Thing.data.any(wc('disabled', u'0')))\
            .filter(Thing.data.any(wc('deleted', u'0')))\
            .filter(Thing.data.any(or_(or_(and_(Data.key.ilike('%public'), Data.value == u'1'), and_(Data.key.ilike('%searchable'), Data.value == u'1')), and_(Data.key == 'format', Data.value == 'png'))))\
            .order_by('-date')\
            .offset(offset)
        if limit:
            postList = q.limit(limit)
        else:
            postList = q.all()
        if postList:
            return postList
        else:
            return []

def getInitiativeActivity(limit, comments = 0, offset = 0, geoScope = False):
        objectList = ['initiative']
        if comments:
            objectList.append('comment')
        q = meta.Session.query(Thing)\
            .filter(Thing.objType.in_(objectList))\
            .filter(Thing.data.any(wc('disabled', u'0')))\
            .filter(Thing.data.any(wc('deleted', u'0')))\
            .filter(Thing.data.any(or_(or_(and_(Data.key.ilike('%public'), Data.value == u'1'), and_(Data.key == 'workshop_searchable', Data.value == u'1')), and_(Data.key == 'format', Data.value == 'png'))))\
            .order_by('-date')\
            .offset(offset)
        if geoScope:
            q.filter(Thing.data.any(wkcl('scope', geoScope)))
        if limit:
            postList = q.limit(limit)
        else:
            postList = q.all()

        if postList:
            return postList
        else:
            return []

def getRecentGeoActivity(limit, scopes, comments = 0, offset = 0, itemType = ''):
    #log.info("In getRecentGeoActivity and itemType is %s" % itemType)
    postList = []
    if itemType is '':
        objectList = ['idea', 'workshop', 'resource', 'discussion', 'initiative', 'photo']
    else:
        objectList = itemType
    if comments:
        objectList.append('comment')
        
    q = meta.Session.query(Thing)\
        .filter(Thing.objType.in_(objectList))\
        .filter(Thing.data.any(wc('disabled', u'0')))\
        .filter(Thing.data.any(wc('deleted', u'0')))\
        .filter(Thing.data.any(or_(wkcl('scope', scopes[0]),  wkcl('scope', scopes[1]), wkcl('scope', scopes[2]))))\
        .filter(Thing.data.any(or_(and_(Data.key.ilike('%public'), Data.value == u'1'), and_(Data.key == 'workshop_searchable', Data.value == u'1'))))\
        .order_by('-date')\
        .offset(offset)
    if limit:
        postList += q.limit(limit)
    else:
        postList += q.all()
    
    return postList

def getUpcomingGeoMeetings(limit, scope, comments = 0, offset = 0):
    now = datetime.datetime.now()
    twodays = datetime.timedelta(days=2)
    mdate = now - twodays
    SQLtoday = mdate.strftime("%Y-%m-%d")
    postList = []
    objectList = ['meeting']

    q = meta.Session.query(Thing)\
        .filter(Thing.objType.in_(objectList))\
        .filter(Thing.data.any(wc('disabled', u'0')))\
        .filter(Thing.data.any(wc('deleted', u'0')))\
        .filter(Thing.data.any(wkcl('scope', scope)))\
        .filter(Thing.data.any(gtc('meetingDate', SQLtoday)))\
        .filter(Thing.data.any(and_(Data.key.ilike('%public'), Data.value == u'on')))\
        .order_by('sort')\
        .offset(offset)
    if limit:
        postList += q.limit(limit)
    else:
        postList += q.all()
            
    return postList



def getActivityForWorkshopList(limit, workshops, comments = 0, offset = 0):
        objectList = ['idea', 'resource', 'discussion', 'initiative']
        if comments:
            objectList.append('comment')
        q = meta.Session.query(Thing)\
            .filter(Thing.objType.in_(objectList))\
            .filter(Thing.data.any(wc('disabled', u'0')))\
            .filter(Thing.data.any(wc('deleted', u'0')))\
            .filter(Thing.data.any(wkil('workshopCode', workshops)))\
            .filter(Thing.data.any(or_(and_(Data.key.ilike('%public'), Data.value == u'1'), and_(Data.key == 'workshop_searchable', Data.value == u'1'))))\
            .order_by('-date')\
            .offset(offset)
        if limit:
            postList = q.limit(limit)
        else:
            postList = q.all()

        if postList:
            return postList
        else:
            return []
        
def getActivityForInitiativeList(limit, initiatives, comments = 0, offset = 0):
        objectList = ['resource', 'discussion']
        if comments:
            objectList.append('comment')
        q = meta.Session.query(Thing)\
            .filter(Thing.objType.in_(objectList))\
            .filter(Thing.data.any(wc('disabled', u'0')))\
            .filter(Thing.data.any(wc('deleted', u'0')))\
            .filter(Thing.data.any(wc('initiative_public', u'1')))\
            .filter(Thing.data.any(wkil('initiativeCode', initiatives)))\
            .order_by('-date')\
            .offset(offset)
        if limit:
            postList = q.limit(limit)
        else:
            postList = q.all()
            
        if postList:
            return postList
        else:
            return []
        
def getActivityForUserList(limit, users, comments = 0, offset = 0):
        objectList = ['idea', 'resource', 'discussion', 'initiative', 'photo']
        if comments:
            objectList.append('comment')
        q = meta.Session.query(Thing)\
            .filter(Thing.owner.in_(users))\
            .filter(Thing.objType.in_(objectList))\
            .filter(Thing.data.any(wc('disabled', u'0')))\
            .filter(Thing.data.any(wc('deleted', u'0')))\
            .filter(Thing.data.any(or_(or_(and_(Data.key.ilike('%public'), Data.value == u'1'), and_(Data.key.ilike('%searchable'), Data.value == u'1')), and_(Data.key == 'format', Data.value == 'png'))))\
            .order_by('-date')\
            .offset(offset)
        if limit:
            postList = q.limit(limit)
        else:
            postList = q.all()

        if postList:
            return postList
        else:
            return []
            
def getActivityForObjectAndUserList(limit, objects, users, comments = 0, offset = 0):
        if not objects and not users:
            return []
        objectList = ['idea', 'resource', 'discussion', 'initiative', 'photo']
        if comments:
            objectList.append('comment')
        q = meta.Session.query(Thing)\
            .filter(Thing.objType.in_(objectList))\
            .filter(Thing.data.any(wc('disabled', u'0')))\
            .filter(Thing.data.any(wc('deleted', u'0')))\
            .filter(Thing.data.any(or_(or_(and_(Data.key.ilike('%public'), Data.value == u'1'), and_(Data.key.ilike('%searchable'), Data.value == u'1')), and_(Data.key == 'format', Data.value == 'png'))))\
            .filter(Thing.data.any(or_(or_(wkil('initiativeCode', objects), wkil('workshopCode', objects), Thing.owner.in_(users)))))\
            .order_by('-date').offset(offset)
        
        if limit:
            postList = q.limit(limit)
        else:
            postList = q.all()
            
        if postList:
            return postList
        else:
            return []