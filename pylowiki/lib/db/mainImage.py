#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, meta
import sqlalchemy as sa
from sqlalchemy import or_
from dbHelpers import commit
from dbHelpers import with_characteristic as wc

import pylowiki.lib.utils           as utils
import pylowiki.lib.db.revision     as revisionLib
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.images          as imageLib

log = logging.getLogger(__name__)

def getMainImage(workshop):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'mainImage')\
            .filter(Thing.data.any(wc('workshopCode', workshop['urlCode'])))\
            .one()
    except:
        return False

def setMainImage(user, workshop, slide):
    """
        user        ->  The user Thing creating the mainImage
        workshop    ->  The workshop to which this image is being attached
        slide       ->  The slide object being set as the MainImage
        
        With a small amount of modification (assume Thing instead of slide), this can be rewritten
        to give any object with a urlCode a mainImage.
    """
    mainImage = getMainImage(workshop)
    if not mainImage:
        mainImage = Thing('mainImage', user.id)
        generic.linkChildToParent(mainImage, workshop)
        commit(mainImage)
        mainImage['urlCode'] = utils.toBase62(mainImage)
        
    if slide['pictureHash'] != 'supDawg':
        imageLocation, directoryNum = imageLib.getImageLocation(slide)
        image = open(imageLocation, 'rb')
        imgHash = imageLib.saveImage(image, slide['pictureHash'], 'mainImage', mainImage)
        imageLib.resizeImage('mainImage', imgHash, 128, 128, 'thumbnail', preserveAspectRatio = True)
        imageLib.resizeImage('mainImage', imgHash, 400, 400, 'listing', preserveAspectRatio = True)
        image.close()
    else:
        imgHash = u'supDawg'
        directoryNum = u'0'
    mainImage['pictureHash'] = imgHash
    # Possible edge case: orig is in directory 0, thumbnail in directory 1.  But all three get processed 
    # in the same function, so this *shouldn't* happen
    mainImage['directoryNum'] = directoryNum
    commit(mainImage)
    return mainImage