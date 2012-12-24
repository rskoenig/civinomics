from pylowiki.model import Thing, Data, meta
from dbHelpers import with_characteristic as wc, with_characteristic_like as wcl, greaterThan_characteristic as gtc 
from pylowiki.lib.db.workshop import getWorkshop, getWorkshopByID
from pylowiki.lib.db.discussion import getDiscussionByID
from dbHelpers import commit
from pylowiki.lib.utils import urlify

def getMemberPosts(user, activeOnly = 1):
    returnList = []
    if activeOnly == 1:
        postList = meta.Session.query(Thing).filter(Thing.objType.in_(['suggestion', 'resource', 'comment', 'discussion'])).filter_by(owner = user.id).filter(Thing.data.any(wc('deleted', '0'))).order_by('-date').all()
    else:
        postList = meta.Session.query(Thing).filter(Thing.objType.in_(['suggestion', 'resource', 'comment', 'discussion'])).filter_by(owner = user.id).order_by('-date').all()

    for item in postList:
       if item.objType == 'suggestion' or item.objType == 'resource' or item.objType == 'comment' or (item.objType == 'discussion' and item['discType'] == 'general'):
           if activeOnly == 1 and isActiveWorkshop(item) == True:
               returnList.append(item)
           elif activeOnly == 0:
               returnList.append(item)
                

    return returnList

def isActiveWorkshop(thing):
    w = False
    if thing.objType == 'suggestion':
        w = getWorkshop(thing['workshopCode'], thing['workshopURL'])
    elif thing.objType == 'resource':
        w = getWorkshopByID(thing['workshop_id'])
    elif thing.objType == 'discussion':
        w = getWorkshop(thing['workshopCode'], thing['workshopURL'])
    elif thing.objType == 'comment':
        d = getDiscussionByID(thing['discussion_id'])
        if d:
            w = getWorkshop(d['workshopCode'], d['workshopURL'])
        else:
            w = False

    if w and w['deleted'] == '0' and w['startTime'] != '0000-00-00' and w['public_private'] == 'public':
        return True
    else:
        return False


