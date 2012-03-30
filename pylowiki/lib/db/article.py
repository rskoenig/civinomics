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
def getArticleByID(id):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'article').filter_by(id = id).one()
    except:
        return False

def getArticle(url, workshop):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'article').filter(Thing.data.any(wc('internalURL', url))).filter(Thing.data.any(wc('workshop_id', workshop.id))).one()
    except:
        return False

def getArticleByURL(url, workshopID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'article').filter(Thing.data.any(wc('url', url))).filter(Thing.data.any(wc('workshopID', workshopID))).one()
    except:
        return False

def getArticlesByWorkshopID(workshopID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'article').filter(Thing.data.any(wc('workshop_id', workshopID))).all()
    except:
        return False

def getArticleByTitle(title, workshopID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'article').filter(Thing.data.any(wc('title', title))).filter(Thing.data.any(wc('workshopID', workshopID))).one()
    except:
        return False

def getAllArticles():
    try:
        return meta.Session.query(Thing).filter_by(objType = 'article').all()
    except:
        return False

# Object
class Article(object):
    def __init__( self, url, title, comment, owner, workshop):
        a = Thing('article', owner.id)
        a['url'] = url
        a['title'] = title
        a['comment'] = comment
        a['internalURL'] = urlify(title)
        a['workshop_id'] = workshop.id
        a['type'] = 'post'
        a['pending'] = True
        a['disabled'] = False
        commit(a)
        self.a = a

