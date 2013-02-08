import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.goal         as goalLib
import simplejson                   as json

from pylowiki.lib.base import BaseController, render

log = logging.getLogger(__name__)

class GoalsController(BaseController):

    def __before__(self, action, workshopCode = None):
        if 'user' not in session:
            abort(404)
        if workshopCode is None:
            abort(404)
        c.w = workshopLib.getWorkshopByCode(workshopCode)
        if not c.w:
            abort(404)
        workshopLib.setWorkshopPrivs(c.w)
        if not c.privs['admin'] and not c.privs['facilitator']:
            abort(404)

    def add(self, workshopCode, workshopURL):
        payload = json.loads(request.body)
        if 'title' not in payload:
            abort(404)
        title = payload['title'].strip()
        status = u'0' # as in 0 percent.  Binary at the moment...either 0 or 100.
        goal = goalLib.Goal(title, status, c.w, c.authuser)
        response.content_type = 'text/plain'
        response.status_int = 200
        return
    
    def edit(self, workshopCode, workshopURL, goalCode):
        return "hi"