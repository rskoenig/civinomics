#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic
from pylons import config

from pylowiki.lib.images import saveImage, resizeImage

log = logging.getLogger(__name__)

# Getters
def getSlide(slideID, deleted = False):
    try:
        return meta.Session.query(Thing).filter_by(id = slideID).filter(Thing.data.any(with_characteristic('deleted', deleted))).one()
    except:
        return False

# Setters
def deleteSlide( slide ):
    """delete this slide"""
    slide['deleted'] = True
    commit(slide)

def undeleteSlide( slide ):
    """undelete this slide"""
    slide['deleted'] = False
    commit(slide)

# Object
# If newSlide is False, then we are dealing with the initialization of a workshop, in which case we do not need to save the image.
class Slide(object):
    def __init__( self, owner, slideshow, title, caption, filename, image, newSlide = False):
        if newSlide:
            s = Thing('slide', owner.id)
            s['slideShow_id'] = slideshow.id
            hash = saveImage(image, filename, owner, 'slide')
            s['pictureHash'] = hash
            s['caption'] = caption
            s['title'] = title
            s['filename'] = filename
            s['deleted'] = 0
            commit(s)
            self.s = s        
    
            # identifier, hash, x, y, postfix
            resizeImage('slide', hash, 835, 550, 'slideshow')
            resizeImage('slide', hash, 120, 65, 'thumbnail')
        else:
            s = Thing('slide', owner.id)
            hash = 'supDawg'
            s['slideShow_id'] = slideshow.id
            s['pictureHash'] = hash
            s['caption'] = caption
            s['title'] = title
            s['filename'] = filename
            s['deleted'] = 0
            commit(s)
            self.s = s