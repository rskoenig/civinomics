import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from pylowiki.model import get_all_pages, commit, getComment, getAllSuggestions, getSuggestionByID
from pylowiki.model import Event, get_user, getAllArticles, getArticle

import pylowiki.lib.helpers as h

from pylowiki.lib.base import BaseController, render

log = logging.getLogger(__name__)

class ModerationController(BaseController):

    @h.login_required
    def index(self, id1 = 'none', id2 = 'none'):
        log.info('%s accessing moderation page %s/%s'%(c.authuser.name, id1, id2))
        if c.authuser.accessLevel >= 200:
            c.title = '%s %s' %(id2, id1)
            c.type = id2
            if id1 == 'none' and id2 == 'none':
                c.title = 'Moderation panel'
                return render('/derived/moderation.html')
            elif id1 == 'comments':
                c.pages = get_all_pages()
                c.suggestions = getAllSuggestions()
                return render('/derived/commentModeration.mako')
            elif id1 == 'suggestions':
                c.suggestions = getAllSuggestions()
                return render('/derived/suggestionModeration.mako')
            elif id1 == 'articles':
                c.articles = getAllArticles()
                return render('/derived/articleModeration.mako')
            else:
                h.flash('Unknown moderation type!', 'warning')
                return redirect('/moderation')
        else:
            h.flash("You are not authorized to view that page", "warning")
            try:
                return redirect(session['return_to'])
            except:
                return redirect('/')
    
    @h.login_required
    def handler(self, id):
        if c.authuser.accessLevel >= 200:
            u = get_user(c.authuser.name)
            if id == 'comment':
                log.info('%s pushing changes in %s moderation' %(c.authuser.name, id))
                commentIDs = []
                c.pages = get_all_pages()
                for page in c.pages:
                    for comment in page.comments:
                        if comment.disabled:
                            commentIDs.append(comment.id)
                results = []
                c.commentIDs = commentIDs
                for id in session['comments']:
                    value = request.params[str(id)]
                    if value == '2':
                        continue
                    comment = getComment(id)
                    comment.pending = 0
                    comment.disabled = value
                    e = Event('C_enable', 'Enabled by %s'%c.authuser.name)
                    comment.events.append(e)
                    u.events.append(e)
                    commit(e)
            elif id == 'suggestion':
                log.info('%s pushing changes in %s moderation' %(c.authuser.name, id))
                for id in session['suggestions']:
                    value = request.params[str(id)]
                    if value == '2':
                        continue
                    s = getSuggestionByID(id)
                    s.pending = 0
                    s.disabled = value
                    e = Event('S_enable', 'Emabled by %s'%c.authuser.name)
                    s.events.append(e)
                    u.events.append(e)
                    commit(e)
                #return render('/derived/test3.html')
                #return redirect('/commentModeration/')
            elif id == 'article':
                log.info('%s pushing changes in %s moderation' %(c.authuser.name, id))
                for id in session['articles']:
                    value = request.params[str(id)]
                    if value == '2':
                        continue
                    a = getArticle(id)
                    a.pending = False
                    a.disabled = value
                    e = Event('A_enable', 'Emabled by %s'%c.authuser.name)
                    a.events.append(e)
                    u.events.append(e)
                    commit(e)

            return redirect('/moderation')
        else:
            h.flash("You are not authorized to view that page", "warning")
            try:
                return redirect(session['return_to'])
            except:
                return redirect('/')
