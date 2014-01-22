#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
from dbHelpers import commit, with_characteristic as wc
from pylowiki.lib.utils import urlify, toBase62
import pylowiki.lib.db.generic as generic
import pylowiki.lib.db.discussion as discussionLib

log = logging.getLogger(__name__)

def getMessages(user, deleted = u'0', disabled = u'0', read = u'all', count = False):
    try:
        query = meta.Session.query(Thing).filter_by(objType = 'message')\
                .filter_by(owner = user.id)\
                .filter(Thing.data.any(wc('deleted', deleted)))\
                .filter(Thing.data.any(wc('disabled', disabled)))
        if read != u'all':
            # Grab items that are read (1) or items that are unread (0).  Grab all by default.
            query = query.filter(Thing.data.any(wc('read', read)))
        if count:
            return query.count()
        return query.order_by('-date').all()
    except:
        return False

def getMessagesForThing(user, thing, deleted = u'0', disabled = u'0'):
    try:
        thingKey = '%sCode' % thing.objType
        thingCode = thing['urlCode']
        query = meta.Session.query(Thing).filter_by(objType = 'message')\
                .filter_by(owner = user.id)\
                .filter(Thing.data.any(wc('deleted', deleted)))\
                .filter(Thing.data.any(wc('disabled', disabled)))\
                .filter(Thing.data.any(wc(thingKey, thingCode)))\
                .all()
    except:
        return False

def getMessage(user, code, deleted = u'0', disabled = u'0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'message')\
                .filter_by(owner = user.id)\
                .filter(Thing.data.any(wc('deleted', deleted)))\
                .filter(Thing.data.any(wc('disabled', disabled)))\
                .filter(Thing.data.any(wc('urlCode', code)))\
                .one()
    except:
        return False

def Message(**kwargs):
    """
        Messages have discussions attached to them to allow for tree-based commenting.  Messages are intended to be an object type that
        provides lightweight methods for accessing these discussions.  Messages also have the flexibility to add any additional metadata
        that discussion objects do not have.
        
        Much like email, one message object is created for every party in the message.  Then each recieving party can mark the message
        as deleted without affecting the other parties.
        
        Messages are used for system messages (e.g. If your item gets disabled/deleted, if someone responds to you, if you get invited
        to facilitate a workshop) and non-public person-to-person messages.
        
        -----Inputs-----
        owner       ->  A User Thing.  The person recieving the message.
        title       ->  Exactly what one would expect.  Just a string.
        text        ->  Any optional message content.  Just a string.
        sender      ->  The User Thing doing that originated/created/generated the message.  If not present, then the message was system-generated.
        
        -----Other non-standard properties-----
        read        ->  If the owner of the message has read it.
    """
    
    m = Thing('message', kwargs['owner'].id)
    if 'title' in kwargs:
        title = kwargs['title']
    else:
        title = '(No title)'
    if 'text' in kwargs:
        text = kwargs['text']
    else:
        text = ''
    if 'sender' in kwargs:
        sender = kwargs['sender']['urlCode']
    else:
        sender = u'0'
    
    if 'extraInfo' in kwargs:
        extraInfo = kwargs['extraInfo']
        m['extraInfo'] = extraInfo
        if 'workshop' in kwargs:
            workshop = kwargs['workshop']
            if extraInfo in ['facilitationInvite', 'listenerInvite', 'listenerSuggestion']:
                generic.linkChildToParent(m, workshop)
        if 'item' in kwargs:
            item = kwargs['item']
            if extraInfo in ['facilitationInvite', 'listenerInvite', 'listenerSuggestion']:
                generic.linkChildToParent(m, item)
    
    m['sender']     = sender
    m['text']       = text
    m['title']      = title
    m['deleted']    = u'0'
    m['disabled']   = u'0'
    m['read']       = u'0'
    commit(m)
    m['urlCode'] = toBase62(m)
    commit(m)
    
    if 'workshop' in kwargs:
        d = discussionLib.Discussion(owner = kwargs['owner'], discType = 'message', attachedThing = m,\
                title = title, text = text, workshop = kwargs['workshop'], privs = kwargs['privs'], role = None)
    elif 'item' in kwargs:
        d = discussionLib.Discussion(owner = kwargs['owner'], discType = 'message', attachedThing = m,\
                title = title, text = text, item = kwargs['item'], privs = kwargs['privs'], role = None)
    else:
        d = discussionLib.Discussion(owner = kwargs['owner'], discType = 'message', attachedThing = m,\
            title = title, text = text, privs = kwargs['privs'], role = None)
        
    return m
    