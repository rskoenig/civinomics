import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render
from pylowiki.model import get_all_pages, commit, get_comment, getAllSuggestions

import pylowiki.lib.helpers as h
import webhelpers.paginate as paginate
#from webhelpers.html.tags import radio

log = logging.getLogger(__name__)

class CommentmoderationController(BaseController):

    @h.login_required
    def index(self, id = "none"):
        if c.authuser.accessLevel >= 200:
            c.type = id
            c.pages = get_all_pages()
            c.suggestions = getAllSuggestions()
            if id == "pending":
                c.title = 'Pending comments'
            elif id == "disabled":
                c.title = 'Disabled comments'
            else:
                c.title = 'Incorrect moderation type'
            session['return_to'] = '/commentModeration/%s' % id
            return render('/derived/commentModeration.mako')
        else:
            h.flash("You are not authorized to view that page", "warning")
            try:
                return redirect(session['return_to'])
            except:
                return redirect('/')

    @h.login_required
    def handler(self):
        if c.authuser.accessLevel >= 200:
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
                comment = get_comment(id)
                comment.pending = 0
                comment.disabled = value
                commit(comment)
            #return render('/derived/test3.html')
            #return redirect('/commentModeration/')
            return redirect(session['return_to'])
        else:
            h.flash("You are not authorized to view that page", "warning")
            try:
                return redirect(session['return_to'])
            except:
                return redirect('/')
