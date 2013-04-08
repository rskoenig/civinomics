import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from pylowiki.lib.base import BaseController, render

from pylowiki.model import getPoints, get_user, addPoints

log = logging.getLogger(__name__)

class TesterController(BaseController):

    def index(self):
        ##return render('/derived/test.html')
        return "<img src = '/images/avatars/%s.profile'>" %(c.authuser.pictureHash)

    def addMyPoints(self):
        addPoints(c.authuser.id, 1)
        return render('/derived/test.html')

    def getMyPoints(self):
        user = get_user(session['user'])
        pointsObj = getPoints(user.id)
        return "%s" % pointsObj.points

    def checkbox(self):
        return render('/derived/test2.html')

    def checkboxHandler(self):
        try:
            request.params['hideBirth']
            return '1'
        except:
            return '0'
