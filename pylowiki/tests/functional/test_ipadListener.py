from pylowiki.tests import *

class TestIpadlistenerController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='ipadListener', action='index'))
        # Test response...
