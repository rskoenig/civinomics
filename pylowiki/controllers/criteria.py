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
        self.workshopCrit = workshopLib.getWorkshopByCode(workshopCode)
        if not self.workshopCrit:
            abort(404)
            #but is it broken?
        workshopLib.setWorkshopPrivs(self.workshopCrit)
        if action in ['rateCriteria']:
            if not criteria:
                log.info("Trying to rate nothing")
                abort(404)
            if criteria not in self.workshopCrit['rating_criteria']:
                log.info("Wrong criteria for thing")
                abort(404)
          
#         if action in ['update', 'delete']:
#             c.goal = goalLib.getGoal(goalCode)
#             if not c.goal:
#                 abort(404)
#             if not c.privs['admin'] and not c.privs['facilitator']:
#                 abort(404)
#         if c.privs['visitor']:
#             if workshopCrit['public_private'] == 'private':
#                 abort(404)
#         elif not c.privs['admin'] and not c.privs['facilitator'] and not c.privs['participant']:
#             abort(404)

    def addToWorkshop(self, workshopCode, workshopURL, criteria):
        if not criteria == '0':
            criteriaList = criteria.split("|")
            self.workshopCrit['rating_criteria'] = criteria
            dbHelpers.commit(self.workshopCrit)
        else:
            log.info("Hell naw. I'm not sure if I want to do anything here")            
    
    def getWorkshopCriteria(self, workshopCode, thingCode):
        # This function returns the criteria related to the workshop
        # In case there's none, it should return false? 
        if 'rating_criteria' in self.workshopCrit:
            criteriaList = []
            for criteria in self.workshopCrit['rating_criteria'].split("|"):
                thing = ideaLib.getIdea(thingCode)
                rating = ratingLib.getCriteriaRatingForThingUser(c.authuser, thing, criteria)
                if not rating:
                    userRat = 0
                else:
                    userRat = rating['amount']
                amount = self.getRatingForCriteria(workshopCode, criteria, thingCode)
                criteriaFull = {'criteria':criteria, 'average': amount[0], 'numVotes':amount[1], 'amount': userRat}
                criteriaList.append(criteriaFull)
            return json.dumps({'statusCode':1, 'criteria': criteriaList})
        else:
            return json.dumps({'statusCode': 0})
    
    #Make this workshop dependent?
    def rateCriteria(self, criteria, thingCode, rating):
        thing = ideaLib.getIdea(thingCode)
        ratingObj = ratingLib.makeOrChangeRating(thing, c.authuser, rating, 'criteria', criteria = criteria)
        if ratingObj:
            return json.dumps({'statusCode':1})
    
    def getRatingForCriteria(self, workshopCode, criteria, thingCode):
        thing = ideaLib.getIdea(thingCode)
        result = ratingLib.getCriteriaRatingForThing(workshopCode, thing, criteria)
        if len(result) == 0:
            return 0  
        else:
            sumVotes = 0
            numVotes  = len(result)
            for vote in result:
                sumVotes += int(vote['amount'])
            amount = int(sumVotes/numVotes)
           # log.info("%s %s", sumVotes, numVotes)
            return [amount, numVotes]