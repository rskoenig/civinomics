import logging
import pickle

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from pylowiki.lib.base import BaseController, render
from pylowiki.lib.db.suggestion import getSuggestion
from pylowiki.lib.db.suggestion import getSuggestion
from pylowiki.lib.db.rating import Rating, changeRating
from pylowiki.lib.db.workshop import getWorkshop


import pylowiki.lib.helpers as h

log = logging.getLogger(__name__)

class RatingController(BaseController):

    def index(self):
        c.rating = '100'
        return render('/derived/rating.html')


    @h.login_required
    def rateSuggestion(self, id1, id2, id3):
        code = id1
        url = id2
        amount = int(id3)
        log.info('%s %s %s' % (id1, id2, id3))
        rKey = 'ratedThings_suggestion_overall'
        log.info('getSuggestion %s %s %s' % (id1, id2, id3))
        s = getSuggestion(code, url)
        if not s:
           log.info('getWorkshop %s %s %s' % (id1, id2, id3))
           s = getWorkshop(code, url)
           rKey = 'ratedThings_workshop_overall'

        found = False
        if rKey in c.authuser.keys():
            """
                Here we get a list of tuples.  Each tuple is of the form (a, b), with the following mapping:
                a         ->    rated Thing's ID  (What was rated) 
                b         ->    rating Thing's ID (The rating object)
            """
            l = pickle.loads(str(c.authuser[rKey]))
            for tup in l:
                if tup[0] == s.id:
                    found = True
                    changeRating(s, tup[1], amount)
            
        if not found:
            r = Rating(amount, s, c.authuser, 'overall')
        return "ok"
        
