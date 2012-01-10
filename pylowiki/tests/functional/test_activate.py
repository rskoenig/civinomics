from pylowiki.tests import *

class TestActivateController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='activate', action='index'))
        # Test response...
