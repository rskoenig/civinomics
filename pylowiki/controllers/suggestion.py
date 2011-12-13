import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylowiki.model import get_page, getSuggestion, getIssueByID, getUserByID, Rating, Event, getSuggestionByID
from pylowiki.model import get_user, commit, get_page, getIssueByID, getAvgRatingForSuggestion, getRatingForSuggestion
from pylowiki.lib.base import BaseController, render

import simplejson as json

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

    def rate(self):
        issueID = request.params['issueID']
        suggestionID = request.params['suggestionID']
        rating = request.params['rate']

        i = getIssueByID(issueID)
        if i == False:
            log.info('i = false')
            return

        s = getSuggestionByID(suggestionID)
        if s == False:
            log.info('s = false')
            return

        r = getRatingForSuggestion(suggestionID, c.authuser.id)
        u = get_user(c.authuser.name)

        """ If a rating doesn't exist """
        if r == False:
            r = Rating('suggestion', rating)
            e = Event('rate_Su', 'User rated a suggestion')
            u.ratings.append(r)
            u.events.append(e)
            i.events.append(e)
            s.ratings.append(r)
            s.events.append(e)
            e.rating = r
            if commit(e) and commit(r):
                log.info('User %s just rated %s in %s as %s' %(c.authuser.name, s.title, i.name, rating))
                s.avgRating = getAvgRatingForSuggestion(s.id)
                if commit(s):
                    log.info('avg rating is now %s' % s.avgRating)
                    return json.dumps({'avgRating':s.avgRating})
        else:
            e = Event('rateSuCh', 'User changed a rating')
            r.rating = float(rating)
            u.events.append(e)
            s.events.append(e)
            i.events.append(e)
            s.avgRating = getAvgRatingForSuggestion(s.id)
            e.rating = r
            try: 
                commit(e)
                return json.dumps({'avgRating':s.avgRating})
            except:
                log.info('error in commiting change to rating.  User: %s, rating: %s, suggestion: %s'%(c.authuser.name, rating, suggestionID))
                return
