#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, meta
from dbHelpers import commit, with_characteristic as wc

log = logging.getLogger(__name__)

# Getters
def isFacilitator( userID, workshopID ):
   f = meta.Session.query(Thing).filter_by(objType = 'facilitator').filter_by(owner = userID).filter(Thing.data.any(wc('workshopID', workshopID))).filter(Thing.data.any(wc('disabled', '0'))).filter(Thing.data.any(wc('pending', 0))).all()
   if f:
      return True
   else:
      return False

def isPendingFacilitator( userID, workshopID ):
   f = meta.Session.query(Thing).filter_by(objType = 'facilitator').filter_by(owner = userID).filter(Thing.data.any(wc('workshopID', workshopID))).filter(Thing.data.any(wc('disabled', '0'))).filter(Thing.data.any(wc('pending', 1))).all()
   if f:
      return True
   else:
      return False

def getFacilitatorsByWorkshop( workshopID, disabled = False):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'facilitator').filter(Thing.data.any(wc('disabled', disabled))).filter(Thing.data.any(wc('workshopID', workshopID))).all()
    except:
        return False

def getFacilitatorsByUser(userID, disabled = False):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'facilitator').filter_by(owner = userID).filter(Thing.data.any(wc('disabled', disabled))).all()
    except:
        return False

def getFacilitatorsByUserAndWorkshop(userID, workshopID, disabled = False):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'facilitator').filter_by(owner = userID).filter(Thing.data.any(wc('workshopID', workshopID))).filter(Thing.data.any(wc('disabled', disabled))).all()
    except:
        return False

# Setters
def disableFacilitator( facilitator ):
    """disable this facilitator"""
    facilitator['disabled'] = True
    commit(facilitator)

def enableFacilitator( facilitator ):
    """enable the facilitator"""
    facilitator['disabled'] = False
    commit(facilitator)

# Object
class Facilitator(object):
    def __init__(self, userID, workshopID, pending = False):
        # note - the userID of the facilitator is the f.owner
        f = Thing('facilitator', userID)
        f['workshopID'] = workshopID
        f['disabled'] = 0
        f['pending'] = pending
        commit(f)
