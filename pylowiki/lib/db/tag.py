#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic as wc

def getWorkshopTags(workshopID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'tag').filter(Thing.data.any(wc('thingID', workshopID))).all()
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
    tL = getPublicTagList()
    for pT in tL:
       tagDict[pT] = meta.Session.query(Thing).filter_by(objType = 'tag').filter(Thing.data.any(wc('tagType', 'system'))).filter(Thing.data.any(wc('tagName', pT))).count()

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
       t = tL['tagName']
       t = t.lstrip()
       t = t.rstrip()
       if t in tagDict:
           tagDict[t] += 1
       else:
           tagDict[t] = 1

    return tagDict

class Tag(object):
    def __init__(self, tagType, tagName, thingID, ownerID):
        t = Thing('tag', ownerID)
        # tagType, one of: system or member (tag from our list or their input)
        t['tagType'] = tagType
        tagName = tagName.lstrip()
        tagName = tagName.rstrip()
        t['tagName'] = tagName
        # the id of the object described by the tag
        t['thingID'] = thingID
        commit(t)


