from pylowiki.tests import *

class TestFollowController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='follow', action='index'))
        # Test response...
