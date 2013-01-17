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

def getIdea(urlCode):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'idea')\
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

def getAllIdeas(deleted = '0', disabled = '0'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'idea')\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .all()
    except:
        return False

def editIdea(idea, title, owner):
    try:
        r = revisionLib.Revision(owner, idea)
        idea['title'] = title
        idea['url'] = urlify(title)
        commit(idea)
        return True
    except:
        log.error('ERROR: unable to edit idea')
        return False

def Idea(user, title, workshop):
    """
        user    ->  The user Thing creating the idea
        title   ->  The idea itself, in string format.
    """
    idea = Thing('idea', user.id)
    idea['title'] = title
    idea['disabled'] = '0'
    idea['deleted'] = '0'
    idea['allowComments'] = '1'
    idea['ups'] = '0'
    idea['downs'] = '0'
    idea['url'] = urlify(title[:20])
    commit(idea)
    idea['urlCode'] = toBase62(idea)
    d = Discussion(owner = user, discType = 'idea', attachedThing = idea, title = title, workshop = workshop)
    idea = generic.linkChildToParent(idea, workshop)
    commit(idea)
    return idea