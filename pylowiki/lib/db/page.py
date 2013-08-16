#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
import pylowiki.lib.db.dbHelpers as dbHelpers
from dbHelpers import with_characteristic as wc
import pylowiki.lib.utils as utils
import pylowiki.lib.db.revision as revisionLib
import pylowiki.lib.db.generic as generic

log = logging.getLogger(__name__)

def getPage(code, disabled = '0', deleted = '0'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'page')\
            .filter(Thing.data.any(wc('urlCode', code)))\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .one()
    except:
        return False

def getPageByID(id, deleted = '0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'page').filter_by(id = id).filter(Thing.data.any(wc('deleted', deleted))).one()
    except:
        return False

def get_all_pages(deleted = '0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'page').filter(Thing.data.any(wc('deleted', deleted))).all()
    except:
        return False

def getInformation(workshop):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'page')\
            .filter(Thing.data.any(wc('workshopCode', workshop['urlCode'])))\
            .one()
    except:
        return False

def editInformation(page, data, owner):
    try:
        revisionLib.Revision(owner, page)
        page['data'] = data
        dbHelpers.commit(page)
        return True
    except:
        log.error("Error: unable to edit information for page %s" % page.id)
        return False

# Assumes title has already been validated
# Takes in a Thing object, sets its page property with the page's Thing id
def Page(title, owner, thing, data):
    p = Thing('page', owner.id)
    p['title'] = title
    p['url'] = utils.urlify(title)
    p['disabled'] = '0'
    p['deleted'] = '0'
    p['data'] = data
    dbHelpers.commit(p)
    p['urlCode'] = utils.toBase62(p)
    p = generic.linkChildToParent(p, thing)
    dbHelpers.commit(p)
    r = revisionLib.Revision(owner, p)
    return p