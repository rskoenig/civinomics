#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic
from pylons import config

log = logging.getLogger(__name__)

# Getters
def getComment( id ):
    try:
        return meta.Session.query( Thing ).filter_by( id = id ).one()
    except sa.orm.exc.NoResultFound:
        return False

# Setters
def disableComment( comment ):
    """disable this comment"""
    comment['disabled'] = True
    commit(comment)

def enableComment( comment ):
    """enable the comment"""
    comment['disabled'] = False
    commit(comment)

# Object
class Comment(object):
    def __init__(self, data, ownerID, pageID, discussionID, parent = None):
        c = Thing('comment', ownerID)
        c['disabled'] = False
        c['pending'] = False
        c['parent'] = Parent
        if parent == None:
            c['isRoot'] = True
        else:
            c['isRoot'] = False
        c['data'] = data
        c['pageID'] = pageID
        c['discussionID'] = discussionID
        c['pending'] = FALSE
        c['avgRating'] = 0
        c['lastModified'] = '0000-00-00'
        commit(c)
