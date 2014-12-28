#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from sqlalchemy import and_, not_, or_
from dbHelpers import commit, with_characteristic as wc, with_characteristic_like as wcl
from pylons import config
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.db.discussion   as discussionLib
import pylowiki.lib.db.geoInfo      as geoInfoLib
import pylowiki.lib.utils           as utils 

log = logging.getLogger(__name__)

# Getters
def getUserPhotos(user, deleted = '0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'photo').filter(Thing.data.any(wc('userCode', user['urlCode']))).filter(Thing.data.any(wc('deleted', deleted))).all()
    except:
        return False
        
def getAllPhotos(deleted = '0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'photo').filter(Thing.data.any(wc('deleted', deleted))).all()
    except:
        return False

def getPhoto(photoCode):
    try:
        return meta.Session.query(Thing).filter(Thing.objType.in_(['photo', 'photoUnpublished'])).filter(Thing.data.any(wc('urlCode', photoCode))).one()
    except:
        return False  
        
def getPhotoByHash(imageHash):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'photo').filter(Thing.data.any(wc('pictureHash_photos', imageHash))).one()
    except:
        return False
        
def getPhotoLocation(photo):
    scope = photo['scope'].split('|')
    if scope[2] != '' and scope[2] != '0':
        country = geoInfoLib.geoDeurlify(scope[2].title())
        if scope[4] != '' and scope[4] != '0':
            state = geoInfoLib.geoDeurlify(scope[4].title())
            if scope[6] != '' and scope[6] != '0':
                county = geoInfoLib.geoDeurlify(scope[6].title())
                if scope[8] != '' and scope[8] != '0':
                    city = geoInfoLib.geoDeurlify(scope[8].title())
                    return country + ", State of " + state + ", County of " + county + ", City of " + city
                else:
                    return country + ", State of " + state + ", County of " + county
            else:
                return country + ", State of " + state
        else:
            return "Country of " + country
    else:
        return "Planet Earth"
    

def searchPhotos( keys, values, deleted = u'0', count = False):
    #log.info("db search")
    try:
        if type(keys) != type([]):
            p_keys = [keys]
            p_values = [values]
        else:
            p_keys = keys
            p_values = values
        map_photos = map(wcl, p_keys, p_values)
        q = meta.Session.query(Thing)\
                .filter_by(objType = 'photo')\
                .filter(Thing.data.any(wc('deleted', deleted)))\
                .filter(Thing.data.any(reduce(or_, map_photos)))
        if count:
            return q.count()
        return q.all()
    except Exception as e:
        log.error(e)
        return False
        
# Setters
def deletePhoto( photo ):
    photo['deleted'] = '1'
    commit(photo)
    
def unpublishPhoto( photo ):
    if 'user' in session and (c.authuser.id == photo.owner or userLib.isAdmin(c.authuser.id)):
        if c.authuser.id == photo.owner:
            photo['unpublished_by'] = 'owner'
        elif userLib.isAdmin(c.authuser.id):
            photo['unpublished_by'] = 'admin'
        
        # get the list of children
        children = generic.getChildrenOfParent(photo)
        for child in children:
            child['unpublished_by'] = 'parent'
            oldType = child.objType
            child.objType = oldType + 'Unpublished'
            commit(child)
        
        # now reset the object types to unpublished
        photo.objType = 'photoUnpublished'
        commit(photo)
    else:
        abort(404)
        
# Object
def Photo(owner, title, description, tags, scope):
    p = Thing('photo', owner.id)
    generic.linkChildToParent(p, owner)
    commit(p)
    p['urlCode'] = utils.toBase62(p)
       
    p['title'] = title
    p['url'] = utils.urlify(title[:20])
    p['description'] = description
    p['tags'] = tags
    p['scope'] = scope
    p['deleted'] = u'0'
    p['disabled'] = u'0'
    p['format'] = u'png'
    p['ups'] = '0'
    p['downs'] = '0'
    commit(p)
    d = discussionLib.Discussion(owner = owner, discType = 'photo', attachedThing = p, title = title)
    p['discussion_child'] = d.d['urlCode']
    commit(p)
    return p

def isPublic(photo):
    if photo.objType != 'photoUnpublished':
        return True
    else:
        return False