#-*- coding: utf-8 -*-
import logging

from pylons import tmpl_context as c
from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit
from dbHelpers import with_characteristic as wc, with_characteristic_like as wcl
from discussion import Discussion
from pylowiki.lib.utils import urlify, toBase62
from pylowiki.lib.db.flag import checkFlagged
from pylons import config
from time import time
from revision import Revision
import pylowiki.lib.db.revision as revisionLib
from tldextract import extract
import pylowiki.lib.db.generic as generic
from embedly import Embedly

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
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .one()
    except:
        return False

def getResourceByLink(link, parent):
    parentCodeKey = parent.objType + 'Code'
    try:
        return meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('link', link))).filter(Thing.data.any(wc(parentCodeKey, parent['urlCode']))).all()
    except:
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
        
def getResourcesByInitiativeCode(initiativeCode, disabled = '0', deleted = '0'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'resource')\
            .filter(Thing.data.any(wc('initiativeCode', initiativeCode)))\
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

def searchResources(keys, values, deleted = u'0', disabled = u'0', count = False):
    try:
        if type(keys) != type([]):
            keys = [keys]
            values = [values]
        m = map(wcl, keys, values)
        q = meta.Session.query(Thing)\
                .filter_by(objType = 'resource')\
                .filter(Thing.data.any(wc('deleted', deleted)))\
                .filter(Thing.data.any(wc('disabled', disabled)))\
                .filter(Thing.data.any(wc('workshop_searchable', '1')))\
                .filter(Thing.data.any(reduce(sa.or_, m)))
        if count:
            return q.count()
        return q.all()
    except Exception as e:
        log.error(e)
        return False

def searchInitiativeResources(keys, values, deleted = u'0', disabled = u'0', count = False):
    try:
        if type(keys) != type([]):
            keys = [keys]
            values = [values]
        m = map(wcl, keys, values)
        q = meta.Session.query(Thing)\
                .filter_by(objType = 'resource')\
                .filter(Thing.data.any(wc('deleted', deleted)))\
                .filter(Thing.data.any(wc('disabled', disabled)))\
                .filter(Thing.data.any(wc('initiative_public', '1')))\
                .filter(Thing.data.any(reduce(sa.or_, m)))
        if count:
            return q.count()
        return q.all()
    except Exception as e:
        log.error(e)
        return False

# setters
def getEObj(link):
    eKey = config['app_conf']['embedly.key']
    eClient = Embedly(eKey)
    eObj = eClient.oembed(link)
    if eObj['type'] == 'error':
        return False
    else:
        return eObj
    
def setAttributes(resource, eObj):
    resource['type'] = eObj['type']
    if eObj['type'] == 'photo':
        resource['info'] = eObj['url']
    elif eObj['type'] == 'video' or eObj['type'] == 'rich':
        resource['info'] = eObj['html']
    if 'width' in eObj.keys():
        resource['width'] = eObj['width']
    if 'height' in eObj.keys():
        resource['height'] = eObj['height']
    if 'provider_name' in eObj.keys():
        resource['provider_name'] = eObj['provider_name']
        
    if 'thumbnail_url' in eObj.keys():
        resource['thumbnail_url'] = eObj['thumbnail_url']
        resource['thumbnail_width'] = eObj['thumbnail_width']
        resource['thumbnail_height'] = eObj['thumbnail_height']
    commit(resource)
    
def editResource(resource, title, text, link, owner):
    try:
        revisionLib.Revision(owner, resource)
        if not link.startswith('http://') and not link.startswith('https://'):
                link = u'http://' + link
        if resource['link'] != link:
            resource['link'] = link
            resource['url'] = urlify(title)
            eObj = getEObj(link)
            if eObj:
                log.info("eObj is %s"%eObj)
                setAttributes(resource, eObj)
                
        resource['title'] = title
        resource['text'] = text

        commit(resource)
        return True
    except:
        log.error('ERROR: unable to edit resource')
        return False

# Object
def Resource(link, title, owner, workshop, privs, role = None, text = None, parent = None):
    if not link.startswith('http://') and not link.startswith('https://'):
            link = u'http://' + link
    eObj = getEObj(link)
    if not eObj:
        return False
        
    a = Thing('resource', owner.id)
    a['link'] = link
    setAttributes(a, eObj)
    a['url'] = urlify(title[:30])
    a['title'] = title
    if text is None:
        a['text'] = ''
    else:
        a['text'] = text
    if workshop is not None:
        a = generic.linkChildToParent(a, workshop)
    a = generic.linkChildToParent(a, owner)
    if parent is not None:
        a = generic.linkChildToParent(a, parent)
    a['disabled'] = '0'
    a['deleted'] = '0'
    a['ups'] = '0'
    a['downs'] = '0'
    a['views'] = '0'
    a = generic.addedItemAs(a, privs, role)
    commit(a)
    a['urlCode'] = toBase62(a)
    commit(a)
    if workshop is not None:
        d = Discussion(owner = owner, discType = 'resource', attachedThing = a, workshop = workshop, title = title, privs = privs, role = role)
    else:
        d = Discussion(owner = owner, discType = 'resource', attachedThing = a, title = title)
    a['discussion_child'] = d.d['urlCode']
    commit(a)
    return a
