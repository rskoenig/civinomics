import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, redirect

from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.event import Event, getParentEvents
from pylowiki.lib.base import BaseController, render
from pylowiki.lib.db.workshop import getWorkshop, isScoped
from pylowiki.lib.db.discussion import getActiveDiscussionsForWorkshop, getDiscussions, getDiscussion, getDiscussionByID
from pylowiki.lib.utils import urlify
from pylowiki.lib.db.user import isAdmin
from pylowiki.lib.db.facilitator import isFacilitator

from pylowiki.lib.db.discussion import Discussion

import pylowiki.lib.helpers as h

log = logging.getLogger(__name__)

class DiscussionController(BaseController):

    @h.login_required
    def index(self, id1, id2):
        workshopCode = id1
        workshopURL = id2
        c.w = getWorkshop(workshopCode, urlify(workshopURL))
        log.info(c.w)
        c.title = c.w['title']
        c.code = c.w['urlCode']
        c.url = c.w['url']
        c.discussions = getActiveDiscussionsForWorkshop(workshopCode, urlify(workshopURL), 'general')

        return render('/derived/discussion_landing.bootstrap')

    @h.login_required
    def topic(self, id1, id2, id3, id4):
        workshopCode = id1
        workshopUrl = id2
        discussionCode = id3
        discussionUrl = id4
        
        c.w = getWorkshop(workshopCode, urlify(workshopUrl))
        c.discussion = getDiscussion(discussionCode, urlify(discussionUrl))
        c.otherDiscussions = getActiveDiscussionsForWorkshop(workshopCode, urlify(workshopUrl))
        if c.discussion['disabled'] == '0' and c.discussion['deleted'] == '0':
            c.otherDiscussions.remove(c.discussion)

        c.title = c.w['title']
        return render('/derived/discussion_topic.bootstrap')

    @h.login_required
    def addDiscussion(self, id1, id2):
        code = id1
        url = id2

        c.w = getWorkshop(code, urlify(url))
        c.title = c.w['title']

        return render('/derived/discussion_edit.bootstrap')

    def newDiscussionHandler(self, id1, id2):
        code = id1
        url = id2
        w = getWorkshop(code, urlify(url))

        
        if 'title' in request.params:
            title = request.params['title']
        else: 
            title = False
        if 'text' in request.params:
            text = request.params['text']
        else:
            text = ''

        if not title or title=='':
            alert = {'type':'error'}
            alert['title'] = 'Title Field Required'
            alert['content'] = ''
            session['alert'] = alert
            session.save()
            return redirect('/workshop/%s/%s/addDiscussion' % (code, url))

        else:
            d = Discussion(owner = c.authuser, discType = 'general', workshop = w, title = title, text = text)
            commit(w)
        
        return redirect('/workshop/%s/%s/discussion/%s/%s' % (code, url, d.d['urlCode'], d.d['url']))
    
    def editDiscussion(self, id1, id2):
        code = id1
        url = id2
        c.discussion = getDiscussion(code, urlify(url))
        c.w = getWorkshop(c.discussion['workshopCode'], urlify(c.discussion['workshopURL']))
        
        return render('/derived/discussion_edit.bootstrap')
        
    def editDiscussionHandler(self, id1, id2):
        code = id1
        url = id2
        discussion = getDiscussion(code, urlify(url))
        w = getWorkshop(discussion['workshopCode'], discussion['workshopURL'])

        
        if 'title' in request.params:
            title = request.params['title']
        else: 
            title = False
        if 'text' in request.params:
            text = request.params['text']
        else:
            text = ''

        if not title or title=='':
            alert = {'type':'error'}
            alert['title'] = 'Title Field Required'
            alert['content'] = ''
            session['alert'] = alert
            session.save()
            return redirect('/editDiscussion/%s/%s' % (code, url))

        else:
            discussion['title'] = title
            discussion['text'] = text
        
        return redirect('/workshop/%s/%s/discussion/%s/%s' % (w['urlCode'], w['url'], discussion['urlCode'], discussion['url']))
    
        
    def adminDiscussion(self, id1, id2):
        code = id1
        url = id2
        c.discussion = getDiscussion(code, urlify(url))
        c.w = getWorkshop(c.discussion['workshopCode'], urlify(c.discussion['workshopURL']))
        
        
        return render('/derived/discussion_admin.bootstrap')

    def adminDiscussionHandler(self):
        
        workshopCode = request.params['workshopCode']
        workshopURL = request.params['workshopURL']
        w = getWorkshop(workshopCode, workshopURL) 

        discussionCode = request.params['discussionCode']
        discussionURL = request.params['discussionURL']
        d = getDiscussion(discussionCode, discussionURL)
        log.info("BEFORE")
                
        try:

           if not isAdmin(c.authuser.id) and not isFacilitator(c.authuser.id, w.id):
              h.flash('You are not authorized', 'error')
              return redirect('/workshop/%s/%s/resource/%s/%s'%(w['urlCode'], w['url'], d['urlCode'], d['url']))
           log.info("HMMMM")
           modType = request.params['modType']
           log.info("1")
           verifyModDiscussion = request.params['verifyModDiscussion']
           log.info("2")
           modDiscussionReason = request.params['modDiscussionReason']
           log.info("3")
           log.info("HERE")
        except:
           alert = {'type':'error'}
           alert['title'] = 'All Fields Required BLAH'
           alert['content'] = ''
           session['alert'] = alert
           session.save()
           return redirect('/adminDiscussion/%s/%s' % (d['urlCode'], d['url']))

        # disable or enable the resource, log the event
        if modType == 'disable':
            if d['disabled'] == '0':
               d['disabled'] = True
               modTitle = "Discussion Disabled"
            else:
               d['disabled'] = False
               modTitle = "Discussion Enabled"
        elif modType == 'delete':
            if d['deleted'] == '0':
                d['disabled'] = False
                d['deleted'] = True
                modTitle = "Discussion Deleted"


        commit(d)
        if modDiscussionReason == "":
            modDiscussionReason = "No Reason Given"
        e = Event(modTitle, modDiscussionReason, d, c.authuser)

        h.flash(modTitle, 'success')
        if modType == 'deleted':
            return redirect('/workshop/%s/%s/discussion/'%(w['urlCode'], w['url']))
        else:
            return redirect('/workshop/%s/%s/discussion/%s/%s'%(w['urlCode'], w['url'], d['urlCode'], d['url']))
            