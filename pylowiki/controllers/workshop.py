import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from pylowiki.lib.db.workshop import Workshop, getWorkshop
from pylowiki.lib.db.revision import Revision

from pylowiki.lib.base import BaseController, render

log = logging.getLogger(__name__)

class WorkshopController(BaseController):

    def addWorkshop(self):
        if c.authuser['accessLevel'] >= 100:
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

    def addWorkshopHandler(self):
        workshopName = request.params['workshopName']
        goals = request.params['goals']
        day = request.params['workshopDay']
        month = request.params['workshopMonth']
        year = request.params['workshopYear']
        backgroundWiki = request.params['backgroundWiki']
        c.numSlideshowEntries = request.params['numSlideshowEntries']
        
        w = Workshop(workshopName, c.authuser, day, month, year, backgroundWiki, goals)
        #r = Revision(c.authuser, backgroundWiki)
        c.workshop_id = w.w.id # TEST
        c.title = 'Add slideshow'
        return render('/derived/addSlideshow.html')
    
    def display(self, id1, id2):
        code = id1
        url = id2
        
        c.w = getWorkshop(code, url)
        c.title = c.w['title']
        
        c.slides = []
        slide_ids = [int(item) for item in c.w['slideshow_order'].split(',')]
        
        
        return render('/derived/issuehome.html')
