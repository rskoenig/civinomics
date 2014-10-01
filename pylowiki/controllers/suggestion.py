import logging, pickle

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from pylowiki.lib.db.event import Event, getParentEvents
from pylowiki.lib.db.workshop import getWorkshop, getWorkshopByCode, getWorkshopByID, isScoped
from pylowiki.lib.db.suggestion import Suggestion, getSuggestion, getSuggestionByID, getSuggestionsForWorkshop, getActiveSuggestionsForWorkshop
from pylowiki.lib.db.user import getUserByID, isAdmin
from pylowiki.lib.db.resource import getActiveResourcesByParentID
from pylowiki.lib.db.facilitator import isFacilitator
from pylowiki.lib.db.discussion import getDiscussionByID
from pylowiki.lib.db.revision import get_revision, Revision, getParentRevisions, getRevisionByCode
from pylowiki.lib.db.page import Page, getPageByID, get_page
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.rating import getRatingByID
from pylowiki.lib.db.flag import Flag, isFlagged, checkFlagged, getFlags, clearFlags
from pylowiki.lib.db.revision import Revision

from pylowiki.lib.base import BaseController, render
from pylowiki.lib.fuzzyTime import timeSince
from pylowiki.lib.utils import urlify

import pylowiki.lib.helpers as h
import simplejson as json

log = logging.getLogger(__name__)

