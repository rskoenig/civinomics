#-*- coding: utf-8 -*-
import logging

from pylons import session, tmpl_context as c
from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic as wc, with_characteristic_like as wcl, with_key_characteristic_like as wkcl
from pylons import config
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.utils           as utils
import pylowiki.lib.db.discussion   as discussionLib

log = logging.getLogger(__name__)

def getMeeting(code):
    try:
        return meta.Session.query(Thing)\
            .filter(Thing.objType.in_(['meeting', 'meetingUnpublished']))\
            .filter(Thing.data.any(wc('urlCode', code)))\
            .one()
    except:
        return False
        
def getAllMeetings():
    try:
        return meta.Session.query(Thing)\
            .filter(Thing.objType.in_(['meeting', 'meetingUnpublished']))\
            .order_by('-date')\
            .all()
    except:
        return False

def getMeetingsForScope(limit, scope, offset = 0):
    postList = []
    objectList = ['meeting']
    q = meta.Session.query(Thing)\
        .filter(Thing.objType.in_(objectList))\
        .filter(Thing.data.any(wkcl('scope', scope)))\
        .order_by('-date')\
        .offset(offset)
    if limit:
        postList += q.limit(limit)
    else:
        postList += q.all()
            
    return postList

        
def getAgendaItem(code):
    try:
        return meta.Session.query(Thing)\
            .filter(Thing.objType.in_(['agendaitem', 'agendaitemUnpublished']))\
            .filter(Thing.data.any(wc('urlCode', code)))\
            .one()
    except:
        return False
        
def getMeetingsForUser(code):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'meeting')\
            .filter(Thing.data.any(wc('userCode', code)))\
            .all()
    except:
        return False
        
def getAgendaItems(code, count = 0, deleted = u'0'):
    try:
        q = meta.Session.query(Thing)\
            .filter_by(objType = 'agendaitem')\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .filter(Thing.data.any(wc('meetingCode', code)))\
            .order_by('sort')
        if count:
            return q.count()
        else:
            return q.all()
    except:
        return False
        
def searchMeetings( keys, values, deleted = u'0', public = '1', count = False):
    try:
        if type(keys) != type([]):
            p_keys = [keys]
            p_values = [values]
        else:
            p_keys = keys
            p_values = values
        map_meetingss = map(wcl, p_keys, p_values)
        q = meta.Session.query(Thing)\
                .filter_by(objType = 'meeting')\
                .filter(Thing.data.any(wc('deleted', deleted)))\
                .filter(Thing.data.any(wc('public', public)))\
                .filter(Thing.data.any(reduce(or_, map_meetingss)))
        if count:
            return q.count()
        return q.all()
    except Exception as e:
        log.error(e)
        return False
        

# Meeting Object
def Meeting(owner, title, text, scope, group, location, meetingDate, meetingTime, tag, public, agendaPostDate = '0000-00-00'):
    m = Thing('meeting', owner.id)
    generic.linkChildToParent(m, owner)
    commit(m)
    m['urlCode'] = utils.toBase62(m)
    m['title'] = title
    m['url'] = utils.urlify(title[:20])
    m['text'] = text
    m['group'] = group
    m['location'] = location
    m['tag'] = tag
    m['scope'] = scope
    m['meetingDate'] = meetingDate
    m['meetingTime'] = meetingTime
    m.sort = meetingDate
    m['agendaPostDate'] = agendaPostDate
    m['deleted'] = u'0'
    m['disabled'] = u'0'
    m['public'] = public
    m['archived'] = u'0'
    m['views'] = '0'
    commit(m)
    return m

# Object
def Agendaitem(owner, meeting, title, number, text, canVote, canComment):
    a = Thing('agendaitem', owner.id)
    generic.linkChildToParent(a, owner)
    generic.linkChildToParent(a, meeting)
    commit(a)
    a['urlCode'] = utils.toBase62(a)
    a['title'] = title
    a['url'] = utils.urlify(title[:20])
    a['text'] = text
    a['canVote'] = canVote
    a['canComment'] = canComment
    a['numComments'] = '0'
    a['deleted'] = u'0'
    a['disabled'] = u'0'
    a['public'] = u'0'
    a['archived'] = u'0'
    a['views'] = '0'
    a['ups'] = '0'
    a['downs'] = '0'
    a.sort = number
    commit(a)
    d = discussionLib.Discussion(owner = owner, discType = 'agendaitem', attachedThing = a, title = title)
    a['discussion_child'] = d.d['urlCode']
    commit(a)
    return a
def isPublic(agenda):
    if agenda['public'] == '1':
        return True
    else:
        return False
