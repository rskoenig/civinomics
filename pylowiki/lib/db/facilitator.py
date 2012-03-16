#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, meta
from dbHelpers import commit, with_characteristic

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

