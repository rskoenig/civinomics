import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylowiki.lib.base import BaseController, render

import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.dbHelpers    as dbHelpers
import simplejson                   as json
import pylowiki.lib.db.user         as userLib

log = logging.getLogger(__name__)

#
# Things needed this controller:
# A dictionary with the different types of demographics (that needs to be accessed by every instance)
# 
# Demographic format: string
# birthday|gender|ethnicity|education|kids|income|language 
#
# Workshop model
# birthday|gender|kids
# (list with the ones that are needed)
#
# Operating with demographics
# Demographics: "Pipenized" list in user field
# Accessing a demographic: Split string - using demographicKeys to access
# Checking if a workshop wants it: String with bools
# Rendering the values for each demographic...? Angular, Front End
# 
# Methods
# Set workshop demographics (for workshop)
#   Input: workshopcode, workshopurl, string with desired obligatory demographics
#   Output: None - sets workshop['demographics']
#   (This way, if 'demographics' in workshop)
#
# Check workshop demographics (do we need to ask the user? is this necessary in the back end? having it won't hurt)
#   Input: workshopcode, workshopurl, string with demographics to check if obligatory
#   Output: JSON stauts 1/0 depending on the result (+errors?)
#
# Set user demographics (Shouldn't I check what demographics the workshop requieres too, or I let the front end handle that?)
#   Input: form dictionary with the values, user in context
#   Output: None - build string and save in user
#
# Check user demographics (as this isn't really independent from whatever the workshop needs, we'll have to check it against it)
#   Input: workshopcode, workshopurl, user in context
#   Output: JSON stauts 1/0 depending on the result (+errors?)
#

class DemographicsController(BaseController):

    def __before__(self, action, workshopCode = None, worshopURL = None, userCode = None, demographics = None):
        self.demographicsKeys = {
            'birthday' : 0,
            'gender': 1,
            'ethnicity': 2,
            'education': 3,
            'kids': 4,
            'house': 5,
            'income': 6,
            'language': 7,
        }
        
        if workshopCode is None:
            abort(404)
        if demographics is None:
            return False
            
        self.workshop = workshopLib.getWorkshopByCode(workshopCode)
        if not self.workshopCrit:
            abort(404)
            
        workshopLib.setWorkshopPrivs(self.workshop)
        

    def setWorkshopDemographics(self, workshopCode, workshopURL, demographics):
        log.info("Setting workshop demographics - we override every time as we suppose that the previous ones have been handled properly")
        self.workshop['demographics'] = demographics
        dbHelpers.commit(self.workshop)
        
    def checkWorkshopDemographics(self, demographics):
        log.info("Checking to see if the workshop has the required demographics")
        if 'demographics' in self.workshop:
            if demographics == self.workshop['demographics']:
                return json.dumps({'statusCode':1})
            else:
                return json.dumps({'statusCode':0, 'error': "Different demographics"})
        else:
            return json.dumps({'statusCode':0, 'error': "Workshop doesn't have demographics"})

            
        log.info("Do something")
        
    def setUserDemographics(self):
        log.info("Setting the user's demographics")
        requestKeys = request.params.keys()
        kwargs = {}
        query = request.POST
        
        demographics = []
        
        if 'birthday' in query:
            demograpics[demograpicsKeys['birthday']] = query['birthday']
        if 'gender' in query:
            demograpics[demograpicsKeys['gender']] = query['gender']
        if 'ethnicity' in query:
            demograpics[demograpicsKeys['ethnicity']] = query['ethnicity']
        if 'education' in query:
            demograpics[demograpicsKeys['education']] = query['education']
        if 'kids' in query:
            demograpics[demograpicsKeys['kids']] = query['kids']
        if 'house' in query:
            demograpics[demograpicsKeys['house']] = query['house']
        if 'income' in query:
            demograpics[demograpicsKeys['income']] = query['income']
        if 'language' in query:
            demograpics[demograpicsKeys['language']] = query['language']
            
        demographicsString = demographicsArrayToString(demographics)
        
        c.authuser['demographics'] = demographicsString
        dbHelpers.commit(c.authuser)
        
        
    def checkUserDemographics(self, workshopCode, workshopURL):
        log.info("Checking if the user has the demographics required by the workshop")
        
        
    #Helper function to convert from array to string
    def demographicsArrayToString(self, demographicsArray):
        demographicsString = ""
        index = 0
        for demographicKey in self.demographicsKeys[:-1]:
            if demographicKey in demographicsArray:
                demographicsString += demographicsArray[demographicKey] + "|"
            else:
                demographicsString += "0|"
        
        if 'language' in demographicsArray:
                demographicsString += demographicsArray[7]
            else:
                demographicsString += "0"
                
        return demographicsString

            
            
            
            
            
            
        