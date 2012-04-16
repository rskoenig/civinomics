import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

#from pylowiki.model import Article, commit, getIssueByName, Event, get_user, getArticleByTitle, get_page
#from pylowiki.model import getIssueByID, getUserByID, getArticle

from pylowiki.lib.db.user import get_user, getUserByID
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.workshop import getWorkshop
from pylowiki.lib.db.event import Event
from pylowiki.lib.db.article import Article, getArticle

from pylowiki.lib.utils import urlify

from pylowiki.lib.base import BaseController, render

#from pylowiki.lib.points import readThisPage

import pylowiki.lib.helpers as h

log = logging.getLogger(__name__)

class NewsController(BaseController):

    def index(self, id1, id2, id3):
        code = id1
        workshopURL = id2
        articleURL = id3
        
        c.w = getWorkshop(code, workshopURL)
        
        c.title = c.w['title']
        c.article = getArticle(urlify(articleURL), c.w)
        log.info('articleURL = %s' % urlify(articleURL))
        log.info('workshop = %s' % c.w.id)
        log.info('Article: %s' % c.article.owner)
        c.poster = getUserByID(c.article.owner)
        
        return render('/derived/news_article.html')

    @h.login_required
    def handler(self, id1, id2):
        code = id1
        url = id2
        
        linkURL = request.params['url']
        comment = request.params['data']
        title = request.params['title']
        
        w = getWorkshop(code, url)
        a = getArticle(linkURL, w)

        if a:
            h.flash('Link already submitted for this issue', 'warning')
            return redirect('/workshop/%s/%s'%(code, url))

        a = Article(linkURL, title, comment, c.authuser, w)
        a = getArticle(urlify(title), w)
        
        if 'articles' not in w.keys():
            w['articles'] = a.id 
        else:
            w['articles'] = w['articles'] + ',' + str(a.id)
        
        w['numArticles'] = int(w['numArticles']) + 1
        e = Event('create', 'Added article %s'%a.id, c.authuser)
        commit(a)
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
