#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic

log = logging.getLogger(__name__)

def get_Revision(id):
    try:
        return meta.Session.query(Thing).filter_by(id = id).one()
    except:
        return False

def get_all_revisions(pageID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'revision').filter(Thing.data.any(with_characteristic('pageID', pageID)))
    except:
        return False

# Every time a revision is made, we make a new revision Thing, and add another revision key-value pair to the page
class Revision(Thing):
    def __init__(self, owner, data, pageID = None):
        r = Thing('revision', owner.id)
        r['data'] = data
        if pageID != None:
            r['page_id'] = pageID
        commit(r)