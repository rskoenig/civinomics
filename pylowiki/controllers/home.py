import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

import pylowiki.lib.helpers as h
from pylowiki.model import get_user, getPoints, getUserSuggestions, getArticlesRead, getVotes
from pylowiki.model import getSolutions, getUserContributions, getUserConnections, getUserWork

from pylowiki.lib.base import BaseController, render

log = logging.getLogger(__name__)

class HomeController(BaseController):

    def index(self):
        """
        if session.get('user'):
            reST = r.data

            reSTlist = self.get_reSTlist(reST)
            HTMLlist = self.get_HTMLlist(reST)

            c.wikilist = zip(HTMLlist, reSTlist)
            return render('/base/template.html')
        """
        if session.get('user'):
            #return render('/derived/issuehome.html')
            return redirect('/issues')
        else:
            return render('/derived/splash.html')

    @h.login_required
    def mainPage(self, id):
        c.user = get_user(id)
        c.user.pointsObj = getPoints(c.user.id)
        c.user.suggestions = getUserSuggestions(c.user)
        c.user.articles = getArticlesRead(c.user)
        c.user.votes = getVotes(c.user)
        c.user.solutions = getSolutions(c.user) # Offending line: truncated incorrect double type
        c.user.contributions = getUserContributions(c.user)
        c.user.connectionList = getUserConnections(c.user)
        education = getUserWork(c.user.id, 'school')

        if education:
            c.user.education = education
        else:
            c.user.education = None
        work = getUserWork(c.user.id, 'work')
        if work:
            c.user.work = work
        else:
            c.user.work = None
        if c.user.pointsObj.solutions == None:
            c.user.numSuggestions = 0
        else:
            c.user.numSuggestions = len(c.user.pointsObj.solutions.split(','))

        if c.user.pointsObj.articles == None:
            c.user.numArticles = 0
        else:
            c.user.numArticles = len(c.user.pointsObj.articles.split(','))

        if c.user.pointsObj.votes == None:
            c.user.numVotes = 0
        else:
            c.user.numVotes = len(c.user.pointsObj.votes.split(','))

        if c.user.pointsObj.solutions == None:
            c.user.numSolutions = 0
        else:
            c.user.numSolutions = len(c.user.pointsObj.solutions.split(','))

        if c.user.pointsObj.contributions == None:
            c.user.numContributions = 0
        else:
            c.user.numContributions = len(c.user.pointsObj.contributions.split(','))

        if c.user.connections == None:
            c.user.numConnections = 0
        else:
            c.user.numConnections = len(c.user.connections.split(','))

        c.title = c.user.name
        return render('/derived/profile.html')
