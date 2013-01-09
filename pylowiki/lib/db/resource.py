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

def getResourceByCode(urlCode):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('urlCode', urlCode))).one()
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

def getResourcesByWorkshopCode(workshopCode):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('workshopCode', workshopCode))).all()
    except:
        return False

def getActiveResourcesByWorkshopCode(workshopCode):
    try:
        #return meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('workshopCode', workshopCode))).filter(Thing.data.any(wc('disabled', '0'))).filter(Thing.data.any(wc('deleted', '0'))).filter(Thing.data.any(wc('parent_type', None))).all()
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

def getAllResources():
    try:
        return meta.Session.query(Thing).filter_by(objType = 'resource').all()
    except:
        return False

# Object
class Resource(object):
    def __init__( self, url, title, comment, owner, allowComments, workshop, parent = None):
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
        a['comment'] = comment
        a['allowComments'] = allowComments
        a = generic.linkChildToParent(a, workshop)
        if parent != None:
             a['parent_id'] = parent.id
             a['parent_type'] = parent.objType
        else:
             a['parent_id'] = 0
             a['parent_type'] = None
        a['type'] = 'post'
        a['pending'] = '0'
        a['disabled'] = '0'
        a['deleted'] = '0'
        a['allowComments'] = '1'
        a['ups'] = '0'
        a['downs'] = '0'
        commit(a)
        a['urlCode'] = toBase62(a)
        if parent != None:
            if parent.objType == 'suggestion':
                d = Discussion(owner = owner, discType = 'sresource', attachedThing = a, workshop = workshop, title = title, suggestion = parent)
        else:
            d = Discussion(owner = owner, discType = 'resource', attachedThing = a, workshop = workshop, title = title)
        self.a = a
        commit(a)
        data = a['comment']
        r = Revision(c.authuser, data, a)

