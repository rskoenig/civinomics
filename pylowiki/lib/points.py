from pylons import config
from pylowiki.model import getPoints, addPoints, commit, Article, Event, getPageByID, getUserByID
from pylowiki.model import getIssueByID, getArticleByTitle, getArticle

import logging
log = logging.getLogger(__name__)

""" Defines the number of points a user gets for an action """
def getPointListing():
    points = {}
    points['readBgWiki']        = 1
    points['readArticle']       = 1
    points['createIssue']       = 1
    
    return points

""" Possible refactoring in the future by passing in the point type """
def readThisPage(userID, thisID, type):
    pts = getPoints(userID)
    d = getPointListing()

    if type == 'background':
        page = getPageByID(thisID)
        e = Event('readBG', 'read background for %s' %page.title[:43])
        i = page.issue[0]
        a = getArticleByTitle(page.title, i.id)
    elif type == 'article':
        a = getArticle(thisID)
        e = Event('readArticle', 'read article for %s' %a.title[:44])
        #i = getIssueByID(a.events.issue_id)
        i = a.issue

    if pts.articles != None:
        l = [int(id) for id in pts.articles.split(',')]
    else:
        l = []
    if a.id in l:
        return False

    u = getUserByID(userID)
    u.events.append(e)
    a.events.append(e)
    i.events.append(e)
    if i not in u.issues:
        u.issues.append(i)
    ptsToAdd = d['readBgWiki']
    addPoints(userID, ptsToAdd)
    if pts.articles == None:
        pts.articles = a.id
    else:
        pts.articles += ',%d'%a.id
    commit(pts)
    commit(e)
    return True

