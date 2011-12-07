import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylowiki.model import get_page, getSuggestion, getIssueByID, getUserByID, Rating, Event, getSuggestionByURL
from pylowiki.model import get_user, commit, get_page, getIssueByName
from pylowiki.lib.base import BaseController, render

import pylowiki.lib.helpers as h

log = logging.getLogger(__name__)

class SuggestionController(BaseController):

    def index(self, id1, id2):
        c.p = get_page(id1)
        if c.p == False:
            abort(404, h.literal("That page does not exist!"))
        
        c.i = getIssueByID(c.p.issue[0].id)
        if c.i == False:
            abort(404, h.literal("That page does not exist!"))

        c.s = getSuggestion(id2, c.p.id)
        if c.s == False:
            abort(404, h.literal("That page does not exist!"))

        c.u = getUserByID(int(c.s.owners.split(',')[0]))

        c.title = c.p.title
        c.url = c.p.url

        r = c.s.revisions[0]
        c.content = h.literal(h.reST2HTML(r.data))

        return render('/derived/suggestion.html')

    def rate(self, id1, id2, id3):
        issueURL = id1
        suggestionURL = id2
        rating = id3
       
        p = get_page(issueURL)
        i = getIssueByName(p.title)
        if i == False:
            log.info('i = false')
            return

        s = getSuggestionByURL(suggestionURL, i.id)
        if s == False:
            log.info('s = false')
            return

        r = Rating('suggestion', rating)
        e = Event('rate_Su', 'User rated a suggestion')
        u = get_user(session['user'])
        u.ratings.append(r)
        u.events.append(e)
        s.ratings.append(r)
        if commit(e) and commit(r):
            log.info('User %s just rated %s in %s as %s' %(c.authuser.name, suggestionURL, issueURL, rating))
            return
