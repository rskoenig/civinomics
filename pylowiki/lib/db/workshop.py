from pylowiki.model import Thing, meta
from pylowiki.lib.utils import urlify, toBase62
from dbHelpers import commit, with_characteristic
import time

# Only support for one facilitator.  Otherwise we need to make a list and add/remove from it
def changeFacilitator(workshop, facilitator):
    workshop['facilitator'] = facilitator
    commit(workshop)
    return True

def getWorkshop(id):
    try:
        meta.Session.query(Thing).filter(Thing.data.any(with_characteristic(id, id))).one()
    except:
        return False

class Workshop(object):
    # title -> A string
    # owner -> A user object in Thing form
    def __init__(self, title, owner):
        w = Thing('workshop', owner.id)
        w['title'] = title
        w['url'] = urlify(title)
        w['urlCode'] = toBase62('%s_%s_%d'%(title, owner['name'], int(time.time())))
        commit(w)

    # Takes in a user's thing ID
    def addFacilitator(self, facilitator):
        self['facilitator'] = facilitator
