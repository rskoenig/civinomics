#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic
from pylowiki.lib.utils import toBase62
import pylowiki.lib.db.generic as generic

log = logging.getLogger(__name__)

def get_revision(id):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'revision').filter_by(id = id).one()
    except:
        return False

def getRevisionByCode(code):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'revision').filter(Thing.data.any(with_characteristic('urlCode', code))).one()
    except:
        return False

def get_all_revisions(pageID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'revision').filter(Thing.data.any(with_characteristic('pageID', pageID)))
    except:
        return False

def getParentRevisions(parent_id):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'revision').filter(Thing.data.any(with_characteristic('parent_id', parent_id))).order_by('-date').all()
    except:
        return False

def Revision(owner, thing):
    # A revision represents a snapshot of the entire object.
    r = Thing('revision', owner.id)
    for key in thing.keys():
        r[key] = thing[key]
    commit(r)
    r['urlCode'] = toBase62(r)
    generic.linkChildToParent(r, thing)
    commit(r)
    return r
