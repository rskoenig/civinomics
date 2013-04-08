#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic as wc
from pylowiki.lib.utils import urlify, toBase62
from time import time
import pylowiki.lib.db.generic as generic
import pylowiki.lib.db.revision as revisionLib

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

def getDiscussions(disabled = '0', deleted = '0', discType = 'general'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'discussion')\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .filter(Thing.data.any(wc('discType', discType)))\
            .all()
    except:
        return False
    
def getDiscussionForThing(parent):
    if parent.objType == 'discussion':
        return parent
    thisKey = '%sCode' % parent.objType
    try:
        return meta.Session.query(Thing).filter_by(objType = 'discussion').filter(Thing.data.any(wc(thisKey, parent['urlCode']))).one()
    except:
        return False

def getDiscussionsForWorkshop(code, discType = 'general', disabled = '0', deleted = '0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'discussion')\
        .filter(Thing.data.any(wc('workshopCode', code)))\
        .filter(Thing.data.any(wc('discType', discType)))\
        .filter(Thing.data.any(wc('disabled', disabled)))\
        .filter(Thing.data.any(wc('deleted', deleted)))\
        .all()
    except:
        return False

def editDiscussion(discussion, title, text, owner):
    try:
        revisionLib.Revision(owner, discussion)
        discussion['title'] = title
        discussion['text'] = text
        discussion['url'] = urlify(title)
        commit(discussion)
        return True
    except:
        log.error('ERROR: Failed to edit discussion')
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
                    workshop             ->    Links the discussion to the workshop.  The discussion type is used to differentiate between a discussion 
                                               linked to, say, an idea, and a discussion linked directly to the workshop.
                    privs                ->    The c.privs object describing what the authuser's role is
                    (optional)
                    text                 ->    Some extra description, if provided
                    role                 ->    The role used to indicate how the discussion was added (admin, facilitator, listener, etc...)  If not provided,
                                               this is automatically set from the privs dict.
        """
        if 'owner' not in kwargs.keys():
            d = Thing('discussion')
        else:
            d = Thing('discussion', kwargs['owner'].id)
        if 'role' not in kwargs.keys():
            role = None
        else:
            role = kwargs['role']
        title = kwargs['title']
        discType = kwargs['discType']
        workshop = kwargs['workshop']
        d['discType'] = discType
        d['disabled'] = '0'
        d['deleted'] = '0'
        d['ups'] = '0'
        d['downs'] = '0'
        d['title'] = title
        d['url'] = urlify(title)
        d['numComments'] = '0' # should instead do a count query on number of comments with parent code of this discussion
        d = generic.linkChildToParent(d, workshop)
        d = generic.addedItemAs(d, kwargs['privs'], role)
        # Optional arguments
        if 'text' in kwargs:
            d['text'] = kwargs['text']
        if 'attachedThing' in kwargs.keys():
            d = generic.linkChildToParent(d, kwargs['attachedThing'])
        commit(d)
        d['urlCode'] = toBase62(d)
        commit(d)
        
        self.d = d
