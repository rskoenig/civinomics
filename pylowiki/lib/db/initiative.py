#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic as wc, with_characteristic_like as wcl
from pylons import config
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.db.discussion   as discussionLib
import pylowiki.lib.utils           as utils 

log = logging.getLogger(__name__)

# getter
def getInitiative(initiativeCode):
    try:
        return meta.Session.query(Thing).filter(Thing.objType.in_(['initiative', 'initiativeUnpublished'])).filter(Thing.data.any(wc('urlCode', initiativeCode))).one()
    except:
        return False
        
def isPublished(initiative):
    if initiative['published'] == '1':
        return True
    else:
        return False

# Object
def Initiative(owner, title, description, scope, workshop = None):
    i = Thing('initiative', owner.id)
    generic.linkChildToParent(i, owner)
    if workshop is not None:
        generic.linkChildToParent(i, workshop)
    commit(i)
    i['urlCode'] = utils.toBase62(i)
       
    i['title'] = title
    i['url'] = utils.urlify(title[:20])
    i['description'] = description
    i['background'] = ""
    i['tags'] = ""
    i['scope'] = scope
    i['deleted'] = u'0'
    i['disabled'] = u'0'
    i['published'] = u'0'
    i['ups'] = '0'
    i['downs'] = '0'
    commit(i)
    i = discussionLib.Discussion(owner = owner, discType = 'initiative', attachedThing = i, title = title)
    return i
