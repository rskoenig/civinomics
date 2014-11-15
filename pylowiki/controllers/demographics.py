import logging
import csv

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylowiki.lib.base import BaseController, render
# from collections import Counter

import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.dbHelpers    as dbHelpers
import simplejson                   as json
import pylowiki.lib.db.user         as userLib
import collections


log = logging.getLogger(__name__)

#
# Things needed this controller:
# A dictionary with the different types of demographics (that needs to be accessed by every instance)
# 
# Demographic format: string
# birthday|gender|ethnicity|education|kids|income|language|residential|multifamily|peoplehousehold
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

def writeCsv(data, path):
    with open(path, "wb") as csvFile:
        writer = csv.writer(csvFile, delimiter=';')
        for line in data:
            log.info("line is %s", line)
            writer.writerow(line)

def parseUserDemo(user, demo):
    try:
        demographicsKeys = {
                'birthday' : 0,
                'gender': 1,
                'ethnicity': 2,
                'education': 3,
                'kids': 4,
                'house': 5,
                'income': 6,
                'language': 7,
                'residential': 8,
                'multifamily': 9,
                'peoplehousehold': 10
        }
        userDemo = user['demographics'].split('|')
        if userDemo[demographicsKeys[demo]] != '0':
            return userDemo[demographicsKeys[demo]]
    except:
        pass
        
def dictionarize(listing):
    result = {}
    for item in listing:
        if item in result:
            result[item] += 1
        else:
            result[item] = 1
    return result
        
def listize(d):
    result = []
    for key, value in d.iteritems():
        result.append(key)
        result.append(value)
    return result


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
            'residential': 8,
            'multifamily': 9,
            'peoplehousehold': 10
        }
        
        if workshopCode is None:
            abort(404)
        if demographics is None:
            return False
            
        self.workshop = workshopLib.getWorkshopByCode(workshopCode)
        if not self.workshop:
            abort(404)
            
        workshopLib.setWorkshopPrivs(self.workshop)
        

    def exportCsv(self, workshopCode):
        workshop = workshopLib.getWorkshopByCode(workshopCode)
        if 'demographics' not in workshop:
            log.info('no demographics')

        demographicsList = workshop['demographics'].split('|')
        allUsersWithDemo = userLib.getAllUsersWithDemographics()

        demoData = []
        for demoname in demographicsList:
                demoRaw = [parseUserDemo(u, demoname) for u in allUsersWithDemo if parseUserDemo(u, demoname)]
                demo = dictionarize(demoRaw)
                demoData.append(demoname)
                demoData.append([[k,v] for k,v in demo.iteritems()])
                log.info(demo.items())
        path = "pylowiki/public/temp/" + workshopCode + ".csv"
        writeCsv(demoData, path)
#         validDemoList = [parseUserDemo(u, demographicsList) for u in allUsersWithDemo if parseUserDemo(u, demographicsList)]
#         log.info(validDemoList)
#         path = "pylowiki/public/temp/" + workshopCode + ".csv"
         
        
        
    

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
        if 'demographics' not in c.authuser:
            demographics = ['0','0','0','0','0','0','0','0','0','0','0']
        else:
            demographics = c.authuser['demographics'].split("|")
            while len(demographics) < 11:
                demographics.append('0')

        if query['optout'] == 'True':
            log.info(query['optout'])
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
            if 'residential' in query:
                demographics[self.demographicsKeys['residential']] = query['residential']
            if 'multifamily' in query:
                demographics[self.demographicsKeys['multifamily']] = query['multifamily']
            if 'peoplehousehold' in query:
                demographics[self.demographicsKeys['peoplehousehold']] = query['peoplehousehold']
                
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
        log.info(userDemo[0] == '-1')
        if userDemo[0] == '-1':
            log.info("opted out")
            return json.dumps({'statusCode':1})
            
        requiredDemos =[]
        for demographic in self.workshop['demographics'].split("|"):
            if len(userDemo) < self.demographicsKeys[demographic]+1:
                requiredDemos.append(demographic)
            else:
                if userDemo[self.demographicsKeys[demographic]] == '0' :
                    log.info("missing %s", demographic)
                    requiredDemos.append(demographic)
        if len(requiredDemos) > 0:
            return json.dumps({'statusCode':0, 'error': "User doesn't have that demographic", 'required':self.workshop['demographics']})
        
        log.info("all ok")
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

            
            
            
            
            
            
        