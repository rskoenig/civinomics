from pylowiki.tests import *

class TestGoalsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='goals', action='index'))
        # Test response...
