#-*- coding: utf-8 -*-
import logging

from pylons import tmpl_context as c, config
from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from time import time

import dbHelpers as dbHelpers
import discussion as discussionLib
import pylowiki.lib.utils as utilsLib
import flag as flgLib
import revision as revisionLib
import generic as genericLib

from embedly import Embedly
from tldextract import extract

log = logging.getLogger(__name__)

def getCommResourceByCode(urlCode, disabled = '0', deleted = '0'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'commresource')\
            .filter(Thing.data.any(wc('urlCode', urlCode)))\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .one()
    except:
        return False

def getAllCommResources(deleted = '0', disabled = '0'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'commresource')\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .all()
    except:
        return False

def searchCommResources(keys, values, deleted = u'0', disabled = u'0', count = False):
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
        
def getCommResourceTypes():
    crtypes = []
    crtypes.append('Blogs and Podcasts')
    crtypes.append('Civic and Municipal')
    crtypes.append('Community Services')
    crtypes.append('Galleries and Museums')
    crtypes.append('Libraries')
    crtypes.append('News Media')
    crtypes.append('Public Parks')
    crtypes.append('Public WiFi')
    crtypes.append('Schools')
    crtypes.append('Weather Stations')
    crtypes.append('Web Cams')

    return crtypes

# setters
def getEObj(link):
    eKey = config['app_conf']['embedly.key']
    eClient = Embedly(eKey)
    eObj = eClient.oembed(link)
    if eObj['type'] == 'error':
        return False
    else:
        return eObj
    
def setAttributes(commresource, eObj):
    commresource['type'] = eObj['type']
    if eObj['type'] == 'photo':
        commresource['info'] = eObj['url']
    elif eObj['type'] == 'video' or eObj['type'] == 'rich':
        commresource['info'] = eObj['html']
    if 'width' in eObj.keys():
        commresource['width'] = eObj['width']
    if 'height' in eObj.keys():
        commresource['height'] = eObj['height']
    if 'provider_name' in eObj.keys():
        commresource['provider_name'] = eObj['provider_name']
        
    if 'thumbnail_url' in eObj.keys():
        commresource['thumbnail_url'] = eObj['thumbnail_url']
        commresource['thumbnail_width'] = eObj['thumbnail_width']
        commresource['thumbnail_height'] = eObj['thumbnail_height']
    dbHelpers.commit(commresource)
    
# Object
def Commresource(owner, **kwargs):
    # get mandatory info first
    error = 0
    if 'title' in kwargs:
        title = kwargs['title']
    else:
        error = 1
        
    if 'text' in kwargs:
        text = kwargs['text']
    else:
        error = 1
        
    if 'type' in kwargs:
        type = kwargs['type']
    else:
        error = 1
        
    if 'scope' in kwargs:
        scope = kwargs['scope']
    else:
        error = 1
    
    # return with an error if we don't have all of our mandatory info    
    if error == 1:
        return 
    
    if 'role' in kwargs:
        role = kwargs['role']
    else:
        role = None
        
    c = Thing('commresource', owner.id)
    c['title'] = title
    c['text'] = text
    c['type'] = type
    c['scope'] = scope
    c['disabled'] = '0'
    c['deleted'] = '0'
    c['ups'] = '0'
    c['downs'] = '0'
    c = genericLib.addedItemAs(c, c.privs, role)
    dbHelpers.commit(c)
    
    # get the optional fields here
    
    c['urlCode'] = toBase62(c)
    dbHelpers.commit(c)
    
    # set the discussion for later comments
    d = discussionLib.Discussion(owner = owner, discType = 'commresource', attachedThing = c, title = title)
    
    return c
