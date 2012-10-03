#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic
from pylowiki.lib.utils import toBase62

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

# Every time a revision is made, we make a new revision Thing, and update the list of revisions with the Thing id
class Revision(Thing):
    def __init__(self, owner, data, thing):
        r = Thing('revision', owner.id)
        r['data'] = data
        if thing.objType == 'user':
            r['firstName'] = thing['firstName']
            r['lastName'] = thing['lastName']
            r['email'] = thing['email']
            r['postalCode'] = thing['postalCode']
            r['pictureHash'] = thing['pictureHash']
            if 'directoryNumber' in thing:
                r['directoryNumber'] = thing['directoryNumber']
            else:
                r['directoryNumber'] = ''

            if 'tagline' in thing:
                r['tagline'] = thing['tagline']
            else:
                r['tagline'] = ''

        if thing.objType == 'resource':
            r['title'] = thing['title']
            r['link'] = thing['link']

        if thing.objType == 'suggestion':
            r['title'] = thing['title']

        if thing.objType == 'discussion':
            if thing['discType'] == 'general':
                r['title'] = thing['title']

        commit(r)
        r['urlCode'] = toBase62(r)
        r['parent_id'] = thing.id
        commit(r)
        self.r = r
        
        if 'revisionList' not in thing.keys():
            thing['revisionList'] = r.id
        else:
            thing['revisionList'] = thing['revisionList'] + ',' + str(r.id)
        commit(thing)
