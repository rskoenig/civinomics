#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic

log = logging.getLogger(__name__)

def get_revision(id):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'revision').filter_by(id = id).one()
    except:
        return False

def get_all_revisions(pageID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'revision').filter(Thing.data.any(with_characteristic('pageID', pageID)))
    except:
        return False

# Every time a revision is made, we make a new revision Thing, and update the list of revisions with the Thing id
class Revision(Thing):
    def __init__(self, owner, data, thing):
        r = Thing('revision', owner.id)
        r['data'] = data
        commit(r)
        self.r = r
        
        if 'revisionList' not in thing.keys():
            thing['revisionList'] = r.id
        else:
            thing['revisionList'] = thing['revisionList'] + ',' + str(r.id)
        commit(thing)