from pylowiki.tests import *

class TestRatingController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='rating', action='index'))
        # Test response...
