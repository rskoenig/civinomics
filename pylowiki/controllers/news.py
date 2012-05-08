import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from pylowiki.lib.db.user import get_user, getUserByID
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.workshop import getWorkshop
from pylowiki.lib.db.event import Event
from pylowiki.lib.db.article import Article, getArticle, getArticleByLink, getArticlesByWorkshopID
from pylowiki.lib.db.discussion import getDiscussionByID
from pylowiki.lib.db.rating import getRatingByID

from pylowiki.lib.utils import urlify

from pylowiki.lib.base import BaseController, render
import pickle

#from pylowiki.lib.points import readThisPage

import pylowiki.lib.helpers as h

log = logging.getLogger(__name__)

class NewsController(BaseController):

    def index(self, id1, id2, id3, id4):
        workshopCode = id1
        workshopURL = id2
        resourceCode = id3
        resourceURL = id4
        
        c.w = getWorkshop(workshopCode, workshopURL)
        
        c.title = c.w['title']
        c.resource = getArticle(resourceCode, urlify(resourceURL), c.w)
        c.poster = getUserByID(c.resource.owner)
        
        c.otherResources = getArticlesByWorkshopID(c.w.id)
        for i in range(len(c.otherResources)):
            resource = c.otherResources[i]
            if resource.id == c.resource.id:
                c.otherResources.pop(i)
                break
        c.discussion = getDiscussionByID(int(c.resource['discussion_id']))
        c.lastmoddate = c.resource.date
        c.lastmoduser = getUserByID(c.resource.owner)
        
        if 'ratedThings_article_overall' in c.authuser.keys():
            """
                Here we get a list of tuples.  Each tuple is of the form (a, b), with the following mapping:
                a         ->    rated Thing's ID  (What was rated) 
                b         ->    rating Thing's ID (The rating object)
            """
            l = pickle.loads(str(c.authuser['ratedThings_article_overall']))
            for tup in l:
                if tup[0] == c.resource.id:
                    c.rating = getRatingByID(tup[1])
        
        return render('/derived/resource.html')

    @h.login_required
    def handler(self, id1, id2):
        code = id1
        url = id2
        
        linkURL = request.params['url']
        comment = request.params['data']
        title = request.params['title']
        
        w = getWorkshop(code, url)
        a = getArticleByLink(linkURL, w)

        if a:
            h.flash('Link already submitted for this issue', 'warning')
            return redirect('/workshop/%s/%s'%(code, url))

        a = Article(linkURL, title, comment, c.authuser, w)
        
        if 'resources' not in w.keys():
            w['resources'] = a.a.id
        else:
            w['resources'] = w['resources'] + ',' + str(a.a.id)
        
        w['numResources'] = int(w['numResources']) + 1
        commit(w)
        return redirect('/workshop/%s/%s'%(code, url))

    @h.login_required
    def readThis(self):
        if readThisPage(c.authuser.id, request.params['articleID'], 'article'):
            h.flash("You have read this article!", "success")
        else:
            h.flash("You have already read this article!", "warning")
        a = getArticle(request.params['articleID'])
        i = getIssueByID(request.params['issueID'])
        return redirect('/issue/%s/news/%s'%(i.page.url, a.title))
