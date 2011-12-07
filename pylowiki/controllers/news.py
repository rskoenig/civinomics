import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from pylowiki.model import Article, commit, getIssueByName, Event, get_user, getArticleByTitle, get_page
from pylowiki.model import getIssueByID, getUserByID, getArticle

from pylowiki.lib.base import BaseController, render

from pylowiki.lib.points import readThisPage

import pylowiki.lib.helpers as h

log = logging.getLogger(__name__)

class NewsController(BaseController):

    def index(self, id1, id2):
        c.p = get_page(id1)
        c.title = c.p.title
        c.url = c.p.url
        if c.p == False:
            abort(404, h.literal("That page does not exist!"))

        c.i = getIssueByID(c.p.issue[0].id)
        if c.i == False:
            abort(404, h.literal("That page does not exist!"))

        c.article = getArticleByTitle(id2, c.i.id)
        log.info('article = %s'%(c.article))
        c.u = getUserByID(c.article.user_id)
        c.article.time = c.article.events[0].date
        return render('/derived/news_article.html')

    @h.login_required
    def handler(self, id):
        url = request.params['url']
        comment = request.params['data']
        title = request.params['title']
        i = getIssueByName(id)
        a = getArticleByTitle(url, i.id)

        if a:
            h.flash('Link already submitted for this issue', 'warning')
            return redirect('/issue/%s'%id.lower().replace(' ', '-'))

        a = Article(url, title)
        a.comment = comment
        a.related = i.id
        i.articles.append(a)
        e = Event('create', 'Added article %s'%title[:49])
        u = get_user(session['user'])
        a.user = u
        u.events.append(e)
        a.events.append(e)
        i.events.append(e)
        if commit(e) and commit(a):
            return redirect('/issue/%s'%id.lower().replace(' ', '-'))

    @h.login_required
    def readThis(self):
        if readThisPage(c.authuser.id, request.params['articleID'], 'article'):
            h.flash("You have read this article!", "success")
        else:
            h.flash("You have already read this article!", "warning")
        a = getArticle(request.params['articleID'])
        i = getIssueByID(request.params['issueID'])
        return redirect('/issue/%s/news/%s'%(i.page.url, a.title))
