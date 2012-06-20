#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit
from dbHelpers import with_characteristic as wc
from pylowiki.lib.utils import urlify
from pylons import config

log = logging.getLogger(__name__)

# Setters
# Getters
def getimageIdentifierByID(id):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'imageIdentifier').filter_by(id = id).one()
    except:
        return False

def getImageIdentifier(identifier):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'imageIdentifier').filter(Thing.data.any(wc('identifier', identifier))).one()
    except:
        return False

# Object
class ImageIdentifier(object):
    def __init__( self, identifier):
        i = Thing('imageIdentifier')
        i['identifier'] = identifier
        i['numImages'] = 0
        commit(i)
        self.i = i

