from pylowiki.tests import *

class TestSurveyController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='survey', action='index'))
        # Test response...
