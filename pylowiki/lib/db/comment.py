#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic
from pylons import config
from datetime import datetime
from revision import Revision
log = logging.getLogger(__name__)

# Getters
def getComment( id ):
    try:
        return meta.Session.query( Thing ).filter_by(objType = 'comment').filter_by( id = id ).one()
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
    # parent is a Thing id
    def __init__(self, data, owner, discussion, parent = None):
        c = Thing('comment', owner.id)
        c['disabled'] = False
        c['pending'] = False
        c['parent'] = parent
        if parent == None:
            c['isRoot'] = True
        else:
            c['isRoot'] = False
        c['data'] = data
        c['discussion_id'] = discussion.id
        c['pending'] = False
        c['ups'] = 0
        c['downs'] = 0
        c['lastModified'] = datetime.now().ctime()
        commit(c)
        
        r = Revision(owner, data, c)
        self.setDiscussionProperties(c, discussion)
        self.c = c
        
    def setDiscussionProperties(self, comment, discussion):
        if int(comment['isRoot']) == 1: 
            if 'children' not in discussion.keys():
                discussion['children'] = comment.id
            else:
                discussion['children'] = discussion['children'] + ',' + comment.id
        discussion['numComments'] = int(discussion['numComments']) + 1
        commit(discussion)
        