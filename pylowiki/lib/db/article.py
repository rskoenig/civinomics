#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit
from dbHelpers import with_characteristic as wc
from discussion import Discussion
from pylowiki.lib.utils import urlify, toBase62
from pylowiki.lib.db.flag import checkFlagged
from pylons import config
from time import time
from tldextract import extract

log = logging.getLogger(__name__)

def getArticleByID(id):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'article').filter_by(id = id).one()
    except:
        return False

def getArticle(urlCode, url, workshop):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'article').filter(Thing.data.any(wc('urlCode', urlCode))).filter(Thing.data.any(wc('url', url))).filter(Thing.data.any(wc('workshop_id', workshop.id))).one()
    except:
        return False

def getArticleByLink(link, workshop):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'article').filter(Thing.data.any(wc('link', link))).filter(Thing.data.any(wc('workshop_id', workshop.id))).one()
    except:
        return False

def getArticleByURL(url, workshopID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'article').filter(Thing.data.any(wc('url', url))).filter(Thing.data.any(wc('workshopID', workshopID))).one()
    except:
        return False

def getArticlesByWorkshopID(workshopID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'article').filter(Thing.data.any(wc('workshop_id', workshopID))).filter(Thing.data.any(wc('disabled', 0))).all()
    except:
        return False

def getDisabledArticlesByWorkshopID(workshopID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'article').filter(Thing.data.any(wc('workshop_id', workshopID))).filter(Thing.data.any(wc('disabled', 1))).all()
    except:
        return False

def getFlaggedArticlesByWorkshopID(workshopID):
    try:
        aList = meta.Session.query(Thing).filter_by(objType = 'article').filter(Thing.data.any(wc('workshop_id', workshopID))).all()
        fList = []
        for a in aList:
           if checkFlagged(a) and a.id not in fList:
              fList.append(a.id)

        return fList
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
        if not url.startswith('http://'):
            url = u'http://' + url
        a['link'] = url # The resource's URL
        tldResults = extract(url)
        a['tld'] = tldResults.tld
        a['domain'] = tldResults.domain
        a['subdomain'] = tldResults.subdomain
        a['url'] = urlify(title[:30])
        a['urlCode'] = toBase62('%s_%s_%s'%(title, owner['name'], int(time())))
        a['title'] = title
        a['comment'] = comment
        a['workshop_id'] = workshop.id
        a['type'] = 'post'
        a['pending'] = False
        a['disabled'] = False
        commit(a)
        d = Discussion(owner = owner, discType = 'resource', attachedThing = a, workshop = workshop, title = title)
        a['discussion_id'] = d.d.id
        self.a = a

