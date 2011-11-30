from pylowiki.tests import *

class TestAddissueController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='addIssue', action='index'))
        # Test response...
