import logging
import pickle

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, redirect
from pylowiki.lib.utils import urlify

from pylowiki.lib.base import BaseController, render
import pylowiki.lib.db.suggestion   as suggestionLib
import pylowiki.lib.db.rating       as ratingLib
import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.resource     as resourceLib
import pylowiki.lib.db.idea         as ideaLib
import pylowiki.lib.db.photo        as photoLib
import pylowiki.lib.db.initiative   as initiativeLib
import pylowiki.lib.db.discussion   as discussionLib
import pylowiki.lib.db.meeting      as meetingLib
import pylowiki.lib.db.ballot       as ballotLib
import pylowiki.lib.db.comment      as commentLib
import pylowiki.lib.db.generic      as genericLib
import pylowiki.lib.utils           as utils

import pylowiki.lib.helpers as h
import simplejson as json

log = logging.getLogger(__name__)

class RatingController(BaseController):

    def __before__(self, action, code = None, amount = None):
        if code is None:
            return
        if amount is None:
            return
        log.info(code)
        amount = int(amount)
        if amount < 0:
            amount = -1
        elif amount > 0:
            amount = 1
        else:
            amount = 0
        ratingType = 'binary'

        if action == 'rateDiscussion':
            thing = discussionLib.getDiscussion(code)
        elif action == 'rateResource':
            thing = resourceLib.getResourceByCode(code)
        elif action == 'rateComment':
            thing = commentLib.getCommentByCode(code)
        elif action == 'rateIdea':
            thing = ideaLib.getIdea(code)
        elif action == 'ratePhoto':
            thing = photoLib.getPhoto(code)
        elif action == 'rateInitiative':
            thing = initiativeLib.getInitiative(code)
        elif action == 'rateAgendaItem':
            thing = meetingLib.getAgendaItem(code)
        elif action == 'rateBallotMeasure':
            thing = ballotLib.getBallotMeasure(code)
        elif action == 'rateBallotCandidate':
            thing = ballotLib.getBallotCandidate(code)
        
        if thing['disabled'] == '1':
            # Should only get triggered when the user posts directly and bypasses the UI
            return False
        
        ratingObj = ratingLib.makeOrChangeRating(thing, c.authuser, amount, ratingType)

    def index(self):
        # Dummy controller, prevents error logs, shows nothing of importance
        return 'hi'

    #
    # Preferred behaviour:  One rating object per thing being rated, keyed by that thing's urlCode.
    #                       One rating function inside lib/db/rating - makeOrChangeRating(thing, amount)
    #                       The rating object tells us what the user's rating is.  The 'makeOrChangeRating' 
    #                       function updates the 'ups' and 'downs' field of the thing that was rated.
    #

    @h.login_required
    def rateDiscussion(self, code, url, amount):
        return redirect(session['return_to'])
    
    @h.login_required
    def rateResource(self, code, url, amount):        
        return redirect(session['return_to'])
    
    @h.login_required
    def rateComment(self, code, amount):
        return redirect(session['return_to'])

    @h.login_required
    def rateIdea(self, code, amount):
        # check to see if this is a request from the iphone app
        iPhoneApp = utils.iPhoneRequestTest(request)
        if iPhoneApp:
            entry = {}
            entry['voted'] = amount
            result = []
            result.append(entry)
            statusCode = 0
            response.headers['Content-type'] = 'application/json'
            return json.dumps({'statusCode':statusCode, 'result':result})
        else:
            return redirect(session['return_to'])
        
    @h.login_required
    def ratePhoto(self, code, amount):
        return redirect(session['return_to'])
        
    @h.login_required
    def rateInitiative(self, code, amount):
        return redirect(session['return_to'])
        
    @h.login_required

    def rateUser(self, code, amount):
        return redirect(session['return_to'])

    def rateAgendaItem(self, code, amount):
        return redirect(session['return_to'])
        
    @h.login_required
    def rateBallotMeasure(self, code, amount):
        return redirect(session['return_to'])
        
    @h.login_required
    def rateBallotCandidate(self, code, amount):
        return redirect(session['return_to'])
        
    ########################################################################
    # 
    # Everything below is unused right now, almost certainly broken
    # 
    ########################################################################
    @h.login_required
    def rateSuggestion(self, code, url, amount):
        rKey = 'ratedThings_suggestion_overall'
        s = suggestionLib.getSuggestion(code, url)

        found = False
        if rKey in c.authuser.keys():
            """
                Here we get a Dictionary with the commentID as the key and the ratingID as the value
                Check to see if the commentID as a string is in the Dictionary keys
                meaning it was already rated by this user
            """
            sugRateDict = pickle.loads(str(c.authuser[rKey]))
            if s.id in sugRateDict.keys():
                found = True
                ratingLib.changeRating(s, sugRateDict[s.id], amount)
            
        if not found:
            r = ratingLib.Rating(amount, s, c.authuser, 'overall')
        return "ok"
        

    @h.login_required
    def rateFacilitation(self, code, url, amount):
        rKey = 'ratedThings_workshop_overall'
        w = workshopLib.getWorkshop(code, url)

        found = False
        if rKey in c.authuser.keys():
            """
                Here we get a Dictionary with the commentID as the key and the ratingID as the value
                Check to see if the commentID as a string is in the Dictionary keys
                meaning it was already rated by this user
            """
            facRateDict = pickle.loads(str(c.authuser[rKey]))
            if w.id in facRateDict.keys():
                found = True
                ratingLib.changeRating(w, facRateDict[w.id], amount)
            
        if not found:
            r = ratingLib.Rating(amount, w, c.authuser, 'overall')
        return "ok"
        