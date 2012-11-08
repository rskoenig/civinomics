import logging, pickle

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, redirect
import webhelpers.paginate as paginate

from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.event import Event, getParentEvents
from pylowiki.lib.base import BaseController, render
from pylowiki.lib.db.workshop import getWorkshop, isScoped
from pylowiki.lib.db.discussion import getActiveDiscussionsForWorkshop, getDeletedDiscussionsForWorkshop, getDisabledDiscussionsForWorkshop, getDiscussions, getDiscussion, getDiscussionByID
from pylowiki.lib.utils import urlify
from pylowiki.lib.db.user import isAdmin, getUserByID
from pylowiki.lib.db.event import getParentEvents
from pylowiki.lib.db.facilitator import isFacilitator, getFacilitatorsByWorkshop
from pylowiki.lib.db.flag import Flag, isFlagged, getFlags, clearFlags
from pylowiki.lib.db.rating import getRatingByID
from pylowiki.lib.db.revision import Revision, getRevisionByCode, getParentRevisions
from pylowiki.lib.sort import sortBinaryByTopPop, sortContByAvgTop

from pylowiki.lib.db.discussion import Discussion

import pylowiki.lib.helpers as h
import simplejson as json

log = logging.getLogger(__name__)

class DiscussionController(BaseController):

    ##@h.login_required
    def index(self, id1, id2):
        workshopCode = id1
        workshopURL = id2
        c.w = getWorkshop(workshopCode, urlify(workshopURL))
        if c.w['public_private'] != 'public':
            if 'user' not in session or not isScoped(c.authuser, c.w):
                    return render('/derived/404.bootstrap')

        c.rating = False
        if 'user' in session:
            c.isScoped = isScoped(c.authuser, c.w)
            c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
            c.isAdmin = isAdmin(c.authuser.id)
            if 'ratedThings_workshop_overall' in c.authuser.keys():
                workRateDict = pickle.loads(str(c.authuser['ratedThings_workshop_overall']))
                if c.w.id in workRateDict.keys():
                    c.rating = getRatingByID(workRateDict[c.w.id])
        else:
            c.isScoped = False
            c.isFacilitator = False
            c.isAdmin = False

        fList = []
        for f in (getFacilitatorsByWorkshop(c.w.id)):
           if 'pending' in f and f['pending'] == '0' and f['disabled'] == '0':
              fList.append(f)

        c.facilitators = fList


        log.info(c.w)
        c.title = c.w['title']
        c.code = c.w['urlCode']
        c.url = c.w['url']
        c.discussions = getActiveDiscussionsForWorkshop(workshopCode, urlify(workshopURL), 'general')
        c.discussions = sortBinaryByTopPop(c.discussions)
        if not c.discussions:
            c.discussions = []
        disabledDiscussions = getDisabledDiscussionsForWorkshop(workshopCode, urlify(workshopURL), 'general')
        if disabledDiscussions:
            c.discussions += disabledDiscussions
        deletedDiscussions = getDeletedDiscussionsForWorkshop(workshopCode, urlify(workshopURL), 'general')
        if deletedDiscussions:
            c.discussions += deletedDiscussions
        

        c.count = len(c.discussions)
        c.paginator = paginate.Page(
            c.discussions, page=int(request.params.get('page', 1)),
            items_per_page = 15, item_count = c.count
        )

        return render('/derived/discussion_landing.bootstrap')

    def topic(self, id1, id2, id3, id4, id5 = ''):
        workshopCode = id1
        workshopUrl = id2
        discussionCode = id3
        discussionUrl = id4
        revisionURL = id5
        
        c.w = getWorkshop(workshopCode, urlify(workshopUrl))
        if c.w['public_private'] != 'public':
            if 'user' not in session or not isScoped(c.authuser, c.w):
                return render('/derived/404.bootstrap')

        if 'user' in session:
            c.isScoped = isScoped(c.authuser, c.w)
            c.isAdmin = isAdmin(c.authuser.id)
            c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
        else:
            c.isScoped = False
            c.isAdmin = False
            c.isFacilitator = False

        c.discussion = getDiscussion(discussionCode, urlify(discussionUrl))
        c.flags = getFlags(c.discussion)
        c.events = getParentEvents(c.discussion)
        c.otherDiscussions = getActiveDiscussionsForWorkshop(workshopCode, urlify(workshopUrl))
        if 'disabled' in c.discussion and 'deleted' in c.discussion:
            if c.discussion['disabled'] == '0' and c.discussion['deleted'] == '0':
                c.otherDiscussions.remove(c.discussion)

        c.title = c.w['title']

        if revisionURL != '':
            r = getRevisionByCode(revisionURL)
            c.content = h.literal(h.reST2HTML(r['data']))
            c.lastmoduser = getUserByID(r.owner)
            c.lastmoddate = r.date
            c.revision = r
        else:
            c.content = h.literal(h.reST2HTML(c.discussion['text']))
            c.revision = False
            c.lastmoduser = getUserByID(c.discussion.owner)
            if 'mainRevision_id' in c.discussion:
                r = get_revision(int(c.discussion['mainRevision_id']))
                c.lastmoddate = r.date
            else:
                c.lastmoddate = c.discussion.date

        c.revisions = getParentRevisions(c.discussion.id)

        return render('/derived/discussion_topic.bootstrap')

    @h.login_required
    def addDiscussion(self, id1, id2):
        code = id1
        url = id2

        c.w = getWorkshop(code, urlify(url))
        if 'user' in session:
            c.isScoped = isScoped(c.authuser, c.w)
            c.isAdmin = isAdmin(c.authuser.id)
            c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
        else:
            c.isScoped = False
            c.isAdmin = False
            c.isFacilitator = False
        
        if c.isScoped or c.isAdmin or c.isFacilitator:
            c.title = c.w['title']
            return render('/derived/discussion_edit.bootstrap')
        else:
            return redirect('/workshop/%s/%s' % (c.w['urlCode'], c.w['url']))

    @h.login_required
    def clearDiscussionFlagsHandler(self, id1, id2):
        code = id1
        url = id2


        clearError = 0
        clearMessage = ""
        c.discussion = getDiscussion(code, urlify(url))
        c.w = getWorkshop(c.discussion['workshopCode'], urlify(c.discussion['workshopURL']))
        if 'user' in session:
            c.isScoped = isScoped(c.authuser, c.w)
            c.isAdmin = isAdmin(c.authuser.id)
            c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
        else:
            c.isScoped = False
            c.isAdmin = False
            c.isFacilitator = False

        if not c.isScoped and not c.isAdmin and not c.isFacilitator:
            return redirect('/workshop/%s/%s' % (c.w['urlCode'], c.w['url']))

        if 'clearDiscussionFlagsReason' in request.params:
            clearReason = request.params['clearDiscussionFlagsReason']
            if clearReason != '':
                clearFlags(c.discussion)
                clearTitle = "Flags cleared"
                e = Event(clearTitle, clearReason, c.discussion, c.authuser)
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
            clearMessage = "Flags cleared from this discussion"
            alert = {'type':'success'}
            alert['title'] = 'Flags cleared!'
            alert['content'] = clearMessage
            session['alert'] = alert
            session.save()

        returnURL = "/adminDiscussion/" + code + "/" + url
        return redirect(returnURL)

    @h.login_required
    def newDiscussionHandler(self, id1, id2):
        code = id1
        url = id2
        w = getWorkshop(code, urlify(url))
        if 'user' in session:
            c.isScoped = isScoped(c.authuser, w)
            c.isAdmin = isAdmin(c.authuser.id)
            c.isFacilitator = isFacilitator(c.authuser.id, w.id)
        else:
            c.isScoped = False
            c.isAdmin = False
            c.isFacilitator = False

        if not c.isScoped and not c.isAdmin and not c.isFacilitator:
            return redirect('/workshop/%s/%s' % (w['urlCode'], w['url']))

        
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
            d = Discussion(owner = c.authuser, discType = 'general', attachedThing = w, title = title, text = text)
            r = Revision(c.authuser, text, d.d)
            commit(w)
        
        return redirect('/workshop/%s/%s/discussion/%s/%s' % (code, url, d.d['urlCode'], d.d['url']))
    
    @h.login_required
    def editDiscussion(self, id1, id2):
        code = id1
        url = id2
        c.discussion = getDiscussion(code, urlify(url))
        c.w = getWorkshop(c.discussion['workshopCode'], urlify(c.discussion['workshopURL']))
        if 'user' in session:
            c.isAdmin = isAdmin(c.authuser.id)
            c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
        else:
            c.isAdmin = False
            c.isFacilitator = False

        if (c.discussion.owner != c.authuser.id)  and not c.isAdmin and not c.isFacilitator:
            return redirect('/workshop/%s/%s' % (c.w['urlCode'], c.w['url']))

        return render('/derived/discussion_edit.bootstrap')
        
    @h.login_required
    def editDiscussionHandler(self, id1, id2):
        code = id1
        url = id2
        discussion = getDiscussion(code, urlify(url))
        w = getWorkshop(discussion['workshopCode'], discussion['workshopURL'])
        if 'user' in session:
            c.isAdmin = isAdmin(c.authuser.id)
            c.isFacilitator = isFacilitator(c.authuser.id, w.id)
        else:
            c.isAdmin = False
            c.isFacilitator = False

        if (discussion.owner != c.authuser.id)  and not c.isAdmin and not c.isFacilitator:
            return redirect('/workshop/%s/%s' % (w['urlCode'], w['url']))
        
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
            dMsg = ''
            if discussion['title'] != title:
                discussion['title'] = title
                dMsg = dMsg + "Title updated. "

            if discussion['text'] != text:
                discussion['text'] = text
                dMsg = dMsg + "Text updated. "
                r = Revision(c.authuser, text, discussion)

            Event('Discussion Edited', dMsg, discussion, c.authuser)
            commit(discussion)
        
        return redirect('/workshop/%s/%s/discussion/%s/%s' % (w['urlCode'], w['url'], discussion['urlCode'], discussion['url']))
    
    @h.login_required
    def flagDiscussion(self, id1, id2):
        code = id1
        url = id2
        discussion = getDiscussion(code, urlify(url))
        c.w = getWorkshop(discussion['workshopCode'], urlify(discussion['workshopURL']))
        if 'user' in session:
            c.isScoped = isScoped(c.authuser, c.w)
            c.isAdmin = isAdmin(c.authuser.id)
            c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
        else:
            c.isScoped = False
            c.isAdmin = False
            c.isFacilitator = False

        if not c.isScoped and not c.isAdmin and not c.isFacilitator:
            return redirect('/workshop/%s/%s/discussion/%s/%s' % (c.w['urlCode'], c.w['url'], discussion['urlCode'], discussion['url']))

        if not discussion:
            return json.dumps({'id':discussion.id, 'result':'ERROR'})
        if not isFlagged(discussion, c.authuser):
            f = Flag(discussion, c.authuser)
            return json.dumps({'id':discussion.id, 'result':"Successfully flagged!"})
        else:
            return json.dumps({'id':discussion.id, 'result':"Already flagged!"})

    @h.login_required
    def adminDiscussion(self, id1, id2):
        code = id1
        url = id2
        c.discussion = getDiscussion(code, urlify(url))
        c.w = getWorkshop(c.discussion['workshopCode'], urlify(c.discussion['workshopURL']))
        if 'user' in session:
            c.isAdmin = isAdmin(c.authuser.id)
            c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
        else:
            c.isAdmin = False
            c.isFacilitator = False

        if not c.isAdmin and not c.isFacilitator:
            return redirect('/workshop/%s/%s/discussion/%s/%s' % (c.w['urlCode'], c.w['url'], c.discussion['urlCode'], c.discussion['url']))

        
        return render('/derived/discussion_admin.bootstrap')

    @h.login_required
    def adminDiscussionHandler(self):
        
        workshopCode = request.params['workshopCode']
        workshopURL = request.params['workshopURL']
        w = getWorkshop(workshopCode, workshopURL) 

        discussionCode = request.params['discussionCode']
        discussionURL = request.params['discussionURL']
        d = getDiscussion(discussionCode, discussionURL)
        ##log.info("BEFORE")
                
        try:

           if not isAdmin(c.authuser.id) and not isFacilitator(c.authuser.id, w.id):
              return redirect('/workshop/%s/%s/discussion/%s/%s'%(w['urlCode'], w['url'], d['urlCode'], d['url']))
           ##log.info("HMMMM")
           modType = request.params['modType']
           ##log.info("1")
           verifyModDiscussion = request.params['verifyModDiscussion']
           ##log.info("2")
           modDiscussionReason = request.params['modDiscussionReason']
           ##log.info("3")
           ##log.info("HERE")
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
               d['disabled'] = '1'
               modTitle = "Discussion Disabled"
            else:
               d['disabled'] = '0'
               modTitle = "Discussion Enabled"
        elif modType == 'delete':
            if d['deleted'] == '0':
                d['disabled'] = '0'
                d['deleted'] = '1'
                modTitle = "Discussion Deleted"


        commit(d)
        if modDiscussionReason == "":
            modDiscussionReason = "No Reason Given"
        e = Event(modTitle, modDiscussionReason, d, c.authuser)

        alert = {'type':'success'}
        alert['title'] = modTitle
        alert['content'] = ''
        session['alert'] = alert
        session.save()

        if modType == 'deleted':
            return redirect('/workshop/%s/%s/discussion/'%(w['urlCode'], w['url']))
        else:
            return redirect('/workshop/%s/%s/discussion/%s/%s'%(w['urlCode'], w['url'], d['urlCode'], d['url']))
            
