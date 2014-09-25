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

class CriteriaController(BaseController):

    def __before__(self, action, workshopCode = None, worshopURL = None, criteria = None):
        if workshopCode is None:
            abort(404)
        c.w = workshopLib.getWorkshopByCode(workshopCode)
        if not c.w:
            abort(404)
        workshopLib.setWorkshopPrivs(c.w)
       #  
#         if action in ['update', 'delete']:
#             c.goal = goalLib.getGoal(goalCode)
#             if not c.goal:
#                 abort(404)
#             if not c.privs['admin'] and not c.privs['facilitator']:
#                 abort(404)
#         if c.privs['visitor']:
#             if c.w['public_private'] == 'private':
#                 abort(404)
#         elif not c.privs['admin'] and not c.privs['facilitator'] and not c.privs['participant']:
#             abort(404)
    def addToWorkshop(self, workshopCode, workshopURL, criteria):
        log.info(criteria == 0)
        log.info(criteria is 0)
        log.info(criteria == "0")
        log.info(criteria is "0")
        log.info(criteria == '0')
        log.info(criteria is '0')
        if not criteria == "0":
            log.info("I guess I'll have to do something.")
            log.info(criteria.split("|"))
        else:
            log.info("Hell naw. I'm not sure if I want to do anything here")            
    
    
    def _returnGoal(self, goal, done = None):
        if done is None:
            return json.dumps({'title':goal['title'], 'done':goal['status'] == u'100', 'code':goal['urlCode']})
        else:
            return json.dumps({'title':goal['title'], 'done':done, 'code':goal['urlCode']})

    def add(self, workshopCode, workshopURL):
        payload = json.loads(request.body)
        if 'title' not in payload:
            abort(404)
        title = payload['title'].strip()
        status = u'0' # as in 0 percent.  Binary at the moment...either 0 or 100.
        goal = goalLib.Goal(title, status, c.w, c.authuser)
        return self._returnGoal(goal, done = False)
    
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
        if len(title) > 60:
            title = title[:60]
        status = unicode(int(payload['done']) * 100)
        r = revisionLib.Revision(c.authuser, c.goal)
        c.goal['title'] = title
        c.goal['status'] = status
        dbHelpers.commit(c.goal)
        return self._returnGoal(c.goal)
    
    def delete(self, workshopCode, workshopURL, goalCode):
        c.goal['deleted'] = u'1'
        dbHelpers.commit(c.goal)
        return self._returnGoal(c.goal)
    