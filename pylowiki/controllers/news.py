import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from pylowiki.lib.db.user import get_user, getUserByID, isAdmin
from pylowiki.lib.db.facilitator import isFacilitator
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.workshop import getWorkshop
from pylowiki.lib.db.event import Event, getParentEvents
from pylowiki.lib.db.article import Article, getArticle, getArticleByLink, getArticlesByWorkshopID, getArticleByID
from pylowiki.lib.db.discussion import getDiscussionByID
from pylowiki.lib.db.rating import getRatingByID
from pylowiki.lib.db.flag import Flag, checkFlagged, getFlags

from pylowiki.lib.utils import urlify

from pylowiki.lib.base import BaseController, render
import pickle

#from pylowiki.lib.points import readThisPage

import pylowiki.lib.helpers as h
import simplejson as json

log = logging.getLogger(__name__)

class NewsController(BaseController):

    def index(self, id1, id2, id3, id4):
        workshopCode = id1
        workshopURL = id2
        resourceCode = id3
        resourceURL = id4
        
        c.w = getWorkshop(workshopCode, workshopURL)
        
        c.title = c.w['title']
        c.resource = getArticle(resourceCode, urlify(resourceURL), c.w)

        c.flagged = False
        if checkFlagged(c.resource):
           c.flagged = True

        if 'user' in session:
            c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
            c.isAdmin = isAdmin(c.authuser.id)

            if 'ratedThings_article_overall' in c.authuser.keys():
                """
                    Here we get a list of tuples.  Each tuple is of the form (a, b), with the following mapping:
                    a         ->    rated Thing's ID  (What was rated) 
                    b         ->    rating Thing's ID (The rating object)
                """
                l = pickle.loads(str(c.authuser['ratedThings_article_overall']))
                for tup in l:
                    if tup[0] == c.resource.id:
                        c.rating = getRatingByID(tup[1])
                    
        c.poster = getUserByID(c.resource.owner)
        
        c.otherResources = getArticlesByWorkshopID(c.w.id)
        for i in range(len(c.otherResources)):
            resource = c.otherResources[i]
            if resource.id == c.resource.id:
                c.otherResources.pop(i)
                break
        c.discussion = getDiscussionByID(int(c.resource['discussion_id']))
        c.lastmoddate = c.resource.date
        c.lastmoduser = getUserByID(c.resource.owner)
        
        return render('/derived/resource.html')

    def modResource(self, id1, id2, id3, id4):
        workshopCode = id1
        workshopURL = id2
        resourceCode = id3
        resourceURL = id4
        
        c.w = getWorkshop(workshopCode, workshopURL)
        
        c.title = c.w['title']
        c.resource = getArticle(resourceCode, urlify(resourceURL), c.w)
        c.flags = getFlags(c.resource)
        c.events = getParentEvents(c.resource)

        c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
        c.isAdmin = isAdmin(c.authuser.id)

        c.author = getUserByID(c.resource.owner)
        
        return render('/derived/resource_admin.html')

    def modResourceHandler(self):
        try:
           w = False
           r = False
           workshopCode = request.params['workshopCode']
           workshopURL = request.params['workshopURL']
           w = getWorkshop(workshopCode, workshopURL) 

           resourceCode = request.params['resourceCode']
           resourceURL = request.params['resourceURL']
           r = getArticle(resourceCode, urlify(resourceURL), w) 

           if not isAdmin(c.authuser.id) and not isFacilitator(c.authuser.id, w.id):
              h.flash('You are not authorized', 'error')
              return redirect('/workshop/%s/%s/resource/%s/%s'%(w['urlCode'], w['url'], r['urlCode'], r['url']))


           modResourceReason = request.params['modResourceReason']
           verifyModResource = request.params['verifyModResource']
        except:
           h.flash('All fields required', 'error')
           return redirect('/workshop/%s/%s/resource/%s/%s'%(w['urlCode'], w['url'], r['urlCode'], r['url']))

        # disable or enable the resource, log the event
        if r['disabled'] == '0':
           r['disabled'] = True
           modTitle = "Resource Disabled"
        else:
           r['disabled'] = False
           modTitle = "Resource Enabled"

        commit(r)
        e = Event(modTitle, modResourceReason, r, c.authuser)

        h.flash(modTitle, 'success')
        return redirect('/workshop/%s/%s/resource/%s/%s'%(w['urlCode'], w['url'], r['urlCode'], r['url']))


    @h.login_required
    def handler(self, id1, id2):
        code = id1
        url = id2
        
        linkURL = request.params['url']
        comment = request.params['data']
        title = request.params['title']
        
        w = getWorkshop(code, url)
        a = getArticleByLink(linkURL, w)

        if a:
            h.flash('Link already submitted for this issue', 'warning')
            return redirect('/workshop/%s/%s'%(code, url))

        a = Article(linkURL, title, comment, c.authuser, w)
        
        if 'resources' not in w.keys():
            w['resources'] = a.a.id
        else:
            w['resources'] = w['resources'] + ',' + str(a.a.id)
        
        w['numResources'] = int(w['numResources']) + 1
        commit(w)
        return redirect('/workshop/%s/%s'%(code, url))

    @h.login_required
    def readThis(self):
        if readThisPage(c.authuser.id, request.params['articleID'], 'article'):
            h.flash("You have read this article!", "success")
        else:
            h.flash("You have already read this article!", "warning")
        a = getArticle(request.params['articleID'])
        i = getIssueByID(request.params['issueID'])
        return redirect('/issue/%s/news/%s'%(i.page.url, a.title))

    @h.login_required
    def flagResource(self, id1):
        resourceID = id1
        resource = getArticleByID(resourceID)
        if not resource:
            return json.dumps({'id':resourceID, 'result':'ERROR'})
        if not isFlagged(resource, c.authuser):
            f = Flag(resource, c.authuser)
            return json.dumps({'id':resourceID, 'result':"Successfully flagged!"})
        else:
            return json.dumps({'id':resourceID, 'result':"Already flagged!"})


