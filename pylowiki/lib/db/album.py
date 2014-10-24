#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic as wc
import pylowiki.lib.db.generic as generic
import pylowiki.lib.utils as utils
from pylons import config

log = logging.getLogger(__name__)

# Setters
def deleteAlbum( album ):
    album['deleted'] = '1'
    commit(album)

def getAlbumsForUser(user):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'album')\
            .filter(Thing.data.any(wc(parentKey, parentValue)))\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .one()
    except:
        return False

def getAlbumByCode(code):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'album')\
            .filter(Thing.data.any(wc('urlCode', code)))\
            .one()
    except:
        return False

def countAlbumPhotos(albumCode, deleted = u'0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'photo').filter(Thing.data.any(wc('albumCode', albumCode))).filter(Thing.data.any(with_characteristic('deleted', deleted))).count()
    except:
        return False

def getAllPhotos(albumCode):
    # Grabs all photos, regardless of the slide's 'deleted' property
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'album')\
            .filter(Thing.data.any(wc('albumCode', albumCode)))\
            .all()
    except:
        return False

# Object creation
def Album(owner, title):
    a = Thing('album', owner.id)
    a['title'] = title
    a['deleted'] = '0'
    a['disabled'] = '0'
    a['ups'] = '0'
    a['downs'] = '0'
    a['mainImage'] = 'None'
    commit(s)
    a['urlCode'] = utils.toBase62(a)
    d = Discussion(owner = user, discType = 'album', attachedThing = album)
    commit(a)
    return a
