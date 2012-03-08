#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit
from dbHelpers import with_characteristic as wc
from pylowiki.lib.db.utils import urlify

log = logging.getLogger(__name__)

def get_page(url, deleted = False):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'page').filter(Thing.data.any(wc('url', url))).filter(Thing.data.any(wc('deleted', deleted))).one()
    except:
        return False

def getPageByID(id, deleted = False):
    try:
        return meta.Session.query(Thing).filter_by(id = id).filter(Thing.data.any(wc('deleted', deleted))).one()
    except:
        return False

def get_all_pages(deleted = False):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'page').filter(Thing.data.any(wc('deleted', deleted))).all()
    except:
        return False

# Assumes title has already been validated
class Page(object):
    def __init__(self, title, owner, type):
        p = Thing('page', owner.id)
        p['title'] = title
        p['url'] = urlify(title)
        p['type'] = type
        p['deleted'] = False
        
