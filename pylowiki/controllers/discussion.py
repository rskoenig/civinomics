import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from pylowiki.lib.base import BaseController, render
from pylowiki.lib.db.workshop import getWorkshop
from pylowiki.lib.utils import urlify

log = logging.getLogger(__name__)

class DiscussionController(BaseController):

    def index(self, id1, id2):
        code = id1
        url = id2
        c.w = getWorkshop(code, urlify(url))
        log.info(c.w)
        return render('/derived/discussionLanding.html')
