#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic
from pylons import config

log = logging.getLogger(__name__)

# Setters
# Getters
def getArticle(id):
    try:
        return meta.Session.query(Thing).filter_by(id = id).one()
    except:
        return False

def getArticleByURL(url, workshopID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'article').filter(Thing.data.any(with_characteristic('url', url))).filter(Thing.data.any(with_characteristic('workshopID', workshopID))).one()
    except:
        return False

def getArticlesByIssueID(workshopID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'article').filter(Thing.data.any(with_characteristic('workshopID', workshopID))).all()
    except:
        return False

def getArticleByTitle(title, workshopID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'article').filter(Thing.data.any(with_characteristic('title', title))).filter(Thing.data.any(with_characteristic('workshopID', workshopID))).one()
    except:
        return False

def getAllArticles():
    try:
        return meta.Session.query(Thing).filter_by(objType = 'article').all()
    except:
        return False


# Object
class Article(object):
    def __init__( self, url, title, ownerID, workshopID, related = '' ):
        a = Thing('article', ownerID)
        a['url'] = url
        a['title'] = title
        a['workshopID'] = workshopID
        a['related'] = related
        a['type'] = 'post'
        a['pending'] = True
        a['disabled'] = False
        commit(a)


