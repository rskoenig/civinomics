import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylowiki.lib.base import BaseController, render

import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.goal         as goalLib
import pylowiki.lib.db.revision     as revisionLib
import pylowiki.lib.db.dbHelpers    as dbHelpers
import simplejson                   as json
import pylowiki.lib.db.idea         as ideaLib
import pylowiki.lib.db.rating       as ratingLib

log = logging.getLogger(__name__)

class CriteriaController(BaseController):

    def __before__(self, action, workshopCode = None, worshopURL = None, criteria = None, thingCode = None, rating = None):
        if workshopCode is None:
            abort(404)
        c.w = workshopLib.getWorkshopByCode(workshopCode)
        if not c.w:
            abort(404)
        workshopLib.setWorkshopPrivs(c.w)
        if action in ['rateCriteria']:
            if not criteria:
                log.info("Trying to rate nothing")
                abort(404)
            if criteria not in c.w['rating_criteria']:
                log.info("Wrong criteria for thing")
                abort(404)
          
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
        if not criteria == '0':
            log.info("I guess I'll have to do something.")
            log.info(criteria.split("|"))
            criteriaList = criteria.split("|")
            c.w['rating_criteria'] = criteria
            dbHelpers.commit(c.w)
        else:
            log.info("Hell naw. I'm not sure if I want to do anything here")            
    
    def getWorkshopCriteria(self, workshopCode, workshopURL):
        # This function returns the criteria related to the workshop
        # In case there's none, it should return false? 
        log.info("")
    
    #Make this workshop dependent?
    def rateCriteria(self, criteria, thingCode, rating):
        log.info("empty")
        thing = ideaLib.getIdea(code)
        ratingObj = ratingLib.makeOrChangeRating(thing, c.authuser, rating, ratingType, criteria = criteria)
    
    def getRatingForCriteria(self, criteria, thingCode):
        lo.info("")   
    