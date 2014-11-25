from pylowiki.tests import *

class TestPointsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='points', action='index'))
        # Test response...
