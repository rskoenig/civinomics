import logging
import pickle

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, redirect
from pylowiki.lib.utils import urlify

from pylowiki.lib.base import BaseController, render
from pylowiki.lib.db.suggestion import getSuggestion
from pylowiki.lib.db.suggestion import getSuggestion
from pylowiki.lib.db.rating import Rating, changeRating, getRatingByID
from pylowiki.lib.db.workshop import getWorkshop
from pylowiki.lib.db.resource import getResource
from pylowiki.lib.db.discussion import getDiscussion
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.comment import getComment, getCommentByCode

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
                Here we get a Dictionary with the commentID as the key and the ratingID as the value
                Check to see if the commentID as a string is in the Dictionary keys
                meaning it was already rated by this user
            """
            sugRateDict = pickle.loads(str(c.authuser[rKey]))
            if s.id in sugRateDict.keys():
                found = True
                changeRating(s, sugRateDict[s.id], amount)
            
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
                Here we get a Dictionary with the commentID as the key and the ratingID as the value
                Check to see if the commentID as a string is in the Dictionary keys
                meaning it was already rated by this user
            """
            facRateDict = pickle.loads(str(c.authuser[rKey]))
            if w.id in facRateDict.keys():
                found = True
                changeRating(w, facRateDict[w.id], amount)
            
        if not found:
            r = Rating(amount, w, c.authuser, 'overall')
        return "ok"

    @h.login_required
    def rateDiscussion(self, id1, id2, id3):
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
        
        dKey = 'ratedThings_discussion_overall'
        dis = getDiscussion(code, urlify(url))
        found = False
        if dKey in c.authuser.keys():
            """
                Here we get a Dictionary with the commentID as the key and the ratingID as the value
                Check to see if the commentID as a string is in the Dictionary keys
                meaning it was already rated by this user
            """
            disRateDict = pickle.loads(str(c.authuser[dKey]))
            if dis.id in disRateDict.keys():
                found = True
                oldRating = int(getRatingByID(disRateDict[dis.id])['rating'])
                if voteType == 0:
                    # user down voted
                    if oldRating == -1:
                        # User undoing old vote
                        dis['downs'] = int(dis['downs']) - 1
                        changeRating(dis, disRateDict[dis.id], 0)
                    elif oldRating == 0:
                        # Change vote from neutral -> down
                        changeRating(dis, disRateDict[dis.id], amount)
                        dis['downs'] = int(dis['downs']) + 1
                    elif oldRating == 1:
                        # Change vote from up -> down
                        changeRating(dis, disRateDict[dis.id], amount)
                        dis['ups'] = int(dis['ups']) - 1
                        dis['downs'] = int(dis['downs']) + 1
                elif voteType == 2:
                    # User up voted
                    if oldRating == -1:
                        # Change vote from down -> up
                        changeRating(dis, disRateDict[dis.id], amount)
                        dis['ups'] = int(dis['ups']) + 1
                        dis['downs'] = int(dis['downs']) - 1
                    elif oldRating == 0:
                        # Change vote from neutral -> up
                        dis['ups'] = int(dis['ups']) + 1
                        changeRating(dis, disRateDict[dis.id], amount)
                    elif oldRating == 1:
                        # User undoing old vote
                        dis['ups'] = int(dis['ups']) - 1
                        changeRating(dis, disRateDict[dis.id], 0)
                    
        if not found:
            rating = Rating(amount, dis, c.authuser, 'overall')
            if voteType == 0:
                dis['downs'] = int(dis['downs']) + 1
            elif voteType == 1:
                pass
                # Nothing to do here, we don't need to change the vote
            else:
                dis['ups'] = int(dis['ups']) + 1
        commit(dis)
        return redirect(session['return_to'])
            
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
        
        rKey = 'ratedThings_resource_overall'
        res = getResource(code, url)
        found = False
        if rKey in c.authuser.keys():
            """
                Here we get a Dictionary with the commentID as the key and the ratingID as the value
                Check to see if the commentID as a string is in the Dictionary keys
                meaning it was already rated by this user
            """
            resRateDict = pickle.loads(str(c.authuser[rKey]))
            if res.id in resRateDict.keys():
                found = True
                oldRating = int(getRatingByID(resRateDict[res.id])['rating'])
                if voteType == 0:
                    # user down voted
                    if oldRating == -1:
                        # User undoing old vote
                        res['downs'] = int(res['downs']) - 1
                        changeRating(res, resRateDict[res.id], 0)
                    elif oldRating == 0:
                        # Change vote from neutral -> down
                        changeRating(res, resRateDict[res.id], amount)
                        res['downs'] = int(res['downs']) + 1
                    elif oldRating == 1:
                        # Change vote from up -> down
                        changeRating(res, resRateDict[res.id], amount)
                        res['ups'] = int(res['ups']) - 1
                        res['downs'] = int(res['downs']) + 1
                elif voteType == 2:
                    # User up voted
                    if oldRating == -1:
                        # Change vote from down -> up
                        changeRating(res, resRateDict[res.id], amount)
                        res['ups'] = int(res['ups']) + 1
                        res['downs'] = int(res['downs']) - 1
                    elif oldRating == 0:
                        # Change vote from neutral -> up
                        res['ups'] = int(res['ups']) + 1
                        changeRating(res, resRateDict[res.id], amount)
                    elif oldRating == 1:
                        # User undoing old vote
                        res['ups'] = int(res['ups']) - 1
                        changeRating(res, resRateDict[res.id], 0)
                    
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
        return redirect(session['return_to'])
    
    @h.login_required
    def rateComment(self, id1, id2):
        commentCode = id1
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
        com = getCommentByCode(commentCode)
        found = False
        if cKey in c.authuser.keys():
            """
                Here we get a Dictionary with the commentID as the key and the ratingID as the value
                Check to see if the commentID as a string is in the Dictionary keys
                meaning it was already rated by this user
            """
            comRateDict = pickle.loads(str(c.authuser[cKey]))
            log.info('cKey found: %s' % comRateDict)
            if com.id in comRateDict.keys():
                found = True
                oldRating = int(getRatingByID(comRateDict[com.id])['rating'])
                if voteType == 0:
                    # user down voted
                    if oldRating == -1:
                        # User undoing old vote
                        com['downs'] = int(com['downs']) - 1
                        changeRating(com, comRateDict[com.id], 0)
                    elif oldRating == 0:
                        # Change vote from neutral -> down
                        changeRating(com, comRateDict[com.id], amount)
                        com['downs'] = int(com['downs']) + 1
                    elif oldRating == 1:
                        # Change vote from up -> down
                        changeRating(com,comRateDict[com.id], amount)
                        com['ups'] = int(com['ups']) - 1
                        com['downs'] = int(com['downs']) + 1
                elif voteType == 2:
                    # User up voted
                    if oldRating == -1:
                        # Change vote from down -> up
                        changeRating(com, comRateDict[com.id], amount)
                        com['ups'] = int(com['ups']) + 1
                        com['downs'] = int(com['downs']) - 1
                    elif oldRating == 0:
                        # Change vote from neutral -> up
                        com['ups'] = int(com['ups']) + 1
                        changeRating(com, comRateDict[com.id], amount)
                    elif oldRating == 1:
                        # User undoing old vote
                        com['ups'] = int(com['ups']) - 1
                        changeRating(com, comRateDict[com.id], 0)
        if not found:
            log.info('cKey not found')
            rating = Rating(amount, com, c.authuser, 'overall')
            if voteType == 0:
                com['downs'] = int(com['downs']) + 1
            elif voteType == 2:
                com['ups'] = int(com['ups']) + 1
        commit(com)
        return redirect(session['return_to'])
