#-*- coding: utf-8 -*-
import logging
import datetime

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic
from pylons import config

log = logging.getLogger(__name__)

# Getters
def getMessage( parentID ):
    try:
        return meta.Session.query( Thing ).filter_by( objType = 'motd' ).filter(Thing.data.any(with_characteristic('parentID', parentID))).one()
    except sa.orm.exc.NoResultFound:
        return False

# Setters
def disableMessage( motd ):
    """disable this motd"""
    motd['disabled'] = True
    commit(motd)

def enableMessage( motd ):
    """enable the motd"""
    motd['disabled'] = False
    commit(motd)

# Object
class MOTD(object):
    def __init__(self, data, ownerID, parentID):
        m = Thing('motd', ownerID)
        m['parentID'] = parentID
        m['enabled'] = True
        m['data'] = data
        mCreated = datetime.datetime.now()
        m['lastModified'] = mCreated.ctime()
        commit(m)

