#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic as wc
from pylowiki.lib.utils import urlify, toBase62
from time import time
import pylowiki.lib.db.generic as generic

log = logging.getLogger(__name__)

def getDiscussionByID(id):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'discussion').filter_by(id = id).one()
    except:
        return False

def getDiscussion(code):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'discussion').filter(Thing.data.any(wc('urlCode', code))).one()
    except:
        return False

def getDiscussions():
    try:
        return meta.Session.query(Thing).filter_by(objType = 'discussion').all()
    except:
        return False
    
def getActiveDiscussionsForWorkshop(code, discType = 'general'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'discussion').filter(Thing.data.any(wc('workshopCode', code))).filter(Thing.data.any(wc('discType', discType))).filter(Thing.data.any(wc('disabled', '0'))).filter(Thing.data.any(wc('deleted', '0'))).all()
    except:
        return False
    
def getAllActiveDiscussionsForWorkshop(code, url):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'discussion').filter(Thing.data.any(wc('workshopCode', code))).filter(Thing.data.any(wc('workshopURL', url))).filter(Thing.data.any(wc('disabled', '0'))).filter(Thing.data.any(wc('deleted', '0'))).all()
    except:
        return False
    
def getDisabledDiscussionsForWorkshop(code, url, discType = 'general'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'discussion').filter(Thing.data.any(wc('workshopCode', code))).filter(Thing.data.any(wc('workshopURL', url))).filter(Thing.data.any(wc('discType', discType))).filter(Thing.data.any(wc('disabled', '1'))).all()
    except:
        return False
    
def getDeletedDiscussionsForWorkshop(code, url, discType = 'general'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'discussion').filter(Thing.data.any(wc('workshopCode', code))).filter(Thing.data.any(wc('workshopURL', url))).filter(Thing.data.any(wc('discType', discType))).filter(Thing.data.any(wc('deleted', '1'))).all()
    except:
        return False
    
class Discussion(object):
    # If the owner is None, the discussion is a system generated discussion, like the comments in the background wiki.
    # If the owner is not None, then the discussion was actively created by some user.
    def __init__(self, **kwargs):
        """
            Discussions can only be attached to a workshop's feedback, background, workshop resources, suggestions and suggestion resources
            kwargs: dict of arguments, keyed as follows:
                    owner                ->    The owner Thing that created the discussion
                    title                ->    The title of the discussion, in string format
                    attachedThing        ->    The Thing to which we are attaching this discussion
                    discType             ->    Used to determine special properties, like a background discussion or a feedback discussion in a workshop
                    workshop             ->    Used for creating the 'workshopCode' and 'workshopURL' linkbacks if the discussion isn't tied directly to a workshop
        """
        if 'owner' not in kwargs.keys():
            d = Thing('discussion')
        else:
            d = Thing('discussion', kwargs['owner'].id)
        title = kwargs['title']
        discType = kwargs['discType']
        d['discType'] = discType # Used in determining the linkbacks
        if 'workshop' in kwargs:
            d = generic.linkChildToParent(d, kwargs['workshop'])
        if 'attachedThing' in kwargs.keys():
            attachedThing = kwargs['attachedThing']
            
            if attachedThing.objType == 'workshop':
                workshop = attachedThing
                d = generic.linkChildToParent(d, workshop)
                if discType == 'general':
                    d['text'] = kwargs['text']
                    d['ups'] = '0'
                    d['downs'] = '0'
                    d['disabled'] = '0'
                    d['deleted'] = '0'
            elif attachedThing.objType == 'sresource':
                d = generic.linkChildToParent(d, kwargs['workshop'])
                sID = attachedThing['parent_id']
                s = getThingByID(sID)
                d = generic.linkChildToParent(d, s)
        else:
            d = generic.linkChildToParent(d, workshop)
            if discType == 'general':
                d['text'] = kwargs['text']
                d['ups'] = '0'
                d['downs'] = '0'
                d['disabled'] = '0'
                d['deleted'] = '0'
        d['title'] = title
        d['url'] = urlify(title)
        d['numComments'] = '0'
        commit(d)
        d['urlCode'] = toBase62(d)
        commit(d)

        if attachedThing.objType != 'workshop':
            attachedThing['discussion_id'] = d.id
            commit(attachedThing)
        
        self.d = d
