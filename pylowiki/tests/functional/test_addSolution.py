from pylowiki.tests import *

class TestAddsolutionController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='addSolution', action='index'))
        # Test response...
