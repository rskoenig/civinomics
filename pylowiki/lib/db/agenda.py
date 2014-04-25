#-*- coding: utf-8 -*-
import logging

from pylons import session, tmpl_context as c
from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic as wc, with_characteristic_like as wcl
from pylons import config
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.utils           as utils
import pylowiki.lib.db.discussion   as discussionLib

log = logging.getLogger(__name__)

def getAgenda(code):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'agenda')\
            .filter(Thing.data.any(wc('urlCode', code)))\
            .one()
    except:
        return False
        
        
def searchAgendas( keys, values, deleted = u'0', public = '1', count = False):
    try:
        if type(keys) != type([]):
            p_keys = [keys]
            p_values = [values]
        else:
            p_keys = keys
            p_values = values
        map_agendas = map(wcl, p_keys, p_values)
        q = meta.Session.query(Thing)\
                .filter_by(objType = 'agenda')\
                .filter(Thing.data.any(wc('deleted', deleted)))\
                .filter(Thing.data.any(wc('public', public)))\
                .filter(Thing.data.any(reduce(or_, map_agendas)))
        if count:
            return q.count()
        return q.all()
    except Exception as e:
        log.error(e)
        return False
        

# Agenda Object
def Agenda(owner, title, text, scope, group, meetingDate, agendaPostDate, tag):
    a = Thing('agenda', owner.id)
    generic.linkChildToParent(a, owner)
    commit(a)
    a['urlCode'] = utils.toBase62(i)
    a['title'] = title
    a['url'] = utils.urlify(title[:20])
    a['text'] = text
    a['group'] = group
    a['tag'] = tag
    a['scope'] = scope
    a['meetingDate'] = meetingDate
    a['agendaPostDate'] = agendaPostDate
    a['deleted'] = u'0'
    a['disabled'] = u'0'
    a['public'] = u'0'
    a['archived'] = u'0'
    a['views'] = '0'
    commit(a)
    return a

# Object
def Agendaitem(owner, agenda, title, text):
    a = Thing('agendaitem', owner.id)
    generic.linkChildToParent(a, owner)
    generic.linkChildToParent(a, agenda)
    commit(a)
    a['urlCode'] = utils.toBase62(i)
    a['title'] = title
    a['url'] = utils.urlify(title[:20])
    a['text'] = title
    a['deleted'] = u'0'
    a['disabled'] = u'0'
    a['public'] = u'0'
    a['archived'] = u'0'
    a['views'] = '0'
    a['ups'] = '0'
    a['downs'] = '0'
    commit(a)
    d = discussionLib.Discussion(owner = owner, discType = 'agendaitem', attachedThing = a, title = title)
    return a
def isPublic(agenda):
    if agenda['public'] == '1':
        return True
    else:
        return False
