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
        if not self.workshop:
            abort(404)
            
        workshopLib.setWorkshopPrivs(self.workshop)
        

    def setWorkshopDemographics(self, workshopCode, workshopURL, demographics):
        self.workshop['demographics'] = demographics
        dbHelpers.commit(self.workshop)
        
    def checkWorkshopDemographics(self, demographics):
        if 'demographics' in self.workshop:
            log.info(self.workshop['demographics'])
            return json.dumps({'statusCode':1, 'required': self.workshop['demographics']})
        else:
            log.info("huh")
            return json.dumps({'statusCode':0, 'error': "Workshop doesn't have demographics"})

                
    def setUserDemographics(self):

        # Will change to POST as soon as I can.
        requestKeys = request.params.keys()
        kwargs = {}
        query = json.loads(request.body)
        log.info(query)
        demographics = ['0','0','0','0','0','0','0','0']

        if 'opt-out' in query:
            demographicsString = "-1"
        else:
            if 'birthday' in query:
                demographics[self.demographicsKeys['birthday']] = query['birthday']
            if 'gender' in query:
                demographics[self.demographicsKeys['gender']] = query['gender']
            if 'ethnicity' in query:
                demographics[self.demographicsKeys['ethnicity']] = query['ethnicity']
            if 'education' in query:
                demographics[self.demographicsKeys['education']] = query['education']
            if 'kids' in query:
                demographics[self.demographicsKeys['kids']] = query['kids']
            if 'house' in query:
                demographics[self.demographicsKeys['house']] = query['house']
            if 'income' in query:
                demographics[self.demographicsKeys['income']] = query['income']
            if 'language' in query:
                demographics[self.demographicsKeys['language']] = query['language']
                
            demographicsString = '|'.join(demographics)
        c.authuser['demographics'] = demographicsString
        dbHelpers.commit(c.authuser)
        
        
    def checkUserDemographics(self, workshopCode, workshopURL):
        self.workshop = workshopLib.getWorkshopByCode(workshopCode)
        if 'demographics' not in self.workshop:
            return json.dumps({'statusCode':2, 'error': "Workshop doesn't have demographics"})
        
        if 'demographics' not in c.authuser and 'demographics' in self.workshop:
            c.required_demographics = self.workshop['demographics']
            return json.dumps({'statusCode':0, 'error': "User doesn't have demographics", 'required': self.workshop['demographics']})
        
        
        #I need to change this            
        userDemo = c.authuser['demographics'].split("|")

        if userDemo == '-1':
            return json.dumps({'statusCode':1})
            
        requiredDemos =[]
        for demographic in self.workshop['demographics'].split("|"):
            if userDemo[self.demographicsKeys[demographic]] == '0':
                log.info("missing %s", demographic)
                requiredDemos.append(demographic)
        if len(requiredDemos) > 0:
            return json.dumps({'statusCode':0, 'error': "User doesn't have that demographic", 'required':self.workshop['demographics']})
                     
        return json.dumps({'statusCode':1})
        
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

            
            
            
            
            
            
        