class SuggestionController(BaseController):

    def index(self, id1, id2, id3, id4, id5 = ''):
        workshopCode = id1
        workshopURL = id2
        suggestionCode = id3
        suggestionURL = id4
        revisionURL = id5
        
        c.w = getWorkshop(workshopCode, urlify(workshopURL))
        if c.w['public_private'] != 'public':
            if 'user' not in session or not isScoped(c.authuser, c.w):
                    return render('/derived/404.bootstrap')
                    
        c.s = getSuggestion(suggestionCode, urlify(suggestionURL))
        # for comment disable
        if 'allowComments' not in c.s:
           c.s['allowComments'] = '1'
        if c.s['disabled'] == '1' or c.s['allowComments'] == '0':
            c.commentsDisabled = 1
        else:
            c.commentsDisabled = 0
        c.events = getParentEvents(c.s)
        c.suggestions = getActiveSuggestionsForWorkshop(workshopCode)
        c.resources = getActiveResourcesByParentID(c.s.id)
        for i in range(len(c.suggestions)):
            suggestion = c.suggestions[i]
            if suggestion.id == c.s.id:
                c.suggestions.pop(i)
                break

        c.title = c.s['title']

        if revisionURL != '':
            c.revision = getRevisionByCode(revisionURL)
            c.content = h.literal(h.reST2HTML(c.revision['data']))
            c.lastmoduser = getUserByID(c.revision.owner)
            c.lastmoddate = c.revision.date
            r = c.revision
        else:
            c.content = h.literal(h.reST2HTML(c.s['data']))
            c.lastmoduser = getUserByID(c.s.owner)
            if 'mainRevision_id' in c.s:
                r = get_revision(int(c.s['mainRevision_id']))
                c.lastmoddate = r.date
            else:
                c.lastmoddate = c.s.date

        c.revisions = getParentRevisions(c.s.id)
        
        # Note we can get original author and last revision author
        c.author = c.lastmoduser = getUserByID(r.owner)
        c.discussion = getDiscussionByID(c.s['discussion_id'])

        if 'user' in session:
            c.isAdmin = isAdmin(c.authuser.id)
            c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
            c.isScoped = isScoped(c.authuser, c.w)
            c.allowComments = c.s['allowComments']
            
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
        else:
            c.isAdmin = False
            c.isFacilitator = False
            c.isScoped = False
            c.allowComments = False
            
        return render('/derived/suggestion.bootstrap')

    @h.login_required
    def newSuggestion(self, id1, id2):
        code = id1
        url = id2

        c.w = getWorkshop(code, urlify(url))
        a = isAdmin(c.authuser.id)
        f =  isFacilitator(c.authuser.id, c.w.id)
        s = isScoped(c.authuser, c.w)
        if (s and c.w['allowSuggestions'] == '1') or a or f:
            c.s = False
            c.suggestions = getActiveSuggestionsForWorkshop(code)

            return render('/derived/suggestion_edit.bootstrap')
        else:
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
        if not title or title == '':
            serror = 1
            serrorMsg = serrorMsg + 'Sugestion title required.'

        if not data or data == '':
            serror = 1
            serrorMsg = serrorMsg + 'Sugestion description required.'

        if allowComments != '1' and allowComments != '0':
            serror = 1
            serrorMsg = 'Allow comments or not?'

        s = getSuggestion(code, urlify(url))
        w = getWorkshopByCode(s['workshopCode'])
        
        a = isAdmin(c.authuser.id)
        f =  isFacilitator(c.authuser.id, w.id)
        if c.authuser.id != s.owner and (a == False and f == False):
           return redirect('/workshop/%s/%s'%(w['urlCode'], w['url']))
        if serror:
           alert = {'type':'error'}
           alert['title'] = "Error."
           alert['content'] = serrorMsg
           session['alert'] = alert
           session.save()
           return redirect('/editSuggestion/%s/%s'%(code, url))
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
           alert = {'type':'success'}
           alert['title'] = 'Suggestion edited.'
           alert['content'] = 'Suggestion updated, thanks!'
           session['alert'] = alert
           session.save()

        
        return redirect('/workshop/%s/%s/suggestion/%s/%s'%(w['urlCode'], urlify(w['url']), code, url))

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
            log.info(serrorMsg)
        if data == '' or title == '':
            serror = 1
            serrorMsg = 'Enter suggestion title and text.'
            log.info(serrorMsg)

        a = isAdmin(c.authuser.id)
        f =  isFacilitator(c.authuser.id, c.w.id)
        s = isScoped(c.authuser, c.w)

        if (not s or c.w['allowSuggestions'] == '0') and not a and not f:
           return redirect('/workshop/%s/%s'%(c.w['urlCode'], c.w['url']))

        if serror:
            alert = {'type':'error'}
            alert['title'] = "Error."
            alert['content'] = serrorMsg
            session['alert'] = alert
            session.save()
            c.s = False
            c.suggestionTitle = title
            c.suggestionData = data
            c.suggestionAllowComments = allowComments
            c.suggestions = getActiveSuggestionsForWorkshop(code)
            return render('/derived/suggestion_edit.bootstrap')

        else:
            alert = {'type':'success'}
            alert['title'] = 'Suggestion added.'
            alert['content'] = 'Thanks for the suggestion!'
            session['alert'] = alert
            session.save()
            s = Suggestion(c.authuser, title, data, allowComments, c.w)
            return redirect('/workshop/%s/%s'%(code, url))
        

    @h.login_required
    def modSuggestion(self, id1, id2):
        suggestionCode = id1
        suggestionURL = id2
        
        c.s = getSuggestion(suggestionCode, urlify(suggestionURL))
        c.w = getWorkshop(c.s['workshopCode'], urlify(c.s['workshopURL']))
        if not isAdmin(c.authuser.id) and not isFacilitator(c.authuser.id, c.w.id):
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
    def clearSuggestionFlagsHandler(self, id1, id2):
        code = id1
        url = id2

        c.s = getSuggestion(code, urlify(url))
        c.author = getUserByID(c.s.owner)
        c.w = getWorkshop(c.s['workshopCode'], c.s['workshopURL'])
        if not isAdmin(c.authuser.id) and not isFacilitator(c.authuser.id, c.w.id):
              return redirect('/workshop/%s/%s/suggestion/%s/%s'%(c.w['urlCode'], c.w['url'], c.s['urlCode'], c.s['url']))

        clearError = 0
        clearMessage = ""

        if 'clearSuggestionFlagsReason' in request.params:
            clearReason = request.params['clearSuggestionFlagsReason']
            if clearReason != '':
                clearFlags(c.s)
                clearTitle = "Flags cleared"
                e = Event(clearTitle, clearReason, c.s, c.authuser)
            else:
                clearError = 1
                clearMessage = "Please include a reason for your action"
        else:
            clearError = 1
            clearMessage = "Please include a reason for your action"

        if clearError:
            alert = {'type':'error'}
            alert['title'] = "Flags not cleared"
            alert['content'] = clearMessage
            session['alert'] = alert
            session.save()
        else:
            clearMessage = "Flags cleared from this suggestion"
            alert = {'type':'success'}
            alert['title'] = 'Flags cleared!'
            alert['content'] = clearMessage
            session['alert'] = alert
            session.save()

        returnURL = "/modSuggestion/" + c.s['urlCode'] + "/" + c.s['url']
        return redirect(returnURL)

        
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
               s['disabled'] = '1'
               modTitle = "Suggestion Disabled"
            else:
               s['disabled'] = '0'
               modTitle = "Suggestion Enabled"
        elif modType == 'delete':
            s['disabled'] = '0'
            s['deleted'] = '1'
            modTitle = "Suggestion Deleted"

        commit(s)
        if modSuggestionReason == "":
            modSuggestionReason = "No Reason Given"
        e = Event(modTitle, modSuggestionReason, s, c.authuser)

        h.flash(modTitle, 'success')

        if modType == 'delete':
            return redirect('/workshop/%s/%s/' %(w['urlCode'], w['url']))
        else:
            return redirect('/workshop/%s/%s/suggestion/%s/%s' %(w['urlCode'], w['url'], s['urlCode'], s['url']))


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
              return redirect('/workshop/%s/%s/suggestion/%s/%s'%(w['urlCode'], w['url'], s['urlCode'], s['url']))


           adoptSuggestionReason = request.params['adoptSuggestionReason']
        except:
           h.flash('All fields required', 'error')
           return redirect('/workshop/%s/%s/suggestion/%s/%s/modSuggestion'%(w['urlCode'], w['url'], s['urlCode'], s['url']))

        if not 'adopted' in s or s['adopted'] == '0':
           s['adopted'] = '1'
           adoptTitle = "Suggestion Adopted"
        else:
           s['adopted'] = '0'
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
              return redirect('/workshop/%s/%s/suggestion/%s/%s'%(w['urlCode'], w['url'], s['urlCode'], s['url']))


           noteSuggestionText = request.params['noteSuggestionText']
        except:
           h.flash('All fields required', 'error')
           return redirect('/workshop/%s/%s/suggestion/%s/%s/modSuggestion'%(w['urlCode'], w['url'], s['urlCode'], s['url']))

        e = Event('Note Added', noteSuggestionText, s, c.authuser)

        h.flash('Note Saved', 'success')
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


