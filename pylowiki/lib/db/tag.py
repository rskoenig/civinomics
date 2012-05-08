#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
from pylowiki.lib.db.workshop import Workshop, isWorkshopDeleted
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic as wc, with_characteristic_like as wcl

log = logging.getLogger(__name__)

def getWorkshopTags(workshopID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'tag').filter(Thing.data.any(wc('thingID', workshopID))).all()
    except:
        return False

def searchTags(searchString):
    log.info('searchString %s' % searchString)
    try:
        return meta.Session.query(Thing).filter_by(objType = 'tag').filter(Thing.data.any(wcl('tagName', searchString))).all()
    except:
        return False

def getPublicTagList():
    pTagList = []
    pTagList.append('Environment')
    pTagList.append('Government')
    pTagList.append('Municipal Services')
    pTagList.append('Economy')
    pTagList.append('Infrastructure')
    pTagList.append('Civil Rights')
    pTagList.append('Civic Response')
    pTagList.append('Business')
    return pTagList

def getPublicTagCount():
    tagDict = dict()
    tSearch =  meta.Session.query(Thing).filter_by(objType = 'tag').filter(Thing.data.any(wc('tagType', 'system'))).all()
    tagDict = dict()
    for tL in tSearch:
       wID = tL['thingID']
       if not isWorkshopDeleted(wID):
          t = tL['tagName']
          t = t.lstrip()
          t = t.rstrip()
          if t in tagDict:
              tagDict[t] += 1
          else:
              tagDict[t] = 1

    return tagDict

def getMemberTagList():
    tSearch =  meta.Session.query(Thing).filter_by(objType = 'tag').filter(Thing.data.any(wc('tagType', 'member'))).all()

    tagList = ()
    for tL in tSearch:
       if tL['tagName'] not in tagList:
          tagList.append(tL['tagName'])

    return tagList

def getMemberTagCount():
    tSearch =  meta.Session.query(Thing).filter_by(objType = 'tag').filter(Thing.data.any(wc('tagType', 'member'))).all()
    tagDict = dict()
    for tL in tSearch:
       wID = tL['thingID']
       if not isWorkshopDeleted(wID):
          t = tL['tagName']
          t = t.lstrip()
          t = t.rstrip()
          if t in tagDict:
              tagDict[t] += 1
          else:
              tagDict[t] = 1

    return tagDict

def setWorkshopTagEnable(workshop, disabled):
    tSearch =  meta.Session.query(Thing).filter_by(objType = 'tag').filter(Thing.data.any(wc('thingID', workshop.id))).all()
    for tL in tSearch:
       tL['disabled'] = disabled
       commit(tL)

class Tag(object):
    def __init__(self, tagType, tagName, thingID, ownerID):
        t = Thing('tag', ownerID)
        # tagType, one of: system or member (tag from our list or their input)
        t['tagType'] = tagType
        tagName = tagName.lstrip()
        tagName = tagName.rstrip()
        t['tagName'] = tagName
        t['disabled'] = False
        # the id of the object described by the tag
        t['thingID'] = thingID
        commit(t)


