#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic
from pylowiki.lib.utils import urlify, toBase62
from time import time

log = logging.getLogger(__name__)

def getDiscussionByID(id):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'discussion').filter_by(id = id).one()
    except:
        return False

class Discussion(object):
    # If the owner is None, the discussion is a system generated discussion, like the comments in the background wiki.
    # If the owner is not None, then the discussion was actively created by some user.
    def __init__(self, title, owner = None):
        if owner == None:
            d = Thing('discussion')
        else:
            d = Thing('discussion', owner.id)
        d['title'] = title
        d['url'] = urlify(title)
        d['urlCode'] = toBase62('%s_%s'%(title, int(time())))
        d['numComments'] = 0
        commit(d)
        
        self.d = d