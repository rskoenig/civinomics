import logging
import pickle

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from pylowiki.lib.base import BaseController, render
from pylowiki.lib.db.suggestion import getSuggestion
from pylowiki.lib.db.suggestion import getSuggestion
from pylowiki.lib.db.rating import Rating, changeRating, getRatingByID
from pylowiki.lib.db.workshop import getWorkshop
from pylowiki.lib.db.resource import getResource
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.comment import getComment

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
        s = getSuggestion(code, url)

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
        

    @h.login_required
    def rateFacilitation(self, id1, id2, id3):
        code = id1
        url = id2
        amount = int(id3)
        log.info('rateFacilitation %s %s %s' % (id1, id2, id3))
        rKey = 'ratedThings_workshop_overall'
        w = getWorkshop(code, url)

        found = False
        if rKey in c.authuser.keys():
            """
                Here we get a list of tuples.  Each tuple is of the form (a, b), with the following mapping:
                a         ->    rated Thing's ID  (What was rated) 
                b         ->    rating Thing's ID (The rating object)
            """
            l = pickle.loads(str(c.authuser[rKey]))
            for tup in l:
                if tup[0] == w.id:
                    found = True
                    changeRating(w, tup[1], amount)
            
        if not found:
            r = Rating(amount, w, c.authuser, 'overall')
        return "ok"
        
    @h.login_required
    def rateResource(self, id1, id2, id3):
        code = id1
        url = id2
        amount = int(id3)
        """
            voteType:   0    ->    down
                        1    ->    neutral
                        2    ->    up
        """
        voteType = 0
        if amount < 0:
            amount = -1
        elif amount > 0:
            voteType = 2
            amount = 1
        else:
            amount = 0
            voteType = 1
        
        rKey = 'ratedThings_article_overall'
        res = getResource(code, url)
        found = False
        if rKey in c.authuser.keys():
            """
                Here we get a list of tuples.  Each tuple is of the form (a, b), with the following mapping:
                a         ->    rated Thing's ID  (What was rated) 
                b         ->    rating Thing's ID (The rating object)
            """
            l = pickle.loads(str(c.authuser[rKey]))
            for tup in l:
                if tup[0] == res.id:
                    found = True
                    oldRating = int(getRatingByID(tup[1])['rating'])
                    if voteType == 0:
                        # user down voted
                        if oldRating == -1:
                            # User undoing old vote
                            res['downs'] = int(res['downs']) - 1
                            changeRating(res, tup[1], 0)
                        elif oldRating == 0:
                            # Change vote from neutral -> down
                            changeRating(res, tup[1], amount)
                            res['downs'] = int(res['downs']) + 1
                        elif oldRating == 1:
                            # Change vote from up -> down
                            changeRating(res, tup[1], amount)
                            res['ups'] = int(res['ups']) - 1
                            res['downs'] = int(res['downs']) + 1
                    elif voteType == 2:
                        # User up voted
                        if oldRating == -1:
                            # Change vote from down -> up
                            changeRating(res, tup[1], amount)
                            res['ups'] = int(res['ups']) + 1
                            res['downs'] = int(res['downs']) - 1
                        elif oldRating == 0:
                            # Change vote from neutral -> up
                            res['ups'] = int(res['ups']) + 1
                            changeRating(res, tup[1], amount)
                        elif oldRating == 1:
                            # User undoing old vote
                            res['ups'] = int(res['ups']) - 1
                            changeRating(res, tup[1], 0)
                        
        if not found:
            rating = Rating(amount, res, c.authuser, 'overall')
            if voteType == 0:
                res['downs'] = int(res['downs']) + 1
            elif voteType == 1:
                pass
                # Nothing to do here, we don't need to change the vote
            else:
                res['ups'] = int(res['ups']) + 1
        commit(res)
        return "OK"
    
    @h.login_required
    def rateComment(self, id1, id2):
        commentID = id1
        amount = int(id2)
        
        """
            voteType:   0    ->    down
                        1    ->    neutral
                        2    ->    up
        """
        voteType = 0
        if amount < 0:
            amount = -1
        elif amount > 0:
            voteType = 2
            amount = 1
        else:
            amount = 0
            voteType = 1
            
        if voteType == 1:
            return "OK"
        
        cKey = 'ratedThings_comment_overall'
        com = getComment(commentID)
        found = False
        if cKey in c.authuser.keys():
            """
                Here we get a list of tuples.  Each tuple is of the form (a, b), with the following mapping:
                a         ->    rated Thing's ID  (What was rated) 
                b         ->    rating Thing's ID (The rating object)
            """
            l = pickle.loads(str(c.authuser[cKey]))
            log.info('cKey found: %s' % l)
            for tup in l:
                if tup[0] == com.id:
                    found = True
                    oldRating = int(getRatingByID(tup[1])['rating'])
                    if voteType == 0:
                        # user down voted
                        if oldRating == -1:
                            # User undoing old vote
                            com['downs'] = int(com['downs']) - 1
                            changeRating(com, tup[1], 0)
                        elif oldRating == 0:
                            # Change vote from neutral -> down
                            changeRating(com, tup[1], amount)
                            com['downs'] = int(com['downs']) + 1
                        elif oldRating == 1:
                            # Change vote from up -> down
                            changeRating(com, tup[1], amount)
                            com['ups'] = int(com['ups']) - 1
                            com['downs'] = int(com['downs']) + 1
                    elif voteType == 2:
                        # User up voted
                        if oldRating == -1:
                            # Change vote from down -> up
                            changeRating(com, tup[1], amount)
                            com['ups'] = int(com['ups']) + 1
                            com['downs'] = int(com['downs']) - 1
                        elif oldRating == 0:
                            # Change vote from neutral -> up
                            com['ups'] = int(com['ups']) + 1
                            changeRating(com, tup[1], amount)
                        elif oldRating == 1:
                            # User undoing old vote
                            com['ups'] = int(com['ups']) - 1
                            changeRating(com, tup[1], 0)
        if not found:
            log.info('cKey not found')
            rating = Rating(amount, com, c.authuser, 'overall')
            if voteType == 0:
                com['downs'] = int(com['downs']) + 1
            elif voteType == 2:
                com['ups'] = int(com['ups']) + 1
        commit(com)
        return "OK"
