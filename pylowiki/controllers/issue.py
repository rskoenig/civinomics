import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import config
from pylowiki.lib.base import BaseController, render
from pylowiki.model import get_page, get_all_pages, getSlideshow, getIssueByName, getSphere, getPageByID, getUserByID
from pylowiki.model import getParticipantsByID, getArticlesByIssueID, getRatingForSuggestion
from pylowiki.lib.points import readThisPage

import pylowiki.lib.helpers as h
import re
from operator import itemgetter

log = logging.getLogger(__name__)

class IssueController(BaseController):

    def home(self, id):
        c.p = get_page(id)
        if c.p == False:
            abort(404, h.literal("That page does not exist!"))

        c.title = c.p.title.decode('latin-1')
        c.url = c.p.url.decode('latin-1')
        
        r = c.p.revisions[0]

        c.lastmoddate = r.event.date
        c.lastmoduser = r.event.user.name
        s = getSlideshow(c.p.id)
        c.slideshow = []
        c.slideshowDirectory = 'slideshows'
        for item in s:
            entry = {}
            entry['hash'] = item.pictureHash
            entry['caption'] = item.caption
            entry['title'] = item.title
            c.slideshow.append(entry)

        i = getIssueByName(c.p.title)
        c.issue = i
        c.issueID = i.id
        c.goals = h.literal(h.reST2HTML(i.goals))
        sphere = getSphere(i.govtSphere)
        if sphere:
            c.govtSphere = {'name': sphere.name, 'image': sphere.pictureHash}
        else:
            c.govtSphere = {'name': 'No sphere!', 'image': 'sphere'}
        suggestions = i.suggestions
        c.suggestions = []

        for item in suggestions:
            if not item.pending and not item.disabled:
                entry = {}
                entry['title'] = item.title
                entry['url'] = item.url
                entry['issue'] = c.title
                user = getUserByID(item.owners.split(',')[0])
                entry['author'] = user.name
                entry['date'] = item.events[0].date
                entry['numComments'] = len([comment for comment in item.comments if comment.disabled == 0 and comment.pending == 0])
                entry['suggestionID'] = item.id

                """ Grab first 250 chars as a summary """
                if len(item.revisions[0].data) <= 250:
                    entry['suggestionSummary'] = h.literal(h.reST2HTML(item.revisions[0].data))
                else:
                    entry['suggestionSummary'] = h.literal(h.reST2HTML(item.revisions[0].data[:250] + '...'))

                """ Populate ratings, if they've already been rated """
                rating = getRatingForSuggestion(item.id, c.authuser.id)
                if rating:
                    entry['rating'] = rating.rating
                else:
                    entry['rating'] = -1
                if item.avgRating == None:
                    entry['avgRating'] = 0
                else:
                    entry['avgRating'] = item.avgRating

                c.suggestions.append(entry)

        events = i.events
        unique = []
        c.participants = []

        for e in events:
            if e.user_id not in unique:
                unique.append(e.user_id)

        for id in unique:
            c.participants.append(getUserByID(id))

        news = getArticlesByIssueID(i.id)
        if not news:
            c.news = None
        else:
            c.news = []
            for n in news:
                if n.type != 'background':
                    if n.pending or n.disabled:
                        continue
                    entry = {}
                    entry['type'] = n.type
                    entry['url'] = h.quote(n.url)
                    entry['title'] = n.title
                    if len(n.comment) > 50:
                        entry['summary'] = n.comment[:50] + '...'
                    else:
                        entry['summary'] = n.comment
                    entry['directory'] = 'news'
                    entry['hash'] = 'news'
                    entry['user'] = n.user.name
                    entry['time'] = n.events[-1].date
                    c.news.append(entry)
            if len(c.news) == 0:
                c.news = None

        if session.get('user'):
            reST = r.data

            reSTlist = self.get_reSTlist(reST)
            HTMLlist = self.get_HTMLlist(reST)

            c.wikilist = zip(HTMLlist, reSTlist)

            c.owners = [int(owner) for owner in c.p.owners.split(',')]
            return render('/derived/issuehome.html')
        else:
            c.content = h.literal(h.reST2HTML(r.data))
            return render('/derived/issuehome.html')


    def background(self, id):
        c.p = get_page(id)
        session['pageID'] = c.p.id
        if c.p == False:
            abort(404, h.literal("That page does not exist!"))

        c.title = c.p.title.decode('latin-1')
        c.url = c.p.url.decode('latin-1')
        
        r = c.p.revisions[0]

        c.lastmoddate = r.event.date
        c.lastmoduser = r.event.user.name
        s = getSlideshow(c.p.id)
        c.slideshow = []
        c.slideshowDirectory = 'slideshows'
        for item in s:
            entry = {}
            entry['hash'] = item.pictureHash
            entry['caption'] = item.caption
            entry['title'] = item.title
            c.slideshow.append(entry)

        if session.get('user'):
            reST = r.data

            reSTlist = self.get_reSTlist(reST)
            HTMLlist = self.get_HTMLlist(reST)

            c.wikilist = zip(HTMLlist, reSTlist)

            c.owners = [int(owner) for owner in c.p.owners.split(',')]
            #return render('/derived/wiki.mako')
            return render('/derived/issuebg.html')
            return render('/derived/testWikilist.html')
        else:
            c.content = h.literal(h.reST2HTML(r.data))
            #return render('/derived/view.mako')
            #return render('/derived/issuebgPublic.html')
            return render('/derived/issuebg.html')

    def index(self, id):
        c.p = get_page(id)
        if c.p == False:
            abort(404, h.literal("That page does not exist!"))

        c.title = c.p.title.decode('latin-1')
        c.url = c.p.url.decode('latin-1')
        
        r = c.p.revisions[0]

        c.lastmoddate = r.event.date
        c.lastmoduser = r.event.user.name

        if session.get('user'):
            reST = r.data

            reSTlist = self.get_reSTlist(reST)
            HTMLlist = self.get_HTMLlist(reST)

            c.wikilist = zip(HTMLlist, reSTlist)

            c.owners = [int(owner) for owner in c.p.owners.split(',')]
            #return render('/derived/wiki.mako')
            return render('/derived/issuebg.html')
            return render('/derived/testWikilist.html')
        else:
            c.content = h.literal(h.reST2HTML(r.data))
            #return render('/derived/view.mako')
            return render('/derived/issuebgPublic.html')
            return render('/derived/issuebg.html')

    def readThis(self):
        if readThisPage(c.authuser.id, session['pageID'], 'background'):
            h.flash("You have read this wiki!", "success")
        else:
            h.flash("You have already read this!", "warning")
        p = getPageByID(session['pageID'])
        return redirect('/issue/%s/background' % p.url.decode('latin-1'))

    """ Renders the leaderborad page for a given issue.  Takes in the issue URL as the id argument. """
    def leaderboard(self, id):
        return render('/derived/leaderboard.html')

    # ------------------------------------------
    #    Helper functions for wiki controller
    #-------------------------------------------

    @h.login_required
    def CleanList( self, l ):
        """ Remove all empty rows from list """
        counter = 0
        length = len( l )
        while counter < length:
            if l[counter].isspace() or l[counter] == None or l[counter] == "":
                del l[counter]
                length = len( l )   
            counter += 1
        return l


    @h.login_required
    def isodd( self, integer ):
        """ if interger is odd return True, else return False"""
        if integer % 2 == 0:
            return False
        else:
            return True
    
    @h.login_required
    def get_reSTlist( self, reST ):
        """Accept a reST string and return a list of sections
        This code is a bit ugly but it works... 
        SORRY IF YOU HAVE TO WORK ON THIS..."""

        splitter = re.compile('(.*\r\n[=\-`:~^_*+#]{3,}.+\r\n+)') # Create regex object that splits reST string by headings
        reSTlist = self.CleanList(splitter.split( reST )) # Split the reST into a list, and remove any empty rows
        
        """reSTlist has heading and section data in seperate rows.
        The logic below merges the heading and section data rows."""
        
        lenght = len( reSTlist )
        
        if self.isodd( lenght ): # if the length is odd, the first row doesn't have a heading and will be in its own section
            offset = counter = 1
        else:
            offset = counter = 0

        """ join the heading list row with the data list row """
        while counter < lenght: # loop through list until end
            if self.isodd( counter + offset ): # do nothing if even
                reSTlist[counter-1] = reSTlist[counter-1] + reSTlist[counter]
                reSTlist[counter] = "" # set current row to empty
            counter = counter + 1

        return self.CleanList( reSTlist ) # remove empty rows and return list

    @h.login_required
    def get_HTMLlist( self, reST):
        """Accept reST list, convert to html, remove newlines so regex works, split HTML into a list by heading."""

        splitter = re.compile('(<div class\="section".*?)(?=<div class\="section")', re.DOTALL) # Create regex object to split HTML by header section.
        HTMLlist = self.CleanList(splitter.split(h.literal(h.reST2HTML( reST ))))
        
        if len(HTMLlist) == 1: # This only happens if there are two sections but only one heading
            splitter = re.compile('(<div class\="section".*</div>)', re.DOTALL) # Create regex object to split HTML by header section.
            HTMLlist = self.CleanList(splitter.split(h.literal(h.reST2HTML( reST ))))      
    
        return HTMLlist
