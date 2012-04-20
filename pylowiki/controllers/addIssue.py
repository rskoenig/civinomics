import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render
from pylowiki.lib.images import saveImage, resizeImage
from pylowiki.lib.utils import urlify
from pylowiki.lib.comments import addDiscussion

#from pylowiki.model import Revision, Page, Event, commit, get_user, getAllSpheres, GovtSphere, Issue, getIssueByID
from pylowiki.lib.db.user import get_user
from pylowiki.lib.db.revision import Revision
from pylowiki.lib.db.page import Page, getPageByID
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.govtSphere import getAllSpheres, GovtSphere
from pylowiki.lib.db.workshop import Workshop, getWorkshopByID
#from pylowiki.model import Slideshow, getPageByID, Article
from pylowiki.lib.db.slideshow import Slideshow

import pylowiki.lib.helpers as h
from time import time
from hashlib import md5

log = logging.getLogger(__name__)

class AddissueController(BaseController):

    @h.login_required
    def index(self):
        if c.authuser['accessLevel'] >= 100:
        #if self._checkAccess(100):
            #return render('/derived/createIssue.mako')
            c.title = "Create Workshop"
            c.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            c.days = range(1, 32)
            c.years = range(2011, 2021)
            c.maxSlideshowEntries = 10
            if getAllSpheres():
                c.governmentSpheres = []
                for item in getAllSpheres():
                    entry = {}
                    entry['id'] = item.id
                    entry['name'] = item['name']
                    c.governmentSpheres.append(entry)
            else:
                c.governmentSpheres = []
            return render('/derived/issue_create.html')
        else:
            h.flash("You are not authorized to view that page", "warning")
            return redirect('/')

    def _checkAccess(self, level):
        if h.accessLevel(level):
            return True
        else:
            h.flash("You are not authorized to view that page", "warning")
            try:
                return redirect(session['return_to'])
            except:
                return redirect('/')

    @h.login_required
    def addIssue(self):
        # Rewrite to use the Workshop constructor, instead of making a page and an issue separately
        if c.authuser['accessLevel'] >= 100:
            try:
                request.params['submit']
                url = request.params['issue_url']
                url = urlify(url)
                
                
                p = Page(url, 'issue', c.authuser.id)
                p.title = request.params['issue_url']
                u = get_user(session['user'])
                r = Revision(request.params['textarea'])

                e = Event('create issue', request.params.get('remark', None))
                p.events.append(e)
                u.events.append(e)
                r.event = e
                p.revisions.append(r)

                if p.url == "" or r.data == "":
                    h.flash("Page was not created.  Please fill all fields.", "warning")
                elif commit(e):
                    h.flash("The issue was created!", "success")
                    return redirect('/issue/' + str(p.url))
                else:
                    h.flash("Page was not created. URL or title might be in use.", "warning")
            except KeyError:
                h.flash("Do not attempt to access a handler directly", "error")
            return redirect('/addIssue/index')
        else:
            h.flash("You are not authorized to view that page", "warning")
            return redirect('/')

    # Todd's editing function?  Check if new page was created on editing
    @h.login_required
    def handler(self):
        if c.authuser['accessLevel'] >= 100:
            try:
                #request.params['submit']
                """
                if request.params['newGovtSphereName']:
                    newGovtSphereName = request.params['newGovtSphereName']
                    photo = request.POST['newGovtSpherePhoto']
                    try:
                        #hash = md5("%s%f"%(photo.filename, time())).hexdigest()
                        #saveImage(photo.filename, hash, photo.file, 'govtSphere')
                        #resizeImage(photo.filename, hash, 40, 40, 'thumbnail', 'govtSphere')
                        image = saveImage(c.authuser, photo.file, photo.filename)
                        image = resizeImage(c.authuser, image, 40, 40)
                        
                    except: #No photo for the government sphere
                        hash = 'earth'
                    gS = GovtSphere(newGovtSphereName, hash)
                    if not commit(gS):
                        h.flash("Government Sphere not created", "warning")
                    else:
                        govtSphere = gS.id
                else:
                    govtSphere = request.params['governmentSpheres']
                """
                issueName = request.params['issueName']
                issueName = urlify(issueName)
                
                p = Page(issueName, 'issue', c.authuser.id)
                #p.title = request.params['issueName']
                p.title = issueName
                u = get_user(session['user'])
                r = Revision(request.params['backgroundWiki'])

                e = Event('create issue', 'Added issue %s' %issueName[:50] )
                p.events.append(e)
                u.events.append(e)
                r.event = e
                p.revisions.append(r)
                #issue = Issue(issueName, p.id)

                """ Set the end date for the suggestion phase """
                if request.params['suggestionMonth']:
                    month = request.params['suggestionMonth']
                else:
                    month = '0'
                if request.params['suggestionDay']:
                    day = request.params['suggestionDay']
                else:
                    day = '0'
                if request.params['suggestionYear']:
                    year = request.params['suggestionYear']
                else:
                    year = '0'
                suggestionEnd = "%s/%s/%s" %(month, day, year)

                """ Set the end date for the solution phase """
                if request.params['solutionMonth']:
                    month = request.params['solutionMonth']
                else:
                    month = '0'
                if request.params['solutionDay']:
                    day = request.params['solutionDay']
                else:
                    day = '0'
                if request.params['solutionYear']:
                    year = request.params['solutionYear']
                else:
                    year = '0'
                solutionEnd = "%s/%s/%s" %(month, day, year)

                """ Set the end date for the solution package phase """
                if request.params['solutionPkgMonth']:
                    month = request.params['solutionPkgMonth']
                else:
                    month = '0'
                if request.params['solutionPkgDay']:
                    day = request.params['solutionPkgDay']
                else:
                    day = '0'
                if request.params['solutionPkgYear']:
                    year = request.params['solutionPkgYear']
                else:
                    year = '0'
                solPkgEnd = "%s/%s/%s" %(month, day, year)
                
                if p.url == "" or r.data == "":
                    h.flash("Page was not created.  Please fill all fields.", "warning")
                elif commit(e):
                    i = Issue(issueName, p.id)
                    discussion = addDiscussion('wikiDiscussion')
                    i.mainDiscussion = discussion
                    discussion.events.append(e)
                    u.issues.append(i)
                    p.issue = i
                    i.govtSphere = govtSphere
                    if request.params['goals']:
                        i.goals = request.params['goals']
                    i.suggestionEnd = suggestionEnd
                    i.solutionEnd = solutionEnd
                    i.solPkgEnd = solPkgEnd
                    a = Article(p.url, issueName)
                    a.pending = False
                    a.type = 'background'
                    i.articles.append(a)
                    i.events.append(e)

                    if commit(i):
                        c.numSlideshowEntries = request.params['numSlideshowEntries']
                        c.title = 'Add Slideshow'
                        session['issueID'] = i.id
                        #h.flash("The issue was created!", "success")
                        #return redirect('/issue/' + str(p.url))
                        return render('/derived/addSlideshow.html')
                    else:
                        h.flash("Background wiki created, issue information was not", "warning")
                else:
                    h.flash("Page was not created. URL or title might be in use.", "warning")
            except KeyError:
                h.flash("Do not attempt to access a handler directly", "error")
            return redirect('/addIssue/index')
        else:
            h.flash("You are not authorized to view that page", "warning")
            return redirect('/')

    @h.login_required
    def slideshow(self):
        numEntries = int(session['numEntries'])
        issueID = session['issueID']
        issue = getIssueByID(issueID)
        slideIDs = []
        for i in range(1, numEntries):
            thisImage = request.POST['image%d'%i]
            thisCaption = request.params['caption%d'%i]
            thisTitle = request.params['title%d'%i]
            
            try:
                hash = md5("%s%f"%(thisImage.filename, time())).hexdigest()
                """ The slideshow """
                saveImage(thisImage.filename, hash, thisImage.file, 'slideshow')
                resizeImage(thisImage.filename, hash, 835, 550, 'slideshow', 'slideshow')

                """ Thumbnail images """
                resizeImage(thisImage.filename, hash, 120, 65, 'thumbnail', 'slideshow')
            except: 
                """ No image uploaded """
                hash = 'mountain'
            
            s = Slideshow(hash, thisCaption, thisTitle)
            issue.slideshow.append(s)
            """
            if issue.slideshowOrder == None:
                issue.slideshowOrder = ''
            else:
                issue.slideshowOrder += ',%d' %s.id
            """
            try:
                commit(s)
                slideIDs.append(s.id)
            except:
                log.info('Failed to commit slideshow with caption %s' % thisCaption)

        issue.slideshowOrder = ','.join(map(str, slideIDs))
        p = getPageByID(issue.pageID)
        return redirect('/issue/%s'%p.url)
