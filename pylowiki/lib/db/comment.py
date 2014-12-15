#-*- coding: utf-8 -*-
import logging

from pylons import tmpl_context as c

from pylowiki.lib.utils import toBase62
from pylowiki.model import Thing, Data, meta
from pylowiki.lib.db.flag import checkFlagged
from pylowiki.lib.db.workshop import getWorkshopByCode
import pylowiki.lib.db.idea         as ideaLib
import pylowiki.lib.db.resource     as resourceLib
import pylowiki.lib.db.photo        as photoLib
import pylowiki.lib.db.initiative   as initiativeLib
import pylowiki.lib.db.meeting      as meetingLib
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

def checkUserCommentInDiscussion(user, discussionCode, deleted = '0', disabled = '0'):
    return meta.Session.query(Thing)\
        .filter_by(objType = 'comment')\
        .filter(Thing.data.any(wc('discussionCode', discussionCode)))\
        .filter_by(owner = user.id)\
        .filter(Thing.data.any(wc('deleted', deleted)))\
        .filter(Thing.data.any(wc('disabled', disabled)))\
        .all()
             

def getCommentsInDiscussionByCode(discussionCode, deleted = '0', disabled = '0'):
    try:
       return meta.Session.query(Thing)\
            .filter_by(objType = 'comment')\
            .filter(Thing.data.any(wc('discussionCode', discussionCode)))\
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
        comments = meta.Session.query(Thing)\
            .filter_by(objType = 'comment')\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .all()
        liveComments = []
        for comment in comments:
            if 'ideaCode' in comment.keys():
                idea = generic.getThing(comment['ideaCode'])
                if idea['deleted'] == u'1':
                    continue
            elif 'resourceCode' in comment.keys():
                resource = generic.getThing(comment['resourceCode'])
                if resource['deleted'] == u'1':
                    continue
            else:
                discussion = generic.getThing(comment['discussionCode'])
                if discussion['deleted'] == u'1':
                    continue
            liveComments.append(comment)
        return liveComments
    except:
        return False

def getCommentsInWorkshop(workshop, disabled = '0', deleted = '0'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'comment')\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .filter(Thing.data.any(wc('workshopCode', workshop['urlCode'])))\
            .all()
    except:
        return False

# Setters
def editComment(comment, data, commentRole = 'neutral'):
    r = Revision(c.authuser, comment)
    comment['data'] = data
    if 'initiativeCode' in comment or 'ideaCode' in comment:
        comment['commentRole'] = commentRole
    commit(comment)
    return comment

# Object
def Comment(data, owner, discussion, privs, role = None, parent = 0):
    profileTypes = ['photo', 'initiative', 'organization_general', 'organization_position']
    attachedThing = None
    thisComment = Thing('comment', owner.id)
    
    log.info("Comment added has %s discussion type."%discussion['discType'])
    if 'workshopCode' in discussion:
        w = getWorkshopByCode(discussion['workshopCode'])
        thisComment = generic.linkChildToParent(thisComment, w)
        if discussion['discType'] == 'idea':
            attachedThing = ideaLib.getIdea(discussion['ideaCode'])
        elif discussion['discType'] == 'resource':
            attachedThing = resourceLib.getResourceByCode(discussion['resourceCode'])
    if discussion['discType'] == 'photo':
        attachedThing = photoLib.getPhoto(discussion['photoCode'])
        profileOwner = generic.getThingByID(attachedThing.owner)
    elif discussion['discType'] == 'initiative':
        attachedThing = initiativeLib.getInitiative(discussion['initiativeCode'])
        profileOwner = generic.getThingByID(attachedThing.owner)
    elif discussion['discType'] == 'agendaitem':
        attachedThing = meetingLib.getAgendaItem(discussion['agendaitemCode'])
    elif discussion['discType'] == 'resource' and 'initiativeCode' in discussion:
        initiative = initiativeLib.getInitiative(discussion['initiativeCode'])
        thisComment = generic.linkChildToParent(thisComment, initiative)
        attachedThing = resourceLib.getResourceByCode(discussion['resourceCode'])
    elif discussion['discType'] == 'resource' and 'initiativeCode' not in discussion:
        attachedThing = resourceLib.getResourceByCode(discussion['resourceCode'])
    elif discussion['discType'] == 'organization_general' or discussion['discType'] == 'organization_position':
        attachedThing = discussion
        profileOwner = generic.getThingByID(attachedThing.owner)
    elif discussion['discType'] == 'idea':
        attachedThing = ideaLib.getIdea(discussion['ideaCode'])
        
            
    thisComment = generic.linkChildToParent(thisComment, owner)
            
    thisComment = generic.linkChildToParent(thisComment, discussion)
    if attachedThing is not None:
        updateParentDate(attachedThing)
        if attachedThing.id != discussion.id:
            thisComment = generic.linkChildToParent(thisComment, attachedThing)
        nComments = 0
        if attachedThing.objType != 'discussion':
            if 'numComments' in attachedThing:
                nComments = int(attachedThing['numComments'])
            
            nComments += 1
        
            attachedThing['numComments'] = str(nComments)
            commit(attachedThing)
        
        if discussion['discType'] in profileTypes:
            thisComment['profileCode'] = profileOwner['urlCode']
            thisComment['profile_url'] = profileOwner['url']
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
        
    setDiscussionProperties(thisComment, discussion)
    return thisComment
        
def setDiscussionProperties(comment, discussion):
    if int(comment['isRoot']) == 1: 
        if 'children' not in discussion.keys():
            discussion['children'] = comment.id
        else:
            discussion['children'] = discussion['children'] + ',' + str(comment.id)
    discussion['numComments'] = int(discussion['numComments']) + 1
    commit(discussion)
        
        
def updateParentDate(thing):
    log.info("Parent thing type is %s"%thing.objType)
    log.info(thing.lastUpdated)
    log.info(datetime.now())
    thing.lastUpdated = datetime.now()
    commit(thing)