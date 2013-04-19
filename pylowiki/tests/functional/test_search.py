from pylowiki.tests import *
import logging
log = logging.getLogger(__name__)

import pylowiki.tests.helpers.registration as registration
import pylowiki.tests.helpers.workshops as workshop
import pylowiki.tests.helpers.authorization as authLib
import pylowiki.tests.helpers.noun_verb_actions as nounAction

import random, string, simplejson as json

class TestSearchController(TestController):

    """
        Here we will be testing each search type (workshops, users, resources, discussions, ideas as of this writing) for functionality and
        for viewing permissions.  
        
        Functionality here means if we add an idea called 'zzyx', then searching for 'zzyx' will yield that idea.
        Probably nothing else, unless the string 'zzyx' also matches other object types.
        
        Viewing permissions mean private workshops and items within private workshops don't show up.  Additionally, unactivated users
        don't show up.
        
        Search responses are JSON-encoded strings.  Following is taken from the search controller:
        
        JSON responses:
            statusCode == 0:    Same as unix exit code (OK)
            statusCode == 1:    No query was submitted
            statusCode == 2:    Query submitted, no results found
            result:             The search result, given there was at least one
    """
    
    def searchPrototype(self, objType, query):
        searchRoutes = {    'workshops':'/search/workshops/',
                            'people':'/search/people/',
                            'resources':'/search/resources/',
                            'discussions':'/search/discussions/',
                            'ideas':'/search/ideas/'}
        
        searchRoute = searchRoutes[objType] + '?searchQuery=' + query
        #response = self.app.get(searchRoute)
        return self.app.post_json(searchRoute)
    
    def searchWorkshop(self):
        return self.searchPrototype('workshops', 'test')
        
    def allTests(self):
        seededValues = self._seedDB()
        searchTypeMapping = {   'usernames': 'people',
                                'workshopTitles': 'workshops',
                                'resourceTitles': 'resources',
                                'resourceTexts': 'resources',
                                'ideaTitles': 'ideas',
                                'discussionTitles': 'discussions',
                                'discussionTexts': 'discussions'}
        for key in seededValues.keys():
            searchType = searchTypeMapping[key]
            for value in seededValues[key]:
                response = self.searchPrototype(searchType, value)
                if response.status_int == 200:
                    statusCode = json.loads(response.body)
                    if statusCode != 0:
                        return False
                else:
                    return False
        return True
    
    def _seedDB(self):
        # One user per workshop
        numUsers = 3
        usernames = [self._generateString(10) for i in range(numUsers)]
        workshopTitles = [self._generateString(20).strip() for i in range(numUsers)]
        resourceTitles = [self._generateString(20).strip() for i in range(numUsers)]
        resourceTexts = [self._generateString(200).strip() for i in range(numUsers)]
        ideaTitles = [self._generateString(20).strip() for i in range(numUsers)]
        ideaTexts = [self._generateString(20).strip() for i in range(numUsers)]
        discussionTitles = [self._generateString(20).strip() for i in range(numUsers)]
        discussionTexts = [self._generateString(200).strip() for i in range(numUsers)]
        
        for i in range(numUsers):
            thisUser = registration.create_and_activate_a_user(self, postal='95060', name=usernames[i])
            thisWorkshop = workshop.create_new_workshop(self, thisUser, title=workshopTitles[i])
            
            objType = 'resource'
            resource = nounAction.addNounToWorkshop(
                self, 
                objType, 
                thisWorkshop, 
                title=resourceTitles[i],
                text=resourceTexts[i]
            )
            
            objType = 'idea'
            resource = nounAction.addNounToWorkshop(
                self, 
                objType, 
                thisWorkshop, 
                title=ideaTitles[i],
                text=ideaTexts[i]
            )
            
            objType = 'conversation'
            resource = nounAction.addNounToWorkshop(
                self, 
                objType, 
                thisWorkshop, 
                title=discussionTitles[i],
                text=discussionTexts[i]
            )
            
            authLib.logout(self)
        return {'usernames' : usernames,
                'workshopTitles': workshopTitles,
                'resourceTitles': resourceTitles,
                'resourceTexts': resourceTexts,
                'ideaTitles': ideaTitles,
                'discussionTitles': discussionTitles,
                'discussionTexts': discussionTexts}
    
    def _generateString(self, length, spacing = .1):
        """
            Inputs:
                length      ->  An integer - how long the string should be.
                spacing     ->  A float - determines how often spaces are inserted.  Values within [0,1]
        """
        str = ''
        source = string.digits + string.ascii_letters
        for i in range(length):
            space = random.uniform(0, 1)
            if space > spacing:
                index = random.randint(0, len(source) - 1)
                str += source[index]
            else:
                str += ' '
        return str
    
    def test_index(self):
        response = self.app.get(url(controller='search', action='index'))
        # Test response...
