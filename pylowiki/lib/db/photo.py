#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic as wc
from pylons import config
import pylowiki.lib.db.generic      as generic
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
    return p
