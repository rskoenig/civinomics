#-*- coding: utf-8 -*-
import logging

from pylons import tmpl_context as c

from pylowiki.lib.utils import toBase62
from pylowiki.model import Thing, Data, meta
from pylowiki.lib.db.flag import checkFlagged
import sqlalchemy as sa
from time import time
from dbHelpers import commit, with_characteristic as wc
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

def getUserComments(user, disabled = False):
    try:
       return meta.Session.query(Thing).filter_by(objType = 'comment').filter_by(owner = user.id).filter(Thing.data.any(wc('disabled', disabled))).all()
    except:
       return False

def getFlaggedDiscussionComments( id ):
    try:
        cList =  meta.Session.query(Thing).filter_by(objType = 'comment').filter(Thing.data.any(wc('discussion_id', id))).all()
        fList = []
        for c in cList:
            if checkFlagged(c) and c.id not in fList:
               fList.append(c.id)        
        return fList
    except sa.orm.exc.NoResultFound:
        return False

def getDisabledComments(discussionID):
    try:
       cList = meta.Session.query(Thing).filter_by(objType = 'comment').filter(Thing.data.any(wc('discussion_id', discussionID))).all()
       comDisabledList = []
       for c in cList:
           if c['disabled'] == '1':
               comDisabledList.append(c.id)
       return comDisabledList
    except:
       return False  

def getDeletedComments(discussionID):
    try:
       cList = meta.Session.query(Thing).filter_by(objType = 'comment').filter(Thing.data.any(wc('discussion_id', discussionID))).all()
       comDisabledList = []
       for c in cList:
           log.info('%d' % int(c['disabled']))
           if c['deleted'] == '1':
               comDisabledList.append(c.id)
       return comDisabledList
    except:
       return False  

"Pure meaning they are not disabled or deleted yet"
def getPureFlaggedDiscussionComments( id ):
    try:
        cList =  meta.Session.query(Thing).filter_by(objType = 'comment').filter(Thing.data.any(wc('discussion_id', id))).all()
        fList = []
        for c in cList:
            if checkFlagged(c) and c.id not in fList:
               if c['disabled'] == '0' and c['deleted'] == '0':
                   fList.append(c.id)
        return fList
    except sa.orm.exc.NoResultFound:
        return False

# Setters
def disableComment( comment ):
    """disable this comment"""
    comment['disabled'] = True
    commit(comment)

def deleteComment( comment ):
    """disable this comment"""
    comment['delete'] = True
    commit(comment)

def enableComment( comment ):
    """enable the comment"""
    comment['disabled'] = False
    commit(comment)

def editComment(commentID, discussionID, data):
    comment = getComment(commentID)
    comment['data'] = data
    r = Revision(c.authuser, data, comment)
    
    commit(comment)
    return comment

# Object
class Comment(object):
    # parent is a Thing id
    def __init__(self, data, owner, discussion, parent = 0):
        c = Thing('comment', owner.id)
        c['disabled'] = False
        c['deleted'] = False
        c['pending'] = False
        c['parent'] = parent
        c['children'] = 0
        c['data'] = data
        if len(data) > 10:
           cData = data[:10]
           c['urlCode'] = toBase62('%s_%s_%s'%(cData, owner['name'], int(time())))
        else:
           c['urlCode'] = toBase62('%s_%s_%s'%(data, owner['name'], int(time())))
        c['discussion_id'] = discussion.id
        c['pending'] = False
        c['ups'] = 0
        c['downs'] = 0
        c['lastModified'] = datetime.now().ctime()
        commit(c)
        
        if parent == 0:
            c['isRoot'] = True
        else:
            c['isRoot'] = False
            parentComment = getComment(parent)
            children = [int(item) for item in parentComment['children'].split(',')]
            if children[0] == 0:
                parentComment['children'] = c.id
            else:
                parentComment['children'] = parentComment['children'] + ',' + str(c.id)
            commit(parentComment)
        
        r = Revision(owner, data, c)
        self.setDiscussionProperties(c, discussion)
        self.c = c
        
    def setDiscussionProperties(self, comment, discussion):
        if int(comment['isRoot']) == 1: 
            if 'children' not in discussion.keys():
                discussion['children'] = comment.id
            else:
                discussion['children'] = discussion['children'] + ',' + str(comment.id)
        discussion['numComments'] = int(discussion['numComments']) + 1
        commit(discussion)
        
