#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit
from dbHelpers import with_characteristic as wc
from discussion import Discussion
from pylowiki.lib.utils import urlify, toBase62
from pylowiki.lib.db.flag import checkFlagged
from pylons import config
from time import time
from tldextract import extract

log = logging.getLogger(__name__)

def getResourceOld1(urlCode, url):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('urlCode', urlCode))).filter(Thing.data.any(wc('url', url))).one()
    except:
        return False
    
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

def getResourceOld3(urlCode, url, workshop):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('urlCode', urlCode))).filter(Thing.data.any(wc('url', url))).filter(Thing.data.any(wc('workshop_id', workshop.id))).one()
    except:
        return False

def getResourceByLink(link, workshop):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('link', link))).filter(Thing.data.any(wc('workshop_id', workshop.id))).one()
    except:
        return False

def getResourceByURL(url, workshopID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('url', url))).filter(Thing.data.any(wc('workshopID', workshopID))).one()
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

def getResourcesByWorkshopID(workshopID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('workshop_id', workshopID))).all()
    except:
        return False

def getActiveResourcesByWorkshopID(workshopID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('workshop_id', workshopID))).filter(Thing.data.any(wc('disabled', '0'))).filter(Thing.data.any(wc('deleted', '0'))).filter(Thing.data.any(wc('parent_type', None))).all()
    except:
        return False

def getDisabledResourcesByWorkshopID(workshopID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('workshop_id', workshopID))).filter(Thing.data.any(wc('disabled', '1'))).all()
    except:
        return False

def getDeletedResourcesByWorkshopID(workshopID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('workshop_id', workshopID))).filter(Thing.data.any(wc('deleted', '1'))).all()
    except:
        return False

def getInactiveResourcesByWorkshopID(workshopID):
    InactiveRes = []
    DisabledRes = getDisabledResourcesByWorkshopID(workshopID)
    DeletedRes = getDeletedResourcesByWorkshopID(workshopID)
    if DisabledRes:
        InactiveRes = DisabledRes
    if DeletedRes:
        InactiveRes += DeletedRes
    if DisabledRes or DeletedRes:
        return InactiveRes
    else:
        return False

def getFlaggedResourcesByWorkshopID(workshopID):
    try:
        aList = meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('workshop_id', workshopID))).all()
        fList = []
        for a in aList:
           if checkFlagged(a) and a.id not in fList:
              fList.append(a.id)

        return fList
    except:
        return False

def getResourceByTitle(title, workshopID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'resource').filter(Thing.data.any(wc('title', title))).filter(Thing.data.any(wc('workshopID', workshopID))).one()
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
        a['urlCode'] = toBase62('%s_%s_%s'%(title, owner['name'], int(time())))
        a['title'] = title
        a['comment'] = comment
        a['allowComments'] = allowComments
        a['workshop_id'] = workshop.id
        if parent != None:
             a['parent_id'] = parent.id
             a['parent_type'] = parent.objType
        else:
             a['parent_id'] = None
             a['parent_type'] = None
        a['type'] = 'post'
        a['pending'] = False
        a['disabled'] = False
        a['deleted'] = False
        a['allowComments'] = True
        a['ups'] = 0
        a['downs'] = 0
        commit(a)
        if parent != None:
            if parent.objType == 'suggestion':
                d = Discussion(owner = owner, discType = 'sresource', attachedThing = a, workshop = workshop, title = title, suggestion = parent)
        else:
            d = Discussion(owner = owner, discType = 'resource', attachedThing = a, workshop = workshop, title = title)
        a['discussion_id'] = d.d.id
        self.a = a

