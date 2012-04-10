import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from pylowiki.lib.base import BaseController, render
from pylowiki.model import getIssueByID, getSuggestionByID, getRatingForSuggestion, get_user, Rating, Event, commit, getAvgRatingForSuggestion
from pylowiki.model import getComment, getRatingForComment, getAvgRatingForComment, getRatingForComment

import pylowiki.lib.helpers as h

import simplejson as json

log = logging.getLogger(__name__)

class RatingController(BaseController):

    def index(self):
        c.rating = '100'
        return render('/derived/rating.html')

    @h.login_required
    def rate(self):
        type = request.params['type']
        rating = request.params['rate']
        u = get_user(c.authuser.name)

        if type == "comment":
            commentID = request.params['commentID']
            
            comment = getComment(commentID)
            r = getRatingForComment(commentID, c.authuser.id)
            
            """ if a rating doesn't exist """
            if r == False:
                r = Rating('comment', rating)
                e = Event('rate_co', 'User rated a comment')
                u.ratings.append(r)
                u.events.append(e)
                comment.ratings.append(r)
                comment.events.append(e)
                e.rating = r
                
                if commit(e) and commit(r) and commit(comment):
                    log.info('User %s just rated comment id = %s as %s' %(c.authuser.name, commentID, rating))
                    comment.avgRating = getAvgRatingForComment(commentID)
                    if commit(comment):
                        log.info('average comment rating is now %s' %comment.avgRating)
                        return json.dumps({'avgRating':comment.avgRating})
            else:
                e = Event('rateCoCh', 'User changed a comment rating')
                r.rating = float(rating)
                u.events.append(e)
                comment.events.append(e)
                comment.avgRating = getAvgRatingForComment(commentID)
                e.rating = r
                try:
                    commit(e)
                    log.info('user %s changed rating of comment id = %s to %s' %(c.authuser.name, commentID, rating))
                    return json.dumps({'avgRating':comment.avgRating})
                except:
                    log.info('Error when user %s tried changing rating of comment id = %s to %s' %(c.authuser.name, commentID, rating))
                    return

        elif type == "suggestion":
            issueID = request.params['issueID']
            suggestionID = request.params['suggestionID']

            i = getIssueByID(issueID)
            if i == False:
                log.info('issue id %d does not exist!' % issueID)
                return

            s = getSuggestionByID(suggestionID)
            if s == False:
                log.info('suggestion id %d does not exist!' % suggestionID)
                return
            
            r = getRatingForSuggestion(suggestionID, c.authuser.id)
            
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
                    log.info('user %s changed rating in %s to %s' %(c.authuser.name, s.title, rating))
                    return json.dumps({'avgRating':s.avgRating})
                except:
                    log.info('error in commiting change to rating.  User: %s, rating: %s, suggestion: %s'%(c.authuser.name, rating, suggestionID))
                    return
