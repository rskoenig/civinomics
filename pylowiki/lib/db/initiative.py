#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from sqlalchemy import and_, not_, or_
from dbHelpers import commit, with_characteristic as wc, with_characteristic_like as wcl
from pylons import config
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.db.discussion   as discussionLib
import pylowiki.lib.utils           as utils 

log = logging.getLogger(__name__)

# getter
def getInitiative(initiativeCode):
    try:
        return meta.Session.query(Thing).filter(Thing.objType.in_(['initiative', 'initiativeUnpublished'])).filter(Thing.data.any(wc('deleted', '0'))).filter(Thing.data.any(wc('urlCode', initiativeCode))).one()
    except:
        return False

def getInitiativesForUser(user):
    try:
        return meta.Session.query(Thing).filter(Thing.objType.in_(['initiative', 'initiativeUnpublished'])).filter(Thing.data.any(wc('deleted', '0'))).filter_by(owner = user.id).all()
    except:
        return False
        
def getAllInitiatives():
    try:
        return meta.Session.query(Thing).filter(Thing.objType.in_(['initiative', 'initiativeUnpublished'])).all()
    except:
        return False
        
def searchInitiatives( keys, values, deleted = u'0', public = '1', count = False):
    log.info("searchInititives got %s and %s and count is %s"%(keys, values, count))
    try:
        if type(keys) != type([]):
            p_keys = [keys]
            p_values = [values]
        else:
            p_keys = keys
            p_values = values
        log.info("search initiatives %s %s"%(keys, values))
        map_initiatives = map(wcl, p_keys, p_values)
        q = meta.Session.query(Thing)\
                .filter_by(objType = 'initiative')\
                .filter(Thing.data.any(wc('deleted', deleted)))\
                .filter(Thing.data.any(wc('public', public)))\
                .filter(Thing.data.any(reduce(or_, map_initiatives)))
        if count:
            return q.count()
        return q.all()
    except Exception as e:
        log.error(e)
        return False
        
def updateInitiativeChildren(initiative, initiativeKey):
    code = initiative['urlCode']        
    key = '%s%s' %(initiative.objType, 'Code')

    try:
        itemList = meta.Session.query(Thing)\
                .filter(Thing.objType.in_(['resource', 'discussion']))\
                .filter(Thing.data.any(wc(key, code)))\
                .all()
                
        for item in itemList:
            if initiativeKey == "initiative_title":
                item[initiativeKey] = initiative["title"]
                item['initiative_url'] = initiative['url']
            else:
                item[initiativeKey] = initiative[initiativeKey]
            commit(item)
            if item.objType == 'discussion':
                discussionCode = item['urlCode']
                commentList = meta.Session.query(Thing)\
                    .filter_by(objType = 'comment')\
                    .filter(Thing.data.any(wc('discussionCode', discussionCode)))\
                    .all()
                for comment in commentList:
                    if initiativeKey == "initiative_title":
                        comment[initiativeKey] = initiative["title"]
                        comment['initiative_url'] = initiative['url']
                    else:
                        comment[initiativeKey] = initiative[initiativeKey]
                    commit(comment)                            
    except Exception as e:
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
    i['proposal'] = ""
    i['tags'] = ""
    i['scope'] = scope
    i['cost'] = u'0'
    i['funding_summary'] = ""
    i['deleted'] = u'0'
    i['disabled'] = u'0'
    i['public'] = u'0'
    i['ups'] = '0'
    i['downs'] = '0'
    i['authors'] = owner['urlCode']
    commit(i)
    d = discussionLib.Discussion(owner = owner, discType = 'initiative', attachedThing = i, title = title)
    return i