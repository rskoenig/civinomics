import logging, re, pickle
import time, datetime

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from pylowiki.lib.db.workshop import Workshop, getWorkshop, isScoped
from pylowiki.lib.db.geoInfo import getScopeTitle
from pylowiki.lib.db.revision import get_revision
from pylowiki.lib.db.slideshow import getSlideshow
from pylowiki.lib.db.slide import getSlide
from pylowiki.lib.db.discussion import getDiscussionByID
from pylowiki.lib.db.article import getArticlesByWorkshopID
from pylowiki.lib.db.suggestion import getSuggestionsForWorkshop
from pylowiki.lib.db.user import getUserByID
from pylowiki.lib.db.facilitator import isFacilitator, getFacilitators
from pylowiki.lib.db.rating import getRatingByID
from pylowiki.lib.db.tag import Tag
from pylowiki.lib.db.motd import MOTD, getMessage
from pylowiki.lib.db.follow import Follow, getFollow, isFollowing

from pylowiki.lib.utils import urlify

from pylowiki.lib.base import BaseController, render
import pylowiki.lib.helpers as h
from pylowiki.lib.db.dbHelpers import commit

import re

log = logging.getLogger(__name__)

class WorkshopController(BaseController):

    def addWorkshop(self):
        if int(c.authuser['accessLevel']) >= 100:
        #if self._checkAccess(100):
            #return render('/derived/createIssue.mako')
            c.title = "Create Workshop"
            c.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            c.days = range(1, 32)
            c.years = range(2012, 2021)
            c.maxSlideshowEntries = 10
            return render('/derived/issue_create.html')
        else:
            h.flash("You are not authorized to view that page", "warning")
            return redirect('/')

    def followHandler(self, id1, id2):
        code = id1
        url = id2
        ##log.info('followHandler %s %s' % (code, url))
        w = getWorkshop(code, urlify(url))
        f = getFollow(c.authuser.id, w.id)
        if f:
           ##log.info('f is %s' % f)
           f['disabled'] = False
           commit(f)
        elif not isFollowing(c.authuser.id, w.id): 
           f = Follow(c.authuser.id, w.id, 'workshop') 
           commit(f)
           
        return "ok"

    def unfollowHandler(self, id1, id2):
        code = id1
        url = id2
        ##log.info('unfollowHandler %s %s' % (code, url))
        w = getWorkshop(code, urlify(url))
        f = getFollow(c.authuser.id, w.id)
        if f:
           ##log.info('f is %s' % f)
           f['disabled'] = True
           commit(f)
           
        return "ok"

    def editWorkshopHandler(self, id1, id2):
        code = id1
        url = id2
        c.title = "Edit Workshop Settings"

        w = getWorkshop(code, urlify(url))
        werror = 0
        werrMsg = 'Missing Info: '
        wstarted = 0
        if w['startTime'] != '0000-00-00':
           wstarted = 1

        ##log.info('wstarted is %s' % wstarted)

        # Is there anything more painful than form validation?
        # I don't think so...

        if 'title' in request.params:
           wTitle = request.params['title']
           if wTitle == '':
              werrMsg += 'Name '
              werror = 1
           else:
              w['title'] = wTitle
        else:
           werrMsg += 'Name '
           werror = 1

        if 'goals' in request.params:
           wGoals = request.params['goals']
           wGoals = wGoals.lstrip()
           wGoals = wGoals.rstrip()
           if wGoals == '' or wGoals == 'No goals set':
              werror = 1
              werrMsg += 'Goals '
           else:
              w['goals'] = request.params['goals']
        else:
           werror = 1
           werrMsg += 'Goals '

        # Hmm... Take this out so they can't change it?
        #if 'publicPostal' in request.params:
        #   w['publicPostal'] = request.params['publicPostal']
        #else:
        #   werror = 1
        #   werrMsg = 'No Workshop Postal'

        if not wstarted:
           if 'publicScope' in request.params:
              w['publicScope'] = request.params['publicScope']
              w['scopeMethod'] = 'publicScope'
           else:
              w['publicScope'] = '00'
              werror = 1
              werrMsg += 'Participants '

           if 'publicPostalList' in request.params:
              plist = request.params['publicPostalList']
              plist = plist.lstrip()
              plist = plist.rstrip()
              w['publicPostalList'] = plist
              if plist != '':
                 w['scopeMethod'] = 'publicPostalList'
                 w['publicScope'] = '00'
                 if werrMsg == 'Participants':
                    werrMsg = ''
                    werror = 0
              elif w['publicScope'] == '00':
                 werror = 1
                 werrMsg += 'Pariticpants or Postal List '
           else:
              werror = 1
              werrMsg += 'Participants or PostalList '

           if w['scopeMethod'] == 'publicScope':
              w['publicScopeTitle'] = getScopeTitle(w['publicPostal'], 'United States', w['publicScope'])
           elif w['scopeMethod'] == 'publicPostalList':
              w['publicScopeTitle'] = 'postal codes of ' + w['publicPostalList']

           if 'publicTags' in request.params:
              publicTags = request.params.getall('publicTags')
              w['publicTags'] = ','.join(publicTags)
           else:
              werror = 1
              werrMsg += 'System Tags '
   
           if 'memberTags' in request.params:
              wMemberTags = request.params['memberTags']
              wMemberTags = wMemberTags.lstrip()
              wMemberTags = wMemberTags.rstrip()
              if wMemberTags == '' or wMemberTags == 'none':
                 werror = 1
                 werrMsg += 'Member Tags '
              else:
                 w['memberTags'] = wMemberTags
           else:
              werror = 1
              werrMsg += 'Member Tags '

           if 'startWorkshop' in request.params:
              startButtons = request.params.getall('startWorkshop')
              ##log.info('Got startWorkshop %s' % ','.join(startButtons))
              if 'Start' in startButtons and 'VerifyStart' in startButtons and werror == 0:
                 startTime = datetime.datetime.now()
                 w['startTime'] = startTime.ctime()
                 endTime = datetime.datetime.now()
                 endTime = endTime.replace(year = endTime.year + 1)
                 w['endTime'] = endTime.ctime()
                 for wTag in request.params.getall('publicTags'):
                    t = Tag('system', wTag, w.id, w.owner)
                 for mTag in wMemberTags.split(','):
                    t = Tag('member', mTag, w.id, w.owner)
                 m = MOTD('Welcome to the workshop!', w.id, w.id)

        commit(w)

        if werror == 1:
            h.flash( werrMsg, 'error')
        else:
            h.flash('Workshop configuration complete!', 'success')

        return redirect('/workshop/%s/%s'%(w['urlCode'], w['url']))


    def addWorkshopHandler(self):
        workshopName = request.params['workshopName']
        """
        goals = request.params['goals']
        day = request.params['workshopDay']
        month = request.params['workshopMonth']
        year = request.params['workshopYear']
        backgroundWiki = request.params['backgroundWiki']
        c.numSlideshowEntries = request.params['numSlideshowEntries']
        """
        publicPrivate = request.params['publicPrivate']
        w = Workshop(workshopName, c.authuser, publicPrivate)
        c.workshop_id = w.w.id # TEST
        c.title = 'Add slideshow'
        #return render('/derived/addSlideshow.html')
        return redirect('/workshops/%s/%s'%(w.w['urlCode'], w.w['url']))
    
    def adminWorkshopHandler(self, id1, id2):
        code = id1
        url = id2
        c.title = "Administrate Workshop"

        w = getWorkshop(code, urlify(url))
        m = getMessage(w.id)
         
        werror = 0
        werrMsg = 'Incomplete information: '

        if 'motd' in request.params:
           motd = request.params['motd']
           m['data'] = motd
        else:
           werror = 1
           werrMsg += 'Message text '
            
        if 'enable' in request.params:
           enable = request.params['enable']
           if enable == '1' or enable == '0':
              m['enabled'] = enable
           else:
              werror = 1
              werrMsg += 'Publish message or not '
        else:
           werror = 1
           werrMsg += 'Publish message or not '
            
        commit(m)
        return redirect('/workshops/%s/%s'%(w['urlCode'], w['url']))
    
    def display(self, id1, id2):
        code = id1
        url = id2
        
        c.w = getWorkshop(code, urlify(url))
        c.title = c.w['title']
        c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
        c.facilitators = getFacilitators(c.w.id)
        c.isScoped = isScoped(c.authuser, c.w)
        c.isFollowing = isFollowing(c.authuser.id, c.w.id)
        ##log.info('c.isFollowing is %s' % c.isFollowing)
        if int(c.authuser['accessLevel']) >= 200:
           c.isAdmin = True
        else:
           c.isAdmin = False
        
        c.slides = []
        c.slideshow = getSlideshow(c.w['mainSlideshow_id'])
        slide_ids = [int(item) for item in c.slideshow['slideshow_order'].split(',')]
        for id in slide_ids:
            s = getSlide(id) # Don't grab deleted slides
            if s:
                c.slides.append(s)
            
        c.articles = getArticlesByWorkshopID(c.w.id)
        c.suggestions = getSuggestionsForWorkshop(code, urlify(url))
        l = []
        ratedSuggestionIDs = []
        if 'ratedThings_suggestion_overall' in c.authuser.keys():
            """
                Here we get a list of tuples.  Each tuple is of the form (a, b), with the following mapping:
                a         ->    rated Thing's ID  (What was rated) 
                b         ->    rating Thing's ID (The rating object)
            """
            l = pickle.loads(str(c.authuser['ratedThings_suggestion_overall']))
            ratedSuggestionIDs = [tup[0] for tup in l]
        
        for item in c.suggestions:
            """ Grab first 250 chars as a summary """
            if len(item['data']) <= 250:
                item['suggestionSummary'] = h.literal(h.reST2HTML(item['data']))
            else:
                item['suggestionSummary'] = h.literal(h.reST2HTML(item['data'][:250] + '...'))
            
            """ Grab the associated rating, if it exists """
            found = False
            try:
                index = ratedSuggestionIDs.index(item.id)
                found = True
            except:
                pass
            if found:
                item.rating = getRatingByID(l[index][1])
            else:
                item.rating = False

        c.discussion = getDiscussionByID(c.w['backgroundDiscussion_id'])

        if 'feedbackDiscussion_id' in c.w:
           c.discussion = getDiscussionByID(c.w['feedbackDiscussion_id'])
        else:
           c.discussion = getDiscussionByID(c.w['backgroundDiscussion_id'])

        c.motd = getMessage(c.w.id)
        # kludge for now
        if c.motd == False:
           c.motd = MOTD('Welcome to the workshop!', c.w.id, c.w.id)

        """ Grab first 250 chars as a summary """
        if len(c.motd['data']) <= 140:
            c.motd['messageSummary'] = h.literal(h.reST2HTML(c.motd['data']))
        else:
            c.motd['messageSummary'] = h.literal(h.reST2HTML(c.motd['data'][:140] + '...'))


        return render('/derived/issuehome.html')

    def background(self, id1, id2):
        code = id1
        url = id2
        
        c.w = getWorkshop(code, url)
        c.title = c.w['title']
        c.articles = getArticlesByWorkshopID(c.w.id)
        
        c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
        c.facilitators = getFacilitators(c.w.id)
        
        c.slides = []
        c.slideshow = getSlideshow(c.w['mainSlideshow_id'])
        slide_ids = [int(item) for item in c.slideshow['slideshow_order'].split(',')]
        for id in slide_ids:
            s = getSlide(id) # Don't grab deleted slides
            if s:
                c.slides.append(s)
        
        r = get_revision(int(c.w['mainRevision_id']))
        reST = r['data']
        reSTlist = self.get_reSTlist(reST)
        HTMLlist = self.get_HTMLlist(reST)
        
        c.wikilist = zip(HTMLlist, reSTlist)
        
        c.discussion = getDiscussionByID(c.w['backgroundDiscussion_id'])
        
        c.lastmoddate = r.date
        c.lastmoduser = getUserByID(r.owner)
        
        return render('/derived/issuebg.html')

    def feedback(self, id1, id2):
        code = id1
        url = id2

        c.w = getWorkshop(code, urlify(url))
        r = get_revision(int(c.w['mainRevision_id']))
        c.lastmoddate = r.date
        c.lastmoduser = getUserByID(r.owner)

        c.title = c.w['title']
        c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
        c.facilitators = getFacilitators(c.w.id)
        c.isScoped = isScoped(c.authuser, c.w)

        if 'feedbackDiscussion_id' in c.w:
           c.discussion = getDiscussionByID(c.w['feedbackDiscussion_id'])
        else:
           c.discussion = getDiscussionByID(c.w['backgroundDiscussion_id'])

        c.rating = False
        if 'ratedThings_workshop_overall' in c.authuser.keys():
            """
                Here we get a list of tuples.  Each tuple is of the form (a, b), with the following mapping:
                a         ->    rated Thing's ID  (What was rated) 
                b         ->    rating Thing's ID (The rating object)
            """
            l = pickle.loads(str(c.authuser['ratedThings_workshop_overall']))
            for tup in l:
                if tup[0] == c.w.id:
                    c.rating = getRatingByID(tup[1])

        c.motd = getMessage(c.w.id)
        # kludge for now
        if c.motd == False:
           c.motd = MOTD('Welcome to the workshop!', c.w.id, c.w.id)

        return render("/derived/issue_feedback.html")
    
    @h.login_required
    def editSettings(self, id1, id2):
        code = id1
        url = id2

        c.w = getWorkshop(code, urlify(url))
        c.title = c.w['title']

        # make sure they can actually do this
        if isFacilitator(c.authuser.id, c.w.id) or int(c.authuser['accessLevel']) >= 100:
            return render('/derived/issue_settings.html')
        else:
            return render('/derived/404.html')
    
    @h.login_required
    def admin(self, id1, id2):
        code = id1
        url = id2

        c.w = getWorkshop(code, urlify(url))
        c.title = c.w['title']
        c.motd = getMessage(c.w.id)
        # kludge for now
        if c.motd == False:
           c.motd = MOTD('Welcome to the workshop!', c.w.id, c.w.id)

        """ Grab first 250 chars as a summary """
        if len(c.motd['data']) <= 140:
            c.motd['messageSummary'] = h.literal(h.reST2HTML(c.motd['data']))
        else:
            c.motd['messageSummary'] = h.literal(h.reST2HTML(c.motd['data'][:140] + '...'))


        # make sure they can actually do this
        if isFacilitator(c.authuser.id, c.w.id) or int(c.authuser['accessLevel']) >= 100:
            return render('/derived/issue_admin.html')
        else:
            return render('/derived/404.html')
    
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
