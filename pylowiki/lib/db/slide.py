#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic
from pylons import config

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
class Slide(object):
    def __init__( self, pictureHash, caption, title, ownerID, slideShowID ):
        s = Thing('slideshow', ownerID)
        s['slideShow_id'] = slideShowID
        s['pictureHash'] = pictureHash
        s['caption'] = caption
        s['title'] = title
        commit(s)


