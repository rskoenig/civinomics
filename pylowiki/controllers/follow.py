import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
import pylowiki.lib.helpers as h
from pylowiki.lib.base import BaseController, render
import pylowiki.lib.db.generic as generic
import pylowiki.lib.db.follow as followLib

log = logging.getLogger(__name__)

class FollowController(BaseController):
    
    @h.login_required
    def followHandler(self, code):
        try:
            thing = generic.getThing(code)
        except:
            abort(404)
        f = followLib.FollowOrUnfollow(c.authuser, thing)
        return "ok"