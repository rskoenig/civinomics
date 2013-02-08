import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.goal         as goalLib
import pylowiki.lib.db.revision     as revisionLib
import pylowiki.lib.db.dbHelpers    as dbHelpers

import simplejson                   as json
from pylowiki.lib.base import BaseController, render

log = logging.getLogger(__name__)

class GoalsController(BaseController):

    def __before__(self, action, workshopCode = None, goalCode = None):
        if 'user' not in session:
            abort(404)
        if workshopCode is None:
            abort(404)
        c.w = workshopLib.getWorkshopByCode(workshopCode)
        if not c.w:
            abort(404)
        workshopLib.setWorkshopPrivs(c.w)
        
        if action in ['update']:
            c.goal = goalLib.getGoal(goalCode)
            if not c.goal:
                abort(404)
        if not c.privs['admin'] and not c.privs['facilitator']:
            abort(404)

    def add(self, workshopCode, workshopURL):
        payload = json.loads(request.body)
        if 'title' not in payload:
            abort(404)
        title = payload['title'].strip()
        status = u'0' # as in 0 percent.  Binary at the moment...either 0 or 100.
        goal = goalLib.Goal(title, status, c.w, c.authuser)
        return json.dumps({'title':goal['title'], 'done':False, 'code':goal['urlCode']})
    
    def getGoals(self, workshopCode, workshopURL):
        goals = goalLib.getGoalsForWorkshop(c.w)
        goalsList = []
        for goal in goals:
            goalsList.append({'title': goal['title'], 'done': goal['status'] == u'100', 'code':goal['urlCode']})
        return json.dumps(goalsList)
    
    def update(self, workshopCode, workshopURL, goalCode):
        payload = json.loads(request.body)
        if 'title' not in payload or 'done' not in payload:
            abort(404)
        title = payload['title'].strip()    
        status = unicode(int(payload['done']) * 100)
        r = revisionLib.Revision(c.authuser, c.goal)
        c.goal['title'] = title
        c.goal['status'] = status
        dbHelpers.commit(c.goal)
        return
    
    