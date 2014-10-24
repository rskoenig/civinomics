import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylowiki.lib.base import BaseController, render
from pylons.controllers.util    import abort, redirect

import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.goal         as goalLib
import pylowiki.lib.db.revision     as revisionLib
import pylowiki.lib.db.dbHelpers    as dbHelpers
import simplejson                   as json
import pylowiki.lib.db.idea         as ideaLib
import pylowiki.lib.db.rating       as ratingLib
import pylowiki.lib.db.initiative   as initiativeLib


log = logging.getLogger(__name__)

class CriteriaController(BaseController):

    def __before__(self, action, workshopCode = None, worshopURL = None, criteria = None, thingCode = None, rating = None):
        if workshopCode is None:
            log.info("wC is none")
            return json.dumps({'statusCode': 0})

        self.workshopCrit = workshopLib.getWorkshopByCode(workshopCode)
        if not self.workshopCrit:
            log.info("cant get that workshop")
            return json.dumps({'statusCode': 0})

            #but is it broken?
        workshopLib.setWorkshopPrivs(self.workshopCrit)
        if action in ['rateCriteria']:
            if not criteria:
                log.info("Trying to rate nothing")
                abort(404)
            if criteria not in self.workshopCrit['rating_criteria']:
                log.info("Wrong criteria for thing")
                return json.dumps({'statusCode': 0})
          
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
        c.ratingConfig = 0
        if criteria != '0':
            criteriaList = criteria.split("|")
            self.workshopCrit['rating_criteria'] = criteria
            dbHelpers.commit(self.workshopCrit)
            c.ratingConfig = 1
            return json.dumps({'statusCode':1, 'criteria': criteriaList})
        else:
            c.ratingConfig = 1
            if 'rating_criteria' in self.workshopCrit:
                self.workshopCrit['rating_criteria'] = ""
                dbHelpers.commit(self.workshopCrit)
        log.info(c.ratingConfig)
        returnURL = '/workshop/%s/%s/preferences'%(workshopCode, workshopURL)
        log.info(returnURL)
        return redirect(returnURL)    
    
    def getWorkshopCriteria(self, workshopCode, thingCode):
        # This function returns the criteria related to the workshop
        # In case there's none, it should return false? 
        if 'rating_criteria' in self.workshopCrit:
            criteriaList = []
            for criteria in self.workshopCrit['rating_criteria'].split("|"):
                thing = ideaLib.getIdea(thingCode)
                if not thing:
                    thing = initiativeLib.getInitiative(thingCode)
                rating = ratingLib.getCriteriaRatingForThingUser(c.authuser, thing, criteria)
                if not rating:
                    userRat = '0'
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
        if not thing:
            thing = initiativeLib.getInitiative(thingCode)
        ratingObj = ratingLib.makeOrChangeRating(thing, c.authuser, rating, 'criteria', criteria = criteria)
        if ratingObj:
            return json.dumps({'statusCode':1})
    
    def getRatingForCriteria(self, workshopCode, criteria, thingCode):
        thing = ideaLib.getIdea(thingCode)
        if not thing:
            thing = initiativeLib.getInitiative(thingCode)
        result = ratingLib.getCriteriaRatingForThing(workshopCode, thing, criteria)
        if len(result) == 0:
            amount = 0  
            numVotes = 0
        else:
            sumVotes = 0
            numVotes  = len(result)
            for vote in result:
                sumVotes += int(vote['amount'])
            amount = int(sumVotes/numVotes)
           # log.info("%s %s", sumVotes, numVotes)
        return [amount, numVotes]