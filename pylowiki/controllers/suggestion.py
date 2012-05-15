import logging, pickle

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from pylowiki.lib.db.event import Event, getParentEvents
from pylowiki.lib.db.workshop import getWorkshop, getWorkshopByID
from pylowiki.lib.db.suggestion import Suggestion, getSuggestion, getSuggestionByID, getSuggestionsForWorkshop
from pylowiki.lib.db.user import getUserByID, isAdmin
from pylowiki.lib.db.facilitator import isFacilitator
from pylowiki.lib.db.discussion import getDiscussionByID
from pylowiki.lib.db.revision import get_revision, Revision
from pylowiki.lib.db.page import getPageByID
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.rating import getRatingByID
from pylowiki.lib.db.flag import Flag, isFlagged, checkFlagged, getFlags

from pylowiki.lib.base import BaseController, render
from pylowiki.lib.fuzzyTime import timeSince
from pylowiki.lib.utils import urlify

import pylowiki.lib.helpers as h
import simplejson as json

log = logging.getLogger(__name__)

class SuggestionController(BaseController):

    def index(self, id1, id2, id3, id4):
        workshopCode = id1
        workshopURL = id2
        suggestionCode = id3
        suggestionURL = id4
        
        c.w = getWorkshop(workshopCode, urlify(workshopURL))
        c.s = getSuggestion(suggestionCode, urlify(suggestionURL))
        c.suggestions = getSuggestionsForWorkshop(workshopCode, urlify(workshopURL))
        for i in range(len(c.suggestions)):
            suggestion = c.suggestions[i]
            if suggestion.id == c.s.id:
                c.suggestions.pop(i)
                break
        r = get_revision(int(c.s['mainRevision_id']))
        
        c.title = c.s['title']
        c.content = h.literal(h.reST2HTML(c.s['data']))
        c.content = h.lit_sub('<p>', h.literal('<p class = "clr suggestion_summary">'), c.content)
        
        # Note we can get original author and last revision author
        c.author = c.lastmoduser = getUserByID(r.owner)
        c.lastmoddate = r.date
        c.discussion = getDiscussionByID(c.s['discussion_id'])

        c.flagged = False
        if checkFlagged(c.s):
           c.flagged = True
           c.flags = getFlags(c.s)

        if 'user' in session:
            c.isAdmin = isAdmin(c.authuser.id)
            c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
            
            c.rating = False
            if 'ratedThings_suggestion_overall' in c.authuser.keys():
                """
                    Here we get a list of tuples.  Each tuple is of the form (a, b), with the following mapping:
                    a         ->    rated Thing's ID  (What was rated) 
                    b         ->    rating Thing's ID (The rating object)
                """
                l = pickle.loads(str(c.authuser['ratedThings_suggestion_overall']))
                for tup in l:
                    if tup[0] == c.s.id:
                        c.rating = getRatingByID(tup[1])
                    
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

    def modSuggestion(self, id1, id2, id3, id4):
        workshopCode = id1
        workshopURL = id2
        suggestionCode = id3
        suggestionURL = id4
        
        c.w = getWorkshop(workshopCode, urlify(workshopURL))
        c.isAdmin = isAdmin(c.authuser.id)
        c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
        c.s = getSuggestion(suggestionCode, urlify(suggestionURL))
        c.events = getParentEvents(c.s)
        r = get_revision(int(c.s['mainRevision_id']))
        
        c.title = c.s['title']
        c.content = h.literal(h.reST2HTML(c.s['data']))
        c.content = h.lit_sub('<p>', h.literal('<p class = "clr suggestion_summary">'), c.content)
        
        # Note we can get original author and last revision author
        c.author = c.lastmoduser = getUserByID(r.owner)
        c.lastmoddate = r.date
        c.discussion = getDiscussionByID(c.s['discussion_id'])

        c.flagged = False
        if checkFlagged(c.s):
           c.flagged = True
           c.flags = getFlags(c.s)

        
        return render('/derived/suggestion_admin.html')

    """ Takes in edits to the suggestion, saves new revision to the database. """
    @h.login_required
    def modSuggestionHandler(self):
        try:
           w = False
           s = False
           workshopCode = request.params['workshopCode']
           workshopURL = request.params['workshopURL']
           w = getWorkshop(workshopCode, workshopURL) 

           suggestionCode = request.params['suggestionCode']
           suggestionURL = request.params['suggestionURL']
           s = getSuggestion(suggestionCode, suggestionURL) 

           if not isAdmin(c.authuser.id) and not isFacilitator(c.authuser.id, w.id):
              h.flash('You are not authorized', 'error')
              return redirect('/workshop/%s/%s/suggestion/%s/%s'%(w['urlCode'], w['url'], s['urlCode'], s['url']))


           modSuggestionReason = request.params['modSuggestionReason']
           verifyModSuggestion = request.params['verifyModSuggestion']
        except:
           h.flash('All fields required', 'error')
           return redirect('/workshop/%s/%s/suggestion/%s/%s/modSuggestion'%(w['urlCode'], w['url'], s['urlCode'], s['url']))

        # disable or enable the suggestion, log the event
        if s['disabled'] == '0':
           s['disabled'] = True
           modTitle = "Suggestion Disabled"
        else:
           s['disabled'] = False
           modTitle = "Suggestion Enabled"

        commit(s)
        e = Event(modTitle, modSuggestionReason, s, c.authuser)

        h.flash(modTitle, 'success')
        return redirect('/workshop/%s/%s/suggestion/%s/%s'%(w['urlCode'], w['url'], s['urlCode'], s['url']))

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
        if (int(c.authuser['accessLevel']) < 200) or (int(c.authuser.id) != int(s.owner)):
            h.flash('You are not authorized to view this page', 'error')
            return redirect('/')
        
        data = request.params['textarea0']
        
        r = Revision(c.authuser, data, p)
        s['mainRevision_id'] = r.r.id
        s['data'] = data
        commit(s)
        
        return redirect('/workshop/%s/%s/suggestion/%s/%s'%(w['urlCode'], w['url'], s['urlCode'], s['url']))

    @h.login_required
    def flagSuggestion(self, id1):
        suggestionID = id1
        suggestion = getSuggestionByID(suggestionID)
        if not suggestion:
            return json.dumps({'id':suggestionID, 'result':'ERROR'})
        if not isFlagged(suggestion, c.authuser):
            f = Flag(suggestion, c.authuser)
            return json.dumps({'id':suggestionID, 'result':"Successfully flagged!"})
        else:
            return json.dumps({'id':suggestionID, 'result':"Already flagged!"})


