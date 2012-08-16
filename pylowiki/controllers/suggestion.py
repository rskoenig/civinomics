import logging, pickle

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from pylowiki.lib.db.event import Event, getParentEvents
from pylowiki.lib.db.workshop import getWorkshop, getWorkshopByID, isScoped
from pylowiki.lib.db.suggestion import Suggestion, getSuggestion, getSuggestionByID, getSuggestionsForWorkshop, getActiveSuggestionsForWorkshop
from pylowiki.lib.db.user import getUserByID, isAdmin
from pylowiki.lib.db.resource import getActiveResourcesByParentID
from pylowiki.lib.db.facilitator import isFacilitator
from pylowiki.lib.db.discussion import getDiscussionByID
from pylowiki.lib.db.revision import get_revision, Revision
from pylowiki.lib.db.page import Page, getPageByID, get_page
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.rating import getRatingByID
from pylowiki.lib.db.flag import Flag, isFlagged, checkFlagged, getFlags
from pylowiki.lib.db.revision import Revision

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
        # for comment disable
        if 'allowComments' not in c.s:
           c.s['allowComments'] = 1
        if c.s['disabled'] == '1' or c.s['allowComments'] == '0':
            c.commentsDisabled = 1
        else:
            c.commentsDisabled = 0
        c.events = getParentEvents(c.s)
        c.suggestions = getActiveSuggestionsForWorkshop(workshopCode, workshopURL)
        c.resources = getActiveResourcesByParentID(c.s.id)
        for i in range(len(c.suggestions)):
            suggestion = c.suggestions[i]
            if suggestion.id == c.s.id:
                c.suggestions.pop(i)
                break
        r = get_revision(int(c.s['mainRevision_id']))
        
        c.title = c.s['title']
        c.content = h.literal(h.reST2HTML(c.s['data']))
        ##c.content = h.lit_sub('<p>', h.literal('<p class = "clr suggestion_summary">'), c.content)
        
        # Note we can get original author and last revision author
        c.author = c.lastmoduser = getUserByID(r.owner)
        c.lastmoddate = r.date
        c.discussion = getDiscussionByID(c.s['discussion_id'])

        if 'user' in session:
            c.isAdmin = isAdmin(c.authuser.id)
            c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
            
            c.rating = False
            if 'ratedThings_suggestion_overall' in c.authuser.keys():
                """
                    Here we get a Dictionary with the commentID as the key and the ratingID as the value
                    Check to see if the commentID as a string is in the Dictionary keys
                    meaning it was already rated by this user
                """
                sugRateDict = pickle.loads(str(c.authuser['ratedThings_suggestion_overall']))
                if c.s.id in sugRateDict.keys():
                    c.rating = getRatingByID(sugRateDict[c.s.id])
                    
        return render('/derived/suggestion.bootstrap')

    @h.login_required
    def newSuggestion(self, id1, id2):
        code = id1
        url = id2

        c.w = getWorkshop(code, urlify(url))
        a = isAdmin(c.authuser.id)
        f =  isFacilitator(c.authuser, c.w)
        s = isScoped(c.authuser, c.w)
        if (s and c.w['allowSuggestions'] == '1') or a or f:
            c.s = False
            c.suggestions = getActiveSuggestionsForWorkshop(code, urlify(url))

            return render('/derived/suggestion_edit.bootstrap')
        else:
           h.flash('You are not authorized', 'error')
           return redirect('/workshop/%s/%s'%(c.w['urlCode'], urlify(c.w['url'])))

    @h.login_required
    def editSuggestion(self, id1, id2):
        code = id1
        url = id2

        c.s = getSuggestion(code, urlify(url))
        c.w = getWorkshop(c.s['workshopCode'], urlify(c.s['workshopURL']))
        a = isAdmin(c.authuser.id)
        f =  isFacilitator(c.authuser, c.w)
        if (c.authuser.id == c.s.owner) or a or f:
            return render('/derived/suggestion_edit.bootstrap')
        else:
           h.flash('You are not authorized', 'error')
           return redirect('/workshop/%s/%s/suggestion/%s/%s'%(c.w['urlCode'], urlify(c.w['url']), c.s['urlCode'], urlify(c.s['url'])))

    @h.login_required
    def saveSuggestion(self, id1, id2):
        code = id1
        url = id2
        
        if 'title' in request.params:
            title = request.params['title']
        else: 
            title = False
        if 'data' in request.params:
            data = request.params['data']
        else:
            data = False
        if 'allowComments' in request.params:
            allowComments = request.params['allowComments']
        else:
            allowComments = -1
        
        serror = 0
        serrorMsg = ''
        if not data or not title:
            serror = 1
            serrorMsg = 'Enter suggestion title and text.'

        if data == '' or title == '':
            serror = 1
            serrorMsg = 'Enter suggestion title and text.'

        if allowComments != '1' and allowComments != '0':
            serror = 1
            serrorMsg = 'Allow comments or not?'

        s = getSuggestion(code, urlify(url))
        w = getWorkshop(s['workshopCode'], urlify(s['workshopURL']))
        
        a = isAdmin(c.authuser.id)
        f =  isFacilitator(c.authuser.id, w.id)
        if c.authuser.id != s.owner and (a == False and f == False):
           serror = 1
           serrorMsg = 'You are not authorized'
        if serror:
           h.flash(serrorMsg, 'error')
        else:
           cMsg = 'Edited: '
           if s['title'] != title:
               cMsg = cMsg + 'Title updated. '
           s['title'] = title
           if s['data'] != data:
               cMsg = cMsg + 'Text updated. '
           s['data'] = data
           if s['allowComments'] != allowComments:
               if allowComments == '0':
                   cMsg = cMsg + 'Comments disabled. '
               else:
                   cMsg = cMsg + 'Comments enabled. '
           s['allowComments'] = allowComments
           r = Revision(c.authuser, data, s)
           s['mainRevision_id'] = r.r.id
           p = Page(title, c.authuser, s, data)
           commit(s)
           Event('Suggestion Edited', cMsg, s, c.authuser)
        
        return redirect('/workshop/%s/%s/suggestion/%s/%s'%(s['workshopCode'], urlify(s['workshopURL']), code, url))

    @h.login_required
    def addSuggestion(self, id1, id2):
        code = id1
        url = id2
        
        c.w = getWorkshop(code, urlify(url))
        if 'title' in request.params:
            title = request.params['title']
        else: 
            title = False
        if 'data' in request.params:
            data = request.params['data']
        else:
            data = False
        if 'allowComments' in request.params:
            allowComments = request.params['allowComments']
        else:
            allowComments = -1

        serror = 0
        serrorMsg = ''
        if not data or not title:
            serror = 1
            serrorMsg = 'Enter suggestion title and text.'
        if data == '' or title == '':
            serror = 1
            serrorMsg = 'Enter suggestion title and text.'
        a = isAdmin(c.authuser.id)
        f =  isFacilitator(c.authuser, c.w)
        s = isScoped(c.authuser, c.w)
        if (not s or c.w['allowSuggestions'] == '0') and not a and not f:
           serror = 1
           serrorMsg = 'You are not authorized.'
        if serror:
           h.flash(serrorMsg, 'error')
        else:
           s = Suggestion(c.authuser, title, data, allowComments, c.w)
        
        return redirect('/workshop/%s/%s'%(code, url))

    @h.login_required
    def modSuggestion(self, id1, id2):
        suggestionCode = id1
        suggestionURL = id2
        
        c.s = getSuggestion(suggestionCode, urlify(suggestionURL))
        c.w = getWorkshop(c.s['workshopCode'], urlify(c.s['workshopURL']))
        if not isAdmin(c.authuser.id) and not isFacilitator(c.authuser.id, c.w.id):
              h.flash('You are not authorized', 'error')
              return redirect('/workshop/%s/%s/suggestion/%s/%s'%(c.w['urlCode'], c.w['url'], c.s['urlCode'], c.s['url']))

        c.isAdmin = isAdmin(c.authuser.id)
        c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
        c.events = getParentEvents(c.s)
        r = get_revision(int(c.s['mainRevision_id']))
        
        c.title = c.s['title']
        c.content = h.literal(h.reST2HTML(c.s['data']))
        ##c.content = h.lit_sub('<p>', h.literal('<p class = "clr suggestion_summary">'), c.content)
        
        # Note we can get original author and last revision author
        c.author = c.lastmoduser = getUserByID(r.owner)
        c.lastmoddate = r.date
        c.discussion = getDiscussionByID(c.s['discussion_id'])

        c.flagged = False
        if checkFlagged(c.s):
           c.flagged = True
           c.flags = getFlags(c.s)

        return render('/derived/suggestion_admin.bootstrap')

    """ Takes in edits to the suggestion, saves new revision to the database. """
    @h.login_required
    def modSuggestionHandler(self):

        workshopCode = request.params['workshopCode']
        workshopURL = request.params['workshopURL']
        w = getWorkshop(workshopCode, workshopURL) 

        suggestionCode = request.params['suggestionCode']
        suggestionURL = request.params['suggestionURL']
        s = getSuggestion(suggestionCode, suggestionURL) 
        
        try:

           if not isAdmin(c.authuser.id) and not isFacilitator(c.authuser.id, w.id):
              h.flash('You are not authorized', 'error')
              return redirect('/workshop/%s/%s/suggestion/%s/%s'%(w['urlCode'], w['url'], s['urlCode'], s['url']))

           modType = request.params['modType']
           modSuggestionReason = request.params['modSuggestionReason']
           verifyModSuggestion = request.params['verifyModSuggestion']

        except:
           "h.flash('All fields required', 'error')"
           alert = {'type':'error'}
           alert['title'] = 'All Fields Required'
           alert['content'] = ''
           "alert['content'] = 'Please check all Required Fields'"
           session['alert'] = alert
           session.save()
           return redirect('/modSuggestion/%s/%s'%(s['urlCode'], s['url']))

        # disable or enable the suggestion, log the event
        if modType == 'disable':
            if s['disabled'] == '0':
               s['disabled'] = True
               modTitle = "Suggestion Disabled"
            else:
               s['disabled'] = False
               modTitle = "Suggestion Enabled"
        elif modType == 'delete':
            s['disabled'] = False
            s['deleted'] = True
            modTitle = "Suggestion Deleted"

        commit(s)
        if modSuggestionReason == "":
            modSuggestionReason = "No Reason Given"
        e = Event(modTitle, modSuggestionReason, s, c.authuser)

        h.flash(modTitle, 'success')
        return redirect('/workshop/%s/%s/suggestion/%s/%s'%(w['urlCode'], w['url'], s['urlCode'], s['url']))

    @h.login_required
    def adoptSuggestionHandler(self):
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


           adoptSuggestionReason = request.params['adoptSuggestionReason']
        except:
           h.flash('All fields required', 'error')
           return redirect('/workshop/%s/%s/suggestion/%s/%s/modSuggestion'%(w['urlCode'], w['url'], s['urlCode'], s['url']))

        if not 'adopted' in s or s['adopted'] == '0':
           s['adopted'] = True
           adoptTitle = "Suggestion Adopted"
        else:
           s['adopted'] = False
           adoptTitle = "Suggestion Unadopted"

        commit(s)
        e = Event(adoptTitle, adoptSuggestionReason, s, c.authuser)

        h.flash('Sugestion Adopted', 'success')
        return redirect('/workshop/%s/%s/suggestion/%s/%s'%(w['urlCode'], w['url'], s['urlCode'], s['url']))

    @h.login_required
    def noteSuggestionHandler(self):
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


           noteSuggestionText = request.params['noteSuggestionText']
        except:
           h.flash('All fields required', 'error')
           return redirect('/workshop/%s/%s/suggestion/%s/%s/modSuggestion'%(w['urlCode'], w['url'], s['urlCode'], s['url']))

        e = Event('Note Added', noteSuggestionText, s, c.authuser)

        h.flash('Note Saved', 'success')
        return redirect('/workshop/%s/%s/suggestion/%s/%s'%(w['urlCode'], w['url'], s['urlCode'], s['url']))

    @h.login_required
    def handler(self, id1, id2):
        suggestionCode = id1
        suggestionURL = id2
        
        s = getSuggestion(suggestionCode, urlify(suggestionURL))
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
    def flagSuggestion(self, id1, id2):
        code = id1
        url = id2
        suggestion = getSuggestion(code, urlify(url))
        if not suggestion:
            return json.dumps({'id':suggestion.id, 'result':'ERROR'})
        if not isFlagged(suggestion, c.authuser):
            f = Flag(suggestion, c.authuser)
            return json.dumps({'id':suggestion.id, 'result':"Successfully flagged!"})
        else:
            return json.dumps({'id':suggestion.id, 'result':"Already flagged!"})


