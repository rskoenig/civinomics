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
def deleteSlideshow( slideshow ):
    """delete this slide"""
    slideshow['deleted'] = '1'
    commit(slideshow)

def undeleteSlideshow( slideshow ):
    """undelete this slide"""
    slideshow['deleted'] = '0'
    commit(slideshow)

def getSlideshow(workshop, deleted = u'0'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'slideshow')\
            .filter(Thing.data.any(wc('workshopCode', workshop['urlCode'])))\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .one()
    except:
        return False

def getSlideshowByCode(code, deleted = u'0'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'slideshow')\
            .filter(Thing.data.any(wc('urlCode', code)))\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .one()
    except:
        return False

def countSlideshowSlides(slideshowID, deleted = u'0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'slide').filter(Thing.data.any(wc('slideshowID', slideshowID))).filter(Thing.data.any(with_characteristic('deleted', deleted))).count()
    except:
        return False

def getAllSlides(slideshow):
    # Grabs all slides given a slideshow id, regardless of the slide's 'deleted' property
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'slide')\
            .filter(Thing.data.any(wc('slideshowCode', slideshow['urlCode'])))\
            .all()
    except:
        return False

def getSlidesInOrder(slideshow):
    try:
        if type(slideshow) in [type(1L), type(1), type(u'a')]:
            slideshow = getSlideshow(slideshow)
        slideshowOrder = map(int, [item for item in slideshow['slideshow_order'].split(',')])
        return [generic.getThingByID(slideID) for slideID in slideshowOrder] 
    except:
        return False

# Object creation
def Slideshow(owner, workshop):
    s = Thing('slideshow', owner.id)
    s['deleted'] = '0'
    s['disabled'] = '0'
    commit(s)
    generic.linkChildToParent(s, workshop)
    s['urlCode'] = utils.toBase62(s)
    commit(s)
    return s
