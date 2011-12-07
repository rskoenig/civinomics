from pylowiki.tests import *

class TestSuggestionController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='suggestion', action='index'))
        # Test response...
