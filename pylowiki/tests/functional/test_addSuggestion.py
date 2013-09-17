from pylowiki.tests import *

class TestAddsuggestionController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='addSuggestion', action='index'))
        # Test response...
