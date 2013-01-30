#-*- coding: utf-8 -*-
import logging

from pylons import tmpl_context as c
from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit
from dbHelpers import with_characteristic as wc
from discussion import Discussion
from pylowiki.lib.utils import urlify, toBase62
from pylowiki.lib.db.flag import checkFlagged
from pylons import config
from time import time
from revision import Revision
import pylowiki.lib.db.revision as revisionLib
from tldextract import extract
import pylowiki.lib.db.generic as generic

log = logging.getLogger(__name__)

def getResourceByID(id):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'resource').filter_by(id = id).one()
    except:
        return False

def getResource(urlCode, url):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('urlCode', urlCode))).filter(Thing.data.any(wc('url', url))).one()
    except:
        return False

def getResourceByCode(urlCode, disabled = '0', deleted = '0'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'resource')\
            .filter(Thing.data.any(wc('urlCode', urlCode)))\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .one()
    except:
        return False

def getResourceByLink(link, item):
    if item.objType == 'workshop':
        try:
            return meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('link', link))).filter(Thing.data.any(wc('workshopCode', item['urlCode']))).filter(Thing.data.any(wc('parent_id', '0'))).all()
        except:
            return False
    elif item.objType == 'suggestion':
        try:
            return meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('link', link))).filter(Thing.data.any(wc('parent_id', item.id))).all()
        except:
            return False
    else:
        return False

def getResourceByURL(url, workshopCode):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('url', url))).filter(Thing.data.any(wc('workshopCode', workshopCode))).one()
    except:
        return False

def getResourcesByParentID(parentID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('parent_id', parentID))).all()
    except:
        return False

def getActiveResourcesByParentID(parentID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('parent_id', parentID))).filter(Thing.data.any(wc('disabled', '0'))).filter(Thing.data.any(wc('deleted', '0'))).all()
    except:
        return False

def getResourcesByWorkshopCode(workshopCode, disabled = '0', deleted = '0'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'resource')\
            .filter(Thing.data.any(wc('workshopCode', workshopCode)))\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .all()
    except:
        return False

def getActiveResourcesByWorkshopCode(workshopCode):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('workshopCode', workshopCode))).filter(Thing.data.any(wc('disabled', '0'))).filter(Thing.data.any(wc('deleted', '0'))).all()
    except:
        return False

def getDisabledResourcesByWorkshopCode(workshopCode):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('workshopCode', workshopCode))).filter(Thing.data.any(wc('disabled', '1'))).all()
    except:
        return False

def getDeletedResourcesByWorkshopCode(workshopCode):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('workshopCode', workshopCode))).filter(Thing.data.any(wc('deleted', '1'))).all()
    except:
        return False

def getInactiveResourcesByWorkshopCode(workshopCode):
    InactiveRes = []
    DisabledRes = getDisabledResourcesByWorkshopCode(workshopCode)
    DeletedRes = getDeletedResourcesByWorkshopCode(workshopCode)
    if DisabledRes:
        InactiveRes = DisabledRes
    if DeletedRes:
        InactiveRes += DeletedRes
    if DisabledRes or DeletedRes:
        return InactiveRes
    else:
        return False

def getFlaggedResourcesByWorkshopCode(workshopCode):
    try:
        aList = meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('workshopCode', workshopCode))).all()
        fList = []
        for a in aList:
           if checkFlagged(a) and a.id not in fList:
              fList.append(a.id)

        return fList
    except:
        return False

def getResourceByTitle(title, workshopCode):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('title', title))).filter(Thing.data.any(wc('workshopCode', workshopCode))).one()
    except:
        return False

def getAllResources(deleted = '0', disabled = '0'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'resource')\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .all()
    except:
        return False

# setters
def editResource(resource, title, text, url, owner):
    try:
        revisionLib.Revision(owner, resource)
        resource['title'] = title
        resource['text'] = text
        if not url.startswith('http://'):
            url = u'http://' + url
        resource['link'] = url
        resource['url'] = urlify(title)
        tldResults = extract(url)
        resource['tld'] = tldResults.tld
        resource['domain'] = tldResults.domain
        resource['subdomain'] = tldResults.subdomain
        return True
    except:
        log.error('ERROR: unable to edit resource')
        return False

# Object
def Resource(url, title, owner, workshop, text = None, parent = None):
    a = Thing('resource', owner.id)
    if not url.startswith('http://'):
        url = u'http://' + url
    a['link'] = url # The resource's URL
    tldResults = extract(url)
    a['tld'] = tldResults.tld
    a['domain'] = tldResults.domain
    a['subdomain'] = tldResults.subdomain
    a['url'] = urlify(title[:30])
    a['title'] = title
    if text is None:
        a['text'] = ''
    else:
        a['text'] = text
    a = generic.linkChildToParent(a, workshop)
    if parent is not None:
        a = generic.linkChildToParent(a, parent)
    a['type'] = 'general'
    a['disabled'] = '0'
    a['deleted'] = '0'
    a['ups'] = '0'
    a['downs'] = '0'
    commit(a)
    a['urlCode'] = toBase62(a)
    commit(a)
    d = Discussion(owner = owner, discType = 'resource', attachedThing = a, workshop = workshop, title = title)
    r = revisionLib.Revision(c.authuser, a)
    return a
