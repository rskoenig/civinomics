import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from pylowiki.lib.db.user import get_user, getUserByID, isAdmin
from pylowiki.lib.db.facilitator import isFacilitator
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.workshop import getWorkshop, getWorkshopByID, isScoped
from pylowiki.lib.db.event import Event, getParentEvents
from pylowiki.lib.db.resource import Resource, getResource, getResourceByLink, getResourcesByWorkshopID, getActiveResourcesByWorkshopID, getResourceByID, getResource
from pylowiki.lib.db.discussion import getDiscussionByID
from pylowiki.lib.db.rating import getRatingByID
from pylowiki.lib.db.flag import Flag, isFlagged, checkFlagged, getFlags
from pylowiki.lib.db.page import Page, getPageByID, get_page
from pylowiki.lib.db.revision import Revision, get_revision

from pylowiki.lib.utils import urlify

from pylowiki.lib.base import BaseController, render
import pickle

#from pylowiki.lib.points import readThisPage

import pylowiki.lib.helpers as h
import simplejson as json

log = logging.getLogger(__name__)

class ResourceController(BaseController):

    def index(self, id1, id2, id3, id4):
        workshopCode = id1
        workshopURL = id2
        resourceCode = id3
        resourceURL = id4
        
        c.w = getWorkshop(workshopCode, workshopURL)
        
        c.title = c.w['title']
        c.resource = getResource(resourceCode, urlify(resourceURL))
        c.events = getParentEvents(c.resource)
        if c.resource['disabled'] == '1' or c.resource['allowComments'] == '0':
            c.commentsDisabled = 1
        else:
            c.commentsDisabled = 0

        c.content = h.literal(h.reST2HTML(c.resource['comment']))

        c.flagged = False
        if checkFlagged(c.resource):
           c.flagged = True

        if 'user' in session:
            c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
            c.isAdmin = isAdmin(c.authuser.id)

            if 'ratedThings_resource_overall' in c.authuser.keys():
                """
                    Here we get a Dictionary with the commentID as the key and the ratingID as the value
                    Check to see if the commentID as a string is in the Dictionary keys
                    meaning it was already rated by this user
                """
                resRateDict = pickle.loads(str(c.authuser['ratedThings_resource_overall']))
                if c.resource.id in resRateDict.keys():
                    c.rating = getRatingByID(resRateDict[c.resource.id])
        else:            
            c.isFacilitator = False
            c.isAdmin = False

        c.poster = getUserByID(c.resource.owner)
        
        c.otherResources = getActiveResourcesByWorkshopID(c.w.id)
        for i in range(len(c.otherResources)):
            resource = c.otherResources[i]
            if resource.id == c.resource.id:
                c.otherResources.pop(i)
                break
        c.discussion = getDiscussionByID(int(c.resource['discussion_id']))
        if 'mainRevision_id' in c.resource:
            r = get_revision(int(c.resource['mainRevision_id']))
            c.lastmoddate = r.date
        else:
            c.lastmoddate = c.resource.date
        c.lastmoduser = getUserByID(c.resource.owner)
        
        return render('/derived/resource.html')

    @h.login_required
    def newResource(self, id1, id2):
        code = id1
        url = id2

        c.w = getWorkshop(code, urlify(url))

        a = isAdmin(c.authuser.id)
        f =  isFacilitator(c.authuser.id, c.w.id)
        s = isScoped(c.authuser, c.w)
        if (s and c.w['allowResources'] == '1') or a or f:
            c.r = False
            c.otherResources = getResourcesByWorkshopID(c.w.id)

            return render('/derived/resource_edit.html')
        else:
            h.flash('You are not authorized', 'error')
            return redirect('/workshop/%s/%s'%(c.w['urlCode'], urlify(c.w['url'])))

    @h.login_required
    def editResource(self, id1, id2):
        code = id1
        url = id2

        c.r = getResource(code, urlify(url))
        c.w = getWorkshopByID(c.r['workshop_id'])
        a = isAdmin(c.authuser.id)
        f =  isFacilitator(c.authuser.id, c.w.id)
        if c.authuser.id == c.r.owner or (a or f):
            for i in range(len(c.otherResources)):
                resource = c.otherResources[i]
                if resource.id == c.r.id:
                    c.otherResources.pop(i)
                    break

            return render('/derived/resource_edit.html')
        else:
            h.flash('You are not authorized a is %s and f is %s'%(a, f), 'error')
            return redirect('/workshop/%s/%s/resource/%s/%s'%(c.w['urlCode'], urlify(c.w['url']), c.r['urlCode'], urlify(c.r['url'])))

    @h.login_required
    def saveResource(self, id1, id2):
        code = id1
        url = id2
        
        if 'title' in request.params:
            title = request.params['title']
        else: 
            title = False
        if 'comment' in request.params:
            comment = request.params['comment']
        else:
            comment = False
        if 'link' in request.params:
            link = request.params['link']
        else:
            link = False
        if 'allowComments' in request.params:
            allowComments = request.params['allowComments']
        else:
            allowComments = -1
        
        rerror = 0
        rerrorMsg = ''
        if not comment or not title:
            rerror = 1
            rerrorMsg = 'Enter resource title and description.'

        if comment == '' or title == '':
            rerror = 1
            rerrorMsg = 'Enter resource title and text.'

        if allowComments != '1' and allowComments != '0':
            rerror = 1
            rerrorMsg = 'Allow comments or not?'

        resource = getResource(code, urlify(url))
        w = getWorkshopByID(resource['workshop_id'])

        a = isAdmin(c.authuser.id)
        f =  isFacilitator(c.authuser.id, w.id)
        if c.authuser.id != resource.owner and (a == False and f == False):
           rerror = 1
           rerrorMsg = 'You are not authorized'
        if rerror:
           h.flash(rerrorMsg, 'error')
        else:
           cMsg = 'Edits: '
           if resource['title'] != title:
              cMsg = 'Title updated. '
           resource['title'] = title
           if resource['comment'] != comment:
              cMsg = cMsg + 'Description updated. '
           resource['comment'] = comment
           if resource['allowComments'] != allowComments:
              if allowComments == '0':
                 cMsg = cMsg + 'Comments disabled. '
              else:
                 cMsg = cMsg + 'Comments enabled. '
           resource['allowComments'] = allowComments
           rev = Revision(c.authuser, comment, resource)
           resource['mainRevision_id'] = rev.r.id
           p = Page(title, c.authuser, resource, comment)
           commit(resource)
           Event('Resource Edited', cMsg, resource, c.authuser)
           h.flash('Changes saved', 'success')
        
        return redirect('/workshop/%s/%s/resource/%s/%s'%(w['urlCode'], urlify(w['url']), code, url))

    @h.login_required
    def addResource(self, id1, id2):
        code = id1
        url = id2
        
        if 'title' in request.params:
            title = request.params['title']
        else: 
            title = False
        if 'comment' in request.params:
            comment = request.params['comment']
        else:
            comment = False
        if 'link' in request.params:
            link = request.params['link']
        else:
            link = False
        if 'allowComments' in request.params:
            allowComments = request.params['allowComments']
        else:
            allowComments = -1

        
        rerror = 0
        rerrorMsg = ''
        if not link or not comment or not title:
            rerror = 1
            rerrorMsg = 'Enter resource title, URL and description.'

        if comment == '' or title == '' or link == '':
            rerror = 1
            rerrorMsg = 'Enter resource title, URL and description.'


        if rerror:
            h.flash(rerrorMsg, 'error')
        else:
            w = getWorkshop(code, urlify(url))
            # make sure link not already submitted
            a = getResourceByLink(link, w)
            if a:
                h.flash('Link already submitted for this issue', 'warning')
                return redirect('/workshop/%s/%s'%(code, url))

            r = Resource(link, title, comment, c.authuser, allowComments, w)
            if 'resources' not in w.keys():
                w['resources'] = r.a.id
            else:
                w['resources'] = w['resources'] + ',' + str(r.a.id)

            w['numResources'] = int(w['numResources']) + 1
            commit(w)

        
        return redirect('/workshop/%s/%s'%(code, url))

    @h.login_required
    def modResource(self, id1, id2, id3, id4):
        workshopCode = id1
        workshopURL = id2
        resourceCode = id3
        resourceURL = id4
        
        c.w = getWorkshop(workshopCode, workshopURL)
        
        c.title = c.w['title']
        c.resource = getResource(resourceCode, urlify(resourceURL))
        c.flags = getFlags(c.resource)
        if not c.flags:
           c.resource['numFlags'] = 0
        c.events = getParentEvents(c.resource)

        c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
        c.isAdmin = isAdmin(c.authuser.id)

        c.author = getUserByID(c.resource.owner)
        
        return render('/derived/resource_admin.html')

    @h.login_required
    def modResourceHandler(self):

        workshopCode = request.params['workshopCode']
        workshopURL = request.params['workshopURL']
        w = getWorkshop(workshopCode, workshopURL) 

        resourceCode = request.params['resourceCode']
        resourceURL = request.params['resourceURL']
        r = getResource(resourceCode, resourceURL) 
        
        try:

           if not isAdmin(c.authuser.id) and not isFacilitator(c.authuser.id, w.id):
              h.flash('You are not authorized', 'error')
              return redirect('/workshop/%s/%s/resource/%s/%s'%(w['urlCode'], w['url'], r['urlCode'], r['url']))

           modType = request.params['modType']
           modResourceReason = request.params['modResourceReason']
           verifyModResource = request.params['verifyModResource']
        except:
           "h.flash('All fields required', 'error')"
           alert = {'type':'error'}
           alert['title'] = 'All Fields Required'
           alert['content'] = ''
           "alert['content'] = 'Please check all Required Fields'"
           session['alert'] = alert
           session.save()
           return redirect('/workshop/%s/%s/resource/%s/%s/modResource'%(w['urlCode'], w['url'], r['urlCode'], r['url']))

        # disable or enable the resource, log the event
        if modType == 'disable':
            if r['disabled'] == '0':
               r['disabled'] = True
               modTitle = "Resource Disabled"
            else:
               r['disabled'] = False
               modTitle = "Resource Enabled"
        elif modType == 'delete':
            if r['deleted'] == '0':
                r['disabled'] = False
                r['deleted'] = True
                modTitle = "Resource Deleted"


        commit(r)
        if modResourceReason == "":
            modResourceReason = "No Reason Given"
        e = Event(modTitle, modResourceReason, r, c.authuser)

        h.flash(modTitle, 'success')
        return redirect('/workshop/%s/%s/resource/%s/%s'%(w['urlCode'], w['url'], r['urlCode'], r['url']))

    @h.login_required
    def noteResourceHandler(self):

        workshopCode = request.params['workshopCode']
        workshopURL = request.params['workshopURL']
        w = getWorkshop(workshopCode, workshopURL) 
        
        resourceCode = request.params['resourceCode']
        resourceURL = request.params['resourceURL']
        r = getResource(resourceCode, resourceURL) 
        
        try:

           if not isAdmin(c.authuser.id) and not isFacilitator(c.authuser.id, w.id):
              h.flash('You are not authorized', 'error')
              return redirect('/workshop/%s/%s/resource/%s/%s'%(w['urlCode'], w['url'], r['urlCode'], r['url']))

           noteResourceText = request.params['noteResourceText']
        except:
           h.flash('All fields required', 'error')
           return redirect('/workshop/%s/%s/resource/%s/%s'%(w['urlCode'], w['url'], r['urlCode'], r['url']))

        e = Event("Note Added", noteResourceText, r, c.authuser)

        h.flash("Note Saved", 'success')
        return redirect('/workshop/%s/%s/resource/%s/%s'%(w['urlCode'], w['url'], r['urlCode'], r['url']))



    @h.login_required
    def handler(self, id1, id2):
        code = id1
        url = id2
        
        linkURL = request.params['url']
        comment = request.params['data']
        title = request.params['title']
        
        w = getWorkshop(code, url)
        a = getResourceByLink(linkURL, w)

        if a:
            h.flash('Link already submitted for this issue', 'warning')
            return redirect('/workshop/%s/%s'%(code, url))

        a = Resource(linkURL, title, comment, c.authuser, w)
        
        if 'resources' not in w.keys():
            w['resources'] = a.a.id
        else:
            w['resources'] = w['resources'] + ',' + str(a.a.id)
        
        w['numResources'] = int(w['numResources']) + 1
        commit(w)
        return redirect('/workshop/%s/%s'%(code, url))

    @h.login_required
    ## Deprecated CCN
    def readThis(self):
        if readThisPage(c.authuser.id, request.params['articleID'], 'article'):
            h.flash("You have read this article!", "success")
        else:
            h.flash("You have already read this article!", "warning")
        a = getResource(request.params['articleID'])
        i = getIssueByID(request.params['issueID'])
        return redirect('/issue/%s/resource/%s'%(i.page.url, a.title))

    @h.login_required
    def flagResource(self, id1):
        resourceID = id1
        resource = getResourceByID(resourceID)
        if not resource:
            return json.dumps({'id':resourceID, 'result':'ERROR'})
        if not isFlagged(resource, c.authuser):
            f = Flag(resource, c.authuser)
            return json.dumps({'id':resourceID, 'result':"Successfully flagged!"})
        else:
            return json.dumps({'id':resourceID, 'result':"Already flagged!"})


