#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
from pylons import session
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic as wc, with_characteristic_like as wcl, without_characteristic as woc, with_key_in_list as wkl
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

def getDiscussion(code, deleted = u'0'):
    try:
        return meta.Session.query(Thing)\
                .filter_by(objType = 'discussion')\
                .filter(Thing.data.any(wc('urlCode', code)))\
                .filter(Thing.data.any(wc('deleted', deleted)))\
                .one()
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
    if parent.objType.replace("Unpublished", "") == 'discussion':
        return parent
    thisKey = '%sCode' % parent.objType.replace("Unpublished", "")
    try:
        return meta.Session.query(Thing)\
        .filter(Thing.objType.in_(['discussion', 'discussionUnpublished']))\
        .filter(Thing.data.any(wc(thisKey, parent['urlCode'])))\
        .filter(Thing.data.any(wc('discType', parent.objType)))\
        .one()
    except:
        return False
        
def getDiscussionsForOrganization(parent, disabled = '0', deleted = '0'):
    thisKey = '%sCode' % parent.objType.replace("Unpublished", "")
    try:
        return meta.Session.query(Thing).filter_by(objType = 'discussion')\
        .filter(Thing.data.any(wc(thisKey, parent['urlCode'])))\
        .filter(Thing.data.any(wc('disabled', disabled)))\
        .filter(Thing.data.any(wc('discType', 'organization_general')))\
        .filter(Thing.data.any(wc('deleted', deleted)))\
        .all()
    except:
        return False
        
def getPositionsForOrganization(parent, disabled = '0', deleted = '0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'discussion')\
        .filter_by(owner = parent.id)\
        .filter(Thing.data.any(wc('disabled', disabled)))\
        .filter(Thing.data.any(wc('discType', 'organization_position')))\
        .filter(Thing.data.any(wc('deleted', deleted)))\
        .all()
    except:
        return False
        
def getPositionsForOrganizationCache(parent, disabled = '0', deleted = '0'):
    try:
        orgPositions = {}
        positions = meta.Session.query(Thing).filter_by(objType = 'discussion')\
        .filter_by(owner = parent.id)\
        .filter(Thing.data.any(wc('disabled', disabled)))\
        .filter(Thing.data.any(wc('discType', 'organization_position')))\
        .filter(Thing.data.any(wc('deleted', deleted)))\
        .all()
        for p in positions:
            if 'ideaCode' in p:
                key = 'ideaCode'
            else:
                key = 'initiativeCode'
            urlCode = p[key]
            orgPositions[urlCode] = p['position']
        return orgPositions
    except:
        return False
        
def getPositionsForItem(parent, disabled = '0', deleted = '0'):
    thisKey = '%sCode' % parent.objType.replace("Unpublished", "")
    try:
        return meta.Session.query(Thing).filter_by(objType = 'discussion')\
        .filter(Thing.data.any(wc(thisKey, parent['urlCode'])))\
        .filter(Thing.data.any(wc('disabled', disabled)))\
        .filter(Thing.data.any(wc('discType', 'organization_position')))\
        .filter(Thing.data.any(wc('deleted', deleted)))\
        .all()
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
        
def getUpdatesForInitiative(code, disabled = '0', deleted = '0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'discussion')\
        .filter(Thing.data.any(wc('initiativeCode', code)))\
        .filter(Thing.data.any(wc('discType', 'update')))\
        .filter(Thing.data.any(wc('disabled', disabled)))\
        .filter(Thing.data.any(wc('deleted', deleted)))\
        .order_by('-date')\
        .all()
    except:
        return False

def editDiscussion(discussion, title, text, owner, position = False):
    try:
        revisionLib.Revision(owner, discussion)
        discussion['title'] = title
        discussion['text'] = text
        discussion['url'] = urlify(title)
        if position:
            discussion['position'] = position
        commit(discussion)
        return True
    except:
        log.error('ERROR: Failed to edit discussion')
        return False

def searchDiscussions(keys, values, deleted = u'0', disabled = u'0', count = False, rootDiscussions = True, hasworkshop = True):
    discussionTypes = ['general']
    try:
        if type(keys) != type([]):
            keys = [keys]
            values = [values]
        m = map(wcl, keys, values)
        q = meta.Session.query(Thing)\
                .filter_by(objType = 'discussion')\
                .filter(Thing.data.any(wc('deleted', deleted)))\
                .filter(Thing.data.any(wc('disabled', disabled)))\
                .filter(Thing.data.any(reduce(sa.or_, m)))
        if rootDiscussions:
            q = q.filter(Thing.data.any(wkl('discType', discussionTypes)))
        if hasworkshop:
            q = q.filter(Thing.data.any(wc('workshop_searchable', '1')))
        if count:
            return q.count()
        return q.all()
    except Exception as e:
        print e
        return False

class Discussion(object):
    # If the owner is None, the discussion is a system generated discussion, like the comments in the background wiki.
    # If the owner is not None, then the discussion was actively created by some user.
    def __init__(self, **kwargs):
        """
            Discussions can be attached to anything, basically
            kwargs: dict of arguments, keyed as follows:
                    owner                ->    The owner Thing that created the discussion
                    title                ->    The title of the discussion, in string format
                    attachedThing        ->    The Thing to which we are attaching this discussion
                    discType             ->    Used to determine special properties, like a background discussion or a feedback discussion in a workshop
                    (optional)
                    workshop             ->    Links the discussion to the workshop.  The discussion type is used to differentiate between a discussion 
                                               linked to, say, an idea, and a discussion linked directly to the workshop.
                    privs                ->    The c.privs object describing what the authuser's role is
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
        d['discType'] = discType
        d['disabled'] = '0'
        d['deleted'] = '0'
        d['ups'] = '0'
        d['downs'] = '0'
        d['views'] = '0'
        d['title'] = title
        d['url'] = urlify(title)
        if 'geoScope' in kwargs:
            d['scope'] = kwargs['geoScope']
            d['public'] = '1'
        if 'tags' in kwargs:
            d['tags'] = kwargs['tags']
        d['numComments'] = '0' # should instead do a count query on number of comments with parent code of this discussion
        # Optional arguments
        if 'workshop' in kwargs and kwargs['workshop'] != None:
            workshop = kwargs['workshop']
            d = generic.linkChildToParent(d, workshop)
            d = generic.addedItemAs(d, kwargs['privs'], role)
        if 'owner' in kwargs.keys():
            d = generic.linkChildToParent(d, kwargs['owner'])
        if 'text' in kwargs:
            d['text'] = kwargs['text']
        if 'attachedThing' in kwargs.keys():
            d = generic.linkChildToParent(d, kwargs['attachedThing'])
        
        if 'workshop_searchable' in d:   
            if discType != 'update' and discType != 'general':
                d['workshop_searchable'] = '0'
                
        commit(d)
        
        d['urlCode'] = toBase62(d)
        commit(d)
                
        if d['discType'] == 'organization_general' or d['discType'] == 'organization_position':
            d['organization_searchable'] = '1'
            if 'position' in kwargs.keys():
                d['position'] = kwargs['position']
                if 'positions' in session:
                    sPositions = session['positions']
                else:
                    sPositions = {}
                urlCode = d['urlCode']
                sPositions[urlCode] = d['position']
                session['positions'] = sPositions
                session.save()
                
            commit(d)

        self.d = d
