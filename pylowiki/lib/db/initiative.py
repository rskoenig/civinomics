#-*- coding: utf-8 -*-
import logging
import pickle

from pylons import session, tmpl_context as c
from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from sqlalchemy import and_, not_, or_
from dbHelpers import commit, with_characteristic as wc, with_characteristic_like as wcl, with_key as wk
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
        
def getInitiatives(initiativeCodes):
    try:
        return meta.Session.query(Thing)\
        .filter(Thing.objType.in_(['initiative', 'initiativeUnpublished']))\
        .filter(Thing.data.any(wc('deleted', '0')))\
        .filter(Thing.data.any(and_(Data.key == 'urlCode',Data.value.in_(initiativeCodes))))\
        .all()
    except:
        return False

def getInitiativeByURL(initiativeURL):
    try:
        return meta.Session.query(Thing).filter(Thing.objType.in_(['initiative', 'initiativeUnpublished'])).filter(Thing.data.any(wc('deleted', '0'))).filter(Thing.data.any(wc('url', initiativeURL))).one()
    except:
        return False

def getInitiativesForUser(user):
    try:
        return meta.Session.query(Thing).filter(Thing.objType.in_(['initiative'])).filter(Thing.data.any(wc('deleted', '0'))).filter_by(owner = user.id).all()
    except:
        return False

def setInitiativesForUserInSession():        
    # initiatives - these are a little odd in that we have to regenerate them every login because the session is set
    # both here and in the facilitator initialization.
    if 'facilitatorInitiatives' in session:
        facilitatorInitiatives = session['facilitatorInitiatives']
    else:
        facilitatorInitiatives = []
    initiativeList = getInitiativesForUser(c.authuser)
    facilitatorInitiatives += [initiative['urlCode'] for initiative in initiativeList if initiative['urlCode'] not in facilitatorInitiatives]

    c.authuser['facilitatorInitiatives'] = str(pickle.dumps(facilitatorInitiatives))
    commit(c.authuser)
    session["facilitatorInitiatives"] = facilitatorInitiatives
    session.save()
        
def getAllInitiatives():
    try:
        return meta.Session.query(Thing).filter(Thing.objType.in_(['initiative', 'initiativeUnpublished'])).all()
    except:
        return False

def getAllYesNoInitiatives():
    try:
        return meta.Session.query(Thing)\
        .filter(Thing.objType.in_(['initiative']))\
        .filter(not_(Thing.data.any(wk('workshopCode'))))\
        .all()
    except:
        return False
        
def getWorkshopCriteriaInitiatives(workshopCode):
    try:
        q = meta.Session.query(Thing)\
        .filter(Thing.objType.in_(['initiative']))\
        .filter(Thing.data.any(wc('workshopCode', workshopCode)))
        log.info(str(q))
        return q.all()
    except:
        return False

def getPublishedInitiatives():
    try:
        return meta.Session.query(Thing).filter(Thing.objType.in_(['initiative', 'initiativeUnpublished'])).filter(Thing.data.any(wc('deleted', '0'))).filter(Thing.data.any(wc('public', '1'))).all()
    except:
        return False
        
def searchInitiatives( keys, values, deleted = u'0', public = '1', count = False):
    #log.info("searchInititives got %s and %s and count is %s"%(keys, values, count))
    try:
        if type(keys) != type([]):
            p_keys = [keys]
            p_values = [values]
        else:
            p_keys = keys
            p_values = values
        #log.info("search initiatives %s %s"%(keys, values))
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
def Initiative(owner, title, description, scope, goal = None, workshop = None, **kwargs):
    i = Thing('initiative', owner.id)
    generic.linkChildToParent(i, owner)
    if workshop is not None:
        generic.linkChildToParent(i, workshop)
        i['workshop_searchable'] = '0' 
    commit(i)
    i['urlCode'] = utils.toBase62(i)
    i['title'] = title
    i['url'] = utils.urlify(title[:20])
    i['description'] = description
    i['background'] = ""
    i['proposal'] = ""
    if 'tag' in kwargs:
        i['tags'] = kwargs['tag']
    else:
        i['tags'] = ""
    i['scope'] = scope
    i['cost'] = u'0'
    i['funding_summary'] = ""
    i['deleted'] = u'0'
    i['disabled'] = u'0'
    i['public'] = u'0'
    i['ups'] = '0'
    i['downs'] = '0'
    i['views'] = '0'
    i['goal'] = goal
    commit(i)
    d = discussionLib.Discussion(owner = owner, discType = 'initiative', attachedThing = i, title = title)
    i['discussion_child'] = d.d['urlCode']
    commit(i)
    return i

def isPublic(initiative):
    if initiative['public'] == '1':
        return True
    else:
        return False