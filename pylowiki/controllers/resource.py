import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from pylowiki.lib.db.user import get_user, getUserByID, isAdmin
from pylowiki.lib.db.facilitator import isFacilitator
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.workshop import getWorkshop, getWorkshopByID, isScoped
from pylowiki.lib.db.event import Event, getParentEvents
from pylowiki.lib.db.resource import Resource, getResource, getResourceByLink, getResourcesByWorkshopID, getActiveResourcesByWorkshopID, getResourceByID, getResource, getActiveResourcesByParentID
from pylowiki.lib.db.suggestion import getSuggestion, getSuggestionByID
from pylowiki.lib.db.discussion import getDiscussionByID
from pylowiki.lib.db.rating import getRatingByID
from pylowiki.lib.db.flag import Flag, isFlagged, checkFlagged, getFlags, clearFlags
from pylowiki.lib.db.page import Page, getPageByID, get_page
from pylowiki.lib.db.revision import Revision, get_revision, getRevisionByCode, getParentRevisions

from pylowiki.lib.utils import urlify

from pylowiki.lib.base import BaseController, render
import pickle

#from pylowiki.lib.points import readThisPage

import pylowiki.lib.helpers as h
import simplejson as json

log = logging.getLogger(__name__)

class ResourceController(BaseController):

    def index(self, id1, id2, id3, id4, id5 = ''):
        workshopCode = id1
        workshopURL = id2
        resourceCode = id3
        resourceURL = id4
        revisionURL = id5
    
        
        c.w = getWorkshop(workshopCode, workshopURL)
        c.title = c.w['title']
        c.resource = getResource(resourceCode, urlify(resourceURL))
        if c.resource['parent_id'] != None and c.resource['parent_type'] != None:
            if c.resource['parent_type'] == 'suggestion':
                c.suggestion = getSuggestionByID(c.resource['parent_id'])

        c.events = getParentEvents(c.resource)
        if c.resource['disabled'] == '1' or c.resource['allowComments'] == '0':
            c.commentsDisabled = 1
        else:
            c.commentsDisabled = 0

        if revisionURL != '':
            rev = getRevisionByCode(revisionURL)
            c.content = h.literal(h.reST2HTML(rev['data']))
            c.lastmoduser = getUserByID(rev.owner)
        else:
            c.content = h.literal(h.reST2HTML(c.resource['comment']))
            c.lastmoduser = getUserByID(c.resource.owner)
            if 'mainRevision_id' in c.resource:
                r = get_revision(int(c.resource['mainRevision_id']))
                c.lastmoddate = r.date
            else:
                c.lastmoddate = c.resource.date

        c.revisions = getParentRevisions(c.resource.id)

        c.flagged = False
        if checkFlagged(c.resource):
           c.flagged = True

        if 'user' in session:
            c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
            c.isAdmin = isAdmin(c.authuser.id)
            c.isScoped = isScoped(c.authuser, c.w)
            c.allowComments = c.resource['allowComments']

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
            c.isScoped = False
            c.allowComments = False

        c.poster = getUserByID(c.resource.owner)
        
        if c.suggestion:
            c.resources = getActiveResourcesByParentID(c.suggestion.id)
        else:
            c.resources = getActiveResourcesByWorkshopID(c.w.id)
        for i in range(len(c.resources)):
            resource = c.resources[i]
            if resource.id == c.resource.id:
                c.resources.pop(i)
                break
        c.discussion = getDiscussionByID(int(c.resource['discussion_id']))
        
        return render('/derived/resource.bootstrap')

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
            c.heading = "OTHER RESOURCES"
            c.resources = getResourcesByWorkshopID(c.w.id)

            return render('/derived/resource_edit.bootstrap')
        else:
            h.flash('You are not authorized', 'error')
            return redirect('/workshop/%s/%s'%(c.w['urlCode'], urlify(c.w['url'])))

    @h.login_required
    def newSResource(self, id1, id2):
        code = id1
        url = id2

        c.s = getSuggestion(code, urlify(url))
        c.w = getWorkshop(c.s['workshopCode'], urlify(c.s['workshopURL']))

        c.isAdmin = isAdmin(c.authuser.id)
        c.isFacilitator =  isFacilitator(c.authuser.id, c.w.id)
        c.isScoped = isScoped(c.authuser, c.w)
        if (c.isScoped and c.w['allowResources'] == '1') or c.isAdmin or c.isFacilitator:
            c.r = False
            c.resources = getActiveResourcesByParentID(c.s.id)

            return render('/derived/resource_edit.bootstrap')
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

            return render('/derived/resource_edit.bootstrap')
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
        if not title or title == '':
            rerror = 1
            rerrorMsg = rerrorMsg + 'Resource title required.'

        if not comment or comment == '':
            rerror = 1
            rerrorMsg = rerrorMsg + 'Resource description required.'

        if not link or link == '':
            rerror = 1
            rerrorMsg = rerrorMsg + 'Resource link required.'

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
            alert = {'type':'error'}
            alert['title'] = "Error."
            alert['content'] = rerrorMsg
            session['alert'] = alert
            session.save()
            return redirect('/editResource/%s/%s'%(code, url))
        else:
           cMsg = 'Edits: '
           if resource['title'] != title:
              cMsg = 'Title updated. '
           resource['title'] = title
           if resource['link'] != link:
              cMsg = cMsg + 'Link updated. '
           resource['link'] = link
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
           alert = {'type':'success'}
           alert['title'] = "Resource edited."
           alert['content'] = "Resource updated, thanks!"
           session['alert'] = alert
           session.save()

        
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

        if 'suggestionCode' in request.params and 'suggestionURL' in request.params:
            suggestionCode = request.params['suggestionCode']
            suggestionURL = request.params['suggestionCode']
            s = getSuggestion(suggestionCode, suggestionURL)
        else:
            s = False

        rerror = 0
        rerrorMsg = ''
        if not title or title == '':
            rerror = 1
            rerrorMsg = rerrorMsg + 'Resource title required.'

        if not link or link == '':
            rerror = 1
            rerrorMsg = rerrorMsg + ' Resource link required.'

        if not comment or comment == '':
            rerror = 1
            rerrorMsg = rerrorMsg + ' Resource comment required.'

        if rerror:
            alert = {'type':'error'}
            alert['title'] = "Error."
            alert['content'] = rerrorMsg
            session['alert'] = alert
            session.save()
            c.s = s
            c.resourceTitle = title
            c.resourceComment = comment
            c.resourceLink = link
            c.resourceAllowComments = allowComments
            c.w = getWorkshop(code, urlify(url))
            c.r = False
            c.heading = "OTHER RESOURCES"
            c.resources = getResourcesByWorkshopID(c.w.id)

            return render('/derived/resource_edit.bootstrap')

        else:
            w = getWorkshop(code, urlify(url))

            # make sure link not already submitted
            if s:
                a = getResourceByLink(link, s)
            else:
                a = getResourceByLink(link, w)

            log.info('a is %s link is %s' % (a, link))

            if a:
                alert = {'type':'error'}
                alert['title'] = "Error."
                if s:
                    alert['content'] = 'Link already submitted for this suggestion.'
                else:
                    alert['content'] = 'Link already submitted for this workshop.'
                session['alert'] = alert
                session.save()
                if s:
                    return redirect('/workshop/%s/%s/suggestion/%s/%s'%(code, url, s['urlCode'], s['url']))
                else:
                    return redirect('/workshop/%s/%s'%(code, url))

            if s:
                r = Resource(link, title, comment, c.authuser, allowComments, w, s)
                alert = {'type':'success'}
                alert['title'] = 'Resource added.'
                alert['content'] = 'Thanks for the new information resource!'
                session['alert'] = alert
                session.save()

                return redirect('/workshop/%s/%s/suggestion/%s/%s'%(code, url, suggestionCode, suggestionURL))
            else:
                r = Resource(link, title, comment, c.authuser, allowComments, w)
                alert = {'type':'success'}
                alert['title'] = 'Resource added.'
                alert['content'] = 'Thanks for the new information resource!'
                session['alert'] = alert
                session.save()
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
        
        return render('/derived/resource_admin.bootstrap')

    @h.login_required
    def clearResourceFlagsHandler(self, id1, id2):
        code = id1
        url = id2
        c.resource = getResource(code, urlify(url))
        c.author = getUserByID(c.resource.owner)
        c.w = getWorkshopByID(c.resource['workshop_id'])
        clearError = 0
        clearMessage = ""

        if 'clearResourceFlagsReason' in request.params:
            clearReason = request.params['clearResourceFlagsReason']
            if clearReason != '':
                clearFlags(c.resource)
                clearTitle = "Flags cleared"
                e = Event(clearTitle, clearReason, c.resource, c.authuser)
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
            clearMessage = "Flags cleared from this resource"
            alert = {'type':'success'}
            alert['title'] = 'Flags cleared!'
            alert['content'] = clearMessage
            session['alert'] = alert
            session.save()

        returnURL = "/workshop/" + c.w['urlCode'] + "/" + c.w['url'] + "/resource/" + c.resource['urlCode'] + "/" + c.resource['url'] + "/modResource"
        return redirect(returnURL)

        
        c.flags = getFlags(c.resource)
        if not c.flags:
           c.resource['numFlags'] = 0
        c.events = getParentEvents(c.resource)

        c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
        c.isAdmin = isAdmin(c.authuser.id)

        c.author = getUserByID(c.resource.owner)
        
        return render('/derived/resource_admin.bootstrap')

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
               r['disabled'] = '1'
               modTitle = "Resource Disabled"
            else:
               r['disabled'] = '0'
               modTitle = "Resource Enabled"
        elif modType == 'delete':
            if r['deleted'] == '0':
                r['disabled'] = '0'
                r['deleted'] = '1'
                modTitle = "Resource Deleted"


        commit(r)
        if modResourceReason == "":
            modResourceReason = "No Reason Given"
        e = Event(modTitle, modResourceReason, r, c.authuser)

        h.flash(modTitle, 'success')
        if modType == 'delete':
            return redirect('/workshop/%s/%s/resource/'%(w['urlCode'], w['url']))
        else:
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
    def flagResource(self, id1, id2):
        code = id1
        url = id2
        resource = getResource(code, urlify(url))
        resourceID = resource.id
        if not resource:
            return json.dumps({'id':resourceID, 'result':'ERROR'})
        if not isFlagged(resource, c.authuser):
            f = Flag(resource, c.authuser)
            return json.dumps({'id':resourceID, 'result':"Successfully flagged!"})
        else:
            return json.dumps({'id':resourceID, 'result':"Already flagged!"})


