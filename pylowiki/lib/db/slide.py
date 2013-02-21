#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic
from pylons import config
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.utils           as utils
from pylowiki.lib.images import saveImage, resizeImage

log = logging.getLogger(__name__)

# Getters
def getSlide(slideID, deleted = '0'):
    try:
        return meta.Session.query(Thing).filter_by(id = slideID).filter_by(objType = 'slide').filter(Thing.data.any(with_characteristic('deleted', deleted))).one()
    except:
        return False

def forceGetSlide(slideID):
    try:
        return meta.Session.query(Thing).filter_by(id = slideID).filter_by(objType = 'slide').one()
    except:
        return False

# Setters
def deleteSlide( slide ):
    """delete this slide"""
    slide['deleted'] = '1'
    commit(slide)

def undeleteSlide( slide ):
    """undelete this slide"""
    slide['deleted'] = '0'
    commit(slide)

# Object
# If newSlide is False, then we are dealing with the initialization of a workshop, in which case we do not need to save the image.
def Slide(owner, slideshow, title, filename, image, newSlide = '0'):
    if newSlide != '0':
        s = Thing('slide', owner.id)
        generic.linkChildToParent(s, slideshow)
        commit(s)
        s['urlCode'] = utils.toBase62(s)
        hash = saveImage(image, filename, 'slide', s)
        slideshow['slideshow_order'] = slideshow['slideshow_order'] + ',' + str(s.id)
        # identifier, hash, x, y, postfix
        resizeImage('slide', hash, 99999, 99999, 'slideshow') # don't resize, but antialias and save appropriately
        resizeImage('slide', hash, 128, 128, 'thumbnail')
    else:
        s = Thing('slide', owner.id)
        s['urlCode'] = utils.toBase62(s)
        hash = 'supDawg'
        generic.linkChildToParent(s, slideshow)
        
    # finally
    s['pictureHash'] = hash
    s['title'] = title
    s['filename'] = filename
    s['deleted'] = u'0'
    s['disabled'] = u'0'
    commit(s)
    return s
