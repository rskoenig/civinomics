#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, meta
from dbHelpers import commit, with_characteristic as wc

log = logging.getLogger(__name__)

# Getters
def isFacilitator( userID, workshopID ):
   f = meta.Session.query(Thing).filter_by(objType = 'facilitator').filter_by(owner = userID).filter(Thing.data.any(wc('workshopID', workshopID))).all()
   if f:
      return True
   else:
      return False

def getFacilitators( workshopID, disabled = False):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'facilitator').filter(Thing.data.any(wc('disabled', disabled))).filter(Thing.data.any(wc('workshopID', workshopID))).all()
    except:
        return False

def getUserFacilitators(userID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'facilitator').filter_by(owner = userID).all()
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
    def __init__(self, userID, workshopID, disabled = False):
        # note - the userID of the facilitator is the f.owner
        f = Thing('facilitator', userID)
        f['workshopID'] = workshopID
        f['disabled'] = disabled
        commit(f)

