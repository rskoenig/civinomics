#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, meta
import sqlalchemy as sa
from sqlalchemy import or_
from dbHelpers import commit
from dbHelpers import with_characteristic as wc, with_characteristic_like as wcl, greaterThan_characteristic as gtc
from pylowiki.lib.utils import urlify, toBase62
from discussion import Discussion
import pylowiki.lib.db.revision as revisionLib
import generic

log = logging.getLogger(__name__)

def getIdea(urlCode, deleted = u'0'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'idea')\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .filter(Thing.data.any(wc('urlCode', urlCode))).one()
    except:
        return False

def getIdeasInWorkshop(workshopCode, deleted = '0', disabled = '0'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'idea')\
            .filter(Thing.data.any(wc('workshopCode', workshopCode)))\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .filter(Thing.data.any(wc('disabled', disabled))).all()
    except:
        return False

def getAllIdeasInWorkshop(workshopCode, deleted = '0'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'idea')\
            .filter(Thing.data.any(wc('workshopCode', workshopCode)))\
            .filter(Thing.data.any(wc('deleted', deleted))).all()
    except:
        return False

def getAllIdeas(deleted = '0', disabled = '0'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'idea')\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .all()
    except:
        return False

def editIdea(idea, title, text, owner):
    try:
        r = revisionLib.Revision(owner, idea)
        idea['title'] = title
        idea['text'] = text
        idea['url'] = urlify(title)
        commit(idea)
        return True
    except:
        log.error('ERROR: unable to edit idea')
        return False

def adoptIdea(idea):
    idea['adopted'] = '1'
    commit(idea)
    return True
        
def isAdopted(idea):
    if idea['adopted'] == '1':
        return True
        
    return False

def searchIdeas(key, value, count = False, deleted = u'0', disabled = u'0'):
    try:
        q = meta.Session.query(Thing).filter_by(objType = 'idea')\
            .filter(Thing.data.any(wcl(key, value)))\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .filter(Thing.data.any(wc('workshop_searchable', '1')))
        if count:
            return q.count()
        return q.all()
    except:
        return False

def Idea(user, title, text, workshop, privs, role = None, **kwargs):
    """
        user    ->  The user Thing creating the idea
        title   ->  The idea itself, in string format.
        text   ->   The additional text, in string format
    """
    idea = Thing('idea', user.id)
    idea['title'] = title
    idea['text'] = text
    idea['disabled'] = '0'
    idea['deleted'] = '0'
    idea['adopted'] = '0'
    idea['allowComments'] = '1'
    idea['ups'] = '0'
    idea['downs'] = '0'
    idea['views'] = '0'
    idea['url'] = urlify(title[:20])
    if 'geoScope' in kwargs:
        idea['scope'] = kwargs['geoScope']
        idea['public'] = '1'
    idea = generic.addedItemAs(idea, privs, role)
    commit(idea)
    idea['urlCode'] = toBase62(idea)
    if workshop is not None:
        d = Discussion(owner = user, discType = 'idea', attachedThing = idea, title = title, workshop = workshop, privs = privs, role = role)
        idea = generic.linkChildToParent(idea, workshop)
    else:
        d = Discussion(owner = user, discType = 'idea', attachedThing = idea, title = title, privs = privs, role = role)

	
    idea['discussion_child'] = d.d['urlCode']
    idea = generic.linkChildToParent(idea, user)
    commit(idea)
    return idea