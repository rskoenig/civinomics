#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit
from dbHelpers import with_characteristic as wc
from pylowiki.lib.utils import urlify
from revision import Revision

log = logging.getLogger(__name__)

def get_page(url, deleted = False):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'page').filter(Thing.data.any(wc('url', url))).filter(Thing.data.any(wc('deleted', deleted))).one()
    except:
        return False

def getPageByID(id, deleted = False):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'page').filter_by(id = id).filter(Thing.data.any(wc('deleted', deleted))).one()
    except:
        return False

def get_all_pages(deleted = False):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'page').filter(Thing.data.any(wc('deleted', deleted))).all()
    except:
        return False

# Assumes title has already been validated
# Takes in a Thing object, sets its page property with the page's Thing id
class Page(object):
    def __init__(self, title, owner, thing, data):
        p = Thing('page', owner.id)
        p['title'] = title
        p['url'] = urlify(title)
        p['type'] = thing.objType
        p['deleted'] = False
        commit(p)
        self.p = p
        
        r = Revision(owner, data, p)
        
        self.setThingProperties(p, r.r, thing)
        
    # thing in this case is the workshop Thing
    def setThingProperties(self, page, revision, thing):
        thing['page_id'] = page.id
        thing['mainRevision_id'] = revision.id
        commit(thing)