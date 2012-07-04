import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from pylowiki.lib.base import BaseController, render

from pylowiki.model import get_page, getUserByID, getNumRatingsForSuggestion

log = logging.getLogger(__name__)

class LeaderboardController(BaseController):

    """ Renders the leaderboard page for a given issue.  Takes in the issue URL as the id argument. """
    def index(self, id):
        p = get_page(id)
        c.i = p.issue
        return render('/derived/leaderboard.html')
