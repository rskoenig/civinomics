import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
#from pylowiki.model import get_page, getSuggestion, getIssueByID, getUserByID, Rating, Event, getSuggestionByID, getSuggestionByURL
#from pylowiki.model import get_user, commit, get_page, getIssueByID, getAvgRatingForSuggestion, getRatingForSuggestion
#from pylowiki.model import getRatingForComment, Revision

from pylowiki.lib.db.workshop import getWorkshop, getWorkshopByID
from pylowiki.lib.db.suggestion import Suggestion, getSuggestion, getSuggestionByID
from pylowiki.lib.db.user import getUserByID
from pylowiki.lib.db.discussion import getDiscussionByID
from pylowiki.lib.db.revision import get_revision, Revision
from pylowiki.lib.db.page import getPageByID
from pylowiki.lib.db.dbHelpers import commit

from pylowiki.lib.base import BaseController, render
from pylowiki.lib.fuzzyTime import timeSince
from pylowiki.lib.utils import urlify

import simplejson as json

import pylowiki.lib.helpers as h

log = logging.getLogger(__name__)

class SuggestionController(BaseController):

    def index(self, id1, id2, id3, id4):
        workshopCode = id1
        workshopURL = id2
        suggestionCode = id3
        suggestionURL = id4
        
        c.w = getWorkshop(workshopCode, urlify(workshopURL))
        c.s = getSuggestion(suggestionCode, urlify(suggestionURL))
        r = get_revision(int(c.s['mainRevision_id']))
        
        c.title = c.s['title']
        c.content = h.literal(h.reST2HTML(c.s['data']))
        c.content = h.lit_sub('<p>', h.literal('<p class = "clr suggestion_summary">'), c.content)
        
        #c.author = getUserByID(c.s.owner)
        # Note we can get original author and last revision author
        c.author = c.lastmoduser = getUserByID(r.owner)
        c.lastmoddate = r.date
        c.discussion = getDiscussionByID(c.s['discussion_id'])
        
        return render('/derived/suggestion.html')

    def addSuggestion(self, id1, id2):
        code = id1
        url = id2
        
        title = request.params['title']
        data = request.params['data']
        
        w = getWorkshop(code, urlify(url))
        s = Suggestion(c.authuser, title, data, w)
        
        if 'suggestionList' not in w.keys():
            w['suggestionList'] = s.s.id
        else:
            w['suggestionList'] = w['suggestionList'] + ',' + str(s.s.id)
        
        return redirect('/workshops/%s/%s'%(code, url))
        
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

    """ Takes in edits to the suggestion, saves new revision to the database. """
    @h.login_required
    def handler(self, id):
        l = id.split('_')
        workshop_id = l[0]
        suggestion_id = l[1]
        s = getSuggestionByID(suggestion_id)
        w = getWorkshopByID(workshop_id)
        p = getPageByID(s['page_id'])
        
        # Does the user have an access level of at least 200?
        # Alternately, is the user marked as an owner of the suggestion and/or issue?
        if (c.authuser['accessLevel'] < 200) or (int(c.authuser.id) != int(s.owner)):
            h.flash('You are not authorized to view this page', 'error')
            return redirect('/')
        
        data = request.params['textarea0']
        
        r = Revision(c.authuser, data, p)
        s['mainRevision_id'] = r.r.id
        s['data'] = data
        commit(s)
        #e = Event('edtSug', 'User %s edited suggestion %s' %(c.authuser.id, suggestion_id))
        
        """
        r.event = e
        c.authuser.events.append(e)
        s.events.append(e)
        s.revisions.append(r)

        if not commit(e):
            h.flash('Error: edit was not saved!', 'error')
        else:
            h.flash('Edit successfully commited!', 'success')
        return redirect('/issue/%s/suggestion/%s' %(i.page.url, s.url))
        """
        return redirect('/workshop/%s/%s/suggestion/%s/%s'%(w['urlCode'], w['url'], s['urlCode'], s['url']))