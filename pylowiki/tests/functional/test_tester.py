from pylowiki.tests import *

class TestTesterController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='tester', action='index'))
        # Test response...
