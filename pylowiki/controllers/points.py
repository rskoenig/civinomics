import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from pylowiki.lib.base import BaseController, render

log = logging.getLogger(__name__)

class PointsController(BaseController):

    # Add one point for reading the article
    def readThisArticle(self):
        readArticle(c.authuser.id)
        return render('/derived/wiki.mako')
