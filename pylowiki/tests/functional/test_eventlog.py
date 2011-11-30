from pylowiki.tests import *

class TestEventlogController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='eventlog', action='index'))
        # Test response...
