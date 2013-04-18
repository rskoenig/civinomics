from pylowiki.tests import *
import logging
log = logging.getLogger(__name__)
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
    
    def test_index(self):
        response = self.app.get(url(controller='search', action='index'))
        # Test response...
