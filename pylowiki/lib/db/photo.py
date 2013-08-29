#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic as wc
from pylons import config
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.db.discussion   as discussionLib
import pylowiki.lib.utils           as utils 

log = logging.getLogger(__name__)

# Getters
def getUserPhotos(user, deleted = '0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'photo').filter(Thing.data.any(wc('userCode', user['urlCode']))).filter(Thing.data.any(wc('deleted', deleted))).all()
    except:
        return False

def getPhoto(photoCode):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'photo').filter(Thing.data.any(wc('urlCode', photoCode))).one()
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
        country = scope[2].title()
        if scope[4] != '' and scope[4] != '0':
            state = scope[4].title()
            if scope[6] != '' and scope[6] != '0':
                county = scope[6].title()
                if scope[8] != '' and scope[8] != '0':
                    city = scope[8].title()
                    return country + ", State of " + state + ", County of " + county + ", City of " + city
                else:
                    return country + ", State of " + state + ", County of " + county
            else:
                return country + ", State of " + state
        else:
            return "Country of " + country
    else:
        return "Planet Earth"
    

# Setters
def deletePhoto( photo ):
    photo['deleted'] = '1'
    commit(photo)

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
    return p
