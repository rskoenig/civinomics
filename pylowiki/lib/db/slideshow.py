#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic
import pylowiki.lib.db.generic as genericLib
from pylons import config

log = logging.getLogger(__name__)

# Setters
def deleteSlideshow( slideshow ):
    """delete this slide"""
    slideshow['deleted'] = '1'
    commit(slideshow)

def undeleteSlideshow( slideshow ):
    """undelete this slide"""
    slideshow['deleted'] = '0'
    commit(slideshow)

# Getters
def getSlideshow(slideshowID, deleted = u'0'):
    try:
        return meta.Session.query(Thing).filter_by(id = slideshowID).filter(Thing.data.any(with_characteristic('deleted', deleted))).one()
    except:
        return False

def countSlideshowSlides(slideshowID, deleted = u'0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'slide').filter(Thing.data.any(with_characteristic('slideshowID', slideshowID))).filter(Thing.data.any(with_characteristic('deleted', deleted))).count()
    except:
        return False

def getAllSlides(slideshow_id):
    # Grabs all slides given a slideshow id, regardless of the slide's 'deleted' property
    try:
        return meta.Session.query(Thing).filter_by(objType = 'slide').filter(Thing.data.any(with_characteristic('slideshow_id', slideshow_id))).all()
    except:
        return False

def getSlidesInOrder(slideshow):
    try:
        if type(slideshow) in [type(1L), type(1), type(u'a')]:
            slideshow = getSlideshow(slideshow)
        slideshowOrder = map(int, [item for item in slideshow['slideshow_order'].split(',')])
        return [genericLib.getThingByID(slideID) for slideID in slideshowOrder] 
    except:
        return False

# Object
class Slideshow(object):
    def __init__( self, owner, workshop):
        s = Thing('slideshow', owner.id)
        s['workshop_id'] = workshop.id
        s['deleted'] = '0'
        self.s = s
        commit(s)
