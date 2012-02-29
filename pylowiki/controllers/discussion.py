import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from pylowiki.lib.base import BaseController, render
from pylowiki.lib.comments import addDiscussion, addComment
from pylowiki.model import get_page

log = logging.getLogger(__name__)

class DiscussionController(BaseController):

    def index(self, id):
        c.p = get_page(id)
        c.i = c.p.issue
        return render('/derived/discussion.html')
