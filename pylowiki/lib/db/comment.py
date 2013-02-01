#-*- coding: utf-8 -*-
import logging

from pylons import tmpl_context as c

from pylowiki.lib.utils import toBase62
from pylowiki.model import Thing, Data, meta
from pylowiki.lib.db.flag import checkFlagged
from pylowiki.lib.db.workshop import getWorkshopByCode
import pylowiki.lib.db.idea         as ideaLib
import pylowiki.lib.db.resource     as resourceLib
import sqlalchemy as sa
from time import time
from dbHelpers import commit, with_characteristic as wc
from pylons import config
from datetime import datetime
from revision import Revision
import pylowiki.lib.db.generic as generic

log = logging.getLogger(__name__)

# Getters
def getComment( id ):
    try:
        return meta.Session.query( Thing ).filter_by(objType = 'comment').filter_by( id = id ).one()
    except sa.orm.exc.NoResultFound:
        return False

def getUserComments(user, disabled = 0):
    try:
       return meta.Session.query(Thing).filter_by(objType = 'comment').filter_by(owner = user.id).filter(Thing.data.any(wc('disabled', disabled))).all()
    except:
       return False

def getCommentByCode( code ):
    try:
        return meta.Session.query( Thing ).filter_by(objType = 'comment').filter(Thing.data.any(wc('urlCode', code))).one()
    except sa.orm.exc.NoResultFound:
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

def getCommentsInDiscussion(discussion, deleted = '0', disabled = '0'):
    try:
       return meta.Session.query(Thing)\
            .filter_by(objType = 'comment')\
            .filter(Thing.data.any(wc('discussionCode', discussion['urlCode'])))\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .all()
    except:
       return False  

def getDeletedComments(discussionID):
    try:
       cList = meta.Session.query(Thing).filter_by(objType = 'comment').filter(Thing.data.any(wc('discussion_id', discussionID))).all()
       comDisabledList = []
       for c in cList:
           if c['deleted'] == '1':
               comDisabledList.append(c.id)
       return comDisabledList
    except:
       return False  

# Pure meaning they are not disabled or deleted yet
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
        
# Pure meaning they are not disabled or deleted yet
def getFlaggedCommentsInDiscussion( discussion, deleted = '0', disabled = '0' ):
    try:
        cList =  meta.Session.query(Thing).filter_by(objType = 'comment')\
                .filter(Thing.data.any(wc('discussionCode', discussion['urlCode'])))\
                .filter(Thing.data.any(wc('deleted', deleted)))\
                .filter(Thing.data.any(wc('disabled', disabled)))\
                .all()
        fList = []
        for c in cList:
            if checkFlagged(c) and c not in fList:
                fList.append(c)
        return fList
    except sa.orm.exc.NoResultFound:
        return False

def isDisabled(comment):
    if comment['disabled'] == '1':
        return True
    return False

def getAllComments(disabled = '0', deleted = '0'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'comment')\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .all()
    except:
        return False

# Setters
def editComment(comment, data):
    r = Revision(c.authuser, comment)
    comment['data'] = data
    commit(comment)
    return comment

# Object
class Comment(object):
    # parent is a Thing id
    def __init__(self, data, owner, discussion, privs, role = None, parent = 0):
        w = getWorkshopByCode(discussion['workshopCode'])
        if discussion['discType'] == 'idea':
            attachedThing = ideaLib.getIdea(discussion['ideaCode'])
        elif discussion['discType'] == 'resource':
            attachedThing = resourceLib.getResourceByCode(discussion['resourceCode'])
        else:
            attachedThing = None
        thisComment = Thing('comment', owner.id)
        thisComment = generic.linkChildToParent(thisComment, w)
        thisComment = generic.linkChildToParent(thisComment, discussion)
        if attachedThing is not None:
            thisComment = generic.linkChildToParent(thisComment, attachedThing)
        thisComment['disabled'] = '0'
        thisComment['deleted'] = '0'
        thisComment['pending'] = '0'
        thisComment['parent'] = parent
        thisComment['children'] = '0'
        thisComment['data'] = data
        thisComment['pending'] = '0'
        thisComment['ups'] = '0'
        thisComment['downs'] = '0'
        thisComment['lastModified'] = datetime.now().ctime()
        thisComment = generic.addedItemAs(thisComment, privs, role)
        commit(thisComment)
        thisComment['urlCode'] = toBase62(thisComment)
        commit(thisComment)
        
        if parent == 0:
            thisComment['isRoot'] = '1'
        else:
            thisComment['isRoot'] = '0'
            parentComment = getComment(parent)
            children = [int(item) for item in parentComment['children'].split(',')]
            if children[0] == 0:
                parentComment['children'] = thisComment.id
            else:
                parentComment['children'] = parentComment['children'] + ',' + str(thisComment.id)
            commit(parentComment)
        
        r = Revision(owner, thisComment)
        self.setDiscussionProperties(thisComment, discussion)
        self.c = thisComment
        
    def setDiscussionProperties(self, comment, discussion):
        if int(comment['isRoot']) == 1: 
            if 'children' not in discussion.keys():
                discussion['children'] = comment.id
            else:
                discussion['children'] = discussion['children'] + ',' + str(comment.id)
        discussion['numComments'] = int(discussion['numComments']) + 1
        commit(discussion)
        
