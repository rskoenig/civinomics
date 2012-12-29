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
    
def getAllActiveDiscussionsForWorkshop(code):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'discussion').filter(Thing.data.any(wc('workshopCode', code))).filter(Thing.data.any(wc('disabled', '0'))).filter(Thing.data.any(wc('deleted', '0'))).all()
    except:
        return False
    
def getDisabledDiscussionsForWorkshop(code, discType = 'general'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'discussion').filter(Thing.data.any(wc('workshopCode', code))).filter(Thing.data.any(wc('discType', discType))).filter(Thing.data.any(wc('disabled', '1'))).all()
    except:
        return False
    
def getDeletedDiscussionsForWorkshop(code, discType = 'general'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'discussion').filter(Thing.data.any(wc('workshopCode', code))).filter(Thing.data.any(wc('discType', discType))).filter(Thing.data.any(wc('deleted', '1'))).all()
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
                    
                    (optional)
                    text                 ->    Some extra description, if provided
        """
        if 'owner' not in kwargs.keys():
            d = Thing('discussion')
        else:
            d = Thing('discussion', kwargs['owner'].id)
        title = kwargs['title']
        discType = kwargs['discType']
        d['discType'] = discType
        d['disabled'] = '0'
        d['deleted'] = '0'
        d['ups'] = '0'
        d['downs'] = '0'
        d['title'] = title
        d['url'] = urlify(title)
        d['numComments'] = '0' # should instead do a count query on number of comments with parent code of this discussion
        
        # Optional arguments
        if 'text' in kwargs:
            d['text'] = kwargs['text']
        if 'attachedThing' in kwargs.keys():
            d = generic.linkChildToParent(d, kwargs['attachedThing'])
        commit(d)
        d['urlCode'] = toBase62(d)
        commit(d)
        
        self.d = d
