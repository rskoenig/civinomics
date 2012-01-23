import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylowiki.model import Suggestion, get_user, Revision, Event, commit, get_page, getIssueByID

import pylowiki.lib.helpers as h

from pylowiki.lib.base import BaseController, render

log = logging.getLogger(__name__)

class AddsuggestionController(BaseController):

    @h.login_required
    def handler(self, id):
        title = request.params['title']
        data = request.params['data']
        tags = request.params['tags']
        s = Suggestion(title,c.authuser.id)
        if tags:
            s.tags = tags
        u = get_user(session['user'])
        r = Revision(data)
        e = Event('create')
        p = get_page(id)
        i = getIssueByID(p.id)
        i.suggestions.append(s)
        s.events.append(e)
        u.events.append(e)
        r.event = e
        s.revisions.append(r)
        s.url = title.replace(' ', '-')

        commit(e)

        return redirect('/issue/%s/suggestion/%s'%(id, title))
