#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic as wc
from pylons import config
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.db.discussion   as discussionLib
import pylowiki.lib.utils           as utils
import pylowiki.lib.images          as imageLib 

log = logging.getLogger(__name__)

# Getters
def getPhoto(photoCode, deleted = '0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'photo').filter(Thing.data.any(wc('deleted', deleted))).one()
    except:
        return False
        
def getUserPhotos(user, deleted = '0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'photo').filter_by(owner = user.id).filter(Thing.data.any(wc('deleted', deleted))).all()
    except:
        return False

# Setters
def deletePhoto( photo ):
    photo['deleted'] = '1'
    commit(photo)

# Object
def Photo(owner, title, text, scope, tags, filename, image):
    image = imageLib.openImage(image)
    if not image:
        abort(404)
    p = Thing('photo', owner.id)
    commit(p)
    p['urlCode'] = utils.toBase62(p)
        
    imageHash = imageLib.generateHash(filename, p)
    image = imageLib.saveImage(image, imageHash, 'slide', 'orig', thing = p)
    image = imageLib.resizeImage(image, imageHash, 1200, 1200, preserveAspectRatio = True)
    image = imageLib.saveImage(image, imageHash, 'slide', 'slideshow')
    image = imageLib.resizeImage(image, imageHash, 128, 128, preserveAspectRatio = True)
    image = imageLib.saveImage(image, imageHash, 'slide', 'thumbnail')

        
    # finally
    p['pictureHash'] = imageHash
    p['title'] = title
    p['text'] = text
    p['scope'] = scope
    p['tags'] = tags
    p['filename'] = filename
    p['deleted'] = u'0'
    p['disabled'] = u'0'
    p['format'] = u'png'
    p['ups'] = '0'
    p['downs'] = '0'
    commit(p)
    d = Discussion(owner = user, discType = 'photo', attachedThing = photo)
    p['urlCode'] = utils.toBase62(p)
    commit(p)
    return p
