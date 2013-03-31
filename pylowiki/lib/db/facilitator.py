#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, meta
from dbHelpers import commit, with_characteristic as wc
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.utils           as utils

log = logging.getLogger(__name__)

# Getters
def isFacilitator( user, workshop ):
   f = meta.Session.query(Thing).filter_by(objType = 'facilitator').filter_by(owner = user.id).filter(Thing.data.any(wc('workshopCode', workshop['urlCode']))).filter(Thing.data.any(wc('disabled', '0'))).filter(Thing.data.any(wc('pending', '0'))).all()
   if f:
      return True
   else:
      return False

def isPendingFacilitator( user, workshop ):
   f = meta.Session.query(Thing).filter_by(objType = 'facilitator').filter_by(owner = user.id).filter(Thing.data.any(wc('workshopCode', workshop['urlCode']))).filter(Thing.data.any(wc('disabled', '0'))).filter(Thing.data.any(wc('pending', '1'))).all()
   if f:
      return True
   else:
      return False

def getFacilitatorsByWorkshop( workshop, disabled = '0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'facilitator').filter(Thing.data.any(wc('disabled', disabled))).filter(Thing.data.any(wc('workshopCode', workshop['urlCode']))).all()
    except:
        return False

def getFacilitatorsByUser(user, disabled = '0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'facilitator').filter_by(owner = user.id).filter(Thing.data.any(wc('disabled', disabled))).all()
    except:
        return False

def getFacilitatorsByUserAndWorkshop(user, workshop, disabled = '0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'facilitator').filter_by(owner = user.id).filter(Thing.data.any(wc('workshopCode', workshop['urlCode']))).filter(Thing.data.any(wc('disabled', disabled))).all()
    except:
        return False

def getFacilitatorInWorkshop(user, workshop):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'facilitator')\
            .filter_by(owner = user.id)\
            .filter(Thing.data.any(wc('workshopCode', workshop['urlCode'])))\
            .one()
    except:
        return False

# Setters
def disableFacilitator( facilitator ):
    """disable this facilitator"""
    facilitator['disabled'] = '1'
    commit(facilitator)

def enableFacilitator( facilitator ):
    """enable the facilitator"""
    facilitator['disabled'] = '0'
    commit(facilitator)

# Object
class Facilitator(object):
    def __init__(self, user, workshop, pending = '0'):
        # note - the userID of the facilitator is the f.owner
        f = Thing('facilitator', user.id)
        f['disabled'] = u'0'
        f['pending'] = pending
        f['itemAlerts'] = u'1'
        f['flagAlerts'] = u'1'
        f['digest'] = u'0'
        generic.linkChildToParent(f, workshop)
        commit(f)
        f['urlCode'] = utils.toBase62(f)
        commit(f)
