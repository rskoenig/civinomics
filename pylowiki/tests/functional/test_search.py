from pylowiki.tests import *
import logging
log = logging.getLogger(__name__)

import pylowiki.tests.helpers.registration as registration
import pylowiki.tests.helpers.workshops as workshop

import random, string

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
        response = self.app.get(searchRoute)
        log.debug('Search query was %s, response was %s' %(query, response))
    
    def searchWorkshop(self):
        return self.searchPrototype('workshops', 'test')
        
    def allTests(self):
        thisUser = registration.create_and_activate_a_user(self, postal='95864', name=self._generateString(10))
        thisWorkshop = workshop.create_new_workshop(self, thisUser, title=self._generateString(20))
    
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
                index = random.randint(0, length - 1)
                str += source[index]
            else:
                str += ' '
        return str
    
    def test_index(self):
        response = self.app.get(url(controller='search', action='index'))
        # Test response...
