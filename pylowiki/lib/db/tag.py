#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic

def getWorkshopTags(workshopID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'tag').filter(Thing.data.any(wc('thingID', workshopID))).all()
    except:
        return False

class Tag(object):
    def __init__(self, tagType, tagName, thingID, ownerID):
        t = Thing('tag', ownerID)
        # tagType, one of: system or member (tag from our list or their input)
        t['tagType'] = tagType
        t['tagName'] = tagName
        # the id of the object described by the tag
        t['thingID'] = thingID
        commit(t)


